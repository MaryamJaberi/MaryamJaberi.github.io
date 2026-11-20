/* دانش‌سرا — لایهٔ تجربهٔ کاربری: «کجا هستم»، جست‌وجوی سراسری، مرتب‌کردن فهرست‌های بلند، لایه‌بندی مدخل‌ها.
   بارگذاری از nav.js. هیچ درخواستی به بیرون از سایت نمی‌فرستد. */
(() => {
"use strict";
if (window.__DS_PLUS) return; window.__DS_PLUS = 1;
const SELF = document.currentScript;
const ROOT = (SELF && SELF.src || "").replace(/core\/plus\.js.*$/, "");
if (!ROOT) return;
const PATH = (() => { try { return decodeURIComponent(location.pathname.slice(new URL(ROOT).pathname.length)) || "index.html"; } catch (e) { return ""; } })();
const fa = n => Number(n).toLocaleString("fa-IR");
const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const norm = s => String(s || "").toLowerCase().replace(/[يى]/g, "ی").replace(/ك/g, "ک").replace(/[ۀة]/g, "ه").replace(/[أإآ]/g, "ا").replace(/ؤ/g, "و")
  .replace(/[ً-ٰٟٔ]/g, "").replace(/[‌‍­]/g, " ").replace(/\s+/g, " ").trim();

/* ---------- لایه‌ها ---------- */
const LAYERS = [
  [/^(psy|soc|phil|tabar|tarikh)\//, "۱", "علم", "#2A6F7A"],
  [/^miyan\//, "۱→۲", "پل علم و ایران", "#9F1239"],
  [/^atlas\//, "۱", "اطلس‌ها", "#1C39BB"],
  [/^iran\//, "۲", "ایران", "#B45309"],
  [/^simorgh\//, "۳", "سیمرغ", "#5B4B8A"],
  [/^sakht\//, "۴", "ساخت ایران", "#2F6B4F"],
  [/^wellbeing\//, "محصول", "سنجش سلامت سازمان", "#0A6B60"],
  [/^(core\/|vault)/, "راهنما", "هسته و ابزارها", "#5C574F"]
];
const layer = LAYERS.find(l => l[0].test(PATH));

const css = document.createElement("style");
css.textContent = `
.ds-layer{display:inline-flex;align-items:center;gap:5px;font-size:.72rem;font-weight:700;border-radius:999px;padding:0 9px;color:#fff;white-space:nowrap}
.ds-here{font-size:.78rem;color:var(--ink-2,#5c574c);border:1px dashed var(--line-strong,#cfc9bc);border-radius:999px;padding:0 10px;cursor:pointer;background:none;font:inherit;max-width:48vw;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ds-here[hidden]{display:none}
.ds-sb{font:inherit;font-size:.8rem;padding:2px 12px;border-radius:999px;border:1px solid var(--line-strong,#cfc9bc);background:var(--surface,#fff);color:var(--ink,#222);cursor:pointer;white-space:nowrap}
.ds-sb kbd{font:600 .65rem ui-monospace,monospace;border:1px solid var(--line-strong,#cfc9bc);border-radius:4px;padding:0 4px;margin-inline-start:4px;opacity:.7}
.ds-prog{position:fixed;top:0;inset-inline:0;height:3px;z-index:90;pointer-events:none}
.ds-prog i{display:block;height:100%;width:0;background:var(--primary,#0a6b60);transition:width .1s}
.ds-crumbs{position:sticky;top:0;z-index:50}
#ds-toc{position:fixed;z-index:75;inset-block-start:48px;inset-inline-end:12px;width:min(320px,calc(100vw - 24px));max-height:70vh;overflow:auto;background:var(--surface,#fff);border:1px solid var(--line-strong,#cfc9bc);border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.2);padding:8px;direction:rtl;font-size:.86rem;line-height:1.7}
#ds-toc[hidden]{display:none}
#ds-toc a{display:block;padding:3px 10px;border-radius:8px;color:var(--ink,#222);text-decoration:none}
#ds-toc a.h3{padding-inline-start:24px;font-size:.8rem;color:var(--ink-2,#5c574c)}
#ds-toc a:hover{background:var(--surface-subtle,#f1ede6)}
#ds-toc a.on{background:var(--primary,#0a6b60);color:#fff}
#ds-search{position:fixed;inset:0;z-index:95;background:color-mix(in srgb,var(--ink,#000) 40%,transparent);display:grid;justify-items:center;align-items:start;padding:8vh 10px 10px}
#ds-search[hidden]{display:none}
#ds-search .in{width:min(100%,720px);background:var(--paper,#faf8f3);border:1px solid var(--line-strong,#cfc9bc);border-radius:16px;box-shadow:0 14px 44px rgba(0,0,0,.3);direction:rtl;overflow:hidden}
#ds-search input{width:100%;box-sizing:border-box;font:inherit;font-size:1.05rem;padding:14px 18px;border:0;border-bottom:1px solid var(--line,#e5e1d8);background:var(--surface,#fff);color:var(--ink,#222);outline:none}
#ds-search .chips{display:flex;flex-wrap:wrap;gap:6px;padding:8px 14px;border-bottom:1px solid var(--line,#e5e1d8)}
#ds-search .chips button{font:inherit;font-size:.78rem;border:1px solid var(--line-strong,#cfc9bc);background:var(--surface,#fff);color:var(--ink,#222);border-radius:999px;padding:0 10px;cursor:pointer}
#ds-search .chips button[aria-pressed=true]{background:var(--primary,#0a6b60);border-color:var(--primary,#0a6b60);color:#fff}
#ds-search ol{list-style:none;margin:0;padding:6px;max-height:58vh;overflow:auto}
#ds-search li a{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;padding:7px 10px;border-radius:10px;color:var(--ink,#222);text-decoration:none;font-size:.92rem;line-height:1.6}
#ds-search li a .w{grid-row:span 2;align-self:center;font-size:.7rem;font-weight:700;color:#fff;border-radius:6px;padding:1px 7px;min-width:3.2em;text-align:center}
#ds-search li a small{color:var(--ink-3,#8a8578);font-size:.76rem}
#ds-search li a.sel,#ds-search li a:hover{background:var(--surface-subtle,#f1ede6)}
#ds-search .ft{font-size:.75rem;color:var(--ink-3,#8a8578);padding:6px 14px;border-top:1px solid var(--line,#e5e1d8)}
.ds-tidy{position:relative}
.ds-tidy.fold{max-height:300px;overflow:hidden}
.ds-tidy.fold::after{content:"";position:absolute;inset-inline:0;bottom:0;height:70px;background:linear-gradient(transparent,var(--paper,var(--bg,#faf8f3)));pointer-events:none}
.ds-tbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:6px 0 8px;font-size:.82rem;color:var(--ink-3,#8a8578)}
.ds-tbar input{font:inherit;font-size:.85rem;padding:4px 12px;border-radius:999px;border:1px solid var(--line-strong,#cfc9bc);background:var(--surface,#fff);color:var(--ink,#222);min-width:min(260px,70vw)}
.ds-tbar button{font:inherit;font-size:.8rem;padding:2px 12px;border-radius:999px;border:1px solid var(--line-strong,#cfc9bc);background:var(--surface,#fff);color:var(--primary,#0a6b60);cursor:pointer}
.ds-tbar .let{display:flex;flex-wrap:wrap;gap:2px}
.ds-tbar .let a{font-size:.75rem;padding:0 6px;border-radius:5px;text-decoration:none;color:var(--ink-2,#5c574c);border:1px solid var(--line,#e5e1d8)}
.ds-hide{display:none!important}
.ds-glance{display:grid;gap:8px;background:var(--surface-subtle,#f1ede6);border-radius:12px;padding:12px 14px;margin:12px 0;font-size:.86rem}
.ds-glance .row{display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center}
.ds-glance .row b{font-size:1.1rem}
.ds-gbar{display:flex;height:12px;border-radius:6px;overflow:hidden;background:var(--line,#e5e1d8)}
.ds-gbar i{display:block;height:100%}
.ds-gleg{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:.76rem;color:var(--ink-2,#5c574c)}
.ds-gleg span::before{content:"";display:inline-block;width:9px;height:9px;border-radius:2px;margin-inline-end:4px;background:var(--c)}
.ds-gtools{display:flex;flex-wrap:wrap;gap:6px}
.ds-gtools button,.ds-gtools a{font:inherit;font-size:.8rem;padding:2px 12px;border-radius:999px;border:1px solid var(--line-strong,#cfc9bc);background:var(--surface,#fff);color:var(--ink,#222);cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:6px}
.ds-gtools a.story{border-color:#B4532A;color:#B4532A;font-weight:700}
.ds-gtools button[aria-pressed=true]{background:var(--primary,#0a6b60);border-color:var(--primary,#0a6b60);color:#fff}
.ds-pl{display:none;font-weight:700}
.ds-compact ol.pts>li{cursor:pointer}
.ds-compact ol.pts>li .ds-pl{display:inline}
.ds-compact ol.pts>li .ds-pb,.ds-compact ol.pts>li>.ref{display:none}
.ds-compact ol.pts>li.open .ds-pl{display:none}
.ds-compact ol.pts>li.open .ds-pb{display:inline}.ds-compact ol.pts>li.open>.ref{display:flex}
.ds-compact ol.pts>li .ds-pl::after{content:" ＋";color:var(--ink-3,#8a8578);font-weight:400}
.ds-dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-inline-end:6px;vertical-align:1px}
@media print{.ds-prog,#ds-toc,#ds-search,.ds-sb,.ds-here{display:none!important}}
`;
document.head.appendChild(css);

const TIERC = {t1:"#2F6B4F", t2:"#0A6B60", t3:"#B45309", t4:"#9F1239", t0:"#8A847A"};
const TIERN = {t1:"فراتحلیل یا تکرار", t2:"مقاله یا آمار رسمی", t3:"کتاب یا سخنرانی", t4:"سرنخ", t0:"بی‌منبع"};
const WIKIC = {psy:"#0A6B60", soc:"#2A6F7A", phil:"#5B4B8A", tabar:"#C45C26", tarikh:"#8A6D2E", core:"#5C574F", atlas:"#1C39BB", page:"#8A847A"};
const WIKIN = {psy:"روان", soc:"جامعه", phil:"فلسفه", tabar:"تبار", tarikh:"تاریخ", core:"چهره", atlas:"اطلس", page:"صفحه"};

/* ---------- داستان‌ها و صفحه‌های تازه ---------- */
const STORIES = {"soc:preference-falsification": "soc/stories/preference-falsification.html"};

function boot() {
  const bar = document.querySelector(".ds-crumbs");
  /* نوار پیشرفت خواندن */
  const prog = document.createElement("div"); prog.className = "ds-prog"; prog.innerHTML = "<i></i>"; document.body.appendChild(prog);
  const pi = prog.firstChild;
  /* برچسب لایه */
  if (bar && layer && !bar.querySelector(".ds-layer")) {
    const c = document.createElement("span"); c.className = "ds-layer"; c.style.background = layer[3];
    c.textContent = (/^\d|۱|۲|۳|۴/.test(layer[1]) ? "لایهٔ " + layer[1] + ": " : layer[1] + ": ") + layer[2];
    c.title = "لایه‌ای که این صفحه در آن است"; bar.insertBefore(c, bar.firstChild);
  }
  /* «اینجا»: بخش فعلی صفحه */
  const here = document.createElement("button"); here.type = "button"; here.className = "ds-here"; here.hidden = true; here.title = "فهرست بخش‌های این صفحه";
  const sb = document.createElement("button"); sb.type = "button"; sb.className = "ds-sb"; sb.innerHTML = "⌕ جست‌وجو<kbd>/</kbd>";
  if (bar) { const mb = bar.querySelector(".ds-mapb"); bar.insertBefore(here, mb || null); bar.insertBefore(sb, mb || null); }
  else { sb.style.cssText = "position:fixed;inset-block-end:14px;inset-inline-start:110px;z-index:60;padding:7px 16px;box-shadow:0 4px 14px rgba(0,0,0,.18)"; document.body.appendChild(sb); }
  sb.addEventListener("click", openSearch);

  /* فهرست این صفحه */
  let toc = null, heads = [];
  const collect = () => { heads = [...document.querySelectorAll("main h2, main h3, article h2, article h3, section > h2, body > h2")].filter(h => h.offsetParent && h.textContent.trim() && !h.closest("#ds-map,#ds-toc,#ds-search,.ds-pv,nav,header")); };
  const buildToc = () => {
    collect(); if (!toc) { toc = document.createElement("nav"); toc.id = "ds-toc"; toc.hidden = true; toc.setAttribute("aria-label", "بخش‌های این صفحه"); document.body.appendChild(toc); }
    heads.forEach((h, i) => { if (!h.id) h.id = "ds-h-" + i; });
    toc.innerHTML = `<div style="font-size:.75rem;color:var(--ink-3,#8a8578);padding:2px 10px 6px">بخش‌های این صفحه</div>` + heads.map(h => `<a class="${h.tagName.toLowerCase()}" href="#${esc(h.id)}">${esc(h.textContent.trim().slice(0, 70))}</a>`).join("");
    toc.onclick = e => { if (e.target.closest("a")) toc.hidden = true; };
  };
  here.addEventListener("click", () => { buildToc(); toc.hidden = !toc.hidden; mark(); });
  document.addEventListener("click", e => { if (toc && !toc.hidden && !e.target.closest("#ds-toc,.ds-here")) toc.hidden = true; });
  let cur = null;
  const mark = () => { if (toc) toc.querySelectorAll("a").forEach(a => a.classList.toggle("on", cur && a.getAttribute("href") === "#" + cur.id)); };
  const onScroll = () => {
    const h = document.documentElement, max = h.scrollHeight - innerHeight;
    pi.style.width = (max > 0 ? Math.min(100, scrollY / max * 100) : 0) + "%";
    if (!heads.length) collect();
    const y = (bar ? bar.offsetHeight : 0) + 20;
    let c = null; for (const x of heads) { if (x.getBoundingClientRect().top < y + 60) c = x; else break; }
    if (c !== cur) { cur = c; if (c) { here.textContent = "§ " + c.textContent.trim().slice(0, 40); here.hidden = false; } else here.hidden = heads.length < 3; if (heads.length >= 3 && !c) here.textContent = "§ بخش‌های صفحه"; mark(); }
  };
  addEventListener("scroll", onScroll, {passive: true}); setTimeout(() => { collect(); onScroll(); }, 600);
  new MutationObserver(() => { heads = []; }).observe(document.body, {childList: true, subtree: false});

  tidyAll(); enhanceEntry();
  new MutationObserver(() => { clearTimeout(boot.t); boot.t = setTimeout(() => { tidyAll(); enhanceEntry(); heads = []; onScroll(); }, 150); }).observe(document.body, {childList: true, subtree: true});
  addEventListener("keydown", e => {
    if ((e.key === "/" && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) && !document.activeElement.isContentEditable) || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k")) { e.preventDefault(); openSearch(); }
  });
}

/* ---------- مرتب‌کردن فهرست‌های بلند ---------- */
function tidyAll() {
  document.querySelectorAll(".lst, .idx, .chips, .tags, ul, ol, div").forEach(el => {
    if (el.dataset.dsTidy || el.closest("[data-notidy],#ds-map,#ds-toc,#ds-search,nav,header,footer,.ds-pv,svg,.row,.rack,#rack") || el.matches("ol.pts")) return;
    const kids = [...el.children]; if (kids.length < 30) return;
    const linky = kids.filter(k => k.tagName === "A" || (k.tagName === "LI" && k.querySelector("a")) || k.classList.contains("ig")).length;
    if (linky < kids.length * 0.8) return;
    if (el.offsetHeight < 420) return;
    el.dataset.dsTidy = 1;
    const tb = document.createElement("div"); tb.className = "ds-tbar";
    const n = el.classList.contains("idx") ? el.querySelectorAll("a").length : kids.length;
    tb.innerHTML = `<input type="search" placeholder="جست‌وجو در این فهرست (${fa(n)} مورد)…" aria-label="جست‌وجو در این فهرست"><button type="button" data-t>نمایش همه</button><span class="cnt"></span>`;
    if (el.classList.contains("idx")) {
      const lets = [...el.querySelectorAll(".ig > b")];
      lets.forEach((b, i) => { if (!b.id) b.id = "ds-l-" + Math.random().toString(36).slice(2, 7); });
      const L = document.createElement("div"); L.className = "let"; L.innerHTML = lets.map(b => `<a href="#${b.id}">${esc(b.textContent)}</a>`).join(""); tb.appendChild(L);
    }
    el.parentNode.insertBefore(tb, el);
    el.classList.add("ds-tidy", "fold");
    const btn = tb.querySelector("[data-t]"), inp = tb.querySelector("input"), cnt = tb.querySelector(".cnt");
    btn.onclick = () => { const f = el.classList.toggle("fold"); btn.textContent = f ? "نمایش همه" : "جمع کن"; if (f) tb.scrollIntoView({block: "nearest"}); };
    inp.oninput = () => {
      const q = norm(inp.value); el.classList.toggle("fold", !q && btn.textContent === "نمایش همه");
      let shown = 0;
      const items = el.classList.contains("idx") ? [...el.querySelectorAll("a")] : kids;
      items.forEach(k => { const ok = !q || norm(k.textContent).includes(q); k.classList.toggle("ds-hide", !ok); if (ok) shown++; });
      if (el.classList.contains("idx")) el.querySelectorAll(".ig").forEach(g => g.classList.toggle("ds-hide", !!q && !g.querySelector("a:not(.ds-hide)")));
      cnt.textContent = q ? fa(shown) + " مورد" : "";
    };
  });
}

/* ---------- لایه‌بندی مدخل ---------- */
function enhanceEntry() {
  const art = document.querySelector("article.detail"); if (!art || art.dataset.dsPlus) return;
  const ol = art.querySelector("ol.pts"); if (!ol) return;
  art.dataset.dsPlus = 1;
  const lis = [...ol.children];
  const cnt = {t1: 0, t2: 0, t3: 0, t4: 0, t0: 0}; let contested = 0;
  lis.forEach(li => {
    const ev = li.querySelector(".ev"); const t = ev ? (ev.className.match(/t(\d)/) || [0, 0])[1] : 0; cnt["t" + t] = (cnt["t" + t] || 0) + 1;
    if (li.querySelector(".flag.contested")) contested++;
    const tn = li.firstChild; if (!tn || tn.nodeType !== 3) return;
    const txt = tn.textContent.trim(); const k = txt.indexOf(":");
    let lead;
    if (k > 2 && k < 90) { lead = txt.slice(0, k); if (/[\(（][\d۰-۹]{3,4}/.test(lead) && lead.length < 30) lead += ": " + txt.slice(k + 1).trim().split(/\s+/).slice(0, 8).join(" ") + "…"; }
    else lead = txt.split(/\s+/).slice(0, 9).join(" ") + "…";
    const pl = document.createElement("span"); pl.className = "ds-pl"; pl.innerHTML = `<i class="ds-dot" style="background:${TIERC["t" + t]}"></i>` + esc(lead);
    const pb = document.createElement("span"); pb.className = "ds-pb"; pb.textContent = txt;
    tn.replaceWith(pl, pb);
  });
  const total = lis.length;
  const g = document.createElement("div"); g.className = "ds-glance";
  const segs = ["t1", "t2", "t3", "t4", "t0"].filter(t => cnt[t]);
  const id = (PATH.split("/")[0] || "") + ":" + decodeURIComponent(location.hash.slice(1));
  const story = STORIES[id];
  const links = art.querySelectorAll("a[href]").length;
  g.innerHTML = `<div class="row"><span><b>${fa(total)}</b> گزاره</span>${contested ? `<span>⚑ <b>${fa(contested)}</b> محل بحث</span>` : ""}<span><b>${fa(links)}</b> پیوند به مدخل‌ها و منابع</span></div>
    <div class="ds-gbar" role="img" aria-label="ترکیب اعتبار گزاره‌ها">${segs.map(t => `<i style="width:${cnt[t] / total * 100}%;background:${TIERC[t]}" title="${TIERN[t]}: ${fa(cnt[t])}"></i>`).join("")}</div>
    <div class="ds-gleg">${segs.map(t => `<span style="--c:${TIERC[t]}">${TIERN[t]} ${fa(cnt[t])}</span>`).join("")}</div>
    <div class="ds-gtools"><button type="button" data-mode aria-pressed="${total > 5}">فقط سرتیترها</button>${story ? `<a class="story" href="${ROOT + story}"><svg width="18" height="18" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 16 C24 11 14 11 6 13 V51 C14 49 24 49 32 54 Z" fill="#F7E6DD" stroke="#B4532A" stroke-width="3"/><path d="M32 16 C40 11 50 11 58 13 V51 C50 49 40 49 32 54 Z" fill="#E3EFF1" stroke="#2A6F7A" stroke-width="3"/><rect x="11" y="36" width="4" height="8" fill="#2A6F7A"/><rect x="18" y="30" width="4" height="14" fill="#2A6F7A"/><rect x="25" y="22" width="4" height="22" fill="#B4532A"/></svg>داستان‌های واقعی این مدخل</a>` : ""}</div>`;
  const lead = art.querySelector(".lead"); (lead || ol).parentNode.insertBefore(g, lead ? lead.nextSibling : ol);
  const mb = g.querySelector("[data-mode]");
  const setMode = on => { art.classList.toggle("ds-compact", on); mb.setAttribute("aria-pressed", String(on)); mb.textContent = on ? "متن کامل همه" : "فقط سرتیترها"; };
  setMode(total > 5);
  mb.onclick = () => setMode(!art.classList.contains("ds-compact"));
  ol.addEventListener("click", e => { if (!art.classList.contains("ds-compact") || e.target.closest("a")) return; const li = e.target.closest("ol.pts > li"); if (li) li.classList.toggle("open"); });
}

/* ---------- جست‌وجوی سراسری ---------- */
let IDX = null, box = null, filt = "all";
async function loadIdx() {
  if (IDX) return IDX;
  const [r, p] = await Promise.all([fetch(ROOT + "core/registry.json").then(x => x.json()).catch(() => ({entries: {}})), fetch(ROOT + "core/preview.json").then(x => x.json()).catch(() => ({p: {}}))]);
  IDX = [];
  for (const [id, e] of Object.entries(r.entries || {})) {
    const t = e.title || {}; const w = e.wiki || id.split(":")[0];
    IDX.push({t: t.fa || t.en || id, s: [t.en, t.nl].filter(Boolean).join(" · "), u: e.url, w, k: e.type === "person" ? "person" : "entry", n: norm((t.fa || "") + " " + (t.en || "") + " " + (t.nl || ""))});
  }
  for (const [u, v] of Object.entries(p.p || {})) IDX.push({t: v[0], s: v[1] ? v[1].slice(0, 90) : "", u, w: "page", k: "page", n: norm(v[0] + " " + (v[1] || ""))});
  for (const [id, u] of Object.entries(STORIES)) IDX.push({t: "داستان‌ها: " + id.split(":")[1].replace(/-/g, " "), s: "داستان‌های واقعی و تصویرسازی داده", u, w: "page", k: "page", n: norm("داستان داستان‌ها " + id)});
  IDX.push({t: "کتابخانهٔ دانش‌سرا", s: "همهٔ کتاب‌ها و منابع در یک قفسه، با فیلتر و بینش", u: "core/library.html", w: "page", k: "page", n: norm("کتابخانه کتاب منبع library")});
  IDX.push({t: "نقشهٔ لایه‌ها", s: "همهٔ بخش‌های دانش‌سرا روی یک نقشه", u: "core/map.html", w: "page", k: "page", n: norm("نقشه لایه sitemap map")});
  IDX.push({t: "بینش‌ها", s: "دانش‌سرا در عدد: پوشش، اعتبار، شکاف‌ها", u: "core/insights.html", w: "page", k: "page", n: norm("بینش آمار insight داشبورد")});
  return IDX;
}
function openSearch() {
  if (!box) {
    box = document.createElement("div"); box.id = "ds-search"; box.hidden = true; box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "جست‌وجو در دانش‌سرا");
    box.innerHTML = `<div class="in"><input type="search" placeholder="جست‌وجو در همهٔ مدخل‌ها، چهره‌ها و صفحه‌ها… (فارسی یا انگلیسی)" aria-label="جست‌وجو"><div class="chips">${[["all", "همه"], ["entry", "مدخل‌ها"], ["person", "چهره‌ها"], ["page", "صفحه‌ها و ابزارها"]].map(([k, v]) => `<button type="button" data-f="${k}" aria-pressed="${k === "all"}">${v}</button>`).join("")}</div><ol></ol><div class="ft">↑↓ برای جابه‌جایی · Enter برای باز کردن · Esc برای بستن</div></div>`;
    document.body.appendChild(box);
    const inp = box.querySelector("input"), ol = box.querySelector("ol");
    let sel = 0, res = [];
    const draw = async () => {
      await loadIdx(); const q = norm(inp.value);
      res = !q ? [] : IDX.filter(x => (filt === "all" || x.k === filt) && x.n.includes(q)).sort((a, b) => (norm(a.t).startsWith(q) ? 0 : 1) - (norm(b.t).startsWith(q) ? 0 : 1) || a.t.length - b.t.length).slice(0, 40);
      sel = 0;
      ol.innerHTML = !q ? `<li style="padding:14px;color:var(--ink-3,#8a8578);font-size:.88rem">چیزی بنویسید: نام یک مفهوم، اندیشمند، کتاب یا ابزار. ${fa(IDX.length)} مورد در نمایه است.</li>` : res.length ? res.map((x, i) => `<li><a href="${ROOT + x.u}" class="${i === 0 ? "sel" : ""}"><span class="w" style="background:${WIKIC[x.w] || "#8A847A"}">${WIKIN[x.w] || x.w}</span><span>${esc(x.t)}</span><small>${esc(x.s)}</small></a></li>`).join("") : `<li style="padding:14px;color:var(--ink-3,#8a8578)">چیزی پیدا نشد.</li>`;
    };
    inp.addEventListener("input", draw);
    box.querySelector(".chips").onclick = e => { const b = e.target.closest("button"); if (!b) return; filt = b.dataset.f; box.querySelectorAll(".chips button").forEach(x => x.setAttribute("aria-pressed", x === b)); draw(); inp.focus(); };
    inp.addEventListener("keydown", e => {
      const as = [...ol.querySelectorAll("a")];
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); if (!as.length) return; sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + as.length) % as.length; as.forEach((a, i) => a.classList.toggle("sel", i === sel)); as[sel].scrollIntoView({block: "nearest"}); }
      if (e.key === "Enter" && as[sel]) { location.href = as[sel].href; box.hidden = true; }
      if (e.key === "Escape") box.hidden = true;
    });
    box.addEventListener("click", e => { if (e.target === box) box.hidden = true; if (e.target.closest("a")) box.hidden = true; });
    draw();
  }
  box.hidden = false; const i = box.querySelector("input"); i.focus(); i.select();
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
