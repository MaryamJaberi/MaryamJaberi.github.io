# -*- coding: utf-8 -*-
"""Build core/people.html and core/sources.html — the shared registers, with reverse links to every concept that cites them."""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
def load(p): return json.load(open(p, encoding='utf-8'))
people = load(f'{R}/core/people.json'); sources = load(f'{R}/core/sources.json'); reg = load(f'{R}/core/registry.json')['entries']
concepts = [load(p) for p in glob.glob(f'{R}/data/*/concepts/*.json')]
pref = {}; sref = {}
for c in concepts:
    for p in c.get('people', []): pref.setdefault(p, []).append(c['id'])
    cited = set(c.get('sources', [])) | {s for pt in c.get('points', []) for s in pt.get('sources', [])}
    for s in cited: sref.setdefault(s, []).append(c['id'])
def ref(ids): return [{'id': i, 'title': reg[i]['title'], 'url': '../' + reg[i]['url'], 'wiki': i.split(':')[0]} for i in sorted(set(ids)) if i in reg]
P = [{'id': k, 'name': v['name'], 'years': v.get('years', ''), 'note': v.get('note', {}).get('fa', ''), 'wikis': v.get('wikis', []), 'qid': v.get('wikidata'), 'in': ref(pref.get(k, []))} for k, v in people.items()]
P.sort(key=lambda x: -len(x['in']))
S = [{'id': k, 'cite': v['cite'], 'year': v.get('year'), 'tier': v.get('tier'), 'url': v.get('url'), 'wikis': v.get('wikis', []), 'in': ref(sref.get(k, []))} for k, v in sources.items()]
S.sort(key=lambda x: (-(x['year'] or 0), x['cite']))

HEAD = '''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>__T__ | هستهٔ مشترک | دانش‌سرا</title><meta name="description" content="__D__"><link rel="stylesheet" href="../core/design/tokens.css">
<style>
header.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);min-height:var(--header-h)}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--ink)} .brand svg{width:26px;height:26px;color:var(--primary)}
.crumbs{font-size:var(--small);color:var(--ink-2)} .crumbs a{color:var(--ink-2)}
.lang{display:flex;gap:2px;border:1px solid var(--line-strong);border-radius:var(--r-full);padding:2px}
.lang button{font:inherit;font-size:var(--chip);padding:4px 10px;border:0;border-radius:var(--r-full);background:transparent;color:var(--ink-2);cursor:pointer}
.lang button[aria-pressed=true]{background:var(--ink);color:var(--paper)}
main{padding-block:var(--s6) var(--s16)} h1{margin:0 0 var(--s2)} .lead{color:var(--ink-2);max-width:70ch;margin:0 0 var(--s4)}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:var(--s5)}
.bar input{font:inherit;flex:1;min-width:220px;padding:10px 14px;border-radius:var(--r-md);border:1px solid var(--line-strong);background:var(--surface);color:var(--ink)}
.bar button{font:inherit;font-size:var(--small);padding:6px 14px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer}
.bar button[aria-pressed=true]{background:var(--primary);color:#fff;border-color:var(--primary)}
.list{display:grid;gap:10px}
.row{padding:var(--s4) var(--s5);display:grid;gap:6px;scroll-margin-top:80px}
.row:target{outline:2px solid var(--primary)}
.row h3{margin:0;font-size:var(--h4);display:flex;gap:10px;align-items:baseline;flex-wrap:wrap} .row h3 small{color:var(--ink-3);font-weight:400;font-size:var(--small)}
.row .n{color:var(--ink-2);font-size:var(--small)}
.cite{direction:ltr;text-align:left;font-size:var(--small);line-height:1.7} .cite a{color:var(--primary)}
.tags{display:flex;flex-wrap:wrap;gap:6px} .tags a,.tags span{font-size:var(--chip);padding:2px 10px;border-radius:var(--r-full);border:1px solid var(--line-strong);text-decoration:none;color:var(--ink);background:var(--surface)}
.tags .psy{border-color:var(--fam-psy)} .tags .soc{border-color:var(--fam-soc)} .tags .tabar{border-color:var(--fam-bio)} .tags .phil{border-color:var(--fam-hum)}
.tier{font-size:var(--chip);padding:1px 8px;border-radius:var(--r-full);background:var(--ink);color:var(--paper)}
.more{text-align:center;margin-top:var(--s5)} .more button{font:inherit;padding:8px 18px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer}
footer.foot{border-top:1px solid var(--line);padding-block:var(--s8);color:var(--ink-3);font-size:var(--small)}
</style></head><body>
<header class="top"><div class="wrap"><a class="brand" href="../"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 7l8-4 8 4-8 4-8-4z"/><path d="M4 12l8 4 8-4"/><path d="M4 17l8 4 8-4"/></svg><span>دانش‌سرا</span></a>
<div class="crumbs"><a href="../" data-i="home">خانه</a> › <span data-i="h1">__T__</span></div>
<div class="lang" role="group"><button data-l="fa" aria-pressed="true">فا</button><button data-l="en">EN</button><button data-l="nl">NL</button></div></div></header>
<main class="wrap"><h1 data-i="h1">__T__</h1><p class="lead" data-i="lead"></p><div class="bar" id="bar"></div><div class="list" id="list"></div><div class="more" id="more"></div></main>
<footer class="foot"><div class="wrap" data-i="foot"></div></footer>
<script>
const D = __DATA__;
const WN = {fa:{psy:"روان",soc:"جامعه",tabar:"تبار",phil:"فلسفه"},en:{psy:"Mind",soc:"Society",tabar:"Lineage",phil:"Philosophy"},nl:{psy:"Geest",soc:"Samenleving",tabar:"Afstamming",phil:"Filosofie"}};
let L = "fa"; try { L = localStorage.getItem("ds-lang") || "fa"; } catch(_) {}
const T = k => (UI[L] && UI[L][k]) ?? UI.fa[k];
const tx = o => !o ? "" : (typeof o === "string" ? o : (L === "fa" ? o.fa : (o[L] || o.en || o.fa)) || "");
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fa = s => L === "fa" ? String(s).replace(/\\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[d]) : String(s);
let q = "", w = "", shown = 60;
'''
TAIL = '''
function i18n(){ document.documentElement.lang = L; document.documentElement.dir = L === "fa" ? "rtl" : "ltr"; document.querySelectorAll("[data-i]").forEach(el => el.textContent = T(el.dataset.i)); document.querySelectorAll(".lang button").forEach(b => b.setAttribute("aria-pressed", b.dataset.l === L)); document.title = T("h1") + (L === "fa" ? " | هستهٔ مشترک | دانش‌سرا" : " | Daneshsara"); render(); }
document.querySelector(".lang").addEventListener("click", ev => { const b = ev.target.closest("[data-l]"); if (!b) return; L = b.dataset.l; try { localStorage.setItem("ds-lang", L); } catch(_) {} i18n(); });
document.addEventListener("input", ev => { if (ev.target.id === "q") { q = ev.target.value.toLowerCase(); shown = 60; render(); const i = document.getElementById("q"); i.focus(); i.setSelectionRange(i.value.length, i.value.length); } });
document.addEventListener("click", ev => { const b = ev.target.closest("[data-w]"); if (b) { w = b.dataset.w; shown = 60; render(); } if (ev.target.closest("[data-more]")) { shown += 100; render(); } });
i18n();
if (location.hash) { const el = document.getElementById(location.hash.slice(1)); if (!el) { shown = 10000; render(); } setTimeout(() => { const e = document.getElementById(location.hash.slice(1)); if (e) e.scrollIntoView({block: "start"}); }, 50); }
</script></body></html>'''

