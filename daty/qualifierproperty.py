# -*- coding: utf-8 -*-

#    QualiferProperty
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
from gi.repository.Gtk import EventBox, Template

from .wikidata import Wikidata

@Template.from_resource("/ml/prevete/Daty/gtk/qualifierproperty.ui")
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
