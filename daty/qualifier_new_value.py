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

from .util import set_style
#from .wikidata import Wikidata

@Template.from_resource("/ml/prevete/Daty/gtk/qualifier_new_value.ui")
class QualifierNewValue(Button):
    __gtype_name__ = "QualifierNewValue"

    #property_label = Template.Child("property_label")
    #values = Template.Child("values")

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)

        # Styling
        context = self.get_style_context()
        resource = '/ml/prevete/Daty/gtk/qualifier_new_value.css'
        set_style(context, resource, 'value', True)
