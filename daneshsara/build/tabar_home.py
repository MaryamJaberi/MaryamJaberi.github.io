# -*- coding: utf-8 -*-
"""Landing page of ویکی تبار: python3 build/tabar_home.py → tabar/index.html
The entry list lives at tabar/entries.html (build/reader.py tabar); old links tabar/#slug are forwarded there."""
import json, glob, os, html
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
load = lambda p: json.load(open(p, encoding='utf-8'))
cs = {c['id']: c for c in (load(p) for p in glob.glob(f'{R}/data/tabar/concepts/*.json'))}
order = load(f'{R}/data/tabar/order.json')
entries = [c for c in cs.values() if c['kind'] == 'concept']
srcs = {s for c in entries for s in c.get('sources', [])} | {s for c in entries for p in c.get('points', []) for s in p.get('sources', [])}
irans = [i for i in (load(p) for p in glob.glob(f'{R}/iran/*.json')) if i['id'].startswith('tabar:') or any(c.get('iran') == i['id'] for c in entries)]
nums = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
E = html.escape
def fieldblock(fid):
    f = cs[fid]; es = sorted([c for c in entries if c.get('field') == fid or c.get('parent') == fid], key=lambda c: c['title']['fa'])
    items = ''.join(f'<a href="entries.html#{E(c["id"].split(":")[1])}">{E(c["title"]["fa"])}</a>' for c in es)
    return f'<div class="fld"><h3>{E(f["title"]["fa"])}</h3><p>{E(f.get("summary",{}).get("fa",""))}</p><div class="lst">{items}</div></div>' if es else ''
