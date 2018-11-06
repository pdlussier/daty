#!/usr/bin/env python3


class Importer:

    def __init__(self):
        pass 

    def same_name(self, wikidata_physician, naples_physician):
        item = ItemPage(self.repo, physician)
        item.get()
        if any(item.labels[lang] == naples_physician for lang in item.labels.keys()):
            return True

    def same_as(self, physician):
        item = ItemPage(self.repo, physician)
        item.get()
        for P in item.claims.keys():
            for claim in item.claims[P]:
                for ref in claim.sources:
                    if 'P854' in ref.keys():
                        for statement in ref['P854']:
                            if "http://www.ordinemedicinapoli.it/scheda_medico.php?id=" in statement.toJSON()['datavalue']['value']:
                                return statement.toJSON()['datavalue']['value'].split('=')[-1]
                            else:
                                return False

