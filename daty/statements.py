# -*- coding: utf-8 -*-

#    Statements
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


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

@Template.from_resource("/ml/prevete/Daty/gtk/statements.ui")
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
