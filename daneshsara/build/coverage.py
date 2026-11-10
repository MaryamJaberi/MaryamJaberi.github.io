# -*- coding: utf-8 -*-
"""«نقشهٔ پوشش» — برای هر بُعد کشورداری: چقدر علم داریم، چقدر آمار ایران، چند ریسک، چند ایده، چند کتابِ نخوانده.
Every number is counted from the repo's own data; the only hand-made part is which wiki field / shelf belongs to which domain
(data/coverage.json).  python3 build/coverage.py"""
import os, json, glob, html, math, collections
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.chdir(R)
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
CV = json.load(open('data/coverage.json', encoding='utf-8'))
SK = json.load(open('data/sakht/sakht.json', encoding='utf-8'))
WK = json.load(open('data/sakht/work.json', encoding='utf-8'))
col = json.load(open('data/library/collection.json', encoding='utf-8'))
shelf = collections.Counter(x['shelf'] for x in col)
fcount = collections.Counter(); ftitle = {}
for p in glob.glob('data/*/concepts/*.json'):
    if p.endswith('order.json'): continue
    c = json.load(open(p, encoding='utf-8'))
    if not isinstance(c, dict): continue
    ftitle[c['id']] = c['title']['fa']
    if c['kind'] not in ('root', 'field') and c.get('field'): fcount[c['field']] += 1
iranq = {os.path.basename(p)[:-5]: json.load(open(p, encoding='utf-8'))['question']['fa'] for p in glob.glob('iran/*.json')}
risk_names = {r['k'] for r in SK['risks']}
seat = {s['id']: s for s in WK['seats']}
ideac = collections.Counter(x['c'] for x in SK['ideas'])
SP = json.load(open('data/simorgh/problems.json', encoding='utf-8'))
prob = collections.defaultdict(list)
for x in SP['problems']: prob[x['domain']].append(x['t'])
WN = {'soc': 'جامعه', 'phil': 'فلسفه', 'psy': 'روان', 'tabar': 'تبار', 'tarikh': 'تاریخ'}
WV = {'soc': '--fam-soc', 'phil': '--fam-hum', 'psy': '--fam-psy', 'tabar': '--fam-bio', 'tarikh': '--fam-hist'}

COLS = [('sci', 'علم', 'مفهوم در ویکی‌ها', '--fam-soc'), ('iran', 'ایران', 'یادداشت آماری', '--primary'),
        ('prob', 'مشکل مردم', 'نقشهٔ مشکل‌های سیمرغ', '--warn'), ('risk', 'ریسک', 'در دفتر ریسک', '--err'), ('idea', 'ایده', 'از مخزن ایده‌ها', '--ok'), ('book', 'کتاب', 'در مخزن، نخوانده', '--fam-hist')]
rows = []
for d in CV['domains']:
    for f in d['fields']: assert f in ftitle, f
    for i in d['iran']: assert i in iranq, i
    for r in d['risks']: assert r in risk_names, r
    for s in d['seats']: assert s in seat, s
    for s in d['shelves']: assert s in shelf, s
    v = {'sci': sum(fcount[f] for f in d['fields']), 'iran': len(d['iran']), 'prob': len(prob[d['id']]), 'risk': len(d['risks']),
         'idea': sum(ideac[c] for c in d['ideas']), 'book': sum(shelf[s] for s in d['shelves'])}
    gap = ('علم این حوزه هنوز ویکی ندارد' if v['sci'] == 0 else 'آمار ایران ندارد' if v['iran'] == 0 else
           'هنوز ریسک یا مشکلی برایش ثبت نشده' if v['risk'] + v['prob'] == 0 else 'هر سه لایه شروع شده')
    rows.append((d, v, gap))
mx = {k: max(v[k] for _, v, _ in rows) or 1 for k, *_ in COLS}
tot = {k: sum(v[k] for _, v, _ in rows) for k, *_ in COLS}
nosci = sum(1 for _, v, _ in rows if v['sci'] == 0); noiran = sum(1 for _, v, _ in rows if v['iran'] == 0)
full = sum(1 for _, v, _ in rows if v['sci'] and v['iran'] and (v['risk'] or v['prob']))

