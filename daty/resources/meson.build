gnome = import('gnome')

# message('TODO: Compiling resources')
# gnome.compile_resources(
#     'daty', 'daty.gresource.xml',
#      source_dir : '.',
#      c_name : 'daty',
#      install_dir : python_dir,
#      install: true)


message('Compiling schemas')
gnome.compile_schemas()
install_data(
    'org.gnome.Music.gschema.xml',
    install_dir : 'share/glib-2.0/schemas')

message('TODO: Making a .desktop file')

message('TODO: Preparing appdata')

message('Install a man page')
install_man('gnome-music.1')

message('TODO: Making a list of icons')
icon_names = []

icon_themes = ['hicolor', 'HighContrast']
icon_sizes = ['16', '22', '32', '48', '256']

foreach theme : icon_themes
    foreach size: icon_sizes
        icon_names = icon_names + ['icons/' + theme + '/' + size + 'x' + size + '/apps/gnome-music.png']
    endforeach
endforeach
icon_names = icon_names + ['icons/hicolor/gnome-music.svg']
install_data(icon_names, install_dir : 'share')
