

```python
from copy import deepcopy
from daty.wikidata import Wikidata
from itertools import chain
from pprint import pprint
from random import randint
wikidata = Wikidata()
```

## Tools


```python
def pick_entities(N=100, random=False, verbose=False):
    """Pick lots of entities
    
        Args:
            N (int): number of items;
            random (bool): random or sequential;
            verbose (bool): extendend output.
        Returns:
            (list) entities.
    """
    f = lambda x: randint(1,50000000) if random else x
    entities = []
    for i in range(1,N):
        try:
            entities.append(wikidata.download(['Q', 'P', 'L'][randint(0,1)] + str(f(i))))
        except Exception as e:
            if verbose:
                print(e)
    return entities

def dict_list_union_keys(dict_list):
    keys = set()
    for d in dict_list:
        keys = keys.union(set(d.keys()))
    return keys

def dict_list_keys(dict_list, verbose=True):
    """Returns keys of dictionary list"""
    all_keys = dict_list_union_keys(dict_list)
    common_keys = deepcopy(all_keys)
    for d in dict_list:
        common_keys = common_keys.intersection(set(d.keys()))
    diff_keys = all_keys.difference(common_keys)
    if verbose:
        print("".join(["Union:\t\t", str(all_keys), "\n",
                       "Intersection:\t", str(common_keys), "\n",
                       "Difference\t", str(diff_keys)]))
    return all_keys, common_keys, diff_keys
```

# Entity


```python
entities = pick_entities(100)
print("Campione:", len(entities))
keys = dict_list_keys(entities)
```

    Campione: 63
    Union:		{'labels', 'aliases', 'claims', 'datatype', 'sitelinks', 'descriptions'}
    Intersection:	{'labels', 'aliases', 'descriptions', 'claims'}
    Difference	{'sitelinks', 'datatype'}


## Claim

Let's group claims (`dict`) from `entities`; claims of an entity are grouped by property; claims have to be converted into JSONs to be read:


```python
entities_claims = []
for e in entities:
    for P in e['claims'].keys():
        claims = (c.toJSON() for c in e['claims'][P])
        entities_claims.append(claims)
entities_claims = list(chain.from_iterable(entities_claims))
print("Campione:", len(entities_claims))
keys = dict_list_keys(entities_claims)
```

    Campione: 11511
    Union:		{'references', 'rank', 'mainsnak', 'type', 'qualifiers', 'id', 'qualifiers-order'}
    Intersection:	{'mainsnak', 'rank', 'id', 'type'}
    Difference	{'references', 'qualifiers', 'qualifiers-order'}


### Type


```python
types = [c['type'] for c in entities_claims]
print("Campione:\t", len(types))
print("Valori:\t\t", set(types))
```

    Campione:	 11511
    Valori:		 {'statement'}


### Mainsnak
Let's group claims' mainsnaks (`dict`).


```python
mainsnaks = [c['mainsnak'] for c in entities_claims]
print("Campione:", len(mainsnaks))
keys = dict_list_keys(mainsnaks)
```

    Campione: 11511
    Union:		{'datatype', 'snaktype', 'property', 'datavalue'}
    Intersection:	{'property', 'snaktype'}
    Difference	{'datatype', 'datavalue'}


#### Snaktype


```python
snaktypes = set(snak['snaktype'] for snak in mainsnaks)
print(snaktypes)
```

    {'value', 'somevalue', 'novalue'}


#### Property


```python
properties = set(snak['property'] for snak in mainsnaks)
print("Campione:", len(properties))
print("Values: [P1,...]")
```

    Campione: 636
    Values: [P1,...]


#### Datatype


```python
datatypes = set(s['datatype'] for s in mainsnaks if 'datatype' in s.keys())
pprint(datatypes)
```

    {'commonsMedia',
     'external-id',
     'geo-shape',
     'globe-coordinate',
     'monolingualtext',
     'quantity',
     'string',
     'tabular-data',
     'time',
     'url',
     'wikibase-item',
     'wikibase-property'}


##### wikibase-property


```python
def set_datatype(datatype):
    return [s for s in mainsnaks if ('datatype' in s.keys()) and
                                      (s['datatype'] == datatype)]
Oprint()
print("Snaks with wikibase-property as datatype")
print("Campione:", len(snak_dt_wp))
keys = dict_list_keys(snak_dt_wp)

#print(set(s['datavalue']['value']['entity-type'] for s in snak_dt_wp))
#keys = dict_list_keys([s['datavalue']['value']['entity-type'] for s in snak_dt_wp])
print(set(s['datavalue'] for s in snak_dt_wp))
#pprint(datatypes)
```

    Snaks with wikibase-property as datatype
    Campione: 125
    Union:		{'datatype', 'snaktype', 'property', 'datavalue'}
    Intersection:	{'property', 'snaktype', 'datatype', 'datavalue'}
    Difference	set()



    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-91-ba1c6b701037> in <module>
          9 #print(set(s['datavalue']['value']['entity-type'] for s in snak_dt_wp))
         10 #keys = dict_list_keys([s['datavalue']['value']['entity-type'] for s in snak_dt_wp])
    ---> 11 print(set(s['datavalue'] for s in snak_dt_wp))
         12 #pprint(datatypes)


    TypeError: unhashable type: 'dict'


#### Datavalue


```python
datavalues = [s['datavalue'] for s in mainsnaks if 'datavalue' in s.keys()]
print("Campione:", len(datavalues))
keys = dict_list_keys(datavalues)
```

    Campione: 11493
    Union:		{'type', 'value'}
    Intersection:	{'type', 'value'}
    Difference	set()


##### type


```python
types = set(d['type'] for d in datavalues)
print("Campione:", len(types))
print(types)
```

    Campione: 6
    {'globecoordinate', 'string', 'monolingualtext', 'wikibase-entityid', 'time', 'quantity'}


##### Value
###### wikibase-entityid


```python
values = [d['value'] for d in datavalues if d['type'] == 'wikibase-entityid']
print("Campione:", len(values))
keys = dict_list_keys(values)
```

    Campione: 5067
    Union:		{'numeric-id', 'entity-type'}
    Intersection:	{'entity-type', 'numeric-id'}
    Difference	set()


###### entity-type


```python
entity_types = [value['entity-type'] for value in values]
print("Campione:", len(entity_types))
print(set(entity_types))
```

    Campione: 5067
    {'property', 'item'}



```python
values = [d['value'] for d in datavalues if d['type'] == 'wikibase']
print("Campione:", len(values))
keys = dict_list_keys(values)
```

    Campione: 5067
    Union:		{'numeric-id', 'entity-type'}
    Intersection:	{'entity-type', 'numeric-id'}
    Difference	set()

