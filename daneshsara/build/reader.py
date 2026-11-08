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
order = load(f'{R}/data/{W}/order.json') if os.path.exists(f'{R}/data/{W}/order.json') else []
DATA = {'wiki': W, 'order': order, 'concepts': list(concepts.values()), 'people': {k: people[k] for k in pids if k in people},
        'sources': {k: sources[k] for k in sids if k in sources}, 'iran': {k: irans[k] for k in iids if k in irans}, 'ext': ext}
root = next((c for c in concepts.values() if c['kind'] == 'root'), None)
title = root['title'] if root else {'fa': W, 'en': W, 'nl': W}
tpl = open(f'{HERE}/reader.tpl.html', encoding='utf-8').read()
out = tpl.replace('__DATA__', json.dumps(DATA, ensure_ascii=False)).replace('__TITLE_FA__', title['fa']).replace('__TITLE_EN__', title.get('en') or title['fa'])
os.makedirs(f'{R}/{W}', exist_ok=True)
open(f'{R}/{W}/index.html', 'w', encoding='utf-8').write(out)
print(W, 'concepts', len(concepts), 'people', len(DATA['people']), 'sources', len(DATA['sources']), 'iran', len(DATA['iran']), 'ext', len(ext), 'bytes', len(out))
