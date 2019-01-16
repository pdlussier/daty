# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import PopoverMenu, Template

from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/entitypopover.ui")
class EntityPopover(PopoverMenu):
    __gtype_name__ = "EntityPopover"

    description = Template.Child("description")
    new_window = Template.Child("new_window")

    def __init__(self, URI, label, description, *args, load=None, parent=None, **kwargs):
        PopoverMenu.__init__(self, *args, **kwargs)

        self.load = load
        self.label = {"Label":label, "Description":description, "URI":URI}

        if parent:
            self.set_relative_to(parent)
        #print(self.description)
        self.description.set_text(description)

    @Template.Callback()
    def new_window_clicked_cb(self, widget):
        self.load([self.label])
