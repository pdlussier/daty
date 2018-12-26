# -*- coding: utf-8 -*-


from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import ListBoxRow, Template, Window
from gi.repository.Gdk import unicode_to_keyval
#from gi.repository.Handy import Column

from .triplet import Triplet

@Template.from_resource("/org/prevete/Daty/gtk/open.ui")
class Open(Window):
    __gtype_name__ = "Open"

    #properties = Template.Child("properties")
    content_stack = Template.Child("content_stack")
    header_bar_stack = Template.Child("header_bar_stack")
    search_stack = Template.Child("search_stack")
    constraint_listbox = Template.Child("constraint_listbox")
    constraint_search = Template.Child("constraint_search")

    def __init__(self, *args, new_session=True):
        Window.__init__(self, *args)

        if new_session:
            constraint = ListBoxRow()
            constraint.add(Triplet())
            self.constraint_listbox.add(constraint)
            self.constraint_listbox.show_all()

            self.header_bar_stack.set_visible_child_name("open_entities")
            self.content_stack.set_visible_child_name("placeholder") 

        self.show_all()
        #self.properties.add(Property())

    @Template.Callback()
    def placeholder_add_constraint_clicked_cb(self, widget):
        if self.content_stack.get_visible_child_name() == "placeholder":
            self.header_bar_stack.set_visible_child_name("header_search_type")
            self.content_stack.set_visible_child_name("search")
            self.search_stack.set_visible_child_name("constraints")

    @Template.Callback()
    def key_press_event_cb(self, widget, event):
        if not event.keyval == 65307:
            if self.content_stack.get_visible_child_name() == "placeholder":
                self.header_bar_stack.set_visible_child_name("header_search_type")
                self.content_stack.set_visible_child_name("search")
        else:
            self.header_bar_stack.set_visible_child_name("open_entities")
            self.content_stack.set_visible_child_name("placeholder")
            #self.print(event.group)
        #print(unicode_to_keyval(event.string)) 
