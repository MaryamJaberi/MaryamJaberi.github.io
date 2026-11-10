# -*- coding: utf-8 -*-
"""Build atlas/sitemap.html (نقشهٔ سایت): 1) mind-map tree of everything, 2) link graph between groups, 3) proposed structure.
All numbers come from the files themselves (pages, hyperlinks, data/*/concepts, core/*.json)."""
import os, re, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
pages = {}
for dp, _, fs in os.walk(R):
    rel = os.path.relpath(dp, R)
    if rel.startswith('build') or rel.startswith('.git'): continue
    for f in fs:
        if f.endswith('.html'):
            p = os.path.normpath(os.path.join(rel, f))
            txt = open(os.path.join(R, p), encoding='utf-8', errors='ignore').read()
            if 'http-equiv="refresh"' in txt: continue   # redirect stubs are not pages
            pages[p] = txt
def title(s, p):
    m = re.search(r'<title>(.*?)</title>', s, re.S); t = re.sub(r'\s+', ' ', m.group(1)).split(' | ')[0].strip() if m else p
    return t
TITLE = {p: title(s, p) for p, s in pages.items()}
PSY_TOOLS = {'graph', 'land', 'body', 'emotions', 'timeline', 'heat', 'river', 'lineage', 'prism', 'path', 'effect', 'evidence', 'debate', 'guess', 'lab', 'scales', 'learn', 'library', 'atlas2'}
def group(p):
    d, f = os.path.dirname(p), os.path.basename(p)[:-5]
    if p == 'index.html': return 'home'
    if d == 'psy':
        if f == 'index': return 'psy-home'
        if re.fullmatch(r's\d+', f): return 'psy-lessons'
        if f in PSY_TOOLS: return 'psy-tools'
        if f == 'orgsvc': return 'product-org'
        return 'psy-books'
    if d == 'psy/tools': return 'psy-tools'
    if d == 'psy/lessons': return 'psy-lessons'
    if d == 'psy/topics': return 'psy-books'
    if d == 'wellbeing': return 'product-org'
    if d in ('soc', 'phil', 'tabar', 'tarikh', 'iran'):
        return d + '-home'
    if d == 'miyan': return 'miyan'
    if d == 'simorgh': return 'simorgh'
    if d in ('soc/tools', 'phil/tools', 'tabar/tools', 'tarikh/tools'): return d.split('/')[0] + '-tools'
    if d == 'iran/tools': return 'iran-tools'
    if d == 'atlas':
        return 'atlas-bridges' if f == 'bridge' else 'atlas-worlds'
    if d == 'atlas/tools': return 'atlas-tools'
    if d == 'core': return 'core'
    return 'other'
G = collections.defaultdict(list)
for p in sorted(pages): G[group(p)].append(p)
# ---- real hyperlinks between groups
edges = collections.Counter(); inc = collections.Counter(); page_in = collections.Counter(); page_out = collections.Counter()
for p, s in pages.items():
    seen = set()
    for h in re.findall(r'href="([^"#?]+)', s):
        if h.startswith(('http', 'mailto', 'tel', 'data', 'javascript')): continue
        t = os.path.normpath(os.path.join(os.path.dirname(p), h))
        if os.path.isdir(os.path.join(R, t)): t = os.path.join(t, 'index.html')
        if t in pages and t != p and (p, t) not in seen:
            seen.add((p, t)); page_in[t] += 1; page_out[p] += 1
            a, b = group(p), group(t)
            if a != b: edges[(a, b)] += 1
orphans = sorted(p for p in pages if page_in[p] == 0)
# ---- concept layer
C = {}
for f in glob.glob(f'{R}/data/*/concepts/*.json'):
    d = json.load(open(f, encoding='utf-8')); C[d['id']] = d
ROOT = {'psy': 'psy:psyche', 'soc': 'soc:soc', 'phil': 'phil:phil', 'tabar': 'tabar:tabar', 'tarikh': 'tarikh:tarikh'}
def top_city(k, w):
    n = 0
    while C[k]['parent'] in C and C[k]['parent'] != ROOT[w] and n < 20: k = C[k]['parent']; n += 1
    return k if C[k]['parent'] == ROOT[w] else None
cnt = collections.Counter(); 
for k in C:
    w = k.split(':')[0]; c = top_city(k, w)
    if c: cnt[c] += 1
cities = {w: sorted([[d['title']['fa'], cnt[c]] for c, d in C.items() if d['parent'] == ROOT[w]], key=lambda x: -x[1]) for w in ROOT}
wl = collections.Counter()
for i, d in C.items():
    a = i.split(':')[0]
    for l in d['links']:
        b = l['to'].split(':')[0]
        if a != b and a < b: wl[(a, b)] += 1
        elif a != b: wl[(b, a)] += 1
