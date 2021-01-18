# -*- coding: utf-8 -*-

#    Property
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import CssProvider, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION, Button, IconTheme, Template
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT


from .util import set_style
#from .wikidata import Wikidata

@Template.from_resource("/ml/prevete/Daty/gtk/property.ui")
class Property(Button):
    __gtype_name__ = "Property"

    __gsignals__ = {'value-new':(sf.RUN_LAST,
                                 TYPE_NONE,
                                 (TYPE_PYOBJECT,))}

    property_label = Template.Child("property_label")
    popover = Template.Child("popover")
    description = Template.Child("description")
    #values = Template.Child("values")

    def __init__(self, prop, *args, debug=True, **kwargs):
        Button.__init__(self, *args, **kwargs)

        # Styling
        context = self.get_style_context()      
        provider = CssProvider()
        resource = 'ml/prevete/Daty/gtk/property.css'
        provider.load_from_resource(resource)
        context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION) 

        context = self.description.get_style_context()
        set_style(context, resource, 'popover_description', True)

        self.set_label(prop["Label"], prop["Description"])
        self.description.set_text(prop['Description'])
        self.description.set_line_wrap(True)

        if debug:
          print(prop.keys())



    def set_label(self, label, tooltip):
        self.property_label.set_text(label)
        self.property_label.set_tooltip_text(tooltip)

    @Template.Callback()
    def value_new_clicked_cb(self, widget):
        print("value-new emitted")
        self.emit('value-new', self.position)
        self.popover.popdown()

    @Template.Callback()
    def clicked_cb(self, widget):
        print("hi")
        self.popover.popup()
