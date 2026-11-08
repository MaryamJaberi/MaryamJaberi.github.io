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
def T3(fa, en, nl, tag='span', cls='', extra=''):
    a = f' class="{cls}"' if cls else ''
    return f'<{tag}{a}{extra} data-fa="{E(fa)}" data-en="{E(en)}" data-nl="{E(nl)}">{E(fa)}</{tag}>'
def tl(d): return (d['fa'], d.get('en') or d['fa'], d.get('nl') or d.get('en') or d['fa'])
def fieldblock(fid):
    f = cs[fid]; es = sorted([c for c in entries if c.get('field') == fid or c.get('parent') == fid], key=lambda c: c['title']['fa'])
    items = ''.join('<a href="entries.html#%s" data-fa="%s" data-en="%s" data-nl="%s">%s</a>' % ((E(c["id"].split(":")[1]),) + tuple(E(x) for x in tl(c['title'])) + (E(c['title']['fa']),)) for c in es)
    if not es: return ''
    sm = f.get('summary') or {}
    return '<div class="fld">' + T3(*tl(f['title']), tag='h3') + (T3(*tl(sm), tag='p') if sm.get('fa') else '') + f'<div class="lst">{items}</div></div>'
fields = ''.join(fieldblock(f) for f in order if f in cs)
basics = fieldblock('tabar:basics') if 'tabar:basics' in cs else ''
nE, nS, nI = nums(len(entries)), nums(len(srcs)), nums(len(irans))
TOOLS = [
 (('مدخل‌ها', 'Entries', 'Lemma’s'), (f'{nE} مدخل پیش‌نویس با منبع، پرچم قطعیت و پیوند به ویکی‌های دیگر؛ جست‌وجو و فیلتر بر اساس حوزه.', f'{len(entries)} draft entries with sources, certainty flags and links to the other wikis; search and filter by field.', f'{len(entries)} conceptlemma’s met bronnen, zekerheidsvlaggen en links naar de andere wiki’s; zoeken en filteren per vakgebied.'), 'entries.html', ('خواندن', 'Read', 'Lezen')),
 (('اطلس میان‌رشته‌ای', 'Interdisciplinary atlas', 'Interdisciplinaire atlas'), ('پل‌هایی که تبار و ژنتیک را به روان، جامعه و فلسفه وصل می‌کنند (مثل جامعه‌شناسی ژنوم یا فرگشت فرهنگی).', 'Bridges that connect lineage and genetics to mind, society and philosophy (e.g. sociogenomics or cultural evolution).', 'Bruggen die afstamming en genetica verbinden met geest, samenleving en filosofie (bijv. sociogenomica of culturele evolutie).'), '../atlas/', ('باز کردن', 'Open', 'Openen')),
 (('سرزمین دانش', 'Land of knowledge', 'Land van kennis'), ('نقشهٔ سرزمین‌ها و شهرهای دانش و پل‌هایی که میان آن‌ها زده شده.', 'A map of the lands and cities of knowledge and the bridges built between them.', 'Een kaart van de landen en steden van kennis en de bruggen ertussen.'), '../atlas/lands.html', ('گشتن', 'Explore', 'Verkennen')),
 (('برای ایران', 'For Iran', 'Voor Iran'), (f'{nI} یادداشت دادهٔ ایرانی (مثل ناهمگنی ژنتیکی، ازدواج خویشاوندی، غربالگری تالاسمی) با ردهٔ داده A تا D.', f'{len(irans)} Iranian data notes (e.g. genetic heterogeneity, consanguineous marriage, thalassemia screening) graded A to D.', f'{len(irans)} Iraanse datanotities (o.a. genetische heterogeniteit, bloedverwante huwelijken, thalassemiescreening) met gradatie A tot D.'), '../iran/', ('دیدن', 'View', 'Bekijken')),
 (('چهره‌ها', 'People', 'Personen'), ('پژوهشگرانی که در مدخل‌ها آمده‌اند، با شناسهٔ مشترک و پیوند ویکی‌داده.', 'The researchers who appear in the entries, with a shared ID and Wikidata link.', 'De onderzoekers uit de lemma’s, met een gedeeld ID en Wikidata-link.'), '../core/people.html', ('دیدن', 'View', 'Bekijken')),
 (('منابع', 'Sources', 'Bronnen'), (f'منابع مدخل‌های تبار ({nS} منبع) در کنار کتابخانهٔ مشترک دانش‌سرا.', f'Sources of the lineage entries ({len(srcs)}) within the shared Daneshsara library.', f'Bronnen van de afstammingslemma’s ({len(srcs)}) binnen de gedeelde Daneshsara-bibliotheek.'), '../core/sources.html', ('دیدن', 'View', 'Bekijken')),
 (('بازبینی و مشارکت', 'Review & contribute', 'Beoordelen & bijdragen'), ('اگر در ژنتیک یا انسان‌شناسی تخصص داری، مدخل‌ها را بسنج یا مدخل تازه پیشنهاد بده.', 'If you are an expert in genetics or anthropology, check entries or propose a new one.', 'Ben je expert in genetica of antropologie? Beoordeel lemma’s of stel een nieuw voor.'), '../core/contribute.html', ('راهنما', 'Guide', 'Gids')),
]
cards = ''.join(f'<a class="tool" href="{u}">{T3(*t, tag="h3")}{T3(*d, tag="p")}<span class="go">{T3(*g)} <i class="arr"></i></span></a>' for t, d, u, g in TOOLS)
PLANNED = [('کتابخانه و بخش دانشمندان (کتاب‌ها، مقاله‌ها، زندگی‌نامهٔ پژوهشگران)', 'Library and scientists section (books, papers, researcher biographies)', 'Bibliotheek en wetenschappersgedeelte (boeken, artikelen, biografieën)'),
           ('ابزارهای بصری خلاق برای مسیر مهاجرت‌ها و درخت تبار', 'Creative visual tools for migration routes and family trees', 'Creatieve visuele tools voor migratieroutes en stambomen'),
           ('فهرست خلأهای محتوایی برای تکمیل با داده و منبع بیشتر', 'A list of content gaps to fill with more data and sources', 'Een lijst met inhoudelijke hiaten om aan te vullen met data en bronnen')]
