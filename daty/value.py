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
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gi.repository.GLib import idle_add #, PRIORITY_LOW
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, CssProvider, IconSize, Separator, StyleContext, Grid, Template

from .entity import Entity
from .qualifierproperty import QualifierProperty
from .util import MyThread, download_light

@Template.from_resource("/ml/prevete/Daty/gtk/value.ui")
class Value(Grid):

    __gtype_name__ = "Value"

    __gsignals__ = {'claim-changed':(sf.RUN_LAST,
                                     TYPE_NONE,
                                     (TYPE_PYOBJECT,
                                      TYPE_PYOBJECT)),
                    'new-window-clicked':(sf.RUN_LAST,
                                          TYPE_NONE,
                                          (TYPE_PYOBJECT,)),
                    'references-toggled':(sf.RUN_LAST,
                                         TYPE_NONE,
                                         (TYPE_PYOBJECT,))}

    button = Template.Child("button")
    icon = Template.Child("icon")
    qualifiers = Template.Child("qualifiers")
    mainsnak = Template.Child("mainsnak")
    references_grid = Template.Child("references_grid")

    def __init__(self, claim, *args, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        self.qualifier_row = 0
        self.reference_row = 0
        self.references_expanded = False

        context = self.get_style_context()

        entity = Entity(claim['mainsnak'])
        entity.connect("object-selected", self.object_selected_cb, claim)
        entity.connect('new-window-clicked', self.new_window_clicked_cb)
        self.mainsnak.add(entity)

        if 'qualifiers' in claim:
            self.qualifiers.props.margin_bottom = 6
            claims = claim['qualifiers']
            for i,P in enumerate(claims):
                download_light(P, self.load_qualifiers, i, claims[P])

        if 'references' in claim:
            self.references = claim['references']
            self.button.connect("toggled", self.references_expand_clicked_cb)#,
                                #claim['references'])
        else:
            self.icon.set_from_icon_name('list-add-symbolic', IconSize.BUTTON)
            #self.button.connect("clicked", self.reference_new_clicked_cb)

        del claim

    def new_window_clicked_cb(self, entity, payload):
        print("Value: new window clicked")
        self.emit("new-window-clicked", payload)

    def references_expand_clicked_cb(self, widget):
        state = widget.get_active()
        if state:
            icon_name = 'pan-down-symbolic'
        else:
            icon_name = 'pan-end-symbolic'
        self.icon.set_from_icon_name(icon_name, IconSize.BUTTON)
        self.emit('references-toggled', self)

    def load_reference(self, URI, property, error, i, values):
        try:
            print(property["Label"], i)
            #i = 2*i
            property = QualifierProperty(property)
            separator = Separator()
            self.references_grid.attach(separator, 0, i, 5, 1)
            self.references_grid.attach(property, 0, i+1, 1, 1)
            #self.references_grid.show_all()
            #self.qualifiers.attach(qualifier, 0, i+self.extra, 1, 1)
            #for j, value in enumerate(claims):
            #    self.load_value_async(URI, claim, i+self.extra+j)
            #self.extra += len(claims) - 1
            #return None
        except Exception as e:
            print(URI)
            raise e

    def load_qualifiers(self, URI, qualifier, error, i, claims):
        try:
            qualifier = QualifierProperty(qualifier)
            self.qualifiers.attach(qualifier, 0, i+self.qualifier_row, 1, 1)
            for j, claim in enumerate(claims):
                self.load_value_async(URI, claim, i+self.qualifier_row+j)
            self.qualifier_row += len(claims) - 1
            return None
        except Exception as e:
            print(URI)
            raise e

    def load_value_async(self, URI, claim, j):
        def do_call():
            error = None
            try:
                pass
            except Exception as err:
                print(URI)
                raise err
            idle_add(lambda: self.on_value_complete(claim, j))
        thread = MyThread(target = do_call)
        thread.start()

    def on_value_complete(self, claim, j):
        value = Entity(claim, qualifier=True)
        value.connect("object-selected", self.object_selected_cb, claim)
        self.set_font_deprecated(value)
        self.qualifiers.attach(value, 1, j, 3, 1)
        return None

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
