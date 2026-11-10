# -*- coding: utf-8 -*-
"""لایهٔ ۴ «ساخت ایران» — نهادهای ضروری، دوران گذار، دفتر ریسک، زیرساخت دیجیتال، ایده‌ها.
Reads data/sakht/sakht.json, writes sakht/index.html:  python3 build/sakht_page.py
Every claim carries numbered refs; every block links to the wiki concepts it leans on."""
import os, json, html, math, collections
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.chdir(R)
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
D = json.load(open('data/sakht/sakht.json', encoding='utf-8'))
SRC = D['sources']
used = []

def refs(keys):
    out = []
    for k in keys:
        assert k in SRC, k
        if k not in used: used.append(k)
        out.append(f'<a class="ref" href="#s-{k}" data-ref="{k}" aria-label="منبع {fa(used.index(k) + 1)}">{fa(used.index(k) + 1)}</a>')
    return '<span class="refs">' + ''.join(out) + '</span>'

# ---- links into the wikis: title comes from the concept itself, so it cannot drift
WN = {'soc': 'جامعه', 'phil': 'فلسفه', 'psy': 'روان', 'tabar': 'تبار', 'tarikh': 'تاریخ', 'iran': 'ایران'}
WV = {'soc': '--fam-soc', 'phil': '--fam-hum', 'psy': '--fam-psy', 'tabar': '--fam-bio', 'tarikh': '--fam-hist', 'iran': '--primary'}
nlinks = collections.Counter()
def wiki(ids):
    if not ids: return ''
    out = []
    for i in ids:
        w, s = i.split(':')
        if w == 'iran':
            t = json.load(open(f'iran/{s}.json', encoding='utf-8'))['question']['fa']
        else:
            t = json.load(open(f'data/{w}/concepts/{s}.json', encoding='utf-8'))['title']['fa']
        short = t if len(t) <= 46 else t[:44].rsplit(' ', 1)[0] + '…'
        nlinks[w] += 1
        out.append(f'<a class="wl" style="--w:var({WV[w]})" href="../{w}/entries.html#{s}" title="{E(t)}"><i>{WN[w]}</i>{E(short)}</a>')
    return '<div class="wls"><span>در ویکی‌ها:</span>' + ''.join(out) + '</div>'

LV = {'کم': 1, 'متوسط': 2, 'زیاد': 3, 'بسیار زیاد': 4, 'فاجعه‌بار': 5}
def pill(v): return f'<span class="lv l{LV[v]}">{E(v)}</span>'

# ---- 1 · wheel of the seven functions (structure, not quantity: a diagram)
N = len(D['organs']); CX = CY = 170; RO, RI = 160, 54
def pt(r, a): return f'{CX + r * math.cos(math.radians(a)):.1f},{CY + r * math.sin(math.radians(a)):.1f}'
wedges = ''
for i, o in enumerate(D['organs']):
    a0 = -90 + i * 360 / N + 1.2; a1 = -90 + (i + 1) * 360 / N - 1.2; am = (a0 + a1) / 2
    tx, ty = [float(v) for v in pt(112, am).split(',')]
    mix = 62 - i * 7
    wedges += (f'<g class="wedge" role="button" tabindex="0" data-i="{i}" aria-label="{E(o["k"])}">'
               f'<path d="M{pt(RO, a0)} A{RO},{RO} 0 0 1 {pt(RO, a1)} L{pt(RI, a1)} A{RI},{RI} 0 0 0 {pt(RI, a0)} Z" style="fill:color-mix(in srgb,var(--c) {mix}%,var(--surface))"/>'
               f'<text x="{tx:.1f}" y="{ty - 9:.1f}" class="wn">{fa(i + 1)}</text><text x="{tx:.1f}" y="{ty + 12:.1f}">{E(o["s"])}</text></g>')
wheel = (f'<svg class="wheel" viewBox="0 0 340 340" role="group" aria-label="هفت کارکرد ضروری دولت">{wedges}'
         f'<circle cx="{CX}" cy="{CY}" r="{RI - 6}" class="hub"/><text x="{CX}" y="{CY - 3}" class="hubt">دولتِ</text><text x="{CX}" y="{CY + 16}" class="hubt">کارآمد</text></svg>')
