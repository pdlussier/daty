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
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gtk import ApplicationWindow, IconTheme, IMContext, Label, Template, Separator, SearchEntry
from gi.repository.Handy import Column
from pprint import pprint
from threading import Thread

from .entityselectable import EntitySelectable
from .loadingpage import LoadingPage
from .open import Open
from .sidebarentity import SidebarEntity
from .sidebarlist import SidebarList
from .util import MyThread
from .wikidata import Wikidata

name = "ml.prevete.Daty"

@Template.from_resource("/ml/prevete/Daty/gtk/editor.ui")
class Editor(ApplicationWindow):
    __gtype_name__ = "Editor"

    # Title bar
    titlebar = Template.Child("titlebar")
    header_box = Template.Child("header_box")

    # Header bar
    header_bar = Template.Child("header_bar")
    select_entities = Template.Child("select_entities")
    cancel_entities_selection = Template.Child("cancel_entities_selection")
    app_menu = Template.Child("app_menu")
    app_menu_popover = Template.Child("app_menu_popover")

    # Sub header bar
    sub_header_bar = Template.Child("sub_header_bar")
    entity_back = Template.Child("entity_back")
    entity_stack = Template.Child("entity_stack")
    item_button = Template.Child("item_button")
    entity = Template.Child("entity")
    description = Template.Child("description")

    # Sidebar
    sidebar = Template.Child("sidebar")
    #sidebar_search_bar = Template.Child("sidebar_search_bar")
    #sidebar_search_entry = Template.Child("sidebar_search_entry")
    sidebar_viewport = Template.Child("sidebar_viewport")

    # Content
    content_box = Template.Child("content_box")
    content_stack = Template.Child("content_stack")
    single_column = Template.Child("single_column")

    # Specific
    entity_search_bar = Template.Child("entity_search_bar")
    entity_search_entry = Template.Child("entity_search_entry")
    pages = Template.Child("pages")

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

        # Set window icon
        icon = lambda x: IconTheme.get_default().load_icon((name), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        #self.common.set_visible(False)

        # Init sidebar
        self.sidebar_list = SidebarList(self.single_column,
                                        self.header_box,
                                        self.pages, 
                                        self.entity,
                                        self.description,
                                        self.entity_search_entry,
                                        load=self.load)
        self.sidebar_viewport.add(self.sidebar_list)

        #self.sidebar_search_bar.set_search_mode(True)

        # Init pages
        loading = LoadingPage()
        self.pages.add_titled(loading, "loading", "Loading")

        # Parse args
        self.max_pages = max_pages
        if entities:
            self.load(entities)
        else:
            Open(self.load, quit_cb=quit_cb, new_session=True)

    def load(self, entities):
        """Open entities

            Args:
                entities (list): of dict having "URI", "Label", "Description" keys;
        """
        for entity in entities:
            self.download(entity, self.load_row_async)
        self.show()

    def download(self, entity, callback):
        """Asynchronously download entity from wikidata
        
            Args:
                entity (dict): have keys "URI", "Label", "Description"
        """
        entity = cp(entity)
        wikidata = cp(self.wikidata)
        def do_call():
            entity['Data'] = wikidata.download(entity['URI'])
            if not entity['Label']:
                entity['Label'] = wikidata.get_label(entity['Data'])
            if not entity['Description']:
                entity['Description'] = wikidata.get_description(entity['Data'])
            idle_add(lambda: callback(entity))
        thread = MyThread(target = do_call)
        thread.start()

    def load_row_async(self, entity):
        """It creates sidebar passing downloaded data to its rows.

            Gets executed when download method has finished its task

            Args:
                entity (dict): have keys "URI", "Label", "Description", "Data"
        """
        entity = cp(entity)
        f = lambda : entity
        def do_call():
            entity = f()
            idle_add(lambda: self.on_row_complete(entity))
        thread = MyThread(target = do_call)
        thread.start()

    def on_row_complete(self, entity):
        sidebar_entity = SidebarEntity(entity, description=True)
        self.sidebar_list.add(sidebar_entity)
        self.sidebar_list.show_all()

    @Template.Callback()
    def new_item_clicked_cb(self, widget):
        """New item button clicked callback

            If clicked, it opens the 'open new entities' window.

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        Open(self.load, new_session=False,)

    @Template.Callback()
    def select_entities_clicked_cb(self, widget):
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
        # App menu
        self.app_menu.set_visible(not value)
        # Select button
        self.select_entities.set_visible(not value)
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
                # WIP: self.sub_header_bar.set_title("test")
                # Set the switcher to something else
                self.entity_stack.set_visible_child_name("item_button")

                # Show sub header properties
                #print(dir(self.sub_header_bar.props))
                #.remove(self.entity_stack)

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
    def key_press_event_cb(self, window, event):
        focused = window.get_focus()
        print(focused)
        if type(focused) == SearchEntry:
            pass
        elif type(focused) == SidebarEntity:
            print("sidebar")
        else:
            #if Esc, set placeholder at [Right Alt, Tab, Esc, Maiusc, Control, Bloc Maiusc, Left Alt]
            if event.keyval == 65307:
                self.entity_search_bar.set_search_mode(False)
            # else if key is [Right Alt, Tab, Maiusc, Control, Bloc Maiusc, Left Alt]
            elif event.keyval in [65027, 65289, 65505, 65509, 65513]:
                pass
            else:
                if not self.entity_search_bar.get_search_mode():
                    #context = IMContext()
                    #context.connect("commit", self.to_entity_search_entry)
                    #context.filter_event()
                    #print("Set search mode True")
                    #self.entity_search_bar.entry.set_visible(True)
                    self.entity_search_bar.set_search_mode(True)
                    #self.entity_search_entry.grab_focus()
                    #self.event
                    #self.entity|search_bar.entry.grab_focus()
