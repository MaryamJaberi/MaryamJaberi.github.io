# -*- coding: utf-8 -*-
"""Build atlas/lands.html (سرزمین دانش): families as lands, fields as cities, interdisciplinary fields as roads,
with the people recorded on each bridge. Data: atlas/fields.json + atlas/bridges.json (inlined, no fetch)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
A = json.load(open(f'{R}/atlas/fields.json', encoding='utf-8'))
B = json.load(open(f'{R}/atlas/bridges.json', encoding='utf-8'))
keep = ('id', 'fam', 'par', 'fa', 'en', 'nl', 'q', 'ppl', 'b', 'wikis')
fields = [{k: f[k] for k in keep if k in f} for f in A['fields']]
bridges = {k: {'people': v.get('people', []), 'title': v.get('title')} for k, v in B.items()}
tpl = open(f'{HERE}/lands.tpl.html', encoding='utf-8').read()
out = (tpl.replace('__FAM__', json.dumps(A['fam'], ensure_ascii=False))
          .replace('__FIELDS__', json.dumps(fields, ensure_ascii=False))
          .replace('__BRIDGES__', json.dumps(bridges, ensure_ascii=False)))
open(f'{R}/atlas/lands.html', 'w', encoding='utf-8').write(out)
print('lands.html', len(out), 'fields', len(fields), 'bridges', len(bridges))
