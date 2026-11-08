# -*- coding: utf-8 -*-
"""Import draft entries written from lecture transcripts: python3 build/lecture_import.py
Reads build/lectures/*.json (one file per lecture, schema in the transcript brief), and writes concept files into data/<wiki>/concepts/
(additive; never touches order.json). The lecture video is a tier-3 source; every imported entry is status 'draft'."""
import json, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import Seed, R
URL = {}
CHANNEL = 'https://www.youtube.com/@darwinsabouri'
RELS = {'explains', 'see-also', 'critiques', 'bridges', 'part-of', 'contrasts'}
n = 0
S = Seed('soc')
FIELDS = {W: set(json.load(open(f'{R}/data/{W}/order.json'))) for W in ('soc', 'phil')}
for f in sorted(glob.glob(f'{R}/build/lectures/*.json')):
    stem = os.path.basename(f)[:-5]; d = json.load(open(f, encoding='utf-8'))
    for e in d['entries']:
        W = e['wiki']; S.W = W
        lec_cite = f"Sabouri, D. (n.d.). {d['lecture']} [ویدیو]. YouTube, کانال @darwinsabouri. {URL.get(stem, CHANNEL)} (زیرنویس خودکار)"
        lec = S.src(lec_cite, 3, URL.get(stem, CHANNEL))
        ext = [S.src(x['cite'], x.get('tier', 2)) for x in d.get('sources', [])]
        pts = []
        for p in e['points']:
            ss = [lec if s == 'lecture' else ext[s] for s in p.get('src', []) if s == 'lecture' or isinstance(s, int)]
            pts.append(S.pt(p['fa'], p['en'], ss, [x for x in p.get('flags', []) if x in ('unreplicated', 'contested', 'dated', 'editor-note')]))
        ppl = [S.person(x['latin'], x['fa'], x.get('years', ''), x.get('note', '')) for x in e.get('people', [])]
        links = [S.ln(l['to'], l['rel'], l['fa'], l['en']) for l in e.get('links', []) if l['rel'] in RELS]
        field = e.get('field') if f"{W}:{e.get('field')}" in FIELDS[W] else ('theory' if W == 'soc' else 'epistemology')
        S.C = []; S.add(e['id'], 'concept', e['title'], e['summary'], parent=field, field=field, points=pts, links=links, people=ppl)
        c = S.C[0]
        json.dump(c, open(f"{R}/data/{W}/concepts/{e['id']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1); n += 1
if True:
    json.dump(S.people, open(f'{R}/core/people.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(S.sources, open(f'{R}/core/sources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('imported', n, 'entries')
