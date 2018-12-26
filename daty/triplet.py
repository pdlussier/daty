# -*- coding: utf-8 -*-


from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.Gtk import Grid, Template

@Template.from_resource("/org/prevete/Daty/gtk/triplet.ui")
class Triplet(Grid):
    __gtype_name__ = "Triplet"

    #properties = Template.Child("properties")

    def __init__(self, *args, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        self.show_all()
        #self.properties.add(Property())

#    @Template.Callback()
    #def key_press_event_cb(self, widget, event):
    #    if event.keyval == 65307:
    #        self.header_bar_stack.set_visible_child_name("open_entities")
    #        self.content_stack.set_visible_child_name("placeholder")
    #        #self.print(event.group)
    #    else:
    #        if self.content_stack.get_visible_child_name() == "placeholder":
    #            self.header_bar_stack.set_visible_child_name("header_search_type")
    #            self.content_stack.set_visible_child_name("search")
    #    #print(unicode_to_keyval(event.string)) 
