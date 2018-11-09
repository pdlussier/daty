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
            popover_box = VBox()
            label_test = Label()
            label_test.set_label("test")
            popover_box.add(label_test)
            #popover_box.add(ItemSearchBox(self, wikidata))

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

        # Overlay
        self.overlay = Overlay()

        # Remove Icon
        self.remove_icon = Image.new_from_icon_name('window-close-symbolic', IconSize.BUTTON)

        # Remove Row EventBox
        remove_row_eventbox = EventBox()
        remove_row_eventbox.add(self.remove_icon)
        remove_row_eventbox.connect("button_press_event", self.on_delete_row, listbox, delete_callback, *delete_callback_arguments)

        # Remove Row Revealer
        revealer = Revealer()
        revealer.set_transition_type (RevealerTransitionType.NONE)
        revealer.add(remove_row_eventbox)
        revealer.set_reveal_child(False)

        # Overlay Box
        overlay_box = HBox()
        overlay_box.pack_end(revealer, False, False, 4)
        self.overlay.add_overlay(overlay_box)

        # Event Box
        eventbox = EventBox()
        eventbox.add(self.overlay)
        eventbox.connect("enter_notify_event", self.enter, revealer)
        eventbox.connect("leave_notify_event", self.leave, revealer)
        self.add(eventbox)


    def add_widget(self, widget):
        self.overlay.add(widget)
        self.show_all()

    def on_delete_row(self, widget, event, listbox, callback, *callback_arguments):
        listbox.remove(self)
        callback(self, widget, event, *callback_arguments)

    def enter(self, widget, event, revealer):
        revealer.set_reveal_child(True)

    def leave(self, widget, event, revealer):
        revealer.set_reveal_child(False)

class TripleBox(VBox):
    def __init__(self, wikidata, vertical_padding=8):
        VBox.__init__(self)

        # Tuple Box
        hbox = HBox()
        self.pack_start(hbox, True, True, vertical_padding)

        # S/P/O 
        subject = ButtonWithPopover(text="Soggetto", css="unselected")
        prop = ButtonWithPopover(text="Proprietà", css="unselected")
        obj = ButtonWithPopover(text="Oggetto", css="unselected")

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

