# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import AboutDialog, Template

@Template.from_resource("/org/prevete/Daty/gtk/aboutdaty.ui")
class AboutDaty(AboutDialog):
    __gtype_name__ = "AboutDaty"

    def __init__(self, *args, **kwargs):
        AboutDialog.__init__(self, *args, **kwargs)
