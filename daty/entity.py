# -*- coding: utf-8 -*-

from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
require_version('Gdk', '3.0')
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gdk import EventType, KEY_Escape
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, CssProvider, Stack, StyleContext, Template
from pprint import pprint
from threading import Thread
from time import sleep

from .entitypopover import EntityPopover
from .qualifierproperty import QualifierProperty
from .util import MyThread
from .values import Values
from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/entity.ui")
class Entity(Stack):
    
    __gtype_name__ = "Entity"

    entry = Template.Child("entry")
    label = Template.Child("label")
    unit = Template.Child("unit")

    wikidata = Wikidata()

    def __init__(self, snak, *args, css=None, load=None, **kwargs):
        Stack.__init__(self, *args, **kwargs)

        self.load = load

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
                  entity = self.download(URI, self.load_entity)
              if dt == 'url':
                  url = dv['value']
                  label = "".join(["<a href='", url, "'>", url.split('/')[2], '</a>'])
                  self.label.set_markup(label)
              if dt == 'quantity':
                  # Unit
                  #self.unit.props.set_no_show_all = False
                  unit = dv['value']['unit']
                  if unit.startswith('http'):
                      unit = dv['value']['unit'].split('/')[-1]
                      self.download(unit, self.on_download_unit)

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
                  self.label.set_text(dv['value'])
                  self.label.set_tooltip_text("Text")
              if dt == 'monolingualtext':
                  self.label.set_text(dv['value']['text'])
                  self.label.set_tooltip_text(dv['value']['language'])
              if dt == 'commonsMedia':
                  self.label.set_text(dv['value'])
                  self.label.set_tooltip_text("Picture")
              if dt == 'external-id':
                  self.label.set_text(dv['value'])
                  self.label.set_tooltip_text("External ID")
              if dt == 'geo-shape':
                  print('geo-shape')
              if dt == 'globe-coordinate':
                  print('globe-coordinate')
              if dt == 'tabular-data':
                  print('tabular-data')
              if dt == 'time':
                  print('time')

        except Exception as err:
            print(err)
            print(type(err))
            print(err.__traceback__)

    def download(self, URI, callback, *cb_args):
        f = lambda : (cp(arg) for arg in cb_args)
        URI, wikidata = cp(URI), cp(self.wikidata)
        def do_call():
            cb_args = list(f())
            entity, error = None, None
            try:
                entity = wikidata.download(URI)
            except Exception as err:
                error = err
            idle_add(lambda: callback(URI, entity, error, *cb_args),
                     priority=PRIORITY_LOW)
        thread = Thread(target = do_call)
        thread.start()

    def on_download_unit(self, URI, unit, error):
        if error:
            print(error)
            print(type(error))
        if unit:
            label = self.wikidata.get_label(unit)
            self.unit.set_text(label)
            self.unit.set_visible(True)

    def load_entity(self, URI, entity, error):
        if error:
            print(type(error))
            print(error)
        self.URI = URI
        label = self.wikidata.get_label(entity)
        description = self.wikidata.get_description(entity)
        self.label.set_text(label)
        self.label.set_tooltip_text(description)
        self.entry.set_text(label)
        self.entity_popover = EntityPopover(self.URI, label, description, parent=self, load=self.load)

    @Template.Callback()
    def button_press_event_cb(self, widget, event):
        if event.type == EventType._2BUTTON_PRESS:
            print("double click")   
        elif event.type == EventType.BUTTON_PRESS:
            self.set_visible_child_name("entry")
            self.entry.grab_focus()

    @Template.Callback()
    def entry_focus_in_event_cb(self, widget, event):
        #self.entity_popover = EntityPopover(self.URI, label, description, parent=self, load=self.load)
        self.entity_popover.set_visible(True)

    @Template.Callback()
    def entry_focus_out_event_cb(self, widget, event):
        self.set_visible_child_name("view")
        self.entity_popover.hide()
        
    @Template.Callback()
    def entry_key_release_event_cb(self, widget, event):
        if event.keyval == KEY_Escape:
            self.set_visible_child_name("view")
            self.entity_popover.hide()
