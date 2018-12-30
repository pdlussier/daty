# -*- coding: utf-8 -*-


from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ApplicationWindow, IconTheme, ListBoxRow, Template

from .entity import Entity
from .page import Page
from .open import Open
from .sidebarrow import SidebarEntity

@Template.from_resource("/org/prevete/Daty/gtk/editor.ui")
class Editor(ApplicationWindow):
    __gtype_name__ = "Editor"

    app_menu = Template.Child("app_menu_popover")
    entities = Template.Child("entities")
    item_stack = Template.Child("item_stack")
    content_box = Template.Child("content_box")
    content_stack = Template.Child("content_stack")
    #specific_viewport = Template.Child("specific_viewport")
    pages = Template.Child("pages")
    common = Template.Child("common-viewport")
    label_test = Template.Child("label-test")

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

        if entities == []:
            Open(new_session=True, parent=self)
        else:
            self.load_content(entities)

    def load_content(self, entities):
        for e in entities:

            # Sidebar
            entity = SidebarEntity(e, description=False)
            row = ListBoxRow()
            row.entity = e
            row.add(entity)
            self.entities.add(row)

            # Page
            page = Page(entity=e)
            page.show_all()
            self.pages.add_titled(page, e['URI'], e['Label'])
        self.pages.show_all()
        self.entities.show_all()

        #self.specific_viewport.add(Page())

        #self.show_all()

    @Template.Callback()
    def new_item_clicked_cb(self, widget):
        Open(new_session=False)

    @Template.Callback()
    def app_menu_clicked_cb(self, widget):
        if self.app_menu.get_visible():
            self.app_menu.hide()
        else:
            self.app_menu.set_visible(True)

    @Template.Callback()
    def entities_row_activated_cb(self, widget, row):
        self.pages.set_visible_child_name(row.entity['URI'])
        print(self.pages.get_visible_child_name())
        self.pages.show_all()
        #print(row.entity)

    @Template.Callback()
    def check_resize_cb(self, widget):
        if self.content_box.props.folded:
            self.item_stack.set_visible_child_name("column_switcher")
            if self.label_test in self.common:
                self.common.remove(self.label_test)
                self.content_stack.add_titled(self.label_test, "common", "Common")
        else:
            self.item_stack.set_visible_child_name("item_button")
            if self.label_test in self.content_stack.get_children():
                self.content_stack.remove(self.label_test)
                self.common.add(self.label_test)
