#!/usr/bin/env python3

#    Wikidata Editor: wikidata library
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from bleach import clean
from bs4 import BeautifulSoup
from os import mkdir
from pprint import pprint
from pywikibot import ItemPage, Site
from pywikibot.data.sparql import SparqlQuery
from re import sub
from requests import get
import pickle

def save(variable, path):
    """Save variable on given path using Pickle
    
    Args:
        variable: what to save
        path (str): path of the output
    """
    with open(path, 'wb') as f:
        pickle.dump(variable, f)
    f.close()

def load(path):
    """Load variable from Pickle file
    
    Args:
        path (str): path of the file to load

    Returns:
        variable read from path
    """
    with open(path, 'rb') as f:
        variable = pickle.load(f)
    f.close()
    return variable

class Wikidata:
    def __init__(self, verbose=True):
        self.verbose = verbose
        site = Site('wikidata', 'wikidata')
        self.repo = site.data_repository()
        self.sparql_vars = []
        self.vars = []

    def select(self, what, subject, property, object):
        query = """SELECT what WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          subject property object.
        }
        """
        query = sub('subject', subject, query)
        query = sub('property', property, query)
        query = sub('object', object, query)
        query = sub('what', what, query)
        sparql = SparqlQuery()
        results = sparql.query(query)['results']['bindings']
        results = list(set([r['subject']['value'].split("/")[-1] for r in results]))
        return results 

    def search(self, query, verbose=False):
        pattern = 'https://www.wikidata.org/w/index.php?search='
        page = get(pattern + query).content
        soup = BeautifulSoup(page, 'html.parser')
        results = []
        try:
            results = soup.find(name='ul', attrs={'class':'mw-search-results'})
            results = results.find_all(name='li', attrs={'class':'mw-search-result'})
            results = [{"URI":r.find(name="span", attrs={'class':'wb-itemlink-id'}).text.split("(")[1].split(")")[0],
                        "Label":clean(r.find(name="span", attrs={'class':'wb-itemlink-label'}).text),
                        "Description":clean(r.find(name='span', attrs={'class':'wb-itemlink-description'}).text)} for r in results]
        except Exception as e:
            results = []
            if verbose:
                print(e)
        if self.verbose:
            pprint(results)
        return results

class WikidataPhysician:
    def __init__(self):
        site = Site('wikidata', 'wikidata')
        self.repo = site.data_repository()

    def get_all(self):
        physician = 'Q39631'

        query = """SELECT ?subclass_of WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          ?subclass_of wdt:P279 wd:Q39631.
        }
        """
        sparql = SparqlQuery()
        results = sparql.query(query)

        physician_types = set([q['subclass_of']['value'].split("/")[-1] for q in results['results']['bindings']])
        physician_types.add(physician)

        physicians = set()

        for t in physician_types:
            query = sub('physician_type', t, """SELECT ?physician WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          ?physician wdt:P106 wd:physician_type.
          ?physician wdt:P31 wd:Q5.
        }
        """)
            sparql = SparqlQuery()
            try:
                results = sparql.query(query)
                results = set([q['physician']['value'].split("/")[-1] for q in results['results']['bindings']])
            except Exception as e:
                pprint(e)
            physicians = physicians.union(results)
        return physicians

    def save_all_to_disk(self):
        physicians = self.get_all()
        save(physicians, 'wikidata_physicians.pkl')


class Physician:
    """Access data from ordinemedicinapoli.it"""
    pattern = "http://www.ordinemedicinapoli.it/scheda_medico.php?id="    

    def __init__(self, id=None):
        self.data_path = 'physicians_order_data'
        if id:
            self.id = str(id)
            try:
                self.data = load(self.data_path + '/' + self.id)
                self.label = (self.data["Name"] + " " + self.data["Surname"]).lower()
            except FileNotFoundError:
                data = self.get_from_order(self.id)
                if data["Name"] == None:
                    print("id not valid")
                else:
                   self.data = data
               

    def get_from_order(self, id):
        """Get physician data from 'ordinemedicinapoli.it' id

        Args:
            id (int): id of the physician on the website
        
        Returns:
            (dict) data on the physician
        """
        page = get(self.pattern + id).content
        soup = BeautifulSoup(page, 'html.parser')
        tds = soup.findAll("td")
        data = []
        print("cacca")
        for el in tds:
            if el.attrs == {}:
               data.append(el.string)
        physician = {"Name":data[0],
                     "Surname":data[1],
                     "Birth date":data[2],
                     "Birth place":data[3],
                     "Albo":data[4], 
                     "Registration code":data[5], 
                     "Degree":data[6], 
                     "Abilitation Year":data[7]}
        return physician

    def get_Q(self, id=None):
        if not id:
            id = self.id
        self.wikidata_physician = WikidataPhysician()
        collisions = []
        for Q in self.wikidata_physician.get_all():
            item = ItemPage(self.wikidata_physician.repo, Q)
            item.get()
            collision = self.name_collision(self.label, item)
            if collision:
                pprint("Name collision with " + Q)
                collisions.append(Q)
            already_existing = self.same_as(item)
            if already_existing:
                print(self.label + " has " + Q)
                self.Q = Q
                break
        if collisions == []:
            print("creating Q")
        if collisions != []:
            return collisions

    def name_collision(self, physician, item):
        if any(item.labels[lang].lower() == physician for lang in item.labels.keys()):
            return True
        else:
            return False

    def same_as(self, item):
        for P in item.claims.keys():
            for claim in item.claims[P]:
                for ref in claim.sources:
                    if 'P854' in ref.keys():
                        for statement in ref['P854']:
                            if "http://www.ordinemedicinapoli.it/scheda_medico.php?id=" + str(self.id) in statement.toJSON()['datavalue']['value']:
                                return statement.toJSON()['datavalue']['value'].split('=')[-1]
                            else:
                                return False

    def save_all_to_disk(self):
        """Save on disk all physicians from 'ordinemedicinapoli.it'"""
        try:
            mkdir('physicians_order_data')
        except FileExistsError as e:
            pass
        i=0
        while True:
            physician = self.get_from_website(i)
            if physician["Name"] != None:
                save(physician, self.data_path + "/" + str(i))
                i = i + 1
            else:
                break

class Importer:

    def __init__(self):
        pass 

    def same_name(self, wikidata_physician, naples_physician):
        item = ItemPage(self.repo, physician)
        item.get()
        if any(item.labels[lang] == naples_physician for lang in item.labels.keys()):
            return True

    def same_as(self, physician):
        item = ItemPage(self.repo, physician)
        item.get()
        for P in item.claims.keys():
            for claim in item.claims[P]:
                for ref in claim.sources:
                    if 'P854' in ref.keys():
                        for statement in ref['P854']:
                            if "http://www.ordinemedicinapoli.it/scheda_medico.php?id=" in statement.toJSON()['datavalue']['value']:
                                return statement.toJSON()['datavalue']['value'].split('=')[-1]
                            else:
                                return False


if __name__ == "__main__":
    Physician().save_all_to_disk()
