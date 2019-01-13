# -*- coding: utf-8 -*-

from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import Box, CssProvider, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION, Template
from pprint import pprint
from threading import Thread

from .util import MyThread
from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/value.ui")
class Value(Box):
    
    __gtype_name__ = "Value"

    entry = Template.Child("entry")
    label = Template.Child("label")
    unit = Template.Child("unit")
    wikidata = Wikidata()

    def __init__(self, claim, *args, **kwargs):
        #self.unit.props.set_no_show_all = True
        try:
            Box.__init__(self, *args, **kwargs)
            mainsnak = claim['mainsnak']
            if mainsnak['snaktype'] == 'novalue':
              self.label.set_text("No value")
            if mainsnak['snaktype'] == 'value':
              dv = mainsnak['datavalue']
              dt = mainsnak['datatype']
              if dt == 'wikibase-item' or dt == 'wikibase-property':
                if dv['type'] == 'wikibase-entityid':
                  entity_type = dv['value']['entity-type']
                  numeric_id = dv['value']['numeric-id']
                  if entity_type == 'item':
                    URI = 'Q' + str(numeric_id)
                  if entity_type == 'property':
                    URI = 'P' + str(numeric_id)
                  entity = self.download(URI, self.on_download_done)
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
                  print(dv['value'])
              if dt == 'commonsMedia':
                  self.label.set_text(dv['value'])
                  self.label.set_tooltip_text("Picture")
              if dt == 'external-id':
                  self.label.set_text(dv['value'])
                  self.label.set_tooltip_text("External ID")
              if dt == 'geo-shape':
                  print(dv['value'])
              if dt == 'globe-coordinate':
                  print(dv['value'])
              if dt == 'monolingualtext':
                  print(dv['value'])
              if dt == 'tabular-data':
                  print(dv['value'])
              if dt == 'time':
                  print(dv['value'])

        except Exception as err:
            print(err)

    def download(self, entity, callback):
        f = cp(entity), cp(self.wikidata)
        def do_call():
            entity, wikidata = f
            error = None
            try:
                entity = wikidata.download(entity)
            except Exception as e:
                error = e
            idle_add(lambda: callback(entity, error))
        thread = MyThread(target = do_call)
        thread.start()

    def on_download_unit(self, unit, error):
        if error:
            print(error)
        if unit:
            label = self.wikidata.get_label(unit)
            self.unit.set_text(label)
            self.unit.set_visible(True)

    def on_download_done(self, entity, error):
        if error:
            print(error)
        label = self.wikidata.get_label(entity)
        description = self.wikidata.get_description(entity)
        self.label.set_text(label)
        self.label.set_tooltip_text(description)

    @Template.Callback()
    def label_button_press_event_cb(self, widget, event):
        print(event.type)
        #if event.button == 1 :
        #    data = widget.get_path_at_pos(int(event.x), int(event.y))
        #    if data :
        #        if event.type == gtk.gdk._2BUTTON_PRESS :
        #            print(" double click ")

        #        elif event.type == gtk.gdk.BUTTON_PRESS :
        #            print("single click ")

    #def 
