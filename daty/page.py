# -*- coding: utf-8 -*-


from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ApplicationWindow, IconTheme, Template
from gi.repository.Handy import Leaflet

@Template.from_resource("/org/prevete/Daty/gtk/page.ui")
class Page(Leaflet):
    __gtype_name__ = "Page"

    def __init__(self, *args, **kwargs):
        pass
        #ApplicationWindow.__init__(self, *args, **kwargs)
        #icon = lambda x: IconTheme.get_default().load_icon(("accessories-dictionary"), x, 0)
        #icons = [icon(size) for size in [32, 48, 64, 96]];

        #self.show_all()
    
