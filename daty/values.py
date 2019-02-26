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
from gi.repository.Gtk import ListBox, ListBoxRow, Separator, Template
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
        row.add(widget)
        super(Values, self).add(row)
        
#    def add_reference(self, value, reference):
#        row = ListBoxRow()
#        context = row.get_style_context()
#        widget.context = context
#        widget.set_references()
#        row.add(widget)
#        super(Values, self).add(row)
        
