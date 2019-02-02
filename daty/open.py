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

#import asyncio
from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import Align, IconTheme, ListBox, ListBoxRow, Template, Window, main_quit
from threading import Thread

from .entityselectable import EntitySelectable
from .triplet import Triplet
from .wikidata import Wikidata

name = 'ml.prevete.Daty'

@Template.from_resource("/ml/prevete/Daty/gtk/open.ui")
class Open(Window):
    __gtype_name__ = "Open"

    wikidata = Wikidata()

    #properties = Template.Child("properties")
    content_stack = Template.Child("content_stack")
    header_bar = Template.Child("header_bar")
#    header_bar_stack = Template.Child("header_bar_stack")
    search_stack = Template.Child("search_stack")
    constraint_button_box = Template.Child("constraint_button_box")
    constraint_listbox = Template.Child("constraint_listbox")
    constraint_search = Template.Child("constraint_search")
    open_session = Template.Child("open_session")
    page = Template.Child("page")
    placeholder_back = Template.Child("placeholder_back")
    label_listbox = Template.Child("label_listbox")
    open_button = Template.Child("open_button")
    results = Template.Child("results")
    search_box = Template.Child("search_box")
    search_entry = Template.Child("search_entry")
    subtitle = Template.Child("subtitle")
    title = Template.Child("title")

    def __init__(self, load, *args, new_session=True, quit_cb=None, verbose=False):
        Window.__init__(self, *args)

        # Set window icon
        icon = lambda x: IconTheme.get_default().load_icon((name), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        self.verbose = verbose
        self.new_session = new_session

        if quit_cb:
            self.quit_cb = quit_cb
            self.connect("delete-event", self.on_quit)
        #self.show_all()
        self.show()

        constraint = ListBoxRow()
        constraint.add(Triplet())
        self.constraint_listbox.add(constraint)
        self.constraint_listbox.show_all()

        self.label_listbox.selected = []

        if new_session:
            self.set_search_placeholder(True)
              
        else:
            self.set_search_placeholder(False, search_stack="label_search")

        self.entities = self.label_listbox.selected

        self.open_button.connect('clicked', self.open_button_clicked_cb, load)

    def on_quit(self, widget, event):
        self.quit_cb()

    def set_search_placeholder(self, value, search_stack="label_search"):
        self.title.set_visible(value)
        self.subtitle.set_visible(value)
        self.open_button.set_visible(not value)
        self.results.set_visible(not value)
        child = self.page.get_child_at(0,0)
        child.set_property("vexpand", value)
        if value:
            print(child.props)
            self.page.child_set_property(child, "width", 2)
            self.constraint_button_box.props.valign = 1

        else:
            print(child.props)
            self.page.child_set_property(child, "width", 1)
            #child.set_property("vexpand", False)
            self.constraint_button_box.props.valign = 0
            #self.open_button.set_visible(value)
       #if value:
       #    self.header_bar_stack.set_visible_child_name("open_entities")
       #    self.content_stack.set_visible_child_name("placeholder")
       #    self.open_session.set_visible(True)
       #    self.placeholder_back.set_visible(False)
       #    self.open_button.set_visible(False)
       #    self.header_bar.set_show_close_button(True)
       #else:
       #    if self.content_stack.get_visible_child_name() == "placeholder":
       #         self.header_bar_stack.set_visible_child_name("header_search_type")
       #         self.content_stack.set_visible_child_name("search")
       #         self.search_stack.set_visible_child_name(search_stack)
       #         self.open_session.set_visible(False)
       #         self.placeholder_back.set_visible(True)
       #         self.open_button.set_visible(True)
       #         self.header_bar.set_show_close_button(False)

    def open_button_clicked_cb(self, widget, load):
        if self.entities != []:
            load(self.entities)
        self.destroy()

    @Template.Callback()
    def placeholder_back_clicked_cb(self, widget):
        self.set_search_placeholder(True)

    @Template.Callback()
    def placeholder_add_constraint_clicked_cb(self, widget):
        self.set_search_placeholder(False, search_stack="constraints")

    @Template.Callback()
    def key_press_event_cb(self, widget, event):
        #pass
    #    if self.verbose:
    #        print("Keyval of key pressed:", event.keyval)
        # if Esc, set placeholder ot [Right Alt, Tab, Esc, Maiusc, Control, Bloc Maiusc, Left Alt]
        if event.keyval == 65307 and self.new_session:
            #self.set_search_placeholder(True)
            self.search_entry.set_text("")
    #    # else if key is [Right Alt, Tab, Maiusc, Control, Bloc Maiusc, Left Alt]
    #    elif event.keyval in [65027, 65289, 65505, 65509, 65513]:
    #        pass
    #    else:
    #        self.set_search_placeholder(False)

    def on_search_done(self, results, error):
        self.label_listbox.foreach(self.label_listbox.remove)
        for r in results:
            entity = EntitySelectable(r, selected=self.label_listbox.selected)
            row = ListBoxRow()
            row.add(entity)
            self.label_listbox.add(row)
        self.label_listbox.show_all()
        self.set_search_placeholder(False)

    def search(self, query):
        if query:
            query = cp(query)
            wikidata = cp(self.wikidata)
            f = lambda : wikidata.search(query)
            def do_call():
                results, error = None, None
                try:
                    results = f()
                except Exception as err:
                    error = err

                idle_add(lambda: self.on_search_done(results, error))
            thread = Thread(target = do_call)
            thread.start()
        else:
            self.set_search_placeholder(True)

    @Template.Callback()
    def search_entry_search_changed_cb(self, entry):
        self.search(entry.get_text())

    @Template.Callback()
    def label_listbox_row_activated_cb(self, widget, row):
        toggle = row.get_children()[0]
        toggle.set_active(False) if toggle.get_active() else toggle.set_active(True)
