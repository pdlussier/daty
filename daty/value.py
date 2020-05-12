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
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, CssProvider, Grid, IconSize, PositionType, SearchEntry, Separator, StyleContext, Grid, Template
from gi.repository.Pango import FontDescription
from pprint import pprint

from .entity import Entity
from .entitypopover import EntityPopover
#from .qualifier_new_property import QualifierNewProperty
#from .qualifier_new_value import QualifierNewValue
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

    def __init__(self, claim, *args, new=False, **kwargs):
        Grid.__init__(self, *args, **kwargs)


        self.qualifier_new.modify_font(FontDescription('Cantarell 8'))
        self.reference_new.modify_font(FontDescription('Cantarell 8'))
        self.qualifier_pos = {}

        self.qualifier_row = 0
        self.reference_row = 0
        self.references_expanded = False

        if new:
            snak = None
        else:
            snak = claim['mainsnak']

        self.entity = Entity(snak=snak, new=new)
        self.entity.connect("entity-editing", self.entity_editing_cb)
        self.entity.connect("entity-leaving", self.entity_leaving_cb)
        self.entity.connect("object-selected", self.object_selected_cb, claim)
        self.entity.connect('new-window-clicked', self.new_window_clicked_cb)
        self.mainsnak.add(self.entity)


        self.hide_actions = True

        if 'qualifiers' in claim:
            self.props.row_spacing = 3
            self.qualifiers.set_visible(True)
            claims = claim['qualifiers']

            for i,P in enumerate(claims):
                download_light(P, self.load_qualifier, i, claims[P])

        self.actions_hide = False

        if 'references' in claim:
            self.references = claim['references']
            self.button_connection = self.button.connect("button-press-event", self.references_expand_clicked_cb)
        else:
            self.icon.set_from_icon_name('list-add-symbolic', IconSize.BUTTON)
            #self.button_connection = self.button.connect("button-press-event", self.reference_new_clicked_cb)

        self.button_press_connection = self.connect("button-press-event", self.clicked_cb)

        del claim

    @Template.Callback()
    def object_new_focus_in_event_cb(self, object, event):
        if not object.get_name() == 'qualifier_new':
            object.props.secondary_icon_name = "user-trash-symbolic"
            object.props.secondary_icon_activatable = True
            N = self.get_grid_rows(self.qualifiers)
            #object.connect("icon-press", self.object_new_icon_press_cb, position)
        context = object.get_style_context()
        resource = '/ml/prevete/Daty/gtk/entity.css'
        set_style(context, resource, 'search_entry', True)
        object.popover = EntityPopover(filters=['property'])
        object.popover.set_relative_to(object)
        object.popover.set_position(PositionType(3))
        object.connect("search-changed",
                       object.popover.search_entry_search_changed_cb)
        object.popover.connect("new-window-clicked", self.new_window_clicked_cb)
        object.popover.connect("object-selected", self.object_new_selected_cb)
        object.popover.popup()
        #self.emit("entity-editing", self.entity, object.popover)

    def get_grid_rows(self, grid):
        rows = 0
        for child in grid.get_children():
            y = grid.child_get_property(child, 'top-attach')
            height = grid.child_get_property(child, 'height')
            rows = max(rows, y+height)
        return rows

    def object_new_icon_press_cb(self, entry, icon_pos, event, position):
        if entry.props.secondary_icon_name == "user-trash-symbolic":
            if position == PositionType(1):
                prop = self.qualifiers.get_child_at(0,row)
                prop.destroy()
            entry.destroy()
            get

    def qualifier_new_check(self, property):
        for child in self.qualifiers.get_children():
            if type(child) == QualifierProperty:
                if child.URI == property['URI']:
                    N = self.qualifiers.child_get_property(child, 'height')
                    child = self.qualifiers.get_child_at(1,N)
                    prop = self.qualifiers.get_child_at(0,N)
                    self.qualifiers.insert_next_to(child, PositionType(2))
                    self.qualifiers.remove(prop)
                    self.qualifiers.attach(prop, 0, N, 1, 1)
                    return N, child, PositionType(2)
        return None, None, None

    def object_new_selected_cb(self, popover, property):
        parent = popover.get_relative_to()
        parent.set_text("")
        self.actions.set_visible(False)
        self.button.set_visible(True)
        if parent.get_name() == "qualifier_new":
            if property['URI'] in self.qualifier_pos:
                pos = self.qualifier_pos[property['URI']]
                N = pos['start'] + pos['end']
                child = self.qualifiers.get_child_at(1,N)
                position = PositionType(3)
                self.qualifiers.insert_next_to(child, PositionType(3))
                pos['end'] += 1
                for uri in self.qualifier_pos:
                    q_pos = self.qualifier_pos[uri]
                    if q_pos['start'] > pos['start']:
                        q_pos['start'] += 1
            else:
                qualifier = QualifierProperty(property)
                N = self.get_grid_rows(self.qualifiers)
                self.qualifiers.attach(qualifier, 0, N, 1, 1)
                child = qualifier
                position = PositionType(1)

            qualifier_value = SearchEntry()
            context = qualifier_value.get_style_context()
            resource = '/ml/prevete/Daty/gtk/entity.css'
            set_style(context, resource, 'flat', True)
            qualifier_value.props.secondary_icon_activatable = True
            qualifier_value.set_visible(True)
            qualifier_value.set_name("qualifier_new_value")
            qualifier_value.set_placeholder_text("Search to add the value")
            qualifier_value.connect("icon-press", self.object_new_icon_press_cb, position)
            qualifier_value.connect("focus-in-event", self.object_new_focus_in_event_cb)
            qualifier_value.connect("focus-out-event", self.object_new_focus_out_event_cb)
            self.qualifiers.attach_next_to(qualifier_value, child, position, 2, 1)

            qualifier_value.grab_focus()
        if parent.get_name() == "qualifier_new_value":
            print("hi, I am a new qualifier value")


    @Template.Callback()
    def object_new_focus_out_event_cb(self, object, event):
        context = object.get_style_context()
        resource = '/ml/prevete/Daty/gtk/entity.css'
        set_style(context, resource, 'search_entry', False)
        #object.set_text("")
        if not object.get_name() == 'qualifier_new':
            object.props.secondary_icon_name = "user-trash-symbolic"
            object.props.secondary_icon_activatable = True
            N = self.get_grid_rows(self.qualifiers)
            #object.connect("icon-press", self.object_new_icon_press_cb)
        object.popover.popdown()

    def entity_leaving_cb(self, entity, popover):
        print("Value: entity leaving")
        self.emit("entity-leaving", entity)
        return True

    def new_window_clicked_cb(self, entity, payload):
        print("Value: new window clicked")
        self.emit("new-window-clicked", payload)

    def clicked_cb(self, widget, event):
        print(event.button)
        if hasattr(self, 'references'):
            if event.button == 1: #EventType(4) single click
                self.references_expand_clicked_cb(widget, event)
            if event.button == 3:
                self.reference_new_clicked_cb(widget, event)
        else:
            self.reference_new_clicked_cb(widget, event)

    def reference_new_clicked_cb(self, widget, event):
        if not self.actions_hide:
            self.emit("reference-new-clicked", self.entity)
            print("Value: 'reference-new' emitted")
            if self.icon.get_icon_name()[0] == "list-add-symbolic":
                self.button.set_visible(False)
        else:
            print("Value: hiding actions")
            self.actions.set_visible(False)
            if self.icon.get_icon_name()[0] == "list-add-symbolic":
                self.button.set_visible(True)

    def references_expand_clicked_cb(self, widget, event):
        self.references_expanded = not self.references_expanded
        state = self.references_expanded
        if state:
            icon_name = 'pan-down-symbolic'
        else:
            icon_name = 'pan-end-symbolic'
        self.icon.set_from_icon_name(icon_name, IconSize.BUTTON)
        self.emit('references-toggled', self)

    def init_references(self):
        self.references_widgets = []
        for j,ref in enumerate(self.references):
            widget = Reference()
            self.references_widgets.append(widget)
            for i,P in enumerate(ref['snaks-order']):
                download_light(P, self.load_reference, i, widget, ref['snaks'][P])
        #self.references_widgets.append(Reference(new=True))

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
            self.qualifier_pos[URI] = {"start":i + self.qualifier_row}
            self.qualifiers.attach(qualifier, 0, self.qualifier_pos[URI]['start'], 1, 1)

            for j, claim in enumerate(claims):
                self.load_async(self.on_value_complete,
                                URI,
                                claim,
                                self.qualifiers,
                                self.qualifier_pos[URI]['start']+j)
            self.qualifier_pos[URI]['end'] = len(claims) - 1
            self.qualifier_row += self.qualifier_pos[URI]['end']
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
        print("Value: entity", entity.data['Label'])
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
