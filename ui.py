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
    border-width: 0px 1px 0px 1px;
}

row {
    border-bottom-color: rgb(192,192,189);
    border-bottom-style: solid;
    border-bottom-width: 1px;
}

.itemResultsListBox {
    border-style: solid;
    border-width: 1px 1px 1px 1px;
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
    color: white;
}

.unselected { 
    background-image: linear-gradient(180deg, #c2c0be, #c2c0be);
    border-bottom-width:1px;
    border-color: #5d5d64;
    border-radius: 7px;
    border-style: solid;
    border-width:0.5px;
    color: white;
    padding: 4.5px;
    text-shadow: 1px 1px #5d5d64;
}

.variable { 
    background-image: linear-gradient(180deg, #fb7d40, #fb7d40);
    border-bottom-width:1px;
    border-color: #a04127;
    border-radius: 7px;
    border-style: solid;
    border-width:0.5px;
    color: white;
    padding: 4.5px;
    text-shadow: 0px -1px #a04127;
}

.property { 
    background-image: linear-gradient(180deg, #b783cb, #b783cb);
    border-bottom-width:1px;
    border-color: #8864ac;
    border-radius: 7px;
    border-style: solid;
    border-width:0.5px;
    color: white;
    padding: 4.5px;
    text-shadow: 0px -1px #8864ac;
}

.item { 
    background-image: linear-gradient(180deg, #b58261, #b58261);
    border-bottom-width:1px;
    border-color: #865c41;
    border-radius: 7px;
    border-style: solid;
    border-width:0.5px;
    color: white;
    padding: 4.5px;
    text-shadow: 0px -1px #865c41;
}


.target { 
    background-image: linear-gradient(180deg, #5bc17a, #52b47d);
    border-bottom-width:1.5px;
    border-color: #439768;
    border-radius: 7px;
    border-style: solid;
    border-width:1px;
    color: white;
    padding: 4.5px;
    text-shadow: 0px -1px #2d6445;
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
        stack.set_transition_duration (500)

        # Stack revealer 
        stack_revealer = Revealer()
        stack_revealer.set_transition_type (RevealerTransitionType.CROSSFADE)
        stack_revealer.set_transition_duration(500)
        stack_revealer.set_reveal_child(False)
        stack_revealer.add(stack)

        # Label search
        label_search_page = LabelSearchPage(wikidata, set_visible_search_entry=True)
        stack.add_titled(label_search_page, "Seleziona per etichetta", "Seleziona per etichetta")

        # Sparql Page
        sparql_page = SparqlPage(wikidata)
        stack.add_titled(sparql_page, "Seleziona per vincolo", "Seleziona per vincolo")

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
<b>Digita sulla tastiera quello che vorresti consultare</b> oppure clicca sul pulsante in basso per utilizzare il form di selezione avanzata!"""
        welcome_page = WelcomePage(icon_name="system-search-symbolic",
                                   description=daty_description,
                                   button_text="Aggiungi un vincolo",
                                   button_callback=self.on_constraint_search,
                                   button_callback_arguments=[stack, sparql_page, hb, open_session, back, title_revealer, switcher_revealer, stack_revealer, welcome_revealer],
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
        stack.set_visible_child_full("Seleziona per etichetta", StackTransitionType.NONE)
        self.search_visible = True 
        self.show_all()
        search_entry = stack.get_child_by_name("Seleziona per etichetta").search_entry
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
        stack.set_visible_child_full("Seleziona per vincolo", StackTransitionType.NONE)
        #sparql_page.constraints.eventbox.emit("button_press_event", Event())
        #add_items = AddItemsWindow(wikidata)
        #add_items.show_all()

    def on_tet(self, *args):
        print(*args)

class WelcomePage(HBox):
    def __init__(self, icon_name='system-search-symbolic', icon_size=192, vpadding=25, description="Sample description", description_max_length=50, button_text=None, button_callback=None, button_callback_arguments=[], parent=None):
        HBox.__init__(self)

        #Vertical Box
        vbox = VBox()
        self.pack_start(vbox, expand=True, fill=False, padding=0)

        # Placeholder image
        icon = Image.new_from_icon_name(icon_name, size=IconSize.DIALOG)
        icon.set_pixel_size(icon_size)
        icon.get_style_context().add_class("dim-label")
        vbox.pack_start(icon, False, True, vpadding)

        # Welcome text box
        textbox = Box(orientation=Orientation(1))
        vbox.pack_start(textbox, False, True, 0)

        if description:

            if not button_text:
                tb_padding = vpadding
            else:
                tb_padding = 0
            # Welcome description
            for line in description.split("<br>"):
                label = Label(label=line, halign=Align.FILL)
                label.set_max_width_chars(description_max_length)
                label.set_use_markup(True)
                label.set_line_wrap(True)
                textbox.pack_start(label, True, True, tb_padding)

        if button_text:

            # Welcome button
            button = Button.new_with_label(button_text)
            button.get_style_context().add_class(STYLE_CLASS_SUGGESTED_ACTION)
            if button_callback:
                button.connect ("clicked", button_callback, *button_callback_arguments)

            # Welcome button box
            button_box = Box(orientation=Orientation(0))
            button_box.pack_start(button, True, False, 0)                
            vbox.pack_start(button_box, False, False, vpadding)

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
    def __init__(self, wikidata, selection_vpadding=3):
        VBox.__init__(self)

        # Selection Box
        selection_box = VBox()
        self.pack_start(selection_box, False, False, 0)

        # label + Button vertical Box
        label_button_vbox = VBox()

        # Label + Button horizontal Box
        label_button_hbox = HBox()
        label_button_vbox.pack_start(label_button_hbox, True, True, selection_vpadding)

        # Select label
        label = Label()
        label.set_label("Seleziona")
        label_button_hbox.pack_start(label, True, True, 2)

        # Selected variable
        variable = ButtonWithPopover(text="variabile", css="target", vpadding=2)
        variable.set_popover_box(ItemSearchBox(variable, wikidata, type="var"))
        label_button_hbox.pack_start(variable, True, True, 2)

        # Search bar
        self.selection_bar = SearchBar()
        self.selection_bar.set_search_mode(True)
        self.selection_bar.add(label_button_vbox)
        selection_box.pack_start(self.selection_bar, expand=True, fill=True, padding=0)

        # Constraints
        self.constraints = EditableListBox(new_row_callback=self.new_constraint, new_row_callback_arguments = [wikidata], horizontal_padding=0)
        self.pack_start(self.constraints, True, True, 0)
        self.constraints.eventbox.emit("button_press_event", Event())

    def new_constraint(self, row, wikidata):
        # Add a triple box
        triple_box = TripleBox(wikidata)
        same_size_widget = TripleBox(wikidata, first=" ", second=" ", third=" ", css="empty")
        row.add_widget(triple_box, same_size_widget)

class ItemResults(HBox):
    def __init__(self, wikidata, row_activated_callback=None, row_activated_callback_arguments=[]):
        HBox.__init__(self)

        # Scrolled Window
        self.scrolled = ScrolledWindow()
        self.scrolled.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.pack_start(self.scrolled, True, True, padding=0)

        # ListBox             			# per dopo l'itwikicon. rendere eliminabili le variabili dichiarate
        self.listbox = ListBox()
        StyleContext.add_class(self.listbox.get_style_context(), "itemResultsListBox")
        self.scrolled.add(self.listbox)
        self.listbox.connect("row_activated", self.on_row_activated, row_activated_callback, row_activated_callback_arguments)
        self.listbox.show_all()

        # Populate listbox with sparql vars
        for var in wikidata.vars:
            row = Result(var)
            self.listbox.add(row)


    def on_row_activated(self, listbox, row, row_activated_callback, row_activated_callback_arguments):
        row_activated_callback(self, listbox, row, *row_activated_callback_arguments)

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

class ItemSearchBox(VBox):
    def __init__(self, item_selection_button, wikidata, type="var+search", vpadding=2, hpadding=4):
        VBox.__init__(self)
        if type == "var":
            icon_name = "bookmark-new-symbolic"
            description = "Definisci una nuova variabile"
        if type == "var+search":
            icon_name = "system-search-symbolic"
            description = "Cerca un item o una variabile, oppure <b>definiscine una nuova</b>"

        # Horizontal box
        hbox = HBox()
        self.pack_start(hbox, True, True, 0)

        # Vertical box
        vbox = VBox()
        hbox.pack_start(vbox, True, True, hpadding)

        # Search entry
        self.search_entry = SearchEntry()
        vbox.pack_start(self.search_entry, False, False, vpadding)

        # Placeholder
        welcome_page = WelcomePage(icon_name=icon_name,
                                   icon_size=96,
                                   vpadding=15,
                                   description=description,
                                   description_max_length=25,
                                   parent=None)

        # Placeholder revealer
        welcome_revealer = Revealer()
        welcome_revealer.set_transition_type(RevealerTransitionType.NONE)
        welcome_revealer.set_reveal_child(True)
        welcome_revealer.add(welcome_page)
        vbox.pack_start(welcome_revealer, False, True, vpadding)

        # Results revealer
        results_revealer = Revealer()
        results_revealer.set_transition_type(RevealerTransitionType.NONE)
        results_revealer.set_reveal_child(False)
        results_revealer_box = VBox()
        results_revealer.add(results_revealer_box)
        vbox.pack_start(results_revealer, True, True, 0)

        # New variable button 
        new_variable_label = NameDescriptionLabel("<b>Seleziona un item o una variabile</b>", "oppure definiscine una nuova")
        new_variable = ExtendedModelButton(new_variable_label)
        new_variable.set_sensitive(False)
        results_revealer_box.pack_start(new_variable, False, False, vpadding)

        # Search results 
        results = ItemResults(wikidata,
                              row_activated_callback=self.on_result_clicked,
                              row_activated_callback_arguments=[item_selection_button])
        results.set_visible(False)
        self.search_entry.connect("search_changed", self.on_search_changed, results_revealer,
                                                    welcome_revealer,
                                                    new_variable, results,
                                                    item_selection_button, wikidata)
        results_revealer_box.pack_start(results, True, True, vpadding)

    def on_new_variable(self, widget, event, welcome_revealer, item_selection_button, query, wikidata):
        var = self.search_entry.get_text()
        labels = set([v["Label"] for v in wikidata.vars])
        
        if not var in labels and var != "":
            wikidata.vars.append({"Label":var, "Description":"Sparql variable"})

        item_selection_button.popover.trigger()
        item_selection_button.label.set_label(query)
        item_selection_button.set_css("variable")
        self.search_entry.set_text("")
        welcome_revealer.set_reveal_child(False)

    def on_result_clicked(self, item_results, listbox, row, item_selection_button):
        item_selection_button.label.set_label(row.content["Label"])
        item_selection_button.popover.hide()
        print(row.content)
        self.process_type(row.content, item_selection_button)

    def process_type(self, dictionary, item_selection_button):
        if "URI" in dictionary.keys():
            if dictionary["URI"].startswith("Q"):
                item_selection_button.set_css("item")
            if dictionary["URI"].startswith("P"):
                item_selection_button.set_css("property")
            if dictionary["URI"] == "":
                item_selection_button.set_css("variable")
        else:
            item_selection_button.set_css("variable")


    def on_search_changed(self, widget, results_revealer, welcome_revealer, new_variable, results, item_selection_button, wikidata):

        # Obtain query from search widget
        query = widget.get_text()

        if query != "":
            # Hide welcome and show search revealer
            welcome_revealer.set_reveal_child(False)
            results_revealer.set_reveal_child(True)

            # Check variable existence
            labels = set([v["Label"] for v in wikidata.vars])
            if query in labels:
                description = "Seleziona variabile"
            else:
                description = "Registra variabile"

            # Set new variable label
            new_variable.child = NameDescriptionLabel("<b>" + query + "</b>", description)
            new_variable.set_sensitive(True)
            new_variable.update_child()
            new_variable.connect("button_press_event", self.on_new_variable, welcome_revealer, item_selection_button, query, wikidata)

        if query == "":
            if wikidata.vars == []:
                # Hide revealer and show placeholder
                results_revealer.set_reveal_child(False)
                welcome_revealer.set_reveal_child(True)

            if wikidata.vars != []:
                # Show new variable not selectable and hide welcome revealer
                new_variable.child = NameDescriptionLabel("<b>Seleziona un item o una variabile</b>", "oppure definiscine una nuova")
                new_variable.set_sensitive(False)
                new_variable.update_child()
                new_variable.set_visible(True)
                welcome_revealer.set_reveal_child(False)

        if query != "" or wikidata.vars != []:
            # Destroy and re-create listbox
            results.scrolled.remove(results.listbox)
            results.listbox = ListBox()
            StyleContext.add_class(results.listbox.get_style_context(), "itemResultsListBox")
            results.listbox.connect("row_activated", results.on_row_activated, self.on_result_clicked, [item_selection_button])
            results.scrolled.add(results.listbox)
         
            # Get data
            data = [v for v in wikidata.vars if query in v["Label"] and query != v["Label"]] + wikidata.search(query)
         
            # Populate listbox
            for d in data:
                row = Result(d)
                results.listbox.add(row)
            results.listbox.show_all()
            results.set_visible(True)

class BetterPopover(PopoverMenu):
    def __init__(self, parent, child, width=300, height=275, vpadding=2):
        PopoverMenu.__init__(self)
        self.width = width
        self.height = height
        self.set_relative_to(parent)
        vbox = VBox()
        vbox.pack_start(child, True, True, vpadding)
        self.add(vbox)

    def trigger(self):
        if self.get_visible():
            self.hide()
        else:
            self.set_size_request(self.width, self.height)
            self.show_all()

class ButtonWithPopover(EventBox):
    def __init__(self, popover_box=None, text="var", css="unselected", vpadding=2):
        EventBox.__init__(self)
        if popover_box == None:
            popover_box = HBox()

        # Popover
        self.popover = BetterPopover(self, popover_box, vpadding=vpadding)
        self.connect ("button_press_event", self.clicked)

        # Label and style
        self.label = Label()
        self.label.set_label(text)
        self.label.set_use_markup(True)
        self.label.set_line_wrap(False)
        self.label.set_max_width_chars(30)
        self.set_css(css)
        self.add(self.label)

    def set_css(self, css):
        self.label.set_tooltip_text("Seleziona la variabile o il valore da assumere come soggetto")
        StyleContext.add_class(self.label.get_style_context(), css)
        self.label.set_css_name(css)
        gtk_style()
        self.label.show_all()

    def set_popover_box(self, popover_box):
        self.popover = BetterPopover(self, popover_box)

    def clicked(self, widget, event):
        self.popover.trigger()

class EditableListBox(HBox):
    def __init__(self, new_row_callback=None, new_row_callback_arguments=[], delete_row_callback=None, delete_row_callback_arguments=[], horizontal_padding=0, new_row_height=14, selectable=0):
        HBox.__init__(self)

        # Scrolled window
        self.scrolled = ScrolledWindow()
        self.scrolled.set_policy(PolicyType.AUTOMATIC, PolicyType.AUTOMATIC)
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

        # Data handling
        self.triple = (0,0,0)
        #if css !=
        wikidata.triples.append(self.triple)

        # Tuple Box
        hbox = HBox()
        self.pack_start(hbox, True, True, vertical_padding)

        # S/P/O
        subject = ButtonWithPopover(text=first, css=css)
        subject.set_popover_box(ItemSearchBox(subject, wikidata))
        prop = ButtonWithPopover(text=second, css=css)
        prop.set_popover_box(ItemSearchBox(prop, wikidata))
        obj = ButtonWithPopover(text=third, css=css)
        obj.set_popover_box(ItemSearchBox(obj, wikidata))

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
        main()

if __name__ == "__main__":
    editor = WikidataEditor()
