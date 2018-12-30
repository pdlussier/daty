# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ApplicationWindow, IconTheme, Label, Template
from gi.repository.Handy import Column

from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/page.ui")
class Page(Column):
    __gtype_name__ = "Page"

    wikidata = Wikidata()
    statements = Template.Child("statements")

    def __init__(self, *args, entity=None, **kwargs):
        Column.__init__(self, *args, **kwargs)
        
        if entity:
            print(entity)
            data = self.wikidata.download(entity['URI'])
            claims = data['claims'] 
            for P in claims.keys(): 
                for claim in claims[P]:
                    print(self.wikidata.get_claim(claim))
            self.statements.add(Label(label=''.join(["test ", entity['Label']])))
            #print(self.wikidata.get_claim(claim))

            #for property in entity['claims'].keys()
