# -*- coding: utf-8 -*-
"""Inject the «کمک عملی» block into psy/topics/*.html from data/psy/help.json. Idempotent (markers)."""
import json, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
H = json.load(open(f'{R}/data/psy/help.json', encoding='utf-8'))
CSS = ('<style>.ds-help{margin:32px 0;padding:18px 20px;border:2px solid var(--good,#2f7d5b);border-radius:16px;background:var(--paper,var(--bg,#fff));line-height:1.95}'
       '.ds-help h2{margin:0 0 4px;font-size:1.2rem}.ds-help .hs{margin:0 0 10px;color:var(--muted,#667);font-size:.9rem}'
       '.ds-help ol{list-style:persian;margin:0;padding-inline-start:1.3em;display:grid;gap:6px}'
       '.ds-help .pro{margin-top:12px;padding:10px 14px;border-inline-start:4px solid var(--bad,#b3261e);background:color-mix(in srgb,var(--bad,#b3261e) 6%,transparent);border-radius:10px;font-size:.95rem}'
       '.ds-help .sos,.ds-help .base{margin:8px 0 0;font-size:.82rem;color:var(--muted,#667)}</style>')
SOS = 'اگر فکر آسیب به خودت داری، تنها نمان: همین حالا با یک نفر مورد اعتماد حرف بزن و با اورژانس تماس بگیر (ایران ۱۱۵ و اورژانس اجتماعی ۱۲۳؛ هلند ۱۱۳).'
n = 0
for slug, (title, steps, pro, base) in H.items():
    p = f'{R}/psy/topics/{slug}.html'
    if not os.path.isfile(p): print('missing', slug); continue
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--ds-help-->.*?<!--/ds-help-->\n?', '', s, flags=re.S)
    s = re.sub(r'<li class="ds-help-li">.*?</li>\n?', '', s)
    e = html.escape
    block = ('<!--ds-help-->' + CSS + '<section class="ds-help" id="help" aria-labelledby="help-h"><h2 id="help-h">کمک عملی: ' + e(title) + '</h2>'
             '<p class="hs">سه قدم که می‌شود از امروز امتحان کرد.</p><ol>' + ''.join(f'<li>{e(x)}</li>' for x in steps) + '</ol>'
             + (f'<div class="pro"><b>کی سراغ متخصص بروم؟</b> {e(pro)}</div>' if pro else '')
             + f'<p class="base">پایه: {e(base)}. این‌ها آموزش عمومی‌اند، نه تشخیص یا درمان.</p><p class="sos">{SOS}</p></section><!--/ds-help-->\n')
    i = s.find('id="nx-h"')
    if i < 0: print('no anchor', slug); continue
    j = s.rfind('\n', 0, i) + 1
    s = s[:j] + block + s[j:]
    s = s.replace('<nav class="toc" aria-label="فهرست"><h2>فهرست این جزوه</h2><ol>\n', '<nav class="toc" aria-label="فهرست"><h2>فهرست این جزوه</h2><ol>\n<li class="ds-help-li"><a href="#help">کمک عملی: از امروز چه کنم</a></li>\n', 1)
    open(p, 'w', encoding='utf-8').write(s); n += 1
print(f'psy help blocks: {n}')
