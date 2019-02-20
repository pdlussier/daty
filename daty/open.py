# -*- coding: utf-8 -*-

#    Open
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

from copy import deepcopy as cp
from gi import require_version
require_version('Gdk', '3.0')
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.Gdk import CURRENT_TIME
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, CssProvider, IconTheme, ListBox, ListBoxRow, Template, Window, main_quit, show_uri
from platform import system
from pprint import pprint
from re import search as re_search

from .constraintlist import ConstraintList
from .entityselectable import EntitySelectable
from .overlayedlistboxrow import OverlayedListBoxRow
from .roundedbutton import RoundedButton
from .sidebarentity import SidebarEntity
from .triplet import Triplet
from .wikidata import Wikidata
from .util import EntitySet, download_light, search, select

name = 'ml.prevete.Daty'

@Template.from_resource("/ml/prevete/Daty/gtk/open.ui")
class Open(Window):
    __gtype_name__ = "Open"

    wikidata = Wikidata()

    app_menu = Template.Child("app_menu")
    back = Template.Child("back")
    bottom_bar = Template.Child("bottom_bar")
    header_bar = Template.Child("header_bar")
    cancel = Template.Child("cancel")
    constraint_box = Template.Child("constraint_box")
    constraint_viewport = Template.Child("constraint_viewport")
    constraint_button_box = Template.Child("constraint_button_box")
    help = Template.Child("help")
    help_menu = Template.Child("help_menu")
    open_session = Template.Child("open_session")
    page = Template.Child("page")
    open_button = Template.Child("open_button")
    results = Template.Child("results")
    results_listbox = Template.Child("results_listbox")
    select = Template.Child("select")
    select_entities = Template.Child("select_entities")
    select_menu = Template.Child("select_menu")
    search_box = Template.Child("search_box")
    search_entry = Template.Child("search_entry")
    subtitle = Template.Child("subtitle")
    title = Template.Child("title")
    titlebar = Template.Child("titlebar")

    def __init__(self, load, *args, new_session=True, quit_cb=None, verbose=False):
        Window.__init__(self, *args)

        # Set window icon
        icon = lambda x: IconTheme.get_default().load_icon((name), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        self.verbose = verbose
        self.new_session = new_session
        self.load = load
        self.results_listbox.selected = EntitySet()
        self.filtered_results = EntitySet()
        self.entities = self.results_listbox.selected
        self.variables = EntitySet(triplet=False)
        self.hb_title = self.header_bar.get_title()
        self.hb_subtitle = self.header_bar.get_subtitle()

        self.constraint_listbox = ConstraintList()
        self.constraint_viewport.add(self.constraint_listbox)

        if quit_cb:
            self.quit_cb = quit_cb
            self.connect("delete-event", self.on_quit)
        self.show()

        if new_session:
            self.header_bar.set_show_close_button(True)
        else:
            self.header_bar.set_show_close_button(False)
            self.back.set_visible(True)

        self.open_button.connect('clicked', self.open_button_clicked_cb, load)


    def on_quit(self, widget, event):
        self.quit_cb()


    def set_search_placeholder(self, value):
        self.title.set_visible(value)
        self.subtitle.set_visible(value)
        self.help.set_visible(value)
        self.help_menu.set_visible(not value)
        self.select.set_visible(not value)
        #self.open_button.set_visible(not value)
        self.results.set_visible(not value)
        child = self.page.get_child_at(0,0)
        child.set_property("vexpand", value)
        if value:
            self.page.child_set_property(child, "width", 2)
            if not self.constraint_box.get_visible():
                self.constraint_button_box.props.valign = 1
        else:
            self.page.child_set_property(child, "width", 1)
            if not self.constraint_box.get_visible():
                self.constraint_button_box.props.valign = 0

    def open_button_clicked_cb(self, widget, load):
        if self.entities != []:
            load(self.entities)
        self.destroy()

    @Template.Callback()
    def back_clicked_cb(self, widget):
        self.destroy()

    @Template.Callback()
    def app_menu_clicked_cb(self, widget):
        if self.app_menu.get_visible():
            self.app_menu.hide()
        else:
            self.app_menu.set_visible(True)

    @Template.Callback()
    def help_clicked_cb(self, widget):
        print("chitemmuort")
        print(system())
        if system() == 'Linux':
            show_uri (None, "help:daty", CURRENT_TIME)
        if system() == 'Windows':
            from webbrowser import open
            #open(https://)

    @Template.Callback()
    def on_about(self, widget):
        print("cazzi")
        from .aboutdaty import AboutDaty
        about_dialog = AboutDaty(transient_for=self, modal=True)
        about_dialog.present()

    @Template.Callback()
    def add_constraint_clicked_cb(self, widget):
        self.constraint_box.set_visible(True)
        triplet = Triplet(load=self.load, variables=self.variables)
        triplet.connect("default-variable-selected", self.triplets_default_variable_selected_cb)
        triplet.connect("object-selected", self.triplets_check_cb)
        triplet.connect("variable-deleted", self.triplet_variable_deleted_cb)
        row = OverlayedListBoxRow(triplet)
        row.context = row.get_style_context()
        provider = CssProvider()
        provider.load_from_resource('/ml/prevete/Daty/gtk/value.css')
        row.context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION)
        row.context.add_class('unreferenced')

        close_button = RoundedButton(callback=self.triplet_delete,
                                     cb_args=[row])
        close_button.set_visible(True)
        row.revealer.add(close_button)
        self.constraint_listbox.add(row)
        self.constraint_listbox.show_all()

    def triplet_variable_deleted_cb(self, triplet, entity):
        output = self.objects_foreach(self.object_delete, entity)
        for object in (o for o in output if o):
            object.entity["Label"] = "deleted variable"
            object.entity["Description"] = "deleted variable"
            object.entity["URI"] = ""
            del object.entity["Variable"]
            triplet.set_widget(object, object.entity)
        self.triplets_check_cb(triplet, entity)


    def object_delete(self, triplet, object, entity):
        if object.entity == entity:
            return object

    def objects_foreach(self, function, *args):
        output = []
        for row in (r for r in self.constraint_listbox if hasattr(r, 'child')):
            triplet = row.child
            for object in triplet.members:
                output.append(function(triplet, object, *args))
        return output

    def triplet_delete(self, widget, row):
        row.destroy()
        if not [r for r in self.constraint_listbox if hasattr(r, 'child')]:
            self.constraint_box.set_visible(False)


    def triplets_check_cb(self, triplet, entity):
        print("Open: checking triplet")
        triplets = []
        statements = []
        for row in (r for r in self.constraint_listbox if hasattr(r, 'child')):
            triplet = row.child
            entities = [o.entity for o in triplet.members]
            ready = all('Variable' in e or e['URI'] for e in entities)
            #triplets.append(ready)
            if ready:
                statements.append({'s':entities[0],
                                   'p':entities[1],
                                   'o':entities[2]})
                try:
                    row.context.remove_class('unreferenced')
                except:
                    pass
            else:
                row.context.add_class("unreferenced")
        var = [s[r] for s in statements for r in s if "Variable" in s[r] and s[r]["Variable"]]
        if var: var = var[-1]
        if statements and var:
            select(var, statements, self.on_select_done)
            self.set_search_placeholder(False)
        else:
            if not self.search_entry.get_text():
                self.set_search_placeholder(True)

    def on_download_done(self, URI, entity, error):
        if not entity:
            print("problematic URI", URI)
        else:
            entity = SidebarEntity(entity, button=False)
            row = ListBoxRow()
            row.child = entity
            row.add(entity)
            self.results_listbox.add(row)
            self.results_listbox.show_all()

    def on_select_done(self, results):
        if self.results != results:
            self.results_listbox.foreach(self.results_listbox.remove)
            self.filtered_results = results
            if len(results) > 20:
                results = results[:20]
            for URI in results:
                if re_search("^[QP]([0-9]|[A-Z]|-)+([0-9]|[A-Z])$", URI):
                    download_light(URI, self.on_download_done)
                else:
                    entity = {"Label":URI,
                              "Description":"String",
                              "URI":""}
                    self.on_download_done(URI, entity, "")
        #print(results)

    def object_is_empty(self, triplet, object):
        is_var = 'Variable' in object.entity
        has_uri = 'URI' in object.entity and object.entity['URI']
        return any([is_var, has_uri])

    def is_default_variable_set(self, triplet, object):
        if 'Variable' in object.entity and object.entity["Variable"]:
            return object.entity

    def object_is_default_variable(self, triplet, object, entity):
        if 'Variable' in object.entity:
            if object.entity["Label"] == entity["Label"]:
                object.entity["Variable"] = True
                object.entity["Description"] = "selected query variable"
                triplet.set_widget(object, object.entity)
                triplet.set_selected(object, True)
            else:
                object.entity["Variable"] = False
                object.entity["Description"] = "query variable"
                triplet.set_widget(object, object.entity)
                triplet.set_selected(object, False)
        object.popover.search_entry.set_text("")

    def triplets_default_variable_selected_cb(self, triplet, entity):
        print("Open: triplets default variable selected callback")
        self.objects_foreach(self.object_is_default_variable, entity)
        triplet.emit("object-selected", entity)

    @Template.Callback()
    def key_press_event_cb(self, widget, event):
        # if Esc, set placeholder ot [Right Alt, Tab, Esc, Maiusc, Control, Bloc Maiusc, Left Alt]
        if event.keyval == 65307:
            if not self.search_entry.get_text() and not self.new_session:
                self.destroy()
                return None
            self.search_entry.set_text("")

    def on_search_done(self, results, query):
        if query == self.search_entry.get_text():
            self.results_listbox.foreach(self.results_listbox.remove)

            #TODO: Implement selection mode and make single selection the default
            for r in results:
                if self.titlebar.get_selection_mode():
                    entity = EntitySelectable(r,
                                              selected=self.entities,
                                              open_button=self.open_button,
                                              select_entities=self.select_entities)
                else:
                    entity = SidebarEntity(r, button=False)
                row = ListBoxRow()
                row.child = entity
                row.add(entity)
                self.results_listbox.add(row)
            self.results_listbox.show_all()
            self.set_search_placeholder(False)


    @Template.Callback()
    def search_entry_search_changed_cb(self, entry):
        query = entry.get_text()
        if query:
            search(entry.get_text(), self.on_search_done, query)
        else:
            self.set_search_placeholder(True)

    @Template.Callback()
    def results_listbox_row_activated_cb(self, widget, row):
        if self.titlebar.get_selection_mode():
            toggle = row.child #row.get_children()[0]
            toggle.set_active(False) if toggle.get_active() else toggle.set_active(True)
        else:
            self.entities.add(row.child.entity)
            self.load(self.entities)
            self.destroy()

    def set_selection_mode(self, value):
        self.titlebar.set_selection_mode(value)
        self.select.set_visible(not value)
        self.cancel.set_visible(value)
        self.bottom_bar.set_visible(value)
        if value:
            self.header_bar.set_custom_title(self.select_entities)
        else:
            self.header_bar.set_custom_title(None)
        self.results_listbox.foreach(self.set_row_selection, value)

    def set_row_selection(self, row, value):
        entity = row.child.entity
        if value:
            entity = EntitySelectable(entity,
                                      selected=self.entities,
                                      open_button=self.open_button,
                                      select_entities=self.select_entities)
        else:
            entity = SidebarEntity(entity, description=True, button=False)
        row.child.destroy()
        row.add(entity)
        row.child = entity

    @Template.Callback()
    def select_clicked_cb(self, widget):
        if not self.titlebar.get_selection_mode():
            self.set_selection_mode(True)
        else:
            self.set_selection_mode(False)

    @Template.Callback()
    def select_entities_clicked_cb(self, widget):
        self.select_menu.set_visible(True)

    @Template.Callback()
    def select_all_clicked_cb(self, widget):
        self.results_listbox.foreach(self.select_row, True)

    def select_row(self, row, value):
        row.child.set_active(value)

    @Template.Callback()
    def deselect_all_clicked_cb(self, widget):
        self.results_listbox.foreach(self.select_row, False)
