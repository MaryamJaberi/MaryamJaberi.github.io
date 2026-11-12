# -*- coding: utf-8 -*-
"""Build simorgh/birds.html — the bird cards: one card per bird with goal, damages it repairs,
safe step today, freedom-day role and first-100-days role. Data: data/plan/plan.json (bird_cards)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
D = json.load(open(f'{R}/data/plan/plan.json', encoding='utf-8'))
DATA = json.dumps({'birds': D['birds'], 'cards': D['bird_cards'], 'tasks': D['tasks'], 'risks': D['risks']}, ensure_ascii=False)
TPL = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>کارت‌های سی مرغ | سیمرغ | دانش‌سرا</title>
<meta name="description" content="سی مرغ، سی گروه سازنده: هدف هرکدام، ویرانی‌هایی که ترمیم می‌کند، قدم امن امروز، نقش روز آزادی و صد روز اول.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
:root{--c:#b7791f}
main{padding-block:var(--s5) var(--s10)}
h1{font-size:var(--h1);margin:var(--s4) 0 var(--s2);line-height:var(--lh-tight)}
.lead{color:var(--ink-2);max-width:60ch;line-height:1.9;margin:0 0 var(--s4)}
.flt{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 var(--s4)}
.flt button{font:inherit;font-size:.88rem;min-height:40px;padding:6px 14px;border-radius:99px;border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer}
.flt button[aria-pressed=true]{background:var(--c);border-color:var(--c);color:#fff;font-weight:650}
.lay{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,400px);gap:18px;align-items:start}
@media (max-width:900px){.lay{grid-template-columns:minmax(0,1fr)}}
.fam{margin:0 0 var(--s4)}.fam h2{font-size:1rem;margin:0 0 8px;color:var(--k)}
.bs{display:grid;grid-template-columns:repeat(auto-fill,minmax(128px,1fr));gap:8px}
.b{font:inherit;text-align:start;display:grid;gap:4px;padding:12px;border-radius:14px;border:1px solid var(--line);border-top:4px solid var(--k);background:var(--surface);color:var(--ink);cursor:pointer;line-height:1.6;min-height:84px;align-content:start}
.b b{font-size:.95rem}.b small{color:var(--ink-3);font-size:.76rem}
.b[aria-pressed=true]{box-shadow:0 0 0 2px var(--k)}
.b.off{opacity:.3}
.card{position:sticky;top:12px;padding:18px;border-radius:18px;border:2px solid var(--k,var(--c));background:var(--surface);display:grid;gap:10px;line-height:1.85;max-height:calc(100vh - 24px);overflow:auto}
.card h2{margin:0;font-size:1.4rem;color:var(--k)}
.card .goal{font-size:1.05rem;font-weight:600}
.st{padding:10px 12px;border-radius:12px;background:var(--surface-subtle);border-inline-start:4px solid var(--k);font-size:.93rem}
.st small{display:block;color:var(--ink-3);font-size:.76rem}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips a,.chips span{font-size:.8rem;padding:2px 10px;border-radius:99px;border:1px solid var(--line-strong);color:var(--ink-2);text-decoration:none}
.chips a:hover{border-color:var(--k);color:var(--k)}
.card h3{margin:6px 0 0;font-size:.85rem;color:var(--ink-3);font-weight:600}
.card ul{margin:0;padding-inline-start:18px;font-size:.88rem;color:var(--ink-2)}
.note{font-size:.82rem;color:var(--ink-3);margin-top:var(--s4);max-width:62ch;line-height:1.9}
</style>
</head>
<body>
<main class="wrap" id="main">
<h1>کارت‌های سی مرغ</h1>
<p class="lead">هر مرغ یک گروه سازنده با یک هدف است. یکی را بردار و ببین امروز، روز آزادی و در صد روز اول چه می‌کند. فهرست زنده است و در طول راه عوض می‌شود.</p>
<div class="flt"><button type="button" id="fAll" aria-pressed="true">همهٔ مرغ‌ها</button><button type="button" id="fOpen" aria-pressed="false">بدون نیاز به تخصص</button></div>
<div class="lay"><div id="fams"></div><aside class="card" id="card" aria-live="polite"></aside></div>
<p class="note">قدم امروز همیشه کوچک، قانونی و کم‌خطر است، به‌ویژه برای کسی که داخل ایران است. انتخاب مرغ جایی ثبت نمی‌شود. تصویر کامل: <a href="plan.html">نقشهٔ کلان سیمرغ</a> · سهم خودت: <a href="plan.html#me">سهم من</a></p>
</main>
<script>
const D = __DATA__, $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const FAM = ["--fam-psy", "--fam-bio", "--fam-soc", "--fam-hum", "--fam-hist", "--fam-formal"];
const KOF = {}; D.birds.forEach((f, i) => f[1].forEach(b => KOF[b] = FAM[i]));
let sel = null, open = false;
function list(){
  $("fams").innerHTML = D.birds.map((f, i) => `<div class="fam" style="--k:var(${FAM[i]})"><h2>${esc(f[0])}</h2><div class="bs">${f[1].map(b => { const c = D.cards[b]; return `<button type="button" class="b${open && !c[5] ? " off" : ""}" data-b="${esc(b)}" aria-pressed="${b === sel}"><b>${esc(b)}</b><small>${esc(c[0])}</small></button>`; }).join("")}</div></div>`).join("");
}
function card(){
  const c = D.cards[sel], k = KOF[sel];
  const tasks = D.tasks.filter(t => t[3] === sel), risks = D.risks.filter(r => r[3] === sel);
  $("card").style.setProperty("--k", `var(${k})`);
  $("card").innerHTML = `<h2>${esc(sel)}</h2><div class="goal">${esc(c[0])}</div>
    <div class="chips">${c[1].map(x => `<a href="plan.html#ledger">${esc(x)}</a>`).join("")}${c[5] ? "<span>بدون نیاز به تخصص</span>" : "<span>با مهارت یا تخصص</span>"}</div>
    <div class="st"><small>قدم امن امروز</small>${esc(c[2])}</div>
    <div class="st"><small>روز آزادی</small>${esc(c[3])}</div>
    <div class="st"><small>صد روز اول</small>${esc(c[4])}</div>
    ${tasks.length ? `<h3>کارهای این مرغ در فهرست روز آزادی</h3><ul>${tasks.map(t => `<li>${esc(t[1])} <small>(${esc(t[0])})</small></li>`).join("")}</ul>` : ""}
    ${risks.length ? `<h3>خطرهایی که این مرغ پاسخگوست</h3><ul>${risks.map(r => `<li>${esc(r[0])}: ${esc(r[2])}</li>`).join("")}</ul>` : ""}
    ${c[6].length ? `<h3>دانش پشت این مرغ</h3><div class="chips">${c[6].map(l => `<a href="${l[1]}">${esc(l[0])}</a>`).join("")}</div>` : ""}`;
}
function pick(b, scroll){ sel = b; try { history.replaceState(null, "", "#" + encodeURIComponent(b)); } catch (_) {} list(); card(); if (scroll && innerWidth < 900) $("card").scrollIntoView({behavior: "smooth", block: "start"}); }
$("fams").addEventListener("click", e => { const b = e.target.closest("[data-b]"); if (b) pick(b.dataset.b, true); });
$("fAll").addEventListener("click", () => { open = false; $("fAll").setAttribute("aria-pressed", true); $("fOpen").setAttribute("aria-pressed", false); list(); });
$("fOpen").addEventListener("click", () => { open = true; $("fAll").setAttribute("aria-pressed", false); $("fOpen").setAttribute("aria-pressed", true); list(); });
let h = ""; try { h = decodeURIComponent(location.hash.slice(1)); } catch (_) {}
pick(D.cards[h] ? h : "همسایه‌یار محله", false);
</script>
</body>
</html>
'''
open(f'{R}/simorgh/birds.html', 'w', encoding='utf-8').write(TPL.replace('__DATA__', DATA))
print(f'simorgh/birds.html: {len(D["bird_cards"])} cards')
