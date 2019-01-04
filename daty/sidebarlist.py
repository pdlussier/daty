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

        self.stack = stack

    def update_header(self, row, before, *args):
        if before:
            row.set_header(Separator())
 
    def add(self, widget):
        row = ListBoxRow()
        row.add(widget)
        super(SidebarList, self).add(row)
      
    @Template.Callback() 
    def sidebar_row_activated_cb(self, widget, row):
        entity = row.get_children()[0].entity
        if not self.stack.get_child_by_name(entity['URI']):
            self.stack.add_titled(Page(entity['Data']), entity['URI'], entity['Label'])
        self.stack.set_visible_child_name(entity['URI'])
        self.stack.show_all() 
