# -*- coding: utf-8 -*-
"""Build iran/index.html — the «برای ایران» lens: every Iran note in one place, by domain and by capability,
with grade, method, year, contested flag, critique, sources and links to the concepts it informs."""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
def load(p): return json.load(open(p, encoding='utf-8'))
notes = sorted((load(p) for p in glob.glob(f'{R}/iran/*.json')), key=lambda n: (n['domain'], -n['year']))
reg = load(f'{R}/core/registry.json')['entries']
for n in notes:
    n['_concepts'] = [{'id': c, 'title': reg[c]['title'], 'url': '../' + reg[c]['url']} for c in n.get('concepts', []) if c in reg]
DATA = {'notes': notes}
tpl = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>برای ایران — دانش‌سرا</title>
<meta name="description" content="داده‌های واقعی دربارهٔ ایران، هر کدام با سال، روش، ردهٔ کیفیت و منبع؛ به تفکیک حوزه و قابلیت انسانی.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
header.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);min-height:var(--header-h)}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--ink)} .brand svg{width:26px;height:26px;color:var(--primary)}
.crumbs{font-size:var(--small);color:var(--ink-2)} .crumbs a{color:var(--ink-2)}
.lang{display:flex;gap:2px;border:1px solid var(--line-strong);border-radius:var(--r-full);padding:2px}
.lang button{font:inherit;font-size:var(--chip);padding:4px 10px;border:0;border-radius:var(--r-full);background:transparent;color:var(--ink-2);cursor:pointer}
.lang button[aria-pressed=true]{background:var(--ink);color:var(--paper)}
main{padding-block:var(--s6) var(--s16)}
.hero{display:grid;gap:var(--s3);margin-bottom:var(--s6)} .hero p{color:var(--ink-2);max-width:72ch;margin:0;font-size:1.05rem}
.grades{display:flex;flex-wrap:wrap;gap:8px;font-size:var(--small);color:var(--ink-2)}
.grades span{display:inline-flex;align-items:center;gap:6px}
.g{display:inline-block;min-width:1.6em;text-align:center;font-size:var(--chip);font-weight:700;padding:1px 7px;border-radius:var(--r-full);color:#fff}
.g.A{background:#0A6B60}.g.B{background:#2A6F7A}.g.C{background:#B8860B}.g.D{background:#8A2E2E}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin:var(--s4) 0 var(--s6)}
.tabs button{font:inherit;font-size:var(--small);padding:6px 14px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer}
.tabs button[aria-pressed=true]{background:var(--primary);color:#fff;border-color:var(--primary)}
.sec h2{font-size:var(--h3);margin:var(--s6) 0 var(--s3)}
.notes{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:var(--s4)}
.note{scroll-margin-top:90px;padding:var(--s5);display:grid;gap:10px;border-inline-start:4px solid var(--fc,var(--primary))}
.note .q{font-weight:700;font-size:var(--h4);margin:0}
.note .f{margin:0;line-height:1.8}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:var(--chip);color:var(--ink-3)}
.flag{font-size:var(--chip);padding:1px 8px;border-radius:var(--r-full);border:1px solid #E8D39A;background:#FBF1D9;color:#6B4E00}
.crit{font-size:var(--small);color:var(--ink-2);border-inline-start:2px solid var(--line-strong);padding-inline-start:10px;margin:0}
.links{display:flex;flex-wrap:wrap;gap:6px;align-items:flex-start} .links a{display:inline-block;line-height:1.6;font-size:var(--chip);padding:3px 10px;border-radius:var(--r-full);border:1px solid var(--line-strong);text-decoration:none;color:var(--ink);background:var(--surface)}
.src{font-size:var(--chip);color:var(--ink-3);direction:ltr;text-align:left;line-height:1.6} .src a{color:var(--primary)}
.cap{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;margin:var(--s4) 0}
.cap div{padding:10px 12px;border-radius:var(--r-md);background:var(--surface);border:1px solid var(--line);font-size:var(--small);display:flex;justify-content:space-between;gap:8px}
.cap b{color:var(--primary)}
footer.foot{border-top:1px solid var(--line);padding-block:var(--s8);color:var(--ink-3);font-size:var(--small)}
@media (prefers-color-scheme: dark){:root:not([data-theme=light]) .flag{background:#3A3010;color:#F0D78A;border-color:#6B5A2A}}
:root[data-theme=dark] .flag{background:#3A3010;color:#F0D78A;border-color:#6B5A2A}
</style>
</head>
<body>
<header class="top"><div class="wrap">
 <a class="brand" href="../"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 7l8-4 8 4-8 4-8-4z"/><path d="M4 12l8 4 8-4"/><path d="M4 17l8 4 8-4"/></svg><span>دانش‌سرا</span></a>
 <div class="crumbs"><a href="../" data-i="home">خانه</a> › <span data-i="h1">برای ایران</span></div>
 <div class="lang" role="group" aria-label="زبان"><button data-l="fa" aria-pressed="true">فا</button><button data-l="en">EN</button><button data-l="nl">NL</button></div>
</div></header>
<main class="wrap">
 <section class="hero"><h1 data-i="h1">برای ایران</h1><p data-i="lead"></p>
  <div class="grades"><span data-i="gradeL">ردهٔ داده:</span><span><i class="g A">A</i> <span data-i="gA"></span></span><span><i class="g B">B</i> <span data-i="gB"></span></span><span><i class="g C">C</i> <span data-i="gC"></span></span><span><i class="g D">D</i> <span data-i="gD"></span></span></div>
 </section>
 <div class="tabs" id="tabs"></div>
 <div id="body"></div>
</main>
<footer class="foot"><div class="wrap" data-i="foot"></div></footer>
<script>
const D = __DATA__;
const UI = {
 fa:{home:"خانه",h1:"برای ایران",lead:"هر یادداشت یک پرسش دربارهٔ ایران است با پاسخی از داده‌های واقعی: سال، روش، ردهٔ کیفیت و منبع اصلی. یادداشت‌ها به مدخل‌های ویکی‌ها وصل‌اند و وقتی یافته محل بحث است، نقدش کنارش آمده. این لایه با هر ویکی تازه بزرگ‌تر می‌شود.",gradeL:"ردهٔ داده:",gA:"پیمایش ملی یا مطالعهٔ داوری‌شدهٔ قوی",gB:"دادهٔ خوب با محدودیت نمونه یا زمان",gC:"برآورد، نمونهٔ غیراحتمالی یا منبع ثانویه",gD:"گمانه یا دادهٔ قدیمی",byDomain:"به تفکیک حوزه",byCap:"به تفکیک قابلیت",method:"روش",contested:"محل بحث",critique:"نقد",informs:"مدخل‌های مرتبط",foot:"ردهٔ داده دربارهٔ کیفیت شواهد است، نه دربارهٔ اهمیت موضوع. «قابلیت» به فهرست ده‌گانهٔ نوسبام اشاره دارد که چارچوب لایهٔ «برای ایران» است.",
   dom:{psy:"روان",soc:"جامعه",tabar:"تبار و ژنتیک",phil:"فلسفه"},
   cap:{1:"زندگی",2:"سلامت بدنی",3:"یکپارچگی بدنی",4:"حس، تخیل و اندیشه",5:"عواطف",6:"عقل عملی",7:"پیوستگی",8:"دیگر گونه‌ها",9:"بازی",10:"کنترل بر محیط"}},
 en:{home:"Home",h1:"For Iran",lead:"Each note is a question about Iran answered with real data: year, method, quality grade and primary source. Notes link to wiki entries, and where a finding is contested its critique sits beside it. This layer grows with every new wiki.",gradeL:"Data grade:",gA:"national survey or strong peer-reviewed study",gB:"good data with sample or time limits",gC:"estimate, non-probability sample or secondary source",gD:"conjecture or dated data",byDomain:"By domain",byCap:"By capability",method:"Method",contested:"contested",critique:"Critique",informs:"Related entries",foot:"The data grade is about the quality of evidence, not the importance of the topic. \"Capability\" refers to Nussbaum's list of ten, the frame of the Iran layer.",
   dom:{psy:"Mind",soc:"Society",tabar:"Lineage & genetics",phil:"Philosophy"},
   cap:{1:"Life",2:"Bodily health",3:"Bodily integrity",4:"Senses, imagination, thought",5:"Emotions",6:"Practical reason",7:"Affiliation",8:"Other species",9:"Play",10:"Control over environment"}},
 nl:{home:"Home",h1:"Voor Iran",lead:"Elke notitie is een vraag over Iran, beantwoord met echte data: jaar, methode, kwaliteitsgraad en primaire bron. Notities linken naar wiki-lemma's, en waar een bevinding omstreden is staat de kritiek ernaast. Deze laag groeit met elke nieuwe wiki.",gradeL:"Datakwaliteit:",gA:"nationale survey of sterke peer-reviewed studie",gB:"goede data met steekproef- of tijdsbeperkingen",gC:"schatting, niet-probabilistische steekproef of secundaire bron",gD:"vermoeden of verouderde data",byDomain:"Per domein",byCap:"Per capability",method:"Methode",contested:"omstreden",critique:"Kritiek",informs:"Gerelateerde lemma's",foot:"De datakwaliteit gaat over de kwaliteit van het bewijs, niet over het belang van het onderwerp. \"Capability\" verwijst naar Nussbaums lijst van tien, het kader van de Iran-laag.",
   dom:{psy:"Geest",soc:"Samenleving",tabar:"Afstamming & genetica",phil:"Filosofie"},
   cap:{1:"Leven",2:"Lichamelijke gezondheid",3:"Lichamelijke integriteit",4:"Zintuigen, verbeelding, denken",5:"Emoties",6:"Praktische rede",7:"Verbondenheid",8:"Andere soorten",9:"Spel",10:"Controle over omgeving"}}
};
let L = "fa"; try { L = localStorage.getItem("ds-lang") || "fa"; } catch(_) {}
const T = k => (UI[L] && UI[L][k]) ?? UI.fa[k];
const tx = o => !o ? "" : (typeof o === "string" ? o : (L === "fa" ? o.fa : (o[L] || o.en || o.fa)) || "");
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fa = s => L === "fa" ? String(s).replace(/\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[d]) : String(s);
const FC = {psy:"var(--fam-psy)", soc:"var(--fam-soc)", tabar:"var(--fam-bio)", phil:"var(--fam-hum)"};
let mode = "dom";
function card(n){
  return `<article class="card note" id="${n.id.split(":")[1]}" style="--fc:${FC[n.domain] || "var(--primary)"}"><h3 class="q">${esc(tx(n.question))}</h3><p class="f">${esc(tx(n.finding))}</p>
   <div class="meta"><i class="g ${n.grade}">${n.grade}</i><span>${fa(n.year)}</span>${n.method ? `<span>${T("method")}: ${esc(n.method)}</span>` : ""}${n.contested ? `<span class="flag">${T("contested")}</span>` : ""}<span>${esc(T("dom")[n.domain] || n.domain)}</span></div>
   ${n.critique ? `<p class="crit"><b>${T("critique")}:</b> ${esc(n.critique)}</p>` : ""}
   ${n._concepts.length ? `<div class="links">${n._concepts.map(c => `<a href="${c.url}">${esc(tx(c.title))} ↗</a>`).join("")}</div>` : ""}
   <div class="src">${(n.source || []).map(s => s.url ? `<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title)}</a>` : esc(s.title)).join("<br>")}</div></article>`;
}
function render(){
  document.getElementById("tabs").innerHTML = `<button data-m="dom" aria-pressed="${mode === "dom"}">${T("byDomain")}</button><button data-m="cap" aria-pressed="${mode === "cap"}">${T("byCap")}</button>`;
  let s = "";
  if (mode === "dom") {
    const doms = [...new Set(D.notes.map(n => n.domain))];
    s = doms.map(d => `<section class="sec"><h2 style="color:${FC[d]}">${esc(T("dom")[d] || d)} <small style="color:var(--ink-3);font-weight:400">(${fa(D.notes.filter(n => n.domain === d).length)})</small></h2><div class="notes">${D.notes.filter(n => n.domain === d).map(card).join("")}</div></section>`).join("");
  } else {
    const caps = Object.keys(T("cap")).map(Number);
    s = `<div class="cap">${caps.map(c => `<div><span>${fa(c)}. ${esc(T("cap")[c])}</span><b>${fa(D.notes.filter(n => (n.capability || []).includes(c)).length)}</b></div>`).join("")}</div>`;
    s += caps.filter(c => D.notes.some(n => (n.capability || []).includes(c))).map(c => `<section class="sec"><h2>${fa(c)}. ${esc(T("cap")[c])}</h2><div class="notes">${D.notes.filter(n => (n.capability || []).includes(c)).map(card).join("")}</div></section>`).join("");
  }
  document.getElementById("body").innerHTML = s;
}
document.addEventListener("click", ev => { const b = ev.target.closest("[data-m]"); if (b) { mode = b.dataset.m; render(); } });
function i18n(){ document.documentElement.lang = L; document.documentElement.dir = L === "fa" ? "rtl" : "ltr"; document.querySelectorAll("[data-i]").forEach(el => el.textContent = T(el.dataset.i)); document.querySelectorAll(".lang button").forEach(b => b.setAttribute("aria-pressed", b.dataset.l === L)); document.title = T("h1") + " — " + (L === "fa" ? "دانش‌سرا" : "Daneshsara"); render(); }
document.querySelector(".lang").addEventListener("click", ev => { const b = ev.target.closest("[data-l]"); if (!b) return; L = b.dataset.l; try { localStorage.setItem("ds-lang", L); } catch(_) {} i18n(); });
i18n();
if (location.hash) setTimeout(() => { const e = document.getElementById(location.hash.slice(1)); if (e) { e.scrollIntoView({block: "start"}); e.style.outline = "2px solid var(--primary)"; } }, 50);
</script>
</body>
</html>'''
os.makedirs(f'{R}/iran', exist_ok=True)
open(f'{R}/iran/index.html', 'w', encoding='utf-8').write(tpl.replace('__DATA__', json.dumps(DATA, ensure_ascii=False)))
print('iran/index.html', len(notes), 'notes')
