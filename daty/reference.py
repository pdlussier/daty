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
from gi.repository.Gtk import CssProvider, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION
from gi.repository.Gtk import Box, IconTheme, Template

#from .wikidata import Wikidata

@Template.from_resource("/ml/prevete/Daty/gtk/reference.ui")
class Reference(Box):
    __gtype_name__ = "Reference"

    actions = Template.Child("actions")
    grid = Template.Child("grid")
    #new_ref = Template.Child("new_ref")
    #values = Template.Child("values")

    def __init__(self, *args, new=False, **kwargs):
        Box.__init__(self, *args, **kwargs)

        if new:
            #self.new_ref.set_visible(True)
            self.grid.set_visible(False)
            self.props.margin_top = 0
            self.props.margin_bottom = 0

        # Styling
        #context = self.get_style_context()
        #provider = CssProvider()
        #provider.load_from_resource('/ml/prevete/Daty/gtk/reference.css')
        #context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION) 

    @Template.Callback()
    def button_press_event_cb(self, widget, event):
        visible = self.actions.get_visible()
        self.actions.set_visible(not visible)
