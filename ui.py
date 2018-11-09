from gi import require_version
require_version('Gtk', '3.0')
require_version('Gdk', '3.0')
from wikidata import Wikidata
from gi.repository.Gdk import Color, Event, Screen
from gi.repository.Gio import ThemedIcon
from gi.repository.Gtk import main, main_quit, Align, Box, Button, CheckButton, CssProvider, Entry, EventBox, HBox, IconSize, Image, HeaderBar, Label, ListBox, ListBoxRow, ModelButton, Orientation, Overlay, PolicyType, PopoverMenu, Revealer, RevealerTransitionType, ScrolledWindow, SearchBar, SearchEntry, SelectionMode, Stack, StackSwitcher, StackTransitionType, StyleContext, TextView, VBox, Window, WindowPosition, WrapMode, STYLE_CLASS_DESTRUCTIVE_ACTION, STYLE_CLASS_SUGGESTED_ACTION, STYLE_PROVIDER_PRIORITY_APPLICATION
from gi.repository.GLib import unix_signal_add, PRIORITY_DEFAULT
from signal import SIGINT

def gtk_style():
    css = b"""
list {
    border-style: solid;
    border-width: 0px 1px 1px 1px;
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

.empty { 
    background-color: rgb(255,255,255);
    border-top-width: 5px;
    border-top-style: solid;
    border-top-color: rgb(255,255,255);
    border-left-width: 5px;
    border-left-style: solid;
    border-left-color: rgb(255,255,255);
    border-right-width: 5px;
    border-right-style: solid;
    border-right-color: rgb(255,255,255);
    border-bottom-width: 5px;
    border-bottom-style: solid;
    border-bottom-color: rgb(255,255,255);
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    border-bottom-right-radius: 5px;
    border-bottom-left-radius: 5px;
}

.unselected {

    background-color: rgb(186,189,182);
    border-top-width: 5px;
    border-top-style: solid;
    border-top-color: rgb(186,189,182);
    border-left-width: 5px;
    border-left-style: solid;
    border-left-color: rgb(186,189,182);
    border-right-width: 5px;
    border-right-style: solid;
    border-right-color: rgb(186,189,182);
    border-bottom-width: 5px;
    border-bottom-style: solid;
    border-bottom-color: rgb(186,189,182);
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    border-bottom-right-radius: 5px;
    border-bottom-left-radius: 5px;

}

.target { 
    background-color: rgb(90.8,192.8,121.6);
    border-top-width: 5px;
    border-top-style: solid;
    border-top-color: rgb(90.8,192.8,121.6);
    border-left-width: 5px;
    border-left-style: solid;
    border-left-color: rgb(90.8,192.8,121.6);
    border-right-width: 5px;
    border-right-style: solid;
    border-right-color: rgb(90.8,192.8,121.6);
    border-bottom-width: 5px;
    border-bottom-style: solid;
    border-bottom-color: rgb(90.8,192.8,121.6);
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
        self.set_default_size(500, 200)
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
        open_session = Button.new()
        open_session.set_label ("Apri sessione")
        open_session.connect ("clicked", self.on_constraint_search)
        hb.pack_start(open_session)

        # On demand stack
        stack = Stack()
        stack.set_transition_type (StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration (1000)

        # Stack revealer 
        stack_revealer = Revealer()
        stack_revealer.set_transition_type (RevealerTransitionType.CROSSFADE)
        stack_revealer.set_transition_duration(500)
        stack_revealer.set_reveal_child(False)
        stack_revealer.add(stack)

        # Label search
        label_search_page = LabelSearchPage(wikidata, set_visible_search_entry=True)
        stack.add_titled(label_search_page, "Cerca per etichetta", "Cerca per etichetta")

        # Sparql Page
        sparql_page = SparqlPage(wikidata)
        stack.add_titled(sparql_page, "Cerca per vincolo", "Cerca per vincolo")

        # Back button
        back = Button.new_from_icon_name("go-previous-symbolic", size=IconSize.BUTTON)

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

        # Welcome page
        self.search_visible = False
        daty_description = """Daty ti permette di consultare e modificare Wikidata in maniera facile e intuitiva. <br>
