# -*- coding: utf-8 -*-
"""«روز بعد» — چه کسی، چه زمانی، چه کاری. Reads data/sakht/day.json (+ sources from sakht.json), writes sakht/day.html."""
import os, json, html
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.chdir(R)
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
D = json.load(open('data/sakht/day.json', encoding='utf-8'))
SRC = json.load(open('data/sakht/sakht.json', encoding='utf-8'))['sources']
used = []
def refs(keys):
    out = []
    for k in keys:
        assert k in SRC, k
        if k not in used: used.append(k)
        out.append(f'<a class="ref" href="#s-{k}">{fa(used.index(k) + 1)}</a>')
    return ''.join(out)
T = D['times']; ntask = sum(len(c) for l in D['lanes'] for c in l['cells'])
tabs = ''.join(f'<button type="button" data-t="{i}" aria-pressed="{"true" if i == 1 else "false"}">{E(t)}</button>' for i, t in enumerate(T))
head = '<div class="gh"><span></span>' + ''.join(f'<span class="th" data-t="{i}">{E(t)}</span>' for i, t in enumerate(T)) + '</div>'
rows = ''.join(f'<div class="ln"><span class="lk"><b>{E(l["k"])}</b><small>{E(l["d"])}</small></span>' + ''.join(f'<ul class="cl" data-t="{i}">' + ''.join(f'<li>{E(x)}</li>' for x in c) + '</ul>' for i, c in enumerate(l['cells'])) + '</div>' for l in D['lanes'])
safety = ''.join(f'<article class="sf"><h3>{E(s["k"])} {refs(s["src"])}</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in s["items"])}</ul></article>' for s in D['safety'])
basis = refs(['iso22319', 'usip09', 'sigir09'])
srcs = ''.join(f'<li id="s-{k}"><span class="tier">ردهٔ {fa(SRC[k]["tier"])}</span> {E(SRC[k]["cite"])}{"، " + fa(SRC[k]["year"]) if SRC[k].get("year") else ""}{f""" <a href="{E(SRC[k]["url"])}" rel="noopener">پیوند ↗</a>""" if SRC[k].get("url") else ""}</li>' for k in used)
page = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>روز بعد | ساخت ایران | دانش‌سرا</title>
<meta name="description" content="فردای گذار چه کسی چه کاری بکند: از شهروند بدون تخصص تا محله، متخصص و دولت موقت، از ساعت‌های اول تا سال اول. با قواعد مراقبت از خود.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
:root{{--c:var(--ok)}}
h1{{font-size:var(--h1);margin:var(--s8) 0 var(--s4);line-height:var(--lh-tight);max-width:20ch;text-wrap:balance}}
p.lead{{color:var(--ink-2);max-width:47em;line-height:2;margin:0 0 var(--s5);font-size:1.05rem}}
section{{padding-block:var(--s6);border-top:1px solid var(--line)}}
h2{{font-size:var(--h3);margin:0 0 var(--s2)}}
p.sub{{color:var(--ink-3);font-size:var(--small);line-height:1.9;margin:0 0 var(--s4);max-width:48em}}
.note{{padding:var(--s3) var(--s4);border-radius:var(--r-md);background:color-mix(in srgb,var(--warn) 9%,var(--paper));border:1px solid color-mix(in srgb,var(--warn) 40%,var(--line));font-size:var(--small);line-height:1.9;color:var(--ink-2);max-width:60em;margin:0 0 var(--s4)}}
.ref{{font-size:.72em;vertical-align:super;margin-inline-start:2px;color:var(--c);text-decoration:none;padding:0 4px;border:1px solid currentColor;border-radius:4px}}
.tabs{{display:none;flex-wrap:wrap;gap:6px;margin-bottom:var(--s3)}}
.tabs button{{font:inherit;font-size:var(--small);padding:5px 13px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--surface);color:var(--ink-2);cursor:pointer}}
.tabs button[aria-pressed="true"]{{background:var(--c);border-color:var(--c);color:var(--paper)}}
.gh,.ln{{display:grid;grid-template-columns:minmax(0,.8fr) repeat(5,minmax(0,1fr));gap:6px}}
.gh{{margin-bottom:6px}}
.th{{text-align:center;font-size:var(--small);font-weight:650;padding:7px 4px;border-radius:var(--r-sm);background:color-mix(in srgb,var(--c) calc(12% + var(--i) * 14%),var(--surface));}}
.th[data-t="0"]{{--i:0;background:none;border:1px dashed var(--c)}}.th[data-t="1"]{{--i:4;color:var(--paper);background:var(--c)}}.th[data-t="2"]{{--i:2.4}}.th[data-t="3"]{{--i:1.4}}.th[data-t="4"]{{--i:.5}}
.ln{{padding:8px 0;border-top:1px solid var(--line)}}
.lk{{display:grid;align-content:start;gap:2px}}.lk b{{font-size:var(--small)}}.lk small{{font-size:var(--chip);color:var(--ink-3)}}
.cl{{list-style:none;margin:0;padding:0;display:grid;gap:5px;align-content:start}}
.cl li{{font-size:var(--chip);line-height:1.7;padding:6px 9px;border-radius:var(--r-sm);background:var(--surface);border:1px solid var(--line);border-inline-start:3px solid var(--c);color:var(--ink-2)}}
.cl[data-t="0"] li{{border-inline-start-style:dashed}}
@media (max-width:860px){{.tabs{{display:flex}}.gh{{display:none}}.ln{{grid-template-columns:minmax(0,1fr)}}.js .cl:not(.on){{display:none}}.cl li{{font-size:var(--small)}}}}
.sfs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:var(--s3)}}
.sf{{padding:var(--s4) var(--s5);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);border-top:3px solid var(--warn)}}
.sf h3{{margin:0 0 var(--s2);font-size:var(--h4)}}.sf ul{{margin:0;padding-inline-start:1.2em;display:grid;gap:6px}}
.sf li{{font-size:var(--small);line-height:1.9;color:var(--ink-2)}}
ol.src{{padding-inline-start:1.6em;display:grid;gap:8px;font-size:var(--small);color:var(--ink-2);line-height:1.8;max-width:60em}}
.tier{{font-size:var(--chip);padding:0 8px;border-radius:var(--r-full);border:1px solid var(--line-strong);margin-inline-end:6px;white-space:nowrap}}
.go{{display:flex;flex-wrap:wrap;gap:8px;margin-top:var(--s4)}}
.go a{{font-size:var(--small);padding:4px 13px;border:1px solid var(--line-strong);border-radius:var(--r-full);color:var(--ink-2);text-decoration:none}}
footer.f{{border-top:1px solid var(--line);padding-block:var(--s5);font-size:var(--small);color:var(--ink-3)}}footer.f a{{color:var(--ink-2);margin-inline-end:var(--s4)}}
</style>
</head>
<body>
<main class="wrap">
<h1>روز بعد: چه کسی چه کار کند</h1>
<p class="lead">گذار وقتی آرام می‌گذرد که بیشتر آدم‌ها از پیش بدانند کارشان چیست. اینجا {fa(ntask)} کار هست، از شهروندی که هیچ تخصصی ندارد تا دولت موقت، از همین امروز تا سال اول. یکی را از حالا برای خودتان بردارید.</p>
<p class="note">{E(D["note"])} {basis}</p>

