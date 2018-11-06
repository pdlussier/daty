from gi import require_version
require_version('Gtk', '3.0')
require_version('Gdk', '3.0')
from wikidata import Wikidata
from gi.repository.Gdk import Color, Screen
from gi.repository.Gio import ThemedIcon
from gi.repository.Gtk import main, main_quit, Align, Box, Button, CheckButton, CssProvider, Entry, EventBox, HBox, IconSize, Image, HeaderBar, Label, ListBox, ListBoxRow, ModelButton, Orientation, PolicyType, PopoverMenu, Revealer, RevealerTransitionType, ScrolledWindow, SearchBar, SearchEntry, Stack, StackSwitcher, StackTransitionType, StateFlags, StyleContext, TextView, VBox, Window, WindowPosition, WrapMode, STYLE_CLASS_DESTRUCTIVE_ACTION, STYLE_CLASS_SUGGESTED_ACTION, STYLE_PROVIDER_PRIORITY_APPLICATION
from gi.repository.GLib import unix_signal_add, PRIORITY_DEFAULT
from signal import SIGINT

def gtk_style():
    css = b"""
list {
    border-style: solid;
    border-width: 1px 1px 1px 1px;
}

row {
    border-bottom-color: rgb(192,192,189);
    border-bottom-style: solid;
    border-bottom-width: 1px;
}

.subject {
    background-color: rgb(114,159,207);
    border-top-width: 5px;
    border-top-style: solid;
    border-top-color: rgb(114, 159, 207);
    border-left-width: 5px;
    border-left-style: solid;
    border-left-color: rgb(114, 159, 207);
    border-right-width: 5px;
    border-right-style: solid;
    border-right-color: rgb(114, 159, 207);
    border-bottom-width: 5px;
    border-bottom-style: solid;
    border-bottom-color: rgb(114, 159, 207);
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    border-bottom-right-radius: 5px;
    border-bottom-left-radius: 5px;
}
    """
    style_provider = CssProvider()
    style_provider.load_from_data(css)
    StyleContext.add_provider_for_screen(Screen.get_default(), style_provider, STYLE_PROVIDER_PRIORITY_APPLICATION)

