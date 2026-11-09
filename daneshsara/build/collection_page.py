# -*- coding: utf-8 -*-
"""The collection catalogue: every book in the project's shelf, classified: python3 build/collection_page.py
Drive ids stay out of the published page — the site is public, the drive is not."""
import os, json, html, collections
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
C = json.load(open(f'{R}/data/library/collection.json', encoding='utf-8'))
WIKI = {'tarikh': ('تاریخ و ایران‌شناسی', '#8a6d3b', None),
        'phil': ('فلسفه', 'var(--fam-hum)', '../phil/'),
        'soc': ('جامعه', 'var(--fam-soc)', '../soc/'),
        'psy': ('روان‌شناسی', 'var(--fam-psy)', '../psy/'),
        'tabar': ('تبار و ژنتیک', 'var(--fam-bio)', '../tabar/'),
        'miyan': ('علم و میان‌رشته‌ای', 'var(--fam-formal)', '../miyan/'),
        'zaban': ('زبان‌شناسی', '#5b8a7a', None),
        'adab': ('ادبیات', '#9a6a7a', None),
        'marja': ('مرجع', '#6b6b6b', None),
        'other': ('هنر و عمومی', '#6b6b6b', None),
        'unsorted': ('هنوز دسته‌بندی نشده', '#b3261e', None)}
by = collections.defaultdict(list)
for x in C: by[x['wiki']].append(x)
order = sorted(by, key=lambda k: -len(by[k]))
data = {'n': len(C), 'groups': [{'k': k, 'n': WIKI[k][0], 'c': WIKI[k][1], 'u': WIKI[k][2],
        'shelves': [{'s': s, 'b': sorted(t['title'] for t in v)}
                    for s, v in sorted(collections.Counter.__call__ and
                        {s: [t for t in by[k] if t['shelf'] == s] for s in {t['shelf'] for t in by[k]}}.items(),
                        key=lambda x: -len(x[1]))]} for k in order]}