planned = ''.join(T3(*x, tag='li') for x in PLANNED)
page = f"""<!doctype html>
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
.lang{{display:flex;gap:2px;border:1px solid var(--line-strong);border-radius:var(--r-full);padding:2px}}
.lang button{{font:inherit;font-size:var(--chip);padding:4px 10px;border:0;border-radius:var(--r-full);background:transparent;color:var(--ink-2);cursor:pointer}}
.lang button[aria-pressed=true]{{background:var(--ink);color:var(--paper)}}
i.arr::before{{content:"←"}} [dir=ltr] i.arr::before{{content:"→"}}
main{{padding-block:var(--s8) var(--s16)}}
.draft{{display:inline-block;font-size:var(--chip);padding:3px 12px;border-radius:var(--r-full);background:var(--fam-bio-soft);color:var(--fam-bio);border:1px solid var(--fam-bio)}}
h1{{font-size:var(--h1);line-height:var(--lh-tight);margin:var(--s3) 0;text-wrap:balance}}
.lead{{color:var(--ink-2);font-size:1.1rem;max-width:68ch;margin:0 0 var(--s8)}}
.hero{{display:grid;grid-template-columns:1.3fr 1fr;gap:var(--s6);align-items:stretch;margin-bottom:var(--s10)}}
.main-tool{{display:flex;flex-direction:column;gap:var(--s3);justify-content:center;padding:var(--s8);border-radius:var(--r-xl);background:var(--fam-bio-soft);border:1px solid var(--fam-bio);text-decoration:none;color:var(--ink)}}
.main-tool .tag{{font-size:var(--chip);letter-spacing:.04em;color:var(--fam-bio);font-weight:700}}
.main-tool h2{{margin:0;font-size:2.1rem;line-height:1.25}} .main-tool p{{margin:0;color:var(--ink-2)}}
.main-tool .btn{{align-self:flex-start;margin-top:var(--s2);background:var(--fam-bio);color:#fff;padding:9px 22px;border-radius:var(--r-full);font-weight:700}}
.side{{display:grid;gap:var(--s3);align-content:center}} .side p{{margin:0;color:var(--ink-2)}}
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
<header class="top"><div class="wrap"><a class="brand" href="../">{T3('دانش‌سرا','Daneshsara','Daneshsara')}</a>
<div class="crumbs"><a href="../">{T3('خانه','Home','Home')}</a> › {T3('ویکی تبار','Lineage wiki','Afstammingswiki')}</div>
<div class="lang" role="group" aria-label="language"><button data-l="fa">فا</button><button data-l="en">EN</button><button data-l="nl">NL</button></div></div></header>
<main class="wrap">
{T3('پیش‌نویس · در حال بازبینی','Draft · under review','Concept · in beoordeling', cls='draft')}
{T3('ویکی تبار و ژنتیک','Lineage & Genetics wiki','Wiki Afstamming & genetica', tag='h1')}
{T3('از کجا آمده‌ایم و چه چیزی را از اجدادمان به ارث برده‌ایم؟ وراثت‌پذیری، دی‌ان‌ای باستانی، فرگشت انسان، اپی‌ژنتیک و تبارشناسی، با منبع و پرچم قطعیت برای هر گزاره و یادداشت‌هایی دربارهٔ ایران.','Where do we come from and what did we inherit from our ancestors? Heritability, ancient DNA, human evolution, epigenetics and genealogy, with a source and a certainty flag for every claim, plus notes on Iran.','Waar komen we vandaan en wat hebben we van onze voorouders geërfd? Erfelijkheid, oud DNA, menselijke evolutie, epigenetica en genealogie, met bron en zekerheidsvlag per bewering en notities over Iran.', tag='p', cls='lead')}
<div class="hero">
 <a class="main-tool" href="https://maryamjaberi.github.io/earth-through-time/">
  {T3('ابزار اصلی · اطلس زمین','Main tool · Earth atlas','Hoofdtool · Aardatlas', cls='tag')}
  {T3('زمین در گذر زمان','Earth Through Time','De aarde door de tijd', tag='h2')}
  {T3('نوار زمان را بکش و ببین نقشهٔ زمین، گیاهان و جانوران و زندگی انسان در هر دوره چطور بود. عکس، فسیل و بازسازی هر دوره کنارش است.','Drag the timeline and see what the map of Earth, plants, animals and human life looked like in each era. Photos, fossils and reconstructions accompany each period.','Sleep de tijdlijn en zie hoe de kaart van de aarde, planten, dieren en het menselijk leven er in elk tijdperk uitzagen. Foto’s, fossielen en reconstructies horen erbij.', tag='p')}
  <span class="btn">{T3('باز کردن اطلس زمین','Open the Earth atlas','Open de aardatlas')} <i class="arr"></i></span>
 </a>
 <div class="side">{T3('اطلس زمین، بستر زمانیِ این ویکی است: مدخل‌ها می‌گویند «چه شد»، اطلس نشان می‌دهد «کجا و کِی».','The Earth atlas is the time backdrop of this wiki: the entries say what happened, the atlas shows where and when.','De aardatlas is de tijdachtergrond van deze wiki: de lemma’s vertellen wat er gebeurde, de atlas toont waar en wanneer.', tag='p')}
 <div class="stats">{T3(nE+' مدخل', f'{len(entries)} entries', f'{len(entries)} lemma’s')}{T3(nS+' منبع', f'{len(srcs)} sources', f'{len(srcs)} bronnen')}{T3(nI+' یادداشت ایران', f'{len(irans)} Iran notes', f'{len(irans)} Iran-notities')}</div></div>
</div>
{T3('ابزارها','Tools','Tools', tag='h2', cls='sec')}
<div class="tools">{cards}</div>
{T3('مدخل‌ها به تفکیک حوزه','Entries by field','Lemma’s per vakgebied', tag='h2', cls='sec')}
<div class="flds">{basics}{fields}</div>
{T3('در راه','Coming up','In ontwikkeling', tag='h2', cls='sec')}
<div class="soon">{T3('بخش‌هایی که برنامه‌ریزی شده و هنوز ساخته نشده‌اند:','Planned sections that are not built yet:','Geplande onderdelen die nog niet gebouwd zijn:')}<ul>{planned}</ul></div>
</main>
<footer><div class="wrap">{T3('دانش‌سرا · زیر چتر SoloNovate · متن‌ها CC BY-SA 4.0','Daneshsara · under the SoloNovate umbrella · text CC BY-SA 4.0','Daneshsara · onder de paraplu van SoloNovate · tekst CC BY-SA 4.0')}</div></footer>
<script>
let L="fa";try{{L=localStorage.getItem("ds-lang")||"fa"}}catch(_){{}}
function apply(){{document.documentElement.lang=L;document.documentElement.dir=L==="fa"?"rtl":"ltr";
document.querySelectorAll("[data-fa]").forEach(e=>{{e.textContent=e.dataset[L]||e.dataset.fa}});
document.querySelectorAll(".lang button").forEach(b=>b.setAttribute("aria-pressed",b.dataset.l===L));
document.title=({{fa:"ویکی تبار — دانش‌سرا",en:"Lineage wiki — Daneshsara",nl:"Afstammingswiki — Daneshsara"}})[L]}}
document.querySelector(".lang").addEventListener("click",ev=>{{const b=ev.target.closest("[data-l]");if(!b)return;L=b.dataset.l;try{{localStorage.setItem("ds-lang",L)}}catch(_){{}};apply()}});
apply();
</script>
</body></html>"""
open(f'{R}/tabar/index.html', 'w', encoding='utf-8').write(page)
print('tabar landing', len(page), 'bytes;', len(entries), 'entries,', len(srcs), 'sources,', len(irans), 'iran')
