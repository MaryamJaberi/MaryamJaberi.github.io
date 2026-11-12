# -*- coding: utf-8 -*-
"""Build miyan/roots.html — «ریشه‌یابی آسیب»: causal chains from social roots to harms and outcomes,
with evidence grades, Iran data, turning points and a population-attributable-fraction calculator.
Data: data/flows/*.json (one chain per file) + data/flows/_candidates.json."""
import json, glob, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
load = lambda p: json.load(open(p, encoding='utf-8'))
flows = sorted([load(p) for p in glob.glob(f'{R}/data/flows/*.json') if not p.endswith('_candidates.json')], key=lambda f: f['order'])
cand = load(f'{R}/data/flows/_candidates.json')
reg = load(f'{R}/core/registry.json')['entries']
iran = {}
for f in flows:
    for n in f['nodes']:
        for w in n['wiki'] + f['wiki']:
            assert w in reg, f'{f["id"]}: unknown entry {w}'
        if n.get('iran'):
            d = load(f'{R}/iran/{n["iran"].split(":")[1]}.json')
            iran[d['id']] = {'q': d['question']['fa'], 'f': d['finding']['fa'], 'g': d['grade'], 'y': d['year']}
titles = {w: {'t': reg[w]['title']['fa'], 'u': '../' + reg[w]['url']} for f in flows for n in f['nodes'] for w in n['wiki'] + f['wiki']}
# Where each chain sits in the whole project: wikis, Iran notes, Sakht organs it touches.
organs = load(f'{R}/data/sakht/sakht.json')['organs']
WN = {'psy': 'روان', 'soc': 'جامعه', 'phil': 'فلسفه', 'tabar': 'تبار', 'tarikh': 'تاریخ', 'miyan': 'میان‌رشته', 'din': 'دین'}
WU = {'psy': '../psy/', 'soc': '../soc/', 'phil': '../phil/', 'tabar': '../tabar/', 'tarikh': '../tarikh/', 'miyan': './'}
for f in flows:
    ids = {w for n in f['nodes'] for w in n['wiki']} | set(f['wiki'])
    f['place'] = {
        'wikis': [[k, WN.get(k, k), WU.get(k, '../')] for k in sorted({w.split(':')[0] for w in ids})],
        'iran': sorted({n['iran'] for n in f['nodes'] if n.get('iran')}),
        'sakht': [o['k'] for o in organs if ids & set(o.get('wiki', []))],
    }
DATA = json.dumps({'flows': flows, 'cand': cand, 'iran': iran, 'wiki': titles}, ensure_ascii=False)

