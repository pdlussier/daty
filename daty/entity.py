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

from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
require_version('Gdk', '3.0')
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gdk import EventType, KEY_Escape
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, CssProvider, ListBoxRow, Stack, StyleContext, Template
from pprint import pprint
from threading import Thread
from time import sleep

#from .util import MyThread
from .sidebarentity import SidebarEntity
from .util import download_light, set_style, set_text
from .wikidata import Wikidata

@Template.from_resource("/ml/prevete/Daty/gtk/entity.ui")
class Entity(Stack):
    
    __gtype_name__ = "Entity"

    __gsignals__ = {'entity-editing':(sf.RUN_LAST,
                                      TYPE_NONE,
                                      (TYPE_PYOBJECT,)),
                    'new-window-clicked':(sf.RUN_LAST,
                                          TYPE_NONE,
                                          (TYPE_PYOBJECT,)),
                    'object-selected':(sf.RUN_LAST,
                                       TYPE_NONE,
                                       (TYPE_PYOBJECT,))}

    entry = Template.Child("entry")
    label = Template.Child("label")
    unit = Template.Child("unit")

    #TODO:implement editing

    def __init__(self, snak, *args, qualifier=False, css=None, **kwargs):
        Stack.__init__(self, *args, **kwargs)

        context = self.entry.get_style_context()
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
                  print("Entity: light downloading", URI)
                  download_light(URI, self.load_entity)
              if dt == 'url':
                  url = dv['value']
                  #label = "".join(["<a href='", url, "'>", url.split('/')[2], '</a>'])
                  label = url.split('/')[2]
                  self.data = {"url":url}
                  self.set_text(label, url)
                  context = self.label.get_style_context()
                  set_style(context, '/ml/prevete/Daty/gtk/entity.css', 'url', True)
                  #self.label.props.use_markup = True
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
            raise err

        #self.entry.connect("search-changed", self.entry_search_changed_cb)

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
        self.data = entity
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
        if not hasattr(self, 'popover'):
            try:
                from .entitypopover import EntityPopover
                self.popover = EntityPopover(self.data)
                self.popover.set_relative_to(self)
                self.entry.connect("search-changed", self.popover.search_entry_search_changed_cb)
                self.popover.connect("new-window-clicked", self.new_window_clicked_cb)
                self.popover.connect("object-selected", self.object_selected_cb)
                self.entry.emit("search-changed")
                self.popover.set_visible(True)
                self.emit("entity-editing", self.popover)
            except AttributeError as e:
                #raise e
                print("no popover available for this type of value")
        else:
            self.entry.emit("search-changed")
            self.popover.set_visible(True)
            self.emit("entity-editing", self.popover)

    def object_selected_cb(self, popover, entity):
        print("Editor: object selected:", entity['URI'])
        self.load_entity(entity['URI'], entity, None)
        self.emit("object-selected", entity)

    def new_window_clicked_cb(self, popover, entities):
        print("Entity: new window clicked")
        self.emit("new-window-clicked", entities)

    @Template.Callback()
    def entry_focus_out_event_cb(self, widget, event):
        self.set_visible_child_name("view")
        self.entry.set_visible(False)
        self.entry.props.margin_top = 0
        self.entry.props.margin_bottom = 0
        self.entry.set_text(self.label.get_text())
        try:
            self.popover.hide()
        except AttributeError as e:
            print("this entity has no popover")

    @Template.Callback()
    def entry_key_release_event_cb(self, widget, event):
        try:
            if event.keyval == KEY_Escape:
                self.entry_focus_out_event_cb(widget, event)
        except AttributeError as e:
            print("no entity popover for this value")
