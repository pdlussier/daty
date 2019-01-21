# -*- coding: utf-8 -*-

#    LoadingPage
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

from gi import require_version
require_version('Gtk', '3.0')
require_version('Handy', '0.0')
from gi.repository.Gtk import Image, Template
from .wikidata import Wikidata

@Template.from_resource("/ml/prevete/Daty/gtk/loadingpage.ui")
class LoadingPage(Image):
    __gtype_name__ = "LoadingPage"

    def __init__(self, *args, label="", **kwargs):
        Image.__init__(self, *args, **kwargs)
