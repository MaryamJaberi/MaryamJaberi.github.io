# -*- coding: utf-8 -*-
"""Build core/review.html — the review queue: every draft entry and bridge, a five-point checklist, and an export of approved ids."""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
def load(p): return json.load(open(p, encoding='utf-8'))
reg = load(f'{R}/core/registry.json')['entries']
items = []
for p in glob.glob(f'{R}/data/*/concepts/*.json'):
    c = load(p)
    if c['status'] == 'draft' and c['kind'] in ('concept', 'subfield'):
        items.append({'id': c['id'], 'wiki': c['id'].split(':')[0], 'title': c['title'], 'url': '../' + reg[c['id']]['url'], 'points': len(c.get('points', [])), 'sources': len(c.get('sources', [])), 'flags': sorted({f for pt in c.get('points', []) for f in pt.get('flags', [])})})
for p in glob.glob(f'{R}/atlas/bridges/*.json'):
    b = load(p)
    if b.get('review') == 'draft':
        items.append({'id': 'bridge:' + b['id'], 'wiki': 'atlas', 'title': b['title'], 'url': '../atlas/bridge.html#' + b['id'], 'points': 0, 'sources': 1 + len(b.get('persian', [])), 'flags': []})
for p in glob.glob(f'{R}/iran/*.json'):
    n = load(p); items.append({'id': n['id'], 'wiki': 'iran', 'title': n['question'], 'url': '../iran/#' + n['id'].split(':')[1], 'points': 1, 'sources': len(n.get('source', [])), 'flags': ['contested'] if n.get('contested') else [], 'grade': n['grade']})
