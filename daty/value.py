# -*- coding: utf-8 -*-

#    Value
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


from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
require_version('Gdk', '3.0')
from gi.repository.Gdk import EventType
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gi.repository.GLib import idle_add #, PRIORITY_LOW
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, CssProvider, Grid, IconSize, Separator, StyleContext, Grid, Template
from pprint import pprint

from .entity import Entity
from .entitypopover import EntityPopover
from .qualifier_new_property import QualifierNewProperty
from .qualifier_new_value import QualifierNewValue
from .qualifierproperty import QualifierProperty
from .reference import Reference
from .util import MyThread, download_light, set_style

@Template.from_resource("/ml/prevete/Daty/gtk/value.ui")
class Value(Grid):

    __gtype_name__ = "Value"

    __gsignals__ = {'entity-editing':(sf.RUN_LAST,
                                     TYPE_NONE,
                                     (TYPE_PYOBJECT,
                                      TYPE_PYOBJECT)),
                    'entity-leaving':(sf.RUN_LAST,
                                      TYPE_NONE,
                                      (TYPE_PYOBJECT,)),
                    'edit_new':(sf.RUN_LAST,
                                TYPE_NONE,
                                (TYPE_PYOBJECT,)),
                    'claim-changed':(sf.RUN_LAST,
                                     TYPE_NONE,
                                     (TYPE_PYOBJECT,
                                      TYPE_PYOBJECT)),
                    'new-window-clicked':(sf.RUN_LAST,
                                          TYPE_NONE,
                                          (TYPE_PYOBJECT,)),
                    'reference-new-clicked':(sf.RUN_LAST,
                                      TYPE_NONE,
                                      (TYPE_PYOBJECT,)),
                    'references-toggled':(sf.RUN_LAST,
                                         TYPE_NONE,
                                         (TYPE_PYOBJECT,))}

    button = Template.Child("button")
    actions = Template.Child("actions")
    icon = Template.Child("icon")
    #qualifier_new = Template.Child("qualifier_new")
    qualifiers = Template.Child("qualifiers")
    mainsnak = Template.Child("mainsnak")
    qualifier_new = Template.Child("qualifier_new")
    reference_new = Template.Child("reference_new")

    def __init__(self, claim, *args, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        self.qualifier_row = 0
        self.reference_row = 0
        self.references_expanded = False

        self.entity = Entity(claim['mainsnak'])
        self.entity.connect("entity-editing", self.entity_editing_cb)
        self.entity.connect("entity-leaving", self.entity_leaving_cb)
        self.entity.connect("object-selected", self.object_selected_cb, claim)
        self.entity.connect('new-window-clicked', self.new_window_clicked_cb)
        self.mainsnak.add(self.entity)

        self.qualifier_new.connect("focus-in-event",
                                   self.qualifier_new_focus_in_event_cb)
        self.qualifier_new.connect("focus-out-event",
                                   self.qualifier_new_focus_out_event_cb)
        self.hide_actions = True

        #qualifier_new_property = QualifierNewProperty()#{"URI":"P0",
                                     #"Label":"Example property",
                                     #"Description":"This is an example property"})
        #qualifier_new_value = QualifierNewValue()
        #self.qualifier_new.attach(qualifier_new_property, 0, 0, 1, 1)
        #self.qualifier_new.attach(qualifier_new_value, 1, 0, 2, 1)

        if 'qualifiers' in claim:
            self.props.row_spacing = 3
            self.qualifiers.set_visible(True)
            claims = claim['qualifiers']

            for i,P in enumerate(claims):
                download_light(P, self.load_qualifier, i, claims[P])

        if 'references' in claim:
            self.references = claim['references']
            self.button_connection = self.button.connect("button-press-event", self.references_expand_clicked_cb)
        else:
            self.actions_hide = False
            self.icon.set_from_icon_name('list-add-symbolic', IconSize.BUTTON)
            #self.button_connection = self.button.connect("button-press-event", self.reference_new_clicked_cb)

        self.button_press_connection = self.connect("button-press-event", self.clicked_cb)

        del claim

    @Template.Callback()
    def qualifier_new_focus_in_event_cb(self, qualifier, event):
        context = self.get_style_context
        resource = '/ml/prevete/Daty/gtk/entity.css'
        set_style(self.qualifier_new.get_style_context(), resource, 'search_entry', True)

    @Template.Callback()
    def qualifier_new_focus_out_event_cb(self, qualifier, event):
        context = self.get_style_context()
        resource = '/ml/prevete/Daty/gtk/entity.css'
        set_style(self.qualifier_new.get_style_context(), resource, 'search_entry', False)

    def entity_leaving_cb(self, entity, popover):
        print("Value: entity leaving")
        self.emit("entity-leaving", entity)
        return True

    def new_window_clicked_cb(self, entity, payload):
        print("Value: new window clicked")
        self.emit("new-window-clicked", payload)

    def clicked_cb(self, widget, event):
        if hasattr(self, 'references'):
            if event.type == EventType(5): #double click
                self.references_expand_clicked_cb(widget, event)
        else:
            if event.type == EventType(4): #single click
                self.reference_new_clicked_cb(widget, event)

    def reference_new_clicked_cb(self, widget, event):
        if not self.actions_hide:
            print("Value: 'reference-new' emitted")
            #self.actions.set_visible(True)
            #self.actions_hide = not self.actions_hide
            if self.icon.get_icon_name()[0] == "list-add-symbolic":
                self.button.set_visible(False)
                self.emit("reference-new-clicked", self.entity)
            #self.icon.set_from_icon_name('pan-down-symbolic', IconSize.BUTTON)
        else:
            #self.actions_hide = not self.actions_hide
            print("Value: hiding actions")
            self.actions.set_visible(False)
            if self.icon.get_icon_name()[0] == "list-add-symbolic":
                self.button.set_visible(True)
            #self.icon.set_from_icon_name('list-add-symbolic', IconSize.BUTTON)
        #self.actions_hide = not self.actions_hide

    def references_expand_clicked_cb(self, widget, event):
        self.references_expanded = not self.references_expanded
        state = self.references_expanded
        if state:
            icon_name = 'pan-down-symbolic'
        else:
            icon_name = 'pan-end-symbolic'
        self.icon.set_from_icon_name(icon_name, IconSize.BUTTON)
        #self.reference_new.set_visible(state)
        self.emit('references-toggled', self)

    def init_references(self):
        self.references_widgets = []
        for j,ref in enumerate(self.references):
            widget = Reference()
            self.references_widgets.append(widget)
            for i,P in enumerate(ref['snaks-order']):
                download_light(P, self.load_reference, i, widget, ref['snaks'][P])
        self.references_widgets.append(Reference(new=True))

    def load_reference(self, URI, property, error, i, widget, refs):
        try:
            print(property["Label"], i)
            property = QualifierProperty(property)
            widget.grid.attach(property, 0, i+self.reference_row, 1, 1)
            for j, ref in enumerate(refs):
                self.load_async(self.on_value_complete,
                                URI,
                                ref,
                                widget.grid,
                                i+self.reference_row+j)
            self.reference_row += len(refs) - 1
        except Exception as e:
            print(URI)
            raise e

    def load_qualifier(self, URI, qualifier, error, i, claims):
        try:
            qualifier = QualifierProperty(qualifier)
            self.qualifiers.attach(qualifier, 0, i+self.qualifier_row, 1, 1)
            for j, claim in enumerate(claims):
                self.load_async(self.on_value_complete,
                                URI,
                                claim,
                                self.qualifiers,
                                i+self.qualifier_row+j)
            self.qualifier_row += len(claims) - 1
            return None
        except Exception as e:
            print(URI)
            raise e

    def on_value_complete(self, URI, snak, grid, row):
        value = Entity(snak, qualifier=True)
        value.connect("entity-editing", self.entity_editing_cb)
        value.entry.connect("focus-out-event", self.entity_leaving_cb)
        value.connect("object-selected", self.object_selected_cb, snak)
        value.connect('new-window-clicked', self.new_window_clicked_cb)
        self.set_font_deprecated(value)
        grid.attach(value, 1, row, 2, 1)
        grid.set_size_request(-1,100)
        grid.set_size_request(-1,-1)
        return None

    def entity_editing_cb(self, entity, popover):
        print("Value: entity editing")
        #self.actions_hide = False
        #self.reference_new_clicked_cb(entity, popover)
        self.emit("entity-editing", entity, popover)

    def load_async(self, callback, *cb_args):#URI, claim, j):
        def do_call():
            error = None
            try:
                pass
            except Exception as err:
                print(URI)
                raise err
            idle_add(lambda: callback(*cb_args))#claim, j))
        thread = MyThread(target = do_call)
        thread.start()

    def object_selected_cb(self, entity, target, claim):
        print("Value: object selected")
        print("Value: entity", entity.entity['Label'])
        provider = CssProvider()
        provider.load_from_resource('/ml/prevete/Daty/gtk/value.css')
        self.context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.context.add_class('loading')
        self.emit("claim-changed", claim, target)

    def set_font_deprecated(self, editor_widget):
        pango_context = editor_widget.create_pango_context()
        font_description = pango_context.get_font_description()
        increase = 8 #pt 14
        font_size = 1024*increase
        font_description.set_size(font_size)
        editor_widget.override_font(font_description)

    def set_references(self):
        if not hasattr(self, 'references'):
            provider = CssProvider()
            provider.load_from_resource('/ml/prevete/Daty/gtk/value.css')
            self.context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION)
            self.context.add_class('unreferenced')
        else:
            self.context.remove_class('unreferenced')

    def set_expanded(self):
        if self.references_expanded:
            provider = CssProvider()
            provider.load_from_resource('/ml/prevete/Daty/gtk/value.css')
            self.context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION)
            self.context.add_class('expanded')
        else:
            self.context.remove_class('expanded')
