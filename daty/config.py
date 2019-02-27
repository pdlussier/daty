# -*- coding: utf-8 -*-

#    Config
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


try:
    from .util import chmod_recursively, load, mkdirs, save
except:
    from util import load, mkdirs, save

from appdirs import *
from gettext import bindtextdomain, textdomain, translation
from gi.repository.Gio import Resource, ResourceLookupFlags, resource_load
from locale import getdefaultlocale
from os import chmod, environ, mkdir, sep
from os.path import abspath, dirname, exists, join
from re import sub
from shutil import rmtree as rm

class Config:
    """Daty configuration class.

    Attributes:
        exec_path (str): path where the class resides;
        appname (str): name of the app (daty).
        dirs (dict): paths of cache, data, config directories
    """

    exec_path = dirname(abspath(__file__))

    appname = "daty"
    appauthor = "Pellegrino Prevete"
    dirs = {'data':user_data_dir(appname, appauthor),
            'config':user_config_dir(appname, appauthor),
            'cache':user_cache_dir(appname, appauthor)}

    def __init__(self):
        self.set_dirs()
        self.set_locales()
        self.set_resources()
        self.tette = 3
        if not exists(join(self.dirs['config'], "config.pkl")):
            self.data = {}
        else:
            self.data = load(str(join(self.dirs['config'], "config.pkl")))

    def set_dirs(self):
        """Make user dirs for daty

            It makes pywikibot dir in config and export
            PYWIKIBOT_DIR.

        """
        for dir_type, path in self.dirs.items():
            mkdirs(path)
            if dir_type == 'config': #and not exists(join(path, 'pywikibot')):
                mkdirs(join(path, 'pywikibot'), mode=0o700)

        # Set pywikibot environment variable
        environ['PYWIKIBOT_DIR'] = join(self.dirs['config'], 'pywikibot')

    def set_locales(self):
        """Set locales"""
        langs = []
        lc, encoding = getdefaultlocale()
        if (lc):
            langs = [lc]
        language = environ.get('LANGUAGE', None)
        if (language):
            langs += language.split(':')
        langs += ['it_IT', 'en_US']
        bindtextdomain(self.appname, self.exec_path)
        textdomain(self.appname)
        self.lang = translation(self.appname, self.exec_path,
        languages=langs, fallback=True)

    def create_pywikibot_config(self, user, bot_user, bot_password):
        """Create pywikibot configuration files

        It writes pywikibot configuration files in Daty directories

        Args:
            user (str): your wikimedia user;
            bot_user (str): the name of your bot;
            bot_password (str): the password of your bot;
        """

        # Paths
        config_file = join(self.exec_path, 'resources', 'user-config.py')
        password_file = join(self.exec_path, 'resources', 'user-password.py')
        config_save_file = join(self.dirs['config'], 'pywikibot', 'user-config.py')
        password_save_file = join(self.dirs['config'], 'pywikibot', 'user-password.py')

        # Open files
        with open(config_file) as f:
            config = f.read()
        f.close()

        with open(password_file) as f:
            password_config = f.read()
        f.close()

        # Change config
        config = sub(u'your_user', user, config)
        password_config = sub(u'your_user', user, password_config)
        password_config = sub(u'your_bot_username', bot_user, password_config)
        password_config = sub(u'your_bot_password', bot_password, password_config)

        # Write files
        try:
            with open(config_save_file, 'w') as f:
                f.write(config)
            f.close()
        except PermissionError as e:
            print(e)
            for dir_type, path in self.dirs.items():
                try:
                    print(path)
                    chmod_recursively(path, mode=0o777)
                    rm(path)
                except Exception as e:
                    print(e)
                    print(e.__traceback__)
            self.set_dirs()
            self.create_pywikibot_config(user, bot_user, bot_password)

        with open(password_save_file, 'w') as f:
            f.write(password_config)
        f.close()

        # Save internal config to disk
        self.data['user'] = user
        self.data['bot user'] = bot_user
        self.data['bot password'] = bot_password
        save(self.data, join(self.dirs['config'], 'config.pkl'))

    def set_resources(self):
        """Sets application resource file."""
        path = join(self.exec_path, 'resources', 'daty.gresource')
        resource = resource_load(path)
        Resource._register(resource)
        print(resource.lookup_data("/ml/prevete/Daty/gtk/filterslist.ui", ResourceLookupFlags(0)))
