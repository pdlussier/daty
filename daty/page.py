# -*- coding: utf-8 -*-

from copy import deepcopy
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import Label, ScrolledWindow, Template
from threading import Thread

from .property import Property
from .value import Value
from .values import Values
from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/page.ui")
class Page(ScrolledWindow):
    __gtype_name__ = "Page"

    statements = Template.Child("statements")
    wikidata = Wikidata()   
 
    def __init__(self, entity, *args, **kwargs):
        ScrolledWindow.__init__(self, *args, **kwargs)
       
        claims = entity['claims']
        self.property_button = {}
        for i,P in enumerate(claims.keys()):
            # Property buttons
            self.property_button[P] = Property(label=P)
            self.download_property(P) 
            self.statements.attach(self.property_button[P], 0, i+1, 1, 1)
            # Values Listbox
            values = Values()
            values.set_hexpand(True)
            values.props.expand = True
            self.statements.attach(values, 1, i+1, 2, 1)
            for claim in claims[P]:
                claim = self.wikidata.get_claim(claim)
                value = Value(claim=claim) 
                values.add(value)

    def download_property(self, URI):
        f = lambda : URI
        def do_call():
            URI, prop, error = None, None, None
            try:
                URI, prop = f(), deepcopy(self.wikidata).download(f())
            except Exception as err:
                error = err
            idle_add(lambda: self.on_download_property_done(URI, prop, error))
        thread = Thread(target = do_call)
        thread.start()

    def on_download_property_done(self, URI, prop, error):
        self.property_button[URI].set_label(self.wikidata.get_label(prop))
