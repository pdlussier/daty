# -*- coding: utf-8 -*-

#    Editor
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
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gdk import KEY_Escape, KEY_Control_L, KEY_Control_R, KEY_Alt_R, KEY_Alt_L, KEY_ISO_Level3_Shift, KEY_ISO_Level3_Lock, KEY_Tab, KEY_Menu, KEY_Up, KEY_Down, KEY_Right, KEY_Left
from gi.repository.Gtk import ApplicationWindow, IconTheme, IMContext, Label, ListBoxRow, Template, Separator, SearchEntry
from gi.repository.Handy import Column
from pprint import pprint
from threading import Thread

from .entityselectable import EntitySelectable
from .loadingpage import LoadingPage
from .open import Open
from .overlayedlistboxrow import OverlayedListBoxRow
from .roundedbutton import RoundedButton
from .sidebarentity import SidebarEntity
from .sidebarlist import SidebarList
from .util import MyThread, download
from .wikidata import Wikidata

name = "ml.prevete.Daty"

modifiers = [KEY_Control_L, KEY_Control_R, KEY_Alt_R, KEY_Alt_L,
             KEY_ISO_Level3_Shift, KEY_ISO_Level3_Lock, KEY_Tab, KEY_Menu,
             KEY_Up, KEY_Down, KEY_Right, KEY_Left]

@Template.from_resource("/ml/prevete/Daty/gtk/editor.ui")
class Editor(ApplicationWindow):
    __gtype_name__ = "Editor"

    # Title bar
    titlebar = Template.Child("titlebar")
    header_box = Template.Child("header_box")

    # Header bar
    header_bar = Template.Child("header_bar")
    entity_new = Template.Child("entity_new")
    entities_search = Template.Child("entities_search")
    entities_select = Template.Child("entities_select")
    cancel_entities_selection = Template.Child("cancel_entities_selection")
    app_menu = Template.Child("app_menu")
    app_menu_popover = Template.Child("app_menu_popover")

    # Sub header bar
    sub_header_bar = Template.Child("sub_header_bar")
    entity_back = Template.Child("entity_back")
    entity_stack = Template.Child("entity_stack")
    entity_button = Template.Child("entity_button")
    entity = Template.Child("entity")
    description = Template.Child("description")
    entity_search = Template.Child("entity_search")

    # Sidebar
    sidebar = Template.Child("sidebar")
    sidebar_search_bar = Template.Child("sidebar_search_bar")
    sidebar_search_entry = Template.Child("sidebar_search_entry")
    sidebar_viewport = Template.Child("sidebar_viewport")

    # Content
    content_box = Template.Child("content_box")
    content_stack = Template.Child("content_stack")
    single_column = Template.Child("single_column")

    # Specific
    entity_search_bar = Template.Child("entity_search_bar")
    entity_search_entry = Template.Child("entity_search_entry")
    pages = Template.Child("pages")

    start_pane_size_group = Template.Child("start_pane_size_group")

    # Separator
