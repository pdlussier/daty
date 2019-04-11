# -*- coding: utf-8 -*-

#    Editor
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from copy import deepcopy as cp
from gi import require_version
require_version('Gdk', '3.0')
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.GObject import SignalFlags as sf
from gi.repository.GObject import TYPE_NONE, TYPE_STRING, TYPE_PYOBJECT
from gi.repository.GLib import idle_add, PRIORITY_LOW
from gi.repository.Gdk import KEY_Escape, KEY_Control_L, KEY_Control_R, KEY_Alt_R, KEY_Alt_L, KEY_ISO_Level3_Shift, KEY_ISO_Level3_Lock, KEY_Tab, KEY_Menu, KEY_Up, KEY_Down, KEY_Right, KEY_Left
from gi.repository.Gdk import Event, EventFocus, EventType
from gi.repository.Gtk import AccelGroup, ApplicationWindow, IconTheme, IMContext, Label, ListBoxRow, Template, Separator, SearchEntry
from gi.repository.Handy import Column
from pprint import pprint
from threading import Thread
from webbrowser import open

from .entityselectable import EntitySelectable
from .loadingpage import LoadingPage
from .open import Open
from .page import Page
from .overlayedlistboxrow import OverlayedListBoxRow
from .roundedbutton import RoundedButton
from .sidebarentity import SidebarEntity
from .sidebarlist import SidebarList
from .util import MyThread, add_accelerator, download, edit, label_color, set_style
from .wikidata import Wikidata

name = "ml.prevete.Daty"

modifiers = [KEY_Control_L, KEY_Control_R, KEY_Alt_R, KEY_Alt_L,
             KEY_ISO_Level3_Shift, KEY_ISO_Level3_Lock, KEY_Tab, KEY_Menu,
             KEY_Up, KEY_Down, KEY_Right, KEY_Left]

@Template.from_resource("/ml/prevete/Daty/gtk/editor.ui")
class Editor(ApplicationWindow):

    __gtype_name__ = "Editor"

    __gsignals__ = {'entity-close':(sf.RUN_LAST,
                                    TYPE_NONE,
                                    (TYPE_PYOBJECT,))}

    # Title bar
    titlebar = Template.Child("titlebar")
    header_box = Template.Child("header_box")

    # Header bar
    header_bar = Template.Child("header_bar")
    entity_close = Template.Child("entity_close")
    entity_discussion_open_external = Template.Child("entity_discussion_open_external")
    entity_history_open_external = Template.Child("entity_history_open_external")
    entity_open = Template.Child("entity_open")
    entity_menu_popover = Template.Child("entity_menu_popover")
    entities_search = Template.Child("entities_search")
    entities_select = Template.Child("entities_select")
    entity_open_external = Template.Child("entity_open_external")
    cancel_entities_selection = Template.Child("cancel_entities_selection")
    app_menu = Template.Child("app_menu")
    app_menu_popover = Template.Child("app_menu_popover")
    help = Template.Child("help")

    # Sub header bar
    sub_header_bar = Template.Child("sub_header_bar")
    entity_back = Template.Child("entity_back")
    entity_stack = Template.Child("entity_stack")
    entity_button = Template.Child("entity_button")
    entity = Template.Child("entity")
    description = Template.Child("description")
    entity_search = Template.Child("entity_search")

    # Sidebar
    sidebar = Template.Child("sidebar")
    sidebar_search_bar = Template.Child("sidebar_search_bar")
    sidebar_search_entry = Template.Child("sidebar_search_entry")
    sidebar_viewport = Template.Child("sidebar_viewport")

    # Content
    content_box = Template.Child("content_box")
    content_stack = Template.Child("content_stack")
    single_column = Template.Child("single_column")

    # Specific
    entity_search_bar = Template.Child("entity_search_bar")
    entity_search_entry = Template.Child("entity_search_entry")
    pages = Template.Child("pages")

    start_pane_size_group = Template.Child("start_pane_size_group")

    # Separator
