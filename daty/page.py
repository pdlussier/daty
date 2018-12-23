# -*- coding: utf-8 -*-


from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ApplicationWindow, IconTheme, Template
from gi.repository.Handy import Column

@Template.from_resource("/org/prevete/Daty/gtk/page.ui")
class Page(Column):
    __gtype_name__ = "Page"

    def __init__(self, *args, **kwargs):
        Column.__init__(self, *args, **kwargs)

