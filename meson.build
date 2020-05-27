# See https://github.com/mesonbuild/meson/issues/226
project('daty', 'c')

version = '3.37.1'

project_id = 'ml.prevete.Daty'

i18n = import('i18n')

DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
bindir = join_paths(get_option('prefix'), get_option('bindir'))

# Configuration params
conf = configuration_data()
conf.set('PACKAGE_VERSION', version)
conf.set('PACKAGE_URL', 'https://wiki.gnome.org/World/Daty')
conf.set('DATA_DIR', DATA_DIR)

message('Looking for dependencies')
py3 = find_program('python3')
glib = dependency('glib-2.0')
gobject = dependency('gobject-2.0')
gir = dependency('gobject-introspection-1.0')
gmod = dependency('gmodule-2.0')
gtk = dependency('gtk+-3.0', version : '>=3.13.2')
libhandy = dependency('libhandy-0.0', version :'>=0.0.3')

message('Getting python install dir')
# r = run_command(py3, '-c', 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')
# if r.returncode() != 0
#     error('Cannot find python install dir')
# endif
# python_dir = r.stdout().strip()
python.sysconfig_path('purelib'))
# 
subdir('data')
# subdir('po')
# subdir('help')
# 
# message('Generate libgd')
# 
# libsources = [
#     'libgd/libgd/gd-types-catalog.c', 'libgd/libgd/gd-types-catalog.h',
#     'libgd/libgd/gd-main-view-generic.c', 'libgd/libgd/gd-main-view-generic.h',
#     'libgd/libgd/gd-styled-text-renderer.c', 'libgd/libgd/gd-styled-text-renderer.h',
#     'libgd/libgd/gd-two-lines-renderer.c', 'libgd/libgd/gd-two-lines-renderer.h',
#     'libgd/libgd/gd-revealer.c', 'libgd/libgd/gd-revealer.h',
#     'libgd/libgd/gd-tagged-entry.c', 'libgd/libgd/gd-tagged-entry.h',
# ]
# 
# libgdgir = shared_library('libgd', libsources,
#     dependencies : [glib, gtk, gobject, gir, gmod])
# 
# gnome.generate_gir(
#     libgdgir,
#     sources : libsources,
#     nsversion : '1.0',
#     namespace : 'Gd',
#     symbol_prefix : 'gd_',
#     identifier_prefix : 'Gd',
#     includes : ['GObject-2.0', 'Gio-2.0', 'Gtk-3.0'],
#     install : true
# )
# 
# message('TODO: Generate authors list')
# 
install_subdir('daty', install_dir: python_dir)

message('Preparing init file')
configure_file(
  input: 'daty.in',
  output: 'daty',
  configuration: conf,
  install_dir: bindir
)

# 
# message('Preparing init file')
# configure_file(input : 'gnome-music.in', output : 'gnome-music', configuration : conf)
# install_data('daty', install_dir: 'bin')
# 

meson.add_install_script('meson_post_install.py')

# meson.set_install_script('meson_install.sh')