organs = ''.join(f'<article class="org" data-i="{i}"><h3><i>{fa(i + 1)}</i>{E(o["k"])}</h3><p class="what">{E(o["what"])}</p><p>{E(o["why"])} {refs(o["src"])}</p>{wiki(o["wiki"])}</article>' for i, o in enumerate(D['organs']))

# ---- 2 · transition lessons on an editorial time frame (gantt)
PH = D['phases']
phead = ''.join(f'<span>{E(p)}</span>' for p in PH)
trans = ''.join(f'''<details class="tl"{" open" if i == 1 else ""}><summary><span class="tk"><i>{fa(i)}</i>{E(t["k"])}{" <span class=flag>" + E(t["flag"]) + "</span>" if t.get("flag") else ""}</span>
<span class="track" aria-hidden="true"><b style="grid-column:{t["from"] + 1}/{t["to"] + 2}"></b></span></summary>
<div class="tb"><p>{E(t["body"])} {refs(t["src"])}</p>{wiki(t["wiki"])}</div></details>''' for i, t in enumerate(D['transition'], 1))

# ---- 3 · risk matrix (editor's estimate, said so in the graphic) + register
risks_sorted = sorted(D['risks'], key=lambda r: -(LV[r['p']] * LV[r['s']]))
PX = ['کم', 'متوسط', 'زیاد']; SY = ['فاجعه‌بار', 'بسیار زیاد', 'زیاد', 'متوسط']
cells = ''
for sy in SY:
    for px in PX:
        score = LV[px] * LV[sy]
        dots = ''.join(f'<button class="dot{" sud" if "ناگهانی" in r["speed"] else ""}" data-r="{n}" title="{E(r["k"])}" aria-label="{E(r["k"])}">{fa(n)}</button>'
                       for n, r in enumerate(risks_sorted, 1) if r['p'] == px and r['s'] == sy)
        cells += f'<span class="cell" style="background:color-mix(in srgb,var(--err) {score * 4}%,var(--surface))">{dots}</span>'
    cells += f'<span class="yl">{sy}</span>'
cells += ''.join(f'<span class="xl">{p}</span>' for p in PX) + '<span class="xl">↑ شدت</span>'
matrix = f'<div class="mx" dir="ltr"><div class="mxg">{cells}</div><div class="mxx">احتمال →</div></div>'
risks = ''.join(f'''<details class="risk" id="r{n}"><summary><i class="rn">{fa(n)}</i><b>{E(r["k"])}</b><span class="meta">احتمال {pill(r["p"])} شدت {pill(r["s"])}<em>{E(r["speed"])}</em></span></summary>
<div class="r3"><div><h4>نشانه‌های هشدار</h4><p>{E(r["signs"])}</p></div><div><h4>پیشگیری</h4><p>{E(r["prevent"])}</p></div><div><h4>واکنش سریع</h4><p>{E(r["respond"])} {refs(r["src"])}</p></div></div>{wiki(r["wiki"])}</details>''' for n, r in enumerate(risks_sorted, 1))

# ---- legacy: what to keep, retrain, replace, sort (editor's frame, said so on the page)
QN = [('keep', 'نگه‌دار تا جایگزین برسد', 'کار می‌کند؛ کنار گذاشتن یک‌شبه خلأ می‌سازد'), ('retrain', 'بازآموزی و راه بازگشت', 'آدم‌ها؛ رسیدگی فرد به فرد'),
      ('replace', 'جایگزینی تدریجی', 'دارایی مردم است؛ با هدف ایمنی و آلودگی'), ('triage', 'اول دسته‌بندی، بعد تصمیم', 'ماندنی، اصلاح‌شدنی، بستنی')]
quad = ''.join(f'<div class="qd q-{q}"><b>{t}</b><small>{d}</small>' + ''.join(f'<a href="#lg{i}">{E(x["k"])}</a>' for i, x in enumerate(D['legacy']) if x['q'] == q) + '</div>' for q, t, d in QN)
legacy = ''.join(f'<article class="card" id="lg{i}"><h3>{E(x["k"])}{" <span class=flag>" + E(x["flag"]) + "</span>" if x.get("flag") else ""}</h3><p class="what">{E(x["ex"])}</p><p>{E(x["body"])} {refs(x["src"])}</p>{wiki(x["wiki"])}</article>' for i, x in enumerate(D['legacy']))

