# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import Frame, ListBoxRow, Separator, Template
from pprint import pprint

@Template.from_resource("/org/prevete/Daty/gtk/values.ui")
class Values(Frame):
    __gtype_name__ = "Values"

    list = Template.Child("list")

    def __init__(self, *args, entity=None, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.list.set_header_func(self.update_header)

    def update_header(self, row, before, *args):
        if before:
            row.set_header(Separator())
 
    def add(self, widget):
        row = ListBoxRow()
        row.add(widget)
        self.list.add(row)
        
        
