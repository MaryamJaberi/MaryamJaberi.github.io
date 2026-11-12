# -*- coding: utf-8 -*-
"""Build atlas/library-plan.html «کتابخانهٔ دانش‌سرا» from data/library/library.json + halls.json.
Level 1: floor plan of halls. Level 2: a hall's bookcases and shelves with spines. Level 3: an item's panel with volumes,
copies, assessment and wiki entries. Drive ids never reach the page."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
load = lambda p: json.load(open(p, encoding='utf-8'))
LIB = load(f'{R}/data/library/library.json'); HALLS = load(f'{R}/data/library/halls.json')
reg = load(f'{R}/core/registry.json')['entries']
def eurl(u):
    w, s = u.split('/#') if '/#' in u else (u.split('/')[0], u.split('#')[-1])
    k = f'{w}:{s}'
    return '../' + reg[k]['url'] if k in reg else None
items = []
for it in LIB['items']:
    en = [[e[0], eurl(e[1])] for e in it.get('en') or [] if len(e) == 2 and eurl(e[1])]
    x = {k: it[k] for k in ('id', 't', 'a', 'hall', 'shelf', 'kind') if it.get(k)}
    x['s'] = it['shelf'].split(':')[1]
    for k in ('vols', 'tier', 'mb', 'copies', 'y', 'lv', 'pk', 'd', 'en', 'ch', 'as', 'inrepo'):
        if it.get(k): x[k] = it[k]
    if en: x['en'] = en
    else: x.pop('en', None)
    if it.get('page') and os.path.exists(f'{R}/psy/topics/{it["page"]}.html'): x['pg'] = f'../psy/topics/{it["page"]}.html'
    if x.get('as') and x['as'].get('en'): x['as'] = {k: v for k, v in x['as'].items() if k != 'en'}
    items.append(x)
DATA = json.dumps({'halls': HALLS, 'items': items, 'reception': len(LIB['reception']), 'files': LIB['source_files']}, ensure_ascii=False, separators=(',', ':'))

TPL = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>کتابخانهٔ دانش‌سرا | اطلس‌ها | دانش‌سرا</title>
<meta name="description" content="همهٔ کتاب‌ها، مجموعه‌های چندجلدی، جزوه‌ها و درس‌گفتارهای دانش‌سرا در تالارها و قفسه‌های موضوعی.">
<link rel="stylesheet" href="../core/design/tokens.css">
<link rel="stylesheet" href="../core/tools/tools.css">
<style>
:root{--wood:#6b4a2f;--wood-2:#7d5838;--wood-in:#e9dfcf;--plank:#5a3d26}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--wood:#3b2a1c;--wood-2:#4a3424;--wood-in:#26201a;--plank:#2c1f15}}
:root[data-theme=dark]{--wood:#3b2a1c;--wood-2:#4a3424;--wood-in:#26201a;--plank:#2c1f15}
body{background:var(--paper);color:var(--ink)}
.top{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:end;justify-content:space-between;margin:0 0 14px}
.what{font-size:1.02rem;color:var(--ink-2);max-width:70ch;line-height:1.9;margin:0}
.stats{display:flex;gap:18px;flex-wrap:wrap}
.stats div{display:grid;text-align:center;font-size:.8rem;color:var(--ink-2)}
.stats b{font-size:1.5rem;color:var(--ink);font-weight:700}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 16px}
.bar input{font:inherit;min-height:44px;padding:6px 14px;border-radius:999px;border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);min-width:min(100%,320px);flex:1 1 260px}
.chip{font:inherit;font-size:.88rem;min-height:40px;padding:4px 14px;border-radius:999px;border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer}
.chip[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.lcrumb{display:flex;gap:8px;align-items:center;margin:0 0 12px;font-size:.95rem}
.lcrumb button{font:inherit;background:none;border:0;color:var(--fam-soc);cursor:pointer;padding:6px 0;min-height:40px;text-decoration:underline}
/* level 1: floor plan */
.plan{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:14px;background:repeating-linear-gradient(90deg,var(--surface-subtle) 0 38px,var(--paper) 38px 40px);padding:14px;border-radius:18px;border:1px solid var(--line)}
.room{font:inherit;text-align:start;display:grid;gap:10px;align-content:start;padding:14px;border-radius:14px;border:2px solid var(--c);background:var(--surface);color:var(--ink);cursor:pointer;box-shadow:0 2px 0 var(--line)}
.room:hover,.room:focus-visible{box-shadow:0 0 0 3px var(--c)}
.room h2{margin:0;font-size:1.15rem;color:var(--c)}
.room .n{font-size:.82rem;color:var(--ink-2)}
.mini{display:grid;gap:5px}
.mini .mr{display:grid;grid-template-columns:minmax(80px,40%) 1fr;gap:8px;align-items:end;font-size:.75rem;color:var(--ink-2)}
.mini .ms{display:flex;gap:1px;align-items:flex-end;height:22px;border-bottom:3px solid var(--wood);overflow:hidden;direction:ltr}
.mini .ms i{display:block;width:4px;background:var(--c);opacity:.85;border-radius:1px 1px 0 0}
.mini .ms i.k-set{width:9px;opacity:1}.mini .ms i.k-lecture{background:var(--ink-3)}
.room .more{font-size:.78rem;color:var(--ink-3)}
.recep{margin-top:14px;font-size:.85rem;color:var(--ink-2)}
/* level 2: hall */
.lay{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:16px;align-items:start}
.cases{display:grid;gap:16px;min-width:0}
.case{background:var(--wood);border-radius:14px;padding:10px 10px 14px;box-shadow:inset 0 0 0 3px var(--wood-2)}
.case>h3{margin:2px 6px 10px;color:#f6efe4;font-size:1.1rem;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}
.case>h3 small{font-weight:400;opacity:.8;font-size:.82rem}
.shelf{background:var(--wood-in);border-radius:6px;margin-top:10px;padding:8px 10px 0;box-shadow:inset 0 -10px 0 var(--plank)}
.shelf h4{margin:0 0 6px;font-size:.88rem;color:var(--ink);display:flex;justify-content:space-between;gap:8px}
.shelf h4 small{color:var(--ink-3);font-weight:400}
.row{display:flex;flex-wrap:wrap;gap:3px;align-items:flex-end;padding-bottom:10px;min-height:60px}
.sp{font:inherit;position:relative;border:0;cursor:pointer;padding:6px 0;border-radius:3px 3px 1px 1px;writing-mode:vertical-rl;text-orientation:mixed;font-size:.74rem;line-height:1.2;color:#fff;background:var(--c);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;width:30px;box-shadow:inset -3px 0 0 rgba(0,0,0,.18),inset 0 6px 0 rgba(255,255,255,.12)}
.sp:hover,.sp:focus-visible{transform:translateY(-6px);transition:transform .12s}
.sp.on{outline:3px solid var(--ink);outline-offset:1px;transform:translateY(-6px)}
.sp.t2{filter:saturate(.75) brightness(1.08)}.sp.t3{filter:saturate(.55) brightness(1.15)}
.sp.k-lecture{background:repeating-linear-gradient(0deg,var(--ink-2) 0 6px,var(--ink-3) 6px 8px);color:#fff;width:28px}
.sp.k-booklet{background:var(--surface);color:var(--ink);border:1px dashed var(--c);width:26px}
.sp.k-paper{background:var(--surface);color:var(--ink-2);border:1px solid var(--line-strong);width:20px;font-size:.66rem}
.sp .vb{position:absolute;inset-block-end:4px;inset-inline:0;writing-mode:horizontal-tb;font-size:.62rem;background:rgba(0,0,0,.35);border-radius:3px;margin:0 3px;text-align:center}
.set{display:flex;gap:1px;align-items:flex-end;cursor:pointer;border:0;background:none;padding:0}
.set .sp{width:16px;font-size:.62rem;pointer-events:none}
.set .sp:first-child{width:30px;font-size:.72rem}
.set:hover .sp,.set:focus-visible .sp{transform:translateY(-6px);transition:transform .12s}
.set.on .sp{transform:translateY(-6px)}
.set.on .sp:first-child{outline:3px solid var(--ink)}
.empty{font-size:.8rem;color:var(--ink-3);padding:14px 4px}
.side{position:sticky;top:12px;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px;display:grid;gap:10px;line-height:1.8;font-size:.92rem;max-height:calc(100vh - 24px);overflow:auto}
.side h3{margin:0;font-size:1.15rem;line-height:1.6}
.side .meta{color:var(--ink-2);font-size:.85rem}
.side .tag{display:inline-block;font-size:.75rem;padding:1px 9px;border-radius:99px;border:1px solid var(--line-strong);margin-inline-end:4px;color:var(--ink-2)}
.side .tier{border-color:var(--c);color:var(--c)}
.vols{display:grid;gap:6px;margin:0;padding:0;list-style:none}
.vols li{display:grid;grid-template-columns:auto 1fr;gap:8px;align-items:start;padding:6px 8px;border-radius:10px;background:var(--surface-subtle)}
.vols b.vn{display:inline-grid;place-items:center;min-width:2em;height:2em;border-radius:6px;background:var(--c);color:#fff;font-size:.8rem}
.vols .r{font-size:.75rem;color:var(--ok)}
.vols details summary{cursor:pointer}
.side .links{display:flex;flex-wrap:wrap;gap:6px}
.side .links a{font-size:.8rem;padding:2px 10px;border-radius:999px;border:1px solid var(--line-strong);color:var(--ink-2);text-decoration:none}
.side .links a:hover{border-color:var(--c);color:var(--c)}
.side .note{font-size:.8rem}
.hits{display:grid;gap:6px}
.hit{font:inherit;text-align:start;display:grid;gap:2px;padding:8px 12px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer;border-inline-start:4px solid var(--c)}
.hit small{color:var(--ink-3)}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.8rem;color:var(--ink-2);margin:0 0 12px}
.legend i{display:inline-block;width:14px;height:20px;vertical-align:middle;border-radius:2px;margin-inline-end:4px}
@media (max-width:1000px){.lay{grid-template-columns:minmax(0,1fr)}.side{position:static;max-height:none}}
</style>
</head>
<body>
<main class="wrap" id="main">
<div id="app"></div>
<div class="note foot" role="note" style="margin-top:26px">فایل‌ها در مخزن خصوصی ویراستارند و از این صفحه دانلود نمی‌شوند؛ این صفحه فهرست، دسته‌بندی و سنجش آن‌هاست. ردهٔ اعتبار فقط برای کتاب‌هایی آمده که خوانده و سنجیده شده‌اند. اگر کتابی در قفسهٔ نادرست است یا دو بار آمده، در صف بازبینی بگویید.</div>
</main>
<footer class="foot"><div class="wrap">دانش‌سرا · پیش‌نویس · کتابخانه</div></footer>
<script>
const D = __DATA__;
const fa = n => String(n).replace(/\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[d]);
const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const H = Object.fromEntries(D.halls.map(h => [h.id, h]));
const BY = {}; D.items.forEach(it => (BY[it.hall] = BY[it.hall] || []).push(it));
const IDX = Object.fromEntries(D.items.map(it => [it.id, it]));
const KIND = {book: "کتاب", set: "مجموعهٔ چندجلدی", lecture: "درس‌گفتار", booklet: "جزوه", paper: "مقاله"};
const TIER = {1: "ردهٔ ۱: پژوهشی", 2: "ردهٔ ۲: کتاب معتبر", 3: "ردهٔ ۳: کتاب یا سخنرانی", 4: "ردهٔ ۴: سرنخ یا جدلی"};
const PK = {rev: "مرورشده در ویکی", cite: "ارجاع‌شده در ویکی", rec: "پیشنهاد ویراستار"};
const DEC = {"add": "به ویکی افزوده شد", "add-as-viewpoint": "به‌عنوان یک دیدگاه آمد", "skip": "برای ویکی کنار گذاشته شد", "use": "استفاده شد"};
const hsh = s => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) | 0; return Math.abs(h); };
const nvols = it => it.vols && it.vols.length ? it.vols.length : 1;
let kindF = "all", sel = null;

function route(){
  const h = decodeURIComponent(location.hash.slice(1));
  if (h.startsWith("b-") && IDX[h.slice(2)]) { const it = IDX[h.slice(2)]; hall(it.hall, it.id); }
  else if (h.startsWith("hall-") && H[h.slice(5)]) hall(h.slice(5));
  else plan();
}
function go(h){ if (location.hash.slice(1) === h) route(); else location.hash = h; }
function stats(list){ const vols = list.reduce((a, it) => a + (it.kind === "set" ? it.vols.length : it.kind === "lecture" || it.kind === "booklet" ? it.vols.length : 1), 0);
  const c = k => list.filter(it => it.kind === k).length;
  const S = [[c("book") + c("paper"), "کتاب و مقاله"], [c("set"), "مجموعهٔ چندجلدی"], [c("lecture"), "درس‌گفتار"], [c("booklet"), "جزوه"], [vols, "جلد و جلسه"]].filter(x => x[0]);
  return `<div class="stats">${S.map(x => `<div><b>${fa(x[0])}</b>${x[1]}</div>`).join("")}</div>`; }

function plan(){
  sel = null; document.title = "کتابخانهٔ دانش‌سرا | اطلس‌ها | دانش‌سرا";
  const app = document.getElementById("app");
  app.innerHTML = `<div class="top"><div><h1>کتابخانهٔ دانش‌سرا</h1><p class="what">هر تالار یک حوزه است و هر قفسه یک موضوع. همهٔ کتاب‌ها، مجموعه‌های چندجلدی، جزوه‌ها و درس‌گفتارها یک بار و سر جای خودشان آمده‌اند؛ جلدهای یک اثر کنار هم در یک مجموعه‌اند. روی یک تالار بزنید تا وارد شوید.</p></div>${stats(D.items)}</div>
    <div class="bar"><input id="q" type="search" placeholder="جستجو در عنوان یا نویسنده در همهٔ تالارها…" aria-label="جستجو"></div><div id="hits" class="hits"></div>
    <div class="plan" id="plan">${D.halls.map(room).join("")}</div>
    <p class="recep">میز ورودی: ${fa(D.reception)} فایل که عنوان یا محتوایشان هنوز شناسایی نشده و تا بازبینی در تالارها گذاشته نشده‌اند. از ${fa(D.files)} فایل مخزن، نسخه‌های تکراری و جلدهای یک اثر یکی شده‌اند.</p>`;
  app.querySelector("#plan").addEventListener("click", e => { const b = e.target.closest("[data-h]"); if (b) go("hall-" + b.dataset.h); });
  search(app);
}
function room(h){
  const L = BY[h.id] || [];
  const rows = h.cases.flatMap(c => c.shelves.map(s => [s, L.filter(it => it.s === s.id)])).filter(r => r[1].length);
  return `<button type="button" class="room" data-h="${h.id}" style="--c:var(${h.color})"><h2>${h.fa}</h2><span class="n">${fa(L.length)} اثر در ${fa(rows.length)} قفسه</span>
    <div class="mini">${rows.slice(0, 6).map(([s, its]) => `<div class="mr"><span>${s.fa}</span><span class="ms">${its.slice(0, 40).map(it => `<i class="k-${it.kind}" style="height:${10 + hsh(it.id) % 12}px"></i>`).join("")}</span></div>`).join("")}</div>
    ${rows.length > 6 ? `<span class="more">و ${fa(rows.length - 6)} قفسهٔ دیگر</span>` : ""}</button>`;
}
function search(app){
  const q = app.querySelector("#q"), hits = app.querySelector("#hits");
  q.addEventListener("input", () => { const v = q.value.trim(); if (v.length < 2) { hits.innerHTML = ""; return; }
    const r = D.items.filter(it => (it.t + " " + (it.a || "") + " " + (it.vols || []).map(x => x.title).join(" ")).includes(v)).slice(0, 30);
    hits.innerHTML = r.length ? r.map(it => `<button type="button" class="hit" data-b="${it.id}" style="--c:var(${H[it.hall].color})"><span>${esc(it.t)}</span><small>${H[it.hall].fa} › ${shelfName(it)} · ${KIND[it.kind]}${it.kind !== "book" ? " · " + fa(nvols(it)) + (it.kind === "set" ? " جلد" : " بخش") : ""}</small></button>`).join("") : `<p class="empty">چیزی پیدا نشد.</p>`; });
  hits.addEventListener("click", e => { const b = e.target.closest("[data-b]"); if (b) go("b-" + b.dataset.b); });
}
const shelfName = it => { for (const c of H[it.hall].cases) for (const s of c.shelves) if (s.id === it.s) return s.fa; return ""; };

function hall(hid, pick){
  const h = H[hid], L = BY[hid] || [];
  document.title = h.fa + " | کتابخانهٔ دانش‌سرا";
  const app = document.getElementById("app");
  app.innerHTML = `<nav class="lcrumb" aria-label="مسیر کتابخانه"><button type="button" id="back">کتابخانه</button><span>›</span><b>${h.fa}</b></nav>
    <div class="top"><div><h1 style="color:var(${h.color})">${h.fa}</h1><p class="what">هر قفسه یک موضوع است. عطف‌های پهن‌تر و پشت‌سرهم، مجموعه‌های چندجلدی‌اند؛ روی هر عطف بزنید تا جزئیات، جلدها و مدخل‌های مرتبط را ببینید.</p></div>${stats(L)}</div>
    <div class="bar" role="group" aria-label="نوع">${[["all", "همه"], ["book", "کتاب"], ["set", "چندجلدی"], ["lecture", "درس‌گفتار"], ["booklet", "جزوه"], ["paper", "مقاله"]].filter(([k]) => k === "all" || L.some(it => it.kind === k)).map(([k, t]) => `<button type="button" class="chip" data-k="${k}" aria-pressed="${kindF === k}">${t}</button>`).join("")}
    <input id="q" type="search" placeholder="جستجو در این تالار…" aria-label="جستجو در تالار"></div>
    <div class="legend"><span><i style="background:var(${h.color})"></i>کتاب (کم‌رنگ‌تر = ردهٔ اعتبار پایین‌تر)</span><span><i style="background:var(${h.color});width:26px"></i>مجموعهٔ چندجلدی</span><span><i style="background:repeating-linear-gradient(0deg,var(--ink-2) 0 6px,var(--ink-3) 6px 8px)"></i>درس‌گفتار</span><span><i style="border:1px dashed var(${h.color})"></i>جزوه</span></div>
    <div class="lay" style="--c:var(${h.color})"><div class="cases" id="cases"></div><aside class="side" id="side" aria-live="polite"></aside></div>`;
  app.querySelector("#back").addEventListener("click", () => go(""));
  app.querySelectorAll("[data-k]").forEach(b => b.addEventListener("click", () => { kindF = b.dataset.k; app.querySelectorAll("[data-k]").forEach(x => x.setAttribute("aria-pressed", x === b)); cases(h); }));
  app.querySelector("#q").addEventListener("input", () => cases(h));
  app.querySelector("#cases").addEventListener("click", e => { const b = e.target.closest("[data-b]"); if (b) { sel = b.dataset.b; try { history.replaceState(null, "", "#b-" + sel); } catch (_) {} mark(); panel(IDX[sel]); } });
  sel = pick || null; cases(h); panel(sel ? IDX[sel] : null);
  if (pick) setTimeout(() => { const el = document.querySelector(`[data-b="${pick}"]`); if (el) el.scrollIntoView({block: "center"}); }, 30);
}
function spine(it){
  const tcls = it.tier >= 3 ? " t3" : it.tier === 2 ? " t2" : "";
  const ht = it.kind === "booklet" ? 120 : it.kind === "paper" ? 110 : it.kind === "lecture" ? 130 : 150 + hsh(it.id) % 50;
  const tip = esc(it.t + (it.a ? " — " + it.a : ""));
  if (it.kind === "set") {
    const n = it.vols.length;
    return `<button type="button" class="set${sel === it.id ? " on" : ""}" data-b="${it.id}" title="${tip}" aria-label="${tip}، ${fa(n)} جلد">${it.vols.slice(0, Math.min(n, 8)).map((v, i) => `<span class="sp${tcls}" style="height:${ht}px">${i ? fa(v.v || i + 1) : esc(it.t)}</span>`).join("")}${n > 8 ? `<span class="sp" style="height:${ht}px;width:18px">+${fa(n - 8)}</span>` : ""}</button>`;
  }
  return `<button type="button" class="sp k-${it.kind}${tcls}${sel === it.id ? " on" : ""}" data-b="${it.id}" style="height:${ht}px" title="${tip}" aria-label="${tip}">${esc(it.t)}${it.kind === "lecture" || it.kind === "booklet" ? `<span class="vb">${fa(it.vols.length)}</span>` : ""}</button>`;
}
function cases(h){
  const q = (document.querySelector("#q") || {}).value || "";
  const L = (BY[h.id] || []).filter(it => (kindF === "all" || it.kind === kindF) && (!q || (it.t + " " + (it.a || "")).includes(q)));
  document.getElementById("cases").innerHTML = h.cases.map(c => {
    const sh = c.shelves.map(s => [s, L.filter(it => it.s === s.id)]);
    const n = sh.reduce((a, x) => a + x[1].length, 0);
    if (!n && (kindF !== "all" || q || c.id === "read")) return "";
    return `<section class="case"><h3>${c.fa}<small>${fa(n)} اثر</small></h3>${sh.map(([s, its]) => `<div class="shelf"><h4>${s.fa}<small>${its.length ? fa(its.length) : "خالی"}</small></h4><div class="row">${its.length ? its.sort((a, b) => (a.kind === "set") - (b.kind === "set") || a.t.localeCompare(b.t, "fa")).map(spine).join("") : `<span class="empty">هنوز چیزی در این قفسه نیست؛ جای خالی‌ای که باید پر شود.</span>`}</div></div>`).join("")}</section>`;
  }).join("") || `<p class="empty">با این فیلتر چیزی نیست.</p>`;
}
function mark(){ document.querySelectorAll("#cases [data-b]").forEach(b => b.classList.toggle("on", b.dataset.b === sel)); }
function panel(it){
  const s = document.getElementById("side"); if (!s) return;
  if (!it) { s.innerHTML = `<h3>یک عطف را انتخاب کنید</h3><p class="meta" style="margin:0">روی هر کتاب، مجموعه، جزوه یا درس‌گفتار بزنید. برای مجموعه‌ها فهرست جلدها، برای درس‌گفتارها فهرست جلسه‌ها و خلاصهٔ هر جلسه، و برای کتاب‌هایی که خوانده شده‌اند ردهٔ اعتبار و مدخل‌هایی که از آن‌ها ساخته شد می‌آید.</p>`; return; }
  const a = it.as || {};
  const vols = it.vols && it.vols.length ? `<div><b>${it.kind === "set" ? `${fa(it.vols.length)} جلد در مخزن` : it.kind === "booklet" ? `${fa(it.vols.length)} جلسه` : `${fa(it.vols.length)} جلسه یا قسمت`}</b><ol class="vols">${it.vols.map(v => `<li><b class="vn">${fa(v.v || "؟")}</b><span>${v.u ? `<a href="${v.u}">${esc(v.title)}</a>` : v.sum ? `<details><summary>${esc(v.title)}</summary>${esc(v.sum)}…</details>` : esc(v.title)}${v.read ? ` <span class="r">· خوانده و سنجیده شده</span>` : ""}${v.mb ? ` <span class="meta">· ${fa(v.mb)} مگابایت</span>` : ""}</span></li>`).join("")}</ol></div>` : "";
  s.innerHTML = `<h3>${esc(it.t)}</h3>
    <div class="meta">${it.a ? esc(it.a) : "نویسنده ثبت نشده"}${it.y || a.y ? " · " + fa(it.y || a.y) : ""}</div>
    <div><span class="tag">${KIND[it.kind]}</span><span class="tag">${H[it.hall].fa} › ${shelfName(it)}</span>${it.tier ? `<span class="tag tier">${TIER[it.tier] || ""}</span>` : ""}${it.pk ? `<span class="tag">${PK[it.pk]}</span>` : ""}${it.copies ? `<span class="tag">${fa(it.copies)} نسخه در مخزن (یکی شد)</span>` : ""}${it.inrepo ? `<span class="tag">فایلش در مخزن هست</span>` : ""}</div>
    ${it.d ? `<p style="margin:0">${esc(it.d)}</p>` : ""}
    ${a.lab ? `<p style="margin:0"><b>سنجش:</b> ${esc(a.lab)}</p>` : ""}
    ${a.best ? `<p style="margin:0"><b>بهترین کاربرد:</b> ${esc(a.best)}</p>` : ""}
    ${a.cau && a.cau.length ? `<div><b>احتیاط‌ها</b><ul style="margin:0;padding-inline-start:18px">${a.cau.map(c => `<li>${esc(c)}</li>`).join("")}</ul></div>` : ""}
    ${a.dec ? `<p class="meta" style="margin:0">${DEC[a.dec] || ""}</p>` : ""}
    ${it.ch ? `<p class="meta" style="margin:0">${esc(it.ch)}</p>` : ""}
    ${vols}
    ${it.en && it.en.length ? `<div><b>مدخل‌های ویکی که از این اثر آمده‌اند</b><div class="links">${it.en.map(e => `<a href="${e[1]}">${esc(e[0])}</a>`).join("")}</div></div>` : ""}
    ${it.pg ? `<div class="links"><a href="${it.pg}">صفحهٔ موضوعی ویکی روان</a></div>` : ""}
    ${!it.tier && !it.pk && it.kind !== "lecture" && it.kind !== "booklet" ? `<p class="note meta" style="margin:0">این اثر هنوز خوانده و سنجیده نشده است.</p>` : ""}`;
  if (innerWidth < 1000) s.scrollIntoView({behavior: "smooth", block: "nearest"});
}
addEventListener("hashchange", route); route();
</script>
</body>
</html>
'''
open(f'{R}/atlas/library-plan.html', 'w', encoding='utf-8').write(TPL.replace('__DATA__', DATA))
print(f'atlas/library-plan.html: {len(items)} items, {len(DATA) // 1024} KB')
