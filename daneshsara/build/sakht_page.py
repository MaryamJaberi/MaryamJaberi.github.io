# -*- coding: utf-8 -*-
"""لایهٔ ۴ «ساخت ایران» — نهادهای ضروری، دوران گذار، دفتر ریسک، زیرساخت دیجیتال، ایده‌ها.
Reads data/sakht/sakht.json, writes sakht/index.html:  python3 build/sakht_page.py"""
import os, json, html
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.chdir(R)
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
D = json.load(open('data/sakht/sakht.json', encoding='utf-8'))
SRC = D['sources']
order = list(SRC)
used = []

def refs(keys):
    out = []
    for k in keys:
        assert k in SRC, k
        if k not in used: used.append(k)
        out.append(f'<a class="ref" href="#s-{k}" title="{E(SRC[k]["cite"])}">{fa(used.index(k) + 1)}</a>')
    return '<span class="refs">' + ''.join(out) + '</span>'

LV = {'کم': 1, 'متوسط': 2, 'زیاد': 3, 'بسیار زیاد': 4, 'فاجعه‌بار': 5}
def pill(v): return f'<span class="lv l{LV[v]}">{E(v)}</span>'

organs = ''.join(f'<article class="card"><h3>{E(o["k"])}</h3><p class="what">{E(o["what"])}</p><p>{E(o["why"])} {refs(o["src"])}</p></article>' for o in D['organs'])
trans = ''.join(f'<article class="step"><h3><i>{fa(i)}</i>{E(t["k"])}{" <span class=flag>" + E(t["flag"]) + "</span>" if t.get("flag") else ""}</h3><p>{E(t["body"])} {refs(t["src"])}</p></article>' for i, t in enumerate(D['transition'], 1))
risks_sorted = sorted(D['risks'], key=lambda r: -(LV[r['p']] * LV[r['s']]))
risks = ''.join(f'''<details class="risk"><summary><b>{E(r["k"])}</b><span class="meta">احتمال {pill(r["p"])} شدت {pill(r["s"])}<em>{E(r["speed"])}</em></span></summary>
<dl><dt>نشانه‌های هشدار</dt><dd>{E(r["signs"])}</dd><dt>پیشگیری</dt><dd>{E(r["prevent"])}</dd><dt>واکنش سریع</dt><dd>{E(r["respond"])} {refs(r["src"])}</dd></dl></details>''' for r in risks_sorted)
digital = ''.join(f'<article class="card"><h3>{E(d["k"])}</h3><p>{E(d["body"])} {refs(d["src"])}</p><p class="now"><b>از امروز شدنی:</b> {E(d["now"])}</p></article>' for d in D['digital'])
ideas_sorted = sorted(D['ideas'], key=lambda x: -x['v'])
ideas = ''.join(f'<tr><td dir="auto">{E(x["t"])}</td><td>{E(x["c"])}</td><td class="n">{fa(x["v"])}</td><td class="n">{fa(x["m"])}</td></tr>' for x in ideas_sorted)
srcs = ''.join(f'<li id="s-{k}"><span class="tier t{SRC[k]["tier"]}">ردهٔ {fa(SRC[k]["tier"])}</span> {E(SRC[k]["cite"])}{"، " + fa(SRC[k]["year"]) if SRC[k].get("year") else ""}{f""" <a href="{E(SRC[k]["url"])}" rel="noopener">پیوند</a>""" if SRC[k].get("url") else ""}</li>' for k in used)

page = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>ساخت ایران | دانش‌سرا</title>
<meta name="description" content="لایهٔ چهارم دانش‌سرا: برای کشورداری چه نهادهایی ضروری است، دوران گذار چه می‌خواهد، چه خطرهایی در راه است و برای هر کدام چه باید کرد. با منبع.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
:root{{--c:#2f6b3a}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--c:#7fc08a}}}}
:root[data-theme="dark"]{{--c:#7fc08a}}
h1{{font-size:var(--h1);margin:var(--s8) 0 var(--s4);line-height:var(--lh-tight);max-width:20ch;text-wrap:balance}}
p.lead{{color:var(--ink-2);max-width:47em;line-height:2;margin:0 0 var(--s5);font-size:1.05rem}}
.toc{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:var(--s6)}}
.toc a{{font-size:var(--small);padding:5px 14px;border:1px solid var(--line-strong);border-radius:var(--r-full);color:var(--ink-2);text-decoration:none}}
.toc a:hover{{border-color:var(--c);color:var(--ink)}}
section{{padding-block:var(--s6);border-top:1px solid var(--line)}}
h2{{font-size:var(--h3);margin:0 0 var(--s2)}}h2 b{{color:var(--c)}}
p.sub{{color:var(--ink-3);font-size:var(--small);line-height:1.9;margin:0 0 var(--s4);max-width:46em}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:var(--s4)}}
.card{{padding:var(--s4) var(--s5);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--paper);border-top:3px solid var(--c);min-width:0}}
.card h3,.step h3{{margin:0 0 var(--s2);font-size:var(--h4)}}
.card p,.step p{{margin:0 0 var(--s2);color:var(--ink-2);line-height:1.95;font-size:var(--small)}}
.card p.what{{color:var(--ink);font-weight:550}}
.card p.now{{border-top:1px dashed var(--line-strong);padding-top:var(--s2);margin-bottom:0}}
.steps{{display:grid;gap:var(--s4);max-width:52em}}
.step{{padding-inline-start:var(--s5);border-inline-start:2px solid var(--c)}}
.step h3 i{{font-style:normal;display:inline-grid;place-items:center;width:1.7em;height:1.7em;border-radius:50%;background:var(--c);color:var(--paper);font-size:.8em;margin-inline-end:8px}}
.flag{{font-size:var(--chip);font-weight:500;padding:1px 9px;border-radius:var(--r-full);border:1px solid #b7791f;color:#b7791f;margin-inline-start:6px}}
.refs{{white-space:nowrap}}.ref{{font-size:.72em;vertical-align:super;margin-inline-start:2px;color:var(--c);text-decoration:none;padding:0 3px;border:1px solid currentColor;border-radius:4px}}
.note{{padding:var(--s3) var(--s4);border-radius:var(--r-md);background:color-mix(in srgb,#b7791f 9%,var(--paper));border:1px solid color-mix(in srgb,#b7791f 40%,var(--line));font-size:var(--small);line-height:1.9;color:var(--ink-2);max-width:52em;margin:0 0 var(--s4)}}
.risk{{border:1px solid var(--line);border-radius:var(--r-md);background:var(--paper);margin-bottom:8px;max-width:60em}}
.risk summary{{cursor:pointer;padding:var(--s3) var(--s4);display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;list-style:none}}
.risk summary::-webkit-details-marker{{display:none}}
.risk summary b{{flex:1 1 16em}}
.risk .meta{{font-size:var(--chip);color:var(--ink-3);display:flex;gap:6px;align-items:center;flex-wrap:wrap}}
.risk .meta em{{font-style:normal;margin-inline-start:6px}}
.lv{{padding:1px 9px;border-radius:var(--r-full);color:#fff;font-weight:600}}
.l1{{background:#5f7d6a}}.l2{{background:#a8811f}}.l3{{background:#c2621b}}.l4{{background:#b3261e}}.l5{{background:#6d0f1f}}
.risk dl{{margin:0;padding:0 var(--s4) var(--s4);display:grid;gap:4px}}
.risk dt{{font-weight:650;font-size:var(--small);margin-top:var(--s2)}}
.risk dd{{margin:0;color:var(--ink-2);font-size:var(--small);line-height:1.9}}
.tw{{overflow-x:auto;max-width:100%}}
table{{border-collapse:collapse;width:100%;font-size:var(--small);min-width:520px}}
th,td{{text-align:start;padding:7px 10px;border-bottom:1px solid var(--line)}}
th{{color:var(--ink-3);font-weight:500;font-size:var(--chip)}}td.n{{font-variant-numeric:tabular-nums;white-space:nowrap}}
ol.src{{padding-inline-start:1.4em;display:grid;gap:8px;font-size:var(--small);color:var(--ink-2);line-height:1.8;max-width:60em}}
ol.src li:target{{background:color-mix(in srgb,var(--c) 14%,transparent)}}
.tier{{font-size:var(--chip);padding:0 8px;border-radius:var(--r-full);border:1px solid var(--line-strong);margin-inline-end:6px;white-space:nowrap}}
.tier.t4{{border-color:#b7791f;color:#b7791f}}
footer.f{{border-top:1px solid var(--line);padding-block:var(--s5);font-size:var(--small);color:var(--ink-3)}}
footer.f a{{color:var(--ink-2);margin-inline-end:var(--s4)}}
</style>
</head>
<body>
<main class="wrap">
<h1>ساخت ایران: کشور را چه چیزی سر پا نگه می‌دارد</h1>
<p class="lead">سه لایهٔ پایین می‌پرسند آدم و جامعه چطور کار می‌کنند، ایران کجا ایستاده و راه نجات چیست. این لایه می‌پرسد روز بعد چه باید آماده باشد: کدام نهادها ضروری‌اند، دوران گذار چه می‌خواهد، چه خطرهایی در راه است و چه چیزی را می‌شود از همین امروز ساخت. همه‌چیز بر پایهٔ تجربهٔ مستند کشورهای دیگر است، نه آرزو.</p>
<nav class="toc"><a href="#organs">نهادهای ضروری</a><a href="#transition">دوران گذار</a><a href="#risks">دفتر ریسک</a><a href="#digital">زیرساخت دیجیتال</a><a href="#ideas">ایده‌ها</a><a href="#sources">منابع</a></nav>

<section id="organs">
<h2><b>۱</b> · نهادهای ضروری</h2>
<p class="sub">هفت کارکردی که هر دولتی، با هر شکل حکومت، باید از عهده‌اش برآید. ترتیب تقریباً ترتیب فوریت است.</p>
<div class="cards">{organs}</div>
</section>

<section id="transition">
<h2><b>۲</b> · دوران گذار</h2>
<p class="sub">هشت درس از گذارهای موفق و ناموفق. جایی که پژوهشگران هم‌نظر نیستند، همان‌جا نوشته شده.</p>
<div class="steps">{trans}</div>
</section>

<section id="risks">
<h2><b>۳</b> · دفتر ریسک</h2>
<p class="note">{E(D["risk_note"])}</p>
<p class="sub">{fa(len(D["risks"]))} خطر، مرتب‌شده بر پایهٔ احتمال × شدت. روی هر کدام بزنید تا نشانه‌های هشدار، پیشگیری و واکنش سریع را ببینید.</p>
{risks}
</section>

<section id="digital">
<h2><b>۴</b> · زیرساخت دیجیتال</h2>
<p class="sub">چیزهایی که صدورشان به دولت نیاز دارد ولی طراحی‌شان نه.</p>
<div class="cards">{digital}</div>
</section>

<section id="ideas">
<h2><b>۵</b> · ایده‌ها</h2>
<p class="note">{E(D["ideas_note"])} {refs(["iaa"])}</p>
<div class="tw"><table><thead><tr><th>ایده</th><th>دسته</th><th>رأی</th><th>نظر</th></tr></thead><tbody>{ideas}</tbody></table></div>
</section>

<section id="sources">
<h2>منابع</h2>
<p class="sub">ردهٔ ۲ یعنی گزارش رسمی یا مقالهٔ داوری‌شده، ۳ کتاب یا منبع تخصصی، ۴ سرنخ و ایدهٔ بررسی‌نشده.</p>
<ol class="src">{srcs}</ol>
</section>
</main>
<footer class="f"><div class="wrap"><a href="../">دانش‌سرا</a><a href="../iran/">ویکی ایران</a><a href="../simorgh/">سیمرغ</a><a href="../atlas/sitemap.html">نقشهٔ سایت</a></div></footer>
</body>
</html>
'''
open('sakht/index.html', 'w', encoding='utf-8').write(page)
print(f'sakht/index.html: {len(D["organs"])} organs, {len(D["transition"])} transition, {len(D["risks"])} risks, {len(D["ideas"])} ideas, {len(used)}/{len(SRC)} sources used')
