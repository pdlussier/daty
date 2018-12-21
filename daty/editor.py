# -*- coding: utf-8 -*-


from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ApplicationWindow, IconTheme, Label, Template

from .page import Page

@Template.from_resource("/org/prevete/Daty/gtk/editor.ui")
class Editor(ApplicationWindow):
    __gtype_name__ = "Editor"

    app_menu = Template.Child("app_menu_popover")
    content_box = Template.Child("content_box")

    def __init__(self, *args, **kwargs):
        ApplicationWindow.__init__(self, *args, **kwargs)
        icon = lambda x: IconTheme.get_default().load_icon(("daty"), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        #self.content_box.add(Page())

        self.show_all()

    @Template.Callback()
    def app_menu_clicked_cb(self, widget):
        if self.app_menu.get_visible():
            self.app_menu.hide()
        else:
            self.app_menu.set_visible(True)
