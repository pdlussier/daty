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

    widget = Template.Child("widget")
    label = Template.Child("label")
    description = Template.Child("description")

    def __init__(self, entity, *args, parent=None):
        CheckButton.__init__(self, *args)
       
        self.parent = parent 
        self.entity = entity 
        self.label.set_text(entity['Label'])
        self.description.set_text(entity['Description'])
        self.show_all()

    @Template.Callback()
    def toggled_cb(self, widget):
        if self.parent:
            if widget.get_active():
                self.parent.objects.append(self.entity) 
            else:
                self.parent.objects.remove(self.entity)