PEOPLE_JS = '''
const UI = {fa:{home:"خانه",h1:"چهره‌ها",lead:"همهٔ پژوهشگرانی که در ویکی‌های دانش‌سرا نام برده شده‌اند، با مدخل‌هایی که در آن‌ها حضور دارند. یک نام، یک شناسه، در همهٔ ویکی‌ها.",ph:"جست‌وجوی نام…",all:"همه",inW:"در",more:"نمایش بیشتر",n:"نفر",foot:"شناسهٔ هر فرد در هستهٔ مشترک یکتاست؛ پیوند با Wikidata در مرحلهٔ بعد افزوده می‌شود."},
 en:{home:"Home",h1:"People",lead:"Every researcher named across the Daneshsara wikis, with the entries they appear in. One name, one identifier, in every wiki.",ph:"Search names…",all:"All",inW:"in",more:"Show more",n:"people",foot:"Each person's identifier is unique in the shared core; Wikidata links come in the next phase."},
 nl:{home:"Home",h1:"Personen",lead:"Elke onderzoeker die in de Daneshsara-wiki's wordt genoemd, met de lemma's waarin hij of zij voorkomt. Eén naam, één identificator, in elke wiki.",ph:"Zoek namen…",all:"Alles",inW:"in",more:"Meer tonen",n:"personen",foot:"De identificator van elke persoon is uniek in de gedeelde kern; Wikidata-koppelingen volgen in de volgende fase."}};
function render(){
  const items = D.filter(p => (!w || p.wikis.includes(w)) && (!q || JSON.stringify(p.name).toLowerCase().includes(q) || (p.note || "").toLowerCase().includes(q)));
  document.getElementById("bar").innerHTML = `<input id="q" type="search" placeholder="${T("ph")}" value="${esc(q)}">` + ["", "psy", "soc", "tabar", "phil"].map(k => `<button data-w="${k}" aria-pressed="${w === k}">${k ? WN[L][k] : T("all")}</button>`).join("") + `<span style="align-self:center;color:var(--ink-3);font-size:var(--small)">${fa(items.length)} ${T("n")}</span>`;
  document.getElementById("list").innerHTML = items.slice(0, shown).map(p => `<article class="card row" id="${p.id.split(":")[1]}"><h3>${esc(tx(p.name))}${L === "fa" && p.name.en ? `<small dir="ltr">${esc(p.name.en)}</small>` : ""}${p.years ? `<small>${fa(p.years)}</small>` : ""}${p.qid ? `<small><a href="https://www.wikidata.org/wiki/${p.qid}" target="_blank" rel="noopener" style="color:var(--ink-3)">Wikidata ↗</a></small>` : ""}</h3>${p.note && L === "fa" ? `<div class="n">${esc(p.note)}</div>` : ""}<div class="tags">${p.in.map(c => `<a class="${c.wiki}" href="${c.url}">${esc(tx(c.title))}</a>`).join("")}</div></article>`).join("");
  document.getElementById("more").innerHTML = items.length > shown ? `<button data-more>${T("more")} (${fa(items.length - shown)})</button>` : "";
}'''
SOURCES_JS = '''
const UI = {fa:{home:"خانه",h1:"منابع",lead:"همهٔ منابعی که گزاره‌های ویکی‌ها به آن‌ها ارجاع می‌دهند، با ردهٔ منبع (۱ مقالهٔ داوری‌شده، ۲ کتاب دانشگاهی، ۳ گزارش و وب) و مدخل‌هایی که از آن‌ها استفاده کرده‌اند.",ph:"جست‌وجو در منابع…",all:"همه",more:"نمایش بیشتر",n:"منبع",t:"رده",foot:"ردهٔ منبع دربارهٔ نوع انتشار است، نه کیفیت یافته؛ وضعیت تکرار هر یافته در خود مدخل‌ها پرچم خورده."},
 en:{home:"Home",h1:"Sources",lead:"Every source the wikis' statements cite, with its tier (1 peer-reviewed article, 2 academic book, 3 report or web) and the entries that use it.",ph:"Search sources…",all:"All",more:"Show more",n:"sources",t:"tier",foot:"The tier is about publication type, not the quality of the finding; replication status is flagged in the entries themselves."},
 nl:{home:"Home",h1:"Bronnen",lead:"Elke bron waarnaar de wiki's verwijzen, met niveau (1 peer-reviewed artikel, 2 academisch boek, 3 rapport of web) en de lemma's die haar gebruiken.",ph:"Zoek in bronnen…",all:"Alles",more:"Meer tonen",n:"bronnen",t:"niveau",foot:"Het niveau gaat over het publicatietype, niet over de kwaliteit van de bevinding; replicatiestatus staat in de lemma's zelf."}};
function render(){
  const items = D.filter(s => (!w || s.wikis.includes(w)) && (!q || s.cite.toLowerCase().includes(q)));
  document.getElementById("bar").innerHTML = `<input id="q" type="search" placeholder="${T("ph")}" value="${esc(q)}">` + ["", "psy", "soc", "tabar", "phil"].map(k => `<button data-w="${k}" aria-pressed="${w === k}">${k ? WN[L][k] : T("all")}</button>`).join("") + `<span style="align-self:center;color:var(--ink-3);font-size:var(--small)">${fa(items.length)} ${T("n")}</span>`;
  document.getElementById("list").innerHTML = items.slice(0, shown).map(s => `<article class="card row" id="${s.id.split(":")[1]}"><div class="cite">${s.url ? `<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.cite)}</a>` : esc(s.cite)} <span class="tier">${T("t")} ${fa(s.tier)}</span></div><div class="tags">${s.in.map(c => `<a class="${c.wiki}" href="${c.url}">${esc(tx(c.title))}</a>`).join("")}</div></article>`).join("");
  document.getElementById("more").innerHTML = items.length > shown ? `<button data-more>${T("more")} (${fa(items.length - shown)})</button>` : "";
}'''
open(f'{R}/core/people.html', 'w', encoding='utf-8').write(HEAD.replace('__T__', 'چهره‌ها').replace('__D__', 'فهرست چهره‌های علمی دانش‌سرا: هر کس در کدام مدخل‌ها آمده و کدام ویکی‌ها به او ارجاع داده‌اند.').replace('__DATA__', json.dumps(P, ensure_ascii=False)) + PEOPLE_JS + TAIL)
open(f'{R}/core/sources.html', 'w', encoding='utf-8').write(HEAD.replace('__T__', 'منابع').replace('__D__', 'فهرست منابع دانش‌سرا با ردهٔ اعتبار از ۱ تا ۴؛ هر مدخل به منبع اصلی‌اش وصل است.').replace('__DATA__', json.dumps(S, ensure_ascii=False)) + SOURCES_JS + TAIL)
print('people', len(P), 'with refs', sum(1 for p in P if p['in']), '| sources', len(S), 'with refs', sum(1 for s in S if s['in']))
