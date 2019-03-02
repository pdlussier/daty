# -*- coding: utf-8 -*-

#    Page
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gtk import Frame, Label, ScrolledWindow, Template
from threading import Thread

from .property import Property
from .value import Value
from .values import Values
from .util import MyThread, download_light

@Template.from_resource("/ml/prevete/Daty/gtk/page.ui")
class Page(ScrolledWindow):

    __gtype_name__ = "Page"

    __gsignals__ = {'new-window-clicked':(sf.RUN_LAST,
                                          TYPE_NONE,
                                          (TYPE_PYOBJECT,))}

    image = Template.Child("image")
    statements = Template.Child("statements")

    def __init__(self, entity, *args, **kwargs):
        ScrolledWindow.__init__(self, *args, **kwargs)

        claims = entity['claims']

        if not 'P18' in claims:
            self.image.set_visible(False)

        for i,P in enumerate(claims):
            download_light(P, self.load_property, i)
            N = len(claims[P])
            if N > 5:
                frame = ScrolledWindow()
                frame.set_min_content_height(36*6)
            else:
                frame = Frame()
            frame.set_shadow_type(2)
            frame.set_visible(True)
            values = Values()
            frame.add(values)
            self.statements.attach(frame, 1, i, 2, 1)
            for claim in claims[P]:
                claim = claim.toJSON()
                self.load_value_async(claim, values)

    def load_property(self, URI, prop, error, i):
        try:
            if error:
                print(error)
            prop = Property(prop)
            self.statements.attach(prop, 0, i, 1, 1)
            return None
        except Exception as e:
            print(URI)
            raise e

    def load_value_async(self, claim, values):
        def do_call():
            error = None
            try:
                pass
            except Exception as err:
                error = err
            idle_add(lambda: self.on_value_complete(claim, values, error))#,
                     #priority=PRIORITY_LOW)
        thread = MyThread(target = do_call)
        thread.start()

    def on_value_complete(self, claim, values, error):
        if error:
            print(error)
        value = Value(claim=claim)
        value.connect("new-window-clicked", self.new_window_clicked_cb)
        value.connect('references-toggled', values.references_toggled_cb)
        values.add(value)
        values.show_all()
        return None

    def new_window_clicked_cb(self, value, entity):
        self.emit("new-window-clicked", entity)

#    def references_toggled_cb(self, widget, state):
#        print(widget)
#        print(state)
#        if state:


    #TODO: make method to move properties from side to top when content_box is folded
