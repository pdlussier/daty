# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ApplicationWindow, Frame, IconTheme, Label, ListBox, Template
from gi.repository.Handy import Column
from pprint import pprint

from .property import Property
from .value import Value
#from .statement import Statement
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
            for i,P in enumerate(claims.keys()):
                p = self.wikidata.download(P)
                property_button = Property(P=p['labels']['en'])
                #print(property_button.get_hexpand())
                self.statements.attach(property_button, 0, i, 1, 1)
                frame = Frame()
                values = ListBox()
                frame.add(values)
                print(frame.get_hexpand())
                frame.set_hexpand(True)
                frame.props.expand = True
                self.statements.attach(frame, 1, i, 1, 1)
                #pprint(p)
                for claim in claims[P]:
                    claim = self.wikidata.get_claim(claim)
                    #pprint(claim)
                    value = Value(claim=claim)#claim['maisnak']['datavalue']) 
                    values.add(value)
                    #prop = Label(label=claim['mainsnak']['property'])
                    #prop = Property(P=claim['mainsnak']['property'])
            #self.statements.add(Label(label=''.join(["test ", entity['Label']])))
