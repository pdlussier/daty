# -*- coding: utf-8 -*-

#    Triplet
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
from gi.repository.Gtk import Grid, Template

@Template.from_resource("/ml/prevete/Daty/gtk/triplet.ui")
class Triplet(Grid):
    __gtype_name__ = "Triplet"

    #properties = Template.Child("properties")
    subject = Template.Child("subject")
    property = Template.Child("property")
    object = Template.Child("object")

    def __init__(self, *args, **kwargs):
        Grid.__init__(self, *args, **kwargs)
        self.show_all()
        #self.properties.add(Property())

    @Template.Callback()
    def button_press_event_cb(self, widget, event):
        print(widget)
        print(event)
    #    if event.keyval == 65307:
    #        self.header_bar_stack.set_visible_child_name("open_entities")
    #        self.content_stack.set_visible_child_name("placeholder")
    #        #self.print(event.group)
    #    else:
    #        if self.content_stack.get_visible_child_name() == "placeholder":
    #            self.header_bar_stack.set_visible_child_name("header_search_type")
    #            self.content_stack.set_visible_child_name("search")
    #    #print(unicode_to_keyval(event.string)) 
