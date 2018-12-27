# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import CheckButton, ListBoxRow, Template, Window
from gi.repository.Gdk import unicode_to_keyval
require_version('Handy', '0.0')
from gi.repository.Handy import Column

@Template.from_resource("/org/prevete/Daty/gtk/entity.ui")
class Entity(CheckButton):
    __gtype_name__ = "Entity"

    label = Template.Child("label")
    description = Template.Child("description")

    def __init__(self, *args, label="Entity", description="Description"):
        CheckButton.__init__(self, *args)
        
        self.label.set_text(label)
        self.description.set_text(description)
        self.show_all()

    #@Template.Callback()
    #def search_entry_search_changed_cb(self, entry):
    #    self.query = entry.get_text()
    #    thread = Thread(target=self.search)
    #    thread.daemon = True
    #    thread.start() 
    #    results = self.wikidata.search(entry.get_text())
    #    #print(results)
