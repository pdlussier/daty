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
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, CssProvider, Label, ListBox, ListBoxRow, Separator, StyleContext, Template
from pprint import pprint

@Template.from_resource("/ml/prevete/Daty/gtk/values.ui")
class Values(ListBox):
    __gtype_name__ = "Values"

    #list = Template.Child("list")

    def __init__(self, *args, frame=True, **kwargs):
        ListBox.__init__(self, *args, **kwargs)
        self.set_header_func(self.update_header)

        if not frame:
            self.set_shadow_type(0) #None

    def update_header(self, row, before, *args):
        if before:
            row.set_header(Separator())
 
    def add(self, widget):
        row = ListBoxRow()
        context = row.get_style_context()
        widget.context = context
        widget.set_references()
        row.child = widget
        row.add(widget)
        super(Values, self).add(row)

    def references_toggled_cb(self, widget, child):
        for i, row in enumerate(self.get_children()):
            if hasattr(row, 'child') and row.child == child:
                print(row)
                print(type(child))
                print(i)
                break

        state = row.child.button.get_active()
        
        context = self.get_style_context()
        provider = CssProvider()
        provider.load_from_resource('/ml/prevete/Daty/gtk/value.css')
        context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION)

        if state:
            context.add_class('expanded')
            if hasattr(child, "references")
            row = ListBoxRow()

            #button = Button("New reference")
            #value = Value(claim=claim, load=self.load)
            row.add(Label("Add reference"))
            self.insert(row, i+1)
        else:
            context.remove_class('expanded')

            row = self.get_row_at_index(i+1)
            row.destroy()

        self.show_all()
            #print(state)
        #lambda row: row if row.child == child else None
        #for
        #if
        #that_row = [row for row in self.get_children() if row.child == child][-1]
        #print(widget)
        #print()
        #if state:
        #    print(state)

#    def add_reference(self, value, reference):
#        row = ListBoxRow()
#        context = row.get_style_context()
#        widget.context = context
#        widget.set_references()
#        row.add(widget)
#        super(Values, self).add(row)
        
