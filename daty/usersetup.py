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


from gi.repository.Gtk import Align, Assistant, Grid, IconTheme, Label, ListBoxRow, Separator, Template, main_quit
from locale import getdefaultlocale
from os import environ

name = 'ml.prevete.Daty'

@Template.from_resource("/ml/prevete/Daty/gtk/usersetup.ui")
class UserSetup(Assistant):
    __gtype_name__ = "UserSetup"

    credentials = Template.Child("credentials")
    username = Template.Child("username")
    username_label = Template.Child("username_label")
    bot_username = Template.Child("bot_username")
    bot_username_label = Template.Child("bot_username_label")
    bot_password = Template.Child("bot_password")
    bot_password_label = Template.Child("bot_password_label")
    username_label2 = Template.Child("username_label2")
    bot_username_label2 = Template.Child("bot_username_label2")

    def __init__(self, config, *args, **kwargs):
        Assistant.__init__(self)

        icon = lambda x: IconTheme.get_default().load_icon((name), x, 0)
        icons = [icon(size) for size in [32, 48, 64, 96]];
        self.set_icon_list(icons);

        self.config = config
        self.credentials.set_header_func(self.update_header)

        elements = [("user", self.username_label, self.username),
                    ("bot_user", self.bot_username_label, self.bot_username),
                    ("bot_password", self.bot_password_label, self.bot_password)]

        for key, label, entry in elements:
            row = ListBoxRow()
            grid = Grid()
            grid.props.column_homogeneous = True
            label.props.halign = Align(1)
            grid.attach(label, 0, 0, 1, 1)
            grid.attach(entry, 1, 0, 2, 1)
            row.add(grid)
            self.credentials.add(row)
        self.credentials.show_all()

        lc, encoding = getdefaultlocale()
        if (lc):
            language = lc.split("_")[0]
        else:
            language = environ.get("LANGUAGE", None)
            if language:
                language = language.split(":")[0]
        self.config.data['languages'] = [language]

        self.connect('destroy', main_quit)
        self.show_all()

    def update_header(self, row, before, *args):
        """See GTK+ Documentation"""
        if before:
            row.set_header(Separator())

    def do_cancel(self):
        self.destroy()

    def do_apply(self):
        self.config.create_pywikibot_config(self.username.props.text,
                                       self.bot_username.props.text,
                                       self.bot_password.props.text)

    def do_close(self):
        self.destroy()

    @Template.Callback()
    def credentials_help_clicked_cb(self, widget):
        if system() == 'Linux':
            show_uri (None, "help:daty/daty-credentials", CURRENT_TIME)
        if system() == 'Windows':
            from webbrowser import open
            open('http://daty.prevete.ml/daty-credentials.html')

    @Template.Callback()
    def on_field_changed(self, widget):
        if (  self.username.props.text and
              self.bot_username.props.text and
              self.bot_password.props.text ):

            self.username_label2.props.label = self.username.props.text
            self.bot_username_label2.props.label = self.bot_username.props.text
            page = self.get_nth_page(self.get_current_page())
            self.set_page_complete(page, True)

    @Template.Callback()
    def on_field_activate(self, widget):
        page = self.get_nth_page(self.get_current_page())
        if self.get_page_complete(page):
            self.do_apply()
            self.next_page()
