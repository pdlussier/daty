# -*- coding: utf-8 -*-

from copy import deepcopy
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import ApplicationWindow, IconTheme, ListBoxRow, Template
from pprint import pprint
from threading import Thread

from .entity import Entity
from .page import Page
from .open import Open
from .sidebarentity import SidebarEntity
from .sidebarlist import SidebarList

from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/editor.ui")
class Editor(ApplicationWindow):
    __gtype_name__ = "Editor"

    select_entities = Template.Child("select_entities")
    cancel_entities_selection = Template.Child("cancel_entities_selection")
    app_menu = Template.Child("app_menu")
    app_menu_popover = Template.Child("app_menu_popover")
    titlebar = Template.Child("titlebar")
    sidebar_viewport = Template.Child("sidebar_viewport")
    item_stack = Template.Child("item_stack")
    content_box = Template.Child("content_box")
    content_stack = Template.Child("content_stack")
    #specific_viewport = Template.Child("specific_viewport")
    pages = Template.Child("pages")
    common = Template.Child("common-viewport")
    label_test = Template.Child("label-test")

    wikidata = Wikidata()

    def __init__(self, *args, entities=[], **kwargs):
        """
        Args:
            entities: [{"Label", "URI", "Description"}]
        """
        ApplicationWindow.__init__(self, *args, **kwargs)

        # Set window icon
        icon = lambda x: IconTheme.get_default().load_icon(("daty"), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        # Init sidebar
        self.sidebar_list = SidebarList(self.pages)
        self.sidebar_viewport.add(self.sidebar_list)


        if entities == []:
            Open(new_session=True, parent=self)
        else:
            self.load_content(entities)

    def on_download_done(self, URI, entity, error):
        if error:
            pprint(error)
        label = self.wikidata.get_label(entity)
        e = {"URI":URI, "Description":"", "Label":label, "Data":entity}

        # Sidebar
        sidebar_entity = SidebarEntity(e, description=False)
        self.sidebar_list.add(sidebar_entity)
        self.sidebar_list.show_all()

        # Page
        #page = Page(entity)
        #self.pages.add_titled(page, e['URI'], label)
        #self.pages.show_all()

    def download(self, URI):
        f = lambda : deepcopy(URI)
        def do_call():
            URI, entity, error = None, None, None
            #try:
            URI, entity = f(), deepcopy(self.wikidata).download(f())
            #except Exception as err:
            #    error = err
            idle_add(lambda: self.on_download_done(URI, entity, error))
        thread = Thread(target = do_call)
        thread.start()

    def load_content(self, entities):
        for e in entities:
            self.download(e['URI'])
        self.show()

    @Template.Callback()
    def new_item_clicked_cb(self, widget):
        Open(new_session=False)

    @Template.Callback()
    def select_entities_clicked_cb(self, widget):
        if not self.titlebar.get_selection_mode():
            self.set_selection_mode(True)
        else:
            self.set_selection_mode(False)

    def set_selection_mode(self, value):
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
    def cancel_entities_selection_clicked_cb(self, widget):
        self.set_selection_mode(False)

    @Template.Callback()
    def app_menu_clicked_cb(self, widget):
        if self.app_menu_popover.get_visible():
            self.app_menu_popover.hide()
        else:
            self.app_menu_popover.set_visible(True)

    @Template.Callback()
    def check_resize_cb(self, widget):
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
