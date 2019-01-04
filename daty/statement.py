# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import Box, IconTheme, Label, Template
from gi.repository.Handy import Column

from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/statement.ui")
class Statement(Box):
    __gtype_name__ = "Statement"

    wikidata = Wikidata()
    property_label = Template.Child("property_label")
    values = Template.Child("values")

    def __init__(self, *args, claim=None, **kwargs):
        Box.__init__(self, *args, **kwargs)
       
        if claim:
            self.property_label.set_text(claim['mainsnak']['property'])
            if 'datatype' in claim['mainsnak'].keys():
                if claim['mainsnak']['datatype'] == 'wikibase-item':
                    value = claim['mainsnak']['datavalue']['value']
                    if value['entity-type'] == 'item':
                        item = self.wikidata.download('Q' + str(value['numeric-id']))
                        print(item.keys())
                    
         
