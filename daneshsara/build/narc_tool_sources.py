# -*- coding: utf-8 -*-
"""منبع‌های مشترک ابزارهای پروندهٔ «خودشیفتگی و کنترل».

از همان منبع‌هایی که مدخل‌ها استفاده می‌کنند می‌سازد، با کلیدِ خوانا
(نام نویسندهٔ اول + سال) تا بشود در ابزارها به آن ارجاع داد.
خروجی: psy/tools/narc-sources.js
"""
import json, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE)

SRC = json.load(open(f'{R}/core/sources.json', encoding='utf-8'))
used = set()
for f in glob.glob(f'{R}/data/psy/concepts/*.json'):
    c = json.load(open(f, encoding='utf-8'))
    if c.get('field') != 'psy:narcissism-control':
        continue
    used |= set(c.get('sources', []))
    used |= {x for p in c.get('points', []) for x in p.get('sources', [])}

def key_for(s):
    cite = s['cite']
    m = re.match(r'\s*([A-Z][A-Za-z\'’-]+)', cite)
    if m:
        stem = m.group(1).lower()
        stem = re.sub(r'[^a-z]', '', stem)
    else:                                   # منبع فارسی یا نهادی
        m2 = re.match(r'\s*([^\s،.,(]+)', cite)
        stem = re.sub(r'[^a-z0-9]', '', (m2.group(1) if m2 else 'src').lower()) or 'src'
    y = s.get('year') or ''
    return f'{stem}{y}'

reg, taken = {}, {}
for sid in sorted(used, key=lambda i: SRC[i]['cite']):
    s = SRC[sid]
    k = key_for(s)
    if k in taken:                          # دو منبع با یک کلید
        n = taken[k] = taken[k] + 1
        k = f'{k}{chr(96+n)}'
    else:
        taken[k] = 1
    reg[k] = {'c': s['cite'], 't': s.get('tier'), 'u': s.get('url') or None, 'i': sid}

out = ['// ساخته‌شده با build/narc_tool_sources.py — دستی ویرایش نکنید.',
       '// منبع‌های مشترک ابزارهای پروندهٔ «خودشیفتگی و کنترل».',
       'window.NSRC = {']
for k in sorted(reg):
    v = reg[k]
    j = json.dumps({x: y for x, y in v.items() if y is not None}, ensure_ascii=False)
    out.append(f'  {json.dumps(k)}: {j},')
out += ['};', '']
open(f'{R}/psy/tools/narc-sources.js', 'w', encoding='utf-8').write('\n'.join(out))
print(f'narc-sources.js: {len(reg)} sources ({sum(1 for v in reg.values() if v["u"])} with url)')
if '--keys' in sys.argv:
    for k in sorted(reg): print(f'  {k:28s} t{reg[k]["t"]} {reg[k]["c"][:95]}')
