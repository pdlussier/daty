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
from gi.repository.GLib import idle_add #, PRIORITY_LOW
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, CssProvider, IconSize, StyleContext, Grid, Template

from .entity import Entity
from .qualifierproperty import QualifierProperty
from .util import MyThread, download_light

@Template.from_resource("/ml/prevete/Daty/gtk/value.ui")
class Value(Grid):
    
    __gtype_name__ = "Value"

    button = Template.Child("button")
    icon = Template.Child("icon")
    qualifiers = Template.Child("qualifiers")
    mainsnak = Template.Child("mainsnak")

    def __init__(self, claim, *args, load=None, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        self.load = load
        self.extra = 0

        context = self.get_style_context()

        entity = Entity(claim['mainsnak'], load=self.load)
        self.mainsnak.add(entity)

        if 'qualifiers' in claim:
            self.qualifiers.props.margin_bottom = 6
            claims = claim['qualifiers']
            for i,P in enumerate(claims):
                download_light(P, self.load_qualifiers, i, claims[P])

        if 'references' in claim:
            self.references = claim['references']
            self.icon.set_from_icon_name("pan-end-symbolic", IconSize.BUTTON)
            self.button.connect("clicked", self.references_expand_clicked_cb)
        else:
            self.icon.set_from_icon_name('list-add-symbolic', IconSize.BUTTON)
            #self.button.connect("clicked", self.reference_new_clicked_cb)

        del claim

    def references_expand_clicked_cb(self, widget):
        for i,P in enumerate(self.references):
            print(P.keys())

    def load_qualifiers(self, URI, qualifier, error, i, claims):
        try:
            qualifier = QualifierProperty(qualifier)
            self.qualifiers.attach(qualifier, 0, i+self.extra, 1, 1)
            for j, claim in enumerate(claims):
                self.load_value_async(URI, claim, i+self.extra+j)
            self.extra += len(claims) - 1
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
        value = Entity(claim, qualifier=True, load=self.load)
        self.set_font_deprecated(value)
        self.qualifiers.attach(value, 1, j, 3, 1)
        return None

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
