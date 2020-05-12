# Daty

[![Python 3.x Support](https://img.shields.io/pypi/pyversions/Django.svg)](https://python.org)
[![License: AGPL v3+](https://img.shields.io/badge/license-AGPL%20v3%2B-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

[![Daty overview](https://gitlab.gnome.org/World/Daty/raw/master/screenshots/overview.png)](screenshots/overview.png)

*Daty* is a free cross-platform advanced Wikidata editor adhering to [GNOME Human Interface Guidelines](https://developer.gnome.org/hig/stable/), intended to enable better editing workflow and faster deployment of requested user features.
Use *Daty* to search, select, read, batch edit items, script actions, share, visualize proposed changes and bots.

*Daty* is written in Python 3 and it uses [GTK+ 3.0](https://developer.gnome.org/hig/stable/) python bindings for interface organization and drawing.

It has a progressive layout thanks to [libhandy](https://source.puri.sm/Librem5/libhandy) and uses [pywikibot](https://phabricator.wikimedia.org/project/profile/87/) as a backend. 

## Current status

The development of the current version (1.0β) has been made possible thanks to a sponsorship provided by [Wikimedia CH](https://wikimedia.ch). 

Endorse the project on [Wikidata](https://wikidata.org/wiki/User:Ogoorcs/Daty/Endorsement) to help the development get funds.

An overview of what you will find in the stable 1.0 version is available at project presentation [page](https://prevete.ml/articles/daty.html).


- [X] Search and open entities through elastic search;
- [X] Search and open entities with filters;
- [X] Read entities and follow their values;
- [X] Mobile view;
- [X] Open entities search;
- [X] Property In-page search;
- [X] Edit statements;
- [ ] Create new statements;
- [ ] Mass-edit statements.

## Installation

### Windows
You can download the installer [here](https://gitlab.gnome.org/World/Daty/uploads/41f2a430beae8dba1b1d46f0878eecac/daty-x86_64-1.0beta.msi).

### GNU/Linux

#### Flatpak

[![](https://flathub.org/assets/badges/flathub-badge-en.png)](https://flathub.org/apps/details/ml.prevete.Daty)

#### Archlinux
The package `daty-git` has been published on [AUR](https://aur.archlinux.org/packages/daty-git/).

### PostmarketOS

```
sudo apk add gcc musl-dev python3-dev
pip install --user daty
```

#### Ubuntu Disco (19.04)

    # apt install python3-gi gir1.2-gtk-3.0 python3-pip libhandy-0.0-0
    # pip3 install pywikibot daty

#### Others
Provided you have already installed on your system

```
* pygobject >= 3.20
* Gtk >= 3.20
* libhandy >= 0.0.4
* pywikibot >= 3.0
```
you can install daty from [Pypi](https://pypi.org/project/daty/).

### Mac OS
Hardware or contributors needed.

## Building from source

#### Option 1: with GNOME Builder
Open GNOME Builder, click the "Clone..." button, paste the repository url.
Clone the project and hit the ![](help/C/figures/builder-run.png) button to start building Daty.

**Note**

Depending on your distribution you could have to run

    systemctl --user start xdg-desktop-portal
    
in order to build the flatpak with GNOME Builder.

#### Option 2: with Flatpak Builder
```
# Clone Daty repository
git clone https://gitlab.gnome.org/World/Daty.git
cd daty
# Add Flathub repository
flatpak remote-add flathub --if-not-exists https://dl.flathub.org/repo/flathub.flatpakrepo
# Install the required GNOME runtimes
flatpak install flathub org.gnome.Platform//3.30 org.gnome.Sdk//3.30
# Start building
flatpak-builder --repo=repo ml.prevete.Daty flatpak/ml.prevete.Daty.json --force-clean
# Create the Flatpak
flatpak build-export repo ml.prevete.Daty
flatpak build-bundle repo ml.prevete.Daty.flatpak ml.prevete.Daty
# Install the Flatpak
flatpak install ml.prevete.Daty.flatpak
```

#### Option 3: with Pypi
Provided you have installed

```
* pygobject >= 3.20
* Gtk >= 3.20
* libhandy >= 0.0.4
* pywikibot >= 3.0
```
You just need to enter in the cloned directory and run

    $ sudo python3 setup.py install
    $ daty

## Documentation

Sphinx documentation for the project can be built running

    $ python3 setup.py build_sphinx

You can then read the main page of the built html documentation directing your browser to `doc/build/html/index.html`.

It will be made directly available online after the code will stabilize.

## About

This program is licensed under [GNU Affero General Public License v3 or later](https://www.gnu.org/licenses/agpl-3.0.en.html) by [Pellegrino Prevete](http://prevete.ml).<br>
If you find this program useful, consider [endorsing](https://wikidata.org/wiki/User:Ogoorcs/Daty/Endorsement) the project, offering me a [beer](https://patreon.com/tallero), a new [computer](https://patreon.com/tallero) or a part time remote [job](mailto:pellegrinoprevete@gmail.com) to help me pay the bills.

