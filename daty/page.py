# -*- coding: utf-8 -*-

from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import Label, ScrolledWindow, Template
from threading import Thread

from .property import Property
from .value import Value
from .values import Values
from .wikidata import Wikidata
from .util import MyThread

@Template.from_resource("/org/prevete/Daty/gtk/page.ui")
class Page(ScrolledWindow):
    __gtype_name__ = "Page"

    statements = Template.Child("statements")
    wikidata = Wikidata()   
 
    def __init__(self, entity, *args, **kwargs):
        ScrolledWindow.__init__(self, *args, **kwargs)
       
        self.claims = entity['claims']
        self.properties = {}
        self.values = {}
        self.i = 0
        for i,P in enumerate(self.claims.keys()):
            self.download_property(i,P)

    def download_property(self, i, URI):
        f = i, URI, cp(self.wikidata)
        def do_call():
            i, URI, wikidata = f
            prop, values, error = None ,None, None
            try:
                prop = wikidata.download(URI)
                label = wikidata.get_label(prop)
                print(label)
                prop = Property(label=label)
                prop.show_all()
                values = Values()
                values.props.expand = True
                values.props.hexpand = True
                values.props.vexpand = True
                self.statements.attach(prop, 0, i, 1, 1)
                self.statements.attach(values, 1, i, 2, 1)
                for claim in self.claims[URI]:
                    claim = claim.toJSON()
                    self.load_value_async(URI, claim, values)
            except Exception as err:
                error = err
            idle_add(lambda: self.on_download_property_done(URI,
                                                            prop,
                                                            values,
                                                            error))
        thread = MyThread(target = do_call)
        thread.start()

    def load_value_async(self, URI, claim, values):
        f = cp(URI), cp(claim)
        def do_call():
            URI, claim = f
            error = None
            try:
                value = Value(claim=claim)
                values.add(value)
                values.show_all()
            except Exception as err:
                error = err
            idle_add(lambda: self.on_value_complete(URI, value, error))
        thread = MyThread(target = do_call)
        thread.start()

    def on_value_complete(self, URI, value, error):
        if error:
            print(error)
        self.show_all()

    def on_download_property_done(self, URI, prop, values, error):
        if error:
            print(error)
        self.show_all() 
