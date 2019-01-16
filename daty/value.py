# -*- coding: utf-8 -*-

from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
require_version('Gdk', '3.0')
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gdk import EventType
from gi.repository.Gtk import Grid, Template
from pprint import pprint
from threading import Thread

from .entity import Entity
from .qualifierproperty import QualifierProperty
from .util import MyThread
from .values import Values
from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/value.ui")
class Value(Grid):
    
    __gtype_name__ = "Value"

    qualifiers = Template.Child("qualifiers")
    mainsnak = Template.Child("mainsnak")
    wikidata = Wikidata()

    def __init__(self, claim, *args, load=None, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        self.load = load
        self.extra = 0

        try:
            entity = Entity(claim['mainsnak'], load=self.load)
            self.mainsnak.add(entity)
            #self.attach(entity, 0, 0, 1, 1)

            if 'qualifiers' in claim.keys():
                self.claims = claim['qualifiers']
                for i,P in enumerate(self.claims.keys()):
                    self.download(P, self.load_qualifiers, i)

        except Exception as err:
            print(err)

    def download(self, URI, callback, *cb_args):
        f = lambda : (cp(arg) for arg in cb_args)
        URI, wikidata = cp(URI), cp(self.wikidata)
        def do_call():
            cb_args = list(f())
            entity, error = None, None
            try:
                entity = wikidata.download(URI)
            except Exception as err:
                error = err
            idle_add(lambda: callback(URI, entity, error, *cb_args),
                     priority=PRIORITY_LOW)
        thread = Thread(target = do_call)
        thread.start()

    def load_qualifiers(self, URI, qualifier, error, i):
        try:
            if error:
                print(error)
            #pprint(qualifier)
            qualifier = QualifierProperty(qualifier)
            values = Values(frame=False)
            values.props.expand = True
            values.props.hexpand = True
            values.props.vexpand = True
            self.qualifiers.attach(qualifier, 0, i+self.extra, 1, 1)
            for j, claim in enumerate(self.claims[URI]):
                self.load_value_async(URI, claim, values, i+self.extra+j)
            self.extra += len(self.claims[URI]) - 1
            pprint(j)
        except Exception as e:
            print(URI)
            print(type(e))
            print(e.args)
            pprint(e.__traceback__)

    def load_value_async(self, URI, claim, values, j):
        f = cp(URI), cp(claim)
        def do_call():
            URI, claim = f
            error = None
            try:
                pass
            except Exception as err:
                error = err
            idle_add(lambda: self.on_value_complete(claim, values, error, j))
        thread = MyThread(target = do_call)
        thread.start()

    def on_value_complete(self, claim, values, error, j):
        if error:
            print(error)
        value = Entity(claim, load=self.load)
        self.set_font_deprecated(value)
        self.qualifiers.attach(value, 1, j, 2, 1)

    def set_font_deprecated(self, editor_widget):
        pango_context = editor_widget.create_pango_context()
        font_description = pango_context.get_font_description()
        increase = 8 #pt 14
        font_size = 1024*increase
        font_description.set_size(font_size)
        editor_widget.override_font(font_description)

    def load_entity(self, URI, entity, error):
        if error:
            print(error)
        label = self.wikidata.get_label(entity)
        description = self.wikidata.get_description(entity)
        self.label.set_text(label)
        self.label.set_tooltip_text(description)

#    @Template.Callback()
#    def label_button_press_event_cb(self, widget, event):
#        print(event.type)
#        print(event.button)
#        if event.type == EventType._2BUTTON_PRESS:
#            print(" double click ")
#        elif event.type == EventType.BUTTON_PRESS:
#            print("single click ")

        #if event.button == 1 :
        #    data = widget.get_path_at_pos(int(event.x), int(event.y))
        #    if data :
        #        if event.type == gtk.gdk._2BUTTON_PRESS :
        #            print(" double click ")

        #        elif event.type == gtk.gdk.BUTTON_PRESS :
        #            print("single click ")

    #def 