TPL = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>ریشه‌یابی آسیب | میان‌رشته | دانش‌سرا</title>
<meta name="description" content="زنجیره‌های علّی از ریشه‌های اجتماعی تا آسیب و پیامد، با ردهٔ شواهد، دادهٔ ایران، نقطه‌های عطف و سنجش سهم جمعیتی خطر.">
<link rel="stylesheet" href="../core/design/tokens.css">
<link rel="stylesheet" href="../core/tools/tools.css">
<style>
:root{--l0:var(--fam-soc);--l1:var(--fam-hum);--l2:var(--warn);--l3:var(--err)}
body{background:var(--paper);color:var(--ink)}
.what{font-size:1.05rem;color:var(--ink-2);max-width:72ch;line-height:1.9;margin:0 0 14px}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:.85rem;color:var(--ink-2);margin:0 0 16px}
.g{display:inline-grid;place-items:center;min-width:1.7em;height:1.7em;border-radius:6px;font-weight:700;font-size:.78rem;color:#fff;font-family:var(--f-ui,inherit)}
.gA{background:var(--ok)}.gB{background:var(--fam-soc)}.gC{background:var(--warn)}.gD{background:var(--ink-3)}
.flows{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}
.flows button{font:inherit;font-size:.92rem;min-height:44px;padding:6px 14px;border-radius:999px;border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer;text-align:start}
.flows button[aria-pressed=true]{background:var(--fam-soc-soft);border-color:var(--fam-soc);color:var(--fam-soc);font-weight:700}
.flows small{color:var(--ink-3);font-weight:400}
.head h2{margin:0 0 6px;font-size:1.5rem;text-wrap:balance}
.head .q{color:var(--ink-2);margin:0 0 8px;font-style:italic}
.head p{max-width:72ch;line-height:1.9;margin:0 0 8px}
.place{display:grid;gap:6px;margin:4px 0 16px;padding:10px 14px;border-radius:14px;border:1px dashed var(--line-strong);background:var(--surface-subtle);font-size:.86rem;line-height:1.7}
.place>div{display:flex;flex-wrap:wrap;gap:5px;align-items:center}.place span{color:var(--ink-3);margin-inline-end:4px}
.place a{padding:1px 9px;border-radius:999px;border:1px solid var(--line-strong);color:var(--ink-2);text-decoration:none}.place a:hover{border-color:var(--fam-soc);color:var(--fam-soc)}
.wl{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 16px}
.wl a{font-size:.83rem;padding:2px 10px;border-radius:999px;border:1px solid var(--line-strong);color:var(--ink-2);text-decoration:none}
.wl a:hover{border-color:var(--fam-soc);color:var(--fam-soc)}
.lay{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px;align-items:start}
.cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.col h3{margin:0 0 8px;font-size:.88rem;padding:6px 10px;border-radius:10px;background:var(--surface-subtle);border-inline-start:4px solid var(--c)}
.col{display:grid;gap:8px;align-content:start}
.nd{font:inherit;text-align:start;display:grid;gap:4px;padding:9px 11px;border-radius:12px;border:1px solid var(--line);border-inline-start:4px solid var(--c);background:var(--surface);color:var(--ink);cursor:pointer;line-height:1.6;font-size:.9rem;transition:opacity .15s,box-shadow .15s}
.nd .bd{display:flex;gap:4px;flex-wrap:wrap}
.nd .bd span{font-size:.7rem;padding:0 7px;border-radius:99px;border:1px solid var(--line-strong);color:var(--ink-2)}
.nd .bd .lv{border-color:var(--ok);color:var(--ok)}
.nd.on,.nd[aria-pressed=true]{box-shadow:0 0 0 2px var(--ink);background:var(--surface);color:var(--ink)}
.nd.up{box-shadow:0 0 0 2px var(--c)}
.nd.dn{box-shadow:0 0 0 2px var(--c)}
.dim .nd:not(.on):not(.up):not(.dn){opacity:.32}
.side{position:sticky;top:12px;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:14px 16px;display:grid;gap:10px;line-height:1.8;font-size:.92rem;max-height:calc(100vh - 24px);overflow:auto}
.side h4{margin:0;font-size:1.05rem}
.side ul{margin:0;padding-inline-start:18px}
.side .ir{background:var(--surface-subtle);border-radius:10px;padding:8px 10px;font-size:.86rem}
.side .muted{color:var(--ink-3);font-size:.85rem}
.sec{margin-top:26px}
.sec h3{font-size:1.2rem;margin:0 0 8px}
.loops{display:grid;gap:8px}
.loops button{font:inherit;text-align:start;min-height:44px;padding:8px 12px;border-radius:12px;border:1px dashed var(--err);background:var(--surface);color:var(--ink);cursor:pointer}
.lv-wrap{overflow-x:auto}
table.lv{border-collapse:collapse;width:100%;font-size:.88rem;min-width:720px}
table.lv th,table.lv td{border-bottom:1px solid var(--line);padding:8px;text-align:start;vertical-align:top;line-height:1.7}
table.lv th{color:var(--ink-2);font-weight:600;background:var(--surface-subtle)}
.dots{white-space:nowrap;letter-spacing:2px;color:var(--ok)}
.calc{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px;display:grid;gap:12px}
.calc label{display:grid;gap:4px;font-size:.9rem;color:var(--ink-2)}
.calc input[type=range]{width:100%;direction:ltr;accent-color:var(--fam-soc);min-height:30px}
.calc .big{font-size:1.7rem;font-weight:700;color:var(--fam-soc)}
.row2{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr))}
.cand{display:grid;gap:6px;margin:0;padding-inline-start:18px;line-height:1.8}
.cand small{color:var(--ink-3)}
.toggle{font:inherit;font-size:.85rem;min-height:36px;padding:2px 12px;border-radius:999px;border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer}
.toggle[aria-pressed=true]{background:var(--ok);color:#fff;border-color:var(--ok)}
@media (max-width:980px){.lay{grid-template-columns:minmax(0,1fr)}.side{position:static;max-height:none}}
@media (max-width:640px){.cols{grid-template-columns:minmax(0,1fr)}}
</style>
</head>
<body>
<main class="wrap" id="main">
<h1>ریشه‌یابی آسیب</h1>
<p class="what">هر آسیب اجتماعی یک زنجیره است: ریشه‌هایی در قانون، اقتصاد، آموزش و باورها؛ سازوکارهایی در خانه و محله؛ آسیبی که به فرد می‌رسد؛ و پیامدهایی که اغلب دوباره ریشهٔ نسل بعد می‌شوند. روی هر حلقه بزنید تا ببینید از کجا می‌آید و به کجا می‌رود، چه داده‌ای از ایران داریم، و کجا می‌شود زنجیره را شکست. این نقشه‌ها برای فهم و اولویت‌بندی در سطح جمعیت‌اند، نه برای داوری دربارهٔ یک فرد یا یک خانواده.</p>
<div class="legend" aria-label="ردهٔ شواهد پیوندها"><span><b class="g gA">A</b> شواهد قوی (فراتحلیل یا کارآزمایی)</span><span><b class="g gB">B</b> شواهد خوب (پژوهش‌های طولی و تکرارشده)</span><span><b class="g gC">C</b> شواهد محدود</span><span><b class="g gD">D</b> نظری</span></div>
<div class="flows" id="flows" role="tablist" aria-label="زنجیره‌ها"></div>
<section id="flow" aria-live="polite"></section>
<section class="sec"><h3>زنجیره‌هایی که هنوز ساخته نشده‌اند</h3><p class="muted" style="margin:0 0 8px;color:var(--ink-2)">پیشنهاد برای پژوهش بعدی؛ هر کدام پیش از ساختن به داده و منبع نیاز دارد.</p><ol class="cand" id="cand"></ol></section>
<div class="note foot" role="note" style="margin-top:28px">ردهٔ هر پیوند جمع‌بندی ویراستار از شواهد موجود است و بیشتر پیوندها از پژوهش‌های هم‌بستگی آمده‌اند. ترتیب «اولویت پیشنهادی» با یک قاعدهٔ ساده و آشکار ساخته شده (شواهد، هزینه، زمان و پیشینه در ایران) و جای بحث و بازنگری دارد.</div>
</main>
<footer class="foot"><div class="wrap">دانش‌سرا · پیش‌نویس · ریشه‌یابی آسیب</div></footer>
<script>
const D = __DATA__;
const fa = (x, d = 0) => (typeof x === "number" ? x.toLocaleString("en-US", {maximumFractionDigits: d}) : String(x)).replace(/,/g, "٬").replace(/\./g, "٫").replace(/\d/g, c => "۰۱۲۳۴۵۶۷۸۹"[c]);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const LAYERS = [["ریشه‌ها: قانون، اقتصاد، باور", "--l0"], ["سازوکار: خانه و محله", "--l1"], ["آسیب به فرد", "--l2"], ["پیامد برای بزرگسال و جامعه", "--l3"]];
const GW = {A: 3, B: 2, C: 1, D: 0}, CW = {"کم": 2, "متوسط": 1, "زیاد": 0}, TW = {"کوتاه": 2, "میان": 1, "بلند": 0};
const wl = ids => `<div class="wl">${ids.filter((x, i) => ids.indexOf(x) === i && D.wiki[x]).map(x => `<a href="${D.wiki[x].u}">${esc(D.wiki[x].t)}</a>`).join("")}</div>`;
let F = null, sel = null, cheap = false;
const place = P => `<div class="place"><b>جای این زنجیره در دانش‌سرا</b>
  <div><span>ویکی‌ها:</span> ${P.wikis.map(w => `<a href="${w[2]}">${esc(w[1])}</a>`).join("")}</div>
  ${P.iran.length ? `<div><span>یادداشت‌های ایران:</span> ${P.iran.map(i => `<a href="../iran/#${i.split(":")[1]}">${esc(D.iran[i] ? D.iran[i].q : i)}</a>`).join("")}</div>` : ""}
  ${P.sakht.length ? `<div><span>ساخت ایران:</span> ${P.sakht.map(k => `<a href="../sakht/#organs">${esc(k)}</a>`).join("")}</div>` : `<div><span>ساخت ایران:</span> <a href="../sakht/">هنوز به اندامی وصل نشده</a></div>`}
</div>`;

const fl = document.getElementById("flows");
fl.innerHTML = D.flows.map(f => `<button type="button" data-f="${f.id}">${esc(f.title)}${f.status === "full" ? "" : " <small>· پیش‌نویس</small>"}</button>`).join("");
fl.addEventListener("click", e => { const b = e.target.closest("[data-f]"); if (b) open(b.dataset.f); });
document.getElementById("cand").innerHTML = D.cand.map(c => `<li>${esc(c[0])} <small>— ${esc(c[1])}</small></li>`).join("");

function open(id){
  F = D.flows.find(f => f.id === id) || D.flows[0]; sel = null;
  fl.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b.dataset.f === F.id));
  try { history.replaceState(null, "", "#" + F.id); } catch (_) {}
  const lvAt = new Set(F.levers.flatMap(v => v.at));
  const node = n => `<button type="button" class="nd" data-n="${n.id}" style="--c:var(${LAYERS[n.l][1]})"><span>${esc(n.t)}</span><span class="bd">${n.iran && D.iran[n.iran] ? `<span>دادهٔ ایران · ${D.iran[n.iran].g}</span>` : ""}${lvAt.has(n.id) ? `<span class="lv">نقطهٔ عطف</span>` : ""}</span></button>`;
  document.getElementById("flow").innerHTML = `<div class="head"><h2>${esc(F.title)}</h2><p class="q">${esc(F.q)}</p><p>${esc(F.summary)}</p>${wl(F.wiki)}${place(F.place)}</div>
    <div class="lay"><div class="cols" id="cols">${LAYERS.map((L, i) => `<div class="col" style="--c:var(${L[1]})"><h3>${L[0]}</h3>${F.nodes.filter(n => n.l === i).map(node).join("")}</div>`).join("")}</div>
    <aside class="side" id="side" aria-live="polite"></aside></div>
    ${F.loops.length ? `<div class="sec"><h3>حلقه‌ها: جایی که پیامد دوباره ریشه می‌شود</h3><div class="loops">${F.loops.map(l => `<button type="button" data-loop="${l[0]}|${l[1]}">↺ ${esc(nm(l[0]))} ← ${esc(nm(l[1]))}: ${esc(l[2])}</button>`).join("")}</div></div>` : ""}
    <div class="sec"><h3>نقطه‌های عطف، به ترتیب اولویت پیشنهادی</h3>
    <p style="margin:0 0 8px;color:var(--ink-2);font-size:.9rem">امتیاز = شواهد (۰ تا ۳) + هزینهٔ کم (۰ تا ۲) + اثر زود (۰ تا ۲) + پیشینه در ایران یا جهان (۰ یا ۱). <button type="button" class="toggle" id="cheap" aria-pressed="false">فقط کم‌هزینه‌ها</button></p>
    <div class="lv-wrap" id="levers"></div></div>
    ${F.risk ? `<div class="sec"><h3>سنجش سهم جمعیتی خطر</h3><div class="calc" id="calc"></div></div>` : ""}`;
  document.getElementById("cols").addEventListener("click", e => { const b = e.target.closest("[data-n]"); if (b) pick(b.dataset.n); });
  document.querySelectorAll("[data-loop]").forEach(b => b.addEventListener("click", () => { const [a, c] = b.dataset.loop.split("|"); pick(a, c); }));
  document.getElementById("cheap").addEventListener("click", e => { cheap = !cheap; e.target.setAttribute("aria-pressed", cheap); levers(); });
  levers(); if (F.risk) calc(); side();
}
const nm = id => (F.nodes.find(n => n.id === id) || {t: id}).t;
function reach(id, dir){ const seen = new Set(), st = [id]; while (st.length) { const x = st.pop(); for (const e of F.edges) { const [a, b] = dir > 0 ? [e[0], e[1]] : [e[1], e[0]]; if (a === x && !seen.has(b)) { seen.add(b); st.push(b); } } } return seen; }
function pick(id, also){
  sel = sel === id && !also ? null : id;
  const cols = document.getElementById("cols");
  cols.classList.toggle("dim", !!sel);
  const up = sel ? reach(sel, -1) : new Set(), dn = sel ? reach(sel, 1) : new Set();
  if (also) dn.add(also);
  cols.querySelectorAll(".nd").forEach(b => { const n = b.dataset.n; b.classList.toggle("on", n === sel); b.classList.toggle("up", up.has(n)); b.classList.toggle("dn", dn.has(n)); b.setAttribute("aria-pressed", n === sel); });
  side();
  if (sel && innerWidth < 980) document.getElementById("side").scrollIntoView({behavior: "smooth", block: "nearest"});
}
function side(){
  const s = document.getElementById("side");
  if (!sel) { s.innerHTML = `<h4>یک حلقه را انتخاب کنید</h4><p class="muted" style="margin:0">با انتخاب هر حلقه، همهٔ ریشه‌هایی که به آن می‌رسند و همهٔ پیامدهایی که از آن می‌آیند پررنگ می‌شوند. برچسب «نقطهٔ عطف» یعنی برای آن حلقه اهرم تغییر پیشنهاد شده است.</p><p class="muted" style="margin:0">${fa(F.nodes.length)} حلقه · ${fa(F.edges.length)} پیوند · ${fa(F.levers.length)} نقطهٔ عطف</p>`; return; }
  const n = F.nodes.find(x => x.id === sel);
  const inn = F.edges.filter(e => e[1] === sel), out = F.edges.filter(e => e[0] === sel);
  const li = (e, k) => `<li><b class="g g${e[2]}">${e[2]}</b> ${esc(nm(e[k]))}${e[3] ? ` <span class="muted">— ${esc(e[3])}</span>` : ""}</li>`;
  const ir = n.iran && D.iran[n.iran];
  const lv = F.levers.filter(v => v.at.includes(sel));
  s.innerHTML = `<h4>${esc(n.t)}</h4>${n.d ? `<p style="margin:0">${esc(n.d)}</p>` : ""}
    ${inn.length ? `<div><b>از کجا می‌آید</b><ul>${inn.map(e => li(e, 0)).join("")}</ul></div>` : ""}
    ${out.length ? `<div><b>به کجا می‌رسد</b><ul>${out.map(e => li(e, 1)).join("")}</ul></div>` : ""}
    ${ir ? `<div class="ir"><b>ایران (ردهٔ داده ${ir.g}، ${fa(ir.y)}):</b> ${esc(ir.f)} <a href="../iran/#${n.iran.split(":")[1]}">برگهٔ ایران</a></div>` : ""}
    ${lv.length ? `<div><b>نقطهٔ عطف</b><ul>${lv.map(v => `<li>${esc(v.t)} <span class="muted">(شواهد ${v.ev})</span></li>`).join("")}</ul></div>` : ""}
    ${n.wiki.length ? wl(n.wiki) : ""}`;
}
function levers(){
  const sc = v => GW[v.ev] + CW[v.cost] + TW[v.time] + (v.precedent ? 1 : 0);
  const L = F.levers.filter(v => !cheap || v.cost === "کم").slice().sort((a, b) => sc(b) - sc(a));
  document.getElementById("levers").innerHTML = L.length ? `<table class="lv"><thead><tr><th>اهرم</th><th>روی کدام حلقه</th><th>شواهد</th><th>هزینه</th><th>زمان اثر</th><th>وضع در ایران</th><th>پیشینه</th><th>امتیاز</th></tr></thead><tbody>${L.map(v => `<tr><td><b>${esc(v.t)}</b>${v.d ? `<br><span style="color:var(--ink-2)">${esc(v.d)}</span>` : ""}</td><td>${v.at.map(a => esc(nm(a))).join("، ")}</td><td><b class="g g${v.ev}">${v.ev}</b></td><td>${esc(v.cost)}</td><td>${esc(v.time)}</td><td>${esc(v.iran || "—")}</td><td>${esc(v.precedent || "—")}</td><td><span class="dots" aria-label="${fa(sc(v))} از ۸">${"●".repeat(sc(v))}${"○".repeat(8 - sc(v))}</span></td></tr>`).join("")}</tbody></table>` : `<p>اهرم کم‌هزینه‌ای برای این زنجیره ثبت نشده.</p>`;
}
function calc(){
  const r = F.risk, c = document.getElementById("calc");
  c.innerHTML = `<p style="margin:0;line-height:1.9">اگر «${esc(r.exposure)}» علت واقعی بخشی از «${esc(r.outcome)}» باشد، چه سهمی از آن پیامد در کل جمعیت به همین عامل برمی‌گردد؟ این «کسر منتسب به جمعیت» است: PAF = p(RR−1) / [1 + p(RR−1)].</p>
    <div class="row2"><label>شیوع عامل خطر در جمعیت (p): <b id="pv"></b><input type="range" id="p" min="1" max="40" step="1" value="${r.p}"></label>
    <label>خطر نسبی (RR): <b id="rv"></b><input type="range" id="r" min="1" max="15" step="0.5" value="${r.rr}"></label>
    <label>اگر سیاست‌ها شیوع را این‌قدر کم کنند: <b id="dv"></b><input type="range" id="d" min="0" max="100" step="5" value="30"></label></div>
    <div class="row2"><div>سهم منتسب به این عامل<div class="big" id="paf"></div></div><div>کاهش پیش‌بینی‌شدهٔ پیامد<div class="big" id="cut"></div></div></div>
    <p style="margin:0;font-size:.85rem;color:var(--ink-2)">${esc(r.rrnote)}. ${esc(r.pnote)} محاسبه فرض می‌کند رابطه علّی است و عوامل مخدوش‌کننده کنترل شده‌اند؛ برای همین این عددها مرتبهٔ بزرگی را نشان می‌دهند، نه پیش‌بینی دقیق.</p>`;
  const $ = s => c.querySelector(s);
  const run = () => { const p = +$("#p").value / 100, RR = +$("#r").value, d = +$("#d").value / 100, p2 = p * (1 - d);
    const paf = p * (RR - 1) / (1 + p * (RR - 1)), cut = 1 - (1 + p2 * (RR - 1)) / (1 + p * (RR - 1));
    $("#pv").textContent = fa(p * 100) + "٪"; $("#rv").textContent = fa(RR, 1) + " برابر"; $("#dv").textContent = fa(d * 100) + "٪";
    $("#paf").textContent = fa(paf * 100) + "٪"; $("#cut").textContent = fa(cut * 100, 1) + "٪"; };
  c.querySelectorAll("input").forEach(i => i.addEventListener("input", run)); run();
}
open((location.hash || "").slice(1) || D.flows[0].id);
addEventListener("hashchange", () => { const k = location.hash.slice(1); if (F && k !== F.id && D.flows.some(f => f.id === k)) open(k); });
</script>
</body>
</html>
'''
open(f'{R}/miyan/roots.html', 'w', encoding='utf-8').write(TPL.replace('__DATA__', DATA))
print(f'miyan/roots.html: {len(flows)} chains, {sum(len(f["nodes"]) for f in flows)} nodes, {sum(len(f["levers"]) for f in flows)} levers')
