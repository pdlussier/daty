# -*- coding: iso-8859-15 -*-

#    util.py
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

from ast import literal_eval
#from gi.repository.Gdk import Screen
#from gi.repository.Gtk import CssProvider, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION
from os.path import dirname, realpath
from pickle import dump
from pickle import load as pickle_load

def save(variable, path):
    """Save variable on given path using Pickle

    Args:
        variable: what to save
        path (str): path of the output
    """
    with open(path, 'wb') as f:
        dump(variable, f)
    f.close()

def load(path):
    """Load variable from Pickle file

    Args:
        path (str): path of the file to load

    Returns:
        variable read from path
    """
    with open(path, 'rb') as f:
        variable = pickle_load(f)
    f.close()
    return variable

def import_translations(lang):
    with open('po/'+lang+'.po', 'r') as g:
        content = literal_eval(g.read())
        g.close()
    return content

# def gtk_style():
#     path = dirname(realpath(__file__))
#     with open(path + '/style.css', 'rb') as f:
#         css = f.read()
#         f.close()
#     style_provider = CssProvider()
#     style_provider.load_from_data(css)
#     StyleContext.add_provider_for_screen(Screen.get_default(),
#                                          style_provider,
#                                          STYLE_PROVIDER_PRIORITY_APPLICATION)
