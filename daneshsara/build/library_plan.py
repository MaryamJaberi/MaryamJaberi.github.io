# -*- coding: utf-8 -*-
"""Build atlas/library-plan.html («کتابخانهٔ جهان دانش»): a top-down floor plan of a library.
Wings = wikis, bookcases = fields (depth-1 cities), spines = books (data/library/books.json) placed by where their entries landed.
Books whose entries span 2+ wikis sit on the central interdisciplinary table; books without entries wait at the lobby shelf."""
import json, glob, os, collections, math
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
C = {}
for f in glob.glob(f'{R}/data/*/concepts/*.json'):
    d = json.load(open(f, encoding='utf-8')); C[d['id']] = d
BOOKS = json.load(open(f'{R}/data/library/books.json', encoding='utf-8'))
ROOT = {'psy': 'psy:psyche', 'soc': 'soc:soc', 'phil': 'phil:phil', 'tabar': 'tabar:tabar'}
NAME = {'psy': 'روان‌شناسی', 'soc': 'جامعه‌شناسی', 'phil': 'فلسفه', 'tabar': 'تبار و ژنتیک'}
def city(i):
    while C[i]['parent'] in C and C[C[i]['parent']]['parent'] in C and C[i]['parent'] != i: i = C[i]['parent']
    return i
cities = {w: [c for c, d in C.items() if d['parent'] == r] for w, r in ROOT.items()}
for w in cities: cities[w].sort(key=lambda c: C[c]['title']['fa'])
out_books = []; placed = collections.defaultdict(list); table = []; lobby = []
for k in BOOKS:
    ents = []
    for e in k['entries']:
        w = e['u'].split('/')[0]; cid = f'{w}:{e["id"]}'
        if cid in C: ents.append((w, cid, e))
    ws = collections.Counter(w for w, _, _ in ents)
    b = {'n': k['n'], 't': k['title'].split(' (عنوان از نام فایل')[0], 'a': k['author'], 'y': k['year'], 'ty': k['type'], 'tier': k['tier'], 'dec': k['decision'],
         'lab': k['label'], 'best': k['best'], 'cau': k['cautions'][:3], 'rs': k['reasons'][:3], 'why': k['why'],
         'en': [[e['t'], e['u'], w] for w, _, e in ents[:8]], 'ne': len(k['entries']), 'ws': sorted(ws)}
    idx = len(out_books); out_books.append(b)
    if not ents: lobby.append(idx); continue
    if len(ws) >= 2: table.append(idx); continue
    w = next(iter(ws)); cc = collections.Counter(city(c) for ww, c, _ in ents if ww == w)
    placed[(w, cc.most_common(1)[0][0])].append(idx)
rooms = []
RW, RH, GAP = 900, 560, 260; ROWGAP = 250
pos = {'soc': (60, 60), 'phil': (60 + RW + GAP, 60), 'psy': (60, 60 + RH + ROWGAP), 'tabar': (60 + RW + GAP, 60 + RH + ROWGAP)}
for w in ['soc', 'phil', 'psy', 'tabar']:
    rx, ry = pos[w]; cs = cities[w]; cases = []
    cols = 2; rowsn = math.ceil(len(cs) / cols); cw, chh = 380, 58; padx = (RW - cols * cw) / (cols + 1); pady = 70; stepy = (RH - pady - 40) / max(1, rowsn)
    for i, c in enumerate(cs):
        col, row = i % cols, i // cols; bs = placed.get((w, c), [])
        cases.append({'c': c, 'title': C[c]['title']['fa'], 'x': rx + padx + col * (cw + padx), 'y': ry + pady + row * stepy, 'w': cw, 'h': chh + 38 * max(0, math.ceil(len(bs) / 40) - 1), 'b': bs, 'ne': len([1 for k in C if k.startswith(w + ':') and city(k) == c]) - 1 if False else None})
    rooms.append({'w': w, 'name': NAME[w], 'x': rx, 'y': ry, 'W': RW, 'H': RH, 'cases': cases})
cx = 60 + RW + GAP / 2
plan = {'rooms': rooms, 'table': {'x': cx, 'y': 60 + RH + ROWGAP / 2, 'r': 82, 'b': table},
        'lobby': {'x': cx - 330, 'y': 60 + 2 * RH + ROWGAP + 60, 'w': 660, 'h': 70, 'b': lobby}, 'desk': {'x': cx, 'y': 60 + 2 * RH + ROWGAP + 190},
        'books': out_books, 'bounds': [0, 0, 60 + 2 * RW + GAP + 60, 60 + 2 * RH + ROWGAP + 300]}
js = 'window.LIB=' + json.dumps(plan, ensure_ascii=False, separators=(',', ':')) + ';'
tpl = open(f'{HERE}/library_plan.tpl.html', encoding='utf-8').read()
open(f'{R}/atlas/library-plan.html', 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/', js))
print('library-plan', len(js) // 1024, 'KB; books', len(out_books), 'on shelves', sum(len(v) for v in placed.values()), 'table', len(table), 'lobby', len(lobby), 'cases', sum(len(r['cases']) for r in rooms), 'empty cases', sum(1 for r in rooms for c in r['cases'] if not c['b']))
