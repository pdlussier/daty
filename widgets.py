from gi.repository.Gtk import Align, Button, CheckButton, EventBox, HBox, IconSize, Image, Label, ListBox, ListBoxRow, ModelButton, Overlay, PolicyType, PopoverMenu, Revealer, RevealerTransitionType, ScrolledWindow, SearchEntry, SelectionMode, StyleContext, TextView, VBox, STYLE_CLASS_SUGGESTED_ACTION, STYLE_PROVIDER_PRIORITY_APPLICATION
from util import import_translations, gtk_style
from wikidata import Wikidata

lang = import_translations('it')
wikidata = Wikidata(verbose=False)

class WelcomePage(HBox):
    def __init__(self, icon_name='system-search-symbolic', icon_size=192, vpadding=25,
                       description="Sample description", description_max_length=50,
                       button_text=None, button_callback=None, button_callback_arguments=[],
                       parent=None):
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
        textbox = VBox()
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
            button_box = HBox()
            button_box.pack_start(button, True, False, 0)
            vbox.pack_start(button_box, False, False, vpadding)

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

class ItemResults(HBox):
    def __init__(self, row_activated_callback=None, row_activated_callback_arguments=[]):
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
            row = Result(self.listbox, var)
            self.listbox.add(row)

    def on_row_activated(self, listbox, row, callback, arguments):
        callback(self, listbox, row, *arguments)

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

class BetterPopover(PopoverMenu):
    def __init__(self, parent, child,
                       width=300, height=275, vpadding=2):
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
    def __init__(self, popover_box=None, data=None,
                       text="var", css="unselected", vpadding=2):
        EventBox.__init__(self)
        self.data = data
        if popover_box == None:
            popover_box = HBox()

        # Popover
        self.popover = BetterPopover(self, popover_box, vpadding=vpadding)
        self.connect ("button_press_event", self.clicked)

        # Label and style
        self.label = Label()
        self.label.set_label(text)
        self.label.set_use_markup(True)
        self.label.set_line_wrap(True)
        self.label.set_max_width_chars(50)
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

    def set_data(self, data):
        self.data = data
        self.label.set_label(data["Label"])

class EditableListBox(HBox):
    def __init__(self, new_row=True, new_row_callback=None, new_row_callback_arguments=[],
                       delete_row_callback=None, delete_row_callback_arguments=[],
                       row_activated_callback=None, row_activated_callback_arguments=[],
                       horizontal_padding=0, selectable=0, css="sidebar",
                       new_row_height=14):
        HBox.__init__(self)
        self.get_style_context().add_class("sidebar")
        self.new_row = new_row

        # Scrolled window
        self.scrolled = ScrolledWindow()
        self.scrolled.set_policy(PolicyType.AUTOMATIC, PolicyType.AUTOMATIC)
        self.pack_start(self.scrolled, True, True, padding=horizontal_padding)

        # Listbox
        self.listbox = ListBox()
        self.listbox.set_selection_mode(SelectionMode(selectable))
        self.listbox.connect("row_activated", self.on_row_activated, row_activated_callback, row_activated_callback_arguments)
        self.listbox.connect("motion-notify-event", self.motion)
        self.scrolled.add(self.listbox)

        if new_row:
            self.new_row = ListBoxRow()
            self.listbox.add(self.new_row)

            # New row icon
            icon = Image.new_from_icon_name('list-add-symbolic', IconSize.MENU)

            # New row VBox
            vbox = VBox()
            vbox.pack_start(icon, True, True, new_row_height)

            # New row Eventbox
            self.eventbox = EventBox()
            self.eventbox.add(vbox)
            self.eventbox.connect("button_press_event", self.on_new_row, self.new_row,
                                                   new_row_callback, new_row_callback_arguments,
                                                   delete_row_callback, delete_row_callback_arguments)
            self.new_row.add(self.eventbox)

    def motion(self, listbox, event):
        row = listbox.get_row_at_y(event.y)
        try:
            self.lastrow
        except:
            self.lastrow = row
        if row != self.lastrow:
            try:
                row.revealer.set_reveal_child(True)
            except:
                pass
            try:
                self.lastrow.revealer.set_reveal_child(False)
            except:
                pass
            self.lastrow = row

    def on_row_activated(self, listbox, row, callback, arguments):
        callback(self, listbox, row, *arguments)

    def on_new_row(self, widget, event, new_row,
                                        new_row_callback, new_row_callback_arguments,
                                        delete_row_callback, delete_row_callback_arguments):

        if self.new_row:
            # Remove "New row" from ListBox
            self.listbox.remove(new_row)

        # Create new row and give it to callback
        row = EditableListBoxRow(self.listbox, delete=True, delete_callback=delete_row_callback, delete_callback_arguments=delete_row_callback_arguments)
        new_row_callback(row, *new_row_callback_arguments)

        # Add the new row to the listbox with the "New row" button
        self.listbox.add(row)
        if self.new_row:
            self.listbox.add(new_row)
        self.listbox.show_all()