#    edit_column_separator = Template.Child("edit_column_separator")

    # Common
    #common = Template.Child("common-viewport")
    #common_page = Template.Child("common_page")

    wikidata = Wikidata()

    def __init__(self, *args, entities=[], quit_cb=None, max_pages=10, **kwargs):
        """Editor class

            Args:
                entities (list): of dict having keys"Label", "URI", "Description";
                max_pages (int): maximum number of pages kept in RAM
        """
        ApplicationWindow.__init__(self, *args, **kwargs)

        self.quit_cb = quit_cb

        # Set window icon
        icon = lambda x: IconTheme.get_default().load_icon((name), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        # Init sidebar
        self.sidebar_list = SidebarList(self.single_column,
                                        self.header_box,
                                        self.pages, 
                                        self.entity,
                                        self.description,
                                        self.entity_search_entry,
                                        self.sidebar_search_entry,
                                        load=self.load,
                                        wikidata=self.wikidata)
        self.sidebar_viewport.add(self.sidebar_list)

        # Init pages
        loading = LoadingPage()
        self.pages.add_titled(loading, "loading", "Loading")

        # Parse args
        self.max_pages = max_pages
        if entities:
            self.load(entities)
        else:
            Open(self.load, quit_cb=self.quit_cb, new_session=True)

    def load(self, entities):
        """Open entities

            Args:
                entities (list): of dict having "URI", "Label", "Description" keys;
        """
        for entity in entities[:-1]:
            download(entity, self.load_row_async,)
        download(entities[-1], self.load_row_async, select=True)
        self.show()

    def load_row_async(self, entity, **kwargs):
        """It creates sidebar passing downloaded data to its rows.

            Gets executed when download method has finished its task

            Args:
                entity (dict): have keys "URI", "Label", "Description", "Data"
        """
        f = lambda : entity
        def do_call():
            entity = f()
            idle_add(lambda: self.on_row_complete(entity, **kwargs))
        thread = MyThread(target = do_call)
        thread.start()

    def on_row_complete(self, entity, **kwargs):

        # Build entity
        if not entity['Label']:
            entity['Label'] = self.wikidata.get_label(entity['Data'])
        if not entity['Description']:
            entity['Description'] = self.wikidata.get_description(entity['Data'])

        sidebar_entity = SidebarEntity(entity, description=True, URI=True)
        sidebar_entity.button.connect("clicked", self.entity_close_clicked_cb,
                                      sidebar_entity)

        row = ListBoxRow()
        row.child = sidebar_entity
        row.add(sidebar_entity)

        self.sidebar_list.add(row, **kwargs)
        self.sidebar_list.show_all()

    @Template.Callback()
    def entity_new_clicked_cb(self, widget):
        """New entity button clicked callback

            If clicked, it opens the 'open new entities' window.

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        Open(self.load, quit_cb=self.quit_cb, new_session=False)

    @Template.Callback()
    def entities_search_toggled_cb(self, widget):
        if widget.get_active():
            self.sidebar_search_bar.set_search_mode(True)
        else:
            self.sidebar_search_bar.set_search_mode(False)

    @Template.Callback()
    def entities_select_clicked_cb(self, widget):
        """Select sidebar entities button clicked callback

            If clicked, activates header bar selection mode.

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        self.set_selection_mode(True)

    @Template.Callback()
    def cancel_entities_selection_clicked_cb(self, widget):
        """Cancel sidebar entities selection button clicked callback

            If clicked, disables header bar selection mode.

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        self.set_selection_mode(False)

    def set_selection_mode(self, value):
        """Toggle selection mode

            Args:
                value (bool): if True, activates selection mode.
        """
        # Titlebar
        self.titlebar.set_selection_mode(value)
        # New entity button
        self.entity_new.set_visible(not value)
        # Entities search button
        self.entities_search.set_visible(value)
        # App menu
        self.app_menu.set_visible(not value)
        # Select button
        self.entities_select.set_visible(not value)
        # Cancel selection button
        self.cancel_entities_selection.set_visible(value)
        # Sidebar
        self.sidebar_list.set_selection_mode(value)
        if value:
            self.column_separator = Separator()
            self.common = Label(label="common")
            self.content_box.add(self.column_separator)
            self.content_box.add(self.common)
            self.content_box.show_all()
        else:
            self.content_box.remove(self.column_separator)
            self.content_box.remove(self.common)

    @Template.Callback()
    def app_menu_clicked_cb(self, widget):
        """Primary menu button clicked callback

            If clicked, open primary menu (app menu).

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        if self.app_menu_popover.get_visible():
            self.app_menu_popover.hide()
        else:
            self.app_menu_popover.set_visible(True)

    @Template.Callback()
    def on_content_box_folded_changed(self, leaflet, folded):
        """Third column folding signal

            If in selection/multi-editing mode, set stack switcher
            depending on window size

            Args:
                leaflet (Handy.Leaflet): the leaflet emitting the signal;
                folded (GParamBoolean): whether it is folded or not.
        """
        # If we are in selection mode
        if self.titlebar.get_selection_mode():
            # If the title is displayed
            if self.content_box.props.folded:
                # Set switcher in the titlebar
                self.entity_stack.set_visible_child_name("column_switcher")

                # Move common page from third column to content_stack
                self.content_box.remove(self.column_separator)
                self.content_box.remove(self.common)
                self.content_stack.add_titled(self.common, "common", "Common")

            else:
                # Set the switcher to something else
                self.entity_stack.set_visible_child_name("entity_button")

                # Move common page from content stack to third column
                self.content_stack.remove(self.common)
                self.content_box.add(self.column_separator)
                self.content_box.add(self.common)

    @Template.Callback()
    def on_single_column_folded_changed(self, leaflet, folded):
        if self.single_column.props.folded:
            self.entity_back.set_visible(True)
        else:
            self.entity_back.set_visible(False)

    @Template.Callback()
    def entity_back_clicked_cb(self, widget):
        self.header_box.set_visible_child(self.header_bar)
        self.single_column.set_visible_child(self.sidebar)

    @Template.Callback()
    def entity_search_toggled_cb(self, widget):
        if widget.get_active():
            self.entity_search_bar.set_search_mode(True)
        else:
            self.entity_search_bar.set_search_mode(False)

    @Template.Callback()
    def key_press_event_cb(self, window, event):
        """Manages editor's key press events

        Args:
            window (Gtk.Window): it is self;
            event (Gdk.Event): the key press event.
        """
        if event.keyval in modifiers:
            return None
        focused = window.get_focus()
        sidebar_entity_focused = type(focused) == ListBoxRow
        sidebar_search_entry_focused = focused == self.sidebar_search_entry
        sidebar_leaflet_focused = self.single_column.get_visible_child_name() == 'sidebar'

        if sidebar_search_entry_focused:
            pass
        elif sidebar_entity_focused or sidebar_leaflet_focused:
            if not self.sidebar_search_bar.get_search_mode():
                self.sidebar_search_bar.set_search_mode(True)
            else:
                self.sidebar_search_entry.grab_focus()
        else:
            if event.keyval == KEY_Escape:
                 if self.titlebar.get_selection_mode():
                     self.set_selection_mode(False)
            else:
                if not self.entity_search_bar.get_search_mode():
                    self.entity_search.set_active(True)
                    self.entity_search_bar.set_search_mode(True)

    @Template.Callback()
    def entity_search_entry_stop_search_cb(self, widget):
        if self.entity_search.get_active():
            self.entity_search.set_active(False)
            self.entity_search_bar.set_search_mode(False)

    def entity_close_clicked_cb(self, widget, sidebar_entity):
        row = sidebar_entity.get_parent()
        print(row)
        URI = sidebar_entity.entity["URI"]
        self.sidebar_list.last = list(filter(lambda x: x != row,
                                             self.sidebar_list.last))
        row.destroy()
        try:
            page = self.pages.get_child_by_name(URI)
            page.destroy()
        except Exception as e:
            print ("page not loaded")

    def get_neighbor(self, i, next=True):
        f = lambda x: x + 1 if next else x - 1
        while True:
            try:
                print(self.sidebar_list.get_children())
                self.sidebar_list.get_row_at_index(i)
                return True
            except AttributeError as e:
                i = f(i)
