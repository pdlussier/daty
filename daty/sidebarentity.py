# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import Box, Template

@Template.from_resource("/org/prevete/Daty/gtk/sidebarentity.ui")
class SidebarEntity(Box):
    __gtype_name__ = "SidebarEntity"

    label = Template.Child("label")
    description = Template.Child("description")
    URI = Template.Child("URI")

    def __init__(self, entity, *args, description=True, URI=True):
        """Widget representing an entity in the sidebar

            Args:
                entity (dict): keys are at least "Label", "Description" and "URI";
                description (bool): whether to show description
                URI (bool): whether to show entity URI
        """
        Box.__init__(self, *args)
     
        self.entity = entity
 
        self.label.set_text(entity["Label"])

        if description:
            self.description.set_text(entity['Description'])
        else:
            self.remove(self.description)

        if URI:
            self.URI.set_text("".join(['(', entity['URI'], ')']))
        else:
            self.remove(self.URI)

    def motion_notify_event(self, widget, event):
        print(widget)
        print(event)