fields = ''.join(fieldblock(f) for f in order if f in cs)
basics = fieldblock('tabar:basics') if 'tabar:basics' in cs else ''
TOOLS = [
 ('مدخل‌ها', f'{nums(len(entries))} مدخل پیش‌نویس با منبع، پرچم قطعیت و پیوند به ویکی‌های دیگر؛ جست‌وجو و فیلتر بر اساس حوزه.', 'entries.html', 'خواندن'),
 ('اطلس میان‌رشته‌ای', 'پل‌هایی که تبار و ژنتیک را به روان، جامعه و فلسفه وصل می‌کنند (مثل جامعه‌شناسی ژنوم یا فرگشت فرهنگی).', '../atlas/', 'باز کردن'),
 ('سرزمین دانش', 'نقشهٔ سرزمین‌ها و شهرهای دانش و پل‌هایی که میان آن‌ها زده شده.', '../atlas/lands.html', 'گشتن'),
 ('برای ایران', f'{nums(len(irans))} یادداشت دادهٔ ایرانی (مثل ناهمگنی ژنتیکی، ازدواج خویشاوندی، غربالگری تالاسمی) با ردهٔ داده A تا D.', '../iran/', 'دیدن'),
 ('چهره‌ها', 'پژوهشگرانی که در مدخل‌ها آمده‌اند، با شناسهٔ مشترک و پیوند ویکی‌داده.', '../core/people.html', 'دیدن'),
 ('منابع', f'منابع مدخل‌های تبار ({nums(len(srcs))} منبع) در کنار کتابخانهٔ مشترک دانش‌سرا.', '../core/sources.html', 'دیدن'),
 ('بازبینی و مشارکت', 'اگر در ژنتیک یا انسان‌شناسی تخصص داری، مدخل‌ها را بسنج یا مدخل تازه پیشنهاد بده.', '../core/contribute.html', 'راهنما'),
]
cards = ''.join(f'<a class="tool" href="{u}"><h3>{E(t)}</h3><p>{E(d)}</p><span class="go">{E(g)} ←</span></a>' for t, d, u, g in TOOLS)
PLANNED = ['کتابخانه و بخش دانشمندان (کتاب‌ها، مقاله‌ها، زندگی‌نامهٔ پژوهشگران)', 'ابزارهای بصری خلاق برای مسیر مهاجرت‌ها و درخت تبار', 'فهرست خلأهای محتوایی برای تکمیل با داده و منبع بیشتر']
planned = ''.join(f'<li>{E(x)}</li>' for x in PLANNED)
page = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>ویکی تبار — دانش‌سرا</title>
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font);line-height:var(--lh);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
a{{color:var(--primary)}} .wrap{{max-width:var(--container);margin:0 auto}}
header.top{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);margin-inline:calc(-1*max(16px,env(safe-area-inset-left,0px)));padding-inline:max(16px,env(safe-area-inset-left,0px))}}
header.top .wrap{{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);min-height:56px}}
.brand{{font-weight:700;color:var(--ink);text-decoration:none}} .crumbs{{font-size:var(--small);color:var(--ink-2)}}
main{{padding-block:var(--s8) var(--s16)}}
.draft{{display:inline-block;font-size:var(--chip);padding:3px 12px;border-radius:var(--r-full);background:var(--fam-bio-soft);color:var(--fam-bio);border:1px solid var(--fam-bio)}}
h1{{font-size:var(--h1);line-height:var(--lh-tight);margin:var(--s3) 0;text-wrap:balance}}
.lead{{color:var(--ink-2);font-size:1.1rem;max-width:68ch;margin:0 0 var(--s8)}}
.hero{{display:grid;grid-template-columns:1.3fr 1fr;gap:var(--s6);align-items:stretch;margin-bottom:var(--s10)}}
.main-tool{{display:flex;flex-direction:column;gap:var(--s3);justify-content:center;padding:var(--s8);border-radius:var(--r-xl);background:var(--fam-bio-soft);border:1px solid var(--fam-bio);text-decoration:none;color:var(--ink)}}
.main-tool .tag{{font-size:var(--chip);letter-spacing:.04em;color:var(--fam-bio);font-weight:700}}
.main-tool h2{{margin:0;font-size:2.1rem;line-height:1.25}} .main-tool p{{margin:0;color:var(--ink-2)}}
.main-tool .btn{{align-self:flex-start;margin-top:var(--s2);background:var(--fam-bio);color:#fff;padding:9px 22px;border-radius:var(--r-full);font-weight:700}}
.side{{display:grid;gap:var(--s3);align-content:center}}
.side p{{margin:0;color:var(--ink-2)}}
.stats{{display:flex;flex-wrap:wrap;gap:var(--s2)}} .stats span{{padding:4px 12px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--surface);font-size:var(--small)}}
h2.sec{{font-size:var(--h2);margin:var(--s10) 0 var(--s4)}}
.tools{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:var(--s4)}}
.tool{{display:grid;gap:6px;align-content:start;padding:var(--s5);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);text-decoration:none;color:var(--ink);transition:transform .15s,box-shadow .15s}}
.tool:hover{{transform:translateY(-2px);box-shadow:var(--shadow-md)}} .tool h3{{margin:0;font-size:var(--h4)}} .tool p{{margin:0;color:var(--ink-2);font-size:var(--small)}} .tool .go{{color:var(--primary);font-size:var(--small);font-weight:700}}
.flds{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:var(--s4)}}
.fld{{padding:var(--s5);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);min-width:0}}
.fld h3{{margin:0 0 4px;font-size:var(--h4);color:var(--fam-bio)}} .fld p{{margin:0 0 var(--s3);color:var(--ink-2);font-size:var(--small)}}
.lst{{display:flex;flex-wrap:wrap;gap:6px}} .lst a{{font-size:var(--small);padding:2px 10px;border-radius:var(--r-full);background:var(--surface-subtle);color:var(--ink);text-decoration:none}} .lst a:hover{{background:var(--fam-bio-soft)}}
.soon{{padding:var(--s5);border:1px dashed var(--line-strong);border-radius:var(--r-lg);color:var(--ink-2)}} .soon ul{{margin:var(--s2) 0 0;padding-inline-start:1.2em}}
footer{{border-top:1px solid var(--line);margin-top:var(--s12);padding-block:var(--s6);color:var(--ink-3);font-size:var(--small)}}
@media (max-width:760px){{.hero{{grid-template-columns:1fr}} h1{{font-size:2rem}} .main-tool{{padding:var(--s5)}} .main-tool h2{{font-size:1.6rem}}}}
</style>
<script>if(location.hash.length>1)location.replace('entries.html'+location.hash);</script>
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="../">دانش‌سرا</a><div class="crumbs"><a href="../">خانه</a> › ویکی تبار</div></div></header>
<main class="wrap">
<span class="draft">پیش‌نویس · در حال بازبینی</span>
<h1>ویکی تبار و ژنتیک</h1>
<p class="lead">از کجا آمده‌ایم و چه چیزی را از اجدادمان به ارث برده‌ایم؟ وراثت‌پذیری، دی‌ان‌ای باستانی، فرگشت انسان، اپی‌ژنتیک و تبارشناسی، با منبع و پرچم قطعیت برای هر گزاره و یادداشت‌هایی دربارهٔ ایران.</p>
<div class="hero">
 <a class="main-tool" href="https://maryamjaberi.github.io/earth-through-time/">
  <span class="tag">ابزار اصلی · اطلس زمین</span>
  <h2>زمین در گذر زمان</h2>
  <p>نوار زمان را بکش و ببین نقشهٔ زمین، گیاهان و جانوران و زندگی انسان در هر دوره چطور بود. عکس، فسیل و بازسازی هر دوره کنارش است.</p>
  <span class="btn">باز کردن اطلس زمین ←</span>
 </a>
 <div class="side"><p>اطلس زمین، بستر زمانیِ این ویکی است: مدخل‌ها می‌گویند «چه شد»، اطلس نشان می‌دهد «کجا و کِی».</p>
 <div class="stats"><span>{nums(len(entries))} مدخل</span><span>{nums(len(srcs))} منبع</span><span>{nums(len(irans))} یادداشت ایران</span></div></div>
</div>
<h2 class="sec">ابزارها</h2>
<div class="tools">{cards}</div>
<h2 class="sec">مدخل‌ها به تفکیک حوزه</h2>
<div class="flds">{basics}{fields}</div>
<h2 class="sec">در راه</h2>
<div class="soon">بخش‌هایی که برنامه‌ریزی شده و هنوز ساخته نشده‌اند:<ul>{planned}</ul></div>
</main>
<footer><div class="wrap">دانش‌سرا · زیر چتر SoloNovate · متن‌ها CC BY-SA 4.0</div></footer>
</body></html>'''
open(f'{R}/tabar/index.html', 'w', encoding='utf-8').write(page)
print('tabar landing', len(page), 'bytes;', len(entries), 'entries,', len(srcs), 'sources,', len(irans), 'iran')