class EditableListBoxRow(ListBoxRow):
    def __init__(self, listbox, delete=False, delete_callback=None, delete_callback_arguments=[],
                                activatable=False, vertical_padding=10):
        ListBoxRow.__init__(self)
        self.set_activatable(activatable)
        #self.add_events(EventMask.ENTER_NOTIFY_MASK)

        # Overlay
        self.overlay = Overlay()
        self.add(self.overlay)

        if delete:
            # Remove Icon
            self.remove_icon = Image.new_from_icon_name('window-close-symbolic', IconSize.BUTTON)

            # Remove Row EventBox
            remove_row_eventbox = EventBox()
            remove_row_eventbox.add(self.remove_icon)
            remove_row_eventbox.connect("button_press_event", self.on_delete_row, listbox, delete_callback, delete_callback_arguments)

            # Remove Row Revealer
            self.revealer = Revealer()
            self.revealer.set_transition_type (RevealerTransitionType.NONE)
            self.revealer.add(remove_row_eventbox)
            self.revealer.set_reveal_child(False)
            self.revealer.set_property("halign", Align.END)
            self.overlay.add_overlay(self.revealer)

    def add_widget(self, widget): #, same_size_widget):
        self.child = widget
        self.overlay.add(widget)

    def on_delete_row(self, widget, event, listbox, callback, callback_arguments):
        listbox.remove(self)
        if callback_arguments != []:
            callback(self, widget, event, *callback_arguments)
        else:
            callback(self, widget, event)

class Result(EditableListBoxRow):
    def __init__(self, listbox, result):
        EditableListBoxRow.__init__(self, listbox, activatable=True)
        self.content = result

        # Horizontal Box
        self.hbox = HBox()
        self.add_widget(self.hbox)

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

