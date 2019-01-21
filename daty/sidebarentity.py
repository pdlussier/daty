# -*- coding: utf-8 -*-

#    SidebarEntity
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
from gi.repository.Gtk import Box, Template

@Template.from_resource("/ml/prevete/Daty/gtk/sidebarentity.ui")
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
