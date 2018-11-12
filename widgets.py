from gi.repository.Gtk import main, main_quit, Align, Box, Button, CheckButton, CssProvider, Entry, EventBox, HBox, IconSize, Image, HeaderBar, Label, ListBox, ListBoxRow, ModelButton, Orientation, Overlay, PolicyType, PopoverMenu, Revealer, RevealerTransitionType, ScrolledWindow, SearchBar, SearchEntry, SelectionMode, Stack, StackSwitcher, StackTransitionType, StyleContext, TextView, VBox, Window, WindowPosition, WrapMode, STYLE_CLASS_DESTRUCTIVE_ACTION, STYLE_CLASS_SUGGESTED_ACTION, STYLE_PROVIDER_PRIORITY_APPLICATION


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
            button_box = Box(orientation=Orientation(0))
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