#    edit_column_separator = Template.Child("edit_column_separator")

    # Common
    #common = Template.Child("common-viewport")
    #common_page = Template.Child("common_page")

    wikidata = Wikidata()

    def __init__(self, *args, entities=[], quit_cb=None, max_pages=10, **kwargs):
        """Editor class

            Args:
                entities (list): of dict having keys"Label", "URI", "Description";
                max_pages (int): maximum number of pages kept in RAM
        """
        ApplicationWindow.__init__(self, *args, **kwargs)

        self.quit_cb = quit_cb

        # Set window icon
        icon = lambda x: IconTheme.get_default().load_icon((name), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        # Set shortcuts
        accelerators = AccelGroup()
        self.add_accel_group(accelerators)
        add_accelerator(accelerators, self.entity_open, "<Control>o", signal="clicked")
        add_accelerator(accelerators, self.entity_search, "<Control>f", signal="clicked")
        add_accelerator(accelerators, self.entity_discussion_open_external, "<Control>d", signal="clicked")
        add_accelerator(accelerators, self.entity_history_open_external, "<Control>h", signal="clicked")
        add_accelerator(accelerators, self.entities_select, "<Control>s", signal="clicked")
        add_accelerator(accelerators, self.cancel_entities_selection, "<Control><Shift>s", signal="clicked")
        add_accelerator(accelerators, self.entities_search, "<Control><Shift>f", signal="activate")

        # Init sidebar
        self.sidebar_list = SidebarList()
        self.sidebar_list.connect("entity-selected", self.sidebar_row_selected_cb)
        self.sidebar_viewport.add(self.sidebar_list)

        # Init pages
        loading = LoadingPage()
        self.pages.add_titled(loading, "loading", "Loading")

        #self.entity_search_entry.grab_focus()

        # Parse args
        self.max_pages = max_pages
        if entities:
            self.load(entities)
        else:
            entities_open_dialog = Open(quit_cb=self.quit_cb,
                                        new_session=True)
            entities_open_dialog.connect("new-window-clicked", self.new_window_clicked_cb)
            entities_open_dialog.get_focus()
            #entities_open_dialog.show_all()

    def filter(self, query, text):
        return query.lower() in text.lower()

    def sidebar_search_entry_search_changed_cb(self, entry):
        text = entry.get_text()
        for row in self.sidebar_list.get_children():
            if row.get_children():
                child = row.child
                entity = child.entity
                if text.lower() in entity["Label"].lower() or text.lower() in entity["Description"].lower():
                    row.set_visible(True)
                    label_color(child.label, text)
                    label_color(child.description, text)
                else:
                    row.set_visible(False)

    def sidebar_row_selected_cb(self, sidebar_list, entity):
        print("Editor: sidebar row selected")
        self.single_column.set_visible_child_name("content_stack")
        self.header_box.set_visible_child_name("sub_header_bar")

        # Set titlebar
        def set_text(widget, label):
            widget.set_text(label)
            widget.set_tooltip_text(label)

        set_text(self.entity, entity["Label"])
        set_text(self.description, entity["Description"])

        if hasattr(self, 'entity_open_external_connection'):
            self.entity_open_external.disconnect(self.entity_open_external_connection)
        self.entity_open_external_connection = self.entity_open_external.connect("clicked",
                                                                                 self.entity_open_external_clicked_cb,
                                                                                 entity['URI'])
        if hasattr(self, 'entity_history_open_external_connection'):
            self.entity_history_open_external.disconnect(self.entity_history_open_external_connection)
        self.entity_history_open_external_connection = self.entity_history_open_external.connect("clicked",
                                                                                                 self.entity_history_open_external_clicked_cb,
                                                                                                 entity['URI'])
        if hasattr(self, 'entity_discussion_open_external_connection'):
            self.entity_discussion_open_external.disconnect(self.entity_discussion_open_external_connection)
        self.entity_discussion_open_external_connection = self.entity_discussion_open_external.connect("clicked",
                                                                                                       self.entity_discussion_open_external_clicked_cb,
                                                                                                       entity['URI'])
        # Get selected sidebar entity for popover close button
        current_row = self.sidebar_list.get_selected_row()
        sidebar_entity = current_row.child

        #if hasattr(self, 'entity_close_connection'):
        #    self.entity_close.disconnect(self.entity_close_connection)
        #self.entity_close_connection = self.entity_close.connect("clicked",
        #                                                         self.entity_close_clicked_cb,
        #                                                         sidebar_entity)

        if not self.pages.get_child_by_name(entity['URI']):
            self.pages.set_visible_child_name("loading")
            children = self.pages.get_children()

            if len(children) >= 10:
                oldest = children[1]
                children.remove(oldest)
                oldest.destroy()
                del oldest

            # TODO: Implement a short timeout to make sure you explicitly wanted to load the row

            self.load_page_async(entity)
        else:
            self.pages.set_visible_child_name(entity['URI'])
            self.entity_search_entry.connect('search-changed',
                                             self.entity_search_entry_search_changed_cb)
            self.sidebar_search_entry.connect('search-changed',
                                             self.sidebar_search_entry_search_changed_cb)

    def load_page_async(self, entity):
        def do_call():
            idle_add(lambda: self.on_page_complete(entity))
        thread = MyThread(target = do_call)
        thread.start()

    def on_page_complete(self, entity):
        page = Page(entity['Data'])
        page.connect("claim-changed", self.claim_changed_cb)
        page.connect("entity-editing", self.entity_editing_cb)
        self.entity_leaving_connection = page.connect("entity-leaving", self.entity_leaving_cb)
        #self.connect("claim-changed-done", page.claim_changed_done_cb)
        page.connect("new-window-clicked", self.new_window_clicked_cb)
        page.connect("reference-new-clicked", self.reference_new_clicked_cb)
        self.pages.add_titled(page, entity['URI'], entity['Label'])
        self.pages.set_visible_child_name(entity['URI'])
        self.entity_search_entry.connect("search-changed",
                                         self.entity_search_entry_search_changed_cb)
        self.sidebar_search_entry.connect("search-changed",
                                          self.sidebar_search_entry_search_changed_cb)
        return None

    def reference_new_clicked_cb(self, page, value, entity):
        print("Editor: 'reference-new' received")
        print("Editor: Value 'reference-new' emission disabled")
        value.disconnect(value.button_press_connection)
        if hasattr(self, 'reference_new_connection'):
            print("Editor: 'reference-new' signals already attached; resetting")
            page.disconnect(self.reference_new_connection)
            self.current_value.qualifier_new.disconnect(self.from_value_qualifier_new_enter_connection)
            self.current_value.qualifier_new.disconnect(self.from_value_qualifier_new_leave_connection)
            self.current_value.button_press_connection = self.current_value.connect("button-press-event",
                                                                                    self.current_value.clicked_cb)
            self.current_value.actions.set_visible(False)
            self.current_value.button.set_visible(True)
            del self.reference_new_connection
            print("reconnecting signals")
        if not hasattr(self, 'reference_new_connection'):
            self.current_value = value
            self.reference_new_connection = page.connect("button-release-event",
                                                         self.reference_new_button_press_event_elsewhere,
                                                         value)
            print("Editor: Page 'button-press-event' connected to 'elsewhere' cb with value", self.reference_new_connection)

            self.from_value_qualifier_new_enter_connection = value.qualifier_new.connect("enter-notify-event",
                                                                                         self.from_value_qualifier_new_enter_notify_event_cb,
                                                                                         page,
                                                                                         value)
            self.from_value_qualifier_new_leave_connection = value.qualifier_new.connect("leave-notify-event",
                                                                                         self.from_value_qualifier_new_leave_notify_event_cb,
                                                                                         page,
                                                                                         value)


    def from_value_qualifier_new_enter_notify_event_cb(self, qualifier_new, event, page, value):
        print("Editor: entering new qualifier entry")
        print("disconnect elsewhere signal", self.reference_new_connection)
        #print(entity.entry_focus_out_connection)
        #value.hide_actions = False
        #try:
        page.disconnect(self.reference_new_connection)

        #except Exception as e:
        #    pass


    def from_value_qualifier_new_leave_notify_event_cb(self, actions, event, page, value):
        print("Editor: leaving new qualifier entry")
        self.reference_new_connection = page.connect("button-press-event",
                                                     self.reference_new_button_press_event_elsewhere,
                                                     value)
        print("reconnecting page to 'reference new button press elsewhere'", self.reference_new_connection)
        #else:
        #    self.entity_popover_connection = page.connect("button-press-event",
        #                                                  self.button_press_event_cb,
        #                                                  entity)

        #entity.entry_focus_out_connection = entity.entry.connect("focus-out-event",
        #                                                     entity.entry_focus_out_event_cb)
        #value.hide_actions = True


    def reference_new_button_press_event_elsewhere(self, page, event, value):
        visible = value.actions.get_visible()
        if not visible:
            print("Elsewhere cb: show actions")
            value.actions.set_visible(True)
            value.button.set_visible(False)
        else:
            print("Elsewhere cb: hide actions, disconnect 'elsewhere' signals",
                  self.reference_new_connection)
            print("Elsewhere cb: disconnect NQ enter connection", self.from_value_qualifier_new_enter_connection)
            print("Elsewhere cb: disconnect NQ leave connection", self.from_value_qualifier_new_leave_connection)
            page.disconnect(self.reference_new_connection)
            value.qualifier_new.disconnect(self.from_value_qualifier_new_enter_connection)
            value.qualifier_new.disconnect(self.from_value_qualifier_new_leave_connection)
            del self.reference_new_connection #= False
            del self.from_value_qualifier_new_enter_connection #= False
            del self.from_value_qualifier_new_leave_connection #= False
            print("Elsewhere cb: Value 'reference-new' emission enabled")
            value.button_press_connection = value.connect("button-press-event",
                                                          value.clicked_cb)
            value.actions.set_visible(False)
            value.button.set_visible(True)
        #self.reference_new_connection = True

    def entity_leaving_cb(self, page, value, entity):
        print("Editor: entity leaving")
        #if value.hide_actions:
        value.actions.set_visible(False)
        if not hasattr(value, 'references'):
            value.button.set_visible(True)
        return True

    def entity_editing_cb(self, page, value, entity, popover):
        print("Editor: entity editing")
        if hasattr(self, 'reference_new_connection'):
            print("Editor: 'reference-new' signals already attached; resetting")
            page.disconnect(self.reference_new_connection)
            self.current_value.qualifier_new.disconnect(self.from_value_qualifier_new_enter_connection)
            self.current_value.qualifier_new.disconnect(self.from_value_qualifier_new_leave_connection)
            self.current_value.button_press_connection = self.current_value.connect("button-press-event",
                                                                                    self.current_value.clicked_cb)
            self.current_value.actions.set_visible(False)
            self.current_value.button.set_visible(True)
            del self.reference_new_connection
        value.actions.set_visible(True)
        if not hasattr(value, 'references'):
            value.button.set_visible(False)
        self.entity_popover_connection = page.connect("button-press-event",
                                                      self.button_press_event_cb,
                                                      value,
                                                      entity)
        self.qualifier_new_enter_connection = value.qualifier_new.connect("enter-notify-event",
                                                                          self.qualifier_new_enter_notify_event_cb,
                                                                          page,
                                                                          value)
        self.qualifier_new_leave_connection = value.qualifier_new.connect("leave-notify-event",
                                                                          self.qualifier_new_leave_notify_event_cb,
                                                                          page,
                                                                          value,
                                                                          entity)

    def qualifier_new_enter_notify_event_cb(self, qualifier_new, event, page, value):
        print("Editor: entering new qualifier entry")
        #value.hide_actions = False
        page.disconnect(self.entity_popover_connection)
        page.disconnect(self.entity_leaving_connection)

    def qualifier_new_leave_notify_event_cb(self, actions, event, page, value, entity):
        print("Editor: leaving new qualifier entry")
        self.entity_popover_connection = page.connect("button-press-event",
                                                      self.button_press_event_cb,
                                                      entity)
        self.entity_leaving_connection = page.connect("entity-leaving",
                                                      self.entity_leaving_cb)
        #entity.entry_focus_out_connection = entity.entry.connect("focus-out-event",
        #                                                     entity.entry_focus_out_event_cb)
        #value.hide_actions = True

    def button_press_event_cb(self, page, event, value, entity):
        print("Disconnecting all signals")
        page.disconnect(self.entity_popover_connection)
        value.qualifier_new.disconnect(self.qualifier_new_enter_connection)
        value.qualifier_new.disconnect(self.qualifier_new_leave_connection)

        print("Editor: Entity entry emitting 'focus-out-event'")
        event = Event(EventType(12))
        event.window = page.get_window()  # the gtk.gdk.Window of the widget
        event.send_event = True  # this means you sent the event explicitly
        event.in_ = False
        entity.entry.emit("focus-out-event", event)
        #try:
        #    page.disconnect(self.entity_popover_connection)
        #except Exception as e:
        #    print(e)

    def claim_changed_cb(self, page, claim, target, value):
        print("Editor: claim changed")
        URI = self.pages.get_visible_child_name()
        edit(URI, claim, target, self.on_claim_changed, value)

    def on_claim_changed(self, target, error, value):
        if not error:
            set_style(value.context, '/ml/prevete/Daty/gtk/value.css',
                                     'loading', False)
            print("Modifica effettuata correttamente")
        else:
            print("Error", error)


    def entity_search_entry_search_changed_cb(self, entry):
        text = entry.get_text()
        page = self.pages.get_visible_child()
        statements = page.statements
        i = 0
        row = lambda i,j: statements.get_child_at(j,i)
        while row(i,0):
            p_label = row(i,0).property_label.get_text()
            p_desc = row(i,0).property_label.get_tooltip_text()
            p_found = self.filter(text, p_label) or self.filter(text, p_desc)
            if p_found:
                label_color(row(i,0).property_label, text)
                row(i,0).set_visible(True)
                row(i,1).set_visible(True)
            else:
                label_color(row(i,0).property_label, color='')
                row(i,0).set_visible(False)
                row(i,1).set_visible(False)
            i = i + 1

    def load(self, entities):
        """Open entities

            Args:
                entities (list): of dict having "URI", "Label", "Description" keys;
        """
        for entity in entities[:-1]:
            download(entity, self.load_row_async, use_cache=False)
        download(entities[-1], self.load_row_async, select=True)
        self.show()
        self.present()

    def load_row_async(self, entity, **kwargs):
        """It creates sidebar passing downloaded data to its rows.

            Gets executed when download method has finished its task

            Args:
                entity (dict): have keys "URI", "Label", "Description", "Data"
        """
        f = lambda : entity
        def do_call():
            entity = f()
            idle_add(lambda: self.on_row_complete(entity, **kwargs))
        thread = MyThread(target = do_call)
        thread.start()

    def on_row_complete(self, entity, **kwargs):

        # Build entity
        if not entity['Label']:
            entity['Label'] = self.wikidata.get_label(entity['Data'])
        if not entity['Description']:
            entity['Description'] = self.wikidata.get_description(entity['Data'])

        sidebar_entity = SidebarEntity(entity, description=True, URI=True)
        sidebar_entity.button.connect("clicked", self.entity_close_clicked_cb,
                                      sidebar_entity)

        row = ListBoxRow()
        row.child = sidebar_entity

        row.add(sidebar_entity)

        current_row = self.sidebar_list.get_selected_row()
        rows = self.sidebar_list.get_children()
        i = 0
        for i, r in enumerate(rows):
            if r == current_row:
                break
        if (i < len(rows) - 2):
            self.sidebar_list.insert(row, i+1)
        else:
            self.sidebar_list.add(row)
        self.sidebar_list.show_all()
        if 'select' in kwargs and kwargs['select']:
            self.sidebar_list.select_row(row)

    @Template.Callback()
    def entity_open_clicked_cb(self, widget):
        """New entity button clicked callback

            If clicked, it opens the 'open new entities' window.

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        open_dialog = Open(quit_cb=self.quit_cb, new_session=False)
        open_dialog.connect("entity-new", self.entity_new_clicked_cb)
        open_dialog.connect("new-window-clicked", self.new_window_clicked_cb)

    def new_window_clicked_cb(self, dialog, entities):
        self.load(entities)
        print("Editor: new window clicked")

    def entity_new_clicked_cb(self, open, query):
        print("New entity", query)

    def entity_history_open_external_clicked_cb(self, widget, URI):
       open(''.join(['https://wikidata.org/w/index.php?action=history&title=', URI]))

    def entity_discussion_open_external_clicked_cb(self, widget, URI):
        open(''.join(['https://www.wikidata.org/wiki/Talk:', URI]))

    def entity_open_external_clicked_cb(self, widget, URI):
        open('/'.join(['https://wikidata.org/wiki', URI]))

    @Template.Callback()
    def entities_search_toggled_cb(self, widget):
        if widget.get_active():
            self.sidebar_search_bar.set_search_mode(True)
        else:
            self.sidebar_search_bar.set_search_mode(False)

    @Template.Callback()
    def entities_select_clicked_cb(self, widget):
        """Select sidebar entities button clicked callback

            If clicked, activates header bar selection mode.

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        self.set_selection_mode(True)

    @Template.Callback()
    def cancel_entities_selection_clicked_cb(self, widget):
        """Cancel sidebar entities selection button clicked callback

            If clicked, disables header bar selection mode.

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        self.set_selection_mode(False)

    def set_selection_mode(self, value):
        """Toggle selection mode

            Args:
                value (bool): if True, activates selection mode.
        """
        # Titlebar
        self.titlebar.set_selection_mode(value)
        # New entity button
        self.entity_open.set_visible(not value)
        # Entities search button
        self.entities_search.set_visible(value)
        # App menu
        self.app_menu.set_visible(not value)
        # Select button
        self.entities_select.set_visible(not value)
        # Cancel selection button
        self.cancel_entities_selection.set_visible(value)
        # Sidebar
        self.sidebar_list.set_selection_mode(value)
        if value:
            self.column_separator = Separator()
            self.common = Label(label="common")
            self.content_box.add(self.column_separator)
            self.content_box.add(self.common)
            self.content_box.show_all()
        else:
            self.content_box.remove(self.column_separator)
            self.content_box.remove(self.common)

    @Template.Callback()
    def app_menu_clicked_cb(self, widget):
        """Primary menu button clicked callback

            If clicked, open primary menu (app menu).

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        if self.app_menu_popover.get_visible():
            self.app_menu_popover.hide()
        else:
            self.app_menu_popover.set_visible(True)

    @Template.Callback()
    def entity_menu_clicked_cb(self, widget):
        """Primary menu button clicked callback

            If clicked, open primary menu (app menu).

            Args:
                widget (Gtk.Widget): the clicked widget.
        """
        if self.entity_menu_popover.get_visible():
            self.entity_menu_popover.hide()
        else:
            self.entity_menu_popover.set_visible(True)

    @Template.Callback()
    def on_content_box_folded_changed(self, leaflet, folded):
        """Third column folding signal

            If in selection/multi-editing mode, set stack switcher
            depending on window size

            Args:
                leaflet (Handy.Leaflet): the leaflet emitting the signal;
                folded (GParamBoolean): whether it is folded or not.
        """
        # If we are in selection mode
        if self.titlebar.get_selection_mode():
            # If the title is displayed
            if self.content_box.props.folded:
                # Set switcher in the titlebar
                self.entity_stack.set_visible_child_name("column_switcher")

                # Move common page from third column to content_stack
                self.content_box.remove(self.column_separator)
                self.content_box.remove(self.common)
                self.content_stack.add_titled(self.common, "common", "Common")

            else:
                # Set the switcher to something else
                self.entity_stack.set_visible_child_name("entity_button")

                # Move common page from content stack to third column
                self.content_stack.remove(self.common)
                self.content_box.add(self.column_separator)
                self.content_box.add(self.common)

    @Template.Callback()
    def on_single_column_folded_changed(self, leaflet, folded):
        if self.single_column.props.folded:
            self.entity_back.set_visible(True)
        else:
            self.entity_back.set_visible(False)

    @Template.Callback()
    def entity_back_clicked_cb(self, widget):
        self.header_box.set_visible_child(self.header_bar)
        self.single_column.set_visible_child(self.sidebar)

    @Template.Callback()
    def entity_search_toggled_cb(self, widget):
        if widget.get_active():
            self.entity_search_bar.set_search_mode(True)
        else:
            self.entity_search_bar.set_search_mode(False)

    #@Template.Callback()
    def key_press_event_cb(self, window, event):
        """Manages editor's key press events

        Args:
            window (Gtk.Window): it is self;
            event (Gdk.Event): the key press event.
        """
        if event.keyval in modifiers:
            return None
        focused = window.get_focus()

        # Sidebar
        sidebar_leaflet_focused = self.single_column.get_visible_child_name() == 'sidebar'
        if hasattr(focused, 'child'):
            if type(focused.child) == SidebarEntity:
                sidebar_entity_focused = True
        else:
            sidebar_entity_focused = False
        sidebar_focused = sidebar_leaflet_focused or sidebar_entity_focused

        # Search Entries
        search_entry_focused = type(focused) == SearchEntry
        sidebar_search_entry_focused = focused == self.sidebar_search_entry
        entity_search_entry_focused = type(focused) == self.entity_search_entry

        if sidebar_focused:
            if not self.sidebar_search_bar.get_search_mode():
                self.entities_search.set_active(True)
                self.sidebar_search_bar.set_search_mode(True)
            else:
                self.sidebar_search_entry.grab_focus()
        elif search_entry_focused:
            if entity_search_entry_focused:
                if not self.entity_search_bar.get_search_mode():
                    self.entity_search.set_active(True)
                    self.entity_search_bar.set_search_mode(True)
        else:
            if event.keyval == KEY_Escape:
                 if self.titlebar.get_selection_mode():
                     self.set_selection_mode(False)
            else:
                if not self.entity_search_bar.get_search_mode():
                    self.entity_search.set_active(True)
                    self.entity_search_bar.set_search_mode(True)
                    #self.entity_search_entry.set_text(event.string)

    @Template.Callback()
    def entity_search_entry_stop_search_cb(self, widget):
        if self.entity_search.get_active():
            self.entity_search.set_active(False)
            self.entity_search_bar.set_search_mode(False)

    def entity_close_clicked_cb(self, widget, sidebar_entity):
        row = sidebar_entity.get_parent()
        print(row)
        URI = sidebar_entity.entity["URI"]
        self.sidebar_list.last = list(filter(lambda x: x != row,
                                             self.sidebar_list.last))
        row.destroy()
        try:
            page = self.pages.get_child_by_name(URI)
            page.destroy()
        except Exception as e:
            print ("page not loaded")

    def get_neighbor(self, i, next=True):
        f = lambda x: x + 1 if next else x - 1
        while True:
            try:
                print(self.sidebar_list.get_children())
                self.sidebar_list.get_row_at_index(i)
                return True
            except AttributeError as e:
                i = f(i)
