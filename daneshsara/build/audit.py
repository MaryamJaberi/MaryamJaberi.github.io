# -*- coding: utf-8 -*-
"""Health report for a review milestone: python3 build/audit.py   → prints, and writes data/health.json
Run at every milestone (after each finished book, each ~10 new entries, or once a week)."""
import json, glob, os, re, collections, datetime
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..'); os.chdir(R)
C = {}
for f in glob.glob('data/*/concepts/*.json'):
    d = json.load(open(f, encoding='utf-8')); C[d['id']] = d
src = json.load(open('core/sources.json', encoding='utf-8'))
con = [i for i, d in C.items() if d['kind'] == 'concept']
inb = collections.Counter(l['to'] for d in C.values() for l in d.get('links', []))
def sids(d): return set(d.get('sources', [])) | {x for p in d.get('points', []) for x in p.get('sources', [])}
bysrc = collections.defaultdict(set)
for i in con:
    for s in sids(C[i]): bysrc[s].add(i)
wk = lambda i: i.split(':')[0]
cross = sum(1 for i, d in C.items() for l in d.get('links', []) if wk(i) != wk(l['to']))
dangling = sorted({l['to'] for d in C.values() for l in d.get('links', []) if l['to'] not in C and wk(l['to']) not in ('iran', 'miyan')})
lonely = [i for i in con if not i.startswith('psy:') and inb[i] == 0 and not any(2 <= len(bysrc[s]) <= 30 for s in sids(C[i]))]
flags = collections.Counter(f for d in C.values() for p in d.get('points', []) for f in p.get('flags', []))
nosrc = [i for i in con if not sids(C[i])]
t4 = [i for i in con if sids(C[i]) and all(src.get(s, {}).get('tier', 9) >= 4 for s in sids(C[i]))]
ch = collections.Counter(d.get('parent') for d in C.values())
thin = [(i, ch[i]) for i, d in C.items() if d['kind'] == 'field' and ch[i] < 3]
titles = collections.defaultdict(list)
for i, d in C.items(): titles[re.sub(r'[\s‌:،«»()؟?]+', '', d['title']['fa'])[:24]].append(i)
dup = [v for v in titles.values() if len(v) > 1]
tr = collections.Counter()
for d in C.values():
    for lang in ('en', 'nl'):
        if not d['title'].get(lang) or not d['summary'].get(lang): tr[lang] += 1
books = json.load(open('data/library/books.json', encoding='utf-8')); coll = json.load(open('data/library/collection.json', encoding='utf-8'))
sk = json.load(open('data/sakht/sakht.json', encoding='utf-8'))
used = {s for d in C.values() for s in sids(d)}
bad = 0
for f in glob.glob('**/*.html', recursive=True):
    if f.startswith('build/'): continue
    s = re.sub(r'<script.*?</script>', '', open(f, encoding='utf-8', errors='ignore').read(), flags=re.S)
    for h in set(re.findall(r'href="([^"#?]+)', s)):
        if re.match(r'(https?:|mailto:|data:|javascript:|//)', h): continue
        t = os.path.normpath(os.path.join(os.path.dirname(f), h))
        if not os.path.exists(t) and not os.path.exists(os.path.join(t, 'index.html')): bad += 1
H = {"date": datetime.date.today().isoformat(), "entries": len(con), "by_wiki": dict(collections.Counter(wk(i) for i in con)),
     "cross_wiki_links": cross, "no_inbound": sum(1 for i in con if inb[i] == 0), "lonely": len(lonely), "dangling_targets": dangling,
     "broken_local_links": bad, "no_source": len(nosrc), "only_tier4": len(t4), "flags": dict(flags), "thin_fields": thin, "similar_titles": len(dup),
     "missing_translation": dict(tr), "sources": len(src), "sources_unused": len(set(src) - used),
     "books_tracked": len(books), "books_full": sum(1 for b in books if b.get('read') == 'full'), "books_partial": sum(1 for b in books if b.get('read') == 'partial'), "library_files": len(coll),
     "ideas": len(sk['ideas']), "sakht_sources": len(sk['sources'])}
json.dump(H, open('data/health.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in H.items(): print(f'{k}: {v}')
print('similar title groups (first 8):', dup[:8])
