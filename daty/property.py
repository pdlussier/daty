# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import CssProvider, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION, Button, IconTheme, Label, Template

from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/property.ui")
class Property(Button):
    __gtype_name__ = "Property"

    property_label = Template.Child("property_label")
    #values = Template.Child("values")

    def __init__(self, *args, label="", **kwargs):
        Button.__init__(self, *args, **kwargs)

        context = self.get_style_context()      
        provider = CssProvider()
        provider.load_from_resource('/org/prevete/Daty/gtk/property.css')
        context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION) 
        
        self.set_label(label)

    def set_label(self, label):
        self.property_label.set_text(label)
