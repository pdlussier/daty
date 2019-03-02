# -*- coding: utf-8 -*-

#    EntityPopover
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
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gi.repository.Gtk import IconSize, ListBoxRow, PopoverMenu, Template
from pprint import pprint

from .roundedbutton import RoundedButton
from .sidebarentity import SidebarEntity
from .util import EntitySet, download, search, pango_label, set_text

@Template.from_resource("/ml/prevete/Daty/gtk/entitypopover.ui")
class EntityPopover(PopoverMenu):

    __gtype_name__ = "EntityPopover"

    __gsignals__ = {'default-variable-selected':(sf.RUN_LAST,
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

    label = Template.Child("label")
    description = Template.Child("description")
    entity_grid = Template.Child("entity_grid")
    entity_new = Template.Child("entity_new")
    new_window = Template.Child("new_window")
    results = Template.Child("results")
    results_listbox = Template.Child("results_listbox")
    results_nope_query = Template.Child("results_nope_query")
    results_stack = Template.Child("results_stack")
#    search_box = Template.Child("search_box")
    search_entry = Template.Child("search_entry")
    search_subtitle = Template.Child("search_subtitle")
    variable_grid = Template.Child("variable_grid")
    variable_record = Template.Child("variable_record")
    variable_title = Template.Child("variable_title")
    variable_subtitle = Template.Child("variable_subtitle")

    def __init__(self, entity, *args, parent=None,
                 variables=None, **kwargs):
        PopoverMenu.__init__(self, *args, **kwargs)

        self.variables = variables
        self.entity = entity
        if self.variables != None:
            self.set_modal(True)
            self.search_entry.set_visible(True)
            self.variable_grid.set_visible(True)
            self.entity_grid.set_visible(False)
            subtitle = "Search for entities or\n<i>define new variables</i>"
            set_text(self.search_subtitle, subtitle, subtitle, markup=True)
            self.search_entry.connect("search-changed",
                                      self.search_entry_search_changed_cb)
            self.search_entry.grab_focus()

        if parent:
            self.set_relative_to(parent)
        set_text(self.label, entity["Label"], entity["Label"])
        set_text(self.description, entity["Description"], entity["Description"])

    def search_entry_search_changed_cb(self, entry):
        query = entry.get_text()
        if query:
            self.results_stack.set_visible_child_name("results_searching")
            search(query, self.on_search_done, query, entry)
        else:
            self.variable_grid.set_visible(False)
            if self.variables:
                self.variables_set_results(self.results_listbox)
                self.results_stack.set_visible_child_name("results")
            else:
                self.results_stack.set_visible_child_name("results_placeholder")
                print(self.results_stack.get_visible_child_name())

    def on_search_done(self, results, error, query, entry, *args, **kwargs):
        if query == entry.get_text():
            print("entitypopover: search done:", query)
            try:
                listbox = self.results_listbox
                listbox.foreach(listbox.remove)
                set_text(self.variable_title, query, query)
                pango_label(self.variable_title, 'bold')
                if self.variables != None:
                    self.variables_set_results(listbox, query=query)
                if self.variables or results:
                    self.results_stack.set_visible_child_name("results")
                else:
                    set_text(self.results_nope_query, query, query)
                    self.entity_new.connect("clicked", self.entity_new_clicked_cb, query)
                    self.results_stack.set_visible_child_name("results_nope")
                for r in results:
                    if r['URI'] != self.entity['URI']:
                        entity = SidebarEntity(r, URI=False, button=True)
                        entity.image_button.set_from_icon_name('focus-windows-symbolic', IconSize.BUTTON)
                        entity.button.connect("clicked", self.new_window_clicked_cb, r)

                        row = ListBoxRow()
                        row.child = entity
                        row.add(entity)
                        listbox.add(row)
                listbox.show_all()
                self.set_search_placeholder(False)
            except Exception as e:
                raise e

    def entity_new_clicked_cb(self, widget, query):
        self.emit("entity-new", query)

    def variables_set_results(self, listbox, query=""):
        listbox.foreach(listbox.remove)
        if hasattr(self.variable_record, 'connection'):
            self.variable_record.disconnect(self.variable_record.connection)
        exact_match = [v for v in self.variables if v["Label"] == query]
        if exact_match:
            label = "Select variable"
            self.variable_record.connection = self.variable_record.connect("clicked",
                                                                           self.object_selected_cb,
                                                                           exact_match[-1])
            selected = any(v["Variable"] for v in exact_match)
            if selected:
                pango_label(self.variable_title, 'ultrabold')
        else:
            label = "Record new variable"
            self.variable_record.connection = self.variable_record.connect("clicked",
                                                                           self.variable_record_clicked_cb)
        set_text(self.variable_subtitle, label, label)

        for v in [v for v in self.variables if v["Label"] and "Variable" in v]:
            if query in v["Label"] and not query == v["Label"]:
                row = ListBoxRow()
                if query:
                    entity = SidebarEntity(v, URI=False)
                else:
                    entity = SidebarEntity(v, URI=False, button1=True)
                    entity.button1.connect("clicked", self.variable_row_set_default_clicked_cb,
                                           v)
                    entity.image_button1.set_from_icon_name('edit-select-symbolic',
                                                            IconSize.BUTTON)
                    entity.button1.set_tooltip_text("Select variable for the query")
                entity.button.connect("clicked", self.delete_variable_clicked_cb,
                                      row, v)
                entity.button.set_tooltip_text("Delete variable")
                row.child = entity
                if v["Variable"]:
                    pango_label(entity.label, 'ultrabold')
                    entity.label.props.attributes = None
                row.add(entity)
                listbox.add(row)
                listbox.show_all()

    def delete_variable_clicked_cb(self, widget, row, entity):
        print("Delete variable callback", entity)
        row.destroy()
        self.variables.remove(entity)
        self.emit("variable-deleted", entity)
        if not self.variables:
            self.hide()

    def set_search_placeholder(self, value):
        try:
            if self.variables != None:
                self.variable_grid.set_visible(not value)
            self.results.set_visible(not value)
        except AttributeError as e:
            raise e

    @Template.Callback()
    def new_window_clicked_cb(self, widget, *cb_args):
        if cb_args:
            payload = list(cb_args)
        else:
            payload = [self.entity]
        self.emit("new-window-clicked", payload)

    def is_variable(self, entity):
        if 'Variable' in entity: return True

    def is_default_variable(self, entity):
        if self.is_variable(entity) and entity["Variable"]:
            return True

    @Template.Callback()
    def variable_set_default_clicked_cb(self, widget):
        if not self.is_default_variable(self.entity):
            self.entity["Variable"] = True
            label = self.search_entry.get_text()
            self.entity["Label"] = label
            self.entity["URI"] = ""
            self.variables.add(self.entity)
            self.entity["Description"] = "selected query variable"
            pango_label(self.variable_title, weight='ultrabold')
            set_text(self.variable_subtitle,
                     self.entity["Description"],
                     self.entity["Description"])
            print("EntityPopover: variable_set_default_clicked_cb")
            self.emit("default-variable-selected", self.entity)
        self.hide()

    def variable_row_set_default_clicked_cb(self, widget, entity):
        entity["Variable"] = True
        self.object_selected_cb(widget, entity)
        self.hide()

    def variable_record_clicked_cb(self, widget):
        print("Variable record button: clicked")
        print("Variable record callback: I am setting the popover entity to the query",
        self.search_entry.get_text())
        self.entity["Variable"] = False
        self.entity["URI"] = ""
        self.entity["Label"] = self.search_entry.get_text()
        pango_label(self.variable_title, weight='bold')
        self.variables.add(self.entity)
        self.entity["Description"] = "query variable"
        self.emit("object-selected", self.entity)
        self.hide()

    def object_selected_cb(self, widget, entity):
        print("Object selected callback with argument", entity)
        for field in entity:
            self.entity[field] = entity[field]
        if entity["URI"] and self.is_variable(self.entity):
            del self.entity["Variable"]
        if self.is_default_variable(self.entity):
            print("The entity is default, emitting default variable selected signal")
            self.emit("default-variable-selected", self.entity)
        else:
            self.emit("object-selected", self.entity)
        self.hide()

    @Template.Callback()
    def results_listbox_row_activated_cb(self, listbox, row):
        sidebar_entity = row.child
        entity = sidebar_entity.entity
        self.object_selected_cb(sidebar_entity, entity)
        self.hide()

#    @Template.Callback()
#    def visibility_notify_event_cb(self, popover):
#        if popover.get_visible():
#            if self.variables:
#                self.variable_grid.set_visible(False)
#                self.search_box.set_visible(False)
#                self.variables_set_results()
#                self.results.set_visible(True)
