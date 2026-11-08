# -*- coding: utf-8 -*-
"""Export the psychology graph (280 nodes) into daneshsara concept files.
Reads raw.json (DATA, PSYTR, BOOKLETS, F, SCITR) and writes:
  data/psy/concepts/<id>.json   one concept per file, id psy:<slug>
  core/people.json              shared people, id core:<latin-slug>
  core/sources.json             shared sources, id src:<hash>
  data/psy/booklets.json
"""
import json, re, hashlib, os, sys, unicodedata
RAW = sys.argv[1]
R = json.load(open(RAW))
D = R['DATA']; TR = R['PSYTR']; BK = R['BOOKLETS']; SCI = R.get('SCITR', {})
OUT = os.path.dirname(os.path.abspath(__file__)) + '/..'
by = {n['id']: n for n in D}

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()
    return s

FA_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
# ---- relation vocabulary mapping (closed set + see-also fallback)
RULES = [
    ('contrasts',    r'پادزهر|نقطهٔ مقابل|در برابر|مقابل|تضاد|رقیب|برعکس|ضد'),
    ('explains',     r'سازوکار|علت|پیامد|ریشه|مکانیسم|توضیح|زمینه|منشأ|مبنا|پایه|مدار پاداش'),
    ('same-as',      r'همان|معادل|نام دیگر|هم‌معنا'),
    ('part-of',      r'زیرشاخه|جزئی از|بخشی از|شاخه'),
    ('prerequisite', r'پیش‌نیاز|اول باید'),
    ('measured-by',  r'سنجش|مقیاس|پرسشنامه|آزمون'),
    ('critiques',    r'نقد|چالش|اعتراض|تکرار نشد'),
    ('applies-to',   r'کاربرد|در سازمان|در کار|در درمان|در آموزش|درمان'),
    ('evidence-for', r'شاهد|آزمایش|مطالعه|داده|یافته'),
]
def rel(label):
    for r, pat in RULES:
        if re.search(pat, label):
            return r
    return 'see-also'

# ---- people
people = {}; pidx = {}
def person(s):
    s = s.strip()
    if s in pidx:
        return pidx[s]
    m = re.match(r'^(.*?)\s*(?:\((.*?)\))?\s*(?:—\s*(.*))?$', s)
    fa = m.group(1).strip(); yrs = (m.group(2) or '').strip(); note = (m.group(3) or '').strip()
    latin = TR['P'].get(fa) or SCI.get(fa) or ''
    if not latin and re.search(r'[A-Za-z]', note) and not re.search(r'[؀-ۿ]', note):
        latin = note; note = ''
    pid = 'core:' + (slug(latin) if latin and slug(latin) else 'fa-' + hashlib.md5(fa.encode()).hexdigest()[:8])
    if pid not in people:
        people[pid] = {'id': pid, 'name': {'fa': fa, 'en': latin, 'nl': latin},
                       'years': yrs.translate(FA_DIGITS), 'note': {'fa': note},
                       'wikidata': None, 'wikis': []}
    if 'psy' not in people[pid]['wikis']:
        people[pid]['wikis'].append('psy')
    pidx[s] = pid
    return pid

# ---- sources
sources = {}; sidx = {}
def source(s):
    s = s.strip()
    if s in sidx:
        return sidx[s]
    sid = 'src:' + hashlib.md5(s.encode()).hexdigest()[:10]
    m = re.search(r'\((\d{4})\)', s); year = int(m.group(1)) if m else None
    tier = 2 if re.search(r'\(\d{4}\)\.', s) else 3
    sources[sid] = {'id': sid, 'cite': s, 'year': year, 'tier': tier, 'wikis': ['psy']}
    sidx[s] = sid
    return sid

def depth(n):
    d = 0; c = n
    while c.get('p'):
        c = by[c['p']]; d += 1
    return d

def field_of(n):
    c = n
    while c.get('p') and depth(c) > 2:
        c = by[c['p']]
    return 'psy:' + c['id'] if c is not n else 'psy:' + (n.get('p') or 'psyche')

def tr(k):
    g = TR['G'].get(k, [None, None])
    return {'fa': k, 'en': g[0], 'nl': g[1]}

os.makedirs(OUT + '/data/psy/concepts', exist_ok=True)
count = 0; kinds = {}
for n in D:
    d = depth(n)
    kind = 'root' if d == 0 else 'field' if d == 1 else 'subfield' if d == 2 else 'concept'
    kinds[kind] = kinds.get(kind, 0) + 1
    nl = TR['N'].get(n['id'], [None, None])[1]
    S = TR['S'].get(n['id'], [None, None])
    srcs = [source(r) for r in n.get('res', [])]
    c = {
        'id': 'psy:' + n['id'],
        'kind': kind,
        'title': {'fa': n['fa'], 'en': n['en'], 'nl': nl},
        'parent': ('psy:' + n['p']) if n.get('p') else None,
        'field': field_of(n) if kind == 'concept' else None,
        'summary': {'fa': n['s'], 'en': S[0], 'nl': S[1]},
        'points': [{'text': tr(k), 'sources': srcs[:1] if srcs else [], 'flags': []} for k in n.get('k', [])],
        'links': [{'to': 'psy:' + x[0], 'rel': rel(x[1]), 'note': tr(x[1])} for x in n.get('x', [])],
        'people': [person(p) for p in n.get('ppl', [])],
        'sources': srcs,
        'booklets': ([n['c']] if isinstance(n.get('c'), str) else list(n.get('c') or [])),
        'origin': n.get('src'),
        'iran': None,
        'wikidata': None,
        'status': 'reviewed' if n.get('src') else 'draft',
    }
    json.dump(c, open(f"{OUT}/data/psy/concepts/{n['id']}.json", 'w'), ensure_ascii=False, indent=1)
    count += 1
# keep entries other wikis added (anything not owned by psy), then overwrite psy's
def keep(path, mine):
    old = json.load(open(path)) if os.path.exists(path) else {}
    for k, v in old.items():
        if k in mine:
            for w in v.get('wikis', []):
                if w not in mine[k]['wikis']: mine[k]['wikis'].append(w)
            if v.get('url') and not mine[k].get('url'): mine[k]['url'] = v['url']
        elif 'psy' not in v.get('wikis', []):
            mine[k] = v
    return mine
json.dump(keep(OUT + '/core/people.json', people), open(OUT + '/core/people.json', 'w'), ensure_ascii=False, indent=1)
json.dump(keep(OUT + '/core/sources.json', sources), open(OUT + '/core/sources.json', 'w'), ensure_ascii=False, indent=1)
json.dump({k: {'fa': v['fa'], 'url': v['url']} for k, v in BK.items()},
          open(OUT + '/data/psy/booklets.json', 'w'), ensure_ascii=False, indent=1)
rels = {}
for n in D:
    for x in n.get('x', []):
        r = rel(x[1]); rels[r] = rels.get(r, 0) + 1
print('concepts', count, kinds, 'people', len(people), 'sources', len(sources), 'rels', rels)
