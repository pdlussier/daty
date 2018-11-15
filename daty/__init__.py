#!/usr/bin/env python3

#    Daty
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


from gi import require_version
require_version('Gtk', '3.0')
require_version('Gdk', '3.0')
from gi.repository.Gdk import Event
from gi.repository.Gtk import main, main_quit, Button, HBox, HPaned, IconSize, HeaderBar, Label, ListBox, Revealer, RevealerTransitionType, ScrolledWindow, SearchBar, SearchEntry, Stack, StackSwitcher, StackTransitionType, StyleContext, TextView, VBox, Window, WindowPosition, STYLE_CLASS_SUGGESTED_ACTION
from gi.repository.GLib import unix_signal_add, PRIORITY_DEFAULT
from pprint import pprint
from setproctitle import setproctitle
from signal import SIGINT
from util import gtk_style, import_translations
from widgets import BetterPopover, ButtonWithPopover, CommonEditor, EditableListBox, EditableListBoxRow, ExtendedModelButton, ItemResults, ItemSearchBox, NameDescriptionLabel, Result, ResultsBox, Sidebar, TripleBox, WelcomePage
from wikidata import Wikidata

name = "daty"
setproctitle(name)

class WelcomeWindow(Window):

    def __init__(self):

        # Window properties
        Window.__init__(self, title="Daty")
        self.set_border_width(0)
        self.set_default_size(500, 400)
        self.set_position(WindowPosition(1))
        self.set_title ("Daty")
        #self.set_icon_from_file('icon.png')
        self.connect('destroy', main_quit)
        unix_signal_add(PRIORITY_DEFAULT, SIGINT, main_quit)

        # Title
        label = Label(label="<b>" + lang['name'] + "</b>")
        label.set_use_markup(True)

        # Title revealer 
        title_revealer = Revealer()
        title_revealer.set_transition_type (RevealerTransitionType.CROSSFADE)
        title_revealer.set_transition_duration(500)
        title_revealer.add(label)
        title_revealer.set_reveal_child(True)

        # Headerbar        
        hb = HeaderBar()
        hb.set_show_close_button(True)
        hb.set_custom_title(title_revealer)
        self.set_titlebar(hb)

        # Headerbar: New items
        open_session = Button.new()
        open_session.set_label (lang['open session'])
        open_session.connect ("clicked", self.on_constraint_search)
        hb.pack_start(open_session)

        # On demand stack
        stack = Stack()
        stack.set_transition_type (StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration (500)

        # Stack revealer 
        stack_revealer = Revealer()
        stack_revealer.set_transition_type (RevealerTransitionType.CROSSFADE)
        stack_revealer.set_transition_duration(500)
        stack_revealer.set_reveal_child(False)
        stack_revealer.add(stack)

        # Label search
        label_search_page = LabelSearchPage(set_visible_search_entry=True)
        stack.add_titled(label_search_page, lang['select by label'], lang['select by label'])

        # Back button
        back = Button.new_from_icon_name("go-previous-symbolic", size=IconSize.BUTTON)

        # Add Button
        add = Button.new_with_label (lang['open'])
        add.get_style_context().add_class(STYLE_CLASS_SUGGESTED_ACTION)
        add.set_sensitive(False)

        # Sparql Page
        sparql_page = SparqlPage(add_button=add, parent=self)
        stack.add_titled(sparql_page, lang['select by constraint'], lang['select by constraint'])

        # Switcher
        switcher = StackSwitcher()
        switcher.set_stack(stack)

        # Switcher revealer 
        switcher_revealer = Revealer()
        switcher_revealer.set_transition_type (RevealerTransitionType.CROSSFADE)
        switcher_revealer.set_transition_duration(500)
        switcher_revealer.set_reveal_child(False)
        switcher_revealer.add(switcher)

        # Welcome revealer 
        welcome_revealer = Revealer()
        welcome_revealer.set_transition_type (RevealerTransitionType.CROSSFADE)
        welcome_revealer.set_transition_duration(500)
        welcome_revealer.set_reveal_child(True)
        self.add(welcome_revealer)

        # Things that will have to hide/be revealed
        hide_and_seek = {"hb":                  hb,
                         "open session":        open_session,
                         "back":                back,
                         "add":                 add,
                         "title revealer":      title_revealer,
                         "switcher revealer":   switcher_revealer,
                         "stack revealer":      stack_revealer,
                         "stack":               stack,
                         "welcome revealer":    welcome_revealer}

        # Welcome page
        self.search_visible = False
        wp_args = {'icon_name':                 "system-search-symbolic",
                   'description':               lang['welcome description'],
                   'button_text':               lang['add constraint'],
                   'button_callback':           self.on_constraint_search,
                   'button_callback_arguments': [hide_and_seek],
                   'parent':                    self}
        welcome_page = WelcomePage(**wp_args)
        welcome_revealer.add(welcome_page)

        # Write to search
        self.connect("key_press_event", self.on_key_press, hide_and_seek)
        back.connect("clicked", self.on_back_button, hide_and_seek)

    def on_key_press(self, widget, event, k):
        if self.search_visible:
            if event.keyval == 65307:
                self.deactivate_search(k)
        if not self.search_visible:
            if not event.keyval == 65307:
                self.activate_search(k)

    def on_back_button(self, button, k):
        self.deactivate_search(k)

    def activate_search(self, k):

        # Hide welcome and title
        k['welcome revealer'].set_reveal_child(False)
        self.remove(k['welcome revealer'])
        k['title revealer'].set_reveal_child(False)
        k['hb'].remove(k['open session'])
        k['hb'].set_show_close_button(False)

        # Show switcher, stack and back
        k['hb'].pack_start(k['back'])
        k['hb'].pack_end(k['add'])
        k['hb'].set_custom_title(k['switcher revealer'])
        k['switcher revealer'].set_reveal_child(True)
        k['hb'].show_all()
        self.add(k['stack revealer'])
        k['stack revealer'].set_reveal_child(True)

        # Set search visible
        k['stack'].set_visible_child_full(lang['select by label'], StackTransitionType.NONE)
        self.search_visible = True 
        self.show_all()
        search_entry = k['stack'].get_child_by_name(lang['select by label']).search_entry
        search_entry.grab_focus_without_selecting()

    def deactivate_search(self, k): 
        # Hide stack, switcher and back
        k['stack revealer'].set_reveal_child(False)
        self.remove(k['stack revealer'])
        k['switcher revealer'].set_reveal_child(False)
        k['hb'].remove(k['back'])
        k['hb'].remove(k['add'])
        k['hb'].set_show_close_button(True)

        # Show title and welcome
        k['hb'].set_custom_title(k['title revealer'])
        k['hb'].pack_start(k['open session'])
        k['title revealer'].set_reveal_child(True)
        k['hb'].show_all()
        self.add(k['welcome revealer'])
        k['welcome revealer'].set_reveal_child(True)

        # Set search not visible
        self.search_visible = False
        search_entry = k['stack'].get_child_by_name(lang['select by label']).search_entry
        search_entry.set_text("")
        self.show_all()

    def on_constraint_search(self, button, k):
        self.activate_search(k)
        k['stack'].set_visible_child_full(lang['select by constraint'], StackTransitionType.NONE)

class LabelSearchPage(VBox):

    def __init__(self, set_visible_search_entry=True, results_border=0):
        VBox.__init__(self)

        # Search Box
        search_box = HBox()
        self.pack_start(search_box, False, False, 0)

        # Results Box
        results = ResultsBox()
        self.pack_start(results, True, True, results_border)

        # Search Entry
        self.search_entry = SearchEntry()
        self.search_entry.connect("search_changed", self.on_search_changed, results)
        self.search_entry.show()

        # Search bar
        self.search_bar = SearchBar()
        self.search_bar.set_search_mode(True)
        self.search_bar.connect_entry(self.search_entry)
        self.search_bar.add(self.search_entry)
        search_box.pack_start(self.search_bar, expand=True, fill=True, padding=0)

    def on_search_changed(self, search_entry, results):
        # Get query
        query = search_entry.get_text()

        # Clean results
        results.scrolled.remove(results.listbox)
        results.listbox = ListBox()

        # Obtain data
        if query != "":
            new_item = {"Label":query,
                        "Description":lang['create new item']}
            data = [new_item] + wikidata.search(query)
        else:
            data = []

        # Populate results
        for d in data:
            row = Result(results.listbox, d)
            results.listbox.add(row)
        results.scrolled.add(results.listbox)
        results.listbox.show_all()

class SparqlPage(VBox):
    def __init__(self, add_button=None, parent=None, selection_vpadding=3):
        VBox.__init__(self)
        self.parent = parent
        self.add_button = add_button
        self.query = {'vars':[], 'what':{}, 'triples':[]}
        self.what = {}
        self.triples = []

        # Selection Box
        selection_box = VBox()
        self.pack_start(selection_box, False, False, 0)

        # label + Button vertical Box
        selection_vbox = VBox()

        # Label + Button horizontal Box
        selection_hbox = HBox()
        selection_vbox.pack_start(selection_hbox, True, True, selection_vpadding)

        # Select label
        label = Label()
        label.set_label(lang['select'])
        selection_hbox.pack_start(label, True, True, 2)

        # Selected variable
        bwp_args = {"text":     lang['variable'],
                    "tooltip":  lang['variable tooltip'],
                    "css":      "target",
                    "vpadding": 2,
                    "data":     self.query['what']}
        self.variable = ButtonWithPopover(**bwp_args)
        isb_args = {"type":                  "var",
                    "item_changed_callback": self.check_query} 
        self.variable.set_popover_box(ItemSearchBox(self.variable, **isb_args))
        selection_hbox.pack_start(self.variable, True, True, 2)

        # Search bar
        self.selection_bar = SearchBar()
        self.selection_bar.set_search_mode(True)
        self.selection_bar.add(selection_vbox)
        selection_box.pack_start(self.selection_bar, expand=True, fill=True, padding=0)

        # Constraints
        constraints_args = {"new_row_callback": self.new_constraint,
                            "new_row_callback_arguments":[],
                            "delete_row_callback": self.delete_constraint,
                            "delete_row_callback_arguments": [],
                            "horizontal_padding": 0}
        self.constraints = EditableListBox(**constraints_args)
        self.pack_start(self.constraints, True, True, 0)
        self.constraints.eventbox.emit("button_press_event", Event())

    def new_constraint(self, row):
        # Add a triple box
        triple_box = TripleBox(self.check_query)
        self.query['triples'].append(triple_box)
        row.add_widget(triple_box)
        self.check_query()

    def delete_constraint(self, row, widget, event):
        self.query['triples'].remove(row.child) 
        self.check_query()

    def check_query(self):
        update = [t.get_data() for t in self.query["triples"]]
        self.triples = [t.triple for t in self.query["triples"]]
        self.what = self.variable.data
        ready = all(not any(t[k] == {} for k in t.keys()) for t in self.triples) and self.what != {}
        if ready:
            self.add_button.set_sensitive(True)
            self.add_button.connect("clicked", self.on_add)
        else:
            self.add_button.set_sensitive(False)

    def on_add(self, button):
        results = wikidata.select(self.what, self.triples)
        self.parent.hide()
        editor = Editor(items=results) 
        editor.show_all() 
        del self.parent

class Editor(Window):

    def __init__(self, items=['Q156282']):#, 'Q167983', 'Q24']):

        self.items = [{"URI":item,"Content":wikidata.fetch(item)} for item in items]
        self.properties = {P:wikidata.fetch(P) for P in set.union(*[set(item["Content"]['claims'].keys()) for item in self.items])}
        self.common_properties = set.intersection(*[set(item["Content"]['claims'].keys()) for item in self.items])

        pprint(self.properties['P373'])

        # Window properties
        Window.__init__(self, title="Daty")
        self.set_border_width(0)
        self.set_default_size(1000, 600)
        self.set_position(WindowPosition(1))
        self.set_title ("Daty")
        #self.set_icon_from_file('icon.png')
        self.connect('destroy', main_quit)
        unix_signal_add(PRIORITY_DEFAULT, SIGINT, main_quit)

        # Title
        label = Label(label="<b>Daty</b>")
        label.set_use_markup(True)

        # Headerbar        
        hb = HeaderBar()
        hb.set_show_close_button(True)
        hb.set_custom_title(label)
        self.set_titlebar(hb)

        # Headerbar: New items
        open = Button.new()
        open.set_label ("Apri")
        hb.pack_start(open)

        # Page
        single_editor = Stack()
        sidebar = Sidebar(self.items, self.properties, single_editor)
        common_editor = CommonEditor(self.items)

        # Sidepaned
        paned = HPaned()
        paned.set_position(100)
        paned.add1(sidebar)
        self.add(paned)

        # Editor paned
        editor_paned = HPaned()
        editor_paned.set_position(450)
        editor_paned.add1(single_editor)
        editor_paned.add2(common_editor)
        paned.add2(editor_paned)


class WikidataEditor():
    def __init__(self):
        gtk_style()
        win = WelcomeWindow()
        #win = Editor()
        win.show_all()
        main()

if __name__ == "__main__":
    code = 'it'
    lang = import_translations(code)
    wikidata = Wikidata(verbose=False)
    editor = WikidataEditor()