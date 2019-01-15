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
    wikidata = Wikidata()

    def __init__(self, prop, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)

        # Styling
        context = self.get_style_context()      
        provider = CssProvider()
        provider.load_from_resource('/org/prevete/Daty/gtk/property.css')
        context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION) 
       
        label, tooltip = self.wikidata.get_label(prop), self.wikidata.get_description(prop) 
        self.set_label(label, tooltip)

    def set_label(self, label, tooltip):
        self.property_label.set_text(label)
        self.property_label.set_tooltip_text(tooltip)
