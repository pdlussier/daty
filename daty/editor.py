# -*- coding: utf-8 -*-


from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ApplicationWindow, IconTheme, Label, Template

from .page import Page

@Template.from_resource("/org/prevete/Daty/editor.ui")
class Editor(ApplicationWindow):
    __gtype_name__ = "Editor"

    content_box = Template.Child("content_box")

    def __init__(self, *args, **kwargs):
        ApplicationWindow.__init__(self, *args, **kwargs)
        icon = lambda x: IconTheme.get_default().load_icon(("accessories-dictionary"), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        #self.content_box.add(Page())

        self.show_all()
    
