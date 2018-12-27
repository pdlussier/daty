#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#    Daty
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from .application import Daty
from .config import Config

from argparse import ArgumentParser
from gi import require_version
from gi.repository.GObject import type_ensure
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.Gtk import main as gtk_main
from setproctitle import setproctitle
from sys import argv

name = "daty"
version = "0.0.1"
setproctitle(name)

def main():
    # Argument parser
    parser = ArgumentParser(description="Daty: the Wikidata editor")
    parser.add_argument('--verbose', dest='verbose', action='store_true', default=False, help='extended output')
    parser.add_argument('--editor', dest='editor', action='store_true', default=False, help="skip the welcome window")
    #parser.add_argument('--language', dest='language', nargs=1, action='store', default=['it'], help="start daty in language different from system's")
    args = parser.parse_args()

    #Namespace(editor=False, language=['it'], verbose=False)

    # Start
    config = Config()
    _ = config.lang.gettext
    if not config.data:
        from .usersetup import UserSetup
        UserSetup(config)
        gtk_main()
    if config.data:
        if args.editor:
        #type_ensure(TitleBar)
            app = Daty()
            app.run()#argv)
        else:
            from .open import Open
            open_entities = Open()
            gtk_main()
