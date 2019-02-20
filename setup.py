from os import walk
from os.path import join
from pprint import pprint
from setuptools import setup, find_packages
from subprocess import check_output as sh

with open("README.md", "r") as fh:
    long_description = fh.read()

def explore(path, ):
    """Return all paths of files in a given path

    Args:
        path (str)

    Returns:
        (list) containing the paths of the files in input path
    """
    result = []
    for (path, dirname, files) in walk(path):
        for f in files:
            #print(join(path, f))
            result.append(join(path, f)[5:])
    return result

def help():
    build = []
    for (path, dirname, files) in walk('help'):
        try:
            dirname = join('share/help', path.split('/')[1], 'daty', *path.split('/')[2:])
            if files != []:
                for f in files:
                    build.append((dirname, [join(path, f)]))
        except Exception as e:
            if type(e) == IndexError:
                pass
            else:
                raise e
    return build

data_files = [
    ('share/applications', ['daty/resources/ml.prevete.Daty.desktop']),
    ('share/icons/hicolor/scalable/apps', ['daty/resources/icons/scalable/apps/ml.prevete.Daty.svg']),
    ('share/icons/hicolor/48x48/apps', ['daty/resources/icons/48x48/apps/ml.prevete.Daty.png']),
    ('share/icons/hicolor/16x16/apps', ['daty/resources/icons/16x16/apps/ml.prevete.Daty-symbolic.png'])
]

data_files.extend(help())

print(data_files)
daty_files = explore('daty/po') + explore('daty/resources')

try:
    sh(['daty/resources/compile-resources.sh'])
except Exception as e:
    print("WARNING: to compile gresource be sure to have \"glib-compile-resources\" in your $PATH")

setup(
    name = "daty",
    version = "1.0alpha",
    author = "Pellegrino Prevete",
    author_email = "pellegrinoprevete@gmail.com",
    description = "Advanced Wikidata editor",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/tallero/daty",
    packages = find_packages(),
    package_data = {
        '': ['*.sh'],
        'daty':daty_files
    },
    data_files = data_files, #[
    #    ('share/applications', ['daty/resources/ml.prevete.Daty.desktop']),
    #    ('share/icons/hicolor/scalable/apps', ['daty/resources/icons/scalable/apps/ml.prevete.Daty.svg']),
    #    ('share/icons/hicolor/48x48/apps', ['daty/resources/icons/48x48/apps/ml.prevete.Daty.png']),
    #    ('share/icons/hicolor/16x16/apps', ['daty/resources/icons/16x16/apps/ml.prevete.Daty-symbolic.png'])
    #],
    entry_points = {'gui_scripts': ['daty = daty:main']},
    install_requires = [
    'appdirs',
    'bleach',
    'beautifulsoup4',
    'pygobject',
    'pywikibot',
    'requests',
    'setproctitle',
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: Unix",
    ],
)
