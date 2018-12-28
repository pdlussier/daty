# -*- coding: utf-8 -*-

#import asyncio
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import ListBox, ListBoxRow, Template, Window
from gi.repository.Gdk import unicode_to_keyval
require_version('Handy', '0.0')
from gi.repository.Handy import Column
from threading import Thread

from .entity import Entity
from .triplet import Triplet
from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/open.ui")
class Open(Window):
    __gtype_name__ = "Open"

    wikidata = Wikidata()

    #properties = Template.Child("properties")
    content_stack = Template.Child("content_stack")
    header_bar = Template.Child("header_bar")
    header_bar_stack = Template.Child("header_bar_stack")
    search_stack = Template.Child("search_stack")
    constraint_listbox = Template.Child("constraint_listbox")
    constraint_search = Template.Child("constraint_search")
    open_session = Template.Child("open_session")
    placeholder_back = Template.Child("placeholder_back")
    label_listbox = Template.Child("label_listbox")
    open_button = Template.Child("open_button")

    def __init__(self, *args, new_session=True):
        Window.__init__(self, *args)

        self.new_session = new_session

        self.show_all()

        constraint = ListBoxRow()
        constraint.add(Triplet())
        self.constraint_listbox.add(constraint)
        self.constraint_listbox.show_all()

        self.label_listbox.objects = []
        self.objects = self.label_listbox.objects

        if new_session:
            self.set_search_placeholder(True)

        else:
            self.set_search_placeholder(False, search_stack="label_search")

    def set_search_placeholder(self, value, search_stack="label_search"):
       if value:
           self.header_bar_stack.set_visible_child_name("open_entities")
           self.content_stack.set_visible_child_name("placeholder")
           self.open_session.set_visible(True)
           self.placeholder_back.set_visible(False)
           self.open_button.set_visible(False)
           self.header_bar.set_show_close_button(True)
       else:
           if self.content_stack.get_visible_child_name() == "placeholder":
                self.header_bar_stack.set_visible_child_name("header_search_type")
                self.content_stack.set_visible_child_name("search")
                self.search_stack.set_visible_child_name(search_stack)
                self.open_session.set_visible(False)
                self.placeholder_back.set_visible(True)
                self.open_button.set_visible(True)
                self.header_bar.set_show_close_button(False)

    @Template.Callback()
    def open_button_clicked_cb(self, widget):
        if self.new_session:
            from .editor import Editor
            editor = Editor(entities=self.objects)
            editor.present()
        self.destroy()

    @Template.Callback()
    def placeholder_back_clicked_cb(self, widget):
        self.set_search_placeholder(True)

    @Template.Callback()
    def placeholder_add_constraint_clicked_cb(self, widget):
        self.set_search_placeholder(False, search_stack="constraints")

    @Template.Callback()
    def key_press_event_cb(self, widget, event):
        if not event.keyval == 65307:
            self.set_search_placeholder(False)
        else:
            self.set_search_placeholder(True)

    def on_search_done(self, results, error):
        self.label_listbox.foreach(self.label_listbox.remove)
        for r in results:
            entity = Entity(r, parent=self.label_listbox)
            row = ListBoxRow()
            row.add(entity)
            self.label_listbox.add(row)
        self.label_listbox.show_all()

    def search(self):
        f = lambda : self.wikidata.search(self.query)
        
        def do_call():
            results = None
            error = None

            try:
                results = f()
            except Exception as err:
                error = err

            idle_add(lambda: self.on_search_done(results, error))

        thread = Thread(target = do_call)
        thread.start()

    @Template.Callback()
    def search_entry_search_changed_cb(self, entry):
        self.query = entry.get_text()
        self.search()
        #thread = Thread(target=self.search)
        #thread.daemon = True
        #thread.start() 
        #results = self.wikidata.search(entry.get_text())
        #print(results)
