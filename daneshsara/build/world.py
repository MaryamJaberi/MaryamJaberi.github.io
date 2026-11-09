# -*- coding: utf-8 -*-
"""Build atlas/world.html + atlas/world-data.js («جهان دانش»): a zoomable map where
land = wiki, city = field, town/district = concept (by tree depth), people = shops, cross-wiki links = roads.
Layout is deterministic circle packing of the concept tree (data/*/concepts, core/people.json, core/sources.json)."""
import json, glob, os, math, collections
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
C = {}
for f in glob.glob(f'{R}/data/*/concepts/*.json'):
    d = json.load(open(f, encoding='utf-8')); C[d['id']] = d
REG = json.load(open(f'{R}/core/registry.json', encoding='utf-8'))['entries']
P = json.load(open(f'{R}/core/people.json', encoding='utf-8'))
S = json.load(open(f'{R}/core/sources.json', encoding='utf-8'))
ROOTS = {'psy': 'psy:psyche', 'soc': 'soc:soc', 'phil': 'phil:phil', 'tabar': 'tabar:tabar'}
ORDER = ['soc', 'phil', 'psy', 'tabar']
kids = collections.defaultdict(list)
for i, d in C.items():
    if d['parent'] in C and i != d['parent']: kids[d['parent']].append(i)
size = {}
def sz(i):
    if i not in size: size[i] = 1 + sum(sz(c) for c in kids[i])
    return size[i]
