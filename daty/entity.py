# -*- coding: utf-8 -*-

#    Entity
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

#from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
require_version('Gdk', '3.0')
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gdk import EventType, KEY_Escape
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, CssProvider, ListBoxRow, Stack, StyleContext, Template
from pprint import pprint
from threading import Thread
from time import sleep

#from .util import MyThread
from .sidebarentity import SidebarEntity
from .util import download_light, set_text
from .wikidata import Wikidata

@Template.from_resource("/ml/prevete/Daty/gtk/entity.ui")
class Entity(Stack):
    
    __gtype_name__ = "Entity"

    entry = Template.Child("entry")
    label = Template.Child("label")
    unit = Template.Child("unit")

    #wikidata = Wikidata()

    def __init__(self, snak, *args, qualifier=False, css=None, load=None, **kwargs):
        Stack.__init__(self, *args, **kwargs)

        self.load = load

        context = self.get_style_context()
        provider = CssProvider()
        provider.load_from_resource('/ml/prevete/Daty/gtk/entity.css')
        context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION)

        if qualifier:
            self.label.props.valign = 1
            self.unit.props.valign = 1

        try:
            if snak['snaktype'] == 'novalue':
              self.label.set_text("No value")
            if snak['snaktype'] == 'value':
              dv = snak['datavalue']
              dt = snak['datatype']
              if dt == 'wikibase-item' or dt == 'wikibase-property':
                if dv['type'] == 'wikibase-entityid':
                  entity_type = dv['value']['entity-type']
                  numeric_id = dv['value']['numeric-id']
                  if entity_type == 'item':
                    URI = 'Q' + str(numeric_id)
                  if entity_type == 'property':
                    URI = 'P' + str(numeric_id)
                  download_light(URI, self.load_entity)
              if dt == 'url':
                  url = dv['value']
                  label = "".join(["<a href='", url, "'>", url.split('/')[2], '</a>'])
                  #self.label.set_markup(label)
                  self.set_text(label, url)
                  self.label.props.use_markup = True
              if dt == 'quantity':
                  unit = dv['value']['unit']
                  if unit.startswith('http'):
                      unit = dv['value']['unit'].split('/')[-1]
                      download_light(unit, self.on_download_unit)

                  amount = dv['value']['amount']
                  ub = dv['value']['upperBound']
                  lb = dv['value']['lowerBound']
                  if float(amount) > 0:
                      amount = str(round(float(amount)))
                  if ub and lb:
                      amount = amount + " ± " + str(round(float(ub) - float(amount)))
                  if ub and not lb:
                      amount = amount + " + " + str(round(float(ub) - float(amount)))
                  if not ub and lb:
                      amount = amount + " - " + str(round(float(amount) - float(lb)))
                  self.label.set_text(amount)
              if dt == 'string':
                  self.set_text(dv['value'], "Text")
              if dt == 'monolingualtext':
                  #TODO: better implement monolingual text
                  self.set_text(dv['value']['text'], dv['value']['language'])
              if dt == 'commonsMedia':
                  self.set_text(dv['value'], "Picture")
              if dt == 'external-id':
                  self.set_text(dv['value'], "External ID")
              if dt == 'geo-shape':
                  #TODO: implement geo-shape
                  #print('geo-shape')
                  pass
              if dt == 'globe-coordinate':
                  #TODO: implement globe-coordinate
                  #print('globe-coordinate')
                  pass
              if dt == 'tabular-data':
                  #TODO: implement tabular-data
                  #print('tabular-data')
                  pass
              if dt == 'time':
                  #TODO: implement time point
                  #print('time')
                  pass
            del snak

        except Exception as err:
            print(err)
            print(type(err))
            print(err.__traceback__)

        self.entry.connect("search-changed", self.entry_search_changed_cb)

    def set_text(self, label, description):
        set_text(self.label, label, description)
        set_text(self.entry, label, description)

    def on_download_unit(self, URI, unit, error):
        if error:
            print(error)
            print(type(error))
        if unit:
            self.unit.set_text(unit["Label"])
            self.unit.set_visible(True)
            del unit
            return None

    def load_entity(self, URI, entity, error):
        if error:
            print(type(error))
            print(error)
        self.entity = entity
        self.URI = URI
        self.set_text(entity["Label"], entity["Description"])
        self.show_all()
        return None

    @Template.Callback()
    def button_press_event_cb(self, widget, event):
        if event.type == EventType._2BUTTON_PRESS:
            print("double click")   
        elif event.type == EventType.BUTTON_PRESS:
            self.entry.set_visible(True)
            self.set_visible_child_name("entry")
            self.entry.grab_focus()

    @Template.Callback()
    def entry_focus_in_event_cb(self, entry, event):
        entry.props.margin_top = 3
        entry.props.margin_bottom = 3
        label = self.label.get_label()
        description = self.label.get_tooltip_text()
        try:
            from .entitypopover import EntityPopover
            self.entity_popover = EntityPopover(self.entity, parent=self, load=self.load)
            self.search(entry.get_text())
            self.entity_popover.set_visible(True)
        except AttributeError as e:
            print("no popover available for this type of value")

    @Template.Callback()
    def entry_focus_out_event_cb(self, widget, event):
        self.set_visible_child_name("view")
        self.entry.set_visible(False)
        self.entry.props.margin_top = 0
        self.entry.props.margin_bottom = 0
        self.entry.set_text(self.label.get_text())
        try:
            self.entity_popover.hide()
        except AttributeError as e:
            print("this entity has no popover")

    @Template.Callback()
    def entry_key_release_event_cb(self, widget, event):
        try:
            if event.keyval == KEY_Escape:
                self.entry_focus_out_event_cb(widget, event)
        except AttributeError as e:
            print("no entity popover for this value")

    def search(self, query):
        try:
            if query:
                self.entity_popover
                def do_call():
                    results, error = None, None
                    try:
                        wikidata = Wikidata()
                        results = wikidata.search(query)
                        #results = f()
                    except Exception as err:
                        error = err

                    idle_add(lambda: self.on_search_done(results, error))
                thread = Thread(target = do_call)
                thread.start()
            else:
                self.set_search_placeholder(True)
        except AttributeError as e:
            self.set_search_placeholder(True)

    def on_search_done(self, results, error):
        try:
            listbox = self.entity_popover.label_listbox
            listbox.foreach(listbox.remove)
            for r in results:
                if r['URI'] != self.URI:
                    entity = SidebarEntity(r, URI=False)#,
                    row = ListBoxRow()
                    row.add(entity)
                    listbox.add(row)
            listbox.show_all()
            self.set_search_placeholder(False)
        except AttributeError as e:
            print("this value type has no popover")
            raise e

    def set_search_placeholder(self, value):
        try:
            self.entity_popover.search_box.set_visible(value)
            self.entity_popover.results.set_visible(not value)
        except AttributeError as e:
            pass

    def entry_search_changed_cb(self, entry):
        self.search(entry.get_text())
        
