# -*- coding: utf-8 -*-

from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import ApplicationWindow, IconTheme, Template
from pprint import pprint
from threading import Thread

from .page import Page
from .open import Open
from .sidebarentity import SidebarEntity
from .sidebarlist import SidebarList

from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/editor.ui")
class Editor(ApplicationWindow):
    __gtype_name__ = "Editor"

    # Title bar
    titlebar = Template.Child("titlebar")

    # Header bar
    select_entities = Template.Child("select_entities")
    cancel_entities_selection = Template.Child("cancel_entities_selection")
    app_menu = Template.Child("app_menu")
    app_menu_popover = Template.Child("app_menu_popover")

    # Sub header bar
    item_stack = Template.Child("item_stack")

    # Sidebar 
    sidebar_viewport = Template.Child("sidebar_viewport")

    # Content
    content_box = Template.Child("content_box")
    content_stack = Template.Child("content_stack")

    # Specific
    pages = Template.Child("pages")

    # Common
    common = Template.Child("common-viewport")

    # Test
    label_test = Template.Child("label-test")

    wikidata = Wikidata()

    def __init__(self, *args, entities=[], **kwargs):
        """Editor class

            Args:
                entities (list): of dict having keys"Label", "URI", "Description";
        """
        ApplicationWindow.__init__(self, *args, **kwargs)

        # Set window icon
        icon = lambda x: IconTheme.get_default().load_icon(("daty"), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        # Init sidebar
        self.sidebar_list = SidebarList(self.pages)
        self.sidebar_viewport.add(self.sidebar_list)

        # Parse args
        if entities:
            self.load(entities)
        else:
            Open(new_session=True, parent=self)

    def load(self, entities):
        """Open entities

            Args:
                entities (list): of dict having "URI", "Label", "Description" keys;
        """
        for entity in entities:
            self.download(entity)
        self.show()

    def download(self, entity):
        """Asynchronously download entity from wikidata
        
            Args:
                entity (dict): have keys "URI", "Label", "Description"
        """
        entity = cp(entity)
        wikidata = cp(self.wikidata)
        def do_call():
            entity['Data'] = wikidata.download(entity['URI'])
            idle_add(lambda: self.on_download_done(entity))
        thread = Thread(target = do_call)
        thread.start()

    def on_download_done(self, entity):
        """Gets executed when download method has finished its task

            It creates sidebar passing downloaded data to its rows.

            Args:
                entity (dict): have keys "URI", "Label", "Description", "Data"
        """

        # Sidebar
        sidebar_entity = SidebarEntity(entity, description=False)
        self.sidebar_list.add(sidebar_entity)
        self.sidebar_list.show_all()

        # Page
        #page = Page(entity)
        #self.pages.add_titled(page, e['URI'], label)
        #self.pages.show_all()

    @Template.Callback()
    def new_item_clicked_cb(self, widget):
        """New item button clicked callback

            If clicked, it opens the 'open new entities' window.

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        Open(new_session=False)

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
        if value:
            self.titlebar.set_selection_mode(True)
            self.app_menu.set_visible(False)
            self.select_entities.set_visible(False)
            self.cancel_entities_selection.set_visible(True)
        else:
            self.titlebar.set_selection_mode(False)
            self.cancel_entities_selection.set_visible(False)
            self.app_menu.set_visible(True)
            self.select_entities.set_visible(True)

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
    def check_resize_cb(self, window):
        """Window resizing callback

            Puts window in single/double column editing mode depending on
            Handy.Leaflet folded status (waiting for libhandy:#6).

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        if self.content_box.props.folded and self.titlebar.get_selection_mode():
            self.item_stack.set_visible_child_name("column_switcher")
            if self.label_test in self.common:
                self.common.remove(self.label_test)
                self.content_stack.add_titled(self.label_test, "common", "Common")
        else:
            self.item_stack.set_visible_child_name("item_button")
            if self.label_test in self.content_stack.get_children():
                self.content_stack.remove(self.label_test)
                self.common.add(self.label_test)
