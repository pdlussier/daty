# -*- coding: utf-8 -*-

from copy import deepcopy
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import Box, CssProvider, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION, Template
from pprint import pprint
from threading import Thread

from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/value.ui")
class Value(Box):
    
    __gtype_name__ = "Value"

    entry = Template.Child("entry")
    label = Template.Child("label")
    unit = Template.Child("unit")
    wikidata = Wikidata()

    def __init__(self, claim, *args, **kwargs):
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
              amount = dv['value']['amount']
              self.label.set_text(amount)
              unit = dv['value']['unit'].split('/')[-1]
              unit = self.download(unit, self.on_download_unit)
              self.quantity_label = dv['value']
          


    def download(self, entity, callback):
        f = lambda : entity
        def do_call():
            entity, error = None, None
            entity = self.wikidata.download(f())
            idle_add(lambda: callback(entity, error))
        thread = Thread(target = do_call)
        thread.start()

    def on_download_unit(self, unit, error):
        label = self.wikidata.get_label(unit)
        self.unit.set_text(label)

    def on_download_done(self, entity, error):
        if error:
            print(error)
        self.label.set_text(self.wikidata.get_label(entity))
