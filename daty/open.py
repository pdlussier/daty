# -*- coding: utf-8 -*-

#import asyncio
from copy import deepcopy as cp
from gi import require_version
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import ListBox, ListBoxRow, Template, Window
from threading import Thread

from .entityselectable import EntitySelectable
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

    def __init__(self, load, *args, new_session=True, verbose=False):
        Window.__init__(self, *args)

        self.verbose = verbose

        self.show_all()

        constraint = ListBoxRow()
        constraint.add(Triplet())
        self.constraint_listbox.add(constraint)
        self.constraint_listbox.show_all()

        self.label_listbox.selected = []

        if new_session:
            self.set_search_placeholder(True)
              
        else:
            self.set_search_placeholder(False, search_stack="label_search")

        self.entities = self.label_listbox.selected

        self.open_button.connect('clicked', self.open_button_clicked_cb, load)

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

    def open_button_clicked_cb(self, widget, load):
        if self.entities != []:
            load(self.entities)
        self.destroy()

    @Template.Callback()
    def placeholder_back_clicked_cb(self, widget):
        self.set_search_placeholder(True)

    @Template.Callback()
    def placeholder_add_constraint_clicked_cb(self, widget):
        self.set_search_placeholder(False, search_stack="constraints")

    @Template.Callback()
    def key_press_event_cb(self, widget, event):
        if self.verbose:
            print("Keyval of key pressed:", event.keyval)
        #if Esc, set placeholder ot [Right Alt, Tab, Esc, Maiusc, Control, Bloc Maiusc, Left Alt]
        if event.keyval == 65307:
            self.set_search_placeholder(True)
        # else if key is [Right Alt, Tab, Maiusc, Control, Bloc Maiusc, Left Alt]
        elif event.keyval in [65027, 65289, 65505, 65509, 65513]:
            pass
        else:
            self.set_search_placeholder(False)

    def on_search_done(self, results, error):
        self.label_listbox.foreach(self.label_listbox.remove)
        for r in results:
            entity = EntitySelectable(r, selected=self.label_listbox.selected)
            row = ListBoxRow()
            row.add(entity)
            self.label_listbox.add(row)
            self.label_listbox.show_all()

    def search(self, query):
        query = cp(query)
        wikidata = cp(self.wikidata)
        f = lambda : wikidata.search(query)
        def do_call():
            results, error = None, None
            try:
                results = f()
            except Exception as err:
                error = err

            idle_add(lambda: self.on_search_done(results, error))
        thread = Thread(target = do_call)
        thread.start()

    @Template.Callback()
    def search_entry_search_changed_cb(self, entry):
        self.search(entry.get_text())

    @Template.Callback()
    def label_listbox_row_activated_cb(self, widget, row):
        toggle = row.get_children()[0]
        toggle.set_active(False) if toggle.get_active() else toggle.set_active(True)
