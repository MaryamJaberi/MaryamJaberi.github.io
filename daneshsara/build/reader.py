# -*- coding: utf-8 -*-
"""Generic wiki reader: python3 build/reader.py <wiki>  → <wiki>/index.html
Inlines the wiki's concepts, the people/sources/iran notes they use, and the registry entries that its links point at."""
import json, os, sys, glob, re
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
W = sys.argv[1]
def load(p): return json.load(open(p, encoding='utf-8'))
concepts = {c['id']: c for c in (load(p) for p in glob.glob(f'{R}/data/{W}/concepts/*.json'))}
people = load(f'{R}/core/people.json'); sources = load(f'{R}/core/sources.json'); reg = load(f'{R}/core/registry.json')['entries']
irans = {i['id']: i for i in (load(p) for p in glob.glob(f'{R}/iran/*.json'))}
pids = {p for c in concepts.values() for p in c.get('people', [])}
sids = {s for c in concepts.values() for s in c.get('sources', [])} | {s for c in concepts.values() for p in c.get('points', []) for s in p.get('sources', [])}
iids = {c['iran'] for c in concepts.values() if c.get('iran')}
lids = {l['to'] for c in concepts.values() for l in c.get('links', []) if l['to'] not in concepts}
ext = {k: {'title': reg[k]['title'], 'url': '../' + reg[k]['url']} for k in lids if k in reg}
# ---- connective tissue computed across all wikis: who links here, and what else comes from the same source
import collections
ALLC = {c['id']: c for c in (load(p) for p in glob.glob(f'{R}/data/*/concepts/*.json'))}
_back = collections.defaultdict(list); _bysrc = collections.defaultdict(set)
for c in ALLC.values():
    for l in c.get('links', []):
        if l['to'] in concepts and c['id'] != l['to']: _back[l['to']].append(c['id'])
    if c['kind'] == 'concept':
        for sid in set(c.get('sources', [])) | {x for pt in c.get('points', []) for x in pt.get('sources', [])}: _bysrc[sid].add(c['id'])
BACK = {}; SAME = {}
for cid, c in concepts.items():
    out = {l['to'] for l in c.get('links', [])}
    b = [x for x in dict.fromkeys(_back.get(cid, [])) if x not in out][:12]
    if b: BACK[cid.split(':')[1]] = b
    if c['kind'] != 'concept': continue
    score = collections.Counter()
    for sid in set(c.get('sources', [])) | {x for pt in c.get('points', []) for x in pt.get('sources', [])}:
        grp = _bysrc.get(sid, ())
        if 2 <= len(grp) <= 30:
            for o in grp:
                if o != cid and o not in out and o not in b: score[o] += 1
    sm = [o for o, _ in sorted(score.items(), key=lambda kv: (-kv[1], kv[0]))[:6]]
    if sm: SAME[cid.split(':')[1]] = sm
lids |= {x for v in list(BACK.values()) + list(SAME.values()) for x in v if x not in concepts}
ext = {k: {'title': reg[k]['title'], 'url': '../' + reg[k]['url']} for k in lids if k in reg}
order = load(f'{R}/data/{W}/order.json') if os.path.exists(f'{R}/data/{W}/order.json') else []
DATA = {'wiki': W, 'order': order, 'concepts': list(concepts.values()), 'people': {k: people[k] for k in pids if k in people},
        'sources': {k: sources[k] for k in sids if k in sources}, 'iran': {k: irans[k] for k in iids if k in irans}, 'ext': ext,
        'back': BACK, 'same': SAME,
        'merged': {a.split(':')[1]: b.split(':')[0] for a, b in (load(f'{R}/data/merged-concepts.json') if os.path.exists(f'{R}/data/merged-concepts.json') else {}).items() if a.startswith(W + ':')},
        'renamed': {a.split(':')[1]: b.split(':')[1] for a, b in (load(f'{R}/data/renamed-concepts.json') if os.path.exists(f'{R}/data/renamed-concepts.json') else {}).items() if a.startswith(W + ':')}}
root = next((c for c in concepts.values() if c['kind'] == 'root'), None)
title = root['title'] if root else {'fa': W, 'en': W, 'nl': W}
tpl = open(f'{HERE}/reader.tpl.html', encoding='utf-8').read()

import html as _html
_d = ((root.get('summary') or {}).get('fa') if root else '') or ('همهٔ مدخل‌های ویکی ' + title['fa'] + ' در دانش‌سرا، با خلاصه، نکته‌ها، منبع و پیوند به ویکی‌های دیگر.')
_d = _html.escape(_d[:155])
out = tpl.replace('__DATA__', json.dumps(DATA, ensure_ascii=False)).replace('__TITLE_FA__', title['fa']).replace('__TITLE_EN__', title.get('en') or title['fa']).replace('__DESC__', _d)
os.makedirs(f'{R}/{W}', exist_ok=True)
OUT = sys.argv[2] if len(sys.argv) > 2 else ('index.html' if W == 'psy' else 'entries.html')
open(f'{R}/{W}/{OUT}', 'w', encoding='utf-8').write(out)
print(W, 'concepts', len(concepts), 'people', len(DATA['people']), 'sources', len(DATA['sources']), 'iran', len(DATA['iran']), 'ext', len(ext), 'bytes', len(out))