<b>Batti sulla tastiera per cercare o creare nuovi elementi</b> oppure clicca sul pulsante in basso per utilizzare la ricerca avanzata!"""
        welcome_page = WelcomePage(icon_name="system-search-symbolic",
                                   description=daty_description,
                                   button_text="Aggiungi un vincolo",
                                   button_callback=self.on_constraint_search,
                                   callback_arguments=[stack, sparql_page, hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, welcome_revealer],
                                   parent=self)
        welcome_revealer.add(welcome_page)

        # Write to search
        self.connect("key_press_event", self.on_key_press, hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer)
        back.connect("clicked", self.on_back_button, hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer)

    def on_key_press(self, widget, event, hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer):
        if self.search_visible:
            if event.keyval == 65307:
                self.deactivate_search(hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer)
        if not self.search_visible:
            if not event.keyval == 65307:
                self.activate_search(hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer)

    def on_back_button(self, button, hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer):
        self.deactivate_search(hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer)

    def activate_search(self, hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer):
        # Hide welcome and title
        welcome_revealer.set_reveal_child(False)
        self.remove(welcome_revealer)
        title_revealer.set_reveal_child(False)
        hb.remove(open_session)

        # Show switcher, stack and back
        hb.pack_start(back)
        hb.set_custom_title(switcher_revealer)
        switcher_revealer.set_reveal_child(True)
        hb.show_all()
        self.add(stack_revealer)
        stack_revealer.set_reveal_child(True)

        # Set search visible
        stack.set_visible_child_full("Cerca per etichetta", StackTransitionType.NONE)
        self.search_visible = True 
        self.show_all()
        search_entry = stack.get_child_by_name("Cerca per etichetta").search_entry
        search_entry.grab_focus_without_selecting()

    def deactivate_search(self, hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer):
        # Hide stack, switcher and back
        stack_revealer.set_reveal_child(False)
        self.remove(stack_revealer)
        switcher_revealer.set_reveal_child(False)
        hb.remove(back)

        # Show title and welcome
        hb.set_custom_title(title_revealer)
        hb.pack_start(open_session)
        title_revealer.set_reveal_child(True)
        hb.show_all()
        self.add(welcome_revealer)
        welcome_revealer.set_reveal_child(True)

        # Set search not visible
        self.search_visible = False
        search_entry = stack.get_child_by_name("Cerca per etichetta").search_entry
        search_entry.set_text("")
        self.show_all()

    def on_constraint_search(self, button, stack, sparql_page, hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, welcome_revealer):
        self.activate_search(hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, stack, welcome_revealer)
        stack.set_visible_child_full("Cerca per vincolo", StackTransitionType.NONE)
        sparql_page.constraints.eventbox.emit("button_press_event", Event())
        #add_items = AddItemsWindow(wikidata)
        #add_items.show_all()

    def on_tet(self, *args):
        print(*args)

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
        vbox.pack_start(icon, False, True, 25)

        # Welcome text box
        textbox = Box(orientation=Orientation(1))
        vbox.pack_start(textbox, False, True, 0)

        if description:
            # Welcome description
            for line in description.split("<br>"):
                label = Label(label=line, halign=Align.FILL)
                label.set_max_width_chars(50)
                label.set_use_markup(True)
                label.set_line_wrap(True)
                textbox.pack_start(label, True, True, 0)

        if button_text:

            # Welcome button
            button = Button.new_with_label(button_text)
            button.get_style_context().add_class(STYLE_CLASS_SUGGESTED_ACTION)
            if button_callback:
                button.connect ("clicked", button_callback, *callback_arguments)

            # Welcome button box
            button_box = Box(orientation=Orientation(0))
            button_box.pack_start(button, True, False, 0)                
            vbox.pack_start(button_box, False, False, 25)

class AddWindow(Window): # Da scrivere meglio

    def __init__(self, wikidata):
         
        # Window properties
        Window.__init__(self, title="Aggiungi elementi")
        self.set_border_width(0)
        self.set_default_size(500, 200)
        self.set_position(WindowPosition(1))
        self.set_title ("Aggiungi elementi")
        #self.set_icon_from_file('icon.png')
        unix_signal_add(PRIORITY_DEFAULT, SIGINT, main_quit)

        # Headerbar        
        hb = HeaderBar()
        self.set_titlebar(hb)

        # Stack
        stack = Stack()
        stack.set_transition_type (StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration (1000)

        label_search = LabelSearchPage(wikidata)
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
    def __init__(self, name, description, vertical_padding=2):
        # Init
        VBox.__init__(self)
        self.name = name
        self.description = description

        # Name
        name = Label(halign=Align.START)
        name.set_label(self.name)
        name.set_use_markup(True)
        name.set_xalign(0)
        name.set_line_wrap(True)

        # Description
        description = Label(halign=Align.START)
        description.set_label("<span font_desc=\"8.0\">" + self.description + "</span>")
        description.set_xalign(0)
        description.set_line_wrap(True)
        description.set_use_markup(True)

        # Vertical box
        vbox = VBox()
        vbox.pack_start(name, True, True, 0)
        vbox.pack_start(description, True, True, 0)
        self.pack_start(vbox, True, True, vertical_padding)

class Result(ListBoxRow):
    def __init__(self, result):
        ListBoxRow.__init__(self)
        self.content = result

        # Horizontal Box
        self.hbox = HBox()
        self.add(self.hbox)

        # Contents Box
        self.update()
        self.hbox.pack_start(self.name_description, True, True, self.padding)

    def update(self):
        text = "<b>" + self.content["Label"] + "</b>"
        if "URI" in self.content.keys():
            text = text + " <span font_desc=\"8.0\">(" + self.content["URI"] + ")</span>"
            checkbox = CheckButton()
            self.hbox.pack_start(checkbox, False, False, 10)
            self.padding = 0
        else:
            self.padding = 20
        self.name_description = NameDescriptionLabel(text, self.content["Description"])
        self.show_all() 

class ResultsBox(HBox):
    def __init__(self, horizontal_padding=0):
        HBox.__init__(self)

        # Scrolled Box
        self.scrolled = ScrolledWindow()
        self.scrolled.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.pack_start(self.scrolled, True, True, padding=horizontal_padding)

        # List Box
        self.listbox = ListBox()
        self.scrolled.add(self.listbox)

class LabelSearchPage(VBox):

    def __init__(self, wikidata, set_visible_search_entry=True, results_border=0):
        VBox.__init__(self)

        # Search Box
        search_box = HBox()
        self.pack_start(search_box, False, False, 0)

        # Results Box
        results = ResultsBox()
        self.pack_start(results, True, True, results_border)

        # Search Entry
        self.search_entry = SearchEntry()
        self.search_entry.connect("search_changed", self.on_search_changed, results, wikidata)
        self.search_entry.show()

        # Search bar
        self.search_bar = SearchBar()
        self.search_bar.set_search_mode(True)
        self.search_bar.connect_entry(self.search_entry)
        self.search_bar.add(self.search_entry)
        search_box.pack_start(self.search_bar, expand=True, fill=True, padding=0)

    def on_search_changed(self, search_entry, results, wikidata):
        # Get query
        query = search_entry.get_text()

        # Clean results
        results.scrolled.remove(results.listbox)
        results.listbox = ListBox()

        # Obtain data
        if query != "":
            data = wikidata.search(query)
        else:
            data = []

        # Populate results
        for d in data:
            row = Result(d)
            results.listbox.add(row)
        results.scrolled.add(results.listbox)
        results.listbox.show_all()

class SparqlPage(VBox):
    def __init__(self, wikidata):
        VBox.__init__(self)

        # Selection Box
        selection_box = HBox()
        self.pack_start(selection_box, False, False, 0)

        # Label + Button horizontal Box
        label_button_box = HBox()

        # Select label
        label = Label()
        label.set_label("Seleziona")
        label_button_box.pack_start(label, True, True, 2)

        # Selected variable
        variable = ButtonWithPopover(text="variabile", css="unselected")
        label_button_box.pack_start(variable, True, True, 2)
        label_button_box.remove(variable)
        label_button_box.pack_start(variable, True, True, 2)

        # Search bar
        self.selection_bar = SearchBar()
        self.selection_bar.set_search_mode(True)
        self.selection_bar.add(label_button_box)
        selection_box.pack_start(self.selection_bar, expand=True, fill=True, padding=0)

        # Constraints
        self.constraints = EditableListBox(new_row_callback=self.new_constraint, new_row_callback_arguments = [wikidata], horizontal_padding=0)
        self.pack_start(self.constraints, True, True, 0)

    def new_constraint(self, row, wikidata):
        # Add a triple box
        triple_box = TripleBox(wikidata)
        same_size_widget = TripleBox(wikidata, css="empty")
        row.add_widget(triple_box, same_size_widget)

class ItemResults(HBox):
    def __init__(self, wikidata, search_entry, button, horizontal_padding=10):
        HBox.__init__(self)
        self.search_entry = search_entry
        self.pack_start(self.scrolled, True, True, padding=horizontal_padding)

        # Scrolled Window
        self.scrolled = ScrolledWindow()
        self.scrolled.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)

        # ListBox             			# per dopo l'itwikicon. rendere eliminabili le variabili dichiarate
        self.listbox = ListBox()
        self.scrolled.add(self.listbox)
        self.listbox.connect("row_activated", self.on_row_activated, button)
        self.listbox.show_all()

        # Populate listbox with sparql vars
        for var in wikidata.vars:
            row = Result(var)
            self.listbox.add(row)

    def on_query_changed(self, widget, new_variable, button, wikidata):

        # Obtain query from search widget
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
        self.child = widget
        self.args = args

        # Remove and replace child
        self.forall(self.remove_children)
        self.add(self.child)
        self.show_all()

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

        # Search entry
        search_entry = SearchEntry()

        # New variable button 
        new_variable_label = NameDescriptionLabel("<b>Seleziona un item o una variabile</b>", "oppure definiscine una nuova")
        new_variable = ExtendedModelButton(new_variable_label)
        new_variable.set_sensitive(False)

        
        results = ItemResults(wikidata, search_entry, button)
        search_entry.connect("search_changed", results.on_query_changed, new_variable, button, wikidata)

        hbox = HBox()
        vbox = VBox()

        vbox.pack_start(search_entry, False, False, 10)
        vbox.pack_start(new_variable, False, False, 3)
        hbox.pack_start(vbox, True, True, 10)
        self.pack_start(hbox, False, True, 10)
        self.pack_start(results, True, True, 3)

class BetterPopover(PopoverMenu):
    def __init__(self, parent, child, width=500, height=300):
        PopoverMenu.__init__(self)
        self.width = width
        self.height = height
        self.set_relative_to(parent) 
        self.add(child)

    def trigger(self):
        if self.get_visible():
            self.hide()
        else:
            self.set_size_request(self.width, self.height)
            self.show_all()

class ButtonWithPopover(EventBox):
    def __init__(self, popover_box=None, text="var", css="unselected"):
        EventBox.__init__(self)

        if popover_box == None: # test
            popover_box = ItemSearchBox(self, Wikidata())

        # Popover
        popover = BetterPopover(self, popover_box)
        self.connect ("button_press_event", self.clicked, popover)

        # Label and style
        label = Label()
        label.set_label(text)
        label.set_tooltip_text("Seleziona la variabile o il valore da assumere come soggetto")
        StyleContext.add_class(label.get_style_context(), css)
        self.add(label)

    def remove_children(self, *args):
        for arg in args:
            self.remove(arg)

    def clicked(self, widget, event, popover):
        popover.trigger()

class EditableListBox(HBox):
    def __init__(self, new_row_callback=None, new_row_callback_arguments=[], delete_row_callback=None, delete_row_callback_arguments=[], horizontal_padding=0, new_row_height=14, selectable=0):
        HBox.__init__(self)

        # Scrolled window
        self.scrolled = ScrolledWindow()
        self.scrolled.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.pack_start(self.scrolled, True, True, padding=horizontal_padding)

        # Listbox
        self.listbox = ListBox()
        self.listbox.set_selection_mode(SelectionMode(selectable))
        self.scrolled.add(self.listbox)

        # New row
        new_row = ListBoxRow()
        self.listbox.add(new_row)

        # New row icon
        icon = Image.new_from_icon_name('list-add-symbolic', IconSize.MENU)

        # New row VBox
        vbox = VBox()
        vbox.pack_start(icon, True, True, new_row_height)

        # New row Eventbox
        self.eventbox = EventBox()
        self.eventbox.add(vbox)
        self.eventbox.connect("button_press_event", self.on_new_row, new_row,
                                               new_row_callback, new_row_callback_arguments,
                                               delete_row_callback, delete_row_callback_arguments)
        new_row.add(self.eventbox)

    def on_new_row(self, widget, event, new_row,
                                        new_row_callback, new_row_callback_arguments,
                                        delete_row_callback, delete_row_callback_arguments):

        # Remove "New row" from ListBox
        self.listbox.remove(new_row)

        # Create new row and give it to callback
        row = EditableListBoxRow(self.listbox, delete_row_callback, *delete_row_callback_arguments)
        new_row_callback(row, *new_row_callback_arguments)

        # Add the new row to the listbox with the "New row" button
        self.listbox.add(row)
        self.listbox.add(new_row)
        self.listbox.show_all()

class EditableListBoxRow(ListBoxRow):
    def __init__(self, listbox, delete_callback=None, delete_callback_arguments=[], vertical_padding=10):
        ListBoxRow.__init__(self)
        self.set_activatable(False)

        # Overlay
        self.overlay = Overlay()
        
        # Remove Icon
        self.remove_icon = Image.new_from_icon_name('window-close-symbolic', IconSize.BUTTON)

        # Remove Row EventBox
        remove_row_eventbox = EventBox()
        remove_row_eventbox.add(self.remove_icon)
        remove_row_eventbox.connect("button_press_event", self.on_delete_row, listbox, delete_callback, *delete_callback_arguments)
       
        # Remove Row Revealer
        self.revealer = Revealer()
        self.revealer.set_transition_type (RevealerTransitionType.NONE)
        self.revealer.add(remove_row_eventbox)
        self.revealer.set_reveal_child(False)
        self.revealer.set_property("halign", Align.END)

        # Event Box
        eventbox = EventBox()
        eventbox.set_above_child(False)
        eventbox.add(self.overlay)
        eventbox.connect("enter_notify_event", self.enter)
        eventbox.connect("leave_notify_event", self.leave)
        self.add(eventbox)

    def add_widget(self, widget, same_size_widget): 
        self.overlay.add(same_size_widget)
        self.overlay.add_overlay(widget)
        self.overlay.add_overlay(self.revealer)
        self.show_all()
 
    def on_delete_row(self, widget, event, listbox, callback, *callback_arguments):
        listbox.remove(self)
        callback(self, widget, event, *callback_arguments)

    def enter(self, widget, event):
        self.revealer.set_reveal_child(True)

    def leave(self, widget, event):
        self.revealer.set_reveal_child(False)

class TripleBox(VBox):
    def __init__(self, wikidata, css="unselected", first="Soggetto", second="Proprietà", third="Oggetto", vertical_padding=8):
        VBox.__init__(self)

        # Tuple Box
        hbox = HBox()
        self.pack_start(hbox, True, True, vertical_padding)

        # S/P/O 
        subject = ButtonWithPopover(text=first, css=css)
        prop = ButtonWithPopover(text=second, css=css)
        obj = ButtonWithPopover(text=third, css=css)

        # Tuple
        first = VBox()
        second = VBox()
        third = VBox()
        first.pack_start(subject, False, False, 0)
        second.pack_start(prop, False, False, 0)
        third.pack_start(obj, False, False, 0)

        # Tuple Box
        tuple_box = HBox(homogeneous=True)
        tuple_box.pack_start(first, True, False, 0)
        tuple_box.pack_start(second, True, False, 0)
        tuple_box.pack_start(third, True, False, 0)
        hbox.pack_start(tuple_box, True, True, vertical_padding)

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

class WikidataEditor():
    def __init__(self):
        wikidata = Wikidata(verbose=False)
        gtk_style()
        win = WelcomeWindow(wikidata)
        win.show_all()
#        add_ = AddItemsWindow(wikidata)
#        add_.show_all()
        main()

if __name__ == "__main__":
    editor = WikidataEditor()
