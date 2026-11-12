# -*- coding: utf-8 -*-
"""Build simorgh/why.html — «چرا؟» cards: each of the 47 roles of the Iran Mafia table,
the research finding behind it and the Daneshsara entries that explain it. Data: plan.json (why)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
D = json.load(open(f'{R}/data/plan/plan.json', encoding='utf-8'))
DATA = json.dumps(D['why'], ensure_ascii=False)
TPL = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>چرا؟ علم پشت هر نقش | سیمرغ | دانش‌سرا</title>
<meta name="description" content="چهل و هفت نقش میز مافیای ایران، هرکدام با یافتهٔ پژوهشی پشتش و مدخل‌های دانش‌سرا که توضیحش می‌دهند.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
:root{--c:#b7791f;--mafia:var(--err);--citizen:var(--primary);--third:var(--c)}
main{padding-block:var(--s5) var(--s10)}
h1{font-size:var(--h1);margin:var(--s4) 0 var(--s2);line-height:var(--lh-tight)}
.lead{color:var(--ink-2);max-width:62ch;line-height:1.9;margin:0 0 var(--s4)}
.lay{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,400px);gap:18px;align-items:start}
@media (max-width:900px){.lay{grid-template-columns:minmax(0,1fr)}}
.team{margin:0 0 var(--s4)}.team h2{font-size:1rem;margin:0 0 8px;color:var(--k)}
.rs{display:flex;flex-wrap:wrap;gap:6px}
.r{font:inherit;font-size:.88rem;min-height:40px;padding:6px 12px;border-radius:99px;border:1px solid var(--line-strong);border-inline-start:4px solid var(--k);background:var(--surface);color:var(--ink);cursor:pointer}
.r[aria-pressed=true]{background:var(--k);border-color:var(--k);color:#fff;font-weight:650}
.card{position:sticky;top:12px;padding:18px;border-radius:18px;border:2px solid var(--k,var(--c));background:var(--surface);display:grid;gap:10px;line-height:1.9}
.card h2{margin:0;font-size:1.35rem;color:var(--k)}.card h2 small{display:block;font-size:.8rem;font-weight:400;color:var(--ink-3)}
.sci{padding:12px 14px;border-radius:12px;background:var(--surface-subtle);border-inline-start:4px solid var(--k);font-size:1rem}
.sci small{display:block;color:var(--ink-3);font-size:.76rem}
.ls{display:grid;gap:6px}
.ls a{padding:8px 12px;border-radius:12px;border:1px solid var(--line);text-decoration:none;color:var(--ink);font-size:.9rem;line-height:1.7}
.ls a:hover{border-color:var(--k);color:var(--k)}
.ls a.out{color:var(--ink-2);border-style:dashed}
.red{padding:12px 16px;border-radius:14px;border:1.5px dashed var(--err);background:color-mix(in srgb,var(--err) 5%,var(--paper));font-size:.88rem;line-height:1.9;max-width:760px;margin-top:var(--s4)}
</style>
</head>
<body>
<main class="wrap" id="main">
<h1>چرا؟ علم پشت هر نقش</h1>
<p class="lead">میز مافیای ایران چهل و هفت نقش دارد. روی هر نقش بزنید تا ببینید پژوهش دربارهٔ آن چه می‌گوید و کدام مدخل دانش‌سرا توضیحش می‌دهد.</p>
<div class="lay"><div id="teams"></div><aside class="card" id="card" aria-live="polite"></aside></div>
<div class="red"><b>نقش یعنی جایگاه، نه آدم.</b> این‌ها دسته‌های جمعیتی‌اند برای فهمیدن سازوکارها. هیچ نقشی برچسب یک فرد واقعی نیست، و بیشتر آدم‌ها هم‌زمان در چند نقش‌اند.</div>
<p class="lead" style="margin-top:var(--s4);font-size:.9rem">توضیح کامل هر نقش (قدرت، ضعف، شرط برد): <a href="https://maryamjaberi.github.io/simorgh/roles.html">میز مافیای ایران ↗</a> · بازی به زبان علم: <a href="plan.html#game">نقشهٔ کلان</a></p>
</main>
<script>
const W = __DATA__, $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const fa = n => String(n).replace(/\d/g, c => "۰۱۲۳۴۵۶۷۸۹"[c]);
const T = {mafia: ["تیم حاکم", "--mafia"], citizen: ["تیم شهروند", "--citizen"], third: ["نقش‌های سوم: بیرون از دو تیم", "--third"]};
let sel = 0;
function list(){
  $("teams").innerHTML = Object.keys(T).map(t => { const L = W.map((w, i) => [w, i]).filter(([w]) => w[0] === t);
    return `<div class="team" style="--k:var(${T[t][1]})"><h2>${T[t][0]} <small style="font-weight:400;color:var(--ink-3)">${fa(L.length)} نقش</small></h2><div class="rs">${L.map(([w, i]) => `<button type="button" class="r" data-i="${i}" aria-pressed="${i === sel}">${esc(w[1])}</button>`).join("")}</div></div>`; }).join("");
}
function card(){
  const w = W[sel];
  $("card").style.setProperty("--k", `var(${T[w[0]][1]})`);
  $("card").innerHTML = `<h2>${esc(w[1])}<small>${esc(T[w[0]][0].split(":")[0])} · ${esc(w[2])}</small></h2>
    <div class="sci"><small>پژوهش چه می‌گوید</small>${esc(w[3])}</div>
    <div class="ls">${w[4].map(l => `<a href="${l[1]}">${esc(l[0])} ←</a>`).join("")}<a class="out" href="https://maryamjaberi.github.io/simorgh/roles.html">این نقش روی میز مافیای ایران ↗</a></div>`;
}
function pick(i, scroll){ sel = i; try { history.replaceState(null, "", "#r" + i); } catch (_) {} list(); card(); if (scroll && innerWidth < 900) $("card").scrollIntoView({behavior: "smooth", block: "start"}); }
$("teams").addEventListener("click", e => { const b = e.target.closest("[data-i]"); if (b) pick(+b.dataset.i, true); });
const h = /^#r(\d+)$/.exec(location.hash); pick(h && W[+h[1]] ? +h[1] : 12, false);
</script>
</body>
</html>
'''
open(f'{R}/simorgh/why.html', 'w', encoding='utf-8').write(TPL.replace('__DATA__', DATA))
print(f'simorgh/why.html: {len(D["why"])} roles')
