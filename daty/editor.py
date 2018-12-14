# -*- coding: iso-8859-15 -*-


from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ApplicationWindow, Template

@Template.from_resource("/org/prevete/Daty/editor.ui")
class Editor(ApplicationWindow):
    __gtype_name__ = "Editor"

    def __init__(self, *args, **kwargs):
        ApplicationWindow.__init__(self, *args, **kwargs)
        self.show_all()
    
