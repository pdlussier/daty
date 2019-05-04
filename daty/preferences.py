# -*- coding: utf-8 -*-

#    Preferences
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import Align, CssProvider, Dialog, Entry, Grid, Label, ListBoxRow, Separator, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION, IconTheme, Template, Window
from pprint import pprint
from pywikibot.data.sparql import SparqlQuery
from re import sub
from threading import Thread

from .config import Config
from .languageadd import LanguageAdd
from .util import set_style
#from .wikidata import Wikidata

name = 'ml.prevete.Daty'

@Template.from_resource("/ml/prevete/Daty/gtk/preferences.ui")
class Preferences(Window):
    __gtype_name__ = "Preferences"


    config = Config()
    credentials = Template.Child("credentials")
    languages = Template.Child("languages")
    #values = Template.Child("values")

    def __init__(self, *args, **kwargs):
        Window.__init__(self, *args, **kwargs)

        icon = lambda x: IconTheme.get_default().load_icon((name), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        self.credentials.set_header_func(self.update_header)
        self.languages.set_header_func(self.update_header)

        for key in self.config.data['credentials']:
            row = ListBoxRow()
            grid = Grid()
            grid.props.column_homogeneous = True
            label = Label()
            label.set_text(key)
            label.props.halign = Align(1)
            context = label.get_style_context()
            resource = "/ml/prevete/Daty/gtk/value.css"
            set_style(context, resource, "dim-label", True)
            entry = Entry()
            entry.set_text(self.config.data['credentials'][key])
            context = entry.get_style_context()
            set_style(context, resource, "flat", True)
            grid.attach(label, 0, 0, 1, 1)
            grid.attach(entry, 1, 0, 2, 1)
            row.add(grid)
            self.credentials.add(row)
        self.credentials.show_all()

        query = """SELECT ?item ?itemLabel ?c
{
  ?item wdt:P424 ?c .
  MINUS{?item wdt:P31/wdt:P279* wd:Q14827288} #exclude Wikimedia projects
  MINUS{?item wdt:P31/wdt:P279* wd:Q17442446} #exclude Wikimedia internal stuff
  SERVICE wikibase:label { bd:serviceParam wikibase:language "your_first_language". }
}
        """

        query = sub("your_first_language", self.config.data['languages'][0], query)
        self.retrieve(query, self.languages_callback)

    @Template.Callback()
    def language_new_clicked_cb(self, widget):
        language_add = LanguageAdd(self.language_results)
        print(language_add)
        language_add.show_all()

    def languages_callback(self, results):
        languages = self.config.data['languages']
        self.language_results = results['results']['bindings']
        for lang in languages:
            for r in self.language_results:
                if r['c']['value'] == lang:
                    row = ListBoxRow()
                    label = Label()
                    label.set_text(r['itemLabel']['value'])
                    label.props.halign = Align(1)
                    row.add(label)
                    self.languages.add(row)
        self.languages.show_all()

    def retrieve(self, query, callback, *cb_args, **kwargs):
        """Asynchronously download entity from wikidata
             Args:
                entity (dict): have keys "URI", "Label", "Description"
        """
        def do_call():
            sparql = SparqlQuery()
            results = sparql.query(query)
            idle_add(lambda: callback(results, *cb_args, **kwargs))
            return None
        thread = Thread(target = do_call)
        thread.start()

    def update_header(self, row, before, *args):
        """See GTK+ Documentation"""
        if before:
            row.set_header(Separator())
