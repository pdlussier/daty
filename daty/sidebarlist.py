# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ListBox, ListBoxRow, Separator, Template

from .page import Page

@Template.from_resource("/org/prevete/Daty/gtk/sidebarlist.ui")
class SidebarList(ListBox):
    __gtype_name__ = "SidebarList"

    def __init__(self, stack, *args, **kwargs):
        ListBox.__init__(self, *args, **kwargs)
        self.set_header_func(self.update_header)

        self.connect("row-selected", self.sidebar_row_selected_cb, stack)

    def update_header(self, row, before, *args):
        if before:
            row.set_header(Separator())
 
    def add(self, widget):
        if self.get_children():
            last_row = self.get_children()[-1]
            if not last_row.get_children():
                self.remove(last_row)
        row = ListBoxRow()
        row.add(widget)
        super(SidebarList, self).add(row)
        row = ListBoxRow()
        row.props.activatable = False
        row.props.selectable = False
        super(SidebarList, self).add(row)
      
    def sidebar_row_selected_cb(self, widget, row, stack):
        entity = row.get_children()[0].entity
        if not stack.get_child_by_name(entity['URI']):
            stack.add_titled(Page(entity['Data']), entity['URI'], entity['Label'])
        stack.set_visible_child_name(entity['URI'])
        stack.show_all() 
