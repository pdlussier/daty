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
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gtk import Box, ListBox, ListBoxRow, Separator, Template
from threading import Thread
from re import IGNORECASE, compile, escape, sub

from .entityselectable import EntitySelectable
from .page import Page
from .property import Property
from .sidebarentity import SidebarEntity
from .values import Values
from .util import MyThread, label_color

@Template.from_resource("/ml/prevete/Daty/gtk/sidebarlist.ui")
class SidebarList(ListBox):
    __gtype_name__ = "SidebarList"

    def __init__(self,
                 content_leaflet,
                 titlebar_leaflet,
                 stack, 
                 entity_label,
                 entity_description, 
                 entity_search_entry,
                 sidebar_search_entry,
                 autoselect=True,
                 load=None,
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

        self.autoselect = autoselect
        self.stack = stack
        self.load = load

        self.entity_search_entry = entity_search_entry
        self.sidebar_search_entry = sidebar_search_entry

        # Set separator as row header
        self.set_header_func(self.update_header)

        self.connect("row-selected", self.sidebar_row_selected_cb,
                                     content_leaflet,
                                     titlebar_leaflet,
                                     stack,
                                     entity_label,
                                     entity_description)

    def entity_search_entry_changed_cb(self, entry):
        text = entry.get_text()
        page = self.stack.get_visible_child()
        statements = page.statements
        i = 0
        row = lambda i,j: statements.get_child_at(j,i)
        while row(i,0):
            p_label = row(i,0).property_label.get_text()
            p_desc = row(i,0).property_label.get_tooltip_text()
            p_found = self.filter(text, p_label) or self.filter(text, p_desc)
            if p_found:
                label_color(row(i,0).property_label, text)
                row(i,0).set_visible(True)
                row(i,1).set_visible(True)
            else:
                label_color(row(i,0).property_label, color='')
                row(i,0).set_visible(False)
                row(i,1).set_visible(False)
            i = i + 1

    def filter(query, text):
        return query.lower() in text.lower()

    def sidebar_search_entry_changed_cb(self, entry):
        text = entry.get_text()
        for row in self.get_children():
            if row.get_children():
                child = row.box.child
                entity = child.entity
                if text.lower() in entity["Label"].lower() or text.lower() in entity["Description"].lower():
                    row.set_visible(True)
                    label_color(child.label, text)
                    label_color(child.description, text)
                else:
                    row.set_visible(False)
                   
    def update_header(self, row, before, *args):
        """See GTK+ Documentation"""
        if before:
            row.set_header(Separator())

    def set_selection_mode(self, value):
        """Set selection mode on or off

            Args:
                value (bool): whether to activate selection mode
        """
        self.selected = []
        self.foreach(self.set_checkbutton, value)

    def set_checkbutton(self, row, value):
        """Add checkbutton to row

            Args:
                row (Gtk.ListBoxRow): selected row;
                value (bool): whether to add or remove checkbutton.
        """
        if row.get_children():
            child = row.box.child
            entity = child.entity
            if value:
                row.box.remove(child)
                row.check = EntitySelectable(entity,
                                             widget=False, 
                                             selected=self.selected)
                row.box.add(row.check)
                row.box.add(child)
            else:
                row.box.remove(row.check)
                row.check.destroy()
                del row.check
 
    def add(self, widget):
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

        # Create new row and add to self
        row = ListBoxRow()
        row.box = Box()
        row.add(row.box)
        row.box.child = widget
        row.box.add(row.box.child)
        
        super(SidebarList, self).add(row)

        # Select if 'autoselect'
        if len(self.get_children()) == 1 and self.autoselect:
            self.select_row(row)

        # The final empty row that acts as separator
        row = ListBoxRow()
        row.props.activatable = False
        row.props.selectable = False
        super(SidebarList, self).add(row)
     
    def load_page_async(self, entity):
        entity = cp(entity)
        f = lambda : entity
        def do_call():
            idle_add(lambda: self.on_page_complete(entity))
        thread = MyThread(target = do_call)
        thread.start()

    def on_page_complete(self, entity):
        page = Page(entity['Data'], load=self.load)
        self.stack.add_titled(page, entity['URI'], entity['Label'])
        self.stack.set_visible_child_name(entity['URI'])
        self.entity_search_entry.connect("search-changed", self.entity_search_entry_changed_cb)
        self.sidebar_search_entry.connect("search-changed", self.sidebar_search_entry_changed_cb)

    def sidebar_row_selected_cb(self,
                                listbox, 
                                row,
                                content_leaflet, 
                                titlebar_leaflet,
                                stack, 
                                entity_label,
                                entity_description,
                                load=None):
        """Sidebar row selected callback

            If not existing, creates entity page and then
            switch to it in content_stack.

            Args:
                listbox (Gtk.ListBox): the listbox class, so self;
                row (Gtk.ListBoxRow): the selected row, which has 
                for only child a SidebarEntity object;
                stack (Gtk.Stack): the stack which has to switch
                visible child.
                entity_label (Gtk.Label): widget of entity title
                entity_description(Gtk.Label)
        """

        # Set view for folded mode
        content_leaflet.set_visible_child_name("content_stack")
        titlebar_leaflet.set_visible_child_name("sub_header_bar")
        #sub_header_bar = [c for c in titlebar_leaflet.get_children()
        #                  if c.get_name() == 'sub_header_bar'][-1]
        #entity_back = [c for c in sub_header_bar
        #               if c.get_name() == 'entity_back'][-1]
        #entity_back.set_visible(True)
            
        # Get entity from SidebarEntity child
        sidebar_entity = row.box.child
        entity = sidebar_entity.entity

        # Set titlebar
        entity_label.set_text(entity["Label"])
        entity_label.set_tooltip_text(entity["Label"])
        entity_description.set_text(entity["Description"])
        entity_description.set_tooltip_text(entity["Description"])

        # If there is no corresponding child in stack, create one
        if not stack.get_child_by_name(entity['URI']):
            stack.set_visible_child_name("loading")
            children = stack.get_children()
            if len(children) >= 10:
                print("more than 5 children")
                oldest = children[1]
                children.remove(oldest)
                oldest.destroy()
                del oldest
                print(len(children))
            # To be replaced with a timeout that makes sure 
            # that you are not just passing over the row with arrows.
            #page = Page(entity['Data'])
            #stack.add_titled(page, entity['URI'], entity['Label'])
            #stack.set_visible_child_name(entity['URI'])
            #stack.show_all()
            self.load_page_async(entity)
        else:
            stack.set_visible_child_name(entity['URI'])
            self.entity_search_entry.connect("search-changed", self.entity_search_entry_changed_cb)
            self.sidebar_search_entry.connect("search-changed", self.sidebar_search_entry_changed_cb)
