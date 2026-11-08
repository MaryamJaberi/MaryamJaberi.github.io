# -*- coding: utf-8 -*-
"""Assemble the published site:
  - copy the built psychology wiki (site/*.html from the scratchpad) into daneshsara/psy/
  - make daneshsara/atlas/index.html from the atlas tool, with links re-pointed to ../psy/
  - write redirect pages psychology-wiki/<k>.html -> daneshsara/psy/<k>.html (hash preserved)
  - write core/redirects.json
Usage: python3 build/site.py <scratch site dir>"""
import os, re, sys, glob, json, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); DS = os.path.abspath(HERE + '/..'); ROOT = os.path.abspath(DS + '/..')
SRC = sys.argv[1]
os.makedirs(DS + '/psy', exist_ok=True); os.makedirs(DS + '/atlas', exist_ok=True)
names = []
for p in sorted(glob.glob(SRC + '/*.html')):
    k = os.path.basename(p)[:-5]
    names.append(k)
    s = open(p, encoding='utf-8').read()
    if k == 'orgsvc':
        # the Wellbeing Check is maintained in place at psychology-wiki/orgsvc.html (another workstream); mirror it, never redirect it
        s = open(f'{ROOT}/psychology-wiki/orgsvc.html', encoding='utf-8').read()
    if k == 'atlas2':
        # shared atlas lives at daneshsara/atlas/; re-point tool links to ../psy/
        s2 = re.sub(r'href="((?!https?:|#|\.\./)[a-z0-9]+\.html)', lambda m: 'href="../psy/' + m.group(1), s)
        s2 = s2.replace('href="../psy/atlas2.html', 'href="./')
        # the embedded tool menu / URL map (JSON strings like "land.html")
        s2 = re.sub(r'"([a-z0-9]+)\.html"', lambda m: '"./"' if m.group(1) == 'atlas2' else f'"../psy/{m.group(1)}.html"', s2)
        open(DS + '/atlas/index.html', 'w', encoding='utf-8').write(s2)
        # psy/atlas2.html becomes a hop to the shared atlas
        s = ('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>اطلس رشته‌ها</title>'
             '<meta http-equiv="refresh" content="0; url=../atlas/"><script>location.replace("../atlas/"+location.hash)</script></head>'
             '<body><a href="../atlas/">اطلس رشته‌ها به دانش‌سرا منتقل شد ↗</a></body></html>')
    open(f'{DS}/psy/{k}.html', 'w', encoding='utf-8').write(s)
# redirects from the old address
RED = {}
for k in names:
    if k == 'orgsvc': continue
    target = f'../daneshsara/psy/{k}.html'
    RED[f'psychology-wiki/{k}.html'] = f'daneshsara/psy/{k}.html'
    page = (f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<title>ویکی روان — نشانی تازه</title><meta http-equiv="refresh" content="0; url={target}">'
            f'<link rel="canonical" href="https://maryamjaberi.github.io/daneshsara/psy/{k}.html">'
            f'<script>location.replace("{target}"+location.search+location.hash)</script>'
            f'<style>body{{font-family:Vazirmatn,Tahoma,sans-serif;padding:2rem;text-align:center;color:#1C1915;background:#F7F4EF}}</style></head>'
            f'<body><p>ویکی روان به <b>دانش‌سرا</b> منتقل شد.</p><p><a href="{target}">اگر خودکار نرفتید، این‌جا بزنید ↗</a></p></body></html>')
    open(f'{ROOT}/psychology-wiki/{k}.html', 'w', encoding='utf-8').write(page)
json.dump(RED, open(DS + '/core/redirects.json', 'w'), ensure_ascii=False, indent=0)
print('psy pages', len(names), '| atlas/index.html written | redirects', len(RED))
