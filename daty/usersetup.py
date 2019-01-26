# -*- coding: utf-8 -*-

#    UserSetup
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


from gi.repository.Gtk import Assistant, Template, main_quit

@Template.from_resource("/ml/prevete/Daty/gtk/usersetup.ui")
class UserSetup(Assistant):
    __gtype_name__ = "UserSetup"

    username = Template.Child("username")
    bot_username = Template.Child("bot_username")
    bot_password = Template.Child("bot_password")
    username_label = Template.Child("username_label2")
    bot_username_label = Template.Child("bot_username_label2")

    def __init__(self, config, *args, **kwargs):
        Assistant.__init__(self)
        self.config = config
        self.connect('destroy', main_quit)
        self.show_all()

    def do_cancel(self):
        self.destroy()

    def do_apply(self):
        self.config.create_pywikibot_config(self.username.props.text,
                                       self.bot_username.props.text,
                                       self.bot_password.props.text)

    def do_close(self):
        self.destroy()

    @Template.Callback()
    def on_field_changed(self, widget):
        if (  self.username.props.text and
              self.bot_username.props.text and
              self.bot_password.props.text ):

            self.username_label.props.label = self.username.props.text
            self.bot_username_label.props.label = self.bot_username.props.text
            page = self.get_nth_page(self.get_current_page())
            self.set_page_complete(page, True)

    @Template.Callback()
    def on_field_activate(self, widget):
        page = self.get_nth_page(self.get_current_page())
        if self.get_page_complete(page):
            self.do_apply()
            self.next_page()
