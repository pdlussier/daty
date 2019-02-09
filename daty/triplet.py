# -*- coding: utf-8 -*-

#    Triplet
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
from gi.repository.GLib import idle_add
from gi.repository.Gtk import Grid, Template
from threading import Thread

@Template.from_resource("/ml/prevete/Daty/gtk/triplet.ui")
class Triplet(Grid):
    __gtype_name__ = "Triplet"

    subject = Template.Child("subject")
    property = Template.Child("property")
    object = Template.Child("object")

    def __init__(self, load=None, *args, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        self.load = load

        self.show_all()

    @Template.Callback()
    def button_press_event_cb(self, widget, event):
        from .entitypopover import EntityPopover
        self.entity_popover = EntityPopover("", "Variable", "Nothing",
                                            parent=widget, load=self.load,
                                            search=True)
        self.entity_popover.set_visible(True)

    def search(self, query):
        try:
            if query:
                self.entity_popover
                def do_call():
                    results, error = None, None
                    try:
                        wikidata = Wikidata()
                        results = wikidata.search(query)
                        #results = f()
                    except Exception as err:
                        error = err

                    idle_add(lambda: self.on_search_done(results, error))
                thread = Thread(target = do_call)
                thread.start()
            else:
                self.set_search_placeholder(True)
        except AttributeError as e:
            self.set_search_placeholder(True)

    def set_search_placeholder(self, value):
        try:
            self.entity_popover.search_box.set_visible(value)
            self.entity_popover.results.set_visible(not value)
        except AttributeError as e:
            pass

    def on_search_done(self, results, error):
        try:
            listbox = self.entity_popover.label_listbox
            listbox.foreach(listbox.remove)
            for r in results:
                if r['URI'] != self.URI:
                    entity = SidebarEntity(r, URI=False)#,
                    row = ListBoxRow()
                    row.add(entity)
                    listbox.add(row)
            listbox.show_all()
            self.set_search_placeholder(False)
        except AttributeError as e:
            print("this value type has no popover")
            raise e

    def entry_search_changed_cb(self, entry):
        self.search(entry.get_text())
