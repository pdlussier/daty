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
from gi.repository.GObject import TYPE_NONE, TYPE_BOOLEAN, TYPE_PYOBJECT, TYPE_STRING
from gi.repository.Gtk import Grid, Template

from .entitypopover import EntityPopover
from .util import pango_label, set_text

@Template.from_resource("/ml/prevete/Daty/gtk/triplet.ui")
class Triplet(Grid):
    __gtype_name__ = "Triplet"
    __gsignals__ = {'triplet-ready':(sf.RUN_LAST,
                                     TYPE_NONE,
                                     (TYPE_BOOLEAN,)),
                    'default-variable-selected':(sf.RUN_LAST,
                                                 TYPE_NONE,
                                                 (TYPE_PYOBJECT,)),
                    'entity-new':(sf.RUN_LAST,
                                  TYPE_NONE,
                                  (TYPE_PYOBJECT,)),
                    'new-window-clicked':(sf.RUN_LAST,
                                          TYPE_NONE,
                                          (TYPE_PYOBJECT,)),
                    'object-selected':(sf.RUN_LAST,
                                       TYPE_NONE,
                                       (TYPE_PYOBJECT,)),
                    'variable-deleted':(sf.RUN_LAST,
                                       TYPE_NONE,
                                       (TYPE_PYOBJECT,))}

    subject = Template.Child("subject")
    subject_title = Template.Child("subject_title")
    subject_description = Template.Child("subject_description")
    property = Template.Child("property")
    property_title = Template.Child("property_title")
    property_description = Template.Child("property_description")
    object = Template.Child("object")
    object_title = Template.Child("object_title")
    object_description = Template.Child("object_description")

    def __init__(self, variables=None, *args, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        self.variables = variables
        self.subject.title = self.subject_title
        self.subject.description = self.subject_description
        self.property.title = self.property_title
        self.property.description = self.property_description
        self.object.title = self.object_title
        self.object.description = self.object_description

        self.members = (self.subject, self.property, self.object)

        for widget in self.members:
            widget.entity = {"Label":"", "Description":"", "URI":""}
            widget.popover = EntityPopover(widget.entity,
                                                  variables=self.variables)
            widget.popover.set_relative_to(widget)
            widget.popover.connect("default-variable-selected",
                                          self.default_variable_selected_cb)
            widget.popover.connect("entity-new",
                                          self.entity_new_clicked_cb)
            widget.popover.connect("new-window-clicked",
                                          self.new_window_clicked_cb)
            widget.popover.connect("object-selected",
                                          self.object_selected_cb)
            widget.popover.connect("variable-deleted",
                                          self.variable_deleted_cb)

        self.property.popover.search_entry.set_text("property:")

        self.show_all()

    def entity_new_clicked_cb(self, popover, query):
        #print(query)
        self.emit("entity-new", query)

    def new_window_clicked_cb(self, popover, entities):
        self.emit("new-window-clicked", entities)

    def variable_deleted_cb(self, popover, entity):
        self.emit("variable-deleted", entity)

    def set_widget(self, widget, entity):
        set_text(widget.title, entity["Label"], entity["Label"])
        pango_label(widget.title, 'bold')
        set_text(widget.description, entity["Description"], entity["Description"])
        self.show_all()

    def set_selected(self, widget, value):
        if value:
            pango_label(widget.title, 'ultrabold')
        else:
            pango_label(widget.title, 'bold')

    @Template.Callback()
    def widget_clicked_cb(self, widget):
        widget.popover.set_visible(True)

    def popover_closed_cb(self, popover):
        self.emit('triplet-ready', True)

    def default_variable_selected_cb(self, popover, entity):
        widget = self.object_selected_cb(popover, entity, emit=False)
        pango_label(widget.title, 'ultrabold')
        self.emit('default-variable-selected', widget.entity)

    def object_selected_cb(self, popover, entity, emit=True):
        widget = popover.get_relative_to()
        self.set_widget(widget, entity)
        if emit:
            self.emit("object-selected", entity)
        return widget
