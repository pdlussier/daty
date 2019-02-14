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
                    'variable-deleted':(sf.RUN_LAST,
                                       TYPE_NONE,
                                       (TYPE_PYOBJECT,)),
                    'object-selected':(sf.RUN_LAST,
                                       TYPE_NONE,
                                       (TYPE_PYOBJECT,))}

    label = Template.Child("label")
    description = Template.Child("description")
    entity_grid = Template.Child("entity_grid")
    new_window = Template.Child("new_window")
    results = Template.Child("results")
    results_listbox = Template.Child("results_listbox")
    search_box = Template.Child("search_box")
    search_entry = Template.Child("search_entry")
    search_subtitle = Template.Child("search_subtitle")
    variable_grid = Template.Child("variable_grid")
    variable_record = Template.Child("variable_record")
    variable_title = Template.Child("variable_title")
    variable_subtitle = Template.Child("variable_subtitle")

    def __init__(self, entity, *args, load=None, parent=None,
                 variables=None, **kwargs):
        PopoverMenu.__init__(self, *args, **kwargs)

        self.load = load
        self.variables = variables
        self.entity = entity
        if self.variables != None:
            self.entity_grid.set_visible(False)
            subtitle = "Search for entities or\n<i>define new variables</i>"
            set_text(self.search_subtitle, subtitle, subtitle, markup=True)
            self.set_modal(True)
            self.search_entry.set_visible(True)
            self.search_entry.connect("search-changed",
                                      self.search_entry_search_changed_cb)

        if parent:
            self.set_relative_to(parent)
        set_text(self.label, entity["Label"], entity["Label"])
        set_text(self.description, entity["Description"], entity["Description"])

    def search_entry_search_changed_cb(self, entry):
        query = entry.get_text()
        if query:
            search(query, self.on_search_done, query)
        else:
            if self.variables:
                self.variable_grid.set_visible(False)
                self.variables_set_results()
            else:
                self.set_search_placeholder(True)

    def on_search_done(self, results, query, *args, **kwargs):
        try:
            set_text(self.variable_title, query, query)
            pango_label(self.variable_title, 'bold')
            self.variables_set_results(query=query)
            listbox = self.results_listbox
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

    def variables_set_results(self, query=""):
        listbox = self.results_listbox
        listbox.foreach(listbox.remove)
        exact_match = [v for v in self.variables if v["Label"] == query]
        if exact_match:
            label = "Select variable"
            selected = any(v["Variable"] for v in exact_match)
            if selected:
                pango_label(self.variable_title, 'ultrabold')
            self.variable_record.connect("clicked", self.object_selected_cb,
                                         exact_match[-1])
        else:
            label = "Record new variable"
            self.variable_record.connect("clicked", self.variable_record_clicked_cb)
        set_text(self.variable_subtitle, label, label)

        for v in [v for v in self.variables if v["Label"]]:
            if query in v["Label"] and not query == v["Label"]:
                row = ListBoxRow()
                entity = SidebarEntity(v, URI=False, button=True)
                entity.button.connect("clicked", self.delete_variable_clicked_cb,
                                          row, v)
                if v["Variable"]:
                    pprint(v)
                    pango_label(entity.label, 'ultrabold')
                    entity.label.props.attributes = None
                row.add(entity)
                listbox.add(row)
                listbox.show_all()

    def delete_variable_clicked_cb(self, widget, row, entity):
        row.destroy()
        self.variables.remove(entity)
        entity["Label"] = ""
        entity["Description"] = ""
        entity["URI"] = ""
        del entity["Variable"]
        self.emit("variable-deleted")

    def set_search_placeholder(self, value):
        try:
            self.search_box.set_visible(value)
            if self.variables != None:
                self.variable_grid.set_visible(not value)
            else:
                self.entity_grid.set_visible(not value)
            self.results.set_visible(not value)
        except AttributeError as e:
            pass

    @Template.Callback()
    def new_window_clicked_cb(self, widget, *cb_args):
        if cb_args:
            self.load(cb_args)
        else:
            self.load([self.entity])

    def set_results(self, widget):
        pass

    @Template.Callback()
    def variable_set_default_clicked_cb(self, widget):
        if not ('Variable' in self.entity and self.entity['Variable']):
            label = self.search_entry.get_text()
            self.entity["Variable"] = True
            self.entity["Label"] = label
            self.entity["URI"] = ""
            self.variables.add(self.entity)
            self.entity["Description"] = "selected query variable"
            pango_label(self.variable_title, weight='ultrabold')
            set_text(self.variable_subtitle,
                     self.entity["Description"],
                     self.entity["Description"])
            self.emit("default-variable-selected", self.entity)
        self.hide()

    @Template.Callback()
    def variable_record_clicked_cb(self, widget):
        if (not "Variable" in self.entity or not self.entity["Variable"]):
            print("sto settando la variabile su false perche' la condizione non funziona")
            self.entity["Variable"] = False
            self.entity["URI"] = ""
            self.entity["Label"] = self.search_entry.get_text()
            pango_label(self.variable_title, weight='bold')
            self.variables.add(self.entity)
            self.entity["Description"] = "query variable"
            self.emit("object-selected", self.entity)
        elif "Variable" in self.entity and self.entity["Variable"]:
            print("hi")
            self.emit("default-variable-selected", self.entity)
        self.hide()

    def object_selected_cb(self, widget, entity):
        self.entity = entity
        pass

    @Template.Callback()
    def results_listbox_row_activated_cb(self, listbox, row):
        self.entity = row.child.entity
        #self.emit("variable-selected")
        self.hide()
