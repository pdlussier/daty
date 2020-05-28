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
require_version('Gdk', '3.0')
require_version('Gtk', '3.0')
from gi.repository.Gdk import Event, EventButton, EventKey, KEY_Escape
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gtk import Frame, Label, ScrolledWindow, Template, Viewport
from pprint import pprint
from threading import Thread

from .property import Property
from .value import Value
from .values import Values
from .util import MyThread, download_light

@Template.from_resource("/ml/prevete/Daty/gtk/page.ui")
class Page(ScrolledWindow):

    __gtype_name__ = "Page"

    __gsignals__ = {'claim-changed':(sf.RUN_LAST,
                                     TYPE_NONE,
                                     (TYPE_PYOBJECT,
                                      TYPE_PYOBJECT,
                                      TYPE_PYOBJECT)),
                    'entity-editing':(sf.RUN_LAST,
                                      TYPE_NONE,
                                      (TYPE_PYOBJECT,
                                       TYPE_PYOBJECT,
                                       TYPE_PYOBJECT)),
                    'entity-leaving':(sf.RUN_LAST,
                                      TYPE_NONE,
                                      (TYPE_PYOBJECT,
                                       TYPE_PYOBJECT)),
                    'new-window-clicked':(sf.RUN_LAST,
                                          TYPE_NONE,
                                          (TYPE_PYOBJECT,)),
                    'reference-new-clicked':(sf.RUN_LAST,
                                             TYPE_NONE,
                                             (TYPE_PYOBJECT,
                                              TYPE_PYOBJECT,)),}

    image = Template.Child("image")
    statements = Template.Child("statements")

    references_toggled = 1

    def __init__(self, entity, *args, new=False, **kwargs):
        ScrolledWindow.__init__(self, *args, **kwargs)

        claims = entity['claims']

        if not 'P18' in claims:
            self.image.set_visible(False)

        for i,P in enumerate(claims):
            download_light(P, self.load_property, i)
            N = len(claims[P])
            if N > 5:
                frame = ScrolledWindow()
                frame.height = 36*6
                frame.set_min_content_height(frame.height)
            else:
                frame = Frame()
            frame.set_shadow_type(2)
            frame.set_visible(True)
            values = Values()
            values.connect("reference-toggled", self.reference_toggled_cb, frame)

            frame.add(values)
            self.statements.attach(frame, 1, i, 3, 1)
            for claim in claims[P]:
                claim = claim.toJSON()
                self.load_value_async(claim, values)

    def reference_toggled_cb(self, values, state, frame):
        if type(frame) == ScrolledWindow:
            if state:
                self.references_toggled += 1
            else:
                self.references_toggled -= 1
            frame.set_min_content_height(frame.height*min(self.references_toggled, 3))

    @Template.Callback()
    def statement_add_clicked_cb(self, widget):
        print("deve comparire una barra di ricerca")


    def load_property(self, URI, prop, error, i):
        try:
            if error:
                print(error)
            prop = Property(prop)
            prop.connect('value-new', self.property_value_new_clicked_cb)
            prop.position, prop.size = (0,i), (1,1)
            self.statements.attach(prop, *prop.position, *prop.size)
            return None
        except Exception as e:
            print(URI)
            raise e

    def property_value_new_clicked_cb(self, property, original_position):
        get_top = lambda x: self.statements.child_get_property(x, 'top-attach')
        property_top_value = get_top(property)
        for x in self.statements.get_children():
            if get_top(x) == property_top_value:
                while type(x) in (Frame, ScrolledWindow, Viewport):
                    x = x.get_children()[0]
                    values = x
        while not type(x) == Value:
            x = x.get_children()[0]
            value = x
        print(value.entity)
        print(values.get_children()[0].get_children())
        claim = {'mainsnak':{'snaktype':'value',
                             'datavalue':{'type':'wikibase-entityid',
                                          'value':{'entity-type':'item',
                                                   'numeric-id':1}},
                             'datatype':'wikibase-item'}}
        #value = Value(claim=claim, new=True)
        #values.insert(value,0)
        value = Value(claim={}, new=True)
        values.add(value)
        values.show_all()
        #event = EventButton()
        #value.entity.value_eventbox.do_button_press_event(self, event)
        #value.entity.set_visible_child_name('entry')
        #value.entity.entry.grab_focus()
        #values.show_all()


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
        value.connect("entity-editing", self.entity_editing_cb)
        value.connect("entity-leaving", self.entity_leaving_cb)
        value.connect("claim-changed", self.claim_changed_cb)
        value.connect("new-window-clicked", self.new_window_clicked_cb)
        value.connect("reference-new-clicked", self.reference_new_clicked_cb)
        value.connect('references-toggled', values.references_toggled_cb)
        values.add(value)
        values.show_all()
        return None

    def reference_new_clicked_cb(self, value, entity):
        self.emit("reference-new-clicked", value, entity)
        return True

    def entity_leaving_cb(self, value, entity):
        print("Page: entity leaving")
        self.emit("entity-leaving", value, entity)
        return True

    def entity_editing_cb(self, value, entity, popover):
        self.emit("entity-editing", value, entity, popover)
        #self.entity_popover_connection = self.connect("button-press-event",
        #                                              self.button_press_event_cb,
        #                                              entity,
        #                                              popover)

    def button_press_event_cb(self, widget, event, entity, popover):
        print(event)
        popover.set_visible(False)
        entity.set_visible_child_name("view")
        try:
            self.disconnect(self.entity_popover_connection)
        except Exception as e:
            print(e)

    def claim_changed_cb(self, value, claim, target):
        self.emit("claim-changed", claim, target, value)

    def new_window_clicked_cb(self, value, entity):
        self.emit("new-window-clicked", entity)

#    def references_toggled_cb(self, widget, state):
#        print(widget)
#        print(state)
#        if state:


    #TODO: make method to move properties from side to top when content_box is folded
