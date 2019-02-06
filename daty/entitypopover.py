# -*- coding: utf-8 -*-

#    EntityPopover
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
from gi.repository.Gtk import PopoverMenu, Template

from .wikidata import Wikidata

@Template.from_resource("/ml/prevete/Daty/gtk/entitypopover.ui")
class EntityPopover(PopoverMenu):
    __gtype_name__ = "EntityPopover"

    label = Template.Child("label")
    label_listbox = Template.Child("label_listbox")
    description = Template.Child("description")
    new_window = Template.Child("new_window")
    results = Template.Child("results")
    search_box = Template.Child("search_box")

    def __init__(self, URI, label, description, *args, load=None, parent=None, **kwargs):
        PopoverMenu.__init__(self, *args, **kwargs)

        self.load = load
        self.entity = {"Label":label, "Description":description, "URI":URI}

        if parent:
            self.set_relative_to(parent)
        self.label.set_text(label)
        self.description.set_text(description)

    @Template.Callback()
    def new_window_clicked_cb(self, widget):
        self.load([self.entity])

    def set_results(self, widget):
        pass          