chips = ''.join(f'<button data-k="{E(g["k"])}" style="--c:{g["c"]}">{E(g["n"])}<b>{fa(sum(len(s["b"]) for s in g["shelves"]))}</b></button>' for g in data['groups'])
tpl = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>فهرست کتاب‌ها | اطلس‌ها | دانش‌سرا</title>
<meta name="description" content="فهرست {fa(len(C))} کتاب و سند مجموعهٔ دانش‌سرا، دسته‌بندی‌شده به تفکیک رشته و قفسه. فهرست‌شده از روی عنوان؛ خوانده‌شدن و استخراج محتوا مرحلهٔ بعد است.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
h1{{font-size:var(--h1);margin:var(--s7) 0 var(--s3);line-height:var(--lh-tight)}}
p.lead{{color:var(--ink-2);max-width:47em;line-height:1.95;margin:0 0 var(--s4)}}
.warn{{border:1px solid var(--line-strong);border-inline-start:4px solid #b7791f;border-radius:var(--r-md);padding:12px 16px;margin:0 0 var(--s5);font-size:var(--small);color:var(--ink-2);line-height:1.9;max-width:47em;background:var(--paper)}}
.bar{{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 var(--s4);align-items:center}}
.bar input{{font:inherit;padding:7px 14px;border:1px solid var(--line-strong);border-radius:var(--r-full);background:var(--paper);color:var(--ink);min-width:230px}}
.chips{{display:flex;gap:7px;flex-wrap:wrap;margin:0 0 var(--s5)}}
.chips button{{font:inherit;font-size:var(--small);padding:5px 14px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--paper);color:var(--ink-2);cursor:pointer;display:inline-flex;gap:7px;align-items:baseline}}
.chips button b{{font-size:var(--chip);color:var(--c);font-variant-numeric:tabular-nums}}
.chips button[aria-pressed=true]{{border-color:var(--c);box-shadow:inset 0 0 0 1px var(--c)}}
section.g{{margin-bottom:var(--s6)}}
section.g h2{{font-size:var(--h3);margin:0 0 4px;color:var(--c)}}
section.g h2 small{{font-weight:400;color:var(--ink-3);font-size:var(--chip);margin-inline-start:8px}}
.shelf{{margin:var(--s4) 0 0;border-inline-start:3px solid var(--c);padding-inline-start:14px}}
.shelf h3{{font-size:var(--h4);margin:0 0 6px}}
.shelf h3 small{{font-weight:400;color:var(--ink-3);font-size:var(--chip);margin-inline-start:7px}}
.shelf ul{{margin:0;padding:0;list-style:none;columns:3 250px;column-gap:var(--s5)}}
.shelf li{{font-size:var(--small);color:var(--ink-2);line-height:1.85;break-inside:avoid;padding:1px 0}}
.empty{{color:var(--ink-3);font-size:var(--small)}}
@media (max-width:640px){{.shelf ul{{columns:1}}}}
</style>
</head>
<body>
<main class="wrap">
<h1>فهرست کتاب‌ها</h1>
<p class="lead">{fa(len(C))} کتاب و سند در مجموعهٔ دانش‌سرا، دسته‌بندی‌شده به تفکیک رشته و قفسه. این فهرست نشان می‌دهد پشت هر ویکی چه منابعی خوابیده و کدام قفسه هنوز خالی است.</p>
<div class="warn"><b>این فهرست از روی عنوان ساخته شده، نه از روی خواندن.</b> دسته‌بندی هر کتاب یک حدس آگاهانه بر پایهٔ نامش است و ممکن است اشتباه باشد. هیچ‌کدام از این‌ها هنوز وارد فهرست منابع دانش‌سرا نشده‌اند؛ یک کتاب تنها پس از خوانده شدن، با ردهٔ اعتبار و ارجاع دقیق، به منابع اضافه می‌شود.</div>
<p class="lead" style="margin-bottom:var(--s4)"><a href="library-plan.html">نقشهٔ کتابخانه ←</a> &nbsp;·&nbsp; <a href="story.html">داستان پروژه ←</a></p>
<div class="bar"><input id="q" type="search" placeholder="جست‌وجو در عنوان‌ها…" aria-label="جست‌وجو"><span class="empty" id="count"></span></div>
<div class="chips" id="chips"><button data-k="" aria-pressed="true" style="--c:var(--primary)">همه<b>{fa(len(C))}</b></button>{chips}</div>
<div id="list"></div>
</main>
<script>window.COL={json.dumps(data, ensure_ascii=False)};</script>
<script>
(()=>{{const D=window.COL,$=i=>document.getElementById(i);let K="",Q="";
const esc=s=>String(s).replace(/[&<>"]/g,c=>({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
const fa=n=>String(n).replace(/\\d/g,d=>"۰۱۲۳۴۵۶۷۸۹"[d]);
function render(){{let html="",shown=0;
 for(const g of D.groups){{ if(K&&g.k!==K) continue;
  let inner="",gn=0;
  for(const s of g.shelves){{ const books=Q?s.b.filter(b=>b.toLowerCase().includes(Q)):s.b;
   if(!books.length) continue; gn+=books.length;
   inner+=`<div class="shelf"><h3>${{esc(s.s)}}<small>${{fa(books.length)}} عنوان</small></h3><ul>${{books.map(b=>`<li>${{esc(b)}}</li>`).join("")}}</ul></div>`;}}
  if(!gn) continue; shown+=gn;
  html+=`<section class="g" style="--c:${{g.c}}"><h2>${{esc(g.n)}}<small>${{fa(gn)}} عنوان</small></h2>${{g.u?`<p class="empty"><a href="${{g.u}}">ویکی ${{esc(g.n)}} ←</a></p>`:'<p class="empty">هنوز ویکی ندارد</p>'}}${{inner}}</section>`;}}
 $("list").innerHTML=html||'<p class="empty">چیزی پیدا نشد.</p>';
 $("count").textContent=fa(shown)+" عنوان";}}
$("chips").addEventListener("click",e=>{{const b=e.target.closest("button");if(!b)return;K=b.dataset.k;
 document.querySelectorAll("#chips button").forEach(x=>x.setAttribute("aria-pressed",x===b));render();}});
$("q").addEventListener("input",e=>{{Q=e.target.value.trim().toLowerCase();render();}});
render();}})();
</script>
</body>
</html>
'''
open(f'{R}/atlas/collection.html', 'w', encoding='utf-8').write(tpl)
print('atlas/collection.html —', len(C), 'books,', len(data['groups']), 'groups')