class ItemSearchBox(VBox):
    def __init__(self, parent, 
                       item_changed_callback=None, item_changed_callback_arguments=[],
                       type="var+search", vpadding=2, hpadding=4):
        VBox.__init__(self)
        self.type = type
        if type == "var":
            icon_name = "bookmark-new-symbolic"
            description = lang['new variable']
        if type == "var+search":
            icon_name = "system-search-symbolic"
            description = lang['item search']

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
        wp_args = {"icon_name":     icon_name,
                   "icon_size":     96,
                   "vpadding":      15,
                   "description":   description,
                   "parent":        None} 
        welcome_page = WelcomePage(**wp_args)

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
        new_variable_label = NameDescriptionLabel(lang['new variable unsensitive'],
                                                  lang['new variable unsensitive description'])
        new_variable = ExtendedModelButton(new_variable_label)
        new_variable.set_sensitive(False)
        results_revealer_box.pack_start(new_variable, False, False, vpadding)

        # Search results
        res_args = {"row_activated_callback": self.on_result_clicked,
                    "row_activated_callback_arguments": [{'parent':parent,
                                                          'item changed callback': item_changed_callback,
                                                          'item changed callback arguments': item_changed_callback_arguments}]}
        results = ItemResults(**res_args)
        results.set_visible(False)
        sc_args = {"results revealer": results_revealer,
                   "results": results,
                   "welcome revealer": welcome_revealer,
                   "new variable": new_variable,
                   "parent": parent,
                   "item changed callback": item_changed_callback,
                   "item changed callback arguments": item_changed_callback_arguments}
        self.search_entry.connect("search_changed", self.on_search_changed, sc_args)
        results_revealer_box.pack_start(results, True, True, vpadding)

    def on_new_variable(self, widget, event, k):
        # Extract data
        var = self.search_entry.get_text()
        data = {"Label":var, "Description":"Sparql variable"}

        # Eventually add data
        labels = set([v["Label"] for v in wikidata.vars])
        if not var in labels and var != "":
            wikidata.vars.append(data)

        # Set data
        k['parent'].set_data(data)
        k['parent'].popover.trigger()

        k['item changed callback'](*k['item changed callback arguments'])

        # Adjust button, search entry and addable status after selection
        k['parent'].set_css("variable")
        self.search_entry.set_text("")
        k['welcome revealer'].set_reveal_child(False)

    def on_result_clicked(self, item_results, listbox, row, k):
        k['parent'].set_data(row.content)
        k['parent'].popover.hide() 
        self.process_type(row.content, k['parent'])
        k['item changed callback'](*k['item changed callback arguments'])

    def process_type(self, dictionary, parent):
        if "URI" in dictionary.keys():
            if dictionary["URI"].startswith("Q"):
                parent.set_css("item")
            if dictionary["URI"].startswith("P"):
                parent.set_css("property")
            if dictionary["URI"] == "":
                parent.set_css("variable")
        else:
            parent.set_css("variable")

    def on_search_changed(self, widget, k):

        # Obtain query from search widget
        query = widget.get_text()

        if query != "":
            # Hide welcome and show search revealer
            k['welcome revealer'].set_reveal_child(False)
            k['results revealer'].set_reveal_child(True)

            # Check variable existence
            labels = set([v["Label"] for v in wikidata.vars])
            if query in labels:
                description = lang['select variable']
            else:
                description = lang['new variable']

            # Set new variable label
            k['new variable'].child = NameDescriptionLabel("<b>" + query + "</b>", description)
            k['new variable'].set_sensitive(True)
            k['new variable'].update_child()
            k['new variable'].connect("button_press_event", self.on_new_variable, k)

        if query == "":
            if wikidata.vars == []:
                # Hide revealer and show placeholder
                k['results revealer'].set_reveal_child(False)
                k['welcome revealer'].set_reveal_child(True)

            if wikidata.vars != []:
                # Show new variable not selectable and hide welcome revealer
                k['new variable'].child = NameDescriptionLabel(lang['new variable unsensitive'],
                                                               lang['new variable unsensitive description'])
                k['new variable'].set_sensitive(False)
                k['new variable'].update_child()
                k['new variable'].set_visible(True)
                k['welcome revealer'].set_reveal_child(False)

        if query != "" or wikidata.vars != []:
            # Destroy and re-create listbox
            k['results'].scrolled.remove(k['results'].listbox)
            k['results'].listbox = ListBox()
            StyleContext.add_class(k['results'].listbox.get_style_context(), "itemResultsListBox")
            k['results'].listbox.connect("row_activated", k['results'].on_row_activated, self.on_result_clicked, [k])
            k['results'].scrolled.add(k['results'].listbox)
         
            # Get data
            data = [v for v in wikidata.vars if query in v["Label"] and query != v["Label"]]
            if self.type != "var":
                data = data + wikidata.search(query)
         
            # Populate listbox
            for d in data:
                row = Result(k['results'].listbox, d)
                k['results'].listbox.add(row)
            k['results'].listbox.show_all()
            k['results'].set_visible(True)

class TripleBox(VBox):
    def __init__(self, item_changed_callback=None, css="unselected", first=lang['subject'], second=lang['property'], third=lang['object'], vertical_padding=8):
        VBox.__init__(self)

        # Data handling
        self.triple = {'s':{},'p':{},'o':{}}

        # Tuple Box
        hbox = HBox()
        self.pack_start(hbox, True, True, vertical_padding)

        # S/P/O
        self.subject = ButtonWithPopover(text=first, css=css, data=self.triple['s'])
        self.subject.set_popover_box(ItemSearchBox(self.subject, item_changed_callback=item_changed_callback))
        self.prop = ButtonWithPopover(text=second, css=css, data=self.triple['p'])
        self.prop.set_popover_box(ItemSearchBox(self.prop, item_changed_callback=item_changed_callback))
        self.obj = ButtonWithPopover(text=third, css=css, data=self.triple['o'])
        self.obj.set_popover_box(ItemSearchBox(self.obj, item_changed_callback=item_changed_callback))

        # Tuple
        first = VBox()
        second = VBox()
        third = VBox()
        first.pack_start(self.subject, True, False, 0)
        second.pack_start(self.prop, True, False, 0)
        third.pack_start(self.obj, True, False, 0)
        #first.add(self.subject)
        #second.add(self.prop)
        #third.add(self.obj)
        # Tuple Box
        tuple_box = HBox(homogeneous=True)
        tuple_box.pack_start(first, True, False, 0)
        tuple_box.pack_start(second, True, False, 0)
        tuple_box.pack_start(third, True, False, 0)
        hbox.pack_start(tuple_box, True, True, vertical_padding)

    def get_data(self):
        self.triple = {'s':self.subject.data, 'p':self.prop.data, 'o':self.obj.data}