class WelcomeWindow(Window):

    def __init__(self, wikidata):
        # Window properties
        Window.__init__(self, title="Daty")
        self.set_border_width(0)
        self.set_default_size(850, 450)
        self.set_position(WindowPosition(1))
        self.set_title ("Daty")
        #self.set_icon_from_file('icon.png')
        self.connect('destroy', main_quit)
        unix_signal_add(PRIORITY_DEFAULT, SIGINT, main_quit)

        # Title
        label = Label(label="<b>Daty</b>")
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
#        new_items = Button.new()
#        new_items.set_label ("Aggiungi")
#        new_items.connect ("clicked", self.on_constraint_search)
#        hb.pack_end(new_items)

        # Welcome page
        self.search_visible = False
        daty_description = """Daty ti permette di consultare e modificare Wikidata in maniera facile e intuitiva.
<b>Digita per cercare o creare nuovi item</b> oppure clicca sul pulsante in basso per utilizzare la ricerca avanzata!"""
        welcome_page = WelcomePage(icon_name="system-search-symbolic",
                                   description=daty_description,
                                   button_text="Cerca usando i vincoli",
                                   button_callback=self.on_constraint_search,
                                   callback_arguments=[wikidata],
                                   parent=self)

        # Welcome revealer 
        welcome_revealer = Revealer()
        welcome_revealer.set_transition_type (RevealerTransitionType.CROSSFADE)
        welcome_revealer.set_transition_duration(500)
        welcome_revealer.add(welcome_page)
        welcome_revealer.set_reveal_child(True)
        self.add(welcome_revealer)

        # SparqlPage
        sparql_page = SparqlPage(wikidata)

        # Label search
        #label_search = SearchByLabelPage(wikidata)

        # On demand stack
        stack = Stack()
        stack.set_transition_type (StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration (1000)
        stack.add_titled(sparql_page, "Cerca per vincolo", "Cerca per vincolo")

        # Stack revealer 
        stack_revealer = Revealer()
        stack_revealer.set_transition_type (RevealerTransitionType.CROSSFADE)
        stack_revealer.set_transition_duration(500)
        stack_revealer.set_reveal_child(False)
        stack_revealer.add(stack)

        # Switcher
        switcher = StackSwitcher()
        switcher.set_stack(stack)

        # Switcher revealer 
        switcher_revealer = Revealer()
        switcher_revealer.set_transition_type (RevealerTransitionType.CROSSFADE)
        switcher_revealer.set_transition_duration(500)
        switcher_revealer.set_reveal_child(False)
        switcher_revealer.add(switcher)


#        self.connect("key_press_event", self.on_test, label_search.search_bar)
#        stack.add_titled(label_search, "Per etichetta", "Per etichetta")

        # Write to search
        self.connect("key_press_event", self.on_key_press, hb, title_revealer, switcher_revealer, stack_revealer, welcome_revealer)


    def on_key_press(self, widget, event, hb, title_revealer, switcher_revealer, stack_revealer, welcome_revealer):
        if self.search_visible:
            if event.keyval == 65307:
                self.deactivate_search(hb, title_revealer, switcher_revealer, stack_revealer, welcome_revealer)
        if not self.search_visible:
            if not event.keyval == 65307:
                self.activate_search(hb, title_revealer, switcher_revealer, stack_revealer, welcome_revealer)

    def activate_search(self, hb, title_revealer, switcher_revealer, stack_revealer, welcome_revealer):
        # Hide welcome and title
        welcome_revealer.set_reveal_child(False)
        self.remove(welcome_revealer)
        title_revealer.set_reveal_child(False)

        # Show switcher and stack
        hb.set_custom_title(switcher_revealer)
        switcher_revealer.set_reveal_child(True)
        hb.show_all()
        self.add(stack_revealer)
        stack_revealer.set_reveal_child(True)

        # Set search visible
        self.search_visible = True 
        self.show_all()

    def deactivate_search(self, hb, title_revealer, switcher_revealer, stack_revealer, welcome_revealer):
        # Hide stack and switcher
        stack_revealer.set_reveal_child(False)
        self.remove(stack_revealer)
        switcher_revealer.set_reveal_child(False)

        # Show title and welcome
        hb.set_custom_title(title_revealer)
        title_revealer.set_reveal_child(True)
        hb.show_all()
        self.add(welcome_revealer)
        welcome_revealer.set_reveal_child(True)

        # Set search not visible
        self.search_visible = False
        self.show_all()

    def on_constraint_search(self, button, wikidata):
        add_items = AddItemsWindow(wikidata)
        add_items.show_all() 

class WelcomePage(HBox):
    def __init__(self, icon_name='system-search-symbolic', description="Sample description", button_text="Sample button", button_callback=None, callback_arguments=[], parent=None):
        HBox.__init__(self)

        #Vertical Box
        vbox = VBox()
        self.pack_start(vbox, expand=True, fill=False, padding=0)

        # Placeholder image
        icon = Image.new_from_icon_name(icon_name, size=IconSize.DIALOG)
        icon.set_pixel_size(192)
        icon.get_style_context().add_class("dim-label")
        vbox.pack_start(icon, False, True, 50)

        if description:
            # Welcome description
            label = Label(label="Daty ti permette di consultare e modificare Wikidata in maniera facile e intuitiva. <b>Digita per cercare o creare nuovi item</b> oppure clicca sul pulsante in basso per utilizzare la ricerca avanzata!", halign=Align.BASELINE)
            label.set_max_width_chars(60)
            label.set_use_markup(True)
            label.set_line_wrap(True)

        if button_text:
            # Welcome text box
            textbox = Box(orientation=Orientation(1))
            textbox.pack_start(label, True, True, 0)
            vbox.pack_start(textbox, False, True, 0)

            # Welcome button
            button = Button.new_with_label(button_text)
            button.get_style_context().add_class(STYLE_CLASS_SUGGESTED_ACTION)
            if button_callback:
                button.connect ("clicked", button_callback, *callback_arguments)

            # Welcome button box
            button_box = Box(orientation=Orientation(0))
            button_box.pack_start(button, True, False, 0)                
            vbox.pack_start(button_box, False, False, 25)

class AddItemsWindow(Window):

    def __init__(self, wikidata):

        self.wikidata = wikidata
         
        # Window properties
        Window.__init__(self, title="Add items")
        self.set_border_width(0)
        self.set_default_size(500, 400)
        self.set_position(WindowPosition(1))
        self.set_title ("Add Item")
        #self.set_icon_from_file('icon.png')
        unix_signal_add(PRIORITY_DEFAULT, SIGINT, main_quit)

        # Headerbar        
        hb = HeaderBar()
        self.set_titlebar(hb)

        # Stack
        stack = Stack()
        stack.set_transition_type (StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration (1000)
        #stack.connect("notify::visible-child", self.stack_page_changed)

        label_search = SearchByLabelPage(wikidata)
        self.connect("key_press_event", self.on_test, label_search.search_bar)
        stack.add_titled(label_search, "Per etichetta", "Per etichetta")
        stack.add_titled(SparqlPage(self.wikidata), "Per vincolo", "Per vincolo")

        # Switcher
        switcher = StackSwitcher()
        switcher.set_stack(stack) 

        # Headerbar: Cancel Button
        cancelButton = Button.new_with_label("Annulla")
        cancelButton.connect ("clicked", self.on_cancel_button_clicked, self)

        # Headerbar: Add Button
        addButton = Button.new_with_label ("Aggiungi")
        addButton.get_style_context().add_class(STYLE_CLASS_SUGGESTED_ACTION)
        #addButton.connect ("clicked", self.on_ConfirmNewChain_clicked, self, PriceEntry, RatioEntry, AmountEntry)

        hb.pack_start(cancelButton)
        hb.set_custom_title(switcher)
        hb.pack_end(addButton)

        self.add(stack)

    def on_test(self, widget, event, searchbar):
        #for arg in args:
        #    print(args)
        searchbar.handle_event(event)

    def on_cancel_button_clicked(self, button, window):
        self.destroy()
        del self

class NameDescriptionLabel(VBox):
    def __init__(self, name, description):
        # Init
        VBox.__init__(self)
        self.name = name
        self.description = description

        # Name
        name = Label(halign=Align.START)
        name.set_label(self.name)
        name.set_use_markup(True)
        name.set_line_wrap(True)
        self.pack_start(name, True, True, 0)

        # Description
        description = Label(halign=Align.START)
        description.set_label("<span font_desc=\"8.0\">" + self.description + "</span>")
        description.set_line_wrap(True)
        description.set_use_markup(True)
        self.pack_start(description, True, True, 0)

class Result(ListBoxRow):
    def __init__(self, result):
        ListBoxRow.__init__(self)
        self.content = result

        # Horizontal Box
        self.hbox = HBox()
        self.add(self.hbox)

        # Contents Box
        self.name_description = NameDescriptionLabel(text, self.content["Description"])
        self.hbox.pack_start(self.name_description, True, True, 10)

    def update(self):
        text = "<b>" + self.content["Label"] + "</b>"
        if "URI" in self.content.keys():
            text = text + " (" + result["URI"] + ")"
            checkbox = CheckButton()
            self.hbox.pack_start(checkbox, False, False, 10)
        self.name_description = NameDescriptionLabel(text, self.content["Description"])
        self.show_all() 

class LabelResultsBox(HBox):
    def __init__(self):
        HBox.__init__(self)
        self.scrolled = ScrolledWindow()
        self.scrolled.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.listbox = ListBox()
        self.scrolled.add(self.listbox)
        self.pack_start(self.scrolled, True, True, padding=10)

    def on_query_changed(self, widget, wikidata):
        query = widget.get_text()
        self.scrolled.remove(self.listbox)
        print("searching", query)
        self.listbox = ListBox()

        results = wikidata.search(query) 

        for r in results:
            row = Result(r)
            self.listbox.add(row)
        self.scrolled.add(self.listbox) 
        self.listbox.show_all()

class SearchByLabelPage(VBox):

    def __init__(self, wikidata):
        VBox.__init__(self)

        # Search Box
        search_box = HBox()
        self.pack_start(search_box, False, False, 0)

        # Results Box
        results = LabelResultsBox()
        self.pack_start(results, True, True, 10)

        # Search Entry
        search_entry = SearchEntry()
        search_entry.connect("search_changed", results.on_query_changed, wikidata)
        #search_entry.show()

        # Search bar
        self.search_bar = SearchBar()
        self.search_bar.set_search_mode(True)
        self.search_bar.connect_entry(search_entry)
        self.search_bar.add(search_entry)
        search_box.pack_start(self.search_bar, expand=True, fill=True, padding=0)

class SparqlPage(VBox):
    def __init__(self, wikidata):
        VBox.__init__(self)
        select_box = HBox()
        self.pack_start(select_box, False, False, 20)

        label = Label()
        label.set_label("Variabile selezionata: ")


        constraint_box = SparqlConstraintsBox(wikidata)

        select_box.pack_start(label, False, True, 30)
        select_box.pack_start(ItemSelectionButton(wikidata), False, True, 0)
        #select_box.pack_start(label_2, False, True, 10)
        self.pack_start(constraint_box, True, True, 30)

class ItemResultsBox(HBox):
    def __init__(self, wikidata, search_entry, button):
        HBox.__init__(self)
        self.search_entry = search_entry
        self.scrolled = ScrolledWindow()
        self.scrolled.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.listbox = ListBox()
        self.scrolled.add(self.listbox)
        self.pack_start(self.scrolled, True, True, padding=10)
        for var in wikidata.vars:
            row = Result(var)
            self.listbox.add(row)
        self.listbox.connect("row_activated", self.on_row_activated, button)
        self.listbox.show_all()


    def on_query_changed(self, widget, new_variable, button, wikidata):
        query = widget.get_text()
        self.scrolled.remove(self.listbox)
        print("searching", query)

        if query != "":
            new_variable.child = NameDescriptionLabel("<b>" + query + "</b>", "Registra come variabile")
            new_variable.set_sensitive(True)
            new_variable.update_child()
            new_variable.connect("button_press_event", new_variable.on_new_variable, self.search_entry, wikidata)
        else:
            new_variable.child = NameDescriptionLabel("<b>Seleziona un item o una variabile</b>", "oppure definiscine una nuova")
            new_variable.set_sensitive(False)
            new_variable.update_child()
        self.listbox = ListBox()

        results = [var for var in wikidata.vars if query in var["Label"]] + wikidata.search(query)

        for r in results:
            row = Result(r)
            self.listbox.add(row)
        self.listbox.connect("row_activated", self.on_row_activated, button)
        self.scrolled.add(self.listbox)
        self.listbox.show_all()

    def on_row_activated(self, listbox, row, button):
        print(row.content)
        button.set_label(row.content["Label"])
        button.popover.hide()

class ExtendedModelButton(ModelButton):
    def __init__(self, widget, *args):
        ModelButton.__init__(self)
        self.forall(self.remove_children)
        self.child = widget
        self.args = args
        self.add(self.child)

    def update_child(self):
        self.forall(self.remove_children)
        self.add(self.child)
        self.show_all()

    def remove_children(self, *children):
        for child in children:
            self.remove(child)

    def on_new_variable(self, widget, event, search_entry, wikidata):
        var = search_entry.get_text()
        if not var in set([var["Label"] for var in wikidata.vars]) and var != "":
            wikidata.vars.append({"Label":var, "Description":"Sparql variable"})
        search_entry.set_text("")
        

class ItemSearchBox(VBox):
    def __init__(self, button, wikidata):
        VBox.__init__(self)
        search_entry = SearchEntry()
        vbox = NameDescriptionLabel("<b>Seleziona un item o una variabile</b>", "oppure definiscine una nuova")
        new_variable = ExtendedModelButton(vbox)
        new_variable.set_sensitive(False)
        results = ItemResultsBox(wikidata, search_entry, button)
        search_entry.connect("search_changed", results.on_query_changed, new_variable, button, wikidata)

        hbox = HBox()
        vbox = VBox()

        vbox.pack_start(search_entry, False, False, 10)
        vbox.pack_start(new_variable, False, False, 3)
        hbox.pack_start(vbox, True, True, 10)
        self.pack_start(hbox, False, True, 10)
        self.pack_start(results, True, True, 3)

class ItemSearchPopover(PopoverMenu):
    def __init__(self, parent, wikidata):
        PopoverMenu.__init__(self)
        self.set_relative_to(parent) 

class ItemSelectionButton(ModelButton):
    def __init__(self, wikidata, label="var"):
        ModelButton.__init__(self)

        self.set_css_name("subject")
        StyleContext.add_class(self.get_style_context(), "subject")

        self.set_label(label)
        self.set_tooltip_text("Seleziona la variabile o il valore da assumere come soggetto")

        self.popover = ItemSearchPopover(self, wikidata)
        self.connect ("clicked", self.on_self_clicked, self.popover)

        popover_box = VBox()

        popover_box.add(ItemSearchBox(self, wikidata))

        self.popover.add(popover_box)

    def remove_children(self, *args):
        for arg in args:
            self.remove(arg)

    def on_self_clicked(self, widget, popover):
        if popover.get_visible():
            popover.hide()
        else:
            popover.set_size_request(500,300)
            popover.show_all()

class SparqlConstraintsBox(HBox):
    def __init__(self, wikidata):
        HBox.__init__(self)
        self.scrolled = ScrolledWindow()
        self.scrolled.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.listbox = ListBox()
        self.scrolled.add(self.listbox)
        self.pack_start(self.scrolled, True, True, padding=30)

        new_constraint_row = ListBoxRow()
        eventbox = EventBox()
        new_icon = Image.new_from_icon_name('list-add-symbolic', IconSize.DIALOG)
        new_icon.set_pixel_size(32)
        eventbox.add(new_icon)
        new_constraint_row.add(eventbox)
        eventbox.connect("button_press_event", self.on_new_constraint_row, new_constraint_row, wikidata)

        self.listbox.add(new_constraint_row)

    def on_new_constraint_row(self, widget, event, new_constraint_row, wikidata):
        self.listbox.remove(new_constraint_row)
        row = ListBoxRow()
        triple_box = TripleBox(wikidata)
        eventbox = EventBox()
        eventbox.add(triple_box)
        row.add(eventbox)
        eventbox.connect("enter_notify_event", triple_box.enter)
        eventbox.connect("leave_notify_event", triple_box.leave)
        self.listbox.add(row)
        self.listbox.add(new_constraint_row)
        self.listbox.show_all()
        
        #edit_window = ConstraintEditWindow(self.listbox, row, wikidata)
        #edit_window.show_all()
        #print("selection_get")
        #for arg in args:
        #    print(arg)

class ConstraintEditWindow(Window):
    def __init__(self, listbox, row, wikidata):

        self.wikidata = wikidata

        # Window properties
        Window.__init__(self, title="Add items")
        self.set_border_width(0)
        self.set_default_size(800, 450)
        self.set_position(WindowPosition(1))
        self.set_title ("Add Item")
        #self.set_icon_from_file('icon.png')
        unix_signal_add(PRIORITY_DEFAULT, SIGINT, main_quit)

        # Headerbar        
        hb = HeaderBar()
        self.set_titlebar(hb)

        # Headerbar: Cancel Button
        removeButton = Button.new_with_label("Elimina")
        removeButton.get_style_context().add_class(STYLE_CLASS_DESTRUCTIVE_ACTION)
        removeButton.connect ("clicked", self.on_remove_button_clicked, listbox, row)

        # Headerbar: Add Button
        addButton = Button.new_with_label ("Aggiungi elementi")
        addButton.get_style_context().add_class(STYLE_CLASS_SUGGESTED_ACTION)
        #addButton.connect ("clicked", self.on_ConfirmNewChain_clicked, self, PriceEntry, RatioEntry, AmountEntry)

        hb.pack_start(removeButton)
        hb.set_title("test")
        hb.pack_end(addButton)

        triple_box = TripleBox(wikidata)
        vbox = VBox()
        vbox.pack_start(triple_box, False, False, 30)
        self.add(vbox)

        scrolled = ScrolledWindow()
        scrolled.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        description = TextView()
        description.set_wrap_mode(WrapMode(2))

        scrolled.add(description)
        vbox.pack_start(scrolled, True, True, 0)

    def on_remove_button_clicked(self, button, listbox, row):
        self.destroy()
        del self
        listbox.remove(row)
        del row

class TripleBox(HBox):
    def __init__(self, wikidata):
        HBox.__init__(self)
        hbox = HBox(homogeneous=True)
        self.pack_start(hbox, True, True, 4)
        subject = ItemSelectionButton(wikidata, "Soggetto")
        prop = ItemSelectionButton(wikidata, "Proprietà")
        obj = ItemSelectionButton(wikidata, "Oggetto")
        first = VBox()
        second = VBox()
        third = VBox()
        first.pack_start(subject, False, False, 4)
        second.pack_start(prop, False, False, 4)
        third.pack_start(obj, False, False, 4)
        hbox.pack_start(first, True, False, 0)
        hbox.pack_start(second, True, False, 0)
        hbox.pack_start(third, True, False, 0)

        self.remove_icon = Image.new_from_icon_name('edit-delete-symbolic', IconSize.BUTTON)
        self.remove_icon.set_visible(False)
        eventbox = HBox()
        eventbox.add(self.remove_icon)
        eventbox.connect("button_press_event", self.on_remove_icon_clicked)
        self.pack_end(eventbox, False, False, 4)
        
        #remove_icon.set_pixel_size(32)
        #remove_icon.get_style_context().add_class("dim-label")

    def on_remove_icon_clicked(self, *args):
        print("delete row")
        for arg in args:
            print(arg)

    def enter(self, *args):
        self.remove_icon.set_visible(True)
        for arg in args:
            print(arg)

    def leave(self, *args):
        self.remove_icon.set_visible(False)

class WikidataEditor():
    def __init__(self):
        wikidata = Wikidata()
        gtk_style()
        win = WelcomeWindow(wikidata)
        win.show_all()
        main()

if __name__ == "__main__":
    editor = WikidataEditor()
