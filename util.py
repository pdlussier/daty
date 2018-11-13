from ast import literal_eval
from gi.repository.Gdk import Screen
from gi.repository.Gtk import CssProvider, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION

def import_translations(lang):
    with open('po/'+lang+'.po', 'r') as g:
        content = literal_eval(g.read())
        g.close()
    return content

def gtk_style():
    with open('style.css', 'rb') as f:
        css = f.read()
        f.close()
    style_provider = CssProvider()
    style_provider.load_from_data(css)
    StyleContext.add_provider_for_screen(Screen.get_default(),
                                         style_provider,
                                         STYLE_PROVIDER_PRIORITY_APPLICATION)