def bub(k, n, var):
    if n == 0: return '<span class="bb z" aria-label="صفر"><i></i></span>'
    r = 8 + 22 * math.sqrt(n / mx[k])
    return f'<span class="bb"><i style="width:{r:.0f}px;height:{r:.0f}px;background:var({var})"></i><b>{fa(n)}</b></span>'

def detail(d, v, gap):
    out = [f'<p><b>علم‌های درگیر:</b> {E("، ".join(d["sci"]))}</p>']
    if d['fields']:
        out.append('<p><b>در ویکی‌ها:</b> ' + ' '.join(f'<a class="wl" style="--w:var({WV[f.split(":")[0]]})" href="../{f.split(":")[0]}/"><i>{WN[f.split(":")[0]]}</i>{E(ftitle[f])} · {fa(fcount[f])}</a>' for f in d['fields']) + '</p>')
    if d['iran']:
        out.append('<p><b>آمار ایران:</b> ' + ' '.join(f'<a class="wl" style="--w:var(--primary)" href="../iran/entries.html#{i}"><i>ایران</i>{E(iranq[i][:44])}</a>' for i in d['iran']) + '</p>')
    if prob[d['id']]:
        out.append('<p><b>مشکل‌های مردم:</b> ' + '، '.join(E(x) for x in prob[d['id']]) + f' <a href="{E(SP["from"])}">نقشهٔ مشکل‌های سیمرغ ↗</a></p>')
    if d['risks']:
        out.append('<p><b>ریسک‌ها:</b> ' + '، '.join(E(r) for r in d['risks']) + ' <a href="../sakht/#risks">دفتر ریسک ←</a></p>')
    if d['seats']:
        out.append('<p><b>متخصص:</b> ' + ' '.join(f'<a class="seatl" href="../sakht/work.html#{s}">{E(seat[s]["k"])} · {fa(len(seat[s]["tasks"]))} مسئله</a>' for s in d['seats']) + '</p>')
    if v['book']:
        out.append(f'<p><b>کتاب نخوانده:</b> {fa(v["book"])} عنوان در قفسه‌های {E("، ".join(d["shelves"]))} <a href="collection.html">مخزن ←</a></p>')
    return ''.join(out)

body = ''.join(f'''<details class="row{" nos" if v["sci"] == 0 else ""}" id="{d["id"]}"><summary><span class="dn"><b>{E(d["k"])}</b><em class="g{0 if "ندارد" in gap else 1 if "هنوز" in gap else 2}">{gap}</em></span>
{''.join(f'<span class="c" data-l="{lab}">{bub(k, v[k], var)}</span>' for k, lab, _, var in COLS)}</summary><div class="dt">{detail(d, v, gap)}</div></details>''' for d, v, gap in rows)
head = '<div class="hd"><span></span>' + ''.join(f'<span><b>{lab}</b><small>{sub}</small></span>' for _, lab, sub, _ in COLS) + '</div>'
NS = len(CV['stages']) - 1
road = ''.join(f'<li><div><b>{E(x["k"])}</b><p>{E(x["d"])}</p></div><span class="bar">{"".join("<i class=on></i>" if i <= x["stage"] else "<i></i>" for i in range(1, NS + 1))}</span><em>{CV["stages"][x["stage"]]}</em></li>' for x in CV['roadmap'])

page = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>نقشهٔ پوشش | دانش‌سرا</title>
<meta name="description" content="برای هر بُعد کشورداری: چقدر علم در ویکی‌ها هست، چقدر آمار ایران، چند ریسک و ایده، و کجا هنوز خالی است. همهٔ عددها از خود داده‌های سایت شمرده شده‌اند.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
h1{{font-size:var(--h1);margin:var(--s8) 0 var(--s4);line-height:var(--lh-tight);max-width:20ch;text-wrap:balance}}
p.lead{{color:var(--ink-2);max-width:47em;line-height:2;margin:0 0 var(--s5);font-size:1.05rem}}
section{{padding-block:var(--s6);border-top:1px solid var(--line)}}
h2{{font-size:var(--h3);margin:0 0 var(--s2)}}
p.sub{{color:var(--ink-3);font-size:var(--small);line-height:1.9;margin:0 0 var(--s4);max-width:48em}}
.nums{{display:flex;flex-wrap:wrap;gap:var(--s3);margin-bottom:var(--s5)}}
.nums div{{display:grid;min-width:120px;padding:var(--s3) var(--s4);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);border-top:3px solid var(--c,var(--primary))}}
.nums b{{font-size:1.7rem;line-height:1.15}}.nums span{{font-size:var(--chip);color:var(--ink-3)}}
.mx{{max-width:64em}}
.hd,.row summary{{display:grid;grid-template-columns:minmax(0,1.9fr) repeat(6,minmax(0,1fr));gap:4px;align-items:center}}
.hd{{padding:8px 0;border-bottom:2px solid var(--line-strong);text-align:center}}
.hd b{{display:block;font-size:var(--small)}}.hd small{{font-size:var(--caption,.7rem);color:var(--ink-3);line-height:1.4;display:block}}
.row{{border-bottom:1px solid var(--line)}}.row[open]{{background:var(--surface)}}
.row summary{{cursor:pointer;list-style:none;padding:5px 0;min-height:50px}}.row summary::-webkit-details-marker{{display:none}}
.dn{{display:grid;gap:1px;padding-inline-start:6px;min-width:0}}.dn b{{font-size:var(--small)}}
.dn em{{font-style:normal;font-size:var(--chip)}}.g0{{color:var(--err)}}.g1{{color:var(--warn)}}.g2{{color:var(--ok)}}
.c{{display:grid;place-items:center}}
.bb{{position:relative;display:grid;place-items:center;width:40px;height:40px;max-width:100%}}
.bb i{{border-radius:50%;opacity:.38;display:block}}.bb b{{position:absolute;font-size:var(--chip);font-variant-numeric:tabular-nums}}
.bb.z i{{width:12px;height:12px;border:1.5px dashed var(--ink-3);opacity:.7}}
.dt{{padding:0 var(--s4) var(--s4);display:grid;gap:6px}}.dt p{{margin:0;font-size:var(--small);line-height:2;color:var(--ink-2)}}.dt b{{color:var(--ink)}}
.dt a{{color:var(--primary)}}
.wl{{display:inline-flex;align-items:center;gap:6px;font-size:var(--chip);padding:1px 10px 1px 3px;border-radius:var(--r-full);border:1px solid color-mix(in srgb,var(--w) 45%,var(--line));color:var(--ink-2)!important;text-decoration:none;background:color-mix(in srgb,var(--w) 7%,var(--surface));margin-block:2px}}
.wl i{{font-style:normal;font-weight:650;color:var(--paper);background:var(--w);border-radius:var(--r-full);padding:0 8px}}
.seatl{{font-size:var(--chip);padding:1px 10px;border:1px solid var(--ok);border-radius:var(--r-full);color:var(--ok)!important;text-decoration:none;white-space:nowrap}}
@media (max-width:640px){{.hd,.row summary{{grid-template-columns:repeat(6,minmax(0,1fr))}}.hd span:first-child{{display:none}}.dn{{grid-column:1/-1;padding-top:6px}}.hd small{{display:none}}}}
ol.road{{list-style:none;margin:0;padding:0;display:grid;gap:var(--s3);max-width:60em;counter-reset:r}}
ol.road li{{counter-increment:r;display:grid;grid-template-columns:minmax(0,1fr) 120px auto;gap:12px;align-items:center;padding:var(--s3) var(--s4);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface)}}
ol.road b::before{{content:counter(r,persian) " · ";color:var(--primary)}}
ol.road p{{margin:2px 0 0;font-size:var(--small);color:var(--ink-2);line-height:1.85}}
.bar{{display:grid;grid-template-columns:repeat({NS},1fr);gap:3px}}.bar i{{height:9px;border-radius:5px;background:var(--surface-subtle);border:1px solid var(--line)}}.bar i.on{{background:var(--primary);border-color:var(--primary)}}
ol.road em{{font-style:normal;font-size:var(--chip);color:var(--ink-3);min-width:6em}}
@media (max-width:640px){{ol.road li{{grid-template-columns:minmax(0,1fr) auto}}ol.road li>div{{grid-column:1/-1}}}}
.go{{display:flex;flex-wrap:wrap;gap:8px;margin-top:var(--s4)}}
.go a{{font-size:var(--small);padding:4px 13px;border:1px solid var(--line-strong);border-radius:var(--r-full);color:var(--ink-2);text-decoration:none}}
footer.f{{border-top:1px solid var(--line);padding-block:var(--s5);font-size:var(--small);color:var(--ink-3)}}footer.f a{{color:var(--ink-2);margin-inline-end:var(--s4)}}
</style>
</head>
<body>
<main class="wrap">
<h1>نقشهٔ پوشش: از علم تا مسئله</h1>
<p class="lead">برای ادارهٔ یک کشور باید در هر حوزه سه چیز داشت: علمِ آن حوزه، عددِ واقعی ایران، و فهرست مسئله‌ها و خطرها. این نقشه نشان می‌دهد در هر حوزه کدام را داریم و کجا خالی است.</p>
<div class="nums"><div><b>{fa(len(rows))}</b><span>حوزهٔ کشورداری</span></div><div style="--c:var(--err)"><b>{fa(nosci)}</b><span>حوزه بدون علم در ویکی</span></div><div style="--c:var(--warn)"><b>{fa(noiran)}</b><span>حوزه بدون آمار ایران</span></div><div style="--c:var(--ok)"><b>{fa(full)}</b><span>حوزه با هر سه لایه</span></div><div><b>{fa(tot["book"])}</b><span>کتابِ نخوانده در این حوزه‌ها</span></div></div>

