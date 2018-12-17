from os import walk
from os.path import join
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

def explore(path):
    result = []
    for (path, dirname, files) in walk(path):
        for f in files: 
            result.append(join(path, f)[5:])
    return result

daty_files = explore('daty/po') + explore('daty/resources')

setup(
    name = "daty",
    version = "0.1",
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
    entry_points = {
        'console_scripts': ['daty = daty:main']
    },
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
