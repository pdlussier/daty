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

class Query:
    def __init__(self):
        self.what = None
        self.vars = []
        self.triples = []


class Wikidata:
    def __init__(self, verbose=True):
        self.verbose = verbose
        site = Site('wikidata', 'wikidata')
        self.repo = site.data_repository()
        self.triples = []
        self.what = None
        self.vars = []

    def selfcheck(self):
        pprint(self.triples)
        return all(not any(t == 0 for t in triple) for triple in self.triples)

    def select(self, what, triples):
        query = """SELECT what WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          triples
        }
        """
        line = ""
        for triple in triples:
            lines = line + triple['s'] + " " + triple['p'] + " " + triple['o'] + ".\n"     
        query = sub('triples', lines, query)
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
