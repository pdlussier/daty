import daty
from pprint import pprint
from pywikibot import Site, ItemPage


site = Site('wikidata', 'wikidata')
repo = site.data_repository()

item_page = ItemPage(repo, 'Q4115189')
data = item_page.get()

#del item_page
#print(data)

#data['descriptions']['it'] = "LE MIE MANI SONO INCREDIBILI"

#for p in data['claims']:
    #data['claims'][p] = [c.toJSON() for c in data['claims'][p]]
    #for c in data['claims'][p]:
    #    pprint(c)
    #    c = c.toJSON()
    #    pprint(c)
#pprint(data["claims"])
claim = data['claims']['P31'][0]

#item_page = ItemPage.editEntity(item_page, data=data)

#new_claim = claim.toJSON()

#new_claim['mainsnak']['datavalue']['value']['numeric-id'] = 143526

#for p in
#claim = claim.fromJSON(site, new_claim)
#print(claim)
#item_page = ItemPage(repo, 'Q4115189')

#old_data = item_page.get()
#old_data = data

#item_page.editEntity(data)
#for p in data['claims']:
#    for c in data['claims'][p]:
#        print(type(c))#c = c.toJSON()
