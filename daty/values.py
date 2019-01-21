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
from gi.repository.Gtk import Frame, ListBoxRow, Separator, Template
from pprint import pprint

@Template.from_resource("/ml/prevete/Daty/gtk/values.ui")
class Values(Frame):
    __gtype_name__ = "Values"

    list = Template.Child("list")

    def __init__(self, *args, frame=True, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.list.set_header_func(self.update_header)

        if not frame:
            self.set_shadow_type(0) #None

    def update_header(self, row, before, *args):
        if before:
            row.set_header(Separator())
 
    def add(self, widget):
        row = ListBoxRow()
        row.add(widget)
        self.list.add(row)
        
        