# ---- 4 · digital: schematic of the data-exchange pattern
inst = ['ثبت احوال', 'مالیات', 'سلامت', 'بانک', 'شهرداری']
arch = f'''<figure class="arch"><div class="a1">شهروند</div><div class="ar">↓ یک ورود برای همهٔ خدمات</div>
<div class="a2">هویت دیجیتال</div><div class="ar">↓</div>
<div class="a3">لایهٔ امن تبادل داده<small>هر دسترسی ثبت می‌شود و شهروند می‌تواند ببیند چه کسی داده‌اش را دیده</small></div><div class="ar">↓ ↑</div>
<div class="a4">{''.join(f'<span>{x}</span>' for x in inst)}</div>
<figcaption>طرح‌واره، نه نقشهٔ اجرایی: هر داده فقط نزد نهاد مسئولش می‌ماند و پایگاه دادهٔ مرکزی وجود ندارد. الگو از X-Road استونی. {refs(["xroad"])}</figcaption></figure>'''
digital = ''.join(f'<article class="card"><h3>{E(d["k"])}</h3><p>{E(d["body"])} {refs(d["src"])}</p><p class="now"><b>از امروز شدنی:</b> {E(d["now"])}</p>{wiki(d["wiki"])}</article>' for d in D['digital'])

# ---- 5 · ideas: votes as bars, categories as counts
ideas_sorted = sorted(D['ideas'], key=lambda x: -x['v']); vmax = max(x['v'] for x in ideas_sorted)
bars = ''.join(f'<li><span class="it" dir="auto">{E(x["t"])}</span><span class="ic">{E(x["c"])}</span><span class="ib"><b style="width:{max(x["v"] / vmax * 100, 1.5):.1f}%"></b></span><span class="iv">{fa(x["v"])}</span></li>' for x in ideas_sorted)
cats = collections.Counter(x['c'] for x in D['ideas'])
catchips = ''.join(f'<span class="chip">{E(c)} <b>{fa(n)}</b></span>' for c, n in cats.most_common())

srcs = ''.join(f'<li id="s-{k}"><span class="tier t{SRC[k]["tier"]}">ردهٔ {fa(SRC[k]["tier"])}</span> {E(SRC[k]["cite"])}{"، " + fa(SRC[k]["year"]) if SRC[k].get("year") else ""}{f""" <a href="{E(SRC[k]["url"])}" rel="noopener">پیوند ↗</a>""" if SRC[k].get("url") else ""}</li>' for k in used)
SRCJS = json.dumps({k: {'n': fa(used.index(k) + 1), 'c': SRC[k]['cite'] + ('، ' + fa(SRC[k]['year']) if SRC[k].get('year') else ''), 't': fa(SRC[k]['tier']), 'u': SRC[k].get('url', '')} for k in used}, ensure_ascii=False)
total_links = sum(nlinks.values())
linkchips = ''.join(f'<a class="wl" style="--w:var({WV[w]})" href="../{w}/"><i>{WN[w]}</i>{fa(n)} پیوند</a>' for w, n in nlinks.most_common())

page = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>ساخت ایران | دانش‌سرا</title>
<meta name="description" content="لایهٔ چهارم دانش‌سرا: برای کشورداری چه نهادهایی ضروری است، دوران گذار چه می‌خواهد، چه خطرهایی در راه است و برای هر کدام چه باید کرد. با منبع.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
:root{{--c:var(--ok)}}
h1{{font-size:var(--h1);margin:var(--s8) 0 var(--s4);line-height:var(--lh-tight);max-width:20ch;text-wrap:balance}}
p.lead{{color:var(--ink-2);max-width:47em;line-height:2;margin:0 0 var(--s5);font-size:1.05rem}}
.cta{{margin:0 0 var(--s4)}}.cta a.g2{{background:none;color:var(--c);border:1px solid var(--c)}}
.cta a{{display:inline-block;padding:9px 20px;border-radius:var(--r-full);background:var(--c);color:var(--paper);text-decoration:none;font-weight:650}}
.glance{{display:flex;flex-wrap:wrap;gap:var(--s3);margin:0 0 var(--s5)}}
.glance a{{display:grid;min-width:104px;padding:var(--s3) var(--s4);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);text-decoration:none;color:inherit;border-top:3px solid var(--c)}}
.glance a:hover{{border-color:var(--c)}}
.glance b{{font-size:1.7rem;line-height:1.15;color:var(--ink)}}.glance span{{font-size:var(--chip);color:var(--ink-3)}}
section{{padding-block:var(--s6);border-top:1px solid var(--line);scroll-margin-top:8px}}
h2{{font-size:var(--h3);margin:0 0 var(--s2)}}h2 b{{color:var(--c)}}
p.sub{{color:var(--ink-3);font-size:var(--small);line-height:1.9;margin:0 0 var(--s4);max-width:46em}}
.refs{{white-space:nowrap}}.ref{{font-size:.72em;vertical-align:super;margin-inline-start:2px;color:var(--c);text-decoration:none;padding:0 4px;border:1px solid currentColor;border-radius:4px;cursor:pointer}}
.wls{{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:var(--s3)}}
.wls>span{{font-size:var(--chip);color:var(--ink-3)}}
.wl{{display:inline-flex;align-items:center;gap:6px;font-size:var(--chip);padding:2px 10px 2px 3px;border-radius:var(--r-full);border:1px solid color-mix(in srgb,var(--w) 45%,var(--line));color:var(--ink-2);text-decoration:none;background:color-mix(in srgb,var(--w) 7%,var(--surface));max-width:100%}}
.wl:hover{{border-color:var(--w);color:var(--ink)}}
.wl i{{font-style:normal;font-weight:650;color:var(--paper);background:var(--w);border-radius:var(--r-full);padding:0 8px;white-space:nowrap}}
/* wheel */
.orgw{{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:var(--s6);align-items:center}}
@media (max-width:760px){{.orgw{{grid-template-columns:minmax(0,1fr)}}.wheel{{max-width:300px;margin-inline:auto}}}}
.wheel{{width:100%;height:auto;display:block}}
.wheel text{{text-anchor:middle;font:600 13.5px inherit;fill:var(--ink);pointer-events:none}}
.wheel .wn{{font-size:11px;font-weight:500;fill:var(--ink-2)}}
.wedge{{cursor:pointer;outline:none}}.wedge path{{stroke:var(--paper);stroke-width:2;transition:transform .15s;transform-origin:170px 170px}}
.wedge:hover path,.wedge:focus-visible path{{transform:scale(1.03)}}
.wedge.on path{{stroke:var(--ink);stroke-width:2.5;transform:scale(1.045)}}
.hub{{fill:var(--paper);stroke:var(--c);stroke-width:2}}.wheel .hubt{{font-size:13px;fill:var(--c)}}
.org{{padding:var(--s4) var(--s5);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);border-inline-start:4px solid var(--c);min-width:0}}
.js .org:not(.on){{display:none}}.org+.org{{margin-top:var(--s3)}}
.org h3,.card h3{{margin:0 0 var(--s2);font-size:var(--h4)}}
.org h3 i,.tk i,.rn{{font-style:normal;display:inline-grid;place-items:center;min-width:1.7em;height:1.7em;border-radius:50%;background:var(--c);color:var(--paper);font-size:.8em;margin-inline-end:8px;font-weight:600}}
.org p,.card p,.tb p{{margin:0 0 var(--s2);color:var(--ink-2);line-height:1.95;font-size:var(--small)}}
.org p.what{{color:var(--ink);font-weight:550}}
.hint{{font-size:var(--chip);color:var(--ink-3);text-align:center;margin:var(--s2) 0 0}}
/* gantt */
.gh,.track{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:3px}}
.gh{{font-size:var(--chip);color:var(--ink-3);margin-bottom:6px;text-align:center}}
.gh span{{padding:4px 2px;border-bottom:2px solid var(--line-strong);line-height:1.4}}
.gantt{{max-width:60em}}
.tl{{border-bottom:1px solid var(--line)}}
.tl summary{{cursor:pointer;list-style:none;padding:9px 0;display:grid;gap:6px}}.tl summary::-webkit-details-marker{{display:none}}
.tk{{font-weight:600;font-size:var(--small)}}.tk::after{{content:" ＋";color:var(--ink-3);font-weight:400}}.tl[open] .tk::after{{content:" −"}}
.track{{height:10px;background:repeating-linear-gradient(to left,transparent 0 calc(25% - 1px),var(--line) calc(25% - 1px) 25%)}}
.track b{{background:var(--c);border-radius:5px;opacity:.75}}.tl[open] .track b{{opacity:1}}
.tb{{padding:0 0 var(--s4)}}
.flag{{font-size:var(--chip);font-weight:500;padding:1px 9px;border-radius:var(--r-full);border:1px solid var(--warn);color:var(--warn);margin-inline-start:6px}}
.note{{padding:var(--s3) var(--s4);border-radius:var(--r-md);background:color-mix(in srgb,var(--warn) 9%,var(--paper));border:1px solid color-mix(in srgb,var(--warn) 40%,var(--line));font-size:var(--small);line-height:1.9;color:var(--ink-2);max-width:60em;margin:0 0 var(--s4)}}
/* matrix */
.rw{{display:grid;grid-template-columns:minmax(0,400px) minmax(0,1fr);gap:var(--s6);align-items:start}}
@media (max-width:900px){{.rw{{grid-template-columns:minmax(0,1fr)}}}}
.mx{{position:sticky;top:8px}}@media (max-width:900px){{.mx{{position:static}}}}
.mxg{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) auto;gap:4px}}
.cell{{min-height:74px;border-radius:var(--r-sm);display:flex;flex-wrap:wrap;gap:5px;align-content:center;justify-content:center;padding:6px;border:1px solid var(--line)}}
.yl,.xl{{font-size:var(--chip);color:var(--ink-3);display:grid;place-items:center;padding:2px 6px;direction:rtl}}
.mxx{{text-align:center;font-size:var(--chip);color:var(--ink-3);margin-top:2px}}
.dot{{width:30px;height:30px;border-radius:50%;border:2px solid var(--ink);background:var(--surface);color:var(--ink);font:600 .8rem inherit;cursor:pointer;padding:0}}
.dot.sud{{background:var(--ink);color:var(--paper)}}.dot:hover,.dot.on{{outline:3px solid var(--c);outline-offset:1px}}
.leg{{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:var(--chip);color:var(--ink-3);margin-top:var(--s3);direction:rtl}}
.leg i{{display:inline-block;width:12px;height:12px;border-radius:50%;border:2px solid var(--ink);vertical-align:-2px;margin-inline-end:4px}}.leg i.f{{background:var(--ink)}}
.risk{{border:1px solid var(--line);border-radius:var(--r-md);background:var(--surface);margin-bottom:8px;scroll-margin-top:12px}}
.risk[open]{{border-color:var(--c)}}
.risk summary{{cursor:pointer;padding:var(--s3) var(--s4);display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;list-style:none}}
.risk summary::-webkit-details-marker{{display:none}}
.risk summary b{{flex:1 1 12em;font-size:var(--small)}}.rn{{background:var(--ink)!important;margin:0!important}}
.risk .meta{{font-size:var(--chip);color:var(--ink-3);display:flex;gap:6px;align-items:center;flex-wrap:wrap}}
.risk .meta em{{font-style:normal}}
.lv{{padding:1px 9px;border-radius:var(--r-full);font-weight:600;border:1px solid var(--line-strong);color:var(--ink)}}
.l1{{background:color-mix(in srgb,var(--err) 6%,var(--surface))}}.l2{{background:color-mix(in srgb,var(--err) 16%,var(--surface))}}.l3{{background:color-mix(in srgb,var(--err) 30%,var(--surface))}}.l4{{background:color-mix(in srgb,var(--err) 48%,var(--surface))}}.l5{{background:var(--err);color:var(--paper)}}
.r3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,170px),1fr));gap:var(--s3);padding:0 var(--s4) var(--s3)}}
.r3 h4{{margin:0 0 2px;font-size:var(--chip);color:var(--c)}}.r3 p{{margin:0;font-size:var(--small);line-height:1.85;color:var(--ink-2)}}
.risk .wls{{padding:0 var(--s4) var(--s4);margin:0}}
/* digital */
.dw{{display:grid;grid-template-columns:minmax(0,360px) minmax(0,1fr);gap:var(--s6);align-items:start}}
@media (max-width:900px){{.dw{{grid-template-columns:minmax(0,1fr)}}}}
.arch{{margin:0;display:grid;gap:4px;text-align:center;font-size:var(--small)}}
.arch>div{{border-radius:var(--r-md);padding:9px 10px}}
.a1{{border:1px dashed var(--line-strong);justify-self:center;padding-inline:28px!important}}
.a2{{background:var(--c);color:var(--paper);font-weight:650}}
.a3{{border:2px solid var(--c);font-weight:650}}.a3 small{{display:block;font-weight:400;color:var(--ink-3);font-size:var(--chip);line-height:1.6;margin-top:2px}}
.a4{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;padding:0!important}}
.a4 span{{border:1px solid var(--line-strong);border-radius:var(--r-sm);padding:10px 2px;font-size:var(--chip);background:var(--surface)}}
.ar{{color:var(--ink-3);font-size:var(--chip);padding:0!important}}
.arch figcaption{{font-size:var(--chip);color:var(--ink-3);line-height:1.8;text-align:start;margin-top:var(--s2)}}
.cards{{display:grid;gap:var(--s3)}}.cards.two{{grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr))}}.card p.what{{color:var(--ink);font-weight:550}}.card:target{{border-color:var(--c);box-shadow:0 0 0 2px var(--c)}}
.quad{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;max-width:44em;margin-bottom:var(--s4)}}
.qd{{padding:var(--s3) var(--s4);border-radius:var(--r-md);border:1px solid var(--line-strong);display:grid;gap:4px;align-content:start;min-height:108px;background:var(--surface)}}
.qd b{{font-size:var(--small)}}.qd small{{font-size:var(--chip);color:var(--ink-3);line-height:1.6}}
.qd a{{justify-self:start;font-size:var(--chip);padding:2px 11px;border-radius:var(--r-full);background:var(--c);color:var(--paper);text-decoration:none;margin-top:2px}}
.q-keep{{border-top:3px solid var(--ok)}}.q-retrain{{border-top:3px solid var(--primary)}}.q-replace{{border-top:3px solid var(--warn)}}.q-triage{{border-top:3px solid var(--err)}}
.card{{padding:var(--s4) var(--s5);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);min-width:0}}
.card p.now{{border-top:1px dashed var(--line-strong);padding-top:var(--s2);margin-bottom:0}}
/* ideas */
.cats{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:var(--s4)}}
ol.ideas{{list-style:none;margin:0;padding:0;display:grid;gap:7px;max-width:60em}}
ol.ideas li{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 10px;align-items:center}}
.it{{font-size:var(--small);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.ic{{font-size:var(--chip);color:var(--ink-3)}}
.ib{{height:9px;background:var(--surface-subtle);border-radius:5px;overflow:hidden;display:flex}}.ib b{{background:var(--c);border-radius:5px}}
.iv{{font-size:var(--chip);font-variant-numeric:tabular-nums;color:var(--ink-2);min-width:2ch;text-align:end}}
ol.src{{padding-inline-start:1.6em;display:grid;gap:8px;font-size:var(--small);color:var(--ink-2);line-height:1.8;max-width:60em}}
ol.src li:target{{background:color-mix(in srgb,var(--c) 14%,transparent)}}
.tier{{font-size:var(--chip);padding:0 8px;border-radius:var(--r-full);border:1px solid var(--line-strong);margin-inline-end:6px;white-space:nowrap}}
.tier.t4{{border-color:var(--warn);color:var(--warn)}}
#sheet{{position:fixed;inset:auto 0 0 0;z-index:20;background:var(--surface);border-top:2px solid var(--c);box-shadow:var(--shadow-lg);padding:var(--s3) max(16px,env(safe-area-inset-left,0px)) calc(var(--s3) + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-right,0px));font-size:var(--small);line-height:1.8;display:flex;gap:var(--s3);align-items:flex-start}}
#sheet[hidden]{{display:none}}
#sheet p{{margin:0;flex:1;min-width:0;color:var(--ink-2)}}#sheet b{{color:var(--c)}}
#sheet button{{border:1px solid var(--line-strong);background:none;color:var(--ink-2);border-radius:var(--r-full);padding:2px 12px;cursor:pointer;font:inherit}}
footer.f{{border-top:1px solid var(--line);padding-block:var(--s5) calc(var(--s8) + var(--s5));font-size:var(--small);color:var(--ink-3)}}
footer.f a{{color:var(--ink-2);margin-inline-end:var(--s4)}}
</style>
</head>
<body>
<main class="wrap">
<h1>ساخت ایران: کشور را چه چیزی سر پا نگه می‌دارد</h1>
<p class="lead">سه لایهٔ پایین می‌پرسند آدم و جامعه چطور کار می‌کنند، ایران کجا ایستاده و راه نجات چیست. این لایه می‌پرسد روز بعد چه باید آماده باشد. همه‌چیز بر پایهٔ تجربهٔ مستند کشورهای دیگر است، نه آرزو.</p>
<p class="cta"><a href="work.html">متخصص هستید؟ ببینید کجا به شما نیاز داریم ←</a> <a class="g2" href="day.html">روز بعد: چه کسی چه کار کند ←</a> <a class="g2" href="../atlas/coverage.html">نقشهٔ پوشش ۲۰ حوزه ←</a></p>
<nav class="glance" aria-label="بخش‌ها">
<a href="#organs"><b>{fa(len(D["organs"]))}</b><span>کارکرد ضروری</span></a>
<a href="#transition"><b>{fa(len(D["transition"]))}</b><span>درس دوران گذار</span></a>
<a href="#risks"><b>{fa(len(D["risks"]))}</b><span>ریسک</span></a>
<a href="#legacy"><b>{fa(len(D["legacy"]))}</b><span>میراث ناکارآمد</span></a>
<a href="#digital"><b>{fa(len(D["digital"]))}</b><span>زیرساخت دیجیتال</span></a>
<a href="#ideas"><b>{fa(len(D["ideas"]))}</b><span>ایده</span></a>
<a href="#sources"><b>{fa(len(SRC))}</b><span>منبع</span></a>
<a href="#links"><b>{fa(total_links)}</b><span>پیوند به ویکی‌ها</span></a>
</nav>

<section id="organs">
<h2><b>۱</b> · نهادهای ضروری</h2>
<p class="sub">هفت کارکردی که هر دولتی، با هر شکل حکومت، باید از عهده‌اش برآید. شماره و پررنگی هر قطعه ترتیب فوریت را نشان می‌دهد.</p>
<div class="orgw"><div>{wheel}<p class="hint">روی هر قطعه بزنید</p></div><div id="orgs">{organs}</div></div>
</section>

<section id="transition">
<h2><b>۲</b> · دوران گذار</h2>
<p class="sub">هشت درس از گذارهای موفق و ناموفق. نوار سبز نشان می‌دهد هر درس در کدام مرحله به کار می‌آید؛ این چهار مرحله چارچوب ویراستار است و فقط بازهٔ «یک نسل» از منبع آمده. {refs(["wdr11"])}</p>
<div class="gantt"><div class="gh">{phead}</div>{trans}</div>
</section>

<section id="risks">
<h2><b>۳</b> · دفتر ریسک</h2>
<p class="note">{E(D["risk_note"])}</p>
<div class="rw"><div class="mx-w">{matrix}<div class="leg"><span><i class="f"></i>ناگهانی</span><span><i></i>تدریجی یا تصمیمی</span><span>هر چه خانه پررنگ‌تر، احتمال × شدت بیشتر</span></div></div>
<div>{risks}</div></div>
</section>

<section id="legacy">
<h2><b>۴</b> · میراث ناکارآمد</h2>
<p class="sub">مشکل‌های پنهانِ روز بعد: کالا، کارخانه، دستگاه و آدم‌هایی که در نظم قدیم جا افتاده‌اند. نه همه دورریختنی‌اند و نه همه ماندنی.</p>
<p class="note">{E(D["legacy_note"])}</p>
<div class="quad">{quad}</div>
<div class="cards two">{legacy}</div>
</section>

<section id="digital">
<h2><b>۵</b> · زیرساخت دیجیتال</h2>
<p class="sub">چیزهایی که صدورشان به دولت نیاز دارد ولی طراحی‌شان نه.</p>
<div class="dw">{arch}<div class="cards">{digital}</div></div>
</section>

<section id="ideas">
<h2><b>۶</b> · ایده‌ها</h2>
<p class="note">{E(D["ideas_note"])} {refs(["iaa"])}</p>
<div class="cats">{catchips}</div>
<p class="sub">طول هر نوار تعداد رأی در خود مخزن است ({fa(len(D["ideas"]))} ایدهٔ صفحهٔ نخست از حدود ۳۰۰).</p>
<ol class="ideas">{bars}</ol>
</section>

<section id="links">
<h2>پیوند به لایه‌های پایین</h2>
<p class="sub">هر بخش این صفحه به مفهوم‌هایی در ویکی‌ها تکیه دارد. {fa(total_links)} پیوند، به تفکیک ویکی:</p>
<div class="wls">{linkchips}</div>
</section>

<section id="sources">
<h2>منابع</h2>
<p class="sub">ردهٔ ۲ یعنی گزارش رسمی یا مقالهٔ داوری‌شده، ۳ کتاب یا منبع تخصصی، ۴ سرنخ و ایدهٔ بررسی‌نشده. ارجاع‌ها هنوز شمارهٔ صفحه ندارند.</p>
<ol class="src">{srcs}</ol>
</section>
</main>
<div id="sheet" hidden><p></p><button type="button">بستن</button></div>
<footer class="f"><div class="wrap"><a href="../">دانش‌سرا</a><a href="../iran/">ویکی ایران</a><a href="../simorgh/">سیمرغ</a><a href="../atlas/sitemap.html">نقشهٔ سایت</a></div></footer>
<script>
(() => {{
document.documentElement.classList.add("js");
const S = {SRCJS};
const $$ = (q, r = document) => [...r.querySelectorAll(q)];
// wheel
const pick = i => {{ $$(".wedge").forEach(w => w.classList.toggle("on", w.dataset.i == i)); $$(".org").forEach(o => o.classList.toggle("on", o.dataset.i == i)); }};
$$(".wedge").forEach(w => {{ w.addEventListener("click", () => pick(w.dataset.i)); w.addEventListener("keydown", e => {{ if (e.key === "Enter" || e.key === " ") {{ e.preventDefault(); pick(w.dataset.i); }} }}); }});
pick(0);
// matrix -> register
$$(".dot").forEach(d => d.addEventListener("click", () => {{ $$(".dot").forEach(x => x.classList.toggle("on", x === d)); $$(".risk").forEach(r => r.open = false); const r = document.getElementById("r" + d.dataset.r); r.open = true; r.scrollIntoView({{block: "nearest", behavior: "smooth"}}); }}));
// reference sheet
const sh = document.getElementById("sheet");
document.addEventListener("click", e => {{
  const a = e.target.closest("a.ref");
  if (a) {{ e.preventDefault(); const s = S[a.dataset.ref]; const p = sh.querySelector("p"); p.textContent = ""; const b = document.createElement("b"); b.textContent = "منبع " + s.n + " · ردهٔ " + s.t + " — "; p.append(b, s.c + " "); if (s.u) {{ const l = document.createElement("a"); l.href = s.u; l.rel = "noopener"; l.textContent = "پیوند ↗"; p.append(l); }} sh.hidden = false; return; }}
  if (e.target.closest("#sheet button")) sh.hidden = true;
}});
}})();
</script>
</body>
</html>
'''
open('sakht/index.html', 'w', encoding='utf-8').write(page)
print(f'sakht/index.html: {len(D["organs"])} organs, {len(D["transition"])} transition, {len(D["risks"])} risks, {len(D["ideas"])} ideas, {len(used)}/{len(SRC)} sources used, {total_links} wiki links')
