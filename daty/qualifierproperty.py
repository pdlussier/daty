# -*- coding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import EventBox, Template

from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/qualifierproperty.ui")
class QualifierProperty(EventBox):
    __gtype_name__ = "QualifierProperty"

    label = Template.Child("label")
    wikidata = Wikidata()

    def __init__(self, prop, *args, **kwargs):
        EventBox.__init__(self, *args, **kwargs)

        label, tooltip = self.wikidata.get_label(prop), self.wikidata.get_description(prop) 
        self.set_label(label, tooltip)

    def set_label(self, label, tooltip):
        self.label.set_text(label)
        self.label.set_tooltip_text(tooltip)
