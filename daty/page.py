# -*- coding: utf-8 -*-

from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add, PRIORITY_LOW
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
 
    def __init__(self, entity, *args, load=None, **kwargs):
        ScrolledWindow.__init__(self, *args, **kwargs)
      
        self.load = load
        self.claims = entity['claims']
        for i,P in enumerate(self.claims.keys()):
            self.download(P, self.load_property, i)

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

    def load_property(self, URI, prop, error, i):
        try:
            if error:
                print(error)
            prop = Property(prop)
            values = Values()
            values.props.expand = True
            values.props.hexpand = True
            values.props.vexpand = True
            self.statements.attach(prop, 0, i, 1, 1)
            self.statements.attach(values, 1, i, 2, 1)
            for claim in self.claims[URI]:
                claim = claim.toJSON()
                self.load_value_async(URI, claim, values)
                #self.load_qualifiers_async(
        except Exception as e:
            print(URI)
            pprint(e)
            print(e.traceback)
            print(prop.keys())

    def load_value_async(self, URI, claim, values):
        f = cp(URI), cp(claim)
        def do_call():
            URI, claim = f
            error = None
            try:
                pass
            except Exception as err:
                error = err
            idle_add(lambda: self.on_value_complete(claim, values, error))
        thread = MyThread(target = do_call)
        thread.start()

    def on_value_complete(self, claim, values, error):
        if error:
            print(error)
        value = Value(claim=claim, load=self.load)
        values.add(value)
        values.show_all()
