# -*- coding: utf-8 -*-

#    LanguageAdd
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
from gi.repository.Gtk import CssProvider, Label, ListBoxRow, Separator, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION, Window, IconTheme, Template

from .util import set_style
#from .wikidata import Wikidata

name = 'ml.prevete.Daty'

@Template.from_resource("/ml/prevete/Daty/gtk/languageadd.ui")
class LanguageAdd(Window):
    __gtype_name__ = "LanguageAdd"

    cancel = Template.Child("cancel")
    select = Template.Child("select")
    languages = Template.Child("languages")
    search_entry = Template.Child("search_entry")

    def __init__(self, languages, *args, **kwargs):
        Window.__init__(self, *args, **kwargs)

        icon = lambda x: IconTheme.get_default().load_icon((name), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        self.languages.set_header_func(self.update_header)
        for language in languages:
            row = ListBoxRow()
            label = Label()
            label.set_text(language['itemLabel']['value'])
            label.code = language['c']['value']
            row.child = label
            row.add(label)
            self.languages.add(row)
        self.languages.show_all()

    @Template.Callback()
    def cancel_clicked_cb(self, widget):
        self.hide()
        self.destroy()

    @Template.Callback()
    def select_clicked_cb(self, widget):
        pass

    @Template.Callback()
    def search_entry_search_changed_cb(self, entry):
        for row in self.languages.get_children():
            if entry.get_text().lower() in row.child.get_text().lower():
                row.set_visible(True)
                row.set_no_show_all(False)
            else:
                row.set_visible(False)
                row.set_no_show_all(True)
        self.languages.show_all()

    def update_header(self, row, before, *args):
        """See GTK+ Documentation"""
        if before:
            row.set_header(Separator())
