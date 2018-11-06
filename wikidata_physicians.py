#!/usr/bin/env python3

#    Wikidata Physician
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


import pickle
from pprint import pprint
from pywikibot import ItemPage, Site
from pywikibot.data.sparql import SparqlQuery
from re import sub

#site = Site('wikidata', 'wikidata')
#repo = site.data_repository()

def save(variable, path):
    """Save variable on given path using Pickle
    
    Args:
        variable: what to save
        path (str): path of the output
    """
    with open(path, 'wb') as f:
        pickle.dump(variable, f)
    f.close()


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

if __name__ == "__main__":
    physician = WikidataPhysician()
    physician.save_all_to_disk()

