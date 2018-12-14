from appdirs import *
from gettext import bindtextdomain, textdomain, translation
from gi.repository.Gio import Resource, resource_load
from locale import getdefaultlocale
from os import environ, mkdir
from os.path import abspath, dirname, exists, join
from re import sub
from util import load, save

class Config:
    """Daty configuration class.

    It is responsible for:
        - create user dirs
        - set locales
        - set gresource
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
        """Set user dirs for daty"""
        for type,p in self.dirs.items():
            if not exists(p):
                path = ""
                for d in p.split("/"):
                    path = join(path, d)
                    try:
                        mkdir(path)
                    except Exception as e:
                        print(e)
            if type == 'config' and not exists(join(p, 'pywikibot')):
                mkdir(join(p, 'pywikibot'))

        # Set pywikibot environment variable
        environ['PYWIKIBOT_DIR'] = join(self.dirs['config'], 'pywikibot')

    def set_locales(self):
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
        config_file = join(self.exec_path, 'data', 'user-config.py')
        password_file = join(self.exec_path, 'data', 'user-password.py')
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
        with open(config_save_file, 'w') as f:
            f.write(config)
        f.close()

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
        path = join(self.exec_path, 'data', 'gtk', 'daty.gresource')
        resource = resource_load(path)
        #print(Resource.lookup_data(path))
        Resource._register(resource)
