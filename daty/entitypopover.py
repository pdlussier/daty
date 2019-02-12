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
from gi.repository.GObject import TYPE_NONE, TYPE_STRING
from gi.repository.Gtk import IconSize, ListBoxRow, PopoverMenu, Template

from .roundedbutton import RoundedButton
from .sidebarentity import SidebarEntity
from .util import download, search, set_text

@Template.from_resource("/ml/prevete/Daty/gtk/entitypopover.ui")
class EntityPopover(PopoverMenu):
    __gtype_name__ = "EntityPopover"

    __gsignals__ = {'variable-selected':(sf.RUN_LAST,
                                         TYPE_NONE,
                                        (TYPE_STRING,))}

    label = Template.Child("label")
    description = Template.Child("description")
    entity_grid = Template.Child("entity_grid")
    new_window = Template.Child("new_window")
    results = Template.Child("results")
    results_listbox = Template.Child("results_listbox")
    search_box = Template.Child("search_box")
    search_entry = Template.Child("search_entry")
#    search_title = Template.Child("search_title")
    search_subtitle = Template.Child("search_subtitle")
    variable_grid = Template.Child("variable_grid")
    variable_title = Template.Child("variable_title")
    variable_subtitle = Template.Child("variable_subtitle")

    def __init__(self, entity, *args, load=None, parent=None,
                 search=False, **kwargs):
        PopoverMenu.__init__(self, *args, **kwargs)

        self.load = load
        self.search = search
        self.entity = entity
        #self.entity = {"Label":label, "Description":description, "URI":URI}

        if self.search:
            self.entity_grid.set_visible(False)
            subtitle = "Search for entities or\n<i>define new variables</i>"
            set_text(self.search_subtitle, subtitle, subtitle, markup=True)
            self.set_modal(True)
            self.search_entry.set_visible(True)
            self.search_entry.connect("search-changed",
                                      self.search_entry_search_changed_cb)

        if parent:
            self.set_relative_to(parent)
        self.label.set_text(entity["Label"])
        self.description.set_text(entity["Description"])

    def search_entry_search_changed_cb(self, entry):
        query = entry.get_text()
        if query:
            search(query, self.on_search_done, query)
        else:
            self.set_search_placeholder(True)

    def on_search_done(self, results, query, *args, **kwargs):
        try:
            listbox = self.results_listbox
            listbox.foreach(listbox.remove)
            self.variable_title.set_markup("".join(["<b>",
                                                    query,
                                                    "</b>"]))
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

    def set_search_placeholder(self, value):
        try:
            self.search_box.set_visible(value)
            if self.search:
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
    def select_variable_clicked_cb(self, widget):
        if not ('Variable' in self.entity and self.entity['Variable']):
            label = self.search_entry.get_text()
            self.entity = {"Variable":True,
                           "Label":label}
            label = "".join(["<span font_family='Cantarell Extra Bold' ",
                             "font_weight='ultrabold'>",
                             label,
                             "</span>"])
            self.variable_title.set_markup(label)
            self.variable_title.set_use_markup(True)
            self.variable_subtitle.set_text("Selected query variable")
            self.emit("variable-selected", self.entity["Label"])

    @Template.Callback()
    def record_variable_clicked_cb(self, widget):
        self.entity = {"Variable":False,
                       "Label":self.search_entry.get_text()}
        self.hide()

    @Template.Callback()
    def results_listbox_row_activated_cb(self, listbox, row):
        self.entity = row.child.entity
        self.hide()
