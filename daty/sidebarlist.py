# -*- coding: utf-8 -*-

#    SidebarList
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


from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gi.repository.GLib import idle_add
from gi.repository.Gtk import ListBox, ListBoxRow, Separator, Template
#from re import IGNORECASE, compile, escape, sub

from .entityselectable import EntitySelectable
#from .page import Page
#from .property import Property
from .sidebarentity import SidebarEntity
#from .values import Values
#from .util import MyThread, label_color

@Template.from_resource("/ml/prevete/Daty/gtk/sidebarlist.ui")
class SidebarList(ListBox):

    __gtype_name__ = "SidebarList"

    __gsignals__ = {'entity-selected':(sf.RUN_LAST,
                                       TYPE_NONE,
                                       (TYPE_PYOBJECT,))}

    def __init__(self,
                 autoselect=False,
                 *args, **kwargs):
        """Sidebar ListBox
        
        Args:
            entity_label (Gtk.Label): title of the visible entity;
            description_label (Gtk.Label): description of the visible entity;
            autoselect (bool): whether to select the first element
                by default.

        """
        ListBox.__init__(self, *args, **kwargs)

        # Set some inputs as attributes
        self.autoselect = autoselect

        # Set "last" selected entities attribute
        self.last = []

        # Set separator as row header
        self.set_header_func(self.update_header)

        self.connect("row-selected", self.sidebar_row_selected_cb)

    def update_header(self, row, before, *args):
        """See GTK+ Documentation"""
        if before:
            row.set_header(Separator())

    def set_selection_mode(self, value):
        """Set selection mode on or off

            Args:
                value (bool): whether to activate selection mode
        """
        #TODO: add custom titlebar
        #self.header_bar.add_custom_titlebar
        self.selected = []
        self.foreach(self.set_checkbutton, value)

    def set_checkbutton(self, row, value):
        """Add checkbutton to row

            Args:
                row (Gtk.ListBoxRow): selected row;
                value (bool): whether to add or remove checkbutton.
        """
        if row.get_children():
            child = row.child
            entity = child.entity
            if value:
                row.check = EntitySelectable(entity,
                                             widget=False,
                                             selected=self.selected)
                child.box.pack_start(row.check, False, False, 0)
                row.child.box.child_set_property(row.check, 'position', 0)
            else:
                row.check.destroy()

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

        super(SidebarList, self).add(row)

        # Select if 'autoselect'
        if (len(self.get_children()) >= 1 and self.autoselect) or select:
            self.select_row(row)

        # The final empty row that acts as separator
        row = ListBoxRow()
        row.props.activatable = False
        row.props.selectable = False
        super(SidebarList, self).add(row)

    def sidebar_row_selected_cb(self, listbox, row):
        """Sidebar row selected callback



            Args:
                listbox (Gtk.ListBox): the listbox class, so self;
                row (Gtk.ListBoxRow): the selected row, which has 
                for only child a SidebarEntity object;
                visible child.
                entity_label (Gtk.Label): widget of entity title
                entity_description(Gtk.Label)
        """

        if not row:
            if len(self.last) >= 1:
                row = self.last[-1]
            #TODO: decide what to do when no entities are open
            #if len(self.last) == 0:
            else:
                row = self.get_row_at_index(0)
            #print(self.last)
            self.select_row(row)
            return None

        self.emit("entity-selected", row.child.entity)

        # Set last
        self.last.append(row)
