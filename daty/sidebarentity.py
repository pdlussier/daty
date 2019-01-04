# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import Box, Template

@Template.from_resource("/org/prevete/Daty/gtk/sidebarentity.ui")
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
            self.description.set_visible(True)
        else:
            self.remove(self.description)
