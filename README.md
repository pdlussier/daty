# Daty

[![Python 3.x Support](https://img.shields.io/pypi/pyversions/Django.svg)](https://python.org)
[![License: AGPL v3+](https://img.shields.io/badge/license-AGPL%20v3%2B-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

[![Daty welcome screen](mockups/editor.png)](mockups/editor.png)

*Daty* is a free cross-platform advanced Wikidata editor adhering to [GNOME Human Interface Guidelines](https://developer.gnome.org/hig/stable/), intended to enable better editing workflow and faster deployment of requested user features.
Use *Daty* to search, select, read, batch edit items, script actions, share, visualize proposed changes and bots.

*Daty* is written in Python 3 and it uses [GTK+ 3.0](https://developer.gnome.org/hig/stable/) python bindings for interface organization and drawing.

It has a progressive layout thanks to [libhandy](https://source.puri.sm/Librem5/libhandy) and uses [pywikibot](https://phabricator.wikimedia.org/project/profile/87/) as a backend.

## Currently implemented
- [X] Search and open entities through elasting search and triplets;
- [X] Read entities and follow their values;
- [ ] Page and sidebar search;
- [ ] Edit statements;
- [ ] Mass-edit statements.

## Installation

### Windows
I have to upload the exe.

### Linux
#### Archlinux
The package `daty-git` has been published on [AUR](https://aur.archlinux.org/packages/daty-git/).

### Ubuntu
#### Ubuntu disco
In progress.

#### Fedora
In progress.

#### Flatpak
In progress.

### Mac OS
Hardware or contributors needed.

## Development
In order to run `daty`, you need to install [PyGobject](https://pygobject.readthedocs.io/en/latest/getting_started.html), [pywikibot](https://pypi.org/project/pywikibot) and [libhandy](https://source.puri.sm/tallero/libhandy). If your distribution is not in the following, hopefully it should still have them available for you in their repositories.

### Archlinux
Install `daty-git` from [AUR](https://aur.archlinux.org/packages/daty-git/) and skip to "Run".

### Ubuntu disco / Debian Sid
Run the following commands from your terminal:

    # apt install python3-gi gir1.2-gtk-3.0 python3-pip libhandy-0.0-0
    # pip3 install pywikibot


### Run
To run daty you just need to clone this repository and execute

    $ python3 setup.py sdist bdist_wheel
    $ sudo python3 setup.py install
    $ daty

or you can just open the entry that should have appeared in your menu.

## About

This program is licensed under [GNU Affero General Public License v3 or later](https://www.gnu.org/licenses/agpl-3.0.en.html) by [Pellegrino Prevete](http://prevete.ml).<br>
If you find this program useful, consider voting to give this project a grant at the [itWikiCon 2018 Ideathon](https://meta.wikimedia.org/wiki/ItWikiCon/2018/Ideathon), or offering me a [beer](https://patreon.com/tallero), a new [computer](https://patreon.com/tallero) or a part time remote [job](mailto:pellegrinoprevete@gmail.com) to help me pay the bills.

