# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.Gtk import Image, Template
from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/loadingpage.ui")
class LoadingPage(Image):
    __gtype_name__ = "LoadingPage"

    def __init__(self, *args, label="", **kwargs):
        Image.__init__(self, *args, **kwargs)
