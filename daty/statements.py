# -*- coding: utf-8 -*-

from copy import deepcopy
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import Template, TreeView
from threading import Thread

from .property import Property
from .value import Value
from .values import Values
from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/statements.ui")
class Statements(TreeView):
    __gtype_name__ = "Statements"

    list_store = Template.Child("list_store")
    wikidata = Wikidata()   
 
    def __init__(self, *args, **kwargs):
        TreeView.__init__(self, *args, **kwargs)
       
    def add(self, cell_list):
        self.list_store.append(cell_list)
        self.set_model(self.list_store)
        model = self.get_model()
        print(model)
        print(self.list_store)
        self.show_all()
