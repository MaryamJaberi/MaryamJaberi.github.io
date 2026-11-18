# -*- coding: utf-8 -*-
"""Import reviewed draft entries (from texts, PDFs and lectures) with their plain explanation, examples and try-it:
python3 build/draft_import.py DIR [DIR ...]   (each DIR holds m_*.json in the lecture schema plus the round-2 keys)
Additive: writes data/<wiki>/concepts/<id>.json, never touches order.json, every entry stays status 'draft'.
Round-2 keys per entry: explain{fa,en}, examples[{kind,label,fa,en,source}], why_it_matters_fa, try_it{fa,tool}, confusions_fa."""
import json, glob, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import Seed, R
RELS = {'part-of', 'explains', 'evidence-for', 'evidence-against', 'contrasts', 'prerequisite', 'same-as', 'applies-to', 'measured-by', 'critiques', 'bridges', 'see-also'}
FLAGS = ('unreplicated', 'contested', 'dated', 'editor-note')
WIKIS = ('soc', 'phil', 'tabar')
FIELDS = {W: set(json.load(open(f'{R}/data/{W}/order.json'))) for W in WIKIS}
EXIST = {}
for p in glob.glob(f'{R}/data/*/concepts/*.json'):
    w = p.split('/')[-3]; EXIST.setdefault(os.path.basename(p)[:-5], w)
files = sorted(f for d in sys.argv[1:] for f in glob.glob(f'{d}/m_*.json'))
NEW = {}
for f in files:
    for e in json.load(open(f, encoding='utf-8'))['entries']:
        if e.get('wiki') in WIKIS: NEW[e['id']] = e['wiki']
def target(t):
    t = str(t).strip()
    if ':' in t:
        w, s = t.split(':', 1)
        if s in NEW and NEW[s] == w: return t
        if os.path.exists(f'{R}/data/{w}/concepts/{s}.json'): return t
        s = s
    else: s = t
    if s in NEW: return f'{NEW[s]}:{s}'
    if s in EXIST: return f'{EXIST[s]}:{s}'
    return None
def txt(v):
    if isinstance(v, list): return '\n\n'.join(str(x) for x in v if x)
    if isinstance(v, dict): return v.get('fa') or ''
    return v
def tri(fa, en=None): return {'fa': txt(fa) or None, 'en': txt(en) or None}
S = Seed('soc'); n = 0; skipped = []; dropped_links = 0
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    for e in d['entries']:
        W = e.get('wiki')
        if W not in WIKIS: skipped.append(e.get('id')); continue
        S.W = W
        spk = d.get('speaker') or ''; lec_cite = f"{spk} (n.d.). {d.get('lecture', '')} (متن پیاده‌شده)"
        lec = None if d.get('paper') else S.src(lec_cite, 3)
        ext = [S.src(x['cite'], x.get('tier', 3)) for x in d.get('sources', [])]
        pts = []
        for p in e['points']:
            ss = []
            for s in p.get('src', []):
                if isinstance(s, int) and s < len(ext): ss.append(ext[s])
                elif isinstance(s, str) and s.startswith('lecture'): ss.append(lec if lec else (ext[0] if ext else None))
            ss = [x for x in dict.fromkeys(ss) if x]
            if not ss and ext: ss = [ext[0]]
            pts.append(S.pt(p.get('fa', ''), p.get('en', ''), ss, [x for x in p.get('flags', []) if x in FLAGS]))
        ppl = []
        for x in e.get('people', []):
            if isinstance(x, dict) and x.get('latin'): ppl.append(S.person(x['latin'], x.get('fa') or x['latin'], x.get('years', ''), x.get('note', '')))
            elif isinstance(x, str) and x.strip(): ppl.append(S.person(x, x))
        links = []
        for l in e.get('links', []):
            to, rel, lfa, len_ = (l.get('to'), l.get('rel', 'see-also'), l.get('fa', ''), l.get('en', '')) if isinstance(l, dict) else (l, 'see-also', '', '')
            t = target(to)
            if not t or rel not in RELS or t == f"{W}:{e['id']}": dropped_links += 1; continue
            links.append(S.ln(t, rel, lfa, len_))
        field = e.get('field') if f"{W}:{e.get('field')}" in FIELDS[W] else ('theory' if W == 'soc' else 'epistemology' if W == 'phil' else 'human-evolution')
        title = {k: v for k, v in e['title'].items() if k in ('fa', 'en', 'nl')}
        summ = {k: v for k, v in e['summary'].items() if k in ('fa', 'en', 'nl')}
        S.C = []; S.add(e['id'], 'concept', title, summ, parent=field, field=field, points=pts, links=links, people=ppl, origin=os.path.basename(f))
        c = S.C[0]
        if (S.C[0]['sources'] == [] and ext): c['sources'] = ext[:1]
        x = e.get('explain') or {}
        if x.get('fa'): c['explain'] = tri(x.get('fa'), x.get('en'))
        exs = []
        for ex in e.get('examples', []) or []:
            if not ex.get('fa'): continue
            lab = 'real' if (ex.get('label') or '').strip() in ('داستان واقعی', 'real') and ex.get('source') else 'illustration'
            k = ex.get('kind') if ex.get('kind') in ('everyday', 'iran', 'history', 'story', 'game') else 'everyday'
            exs.append({'kind': k, 'label': lab, 'text': tri(ex['fa'], ex.get('en')), 'source': ex.get('source') or None})
        if exs: c['examples'] = exs
        if e.get('why_it_matters_fa'): c['why'] = tri(e['why_it_matters_fa'])
        t = e.get('try_it') or {}
        if t.get('fa'):
            tool = t.get('tool') if isinstance(t.get('tool'), str) and '.html' in t.get('tool') and os.path.exists(f"{R}/{t['tool'].split('#')[0]}") else None
            c['try'] = {'text': tri(t['fa']), 'tool': tool}
        cf = e.get('confusions_fa')
        if isinstance(cf, str) and cf.strip(): cf = [cf]
        if isinstance(cf, list):
            cf = [tri(x if isinstance(x, str) else (x.get('fa') if isinstance(x, dict) else None)) for x in cf]
            cf = [x for x in cf if x['fa']]
            if cf: c['confusions'] = cf
        json.dump(c, open(f"{R}/data/{W}/concepts/{e['id']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1); n += 1
json.dump(S.people, open(f'{R}/core/people.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S.sources, open(f'{R}/core/sources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('imported', n, 'entries from', len(files), 'files; skipped', len(skipped), 'dropped links', dropped_links)
