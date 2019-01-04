# -*- coding: utf-8 -*-

from copy import deepcopy
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository.GLib import idle_add
from gi.repository.Gtk import Box, CssProvider, StyleContext, STYLE_PROVIDER_PRIORITY_APPLICATION, Template
from pprint import pprint
from threading import Thread

from .wikidata import Wikidata

@Template.from_resource("/org/prevete/Daty/gtk/value.ui")
class Value(Box):
    __gtype_name__ = "Value"

    entry = Template.Child("entry")
    label = Template.Child("label")
    wikidata = Wikidata()

    def __init__(self, claim, *args, **kwargs):
        Box.__init__(self, *args, **kwargs)

        #mainsnak = Wikidata().get_claim_type(claim)
        #entity = self.download(claim_type)
        #if claim_type and any(claim_type.startswith(t) for t in ('P','Q')):
            # Download entity
        #    self.entry.set_text(claim_type)
        #    self.label.set_text(claim_type)

    def download(self, entity):
        f = lambda : deepcopy(entity)
        def do_call():
            entity, error = None, None
            try:
                entity = deepcopy(self.wikidata).download(f())
            except Exception as err:
                error = err
            idle_add(lambda: self.on_download_done(entity, error))
        thread = Thread(target = do_call)
        thread.start()

    def on_download_done(self, entity, error):
        text = Wikidata().get_label(entity)
        self.entry.set_text(text)
        self.label.set_text(text)