for r in ROOTS.values(): sz(r)
U = 26.0  # world units per leaf radius
pos = {}  # id -> [x,y,r] relative to parent centre, filled in pack()
def pack(i):
    ch = sorted(kids[i], key=lambda c: (-size[c], c))
    if not ch: pos[i] = [0, 0, U]; return U
    rs = [pack(c) for c in ch]
    placed = []; grid = {}; CELL = U * 6
    def free(x, y, r):
        gx, gy = int(x // CELL), int(y // CELL)
        for ax in range(gx - 2, gx + 3):
            for ay in range(gy - 2, gy + 3):
                for (px, py, pr) in grid.get((ax, ay), ()):
                    if (x - px) ** 2 + (y - py) ** 2 < (r + pr + U * .35) ** 2: return False
        return True
    for c, r in zip(ch, rs):
        t = 0.0; step = .12
        while True:
            rad = U * 1.1 * math.sqrt(t) * 0.55 + (0 if placed else 0)
            ang = t * 2.399963
            x, y = rad * math.cos(ang), rad * math.sin(ang)
            if not placed: x = y = 0
            if free(x, y, r): break
            t += step if t < 40 else step * 2
        placed.append((x, y, r)); grid.setdefault((int(x // CELL), int(y // CELL)), []).append((x, y, r))
        pos[c] = [x, y, r]
    R_ = max(math.hypot(x, y) + r for x, y, r in placed) + U * .9
    pos[i] = [0, 0, R_]
    return R_
for r in ROOTS.values(): pack(r)
radius = {w: pos[r][2] for w, r in ROOTS.items()}
gap = 700
rowh1 = max(radius['soc'], radius['phil']); rowh2 = max(radius['psy'], radius['tabar'])
cent = {'soc': (-radius['soc'] - gap / 2, 0), 'phil': (radius['phil'] + gap / 2, 0),
        'psy': (-radius['psy'] - gap / 2, rowh1 + rowh2 + gap), 'tabar': (radius['tabar'] + gap / 2, rowh1 + rowh2 + gap)}
# land centre of soc/phil on row 1: align vertically centred
cent['soc'] = (cent['soc'][0], 0); cent['phil'] = (cent['phil'][0], 0)
absx = {}
def place(i, ox, oy):
    x, y, r = pos[i]; absx[i] = (ox + x, oy + y, r)
    for c in kids[i]: place(c, ox + x, oy + y)
for w, r in ROOTS.items():
    pos[r][0], pos[r][1] = 0, 0; place(r, *cent[w])
def depth(i):
    n = 0
    while C[i]['parent'] in C and C[i]['parent'] != i: i = C[i]['parent']; n += 1
    return n
def land_of(i): return i.split(':')[0]
def city_of(i):
    while depth(i) > 1: i = C[i]['parent']
    return i if depth(i) == 1 else None
ids = list(C.keys())
# importance: links + people + points + sources + subtree size
def imp(i):
    d = C[i]; return len(d['links']) * 2 + len(d['people']) + len(d['points']) + len(d['sources']) * .5 + (size[i] - 1) * 3
idx = {i: n for n, i in enumerate(ids)}
used_src = {}; SRC = []
def src(sid):
    if sid not in S: return None
    if sid not in used_src:
        s = S[sid]; used_src[sid] = len(SRC); SRC.append([s.get('cite', ''), s.get('year'), s.get('tier')])
    return used_src[sid]
TITLE = lambda d: d['title']['fa']
nodes = []
imp_sorted = sorted(ids, key=lambda i: -imp(i)); rank = {i: n for n, i in enumerate(imp_sorted)}
for i in ids:
    d = C[i]; x, y, r = absx[i]; dp = depth(i)
    ps = []
    for p in d['points'][:4]:
        ps.append([p['text']['fa'], [src(s) for s in p['sources'][:2] if src(s) is not None], p.get('flags', [])])
    srcs = [k for k in (src(s) for s in d['sources'][:6]) if k is not None]
    lk = [[idx[l['to']], l['rel'], (l.get('note') or {}).get('fa', '')] for l in d['links'] if l['to'] in idx]
    nodes.append({'i': i, 'w': land_of(i), 'd': dp, 'p': idx.get(d['parent'], -1) if d['parent'] in C and i != d['parent'] else -1,
                  'x': round(x, 1), 'y': round(y, 1), 'r': round(r, 1), 't': TITLE(d), 'e': d['title'].get('en', ''),
                  'k': REG.get(i, {}).get('type', 'concept'), 'u': REG.get(i, {}).get('url', ''), 'st': d['status'],
                  's': d['summary']['fa'], 'pt': ps, 'sr': srcs, 'lk': lk, 'pe': [], 'ir': d.get('iran') or '', 'rk': rank[i], 'n': size[i] - 1})
# people: shops
city = {i: city_of(i) for i in ids}
people = []
pcon = collections.defaultdict(list)
for i in ids:
    for pid in C[i]['people']: pcon[pid].append(i)
for pid, cons in pcon.items():
    p = P.get(pid)
    if not p: continue
    cities = collections.Counter(city[c] for c in cons if city[c])
    top = [c for c, _ in cities.most_common(2)]
    people.append({'id': pid, 'n': p['name'].get('fa') or p['name'].get('en'), 'en': p['name'].get('en', ''), 'y': p.get('years', ''),
                   'o': (p.get('note') or {}).get('fa', ''), 'wd': p.get('wikidata') or '', 'c': [idx[c] for c in cons],
                   'ct': [idx[c] for c in top], 'x': len(cities) >= 2})
for pi, p in enumerate(people):
    for c in p['c']: nodes[c]['pe'].append(pi)
xs = [n['x'] for n in nodes]; ys = [n['y'] for n in nodes]
meta = {'bounds': [min(x - 0 for x in xs) - 800, min(ys) - 800, max(xs) + 800, max(ys) + 800],
        'lands': {w: {'root': idx[r], 'x': round(cent[w][0], 1), 'y': round(cent[w][1], 1), 'r': round(radius[w], 1)} for w, r in ROOTS.items()},
        'built': REG and '' or ''}
out = {'meta': meta, 'nodes': nodes, 'people': people, 'src': SRC}
js = 'window.WORLD=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';'
open(f'{R}/atlas/world-data.js', 'w', encoding='utf-8').write(js)
tpl = open(f'{HERE}/world.tpl.html', encoding='utf-8').read()
open(f'{R}/atlas/world.html', 'w', encoding='utf-8').write(tpl)
print('world-data.js', len(js) // 1024, 'KB; nodes', len(nodes), 'people', len(people), 'bounds', meta['bounds'], {w: round(v['r']) for w, v in meta['lands'].items()})
