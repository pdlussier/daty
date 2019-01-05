# -*- coding: utf-8 -*-

from gi.repository.Gtk import CheckButton, Template

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
