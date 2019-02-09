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
require_version('Gdk', '3.0')
from gi.repository.Gdk import NotifyType
from gi.repository.Gtk import EventBox, Revealer, Template

from .roundedbutton import RoundedButton
from .util import set_text

@Template.from_resource("/ml/prevete/Daty/gtk/sidebarentity.ui")
class SidebarEntity(EventBox):
    __gtype_name__ = "SidebarEntity"

    box = Template.Child("box")
    label = Template.Child("label")
    description = Template.Child("description")
    URI = Template.Child("URI")

    def __init__(self, entity, *args, description=True, URI=True, close=True):
        """Widget representing an entity in the sidebar

            Args:
                entity (dict): keys are at least "Label", "Description" and "URI";
                description (bool): whether to show description
                URI (bool): whether to show entity URI
        """
        EventBox.__init__(self, *args)
     
        self.entity = entity
 
        set_text(self.label, entity["Label"], entity["Label"])

        if description:
            set_text(self.description, entity['Description'], entity['Description'])
        else:
            self.description.destroy()

        if URI:
            set_text(self.URI, entity['URI'], entity['URI'])
        else:
            self.URI.destroy()

        if close:
            self.close = RoundedButton()
            self.close.set_visible(False)
            self.box.pack_end(self.close, False, True, 0)
            self.enter_connection = self.connect("enter-notify-event", self.enter_notify_event_cb)
            self.leave_connection = self.connect("leave-notify-event", self.leave_notify_event_cb)
            self.close_enter_connection = self.close.connect("leave-notify-event", self.close_leave_notify_event_cb)

    def enter_notify_event_cb(self, widget, event):
        self.close.set_visible(True)
        self.URI.set_visible(False)

    def leave_notify_event_cb(self, widget, event):
        if event.detail == NotifyType(2):
            self.disconnect(self.enter_connection)
            self.disconnect(self.leave_connection)
        else:
            self.close.set_visible(False)
            self.URI.set_visible(True)

    def close_leave_notify_event_cb(self, widget, event):
        self.enter_connection = self.connect("enter-notify-event", self.enter_notify_event_cb)
        self.leave_connection = self.connect("leave-notify-event", self.leave_notify_event_cb)
