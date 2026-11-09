# -*- coding: utf-8 -*-
"""A small «این اطلس از کجا می‌خواند» bar on each atlas page, matching the landing's dots.
Re-runnable: it rewrites its own block."""
import os, re, glob, html
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.chdir(R)
NAME = {'psy': 'روان‌شناسی', 'soc': 'جامعه', 'phil': 'فلسفه', 'tabar': 'تبار و ژنتیک', 'iran': 'ایران', 'miyan': 'ارتباط رشته‌ها'}
VAR = {'psy': 'var(--fam-psy)', 'soc': 'var(--fam-soc)', 'phil': 'var(--fam-hum)',
       'tabar': 'var(--fam-bio)', 'iran': 'var(--primary)', 'miyan': 'var(--fam-formal)'}
# which layer each atlas reads from, taken from the landing page's own data-u attributes
SRC = {}
land = open('index.html', encoding='utf-8').read()
for m in re.finditer(r'data-u="([^"]*)"\s+href="([^"]*)"', land):
    SRC[os.path.normpath(m.group(2))] = m.group(1).split()
EXTRA = {'atlas/world.html': ['psy', 'soc', 'phil', 'tabar'], 'atlas/library-plan.html': ['psy', 'soc', 'phil', 'tabar'],
         'atlas/lands.html': ['psy', 'soc', 'phil', 'tabar'], 'atlas/bridge.html': ['psy', 'soc', 'phil', 'tabar'],
         'atlas/index.html': ['psy', 'soc', 'phil', 'tabar'], 'atlas/sitemap.html': ['psy', 'soc', 'phil', 'tabar', 'iran']}
CSS = ('<style id="ds-src-css">.ds-src{font:400 .78rem/1.9 inherit;display:flex;flex-wrap:wrap;gap:8px;align-items:center;'
 'padding:7px max(16px,env(safe-area-inset-right,0px)) 8px max(16px,env(safe-area-inset-left,0px));'
 'border-bottom:1px solid var(--line,#e5e1d8);background:var(--surface,#f4f1ea);color:var(--ink-3,#8a8578)}'
 '.ds-src a{display:inline-flex;align-items:center;gap:5px;color:var(--ink-2,#5c574c);text-decoration:none;'
 'border:1px solid var(--line-strong,#d8d3c7);border-radius:999px;padding:1px 10px}'
 '.ds-src a:hover{border-color:currentColor}.ds-src a u{width:7px;height:7px;border-radius:50%;background:var(--d);display:inline-block}'
 '@media (prefers-color-scheme:dark){.ds-src{border-color:var(--line,#33312c);background:var(--surface,#232220)}}</style>')

n = 0
for p in sorted(set(list(SRC) + list(EXTRA))):
    if not p.startswith('atlas' + os.sep) and not p.startswith('atlas/'): continue
    if not os.path.exists(p): continue
    keys = [k for k in (SRC.get(p) or EXTRA.get(p) or []) if k in NAME]
    if not keys: continue
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<style id="ds-src-css">.*?</style>\s*', '', s, flags=re.S)
    s = re.sub(r'<nav class="ds-src".*?</nav>\s*', '', s, flags=re.S)
    chips = ''.join(f'<a href="../{k}/" style="--d:{VAR[k]}"><u></u>{html.escape(NAME[k])}</a>' for k in keys)
    bar = CSS + '<nav class="ds-src" aria-label="سرچشمهٔ داده">این اطلس از این ویکی‌ها می‌خواند:' + chips + '</nav>'
    m = re.search(r'<nav class="ds-crumbs".*?</nav>', s, re.S)
    if m: s = s[:m.end()] + '\n' + bar + s[m.end():]
    else:
        mb = re.search(r'<body[^>]*>', s)
        if not mb: continue
        s = s[:mb.end()] + '\n' + bar + s[mb.end():]
    open(p, 'w', encoding='utf-8').write(s); n += 1
print('source bar on', n, 'atlas pages')
