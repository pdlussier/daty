#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#    Daty: wikidata library
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
from copy import deepcopy as copy
from os import mkdir
from pprint import pprint
from re import sub
from requests import get

from .config import Config
config = Config()
from pywikibot import ItemPage, PropertyPage, Site
from pywikibot.data.sparql import SparqlQuery
from pywikibot.page import Claim

class Wikidata:
    def __init__(self, verbose=False):
        config = Config()
        self.verbose = verbose
        site = Site('wikidata', 'wikidata')
        self.repo = site.data_repository()
        self.vars = []

    def select(self, var, statements, keep_data=False):
        """Return (select) the set of var that satisfy the statements.

        Args:
            var (dict): its keys can be 'URI' and 'Label';
            statements (list): of double dictionaries of the form:
                role ('s','p','o')
                  var

        Returns:
            (list) of results URI, or query sparql response if "keep_data" is True.
        """
        # We will transform them
        var = copy(var)
        statements = copy(statements)

        # Template
        template = """SELECT var WHERE {
          statements
        }
        """

        # Check that var is in the statements
        if not var in (var for s in statements for role,var in s.items()):
            print("WARNING: var not contained in constraints!")

        # Convert var and statements vars to SPARQL
        var = "?" + var["Label"]

        for s in statements:
            for role in s:
                x = s[role]
                if not "URI" in x.keys() or x["URI"] == "":
                    s[role] = "?" + x["Label"]
                elif role == "o":
                    s[role] = "wd:" + x["URI"]
                elif role == "p":
                    s[role] = "wdt:" + x["URI"]

        # Form the SPARQL statements
        expr = ""
        for s in statements:
            expr = expr.join([s['s'], " ", s['p'], " ", s['o'], ".\n"])

        # Do the query
        query = sub('statements', expr, template)
        query = sub('var', var, query)
        sparql = SparqlQuery()

        # Return results
        if keep_data:
            return sparql.query(query)
        results = sparql.query(query)['results']['bindings']
        results = list(set([r[var[1:]]['value'].split("/")[-1] for r in results]))
        return results 

    def download(self, uri):
        """

        Args:
            id (str): LQP id
        Returns:
            
        """
        if uri.startswith("P"):
            return PropertyPage(self.repo, uri).get()
        if uri.startswith("Q") or uri.startswith("L"):
            return ItemPage(self.repo, uri).get()

    def get_claim(self, claim):
        #from pywikibot.page import Claim
        return claim.toJSON()

    def get_label(self, entity, language='en'):
        try:
            if language in entity['labels'].keys():
                return entity['labels'][language]
            else:
                return ""
        except Exception as e:
            print(e)

    def get_description(self, entity, language='en'):
        try:
            if language in entity['descriptions'].keys():
                return entity['descriptions'][language]
            else:
                return ""
        except Exception as e:
            print(self.wikidata.get_description(entity))
            print(e.traceback)

    def search(self, query, verbose=False):
        """
        
        Args:
            query (str): what to search
        Returns:
            ({"URI":, "Label":, "Description":} in results)
        """
        pattern = 'https://www.wikidata.org/w/index.php?search='
        page = get(pattern + query, timeout=10).content
        soup = BeautifulSoup(page, 'html.parser')
        results = []
        try:
            results = soup.find(name='ul', attrs={'class':'mw-search-results'})
            results = results.find_all(name='li', attrs={'class':'mw-search-result'})
            results = ({"URI":r.find(name="span", attrs={'class':'wb-itemlink-id'}).text.split("(")[1].split(")")[0],
                        "Label":clean(r.find(name="span", attrs={'class':'wb-itemlink-label'}).text),
                        "Description":clean(r.find(name='span', attrs={'class':'wb-itemlink-description'}).text)} for r in results)
        except Exception as e:
            results = []
            if verbose:
                print(e)
        if self.verbose:
            pprint(results)
        return results
