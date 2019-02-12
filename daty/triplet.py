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
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_BOOLEAN, TYPE_STRING
from gi.repository.Gtk import Grid, Template

from .entitypopover import EntityPopover

@Template.from_resource("/ml/prevete/Daty/gtk/triplet.ui")
class Triplet(Grid):
    __gtype_name__ = "Triplet"
    __gsignals__ = {'triplet-ready':(sf.RUN_LAST,
                                     TYPE_NONE,
                                     (TYPE_BOOLEAN,)),
                    'variable-selected':(sf.RUN_LAST,
                                         TYPE_NONE,
                                         (TYPE_STRING,))}

    subject = Template.Child("subject")
    property = Template.Child("property")
    object = Template.Child("object")

    def __init__(self, load=None, *args, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        self.load = load
        for widget in (self.subject, self.property, self.object):
            widget.entity_popover = EntityPopover({"Label":"",
                                                   "Description":"",
                                                   "URI":""},
                                                  parent=widget,
                                                  load=self.load,
                                                  search=widget)
            widget.entity_popover.connect("closed",
                                          self.entity_popover_closed_cb)
            widget.entity_popover.connect("variable-selected",
                                          self.variable_selected_cb)

        self.show_all()

    @Template.Callback()
    def button_press_event_cb(self, widget, event):
        widget.entity_popover.set_visible(True)

    def entity_popover_closed_cb(self, popover):
        widget = popover.get_relative_to()
        widget.entity = popover.entity
        self.emit('triplet-ready', True)

    def variable_selected_cb(self, entity_popover, variable):
        self.emit('variable-selected', variable)