stats = json.load(open(f'{R}/core/registry.json', encoding='utf-8'))['stats']
def pl(g): return [[p, TITLE[p]] for p in G.get(g, [])]
NODES = [
 # id, branch, label, note, pages, status
 ('psy-home', 'wiki', 'روان: صفحهٔ اول', '', pl('psy-home'), ''),
 ('psy-lessons', 'wiki', 'درس‌نامه‌ها', 'جزوه‌های دورهٔ مهارت‌های انسانی', pl('psy-lessons'), ''),
 ('psy-books', 'wiki', 'مرور کتاب‌ها و موضوع‌ها', 'صفحه‌های موضوعی و قفسه‌های کتاب', pl('psy-books'), ''),
 ('psy-tools', 'wiki', 'اطلس‌ها و ابزارهای روان', 'گراف، سرزمین، خط زمانی، سنجش‌خانه…', pl('psy-tools'), ''),
 ('product-org', 'product', 'سنجش سلامت سازمانی', 'محصول جدا که الان داخل ویکی روان است', pl('product-org'), 'جابه‌جا شود'),
 ('soc-home', 'wiki', 'جامعه', '', pl('soc-home') + pl('soc-tools'), ''),
 ('tabar-home', 'wiki', 'تبار و ژنتیک', '', pl('tabar-home') + pl('tabar-tools'), ''),
 ('phil-home', 'wiki', 'فلسفه', '', pl('phil-home') + pl('phil-tools'), ''),
 ('tarikh-home', 'wiki', 'تاریخ و ایران‌شناسی', 'تازه، از مخزن ۷۵۲ کتاب', pl('tarikh-home') + pl('tarikh-tools'), ''),
 ('ling', 'wiki', 'زبان‌شناسی', 'برنامه‌ریزی‌شده', [], 'به‌زودی'),
 ('miyan', 'atlas', 'ارتباط رشته‌ها', 'ویکی ۲۵ پل میان‌رشته‌ای', pl('miyan'), ''),
 ('iran-home', 'iran', 'ویکی ایران', '۱۶ برگهٔ داده با سال، روش و ردهٔ کیفیت', pl('iran-home') + pl('iran-tools'), ''),
 ('simorgh', 'sim', 'سیمرغ', 'تمثیل، راه‌حل و بازی بر پایهٔ وضعیت‌ها', pl('simorgh'), 'در ساخت'),
 ('atlas-worlds', 'atlas', 'جهان‌های اطلس', 'جهان دانش، سرزمین دانش، اطلس رشته‌ها، کتابخانه', pl('atlas-worlds'), ''),
 ('atlas-bridges', 'atlas', 'پل‌های میان‌رشته‌ای', '', pl('atlas-bridges'), ''),
 ('atlas-tools', 'atlas', 'ابزارهای اطلس', 'مقایسه، مسیر، شواهد…', pl('atlas-tools'), ''),
 ('core', 'core', 'هستهٔ مشترک', 'چهره‌ها، منابع، صف بازبینی، مشارکت', pl('core'), ''),
 ('time', 'ext', 'اطلس زمان', 'مستقل در earth-through-time', [['https://maryamjaberi.github.io/earth-through-time/', 'اطلس زمان']], ''),
]
BRANCH = {'wiki': 'ویکی‌ها', 'iran': 'لنز ایران', 'sim': 'سیمرغ', 'atlas': 'اطلس‌های میان‌رشته‌ای', 'core': 'هستهٔ مشترک', 'ext': 'خارج از این مخزن', 'product': 'محصول جدا'}
data = {'nodes': [{'id': a, 'br': b, 'l': c, 'n': d, 'p': e, 's': f, 'in': sum(page_in[x[0]] for x in e), 'orph': [x[0] for x in e if page_in[x[0]] == 0]} for a, b, c, d, e, f in NODES],
        'edges': [[a, b, n] for (a, b), n in edges.items() if a != 'home' and b != 'home'], 'homeOut': [[b, n] for (a, b), n in edges.items() if a == 'home'],
        'cities': cities, 'wl': [[a, b, n] for (a, b), n in wl.items()], 'stats': stats, 'orphans': [[p, TITLE[p]] for p in orphans], 'branch': BRANCH, 'npages': len(pages)}
tpl = open(f'{HERE}/sitemap.tpl.html', encoding='utf-8').read()
open(f'{R}/atlas/sitemap.html', 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/', 'window.SM=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';'))
print('pages', len(pages), 'orphans', len(orphans), 'groups', len(NODES), 'edges', len(data['edges']))
print({k: len(v) for k, v in G.items()})
print({w: [x for x in cities[w]] for w in cities})