order = {'psy': 0, 'tabar': 1, 'soc': 2, 'phil': 3, 'atlas': 4, 'iran': 5}
items.sort(key=lambda x: (order.get(x['wiki'], 9), x['id']))
tpl = r'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>صف بازبینی — دانش‌سرا</title><link rel="stylesheet" href="../core/design/tokens.css">
<style>
header.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);min-height:var(--header-h)}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--ink)} .brand svg{width:26px;height:26px;color:var(--primary)}
main{padding-block:var(--s6) var(--s16)} h1{margin:0 0 var(--s2)} .lead{color:var(--ink-2);max-width:72ch;margin:0 0 var(--s4);line-height:1.8}
.check{display:grid;gap:6px;padding:var(--s4) var(--s5);margin-bottom:var(--s5)} .check b{display:block;margin-bottom:4px} .check ol{margin:0;padding-inline-start:1.4em;line-height:1.8;color:var(--ink-2)}
.bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:var(--s4)}
.bar button{font:inherit;font-size:var(--small);padding:6px 14px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer}
.bar button[aria-pressed=true]{background:var(--primary);color:#fff;border-color:var(--primary)}
.bar .n{color:var(--ink-3);font-size:var(--small);margin-inline-start:auto}
table{width:100%;border-collapse:collapse;font-size:var(--small)} th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:start;vertical-align:top} th{color:var(--ink-2);font-weight:600}
tr.ok{background:color-mix(in srgb,var(--primary) 8%,transparent)}
td a{color:var(--ink);font-weight:600;text-decoration:none} td a:hover{color:var(--primary)}
.w{font-size:var(--chip);padding:1px 8px;border-radius:var(--r-full);border:1px solid var(--line-strong)} .w.psy{border-color:var(--fam-psy)} .w.tabar{border-color:var(--fam-bio)} .w.soc{border-color:var(--fam-soc)} .w.phil{border-color:var(--fam-hum)}
.fl{font-size:var(--chip);color:#6B4E00} input[type=checkbox]{width:18px;height:18px;accent-color:var(--primary)}
textarea{width:100%;min-height:90px;font:inherit;font-size:var(--small);padding:10px;border-radius:var(--r-md);border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);direction:ltr}
.exp{display:grid;gap:8px;margin-top:var(--s6)} .exp .row{display:flex;gap:8px;flex-wrap:wrap}
.exp button{font:inherit;font-size:var(--small);padding:8px 16px;border-radius:var(--r-full);border:1px solid var(--primary);background:var(--primary);color:#fff;cursor:pointer}
.exp button.ghost{background:transparent;color:var(--primary)}
footer.foot{border-top:1px solid var(--line);padding-block:var(--s8);color:var(--ink-3);font-size:var(--small)}
</style></head><body>
<header class="top"><div class="wrap"><a class="brand" href="../"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 7l8-4 8 4-8 4-8-4z"/><path d="M4 12l8 4 8-4"/><path d="M4 17l8 4 8-4"/></svg><span>دانش‌سرا</span></a><span style="font-size:var(--small);color:var(--ink-2)">صف بازبینی</span></div></header>
<main class="wrap">
<h1>صف بازبینی</h1>
<p class="lead">همهٔ مدخل‌ها و یادداشت‌هایی که هنوز «پیش‌نویس»اند، یک‌جا. هر کدام را باز کنید، با چک‌لیست زیر بسنجید، و اگر قابل انتشار است تیک بزنید. تیک‌ها فقط در همین مرورگر ذخیره می‌شوند؛ در پایان «کپی فهرست تأییدشده‌ها» را بزنید و متن را برای من بفرستید تا وضعیتشان را به «بازبینی‌شده» تغییر دهم. اگر چیزی باید اصلاح شود، شناسه و نکته را در یادداشت پایین بنویسید.</p>
<div class="card check"><b>چک‌لیست پنج‌گانه</b><ol><li>هر گزاره منبع دارد و منبع واقعاً همان را می‌گوید (یک نمونه را تصادفی باز کنید).</li><li>یافته‌های تکرارنشده یا محل بحث پرچم خورده‌اند و با «قطعی» نوشته نشده‌اند.</li><li>زبان ساده و دقیق است؛ هیچ تشخیص یا توصیهٔ فردی (از جمله دوز دارو) ندارد.</li><li>پیوندها به مدخل درست می‌روند و نوع رابطه معنادار است.</li><li>اگر دربارهٔ ایران است: سال، روش و ردهٔ داده درست و محتاطانه است.</li></ol></div>
<div class="bar" id="bar"></div>
<table><thead><tr><th></th><th>مدخل</th><th>ویکی</th><th>گزاره</th><th>منبع</th><th>پرچم</th></tr></thead><tbody id="tb"></tbody></table>
<div class="exp"><b>یادداشت اصلاحات (شناسه: نکته)</b><textarea id="notes" placeholder="soc:anomie: مثال سوم مبهم است&#10;tabar:consanguinity: رقم ۳۸٫۶ را با منبع جدیدتر مقایسه کنید"></textarea>
<div class="row"><button id="copy">کپی فهرست تأییدشده‌ها + یادداشت</button><button class="ghost" id="clear">پاک کردن تیک‌ها</button><span id="msg" style="align-self:center;color:var(--ink-3);font-size:var(--small)"></span></div></div>
</main>
<footer class="foot"><div class="wrap">این صفحه فقط برای بازبین است؛ هیچ داده‌ای به سرور نمی‌رود.</div></footer>
<script>
const D = __DATA__; const WN = {psy:"روان",tabar:"تبار",soc:"جامعه",phil:"فلسفه",atlas:"پل",iran:"ایران"};
let w = ""; let ok = {}; try { ok = JSON.parse(localStorage.getItem("ds-review") || "{}"); } catch(_) {}
let notes = ""; try { notes = localStorage.getItem("ds-review-notes") || ""; } catch(_) {}
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fa = s => String(s).replace(/\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[d]);
function render(){
  const items = D.filter(x => !w || x.wiki === w); const done = D.filter(x => ok[x.id]).length;
  document.getElementById("bar").innerHTML = ["", "psy", "tabar", "soc", "phil", "atlas", "iran"].map(k => `<button data-w="${k}" aria-pressed="${w === k}">${k ? WN[k] : "همه"} <small>(${fa(D.filter(x => !k || x.wiki === k).length)})</small></button>`).join("") + `<span class="n">${fa(done)} از ${fa(D.length)} تأیید شده</span>`;
  document.getElementById("tb").innerHTML = items.map(x => `<tr class="${ok[x.id] ? "ok" : ""}"><td><input type="checkbox" data-id="${x.id}" ${ok[x.id] ? "checked" : ""} aria-label="تأیید"></td><td><a href="${x.url}" target="_blank" rel="noopener">${esc(x.title.fa)}</a><div style="font-size:var(--chip);color:var(--ink-3);direction:ltr;text-align:start">${esc(x.id)}</div></td><td><span class="w ${x.wiki}">${WN[x.wiki]}</span>${x.grade ? ` <span class="w">${x.grade}</span>` : ""}</td><td>${x.points ? fa(x.points) : "—"}</td><td>${fa(x.sources)}</td><td class="fl">${x.flags.map(f => ({contested:"محل بحث",unreplicated:"تکرارنشده","editor-note":"یادداشت",dated:"قدیمی"}[f] || f)).join("، ")}</td></tr>`).join("");
  document.getElementById("notes").value = notes;
}
document.addEventListener("click", ev => { const b = ev.target.closest("[data-w]"); if (b) { w = b.dataset.w; render(); } });
document.addEventListener("change", ev => { const c = ev.target.closest("[data-id]"); if (c) { if (c.checked) ok[c.dataset.id] = 1; else delete ok[c.dataset.id]; try { localStorage.setItem("ds-review", JSON.stringify(ok)); } catch(_) {} render(); } });
document.addEventListener("input", ev => { if (ev.target.id === "notes") { notes = ev.target.value; try { localStorage.setItem("ds-review-notes", notes); } catch(_) {} } });
document.getElementById("copy").addEventListener("click", async () => { const txt = "approved:\n" + Object.keys(ok).sort().join("\n") + "\n\nnotes:\n" + notes; const m = document.getElementById("msg"); try { await navigator.clipboard.writeText(txt); m.textContent = "کپی شد؛ همین متن را برای من بفرستید."; } catch(_) { const ta = document.getElementById("notes"); ta.value = txt; ta.select(); m.textContent = "کپی خودکار ممکن نبود؛ متن در کادر است، دستی کپی کنید."; } });
document.getElementById("clear").addEventListener("click", () => { ok = {}; try { localStorage.removeItem("ds-review"); } catch(_) {} render(); });
render();
</script></body></html>'''
open(f'{R}/core/review.html', 'w', encoding='utf-8').write(tpl.replace('__DATA__', json.dumps(items, ensure_ascii=False)))
print('review queue', len(items), 'items')
