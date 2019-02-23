# -*- coding: utf-8 -*-

#    FiltersList
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

from .util import MyThread, label_color

@Template.from_resource("/ml/prevete/Daty/gtk/filterslist.ui")
class FiltersList(ListBox):
    __gtype_name__ = "FiltersList"

    def __init__(self,
                 *args, **kwargs):
        """Sidebar ListBox

        Args:
            stack (Gtk.Stack): entities stack;
            entity_label (Gtk.Label): title of the visible entity;
            description_label (Gtk.Label): description of the visible entity;
            autoselect (bool): whether to select the first element
                by default.
        """
        ListBox.__init__(self, *args, **kwargs)
        self.set_header_func(self.update_header)



    def update_header(self, row, before, *args):
        """See GTK+ Documentation"""
        if before:
            row.set_header(Separator())

    def add(self, row, select=False):
        """Add widget to a new row

            Overrides Gtk.Container.add

            Args:
                widget (Gtk.Widget): the widget to add to the new row.
        """
        # If the list has rows
        if self.get_children():

            # Pick the last one
            last_row = self.get_children()[-1]

            # If it has no children, it is the ending separator, so remove it
            if not last_row.get_children():
                self.remove(last_row)

        super(FiltersList, self).add(row)

        # Select if 'autoselect'
        if (len(self.get_children()) >= 1) or select:
            self.select_row(row)

        # The final empty row that acts as separator
        row = ListBoxRow()
        row.props.activatable = False
        row.props.selectable = False
        super(FiltersList, self).add(row)
        self.show_all()
