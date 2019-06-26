# -*- coding: utf-8 -*-

#    Values
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


from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gi.repository.Gtk import ListBox, ListBoxRow, Separator, Template
from pprint import pprint

from .reference import Reference
from .util import set_style

@Template.from_resource("/ml/prevete/Daty/gtk/values.ui")
class Values(ListBox):
    __gtype_name__ = "Values"

    __gsignals__ = {'reference-toggled':(sf.RUN_LAST,
                                         TYPE_NONE,
                                         (TYPE_PYOBJECT,))}

    def __init__(self, *args, frame=True, **kwargs):
        ListBox.__init__(self, *args, **kwargs)
        self.set_header_func(self.update_header)

        if not frame:
            self.set_shadow_type(0) #None

    def update_header(self, row, before, *args):
        if before:
            separator = Separator()
            context = separator.get_style_context()
            set_style(context, '/ml/prevete/Daty/gtk/value.css', 'separator', True)
            row.set_header(separator)
 
    def add(self, widget):
        row = ListBoxRow()
        context = row.get_style_context()
        widget.context = context
        widget.set_references()
        row.child = widget
        row.add(widget)
        super(Values, self).add(row)

    def add_new():
        pass

    def references_toggled_cb(self, widget, child):
        for i, row in enumerate(self.get_children()):
            if hasattr(row, 'child') and row.child == child:
                i = i+1
                break

        state = row.child.references_expanded
        
        row_context = row.get_style_context()
        resource = '/ml/prevete/Daty/gtk/value.css'
        set_style(row_context, resource, 'expanded', state)

        if not hasattr(child, "references_widgets"):
            child.init_references()

        def f(reference):
            if state:
                row = ListBoxRow()
                row_context = row.get_style_context()
                set_style(row_context, resource, 'expanded', state)
                row.add(reference)
                row.show()
                self.insert(row, i+j)
            else:
                print("removing widget")
                row = self.get_row_at_index(i)
                print(reference)
                print(row.get_children())
                row.remove(reference)
                row.destroy()
                #del row

        for j, reference in enumerate(child.references_widgets):
            f(reference)

        #if state:
        #    new_ref = Reference(new=True)
        #    f(new_ref)
        #else:
        #    row = self.get_row_at_index(i+1)
        #    row.destroy()


        self.emit("reference-toggled", state)

        self.show_all()
        
