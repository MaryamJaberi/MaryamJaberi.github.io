# -*- coding: utf-8 -*-
"""Build the shared atlas: atlas/fields.json (52 existing + 25 new) and atlas/bridges/*.json.
Also writes an extended atlas2.data.js for the visual atlas tool (path given as argv[2])."""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = HERE + '/..'
RAW = json.load(open(sys.argv[1]))
sys.path.insert(0, HERE)
from new_fields import NEW
F = RAW['F']; FAM = RAW['FAM']
existing = {f['id'] for f in F}
fields = []
for f in F:
    g = dict(f); g.setdefault('wikis', ['psy']); fields.append(g)
BR = {}
for n in NEW:
    assert n['id'] not in existing, n['id']
    for p in n['par']:
        assert p in existing, (n['id'], p)
    b = n.pop('bridge')
    f = dict(n); f['b'] = True; f['bridge'] = n['id']; f.setdefault('aud', ['stu'])
    fields.append(f)
    BR[n['id']] = {
        'id': n['id'], 'field': n['id'], 'between': n['par'],
        'title': {'fa': n['fa'], 'en': n['en'], 'nl': n['nl']},
        'question': {'fa': n['q'], 'en': b['question_en']},
        'definition': {'fa': b['definition']},
        'landmark': {'fa': b['landmark'], 'url': b['landmark_url']},
        'reference': {'fa': b['reference']},
        'venue': {'fa': b['venue']},
        'people': n['ppl'],
        'finding': {'fa': b['finding'], 'replication': b['replication'], 'url': b['finding_url']},
        'persian': [{'title': t, 'publisher': p, 'url': u, 'verified': v} for (t, p, u, v) in b['persian']],
        'concepts': {'psy': ['psy:' + g for g in n.get('g', [])]},
        'iran': {'fa': b['iran']} if b['iran'] else {},
        'status': 'established' if n['id'] not in ('sociogenomics',) else 'emerging',
        'review': 'draft',
    }
json.dump({'fam': FAM, 'fields': fields}, open(OUT + '/atlas/fields.json', 'w'), ensure_ascii=False, indent=1)
os.makedirs(OUT + '/atlas/bridges', exist_ok=True)
for k, v in BR.items():
    json.dump(v, open(f'{OUT}/atlas/bridges/{k}.json', 'w'), ensure_ascii=False, indent=1)
json.dump(BR, open(OUT + '/atlas/bridges.json', 'w'), ensure_ascii=False, indent=1)
# extended data file for the visual tool
if len(sys.argv) > 2:
    tool = [{k: v for k, v in f.items() if k in ('id', 'b', 'par', 'fam', 'fa', 'en', 'q', 's', 'm', 'jobs', 'study', 'ppl', 'wiki', 'g', 'aud', 'subs', 'bridge', 'wikis')} for f in fields]
    js = 'window.FAM=' + json.dumps(FAM, ensure_ascii=False) + ';\nwindow.F=' + json.dumps(tool, ensure_ascii=False) + ';\n'
    open(sys.argv[2], 'w').write(js)
print('fields', len(fields), 'bridges', len(BR))
