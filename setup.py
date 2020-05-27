from os import walk
from os.path import join
from pathlib import Path
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

# GResources
try:
    sh(['daty/resources/compile-resources.sh'])
    print("Gresources compiled")
except Exception as e:
    print("WARNING: to compile gresource be sure to have \"glib-compile-resources\" in your $PATH")

# Variables
theme_dir = "daty/resources/icons/hicolor"
hicolor_path = "share/icons/hicolor"

# Auxiliary functions
# for paths
in_hicolor_src = lambda x: join(theme_dir, x)
in_hicolor = lambda x: join(hicolor_path, x)

# to install things
encode = lambda src, dest: (dest, [src])
add_data_file = lambda src, dest: data_files.append(encode(src, dest))

# to install icons
def encode_icon(icon):
    icon_path = str(Path(icon).parents[0])
    return encode(in_hicolor_src(icon), in_hicolor(icon_path))
add_icon = lambda icon: data_files.append(encode_icon(icon))

# These files will be installed into prefix
data_files = []

# Icons and desktop file
add_data_file('data/ml.prevete.Daty.desktop', 'share/applications')

icons = ['scalable/apps/ml.prevete.Daty.svg',
         'scalable/apps/ml.prevete.Daty-symbolic.svg',
         'scalable/places/discussion-page-symbolic.svg',
         '48x48/apps/ml.prevete.Daty.png',
         '16x16/apps/ml.prevete.Daty-symbolic.png'
        ]

for icon in icons:
    add_icon(icon)

# data_files = data_files + [encode_icon(icon) for icon in icons]
# 
# data_files = [
#     ('share/applications', ['daty/resources/ml.prevete.Daty.desktop']),
#     (hicolor_path('scalable/apps'),   [hicolor_src_path('scalable/apps/ml.prevete.Daty.svg')]),
#     (hicolor_path('scalable/apps'),   [hicolor_src_path('scalable/apps/ml.prevete.Daty-symbolic.svg')]),
#     (hicolor_path('scalable/places'), [hicolor_src_path('scalable/places/discussion-page-symbolic.svg')]),
#     (hicolor_path('48x48/apps'),      [hicolor_src_path('48x48/apps/ml.prevete.Daty.png')]),
#     (hicolor_path('16x16/apps'),      [hicolor_src_path('16x16/apps/ml.prevete.Daty-symbolic.png')])
# ]

data_files.extend(help())

#print(data_files)
daty_files = explore('daty/po') + explore('daty/resources')

setup(
    name = "daty",
    version = "1.0beta",
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
    data_files = data_files,
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
