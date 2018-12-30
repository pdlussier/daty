# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import Box, Template, Window
from gi.repository.Gdk import unicode_to_keyval
require_version('Handy', '0.0')
from gi.repository.Handy import Column

@Template.from_resource("/org/prevete/Daty/gtk/sidebarrow.ui")
class SidebarEntity(Box):
    __gtype_name__ = "SidebarEntity"

    label = Template.Child("label")
    description = Template.Child("description")

    def __init__(self, entity, *args, description=False):
        Box.__init__(self, *args)
       
        self.entity = entity 
        self.label.set_text(entity['Label'])
        self.description.set_text(entity['Description'])

        if description:
            self.set_visible(True)
        else:
            print('When I am present, sidebar description should not be visible')
            self.set_visible(False)
        self.show_all()

    #def get_label

    #@Template.Callback()
    #def clicked_cb(self, widget):
