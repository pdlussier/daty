# Windows installer

To create the installer you need to follow the next steps:
 - install the latest version of msys2: http://msys2.github.io/
 - launch msys2_shell.bat and update it with pacman -Syu, you will need to
   relaunch msys2_shell.bat after updating it
 - install git: pacman -S git
 - clone daty: git clone https://gitlab.gnome.org/World/daty
 - cd daty/win32
 - edit make-daty-installer and set the right version of gedit
 - ./make-daty-installer.bat
