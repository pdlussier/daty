# -*- coding: utf-8 -*-

from gi.repository.Gtk import CheckButton, Template

@Template.from_resource("/org/prevete/Daty/gtk/entityselectable.ui")
class EntitySelectable(CheckButton):
    __gtype_name__ = "EntitySelectable"

    widget = Template.Child("widget")
    label = Template.Child("label")
    description = Template.Child("description")
    URI = Template.Child("URI")

    def __init__(self, entity, *args, widget=True, selected=None):
        """Search result widget in 'open new entity' dialog

            Args:
                entity (dict): havig keys "URI, "Label", "Description" and "Data".
                selected (list): keep track of entity's selected status
        """
        CheckButton.__init__(self, *args)
        
        self.entity = entity

        if widget:
            self.label.set_text(entity['Label'])
            self.description.set_text(entity['Description'])
            self.URI.set_text('(' + entity['URI'] + ')')
        else:
            self.label.destroy()
            self.description.destroy()
            self.URI.destroy()

        if selected != None:
            self.connect("toggled", self.toggled_cb, selected)
        self.show_all()

    def toggled_cb(self, widget, selected):
        """Toggled callback

            Args:
                widget (Gtk.Widget): toggled widget (so self);
                selected (list): add self's entity attribute to it to 
                keep track of parent listbox selected toggles.
        """
        if widget.get_active():
            selected.append(self.entity)
        else:
            selected.remove(self.entity)
