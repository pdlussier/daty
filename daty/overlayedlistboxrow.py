# -*- coding: utf-8 -*-

#    OverlayedWidget
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
#from gi.repository.GLib import idle_add
from gi.repository.Gtk import Align, EventBox, ListBoxRow, Overlay, Revealer, RevealerTransitionType
from threading import Thread
from time import sleep

class OverlayedListBoxRow(ListBoxRow):
    def __init__(self, top_widget, widget, halign=Align.END, valign=Align.FILL):
        ListBoxRow.__init__(self)

        self.eventbox = EventBox()
        self.overlay = Overlay()
        self.revealer = Revealer()

        self.add(self.eventbox)
        self.eventbox.add(self.overlay)
        self.overlay.add_overlay(self.revealer)
        self.revealer.add(top_widget)
        self.add_widget(widget)

        self.revealer.set_transition_type (RevealerTransitionType.NONE)
        self.revealer.set_reveal_child(False)
        self.revealer.set_property("halign", halign)
        self.revealer.set_property("valign", valign)

        self.enter_connection = self.eventbox.connect("enter-notify-event", self.enter_notify_event_cb)
        self.leave_connection = self.eventbox.connect("leave-notify-event", self.leave_notify_event_cb)

    def add_widget(self, widget):
        self.child = widget
        self.overlay.add(widget)

    def enter_notify_event_cb(self, widget, event):
        self.revealer.set_reveal_child(True)

    def leave_notify_event_cb(self, widget, event):
        self.revealer.set_reveal_child(False)