<section id="plan">
<h2>نقشهٔ کارها</h2>
<p class="sub">ستون‌ها زمان‌اند و ردیف‌ها آدم‌ها. ستون خط‌چین کارهایی است که همین حالا و بی‌خطر شدنی است.</p>
<div class="tabs" id="tabs">{tabs}</div>
{head}{rows}
<div class="go"><a href="work.html">متخصص هستید؟ میز کار ←</a><a href="index.html#risks">دفتر ریسک ←</a><a href="index.html#transition">درس‌های دوران گذار ←</a></div>
</section>

<section id="safety">
<h2>مراقبت از خود و دیگران</h2>
<p class="sub">این قواعد از همهٔ کارهای بالا مهم‌ترند.</p>
<div class="sfs">{safety}</div>
</section>

<section id="sources">
<h2>منابع</h2>
<ol class="src">{srcs}</ol>
</section>
</main>
<footer class="f"><div class="wrap"><a href="../">دانش‌سرا</a><a href="index.html">ساخت ایران</a><a href="work.html">میز کار</a></div></footer>
<script>
(() => {{
document.documentElement.classList.add("js");
const set = t => {{ document.querySelectorAll("#tabs button").forEach(b => b.setAttribute("aria-pressed", b.dataset.t == t)); document.querySelectorAll(".cl").forEach(c => c.classList.toggle("on", c.dataset.t == t)); }};
document.getElementById("tabs").addEventListener("click", e => {{ const b = e.target.closest("button"); if (b) set(b.dataset.t); }});
set(1);
}})();
</script>
</body>
</html>
'''
open('sakht/day.html', 'w', encoding='utf-8').write(page)
print(f'sakht/day.html: {len(D["lanes"])} lanes × {len(T)} times, {ntask} tasks, {len(used)} sources')
