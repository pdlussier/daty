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
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.Gtk import main as gtk_main
from setproctitle import setproctitle
from sys import argv

name = "daty"
version = "1.0alpha"
setproctitle(name)

def main():
    """Daty entry point"""
    # Argument parser
    parser = ArgumentParser(description="Daty: the Wikidata editor")
    parser.add_argument('entities',
                        nargs='*',
                        action='store',
                        default=[],
                        help='entities to open')
    parser.add_argument('--language',
                        dest='language',
                        nargs=1,
                        action='store',
                        default=['en'],
                        help="start daty in a given language (stub)")
    parser.add_argument('--verbose', 
                        dest='verbose', 
                        action='store_true', 
                        default=False, 
                        help='extended output')

    args = parser.parse_args()

    if args.verbose:
        print(args)
        # Namespace(entities=['Q1', 'Q2'], language=['en'])
    
    # Set config
    config = Config()

    # Set gettext
    _ = config.lang.gettext

    # User setup
    if not config.data:
        from .usersetup import UserSetup
        UserSetup(config)
        gtk_main()

    # Editor
    if config.data:
            app = Daty(entities=[{"URI":entity,
                                  "Label":"", 
                                  "Description":""} for entity in args.entities])
            app.run()