<section id="map">
<h2>پوشش هر حوزه</h2>
<p class="sub">اندازهٔ هر دایره در ستون خودش سنجیده می‌شود (ستون‌ها با هم مقایسه‌پذیر نیستند). دایرهٔ خط‌چینِ خالی یعنی صفر. شمارش‌ها خودکار از داده‌های سایت است؛ تنها تصمیم دستی این است که کدام رشتهٔ ویکی و کدام قفسه به کدام حوزه تعلق دارد. شمار ایده‌ها فقط از ۲۵ ایدهٔ واردشده است و «مشکل مردم» رونوشتی از نقشهٔ مشکل‌های پَرِ سیمرغ است. روی هر ردیف بزنید.</p>
<div class="mx">{head}{body}</div>
</section>

<section id="road">
<h2>نقشهٔ راه</h2>
<p class="sub">نُه کار، به ترتیبی که باید پیش بروند. هیچ‌کدام هنوز از بازبینی متخصص نگذشته است.</p>
<ol class="road">{road}</ol>
<div class="go"><a href="../sakht/">ساخت ایران ←</a><a href="../sakht/work.html">میز کار متخصص‌ها ←</a><a href="story.html">داستان پروژه ←</a><a href="collection.html">مخزن کتاب‌ها ←</a></div>
</section>
</main>
<footer class="f"><div class="wrap"><a href="../">دانش‌سرا</a><a href="./">اطلس‌ها</a><a href="sitemap.html">نقشهٔ سایت</a></div></footer>
</body>
</html>
'''
open('atlas/coverage.html', 'w', encoding='utf-8').write(page)
print(f'atlas/coverage.html: {len(rows)} domains, no-science {nosci}, no-iran {noiran}, full {full}, totals {tot}')
