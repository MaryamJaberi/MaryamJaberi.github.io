/* ==========================================================================
   گنجور نو — معماری یکپارچهٔ تک‌لندینگ + دو زیرصفحه (v50)
   کل ابزارهای پژوهشی (هم‌عصران و نقشه، پل‌های تضمین، مردمان شعر، آرایه‌ها،
   واژه‌سنج، جای‌ها در شعر، وزن‌ها و عروض) + تالار شاعران + کتابخانهٔ شخصی
   همه روی صفحهٔ اول؛ و فقط ۲ زیرصفحه: ۱) شاعر/دیوان  ۲) خوانش شعر
   ========================================================================== */

const API = "https://api.ganjoor.net/api/ganjoor";
const ROOT_API = "https://api.ganjoor.net/api";
const DATA_SOURCES = [
  "https://raw.githubusercontent.com/ganjoor/ganjoor-data/main/",
  "https://cdn.jsdelivr.net/gh/ganjoor/ganjoor-data@main/",
];
const STALE = new Error("stale");
const REALM = { minLon: 43, maxLon: 73.5, minLat: 23, maxLat: 47.6 };

const REGIONS = [
  { key: "khorasan", name: "خراسان و فرارود", color: "#0a6b60" },
  { key: "fars", name: "فارس و کرمان", color: "#b2532f" },
  { key: "center", name: "عراق عجم و شمال", color: "#1e3a8a" },
  { key: "azar", name: "آذربایجان و غرب", color: "#b8892a" },
  { key: "hind", name: "هند و شبه‌قاره", color: "#5b6b1f" },
  { key: "rum", name: "روم و عراق", color: "#7a3b5c" },
  { key: "none", name: "بی‌نشان", color: "#8a8174" },
];

const NET_KINDS = [
  { key: "kin", name: "خویشی", color: "#b8892a" },
  { key: "war", name: "دشمنی و نبرد", color: "#b4233c" },
  { key: "court", name: "سپاه و دربار", color: "#1e3a8a" },
  { key: "ally", name: "همراهی و جانشینی", color: "#0a6b60" },
];

const DEVICE_GROUP = {
  0: "بیان",
  1: "بدیع لفظی",
  2: "بدیع معنوی",
  Bayan: "بیان",
  BadiLafzi: "بدیع لفظی",
  BadiManavi: "بدیع معنوی",
};

const root = document.querySelector("#content");
const bar = document.querySelector("#bar");
const foot = document.querySelector("#foot");
const mobile = document.querySelector("#mobile");
const menuBtn = document.querySelector("#menu");
const barForm = document.querySelector("#search-form");
const barInput = document.querySelector("#q");

const cache = new Map();
const files = new Map();
let localData = null;
let deviceList = null;
let renderToken = 0;
let audioNode = null;
let activeTimer = 0;

/* ── ابزارهای پایه و ذخیره‌سازی محلی ── */
const store = {
  key: "ganjoor-no-read",
  get() {
    try {
      const data = JSON.parse(localStorage.getItem(this.key) || "{}");
      data.marks = data.marks || [];
      data.notes = data.notes || {};
      data.history = data.history || [];
      return data;
    } catch {
      return { marks: [], notes: {}, history: [] };
    }
  },
  set(data) {
    localStorage.setItem(this.key, JSON.stringify(data));
  },
  toggle(id) {
    const data = this.get();
    data.marks = data.marks.includes(id) ? data.marks.filter((x) => x !== id) : [id, ...data.marks];
    this.set(data);
  },
  note(id, text) {
    const data = this.get();
    data.notes[id] = text;
    this.set(data);
  },
  visit(id) {
    const data = this.get();
    data.history = [id, ...data.history.filter((x) => x !== id)].slice(0, 24);
    this.set(data);
  },
};

function esc(value) {
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" };
  return String(value ?? "").replace(/[&<>"]/g, (ch) => map[ch]);
}
function bare(text) {
  return String(text).replace(/[\u064B-\u065F\u0670\u0640]/g, "");
}
const fa = (v) => Number(v || 0).toLocaleString("fa-IR");
const yr = (v) => Number(v || 0).toLocaleString("fa-IR", { useGrouping: false });
const toGregorian = (hijri) => Math.round(hijri * 0.970229 + 621.5643);
const centuryOf = (year) => (year ? Math.floor((year - 1) / 100) + 1 : 0);

function project(lon, lat) {
  return {
    x: ((lon - REALM.minLon) / (REALM.maxLon - REALM.minLon)) * 100,
    y: ((REALM.maxLat - lat) / (REALM.maxLat - REALM.minLat)) * 100,
  };
}

function cityOf(poet) {
  const place = poet.birthPlace || "نامشخص";
  const name = `${poet.name || ""} ${poet.nickname || ""}`;
  if (place === "مشهد" && /توس|طوس|فردوسی/.test(name)) return "توس";
  return place;
}

function regionOf(poet) {
  const lat = poet.birthPlaceLatitude;
  const lon = poet.birthPlaceLongitude;
  if (!lat || !lon) return "none";
  if (lon < 45) return "rum";
  if (lon < 48.5) return "azar";
  if (lon >= 66 && lat < 33) return "hind";
  if ((lon >= 56 && lat >= 32.5) || lon >= 60.5) return "khorasan";
  if (lat < 32.3) return "fars";
  return "center";
}

function timelinePoets(list) {
  return (Array.isArray(list) ? list : [])
    .filter((p) => p.published !== false && (p.birthYearInLHijri || p.deathYearInLHijri))
    .map((p) => {
      let b = p.birthYearInLHijri || p.deathYearInLHijri - 60;
      let d = p.deathYearInLHijri || p.birthYearInLHijri + 60;
      const broken = d < b;
      if (broken) [b, d] = [d, b];
      return {
        ...p,
        b,
        d,
        broken,
        sureB: Boolean(p.birthYearInLHijri && p.validBirthDate && !broken),
        sureD: Boolean(p.deathYearInLHijri && p.validDeathDate && !broken),
        region: regionOf(p),
        label: p.nickname || p.name,
      };
    })
    .sort((x, y) => x.b - y.b || x.d - y.d);
}

function yearsText(poet) {
  return `${poet.birthYearInLHijri ? yr(poet.birthYearInLHijri) : ""}${poet.sureB ? "" : "؟"}–${poet.deathYearInLHijri ? yr(poet.deathYearInLHijri) : ""}${poet.sureD ? "" : "؟"} ق`;
}

/* ── تبدیل خودکار ارقام به فارسی ── */
const PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
const SKIP_DIGITS = new Set(["TEXTAREA", "INPUT", "SCRIPT", "STYLE", "CODE"]);
function persianDigits(node) {
  if (!node) return;
  const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, {
    acceptNode: (t) =>
      /[0-9]/.test(t.nodeValue) && !SKIP_DIGITS.has(t.parentNode?.nodeName) && !t.parentNode?.closest?.(".latin")
        ? NodeFilter.FILTER_ACCEPT
        : NodeFilter.FILTER_REJECT,
  });
  const list = [];
  while (walker.nextNode()) list.push(walker.currentNode);
  for (const t of list) t.nodeValue = t.nodeValue.replace(/[0-9]/g, (d) => PERSIAN_DIGITS[d]);
}
new MutationObserver((records) => {
  for (const r of records) {
    if (r.type === "characterData") persianDigits(r.target.parentNode || r.target);
    else r.addedNodes.forEach((n) => (n.nodeType === 3 ? persianDigits(n.parentNode) : n.nodeType === 1 && persianDigits(n)));
  }
}).observe(document.body, { childList: true, subtree: true, characterData: true });
persianDigits(document.body);

/* ── لایهٔ ارتباط با API گنجور و داده‌های باز ── */
function pagingTotal(res) {
  const raw = res.headers.get("paging-headers");
  if (raw) {
    try {
      const info = JSON.parse(raw);
      if (info.totalCount != null) return Number(info.totalCount);
    } catch {}
  }
  return Number(res.headers.get("items-count") || 0);
}

async function api(path) {
  if (cache.has(path)) return cache.get(path);
  const token = renderToken;
  const res = await fetch(API + path);
  if (!res.ok) throw new Error(String(res.status));
  const data = await res.json();
  const packed = { data, total: pagingTotal(res) };
  cache.set(path, packed);
  if (token !== renderToken) throw STALE;
  return packed;
}

async function rootApi(path) {
  const key = `root:${path}`;
  if (cache.has(key)) return cache.get(key).data;
  const token = renderToken;
  const res = await fetch(ROOT_API + path);
  if (!res.ok) throw new Error(String(res.status));
  const data = await res.json();
  cache.set(key, { data, total: 0 });
  if (token !== renderToken) throw STALE;
  return data;
}

async function fileJson(name) {
  if (files.has(name)) return files.get(name);
  const token = renderToken;
  let data = null;
  for (const base of DATA_SOURCES) {
    try {
      const res = await fetch(`${base}${name}`);
      if (!res.ok) continue;
      data = await res.json();
      break;
    } catch {}
  }
  if (data === null) throw new Error(`داده ${name} نیامد`);
  files.set(name, data);
  if (token !== renderToken) throw STALE;
  return data;
}

async function local() {
  if (localData) return localData;
  const res = await fetch("data.json");
  if (!res.ok) throw new Error("data.json");
  localData = await res.json();
  return localData;
}

async function devices() {
  if (!deviceList) deviceList = await rootApi("/ganjoor/literary/devices");
  return deviceList;
}

function stopTimers() {
  if (activeTimer) {
    clearInterval(activeTimer);
    activeTimer = 0;
  }
}

function paint(title, html, quiet = false) {
  document.title = `${title} — گنجور نو`;
  document.body.classList.toggle("quiet", quiet);
  bar.hidden = quiet;
  foot.hidden = quiet;
  root.innerHTML = html;
  root.removeAttribute("aria-busy");
  window.scrollTo(0, 0);
}

function loading(title) {
  paint(title, `<div class="loader" role="status"><span class="spin" aria-hidden="true"></span><span>در حال آوردن از گنجور…</span></div>`);
  root.setAttribute("aria-busy", "true");
}

function failed(error) {
  const offline = typeof navigator !== "undefined" && navigator.onLine === false;
  paint(
    "خطا",
    `<section class="subpage" style="text-align:center;">
       <h1>${offline ? "اینترنت وصل نیست" : "ارتباط برقرار نشد"}</h1>
       <p class="muted">${offline ? "اتصال را برقرار کنید و دوباره امتحان کنید." : "گنجور الان پاسخ نداد. چند لحظه بعد دوباره امتحان کنید."}</p>
       <p class="chips" style="justify-content:center;"><button class="btn primary" type="button" id="retry">تلاش دوباره</button><a class="chip" href="#/">بازگشت به صفحهٔ اول</a></p>
       <p class="muted small">${esc(error?.message || "")}</p>
     </section>`,
  );
  document.querySelector("#retry")?.addEventListener("click", () => {
    cache.clear();
    render();
  });
}

/* ── موتور بوم گردش‌پذیر (Pan/Zoom/Declutter) برای نقشه‌ها و گراف‌ها ── */
function atlasStage(atlas) {
  const stage = document.createElement("div");
  stage.className = "atlas-stage";
  stage.tabIndex = 0;
  stage.setAttribute("aria-label", "بوم تعاملی؛ با کشیدن جابه‌جا شوید و با چرخ ماوس بزرگ‌نمایی کنید");
  atlas.replaceWith(stage);
  stage.append(atlas);
  stage.insertAdjacentHTML(
    "beforeend",
    `<div class="stage-ctl" role="toolbar" aria-label="بزرگ‌نمایی"><button type="button" data-zoom="in" aria-label="بزرگ‌تر">+</button><button type="button" data-zoom="out" aria-label="کوچک‌تر">−</button><button type="button" data-zoom="fit">نمای کل</button></div>`,
  );
  let k = 1, tx = 0, ty = 0, frame = 0;
  const size = () => ({ w: stage.clientWidth || 1, h: stage.clientHeight || 1 });
  const clamp = () => {
    const { w, h } = size();
    k = Math.min(Math.max(k, 1), 8);
    tx = Math.min(0, Math.max(w - w * k, tx));
    ty = Math.min(0, Math.max(h - h * k, ty));
  };
  const declutter = () => {
    const box = stage.getBoundingClientRect();
    const dots = [...atlas.querySelectorAll(".pin i, .pin circle")].map((dot) => ({ r: dot.getBoundingClientRect(), pin: dot.parentElement }));
    const taken = [];
    const pins = [...atlas.querySelectorAll(".pin")].sort((a, b) => (Number(b.dataset.w) || 0) - (Number(a.dataset.w) || 0));
    for (const pin of pins) {
      const label = pin.querySelector("span, text");
      if (!label) continue;
      pin.classList.remove("hush");
      const r = label.getBoundingClientRect();
      const out = r.right < box.left || r.left > box.right || r.bottom < box.top || r.top > box.bottom;
      const meets = (o) => r.left < o.right + 2 && r.right > o.left - 2 && r.top < o.bottom + 1 && r.bottom > o.top - 1;
      const hit = taken.some(meets) || dots.some((dot) => dot.pin !== pin && (Number(dot.pin.dataset.w) || 0) >= (Number(pin.dataset.w) || 0) && meets(dot.r));
      if (out || hit) pin.classList.add("hush");
      else taken.push(r);
    }
  };
  const renderView = () => {
    clamp();
    atlas.style.transform = `translate(${tx.toFixed(1)}px,${ty.toFixed(1)}px) scale(${k.toFixed(4)})`;
    atlas.style.setProperty("--inv", (1 / k).toFixed(4));
    stage.classList.toggle("zoomed", k > 1.02);
    declutter();
  };
  const draw = () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(renderView);
  };
  const zoomAt = (sx, sy, factor) => {
    const next = Math.min(Math.max(k * factor, 1), 8);
    tx = sx - ((sx - tx) * next) / k;
    ty = sy - ((sy - ty) * next) / k;
    k = next;
    draw();
  };
  const pointers = new Map();
  let travelled = 0, pinch = 0;
  stage.addEventListener("pointerdown", (e) => {
    if (e.target.closest(".stage-ctl")) return;
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    travelled = 0;
    if (pointers.size === 2) {
      const [a, b] = [...pointers.values()];
      pinch = Math.hypot(a.x - b.x, a.y - b.y);
    }
  });
  stage.addEventListener("pointermove", (e) => {
    const last = pointers.get(e.pointerId);
    if (!last) return;
    const now = { x: e.clientX, y: e.clientY };
    const box = stage.getBoundingClientRect();
    if (pointers.size === 1) {
      travelled += Math.abs(now.x - last.x) + Math.abs(now.y - last.y);
      if (travelled > 6) {
        if (!stage.hasPointerCapture(e.pointerId)) stage.setPointerCapture(e.pointerId);
        stage.classList.add("grab");
        tx += now.x - last.x;
        ty += now.y - last.y;
        draw();
      }
      pointers.set(e.pointerId, now);
    } else if (pointers.size === 2) {
      pointers.set(e.pointerId, now);
      const [a, b] = [...pointers.values()];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      travelled += 20;
      if (pinch > 0) zoomAt((a.x + b.x) / 2 - box.left, (a.y + b.y) / 2 - box.top, d / pinch);
      pinch = d;
    }
  });
  const lift = (e) => {
    pointers.delete(e.pointerId);
    if (pointers.size < 2) pinch = 0;
    if (!pointers.size) stage.classList.remove("grab");
  };
  stage.addEventListener("pointerup", lift);
  stage.addEventListener("pointercancel", lift);
  stage.addEventListener("click", (e) => {
    if (travelled > 6 && !e.target.closest(".stage-ctl")) {
      e.preventDefault();
      e.stopPropagation();
    }
  }, true);
  stage.addEventListener("wheel", (e) => {
    e.preventDefault();
    const box = stage.getBoundingClientRect();
    zoomAt(e.clientX - box.left, e.clientY - box.top, Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0018)));
  }, { passive: false });
  stage.addEventListener("dblclick", (e) => {
    e.preventDefault();
    const box = stage.getBoundingClientRect();
    zoomAt(e.clientX - box.left, e.clientY - box.top, 2);
  });
  const reset = () => { k = 1; tx = 0; ty = 0; draw(); };
  stage.querySelector(".stage-ctl").addEventListener("click", (e) => {
    const btn = e.target.closest("[data-zoom]");
    if (!btn) return;
    const { w, h } = size();
    if (btn.dataset.zoom === "in") zoomAt(w / 2, h / 2, 1.6);
    else if (btn.dataset.zoom === "out") zoomAt(w / 2, h / 2, 1 / 1.6);
    else reset();
  });
  const watch = new ResizeObserver(() => (document.body.contains(stage) ? draw() : watch.disconnect()));
  watch.observe(stage);
  draw();
  document.fonts?.ready.then(draw);
  return { refresh: draw, reset };
}

/* ==========================================================================
   صفحهٔ اصلی یکپارچه (Unified Landing Page) — همهٔ ۷ ابزار واقعی + تالار شاعران + کتابخانه
   ========================================================================== */
const STUDIO_TABS = [
  { id: "tree", label: "هم‌عصران و نقشه", icon: "❦" },
  { id: "bridges", label: "پل‌های تضمین", icon: "⇄" },
  { id: "people", label: "مردمان شعر", icon: "♙" },
  { id: "devices", label: "آرایه‌های ادبی", icon: "✦" },
  { id: "words", label: "واژه‌سنج و جستجو", icon: "≋" },
  { id: "places", label: "جای‌ها در شعر", icon: "⌖" },
  { id: "vazn", label: "وزن‌ها و عروض", icon: "♪" },
];

let landingState = {
  mounted: false,
  poets: [],
  activeTool: "tree",
  activateTool: null,
};

async function landingPage(opts = {}) {
  const targetTool = opts.tool || "tree";
  const scrollTarget = opts.scrollTo || null;

  // اگر لندینگ همین الان روی صفحه است، بدون رندر مجدد فقط ابزار مورد نظر را فعال کن!
  if (landingState.mounted && document.querySelector("#studio-stage") && landingState.activateTool) {
    if (opts.tool) await landingState.activateTool(targetTool, opts.params || {});
    if (scrollTarget) document.getElementById(scrollTarget)?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }

  loading("گنجور نو");
  const { data: poetsRaw } = await api("/poets").catch(() => ({ data: [] }));
  const poets = Array.isArray(poetsRaw) ? poetsRaw : [];
  const tPoets = timelinePoets(poets);
  landingState.poets = poets;

  paint(
    "اقلیم دیداری شعر پارسی",
    `
    <!-- ۱. هیروی تحریریه -->
    <section class="hero">
      <h1 class="hero-title">اقلیم دیداری <span>شعر پارسی</span></h1>
      <div class="hero-search-wrap">
        <form class="hero-search" id="hero-search-form" role="search">
          <span class="hero-search-icon" aria-hidden="true">⌕</span>
          <input id="hero-q" name="q" placeholder="نام شاعر (مثلاً بیدل، حافظ)، واژه یا تکه‌ای از بیت…" autocomplete="off" />
          <button type="submit">جستجو</button>
        </form>
        <div class="suggest-drop" id="hero-suggest" hidden></div>
      </div>
      <div class="hero-metrics">
        <span><b>${fa(poets.length)}</b> شاعر پارسی‌گوی</span>
        <span><b>هزار سال</b> خط زمان و جغرافیا</span>
        <span><b>۷ ابزار</b> پژوهشی زنده روی داده‌های باز گنجور</span>
      </div>
    </section>

    <!-- ۲. استودیوی یکپارچهٔ ابزارها -->
    <section class="studio" id="studio" aria-label="ابزارهای دیداری گنجور نو">
      <nav class="studio-rail" id="studio-rail" role="tablist">
        ${STUDIO_TABS.map(
          (t) => `<button type="button" class="studio-tab ${t.id === targetTool ? "active" : ""}" role="tab" aria-selected="${t.id === targetTool}" data-tool="${t.id}"><span class="ti" aria-hidden="true">${t.icon}</span><span>${t.label}</span></button>`,
        ).join("")}
      </nav>
      <div class="studio-stage" id="studio-stage"></div>
    </section>

    <!-- ۳. تالار شاعران -->
    <section class="landing-section" id="poets-wall">
      <div class="section-head">
        <div>
          <h2>تالار شاعران</h2>
          <p class="tool-sub">از رودکی تا امروز؛ روی هر شاعر بزنید تا وارد صفحهٔ دیوان و آثارش شوید.</p>
        </div>
        <div class="inline-search" style="margin:0;min-width:min(100%, 280px);">
          <input id="poets-wall-q" placeholder="پالایش نام شاعر یا شهر…" autocomplete="off" />
        </div>
      </div>
      <div class="poets-grid" id="poets-wall-grid"></div>
      <p style="text-align:center;margin-top:14px;" id="poets-wall-more-wrap"></p>
    </section>

    <!-- ۴. کتابخانهٔ من -->
    <section class="landing-section" id="my-shelf">
      <div class="section-head">
        <div>
          <h2>کتابخانهٔ من</h2>
          <p class="tool-sub">شعرهای نشان‌شده، یادداشت‌ها و آخرین خوانش‌های شما (ذخیره‌شده روی همین دستگاه).</p>
        </div>
      </div>
      <div id="my-shelf-body"><p class="muted">در حال خواندن کتابخانه…</p></div>
    </section>
    `,
  );

  landingState.mounted = true;
  const stageEl = document.querySelector("#studio-stage");
  const railEl = document.querySelector("#studio-rail");

  let toolToken = 0;
  const activateTool = async (toolId, params = {}) => {
    stopTimers();
    const mine = ++toolToken;
    landingState.activeTool = toolId;
    railEl.querySelectorAll(".studio-tab").forEach((btn) => {
      const on = btn.dataset.tool === toolId;
      btn.classList.toggle("active", on);
      btn.setAttribute("aria-selected", String(on));
    });
    stageEl.innerHTML = `<div class="loader"><span class="spin"></span><span>در حال آماده‌سازی ابزار…</span></div>`;
    try {
      if (toolId === "tree") await mountContemporariesTool(stageEl, poets, tPoets, params, () => mine !== toolToken);
      else if (toolId === "bridges") await mountBridgesTool(stageEl, poets, params, () => mine !== toolToken);
      else if (toolId === "people") await mountPeopleTool(stageEl, params, () => mine !== toolToken);
      else if (toolId === "devices") await mountDevicesTool(stageEl, params, () => mine !== toolToken);
      else if (toolId === "words") await mountWordsTool(stageEl, poets, params, () => mine !== toolToken);
      else if (toolId === "places") await mountPlacesTool(stageEl, params, () => mine !== toolToken);
      else if (toolId === "vazn") await mountVaznTool(stageEl, params, () => mine !== toolToken);
    } catch (err) {
      if (err === STALE || mine !== toolToken) return;
      stageEl.innerHTML = `<div class="panel"><p class="muted">دریافت داده برای این ابزار با خطا روبه‌رو شد: ${esc(err?.message || "")}</p></div>`;
    }
  };
  landingState.activateTool = activateTool;

  railEl.onclick = (e) => {
    const btn = e.target.closest("[data-tool]");
    if (!btn) return;
    activateTool(btn.dataset.tool, {});
  };

  /* ── جستجوی زندهٔ هیرو (پیشنهاد آنی شاعر برای خط زمان یا دیوان + جستجوی واژه در استودیو) ── */
  const heroForm = document.querySelector("#hero-search-form");
  const heroInput = document.querySelector("#hero-q");
  const heroDrop = document.querySelector("#hero-suggest");

  heroInput.addEventListener("input", () => {
    const q = heroInput.value.trim();
    if (q.length < 2) {
      heroDrop.hidden = true;
      return;
    }
    const hits = poets
      .filter((p) => `${p.nickname || ""} ${p.name || ""} ${p.birthPlace || ""}`.includes(q))
      .slice(0, 6);
    if (!hits.length) {
      heroDrop.hidden = true;
      return;
    }
    heroDrop.hidden = false;
    heroDrop.innerHTML = hits
      .map(
        (p) => `
      <div class="suggest-row">
        <div>
          <strong>${esc(p.nickname || p.name)}</strong>
          <small>${p.birthYearInLHijri ? `${yr(p.birthYearInLHijri)}–${yr(p.deathYearInLHijri || 0)} ق` : ""}${p.birthPlace ? ` · ${esc(p.birthPlace)}` : ""}</small>
        </div>
        <div class="suggest-acts">
          <button type="button" class="suggest-tag" data-hero-tree="${p.id}">روی خط زمان</button>
          <a class="suggest-tag" href="#/poet/${p.id}">دیوان اشعار</a>
        </div>
      </div>`,
      )
      .join("");
  });

  heroDrop.addEventListener("click", (e) => {
    const treeBtn = e.target.closest("[data-hero-tree]");
    if (treeBtn) {
      heroDrop.hidden = true;
      heroInput.value = "";
      document.getElementById("studio")?.scrollIntoView({ behavior: "smooth", block: "start" });
      activateTool("tree", { poet: treeBtn.dataset.heroTree, view: "timeline" });
    }
  });

  document.addEventListener("click", (e) => {
    if (heroDrop && !e.target.closest(".hero-search-wrap")) heroDrop.hidden = true;
  });

  heroForm.onsubmit = (e) => {
    e.preventDefault();
    const q = heroInput.value.trim();
    if (!q) return;
    heroDrop.hidden = true;
    document.getElementById("studio")?.scrollIntoView({ behavior: "smooth", block: "start" });
    activateTool("words", { q });
  };

  /* ── تالار شاعران ── */
  const pinned = [...poets].filter((p) => p.pinOrder).sort((a, b) => a.pinOrder - b.pinOrder);
  const pinnedIds = new Set(pinned.map((p) => p.id));
  const orderedPoets = pinned.concat(
    poets
      .filter((p) => !pinnedIds.has(p.id))
      .sort((a, b) => (a.birthYearInLHijri || 9999) - (b.birthYearInLHijri || 9999) || (a.nickname || "").localeCompare(b.nickname || "", "fa")),
  );
  const wallGrid = document.querySelector("#poets-wall-grid");
  const wallQ = document.querySelector("#poets-wall-q");
  const wallMore = document.querySelector("#poets-wall-more-wrap");
  let showAllPoets = false;

  const drawWall = () => {
    const q = wallQ.value.trim();
    const list = orderedPoets.filter((p) => !q || `${p.nickname || ""} ${p.name || ""} ${p.birthPlace || ""}`.includes(q));
    const slice = q || showAllPoets ? list : list.slice(0, 24);
    wallGrid.innerHTML = slice
      .map((p) => {
        const letter = esc((p.nickname || p.name || "؟").slice(0, 1));
        const img = p.imageUrl ? `<img alt="" loading="lazy" src="https://api.ganjoor.net${esc(p.imageUrl)}" onerror="this.remove()" />` : "";
        const yrs = p.birthYearInLHijri ? `${yr(p.birthYearInLHijri)}–${p.deathYearInLHijri ? yr(p.deathYearInLHijri) : "؟"} ق` : "";
        return `<a class="face" href="#/poet/${p.id}"><span class="medal">${img}<b>${letter}</b></span><strong>${esc(p.nickname || p.name)}</strong><small>${esc(p.birthPlace || "")}${yrs ? " · " + yrs : ""}</small></a>`;
      })
      .join("") || `<p class="muted">شاعری با این نام پیدا نشد.</p>`;
    wallMore.innerHTML =
      !q && !showAllPoets && list.length > 24
        ? `<button type="button" class="btn" id="btn-show-all-poets">نمایش همهٔ ${fa(list.length)} شاعر</button>`
        : "";
    document.querySelector("#btn-show-all-poets")?.addEventListener("click", () => {
      showAllPoets = true;
      drawWall();
    });
  };
  wallQ.oninput = drawWall;
  drawWall();

  /* ── کتابخانهٔ شخصی ── */
  renderShelf(document.querySelector("#my-shelf-body"));

  /* ── فعال‌سازی ابزار اولیه ── */
  await activateTool(targetTool, opts.params || {});
  if (scrollTarget) {
    setTimeout(() => document.getElementById(scrollTarget)?.scrollIntoView({ behavior: "smooth", block: "start" }), 60);
  }
}

async function renderShelf(container) {
  if (!container) return;
  const saved = store.get();
  const noteIds = Object.entries(saved.notes)
    .filter(([, t]) => String(t).trim())
    .map(([id]) => Number(id));
  const ids = [...new Set([...saved.marks, ...noteIds, ...saved.history])].slice(0, 12);
  if (!ids.length) {
    container.innerHTML = `<p class="muted">هنوز شعری را نشان نکرده‌اید یا نخوانده‌اید. با باز کردن هر شعر، می‌توانید آن را نشان کنید یا یادداشت بنویسید تا همین‌جا بماند.</p>`;
    return;
  }
  const items = await Promise.all(
    ids.map((id) =>
      api(`/poem/${id}?catInfo=true&verseDetails=false&recitations=false&navigation=false&comments=false&images=false&songs=false`)
        .then((r) => r.data)
        .catch(() => null),
    ),
  );
  const valid = items.filter(Boolean);
  container.innerHTML = valid.length
    ? `<div class="grid">${valid
        .map((poem) => {
          const p = poem.category?.poet;
          const isMark = saved.marks.includes(poem.id);
          const note = saved.notes[poem.id];
          return `<a class="hit" href="#/poem/${poem.id}"><div class="kicker">${isMark ? "★ نشان‌شده · " : ""}${esc(p?.nickname || p?.name || "")}</div><strong>${esc(poem.title)}</strong>${note ? `<p>یادداشت: ${esc(note.slice(0, 90))}</p>` : ""}</a>`;
        })
        .join("")}</div>`
    : `<p class="muted">موردی در کتابخانه نیست.</p>`;
}

/* ==========================================================================
   ابزار ۱: هم‌عصران و نقشهٔ زادگاه‌ها (سوییچ درجا بدون تغییر صفحه!)
   ========================================================================== */
async function mountContemporariesTool(container, allPoets, poets, params, isStale) {
  const learn = await local().catch(() => ({}));
  if (isStale()) return;

  let viewMode = params.view === "map" ? "map" : "timeline";
  container.innerHTML = `
    <div class="tool-head">
      <div>
        <h2>هم‌عصران و جغرافیای زادگاه‌ها</h2>
        <p class="tool-sub">زندگی ${fa(poets.length)} شاعر از راست به چپ؛ میان خط زمان و نقشهٔ زادگاه‌ها بدون خروج از صفحه جابه‌جا شوید.</p>
      </div>
      <div class="seg-switch" role="tablist" aria-label="نمای هم‌عصران">
        <button type="button" class="seg-btn ${viewMode === "timeline" ? "active" : ""}" data-subview="timeline">خط زمان</button>
        <button type="button" class="seg-btn ${viewMode === "map" ? "active" : ""}" data-subview="map">نقشهٔ زادگاه‌ها</button>
      </div>
    </div>
    <div id="contemp-body"></div>
  `;

  const body = container.querySelector("#contemp-body");
  const switchView = (mode, subParams = {}) => {
    stopTimers();
    viewMode = mode;
    container.querySelectorAll("[data-subview]").forEach((b) => b.classList.toggle("active", b.dataset.subview === mode));
    if (mode === "timeline") renderTimelineCanvas(body, poets, learn, subParams);
    else renderBirthplaceMap(body, allPoets, subParams);
  };

  container.querySelectorAll("[data-subview]").forEach((b) => {
    b.onclick = () => switchView(b.dataset.subview, {});
  });

  switchView(viewMode, params);
}

function renderTimelineCanvas(container, poets, learn, params) {
  const byId = new Map(poets.map((p) => [String(p.id), p]));
  const regionInfo = new Map(REGIONS.map((r) => [r.key, r]));
  const used = REGIONS.filter((r) => poets.some((p) => p.region === r.key));

  const PX = 0.86;
  const from = Math.floor(Math.min(...poets.map((p) => p.b)) / 100) * 100;
  const to = Math.ceil(Math.max(...poets.map((p) => p.d)) / 100) * 100;
  const PAD = 18;
  const W = Math.round((to - from) * PX + PAD * 2);
  const x = (year) => W - PAD - (year - from) * PX;
  const yearAt = (cx) => from + (W - PAD - cx) / PX;

  const ROW = 14;
  const KREF = 1.4;
  const labelYears = (p) => (p.label.length * (p.pinOrder ? 7.6 : 6.8) + 12) / (PX * KREF);
  const laneEnd = [];
  for (const p of poets) {
    let lane = laneEnd.findIndex((end) => end < p.b - 3);
    if (lane < 0) lane = laneEnd.length;
    laneEnd[lane] = p.d + labelYears(p);
    p.lane = lane;
  }
  const H = laneEnd.length * ROW + 16;
  const yOf = (p) => p.lane * ROW + 4;

  const decades = [];
  for (let year = from; year <= to; year += 10) decades.push({ year, n: poets.filter((p) => p.b <= year + 5 && p.d >= year + 5).length });
  const peak = decades.reduce((best, item) => (item.n > best.n ? item : best), decades[0]);
  const toHijri = (g) => Math.round((g - 621.5643) / 0.970229);
  const eras = (learn.events || []).map((item) => ({ ...item, h: toHijri(item.year) })).filter((item) => item.h >= from && item.h <= to);

  const gradients = used
    .map((r) =>
      [
        ["b", "1", "0.3", "1", "0.6"],
        ["d", "0.3", "1", "0.4", "1"],
        ["bd", "0.3", "0.3", "0.35", "0.65"],
      ]
        .map(
          ([kind, left, right, a, z]) =>
            `<linearGradient id="g-${r.key}-${kind}"><stop offset="0" stop-color="${r.color}" stop-opacity="${left}"/><stop offset="${a}" stop-color="${r.color}"/><stop offset="${z}" stop-color="${r.color}"/><stop offset="1" stop-color="${r.color}" stop-opacity="${right}"/></linearGradient>`,
        )
        .join(""),
    )
    .join("");

  const fill = (p) => {
    const kind = (p.sureB ? "" : "b") + (p.sureD ? "" : "d");
    return kind ? `url(#g-${p.region}-${kind})` : regionInfo.get(p.region).color;
  };
  const barSvg = (p) => {
    const y = yOf(p);
    const x1 = x(p.d);
    const width = Math.max(3, x(p.b) - x1);
    const strong = p.pinOrder ? " famous" : "";
    return `<g class="life${strong}" data-id="${p.id}" data-region="${p.region}" tabindex="0" role="button"><title>${esc(p.name)} · ${esc(yearsText(p))}${p.birthPlace ? ` · ${esc(p.birthPlace)}` : ""}</title><rect class="hit" x="${(x1 - (p.label.length * 7 + 10) / KREF).toFixed(1)}" y="${y}" width="${(width + (p.label.length * 7 + 12) / KREF).toFixed(1)}" height="${ROW}"/><rect class="span" x="${x1.toFixed(1)}" y="${y + (p.pinOrder ? 4 : 5)}" width="${width.toFixed(1)}" height="${p.pinOrder ? 6 : 4}" rx="2" fill="${fill(p)}"/><text x="${(x1 - 3).toFixed(1)}" y="${y + 7}">${esc(p.label)}</text></g>`;
  };
  const centuries = [];
  for (let year = from; year <= to; year += 100) centuries.push(year);
  const MINI_W = 160;
  const MINI_H = Math.max(58, Math.min(115, Math.round((MINI_W * H) / W)));
  const mx = MINI_W / W;
  const my = MINI_H / H;

  container.innerHTML = `
    <div class="inline-search" id="tree-search-wrap">
      <input id="tree-q" placeholder="جستجوی شاعر یا شهر روی خط زمان (مثلاً بیدل، صائب، شیراز…)" autocomplete="off" />
      <div class="suggest-drop" id="tree-suggest" hidden></div>
    </div>
    <p class="chips" id="tree-regions">
      <button class="chip on" type="button" data-region="">همه سرزمین‌ها</button>
      ${used.map((r) => `<button class="chip" type="button" data-region="${r.key}" style="--tone:${r.color}"><i class="dot"></i>${r.name} · ${fa(poets.filter((p) => p.region === r.key).length)}</button>`).join("")}
    </p>
    <div class="stage" id="stage" tabindex="0">
      <svg class="stage-head" id="shead" aria-hidden="true"></svg>
      <svg class="chrono" id="chrono">
        <defs>${gradients}</defs>
        <g id="view">
          <g class="axis">${centuries.map((year) => `<line x1="${x(year)}" x2="${x(year)}" y1="0" y2="${H}"/>`).join("")}</g>
          <g class="eras">${eras.map((item) => `<line x1="${x(item.h)}" x2="${x(item.h)}" y1="0" y2="${H}"/>`).join("")}</g>
          <rect class="band" id="band" y="0" height="${H}" hidden/>
          <g id="arcs"></g>
          <g id="lives">${poets.map(barSvg).join("")}</g>
        </g>
        <g id="tags" aria-hidden="true"></g>
      </svg>
      <div class="stage-ctl" role="toolbar">
        <button type="button" data-zoom="in" aria-label="بزرگ‌تر">+</button>
        <button type="button" data-zoom="out" aria-label="کوچک‌تر">−</button>
        <button type="button" data-zoom="fit">نمای کل</button>
        <button type="button" data-zoom="full">تمام‌صفحه</button>
      </div>
      <svg class="mini" id="mini" viewBox="0 0 ${MINI_W} ${MINI_H}" width="${MINI_W}" height="${MINI_H}">
        ${poets.map((p) => `<rect x="${(x(p.d) * mx).toFixed(1)}" y="${(yOf(p) * my).toFixed(1)}" width="${Math.max(1, (x(p.b) - x(p.d)) * mx).toFixed(1)}" height="${Math.max(1, 4 * my).toFixed(1)}" fill="${regionInfo.get(p.region).color}"/>`).join("")}
        <rect class="lens" id="lens"/>
      </svg>
      <p class="stage-hint">بکشید تا جابه‌جا شوید · اسکرول برای بزرگ‌نمایی · روی هر شاعر بزنید</p>
      <div class="focus" id="tree-focus" hidden></div>
    </div>
    <p class="key muted"><span class="sw solid"></span> سال ثبت‌شده <span class="sw fade"></span> سال تقریبی · بالای نمودار: اوج هم‌زیستی (${fa(peak.n)} شاعر زنده حدود ${yr(peak.year)} ق)</p>
  `;

  const stage = container.querySelector("#stage");
  const chart = container.querySelector("#chrono");
  const view = chart.querySelector("#view");
  const tags = chart.querySelector("#tags");
  const headSvg = container.querySelector("#shead");
  const lens = container.querySelector("#lens");
  const mini = container.querySelector("#mini");
  const lives = [...chart.querySelectorAll(".life")];
  const band = chart.querySelector("#band");
  const arcs = chart.querySelector("#arcs");
  const focus = container.querySelector("#tree-focus");
  const box = container.querySelector("#tree-q");
  const drop = container.querySelector("#tree-suggest");

  let region = "", picked = null, ask = 0, linkedIds = new Set();
  let k = 1, tx = 0, ty = 0, fitK = 1, fitted = true, frame = 0, flight = 0;

  const size = () => ({ w: chart.clientWidth || 1, h: chart.clientHeight || 1 });
  const clampAxis = (t, span, room) => (span + 80 <= room ? (room - span) / 2 : Math.min(40, Math.max(room - span - 40, t)));
  const clamp = () => {
    const { w, h } = size();
    k = Math.min(Math.max(k, fitK * 0.8), 9);
    tx = clampAxis(tx, W * k, w);
    ty = clampAxis(ty, H * k, h);
  };
  const near = () => k >= KREF * 0.9;

  const renderHead = () => {
    const { w } = size();
    const HEAD = 92;
    headSvg.setAttribute("viewBox", `0 0 ${w} ${HEAD}`);
    const sx = (year) => tx + k * x(year);
    const lo = Math.min(yearAt(-tx / k), yearAt((w - tx) / k));
    const hi = Math.max(yearAt(-tx / k), yearAt((w - tx) / k));
    const step = [10, 20, 25, 50, 100, 200].find((item) => item * PX * k >= 74) || 200;
    const ticks = [];
    for (let year = Math.ceil(Math.max(lo, from) / step) * step; year <= Math.min(hi, to); year += step) ticks.push(year);
    const top = 22, base = 58;
    const dy = (n) => base - (n / peak.n) * (base - top);
    const area = `M${sx(from).toFixed(1)},${base} ${decades.map((item) => `L${sx(item.year + 5).toFixed(1)},${dy(item.n).toFixed(1)}`).join(" ")} L${sx(to).toFixed(1)},${base} Z`;
    const placed = [];
    const eraTags = eras
      .map((item) => ({ ...item, at: sx(item.h) }))
      .filter((item) => item.at > 0 && item.at < w)
      .sort((a, b) => b.at - a.at)
      .filter((item) => {
        const wide = item.title.length * 6.4 + 12;
        if (placed.some((o) => o.at - item.at < o.wide) || item.at - wide < 0) return false;
        placed.push({ at: item.at, wide });
        return true;
      });
    const px = sx(peak.year + 5);
    const peakTag = px > 90 && px < w - 10 ? `<line x1="${px.toFixed(1)}" x2="${px.toFixed(1)}" y1="${dy(peak.n).toFixed(1)}" y2="${base}"/><text x="${(px - 4).toFixed(1)}" y="${base - 5}">اوج: ${fa(peak.n)} شاعر زنده</text>` : "";
    headSvg.innerHTML = `<g class="dens"><path d="${area}"/>${peakTag}</g>
      <g class="eras">${eras.map((item) => `<line x1="${sx(item.h).toFixed(1)}" x2="${sx(item.h).toFixed(1)}" y1="16" y2="${HEAD}"/>`).join("")}${eraTags.map((item) => `<text x="${(item.at - 3).toFixed(1)}" y="12"><title>${esc(item.text)}</title>${esc(item.title)}</text>`).join("")}</g>
      <g class="axis">${ticks.map((year) => `<line x1="${sx(year).toFixed(1)}" x2="${sx(year).toFixed(1)}" y1="${base}" y2="${base + 5}"/><text x="${sx(year).toFixed(1)}" y="${base + 18}">${yr(year)} ق</text><text class="greg" x="${sx(year).toFixed(1)}" y="${base + 31}">${yr(toGregorian(year))} م</text>`).join("")}</g>`;
  };

  const renderTags = () => {
    if (near()) { tags.innerHTML = ""; return; }
    const { w, h } = size();
    const boxes = [];
    const want = poets
      .filter((p) => p.pinOrder || p === picked || linkedIds.has(String(p.id)))
      .sort((a, b) => (b === picked) - (a === picked) || (a.pinOrder || 99) - (b.pinOrder || 99));
    const out = [];
    for (const p of want) {
      const ax = tx + k * (x(p.d) - 3);
      const ay = ty + k * (yOf(p) + 7) + 4.5;
      const wide = p.label.length * 7.6 + 8;
      const rect = { l: ax - wide, r: ax, t: ay - 12, b: ay + 4 };
      if (rect.l < 2 || rect.r > w - 2 || rect.t < 2 || rect.b > h - 2) continue;
      if (boxes.some((o) => rect.l < o.r && rect.r > o.l && rect.t < o.b && rect.b > o.t)) continue;
      boxes.push(rect);
      const cls = p === picked ? "picked" : linkedIds.has(String(p.id)) ? "linked" : "";
      out.push(`<text class="${cls}" x="${ax.toFixed(1)}" y="${ay.toFixed(1)}" data-id="${p.id}">${esc(p.label)}</text>`);
    }
    tags.innerHTML = out.join("");
  };

  const renderCanvas = () => {
    clamp();
    view.setAttribute("transform", `translate(${tx.toFixed(2)},${ty.toFixed(2)}) scale(${k.toFixed(4)})`);
    chart.classList.toggle("near", near());
    stage.classList.toggle("zoomed", k > fitK * 1.15);
    chart.style.setProperty("--fs", `${(11.5 / k).toFixed(3)}px`);
    chart.style.setProperty("--fs-big", `${(12.5 / k).toFixed(3)}px`);
    renderHead();
    renderTags();
    const { w, h } = size();
    lens.setAttribute("x", ((-tx / k) * mx).toFixed(1));
    lens.setAttribute("y", ((-ty / k) * my).toFixed(1));
    lens.setAttribute("width", ((w / k) * mx).toFixed(1));
    lens.setAttribute("height", ((h / k) * my).toFixed(1));
  };
  const draw = () => { cancelAnimationFrame(frame); frame = requestAnimationFrame(renderCanvas); };
  const fit = () => {
    const { w, h } = size();
    fitK = Math.min(w / W, h / H) * 0.97;
    k = fitK; tx = (w - W * k) / 2; ty = (h - H * k) / 2; fitted = true;
    draw();
  };
  const zoomAt = (sx, sy, factor) => {
    const next = Math.min(Math.max(k * factor, fitK * 0.8), 9);
    tx = sx - ((sx - tx) * next) / k;
    ty = sy - ((sy - ty) * next) / k;
    k = next; fitted = false; draw();
  };
  const flyTo = (cx, cy, targetK, at) => {
    const { w, h } = size();
    const spot = at || { x: w / 2, y: h / 2 };
    const start = { k, tx, ty };
    const endK = Math.min(Math.max(targetK, fitK), 9);
    const end = { k: endK, tx: spot.x - cx * endK, ty: spot.y - cy * endK };
    const t0 = performance.now();
    fitted = false;
    const step = (now) => {
      const p = Math.min(1, (now - t0) / 480);
      const e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      k = start.k + (end.k - start.k) * e;
      tx = start.tx + (end.tx - start.tx) * e;
      ty = start.ty + (end.ty - start.ty) * e;
      renderCanvas();
      if (p < 1) flight = requestAnimationFrame(step);
    };
    cancelAnimationFrame(flight);
    flight = requestAnimationFrame(step);
  };
  const scrollToPoet = (p) => {
    const { w, h } = size();
    const open = !focus.hidden;
    const spot = { x: open && w >= 640 ? Math.min(w - 120, focus.offsetWidth + 20 + (w - focus.offsetWidth - 20) / 2) : w / 2, y: h / 2 };
    flyTo((x(p.b) + x(p.d)) / 2 - 20, yOf(p) + 7, Math.max(k, KREF * 1.6), spot);
  };

  const pointers = new Map();
  let travelled = 0, pinch = null;
  chart.addEventListener("pointerdown", (e) => {
    cancelAnimationFrame(flight);
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    travelled = 0;
    if (pointers.size === 2) {
      const [a, b] = [...pointers.values()];
      pinch = { d: Math.hypot(a.x - b.x, a.y - b.y) };
    }
  });
  chart.addEventListener("pointermove", (e) => {
    const last = pointers.get(e.pointerId);
    if (!last) return;
    const now = { x: e.clientX, y: e.clientY };
    const bRect = chart.getBoundingClientRect();
    if (pointers.size === 1) {
      travelled += Math.abs(now.x - last.x) + Math.abs(now.y - last.y);
      if (travelled > 5) {
        if (!chart.hasPointerCapture(e.pointerId)) chart.setPointerCapture(e.pointerId);
        chart.classList.add("grab");
        tx += now.x - last.x; ty += now.y - last.y; fitted = false; draw();
      }
      pointers.set(e.pointerId, now);
    } else if (pointers.size === 2 && pinch) {
      pointers.set(e.pointerId, now);
      const [a, b] = [...pointers.values()];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if (pinch.d > 0) zoomAt((a.x + b.x) / 2 - bRect.left, (a.y + b.y) / 2 - bRect.top, d / pinch.d);
      pinch.d = d;
    }
  });
  const endPtr = (e) => {
    pointers.delete(e.pointerId);
    if (pointers.size < 2) pinch = null;
    if (!pointers.size) chart.classList.remove("grab");
  };
  chart.addEventListener("pointerup", endPtr);
  chart.addEventListener("pointercancel", endPtr);
  chart.addEventListener("wheel", (e) => {
    e.preventDefault();
    cancelAnimationFrame(flight);
    const bRect = chart.getBoundingClientRect();
    zoomAt(e.clientX - bRect.left, e.clientY - bRect.top, Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0018)));
  }, { passive: false });
  chart.addEventListener("dblclick", (e) => {
    e.preventDefault();
    const bRect = chart.getBoundingClientRect();
    zoomAt(e.clientX - bRect.left, e.clientY - bRect.top, 2.1);
  });
  mini.addEventListener("pointerdown", (e) => {
    e.stopPropagation();
    const bRect = mini.getBoundingClientRect();
    const cx = ((e.clientX - bRect.left) / bRect.width) * W;
    const cy = ((e.clientY - bRect.top) / bRect.height) * H;
    const { w, h } = size();
    if (k <= fitK * 1.05) k = fitK * 2.5;
    tx = w / 2 - cx * k; ty = h / 2 - cy * k; fitted = false; draw();
  });
  stage.querySelector(".stage-ctl").onclick = (e) => {
    const btn = e.target.closest("[data-zoom]");
    if (!btn) return;
    const { w, h } = size();
    if (btn.dataset.zoom === "in") zoomAt(w / 2, h / 2, 1.6);
    else if (btn.dataset.zoom === "out") zoomAt(w / 2, h / 2, 1 / 1.6);
    else if (btn.dataset.zoom === "fit") fit();
    else if (btn.dataset.zoom === "full") {
      if (document.fullscreenElement) document.exitFullscreen();
      else stage.requestFullscreen?.().catch(() => stage.classList.toggle("wide"));
    }
  };

  const paintState = () => {
    const q = box.value.trim();
    const peers = picked ? new Set(poets.filter((o) => o.b <= picked.d && o.d >= picked.b).map((o) => String(o.id))) : null;
    chart.classList.toggle("dim", Boolean(q || region || picked));
    for (const node of lives) {
      const p = byId.get(node.dataset.id);
      const text = `${p.nickname || ""} ${p.name || ""} ${p.birthPlace || ""}`;
      const match = (!q || text.includes(q)) && (!region || p.region === region) && (!peers || peers.has(node.dataset.id));
      node.classList.toggle("on", match);
      node.classList.toggle("picked", picked?.id === p.id);
    }
    renderTags();
  };

  const drawLinks = (links) => {
    if (!picked) return;
    const most = Math.max(1, ...links.map((l) => l.n));
    const cx = (p) => (x(p.b) + x(p.d)) / 2;
    linkedIds = new Set(links.slice(0, 12).map((l) => String(l.id)));
    arcs.innerHTML = links
      .slice(0, 12)
      .map((link) => {
        const other = byId.get(String(link.id));
        if (!other) return "";
        const ax = cx(picked), ay = yOf(picked) + 7, bx = cx(other), by = yOf(other) + 7;
        const lift = Math.min(90, 18 + Math.hypot(bx - ax, by - ay) * 0.25);
        return `<path d="M${ax.toFixed(1)},${ay.toFixed(1)} Q${((ax + bx) / 2).toFixed(1)},${(Math.min(ay, by) - lift).toFixed(1)} ${bx.toFixed(1)},${by.toFixed(1)}" style="stroke-width:${(0.8 + (link.n / most) * 3.2).toFixed(1)}"/>`;
      })
      .join("");
    for (const l of links.slice(0, 12)) chart.querySelector(`.life[data-id="${l.id}"]`)?.classList.add("on", "linked");
    renderTags();
  };

  const select = async (id, jump = false) => {
    const poet = byId.get(String(id));
    if (!poet) return;
    picked = poet;
    linkedIds = new Set();
    lives.forEach((n) => n.classList.remove("linked"));
    arcs.innerHTML = "";
    band.removeAttribute("hidden");
    band.setAttribute("x", x(poet.d));
    band.setAttribute("width", Math.max(3, x(poet.b) - x(poet.d)));
    paintState();

    const peers = poets.filter((o) => o.id !== poet.id && o.b <= poet.d && o.d >= poet.b);
    const overlap = (o) => Math.max(0, Math.min(poet.d, o.d) - Math.max(poet.b, o.b));
    const topPeers = [...peers]
      .sort((a, b) => (a.pinOrder || 999) - (b.pinOrder || 999) || overlap(b) - overlap(a))
      .slice(0, 6);
    const c1 = centuryOf(poet.b), c2 = centuryOf(poet.d);
    const cText = c1 === c2 ? `قرن ${fa(c1)} ق` : `قرن ${fa(c1)} و ${fa(c2)} ق`;
    const rName = regionInfo.get(poet.region)?.name || "";

    focus.hidden = false;
    focus.innerHTML = `
      <button type="button" class="focus-x" id="tree-clear" aria-label="بستن">×</button>
      <div class="focus-head">
        <strong>${esc(poet.label)}</strong>
        <span class="focus-badge">${cText} · ${esc(rName)}</span>
      </div>
      <div class="muted small">${esc(poet.name)}${poet.birthPlace ? ` · زاده ${esc(poet.birthPlace)}` : ""} · ${esc(yearsText(poet))} (${fa(poet.d - poet.b)} سال حیات)</div>
      <p style="margin:6px 0 4px;font-size:0.86rem;"><strong>${fa(peers.length)} شاعر هم‌عصر</strong> (روشن روی نمودار):</p>
      <div class="chips">${topPeers.map((o) => `<button class="chip" type="button" data-pick="${o.id}">${esc(o.label)} <small>(${fa(overlap(o))} سال)</small></button>`).join("")}</div>
      <div class="focus-tip">تمام نوارهای روشن پس‌زمینه، شاعرانی هستند که هم‌زمان با ${esc(poet.label)} زیسته‌اند.</div>
      <p id="tree-links" class="muted small">پیوندهای تضمین را می‌آورم…</p>
      <div class="chips">
        <a class="btn primary" href="#/poet/${poet.id}">صفحهٔ دیوان</a>
        <button class="chip" type="button" data-open-bridges="${poet.id}">پل‌های تضمین</button>
        <button class="chip" type="button" data-go="${poet.id}">تمرکز روی نوار</button>
      </div>`;
    if (jump) scrollToPoet(poet);

    const token = ++ask;
    try {
      const { data: quoted } = await api(`/quoted?poetId=${poet.id}&published=true`);
      const count = new Map();
      for (const item of Array.isArray(quoted) ? quoted : []) {
        if (!item.relatedPoetId || item.relatedPoetId === poet.id || item.rejected) continue;
        count.set(item.relatedPoetId, (count.get(item.relatedPoetId) || 0) + 1);
      }
      const links = [...count].map(([other, n]) => ({ id: other, n })).sort((a, b) => b.n - a.n);
      if (token !== ask || picked !== poet) return;
      drawLinks(links);
      const note = focus.querySelector("#tree-links");
      if (note)
        note.innerHTML = links.length
          ? `پیوند تضمین با ${fa(links.length)} شاعر: ${links.slice(0, 5).map((l) => `<button class="chip" type="button" data-pick="${l.id}">${esc(byId.get(String(l.id))?.label || "شاعر")} · ${fa(l.n)}</button>`).join("")}`
          : "در گنجور برای این شاعر پیوند تضمین ثبت نشده است.";
    } catch {
      if (token !== ask) return;
      const note = focus.querySelector("#tree-links");
      if (note) note.textContent = "پیوندهای تضمین در دسترس نبود.";
    }
  };

  const clear = () => {
    picked = null; linkedIds = new Set(); ask++;
    band.setAttribute("hidden", ""); arcs.innerHTML = "";
    lives.forEach((n) => n.classList.remove("linked"));
    focus.hidden = true;
    paintState();
  };

  chart.addEventListener("click", (e) => {
    if (travelled > 6) return;
    const node = e.target.closest(".life, #tags text");
    if (node) select(node.dataset.id);
  });
  focus.addEventListener("pointerdown", (e) => e.stopPropagation());
  focus.addEventListener("click", (e) => {
    if (e.target.closest("#tree-clear")) return clear();
    const go = e.target.closest("[data-go]");
    if (go) return scrollToPoet(byId.get(go.dataset.go));
    const chip = e.target.closest("[data-pick]");
    if (chip) return select(chip.dataset.pick, true);
    const br = e.target.closest("[data-open-bridges]");
    if (br && landingState.activateTool) landingState.activateTool("bridges", { id: br.dataset.openBridges });
  });

  box.addEventListener("input", () => {
    paintState();
    const q = box.value.trim();
    if (q.length < 2) { drop.hidden = true; return; }
    const hits = poets.filter((p) => `${p.nickname || ""} ${p.name || ""} ${p.birthPlace || ""}`.includes(q)).slice(0, 6);
    if (!hits.length) { drop.hidden = true; return; }
    drop.hidden = false;
    drop.innerHTML = hits
      .map((p) => `<div class="suggest-row" data-pick-id="${p.id}"><div><strong>${esc(p.label)}</strong><small>${esc(yearsText(p))}${p.birthPlace ? ` · ${esc(p.birthPlace)}` : ""}</small></div><span class="suggest-tag">نمایش ➜</span></div>`)
      .join("");
  });
  box.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const q = box.value.trim();
      const hit = q && poets.find((p) => `${p.nickname || ""} ${p.name || ""} ${p.birthPlace || ""}`.includes(q));
      if (hit) { drop.hidden = true; box.value = ""; select(hit.id, true); }
    }
  });
  drop.addEventListener("click", (e) => {
    const row = e.target.closest("[data-pick-id]");
    if (!row) return;
    drop.hidden = true; box.value = ""; select(row.dataset.pickId, true);
  });
  container.querySelector("#tree-regions").onclick = (e) => {
    const chip = e.target.closest("[data-region]");
    if (!chip) return;
    region = chip.dataset.region;
    container.querySelectorAll("#tree-regions .chip").forEach((n) => n.classList.toggle("on", n === chip));
    paintState();
  };

  new ResizeObserver(() => {
    if (!document.body.contains(stage)) return;
    if (fitted) fit(); else draw();
  }).observe(stage);

  fit();
  if (params.poet) setTimeout(() => select(params.poet, true), 60);
}

function renderBirthplaceMap(container, poets, params) {
  const placed = poets.filter((p) => p.birthPlaceLatitude && p.birthPlaceLongitude && p.birthYearInLHijri && p.deathYearInLHijri);
  const min = Math.min(...placed.map((p) => p.birthYearInLHijri));
  const max = Math.max(...placed.map((p) => p.deathYearInLHijri));
  let year = Math.min(max, Math.max(min, Number(params.y || 750)));

  const cities = new Map();
  for (const p of placed) {
    const pt = project(p.birthPlaceLongitude, p.birthPlaceLatitude);
    if (pt.x < 0 || pt.x > 100 || pt.y < 0 || pt.y > 100) continue;
    const c = cityOf(p);
    if (!cities.has(c)) cities.set(c, pt);
  }
  const ghosts = [...cities.values()].map((pt) => `<i class="ghost" style="left:${pt.x}%;top:${pt.y}%"></i>`).join("");
  const decades = [];
  for (let y = Math.floor(min / 10) * 10; y <= max; y += 10) decades.push({ y, n: placed.filter((p) => p.birthYearInLHijri <= y + 5 && p.deathYearInLHijri >= y + 5).length });
  const peak = Math.max(1, ...decades.map((d) => d.n));
  const spark = `<svg class="spark" viewBox="0 0 1000 40" preserveAspectRatio="none"><path d="M0,40 ${decades.map((d) => `L${(((d.y + 5 - min) / (max - min)) * 1000).toFixed(1)},${(40 - (d.n / peak) * 36).toFixed(1)}`).join(" ")} L1000,40 Z"/></svg>`;
  const ticks = [];
  for (let m = Math.ceil(min / 100) * 100; m < max; m += 100) ticks.push(m);

  container.innerHTML = `
    <div class="year-bar">
      <div class="year-top">
        <button type="button" class="play" id="map-play" aria-label="پخش">▶</button>
        <span class="muted small">سفر در زمان</span>
        <strong id="map-year-label"></strong>
      </div>
      <div class="scale">
        ${spark}
        <input id="map-year" type="range" min="${min}" max="${max}" value="${year}" aria-label="سال هجری" />
        <div class="ticks">${ticks.map((m) => `<span style="left:${((m - min) / (max - min)) * 100}%">${yr(m)}</span>`).join("")}</div>
      </div>
    </div>
    <div class="atlas realm" id="realm-atlas"><div class="ghosts">${ghosts}</div><div id="realm-pins"></div></div>
    <p class="muted small" id="map-alive-count"></p>
    <div class="grid" id="map-city-list"></div>
  `;

  const view = atlasStage(container.querySelector("#realm-atlas"));
  const pinsBox = container.querySelector("#realm-pins");
  const slider = container.querySelector("#map-year");
  const label = container.querySelector("#map-year-label");
  const countEl = container.querySelector("#map-alive-count");
  const listEl = container.querySelector("#map-city-list");
  const playBtn = container.querySelector("#map-play");

  const drawYear = (val) => {
    year = Number(val);
    const alive = placed.filter((p) => p.birthYearInLHijri <= year && p.deathYearInLHijri >= year);
    const groups = new Map();
    for (const p of alive) {
      const pt = project(p.birthPlaceLongitude, p.birthPlaceLatitude);
      if (pt.x < 0 || pt.x > 100 || pt.y < 0 || pt.y > 100) continue;
      const city = cityOf(p);
      const g = groups.get(city) || { city, x: pt.x, y: pt.y, poets: [] };
      g.poets.push(p);
      groups.set(city, g);
    }
    const most = Math.max(1, ...[...groups.values()].map((g) => g.poets.length));
    label.textContent = `سال ${yr(year)} هـ.ق · حدود ${yr(toGregorian(year))} میلادی`;
    pinsBox.innerHTML =
      [...groups.values()]
        .map((g, i) => {
          const sz = Math.round(10 + Math.sqrt(g.poets.length / most) * 16);
          return `<a class="pin" data-city="${i}" data-w="${g.poets.length}" style="left:${g.x}%;top:${g.y}%" href="javascript:void(0)"><span>${esc(g.city)}${g.poets.length > 1 ? ` <b>${fa(g.poets.length)}</b>` : ""}</span><i style="width:${sz}px;height:${sz}px"></i></a>`;
        })
        .join("") || `<p class="muted" style="padding:16px;">در این سال شاعری در این گستره ثبت نشده.</p>`;
    countEl.textContent = `${fa(alive.length)} شاعر زنده در این سال، در ${fa(groups.size)} شهر.`;
    listEl.innerHTML = [...groups.values()]
      .map((g, i) => `<article class="card" id="mcity-${i}"><strong>${esc(g.city)}</strong><div class="chips">${g.poets.map((p) => `<a class="chip" href="#/poet/${p.id}">${esc(p.nickname || p.name)}</a>`).join("")}</div></article>`)
      .join("");
    view.refresh();
  };

  playBtn.onclick = () => {
    if (activeTimer) {
      stopTimers();
      playBtn.textContent = "▶";
      return;
    }
    if (year >= max - 5) slider.value = min;
    playBtn.textContent = "❚❚";
    activeTimer = setInterval(() => {
      if (!document.body.contains(playBtn)) return stopTimers();
      const next = Math.min(max, Number(slider.value) + 5);
      slider.value = next;
      drawYear(next);
      if (next >= max) { stopTimers(); playBtn.textContent = "▶"; }
    }, 180);
  };
  slider.oninput = () => { stopTimers(); playBtn.textContent = "▶"; drawYear(slider.value); };
  pinsBox.onclick = (e) => {
    const pin = e.target.closest(".pin[data-city]");
    if (!pin) return;
    e.preventDefault();
    const c = container.querySelector(`#mcity-${pin.dataset.city}`);
    c?.scrollIntoView({ block: "nearest", behavior: "smooth" });
    c?.classList.add("flash");
    setTimeout(() => c?.classList.remove("flash"), 1200);
  };
  drawYear(year);
}

/* ==========================================================================
   ابزار ۲: پل‌های تضمین و استقبال (سوییچ درجا میان شاعران بدون تغییر صفحه!)
   ========================================================================== */
async function mountBridgesTool(container, allPoets, params, isStale) {
  const initialId = Number(params.id || 2); // پیش‌فرض: حافظ
  const featured = [
    { id: 2, name: "حافظ" },
    { id: 7, name: "سعدی" },
    { id: 5, name: "مولانا" },
    { id: 1, name: "فردوسی" },
    { id: 22, name: "صائب" },
    { id: 3, name: "نظامی" },
    { id: 9, name: "عطار" },
    { id: 24, name: "رودکی" },
  ];

  container.innerHTML = `
    <div class="tool-head">
      <div>
        <h2>پل‌های تضمین و بیت‌های مشترک</h2>
        <p class="tool-sub">چه کسی بیتی از دیگری وام گرفته است؟ روی هر حباب بزنید تا شبکهٔ همان شاعر همین‌جا باز شود.</p>
      </div>
      <div class="chips" id="bridge-poet-picks">
        ${featured.map((f) => `<button type="button" class="chip ${f.id === initialId ? "on" : ""}" data-bid="${f.id}">${f.name}</button>`).join("")}
      </div>
    </div>
    <div id="bridges-body"><div class="loader"><span class="spin"></span><span>در حال رسم شبکهٔ تضمین‌ها…</span></div></div>
  `;

  const body = container.querySelector("#bridges-body");
  const loadPoetBridges = async (id) => {
    container.querySelectorAll("#bridge-poet-picks .chip").forEach((b) => b.classList.toggle("on", Number(b.dataset.bid) === Number(id)));
    body.innerHTML = `<div class="loader"><span class="spin"></span><span>در حال دریافت پیوندهای تضمین…</span></div>`;
    const [{ data }, { data: quoted }] = await Promise.all([api(`/poet/${id}`), api(`/quoted?poetId=${id}&published=true`)]);
    if (isStale()) return;

    const poet = data.poet;
    const links = new Map();
    for (const item of Array.isArray(quoted) ? quoted : []) {
      if (!item.relatedPoetId || item.relatedPoetId === poet.id || item.rejected) continue;
      const row = links.get(item.relatedPoetId) || {
        id: item.relatedPoetId,
        name: item.cachedRelatedPoemPoetName || "شاعر",
        died: item.cachedRelatedPoemPoetDeathYearInLHijri || 0,
        n: 0, before: 0, after: 0, both: 0, samples: [],
      };
      row.n += 1;
      if (item.isPriorToRelated) row.before += 1;
      else row.after += 1;
      if (item.claimedByBothPoets) row.both += 1;
      if (row.samples.length < 2)
        row.samples.push({
          mine: item.poemId,
          theirs: item.relatedPoemId,
          line: [item.coupletVerse1, item.coupletVerse2].filter(Boolean).join(" / "),
          other: [item.relatedCoupletVerse1, item.relatedCoupletVerse2].filter(Boolean).join(" / "),
        });
      links.set(item.relatedPoetId, row);
    }
    const rows = [...links.values()].sort((a, b) => b.n - a.n);

    if (!rows.length) {
      body.innerHTML = `<div class="panel"><p class="muted">در بانک تضمین‌های گنجور، برای <strong>${esc(poet.nickname || poet.name)}</strong> پیوند تضمینی منتشر نشده است.</p><p><a class="btn primary" href="#/poet/${poet.id}">مشاهدهٔ دیوان ${esc(poet.nickname || poet.name)}</a></p></div>`;
      return;
    }

    const most = Math.max(1, ...rows.map((r) => r.n));
    const own = poet.deathYearInLHijri || 0;
    const dated = rows.filter((r) => r.died);
    const years = [...dated.map((r) => r.died), ...(own ? [own] : [])];
    const lo = Math.floor((Math.min(...years) - 20) / 50) * 50;
    const hi = Math.ceil((Math.max(...years) + 20) / 50) * 50;
    const GW = 1000, AXIS = 320, EDGE = 44;
    const span = GW - EDGE * 2 - (rows.some((r) => !r.died) ? 70 : 0);
    const gx = (y) => GW - EDGE - ((y - lo) / Math.max(1, hi - lo)) * span;
    const radius = (r) => 5 + Math.sqrt(r.n / most) * 20;
    const tone = (r) => (r.before && !r.after ? "late" : r.after && !r.before ? "early" : "both");
    const placedB = [];
    const bubbles = rows.map((row) => {
      const r = radius(row);
      const cx = row.died ? gx(row.died) : EDGE + 30;
      let cy = AXIS - r - 6;
      for (let t = 0; t < 350; t++) {
        if (!placedB.some((o) => Math.hypot(o.cx - cx, o.cy - cy) < o.r + r + 2)) break;
        cy -= 2;
      }
      const item = { ...row, r, cx, cy };
      placedB.push(item);
      return item;
    });
    const ox = own ? gx(own) : GW / 2;
    const gTicks = [];
    for (let y = lo; y <= hi; y += hi - lo > 600 ? 100 : 50) gTicks.push(y);
    const top = Math.min(...bubbles.map((b) => b.cy - b.r)) - 22;

    body.innerHTML = `
      <div class="bridge-map"><svg class="bridge-svg" viewBox="0 ${top} ${GW} ${AXIS + 145 - top}">
        <g class="b-axis">${gTicks.map((y) => `<line x1="${gx(y)}" x2="${gx(y)}" y1="${top}" y2="${AXIS}"/><text x="${gx(y)}" y="${AXIS + 132}">${yr(y)} ق</text>`).join("")}<line class="base" x1="${EDGE}" x2="${GW - EDGE}" y1="${AXIS}" y2="${AXIS}"/></g>
        <g class="b-arcs">${bubbles.map((b) => {
          const lift = Math.min(110, 14 + Math.abs(b.cx - ox) * 0.3);
          return `<path class="${tone(b)}" d="M${ox.toFixed(1)},${AXIS} Q${((ox + b.cx) / 2).toFixed(1)},${(AXIS + lift * 2).toFixed(1)} ${b.cx.toFixed(1)},${AXIS}" style="stroke-width:${(0.9 + (b.n / most) * 4.5).toFixed(1)}"/>`;
        }).join("")}</g>
        <g class="b-dots">${bubbles.map((b, i) => `<g data-bid="${b.id}" style="cursor:pointer;"><circle class="${tone(b)}" cx="${b.cx.toFixed(1)}" cy="${b.cy.toFixed(1)}" r="${b.r.toFixed(1)}"><title>${esc(b.name)} · ${fa(b.n)} پیوند</title></circle>${i < 12 ? `<text x="${(b.cx - b.r - 3).toFixed(1)}" y="${(b.cy + 4).toFixed(1)}">${esc(b.name)} ${fa(b.n)}</text>` : ""}</g>`).join("")}</g>
        <g class="b-self"><line x1="${ox}" x2="${ox}" y1="${AXIS - 8}" y2="${AXIS + 8}"/><circle cx="${ox}" cy="${AXIS}" r="7"/><text x="${ox}" y="${AXIS - 14}">${esc(poet.nickname || poet.name)}</text></g>
      </svg></div>
      <p class="key muted"><span class="sw late"></span> شعر ${esc(poet.nickname || poet.name)} مقدم است <span class="sw early"></span> شاعر مقابل مقدم است <span class="sw both"></span> دوسویه · مجموعاً ${fa(quoted.length)} پیوند با ${fa(rows.length)} شاعر</p>
      <div class="grid">${rows.slice(0, 18).map((row) => `
        <article class="card">
          <div class="kicker">${fa(row.n)} پیوند · ${row.before && !row.after ? `${esc(poet.nickname || poet.name)} پیش‌تر` : row.after && !row.before ? `${esc(row.name)} پیش‌تر` : "دوسویه"}</div>
          <strong><a href="javascript:void(0)" data-bid="${row.id}">${esc(row.name)}</a></strong>
          ${row.samples.map((s) => `<p><a href="#/poem/${s.mine}">${esc(s.line)}</a></p>`).join("")}
        </article>`).join("")}</div>
    `;
    const mapEl = body.querySelector(".bridge-map");
    if (mapEl) {
      atlasStage(mapEl);
      mapEl.parentElement.classList.add("bridge-stage");
    }
    body.querySelectorAll("[data-bid]").forEach((el) => {
      el.onclick = (e) => { e.preventDefault(); loadPoetBridges(el.dataset.bid); };
    });
  };

  container.querySelector("#bridge-poet-picks").onclick = (e) => {
    const btn = e.target.closest("[data-bid]");
    if (btn) loadPoetBridges(btn.dataset.bid);
  };
  await loadPoetBridges(initialId);
}

/* ==========================================================================
   ابزار ۳: مردمان شعر و تبارنامهٔ شاهنامه (دوسیه و درخت خاندان درجا!)
   ========================================================================== */
function netKind(edge) {
  if (edge.category === "Relation") return "kin";
  if (edge.typeValue === 5 || edge.typeValue === 14) return "war";
  if ([0, 1, 2, 3, 6, 11, 12].includes(edge.typeValue)) return "court";
  return "ally";
}

function buildPeopleNetwork(graph, limit = 85) {
  const degree = new Map(), names = new Map();
  for (const e of graph.edges || []) {
    degree.set(e.person1Id, (degree.get(e.person1Id) || 0) + 1);
    degree.set(e.person2Id, (degree.get(e.person2Id) || 0) + 1);
    names.set(e.person1Id, e.person1Name);
    names.set(e.person2Id, e.person2Name);
  }
  const ids = [...degree.keys()].sort((a, b) => degree.get(b) - degree.get(a)).slice(0, limit);
  const keep = new Set(ids);
  const edges = (graph.edges || []).filter((e) => keep.has(e.person1Id) && keep.has(e.person2Id)).map((e) => ({ a: e.person1Id, b: e.person2Id, kind: netKind(e) }));
  const W = 1000, H = 640;
  const nodes = ids.map((id, i) => {
    const t = i * 2.39996, r = 18 * Math.sqrt(i + 1);
    return { id, name: names.get(id) || "", deg: degree.get(id), x: W / 2 + r * Math.cos(t), y: H / 2 + r * Math.sin(t), vx: 0, vy: 0 };
  });
  const at = new Map(nodes.map((n) => [n.id, n]));
  const links = edges.map((e) => [at.get(e.a), at.get(e.b)]);
  for (let step = 0; step < 360; step++) {
    const cool = 1 - step / 360;
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const p = nodes[i], q = nodes[j];
        let dx = p.x - q.x, dy = p.y - q.y;
        const d2 = dx * dx + dy * dy + 0.01, f = 2400 / d2, d = Math.sqrt(d2);
        dx /= d; dy /= d;
        p.vx += dx * f; p.vy += dy * f; q.vx -= dx * f; q.vy -= dy * f;
      }
    }
    for (const [p, q] of links) {
      const dx = q.x - p.x, dy = q.y - p.y, d = Math.sqrt(dx * dx + dy * dy) || 1, f = (d - 68) * 0.02;
      p.vx += (dx / d) * f; p.vy += (dy / d) * f; q.vx -= (dx / d) * f; q.vy -= (dy / d) * f;
    }
    for (const n of nodes) {
      n.vx += (W / 2 - n.x) * 0.004; n.vy += (H / 2 - n.y) * 0.006;
      n.x += Math.max(-12, Math.min(12, n.vx)) * cool; n.y += Math.max(-12, Math.min(12, n.vy)) * cool;
      n.vx *= 0.5; n.vy *= 0.5;
    }
  }
  const xs = nodes.map((n) => n.x), ys = nodes.map((n) => n.y);
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const s = Math.min((W - 120) / (x1 - x0 || 1), (H - 60) / (y1 - y0 || 1));
  for (const n of nodes) { n.x = 60 + (n.x - x0) * s; n.y = 30 + (n.y - y0) * s; }
  const most = Math.max(1, ...nodes.map((n) => n.deg));
  const color = new Map(NET_KINDS.map((k) => [k.key, k.color]));
  return `<svg class="net-svg" viewBox="0 0 ${W} ${H}">
    <g class="net-edges">${edges.map((e) => {
      const p = at.get(e.a), q = at.get(e.b);
      return `<line class="k-${e.kind}" data-a="${e.a}" data-b="${e.b}" x1="${p.x.toFixed(1)}" y1="${p.y.toFixed(1)}" x2="${q.x.toFixed(1)}" y2="${q.y.toFixed(1)}" stroke="${color.get(e.kind)}"/>`;
    }).join("")}</g>
    <g class="net-nodes">${nodes.map((n) => {
      const r = (4 + Math.sqrt(n.deg / most) * 10).toFixed(1);
      return `<g class="pin" data-person="${n.id}" data-id="${n.id}" data-w="${n.deg}"><title>${esc(n.name)} · ${fa(n.deg)} پیوند</title><circle cx="${n.x.toFixed(1)}" cy="${n.y.toFixed(1)}" r="${r}"/><text x="${n.x.toFixed(1)}" y="${(n.y + Number(r) + 3).toFixed(1)}">${esc(n.name)}</text></g>`;
    }).join("")}</g></svg>`;
}

function buildMiniFamilySvg(tree, focusId) {
  const persons = new Map((tree.persons || []).map((p) => [p.id, p]));
  const kids = new Map(), parents = new Map();
  for (const e of tree.relations || []) {
    if (e.relationType === 0) {
      if (!kids.has(e.person1Id)) kids.set(e.person1Id, []);
      if (!kids.get(e.person1Id).includes(e.person2Id)) kids.get(e.person1Id).push(e.person2Id);
      if (!parents.has(e.person2Id)) parents.set(e.person2Id, e.person1Id);
    }
  }
  const roots = [...[...persons.keys()].filter((id) => !parents.has(id) && kids.has(id)), tree.rootId].filter(Boolean);
  const seen = new Set(), nodes = [], edges = [];
  let slot = 0, depthMax = 0;
  const place = (id, depth) => {
    if (seen.has(id) || !persons.has(id) || depth > 16) return null;
    seen.add(id);
    const node = { id, depth, person: persons.get(id) };
    depthMax = Math.max(depthMax, depth);
    const ch = (kids.get(id) || []).filter((c) => parents.get(c) === id).map((c) => place(c, depth + 1)).filter(Boolean);
    if (ch.length) {
      node.slot = (ch[0].slot + ch[ch.length - 1].slot) / 2;
      for (const c of ch) edges.push([node, c]);
    } else node.slot = slot++;
    nodes.push(node);
    return node;
  };
  for (const r of roots) if (place(r, 0)) slot += 0.5;
  if (!nodes.length) return "";
  const GEN = 140, ROW = 30, W = (depthMax + 1) * GEN + 60, H = Math.max(1, slot) * ROW + 40;
  const nx = (n) => W - 70 - n.depth * GEN;
  const ny = (n) => 24 + n.slot * ROW;
  return `<div class="fmap"><svg viewBox="0 0 ${W} ${H}" style="min-width:${Math.min(W, 560)}px">
    ${edges.map(([a, b]) => `<line x1="${nx(a) - 42}" y1="${ny(a)}" x2="${nx(b) + 42}" y2="${ny(b)}"/>`).join("")}
    ${nodes.map((n) => `<g class="${n.id === focusId ? "me" : ""}" data-person="${n.id}" style="cursor:pointer;"><rect x="${nx(n) - 48}" y="${ny(n) - 12}" width="96" height="24"/><text x="${nx(n)}" y="${ny(n)}">${esc(n.person.name.slice(0, 14))}</text></g>`).join("")}
  </svg></div>`;
}

async function mountPeopleTool(container, params, isStale) {
  const [people, roots, graph] = await Promise.all([rootApi("/people"), rootApi("/people/familytrees"), rootApi("/people/graph")]);
  if (isStale()) return;

  const byId = new Map(people.map((p) => [p.id, p]));
  const degree = new Map();
  for (const e of graph.edges || []) {
    degree.set(e.person1Id, (degree.get(e.person1Id) || 0) + 1);
    degree.set(e.person2Id, (degree.get(e.person2Id) || 0) + 1);
  }
  const sorted = [...people].sort((a, b) => (degree.get(b.id) || 0) - (degree.get(a.id) || 0));

  container.innerHTML = `
    <div class="tool-head">
      <div>
        <h2>مردمان شعر و تبارنامهٔ شاهنامه</h2>
        <p class="tool-sub">${fa(people.length)} شخصیت برچسب‌خورده روی بیت‌های گنجور؛ روی هر نام بزنید تا شجره‌نامه و بیت‌های گواهش همین‌جا باز شود.</p>
      </div>
    </div>
    <div id="person-dossier" hidden></div>
    ${roots.length ? `<div class="chips"><span class="muted small">خاندان‌ها:</span>${roots.map((p) => `<button type="button" class="chip" data-person="${p.id}">${esc(p.familyTreeCaption || p.name)}</button>`).join("")}</div>` : ""}
    <div class="chips net-kinds" id="net-kinds">${NET_KINDS.map((k) => `<button type="button" class="chip on" data-kind="${k.key}" style="--c:${k.color}"><i class="dot"></i>${k.name}</button>`).join("")}</div>
    <div class="net-map">${buildPeopleNetwork(graph)}</div>
    <div class="inline-search" style="margin-top:14px;"><input id="people-q" placeholder="جستجوی شخصیت (مثلاً رستم، سهراب، کیخسرو…)" autocomplete="off" /></div>
    <div class="grid" id="people-grid"></div>
  `;

  const netMap = container.querySelector(".net-map");
  const netSvg = netMap.querySelector("svg");
  const netView = atlasStage(netMap);
  netMap.parentElement.classList.add("net-stage");
  const dossier = container.querySelector("#person-dossier");

  const openPerson = async (id) => {
    const pid = Number(id);
    const person = byId.get(pid);
    if (!person) return;
    dossier.hidden = false;
    dossier.innerHTML = `<div class="inline-dossier"><div class="loader"><span class="spin"></span><span>در حال دریافت تبارنامه و بیت‌های ${esc(person.name)}…</span></div></div>`;
    dossier.scrollIntoView({ behavior: "smooth", block: "nearest" });
    const [tree, rels, poems] = await Promise.all([
      rootApi(`/people/${pid}/familytree`).catch(() => null),
      rootApi(`/people/${pid}/relations?evidenceLimit=1`).catch(() => []),
      rootApi(`/people/${pid}/poems`).catch(() => []),
    ]);
    if (isStale()) return;
    const relList = Array.isArray(rels) ? rels : [];
    const poemList = Array.isArray(poems) ? poems : [];
    dossier.innerHTML = `
      <div class="inline-dossier">
        <div class="inline-dossier-head">
          <div>
            <h3>${esc(person.name)}</h3>
            <p class="muted small" style="margin:2px 0 0;">${esc(person.description || "")}</p>
          </div>
          <button type="button" class="chip" id="close-person-dossier">بستن ×</button>
        </div>
        ${tree?.persons?.length ? `<p class="kicker">شجره‌نامهٔ خاندان</p>${buildMiniFamilySvg(tree, pid)}` : ""}
        ${relList.length ? `<p class="kicker" style="margin-top:10px;">پیوندها (${fa(relList.length)})</p><div class="chips">${relList.slice(0, 14).map((r) => {
          const otherId = r.person1Id === pid ? r.person2Id : r.person1Id;
          const otherName = r.person1Id === pid ? r.person2Name : r.person1Name;
          return `<button type="button" class="chip" data-person="${otherId}">${esc(otherName || "؟")}${r.relationCaption ? ` · ${esc(r.relationCaption)}` : ""}</button>`;
        }).join("")}</div>` : ""}
        ${poemList.length ? `<p class="kicker" style="margin-top:10px;">شعرهای مرتبط</p><div class="chips">${poemList.slice(0, 10).map((pm) => `<a class="chip" href="#/poem/${pm.poemId || pm.id}">${esc(pm.title || pm.poemFullTitle || "خواندن شعر")}</a>`).join("")}</div>` : ""}
      </div>`;
    dossier.querySelector("#close-person-dossier").onclick = () => (dossier.hidden = true);
    dossier.querySelectorAll("[data-person]").forEach((el) => { el.onclick = () => openPerson(el.dataset.person); });
  };

  container.querySelector("#net-kinds").onclick = (e) => {
    const chip = e.target.closest("[data-kind]");
    if (!chip) return;
    chip.classList.toggle("on");
    netSvg.classList.toggle(`hide-${chip.dataset.kind}`, !chip.classList.contains("on"));
  };
  const lines = [...netSvg.querySelectorAll(".net-edges line")];
  netSvg.addEventListener("pointerover", (e) => {
    const pin = e.target.closest(".pin");
    if (!pin) return;
    const id = pin.dataset.id;
    const near = new Set([id]);
    for (const l of lines) {
      const hot = l.dataset.a === id || l.dataset.b === id;
      l.classList.toggle("hot", hot);
      if (hot) near.add(l.dataset.a).add(l.dataset.b);
    }
    netSvg.classList.add("focus");
    netSvg.querySelectorAll(".pin").forEach((n) => n.classList.toggle("near", near.has(n.dataset.id)));
  });
  netSvg.addEventListener("pointerleave", () => netSvg.classList.remove("focus"));
  container.addEventListener("click", (e) => {
    const pBtn = e.target.closest("[data-person]");
    if (pBtn) { e.preventDefault(); openPerson(pBtn.dataset.person); }
  });

  const qInput = container.querySelector("#people-q");
  const grid = container.querySelector("#people-grid");
  const drawGrid = () => {
    const q = qInput.value.trim();
    const shown = sorted.filter((p) => !q || `${p.name} ${p.description || ""}`.includes(q)).slice(0, 24);
    grid.innerHTML = shown.map((p) => `<article class="card" data-person="${p.id}" style="cursor:pointer;"><strong>${esc(p.name)}</strong>${degree.get(p.id) ? `<div class="kicker">${fa(degree.get(p.id))} پیوند</div>` : ""}<p>${esc((p.description || "").slice(0, 90))}</p></article>`).join("") || `<p class="muted">شخصیتی پیدا نشد.</p>`;
  };
  qInput.oninput = drawGrid;
  drawGrid();
  netView.refresh();
  if (params.person) openPerson(params.person);
}

/* ==========================================================================
   ابزار ۴: آرایه‌های ادبی (نوار تناسبی + جزئیات و جفت‌مفاهیم درجا!)
   ========================================================================== */
async function mountDevicesTool(container, params, isStale) {
  const [list, overview] = await Promise.all([devices(), rootApi("/ganjoor/literary/stats/overview")]);
  if (isStale()) return;

  const stats = new Map((overview.devices || []).map((i) => [i.deviceId, i]));
  const shown = list.filter((i) => stats.get(i.id)?.tagCount || i.isCore);
  const groups = [...new Set(shown.map((i) => i.category))];
  const countOf = (i) => stats.get(i.id)?.tagCount || 0;
  const total = shown.reduce((s, i) => s + countOf(i), 0) || 1;
  const most = Math.max(1, ...shown.map(countOf));
  const COLORS = ["#0a6b60", "#1e3a8a", "#b2532f", "#b8892a"];
  const gColor = new Map(groups.map((g, idx) => [g, COLORS[idx % COLORS.length]]));

  const strip = groups
    .map((g) =>
      shown
        .filter((i) => i.category === g)
        .sort((a, b) => countOf(b) - countOf(a))
        .map((i) => {
          const w = (countOf(i) / total) * 100;
          return w > 0 ? `<button type="button" class="fam-seg" data-dev="${i.id}" style="flex:${w.toFixed(3)};--c:${gColor.get(g)}" title="${esc(i.name)} · ${fa(countOf(i))} نمونه">${w > 7 ? `<span>${esc(i.name)}</span><small>${fa(Math.round(w))}٪</small>` : ""}</button>` : "";
        })
        .join(""),
    )
    .join("");

  container.innerHTML = `
    <div class="tool-head">
      <div>
        <h2>آرایه‌های ادبی و شبکه‌های تصویری</h2>
        <p class="tool-sub">${fa(overview.totalTags || 0)} آرایه برچسب‌خورده روی ${fa(overview.totalPoems || 0)} شعر؛ روی هر آرایه بزنید تا جفت‌های پرتکرار و بیت‌های نمونه همین‌جا باز شوند.</p>
      </div>
    </div>
    <div class="fam-strip">${strip}</div>
    <div id="device-dossier" hidden></div>
    <div class="grid">${shown
      .filter((i) => countOf(i) >= 10)
      .sort((a, b) => countOf(b) - countOf(a))
      .map((i) => `<article class="card" data-dev="${i.id}" style="cursor:pointer;--c:${gColor.get(i.category)}"><strong>${esc(i.name)}</strong><div class="dev-bar"><i style="width:${((countOf(i) / most) * 100).toFixed(1)}%"></i></div><div class="kicker">${fa(countOf(i))} نمونه در ${fa(stats.get(i.id)?.poemCount || 0)} شعر</div><p>${esc((i.definition || "").slice(0, 110))}</p></article>`)
      .join("")}</div>
  `;

  const dossier = container.querySelector("#device-dossier");
  const openDevice = async (id, concept = 0) => {
    const dev = list.find((i) => i.id === Number(id));
    if (!dev) return;
    dossier.hidden = false;
    dossier.innerHTML = `<div class="inline-dossier"><div class="loader"><span class="spin"></span><span>در حال دریافت نمونه‌های ${esc(dev.name)}…</span></div></div>`;
    dossier.scrollIntoView({ behavior: "smooth", block: "nearest" });
    const [top, page] = await Promise.all([
      rootApi(`/ganjoor/literary/stats/device/${id}/top-concepts?take=24`).catch(() => []),
      rootApi(`/ganjoor/literary/stats/tags?deviceId=${id}${concept ? `&conceptId=${concept}` : ""}&skip=0&take=9`),
    ]);
    if (isStale()) return;
    const items = page.items || [];
    dossier.innerHTML = `
      <div class="inline-dossier">
        <div class="inline-dossier-head">
          <div>
            <h3>${esc(dev.name)}</h3>
            <p class="muted small" style="margin:2px 0 0;">${esc(dev.definition || "")}</p>
          </div>
          <button type="button" class="chip" id="close-dev-dossier">بستن ×</button>
        </div>
        ${top.length ? `<div class="chips"><button type="button" class="chip ${concept ? "" : "on"}" data-dev-c="0">همه مفاهیم</button>${top.slice(0, 14).map((c) => `<button type="button" class="chip ${c.conceptId === concept ? "on" : ""}" data-dev-c="${c.conceptId}">${esc(c.name)} · ${fa(c.usageCount)}</button>`).join("")}</div>` : ""}
        <div class="grid">${items.map((item) => {
          const spans = (m) => (item.parts || []).filter((p) => p.misra === m && p.wordStart).map((p) => ({ from: p.wordStart, to: p.wordEnd || p.wordStart, label: p.slotName }));
          return `<article class="card"><div class="kicker">${esc(item.poemFullTitle || "")}</div><p class="couplet">${marked(item.hemistich1, spans(1))}<br>${marked(item.hemistich2, spans(2))}</p><a class="chip" href="#/poem/${item.poemId}" style="margin-top:6px;">خواندن شعر ←</a></article>`;
        }).join("")}</div>
      </div>`;
    dossier.querySelector("#close-dev-dossier").onclick = () => (dossier.hidden = true);
    dossier.querySelectorAll("[data-dev-c]").forEach((b) => {
      b.onclick = () => openDevice(id, Number(b.dataset.devC));
    });
  };

  container.addEventListener("click", (e) => {
    const d = e.target.closest("[data-dev]");
    if (d) openDevice(d.dataset.dev, 0);
  });
  if (params.device) openDevice(params.device, Number(params.c || 0));
}

/* ==========================================================================
   ابزار ۵: واژه‌سنج تحلیلی و جستجوی یکپارچه
   ========================================================================== */
async function mountWordsTool(container, allPoets, params, isStale) {
  const initialQ = (params.q || "عشق").trim();
  const samples = ["عشق", "می", "سرو", "دل", "آینه", "خورشید", "رند"];

  container.innerHTML = `
    <div class="tool-head">
      <div>
        <h2>واژه‌سنج و جستجوی پیکره</h2>
        <p class="tool-sub">بسامد هر واژه را در کل گنجینهٔ شعر فارسی مقایسه کنید و شعرهایش را بخوانید.</p>
      </div>
      <div class="chips" id="word-samples">${samples.map((w) => `<button type="button" class="chip ${w === initialQ ? "on" : ""}" data-word="${w}">${w}</button>`).join("")}</div>
    </div>
    <form class="inline-search" id="word-search-form">
      <input id="word-q" value="${esc(initialQ)}" placeholder="واژه، تکه‌ای از بیت یا نام شاعر…" autocomplete="off" />
      <button type="submit" class="btn primary">سنجش و جستجو</button>
    </form>
    <div id="word-results"></div>
  `;

  const resBox = container.querySelector("#word-results");
  const wInput = container.querySelector("#word-q");

  const runSearch = async (q, poetId = 0) => {
    q = q.trim();
    if (!q) return;
    wInput.value = q;
    container.querySelectorAll("#word-samples .chip").forEach((b) => b.classList.toggle("on", b.dataset.word === q));
    resBox.innerHTML = `<div class="loader"><span class="spin"></span><span>در حال سنجش بسامد «${esc(q)}»…</span></div>`;

    const matchedPoet = !poetId && q.length >= 2
      ? allPoets.find((p) => {
          const n = (p.name || "").trim(), nk = (p.nickname || "").trim();
          return n === q || nk === q || n.includes(q) || (nk && nk.includes(q));
        })
      : null;

    const [{ data: poems, total }, meterHtml] = await Promise.all([
      api(`/poems/search?term=${encodeURIComponent(q)}&pageNumber=1&pageSize=9${poetId ? `&poetId=${poetId}` : ""}`).catch(() => ({ data: [], total: 0 })),
      !poetId && !/\s/.test(q) ? buildWordMeter(q).catch(() => "") : Promise.resolve(""),
    ]);
    if (isStale()) return;

    const banner = matchedPoet
      ? `<div class="poet-match-banner">
           <div class="pmb-avatar">${esc((matchedPoet.nickname || matchedPoet.name).slice(0, 1))}</div>
           <div class="pmb-body">
             <span class="kicker">شاعر شناسایی‌شده</span>
             <h3>${esc(matchedPoet.nickname || matchedPoet.name)}</h3>
             <p>${matchedPoet.birthYearInLHijri ? `${yr(matchedPoet.birthYearInLHijri)} تا ${yr(matchedPoet.deathYearInLHijri)} ق` : ""}${matchedPoet.birthPlace ? ` · زاده ${esc(matchedPoet.birthPlace)}` : ""}</p>
           </div>
           <div class="chips">
             <button type="button" class="btn primary" data-jump-tree="${matchedPoet.id}">نمایش روی خط زمان</button>
             <a class="chip" href="#/poet/${matchedPoet.id}">صفحهٔ دیوان</a>
           </div>
         </div>`
      : "";

    const rows = (Array.isArray(poems) ? poems : [])
      .map((poem) => {
        const first = String(poem.plainText || "").split(/\r?\n/).map((l) => l.trim()).filter(Boolean).slice(0, 2).join(" / ");
        const p = poem.category?.poet;
        return `<a class="hit" href="#/poem/${poem.id}"><div class="kicker">${esc(p?.nickname || p?.name || "")}</div><strong>${esc(poem.fullTitle || poem.title)}</strong><p>${esc(first)}</p></a>`;
      })
      .join("");

    resBox.innerHTML = `
      ${banner}
      ${meterHtml}
      <p class="kicker" style="margin-top:14px;">نمونه شعرها (${fa(total)} شعر در گنجور)</p>
      ${rows ? `<div class="grid">${rows}</div>` : `<p class="muted">شعری با این عبارت پیدا نشد.</p>`}
    `;

    resBox.querySelectorAll("[data-jump-tree]").forEach((b) => {
      b.onclick = () => landingState.activateTool?.("tree", { poet: b.dataset.jumpTree, view: "timeline" });
    });
    resBox.querySelectorAll("[data-filter-poet]").forEach((b) => {
      b.onclick = (e) => { e.preventDefault(); runSearch(q, Number(b.dataset.filterPoet)); };
    });
  };

  container.querySelector("#word-search-form").onsubmit = (e) => { e.preventDefault(); runSearch(wInput.value); };
  container.querySelector("#word-samples").onclick = (e) => {
    const b = e.target.closest("[data-word]");
    if (b) runSearch(b.dataset.word);
  };
  await runSearch(initialQ);
}

async function buildWordMeter(q) {
  const [{ data }, totalRow] = await Promise.all([
    api(`/wordcounts/bycat?term=${encodeURIComponent(q)}&PageNumber=1&PageSize=40`),
    api(`/wordcounts/bycat/count?term=${encodeURIComponent(q)}`).catch(() => ({ data: null })),
  ]);
  const rows = (Array.isArray(data) ? data : []).filter((r) => r.count > 0);
  if (!rows.length) return "";
  const most = Math.max(1, ...rows.map((r) => r.count));
  const rate = (r) => (r.totalWordCount ? (r.count / r.totalWordCount) * 10000 : 0);
  const byRate = [...rows].filter((r) => r.totalWordCount > 2000).sort((a, b) => rate(b) - rate(a)).slice(0, 8);
  const topRate = Math.max(0.0001, ...byRate.map(rate));
  const total = totalRow?.data?.count;
  const bar = (r, w, val, cls = "") =>
    `<a class="barrow ${cls}" href="javascript:void(0)" data-filter-poet="${r.poetId}"><span>${esc(r.name)}</span><i style="width:${w.toFixed(1)}%"></i><b>${val}</b></a>`;
  return `
    <p class="kicker">«${esc(q)}» نزد شاعران${total ? ` · ${fa(total)} بار در کل گنجور` : ""}</p>
    <div class="meter-cols">
      <div><p class="muted small" style="margin:0 0 6px;">بیشترین شمار</p><div class="bars">${rows.slice(0, 8).map((r) => bar(r, (r.count / most) * 100, fa(r.count))).join("")}</div></div>
      <div><p class="muted small" style="margin:0 0 6px;">بیشترین نسبت (در هر ۱۰٬۰۰۰ واژه)</p><div class="bars">${byRate.map((r) => bar(r, (rate(r) / topRate) * 100, rate(r).toLocaleString("fa-IR", { maximumFractionDigits: 1 }), "lapis")).join("")}</div></div>
    </div>`;
}

/* ==========================================================================
   ابزار ۶: جای‌ها در شعر و سفرنامهٔ ناصرخسرو (سوییچ درجا!)
   ========================================================================== */
async function mountPlacesTool(container, params, isStale) {
  const [geo, locations, manifest, base] = await Promise.all([
    fileJson("geotags.json"),
    fileJson("locations.json"),
    fileJson("manifest.json"),
    fetch("mideast.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
  ]);
  if (isStale()) return;

  const buckets = [...new Set(geo.map((i) => Math.floor(i.PoemId / 2000)))];
  const index = {};
  const shards = await Promise.all(buckets.map((b) => fileJson(`index/poems-by-id/${b}.json`).catch(() => ({}))));
  if (isStale()) return;
  for (const s of shards) Object.assign(index, s);

  const poetBySlug = new Map((manifest.Poets || []).map((p) => [p.FullUrl, p]));
  const byId = new Map(locations.map((l) => [l.Id, l]));
  const tags = geo
    .map((tag, order) => {
      const place = byId.get(tag.LocationId);
      if (!place) return null;
      const url = index[String(tag.PoemId)] || "";
      const slug = `/${url.split("/")[1] || ""}`;
      return { order, poemId: tag.PoemId, couplet: tag.CoupletIndex || 0, year: tag.LunarYear || 0, place, url, slug, poet: poetBySlug.get(slug)?.Nickname || "" };
    })
    .filter(Boolean);

  const journey = [];
  for (const tag of tags.filter((i) => i.url.startsWith("/naserkhosro/safarname") && i.year).sort((a, b) => a.year - b.year || a.poemId - b.poemId || a.order - b.order)) {
    if (journey.length && journey[journey.length - 1].place.Id === tag.place.Id) continue;
    journey.push(tag);
  }

  let mode = params.all === "1" || !journey.length || !base ? "all" : "journey";
  container.innerHTML = `
    <div class="tool-head">
      <div>
        <h2>جای‌ها در شعر و سفر هفت‌سالهٔ ناصرخسرو</h2>
        <p class="tool-sub">جاهایی که خود شعر و سفرنامه از آن‌ها نام برده است (${fa(tags.length)} برچسب مکانی).</p>
      </div>
      <div class="seg-switch">
        <button type="button" class="seg-btn ${mode === "journey" ? "active" : ""}" data-pmode="journey">سفر ناصرخسرو</button>
        <button type="button" class="seg-btn ${mode === "all" ? "active" : ""}" data-pmode="all">همهٔ شهرها</button>
      </div>
    </div>
    <div id="places-body"></div>
  `;

  const body = container.querySelector("#places-body");
  const renderMode = (m) => {
    stopTimers();
    mode = m;
    container.querySelectorAll("[data-pmode]").forEach((b) => b.classList.toggle("active", b.dataset.pmode === m));
    if (m === "journey" && base && journey.length) {
      const [LON0, , , LAT1] = base.bbox;
      const P = (lon, lat) => [(lon - LON0) * base.k * base.c, (LAT1 - lat) * base.k];
      const pts = journey.map((s) => P(s.place.Longitude, s.place.Latitude));
      const first = journey[0], last = journey[journey.length - 1];
      const cities = new Set(journey.map((s) => s.place.Id)).size;
      body.innerHTML = `
        <div class="journey">
          <div class="journey-map" id="jmap"><svg viewBox="0 0 ${base.w} ${base.h}">
            <rect width="${base.w}" height="${base.h}" class="sea"/>
            <path class="land" d="${base.land}"/>
            <path class="river" d="${base.rivers}"/>
            <polyline class="route-all" points="${pts.map((p) => p.map((v) => v.toFixed(0)).join(",")).join(" ")}"/>
            <polyline class="route-done" id="jdone" points=""/>
            <g id="jstops">${journey.map((s, i) => `<circle class="stop" data-i="${i}" cx="${pts[i][0].toFixed(0)}" cy="${pts[i][1].toFixed(0)}" r="4"><title>${esc(s.place.Name)} · ${yr(s.year)} ق</title></circle>`).join("")}</g>
            <g id="jnames"></g>
          </svg></div>
          <div class="journey-side">
            <p class="jstat"><b>${fa(cities)}</b> شهر · سال <b>${yr(first.year)}</b> تا <b>${yr(last.year)}</b> ق</p>
            <div class="jcard" id="jcard"></div>
            <div class="jctl">
              <button type="button" class="btn" id="jprev">→</button>
              <button type="button" class="btn primary" id="jplay">▶ پخش سفر</button>
              <button type="button" class="btn" id="jnext">←</button>
            </div>
            <input type="range" id="jrange" min="0" max="${journey.length - 1}" value="0" />
          </div>
        </div>
        <ol class="stops-list" id="jlist">${journey.map((s, i) => `<li><button type="button" data-i="${i}">${fa(i + 1)}. ${esc(s.place.Name)}</button></li>`).join("")}</ol>
      `;
      const done = body.querySelector("#jdone"), names = body.querySelector("#jnames"), card = body.querySelector("#jcard");
      const range = body.querySelector("#jrange"), play = body.querySelector("#jplay");
      const circles = [...body.querySelectorAll("#jstops .stop")], listBtns = [...body.querySelectorAll("#jlist button")];
      let at = 0;
      const show = (i) => {
        at = Math.max(0, Math.min(journey.length - 1, i));
        range.value = at;
        done.setAttribute("points", pts.slice(0, at + 1).map((p) => p.map((v) => v.toFixed(0)).join(",")).join(" "));
        circles.forEach((c, k) => { c.classList.toggle("past", k < at); c.classList.toggle("now", k === at); c.setAttribute("r", k === at ? 8 : 4); });
        const [lx, ly] = pts[at];
        names.innerHTML = `<text class="now" x="${(lx + 8).toFixed(0)}" y="${(ly + 4).toFixed(0)}">${esc(journey[at].place.Name)}</text>`;
        const st = journey[at];
        card.innerHTML = `<div class="kicker">منزل ${fa(at + 1)} از ${fa(journey.length)}</div><strong>${esc(st.place.Name)}</strong><p class="muted small">سال ${yr(st.year)} ق · حدود ${yr(toGregorian(st.year))} م</p><a class="chip" href="#/poem/${st.poemId}" style="margin-top:6px;">خواندن این بخش از سفرنامه ←</a>`;
        listBtns.forEach((b, k) => b.classList.toggle("on", k === at));
      };
      play.onclick = () => {
        if (activeTimer) { stopTimers(); play.textContent = "▶ پخش سفر"; return; }
        if (at >= journey.length - 1) show(0);
        play.textContent = "❚❚ ایست";
        activeTimer = setInterval(() => {
          if (!document.body.contains(play) || at >= journey.length - 1) { stopTimers(); play.textContent = "▶ پخش سفر"; return; }
          show(at + 1);
        }, 650);
      };
      body.querySelector("#jprev").onclick = () => { stopTimers(); play.textContent = "▶ پخش سفر"; show(at - 1); };
      body.querySelector("#jnext").onclick = () => { stopTimers(); play.textContent = "▶ پخش سفر"; show(at + 1); };
      range.oninput = () => { stopTimers(); play.textContent = "▶ پخش سفر"; show(Number(range.value)); };
      body.querySelector("#jlist").onclick = (e) => { const b = e.target.closest("[data-i]"); if (b) { stopTimers(); show(Number(b.dataset.i)); } };
      body.querySelector("#jstops").onclick = (e) => { const c = e.target.closest("[data-i]"); if (c) { stopTimers(); show(Number(c.dataset.i)); } };
      show(0);
      atlasStage(body.querySelector("#jmap"));
    } else {
      const others = tags.filter((i) => !i.url.startsWith("/naserkhosro/safarname"));
      const groups = new Map();
      for (const t of others.length ? others : tags) {
        const g = groups.get(t.place.Id) || { place: t.place, tags: [] };
        if (!g.tags.some((x) => x.poemId === t.poemId)) g.tags.push(t);
        groups.set(t.place.Id, g);
      }
      const inside = [...groups.values()]
        .map((g) => ({ ...g, pt: project(g.place.Longitude, g.place.Latitude) }))
        .filter((g) => g.pt.x >= 0 && g.pt.x <= 100 && g.pt.y >= 0 && g.pt.y <= 100)
        .sort((a, b) => b.tags.length - a.tags.length);
      const most = Math.max(1, ...inside.map((g) => g.tags.length));
      body.innerHTML = `
        <div class="atlas realm" id="places-all-atlas">${inside.map((g) => {
          const sz = Math.round(8 + Math.sqrt(g.tags.length / most) * 18);
          return `<a class="pin" data-place="${g.place.Id}" data-w="${g.tags.length}" style="left:${g.pt.x}%;top:${g.pt.y}%" href="javascript:void(0)"><span>${esc(g.place.Name)}</span><i style="width:${sz}px;height:${sz}px"></i></a>`;
        }).join("")}</div>
        <div class="grid">${inside.slice(0, 18).map((g) => `<article class="card" id="pcard-${g.place.Id}"><strong>${esc(g.place.Name)}</strong><div class="kicker">${fa(g.tags.length)} شعر</div><div class="chips">${g.tags.slice(0, 6).map((t) => `<a class="chip" href="#/poem/${t.poemId}">${esc(t.poet || "شعر")}</a>`).join("")}</div></article>`).join("")}</div>
      `;
      atlasStage(body.querySelector("#places-all-atlas"));
      body.querySelectorAll(".pin[data-place]").forEach((p) => {
        p.onclick = (e) => {
          e.preventDefault();
          const c = body.querySelector(`#pcard-${p.dataset.place}`);
          c?.scrollIntoView({ block: "nearest", behavior: "smooth" });
          c?.classList.add("flash");
          setTimeout(() => c?.classList.remove("flash"), 1200);
        };
      });
    }
  };
  container.querySelectorAll("[data-pmode]").forEach((b) => { b.onclick = () => renderMode(b.dataset.pmode); });
  renderMode(mode);
}

/* ==========================================================================
   ابزار ۷: وزن‌ها و بحرهای عروضی (با نمایش نمونه شعرها درجا!)
   ========================================================================== */
async function mountVaznTool(container, params, isStale) {
  const { data } = await api("/rhythms?sortOnVerseCount=true");
  if (isStale()) return;

  const parse = (item) => {
    const m = String(item.rhythm || "").match(/^(.*?)\s*\((.*)\)\s*$/);
    const afaeel = m ? m[1] : item.rhythm;
    const name = m ? m[2] : "";
    const family = (name.split(/\s+/)[0] || "").replace(/[()]/g, "") || "بی‌نام";
    return { ...item, afaeel, name, family };
  };
  const items = [...data].sort((a, b) => b.verseCount - a.verseCount).map(parse);
  const total = items.reduce((s, i) => s + (i.verseCount || 0), 0) || 1;
  const famMap = new Map();
  for (const item of items) {
    const fam = famMap.get(item.family) || { name: item.family, count: 0, items: [] };
    fam.count += item.verseCount || 0;
    fam.items.push(item);
    famMap.set(item.family, fam);
  }
  const PALETTE = ["#0a6b60", "#1e3a8a", "#b2532f", "#b8892a", "#7a3b5c", "#5b6b1f", "#2f7fa6", "#a0456b"];
  const families = [...famMap.values()].sort((a, b) => b.count - a.count);
  families.forEach((f, i) => (f.color = PALETTE[i % PALETTE.length]));
  const colorOf = new Map(families.map((f) => [f.name, f.color]));
  const pct = (n) => `${fa(Math.round((n / total) * 1000) / 10)}٪`;
  const most = Math.max(1, ...items.map((i) => i.verseCount || 0));

  container.innerHTML = `
    <div class="tool-head">
      <div>
        <h2>وزن‌ها و بحرهای عروضی</h2>
        <p class="tool-sub">${fa(items.length)} وزن عروضی در گنجور؛ روی هر بحر یا وزن بزنید تا شعرهای هم‌وزنش همین‌جا باز شوند.</p>
      </div>
    </div>
    <div class="fam-strip" id="vazn-strip">${families.map((f) => {
      const w = (f.count / total) * 100;
      return `<button type="button" class="fam-seg" data-fam="${esc(f.name)}" style="flex:${w.toFixed(3)};--c:${f.color}" title="${esc(f.name)} · ${pct(f.count)}">${w > 6 ? `<span>${esc(f.name)}</span><small>${pct(f.count)}</small>` : ""}</button>`;
    }).join("")}</div>
    <div id="vazn-dossier" hidden></div>
    <div class="inline-search"><input id="vazn-q" placeholder="جستجوی نام بحر یا افاعیل (مثلاً هزج، مفاعیلن، رمل…)" autocomplete="off" /></div>
    <div class="vlist" id="vazn-list"></div>
  `;

  const dossier = container.querySelector("#vazn-dossier");
  const listEl = container.querySelector("#vazn-list");
  const qEl = container.querySelector("#vazn-q");
  let fam = "";

  const openMeter = async (id) => {
    const cur = items.find((i) => i.id === Number(id));
    if (!cur) return;
    dossier.hidden = false;
    dossier.innerHTML = `<div class="inline-dossier"><div class="loader"><span class="spin"></span><span>در حال دریافت شعرهای وزن ${esc(cur.afaeel)}…</span></div></div>`;
    dossier.scrollIntoView({ behavior: "smooth", block: "nearest" });
    const { data: poems, total: pt } = await api(`/poems/similar?metre=${encodeURIComponent(cur.rhythm)}&PageNumber=1&PageSize=9`);
    if (isStale()) return;
    const list = Array.isArray(poems) ? poems : [];
    dossier.innerHTML = `
      <div class="inline-dossier">
        <div class="inline-dossier-head">
          <div>
            <h3>${esc(cur.afaeel)}</h3>
            <p class="muted small" style="margin:2px 0 0;">${esc(cur.name)} · ${fa(cur.verseCount)} مصراع (${pct(cur.verseCount)} کل گنجور)${pt ? ` · ${fa(pt)} شعر` : ""}</p>
          </div>
          <button type="button" class="chip" id="close-vazn-dossier">بستن ×</button>
        </div>
        <div class="grid">${list.map((pm) => {
          const first = String(pm.plainText || "").split(/\r?\n/).filter((l) => l.trim()).slice(0, 2).join(" / ");
          return `<a class="hit" href="#/poem/${pm.id}"><div class="kicker">${esc(String(pm.fullTitle || "").split("»")[0])}</div><strong>${esc(pm.title)}</strong><p>${esc(first)}</p></a>`;
        }).join("")}</div>
      </div>`;
    dossier.querySelector("#close-vazn-dossier").onclick = () => (dossier.hidden = true);
  };

  const draw = () => {
    const q = qEl.value.trim();
    const shown = items.filter((i) => (!q || i.rhythm.includes(q)) && (!fam || i.family === fam)).slice(0, q || fam ? 60 : 20);
    container.querySelectorAll("#vazn-strip .fam-seg").forEach((s) => s.classList.toggle("dim", Boolean(fam) && s.dataset.fam !== fam));
    listEl.innerHTML = shown
      .map((i) => `<button type="button" class="vrow" data-vid="${i.id}" style="--c:${colorOf.get(i.family)}"><span class="vname"><strong>${esc(i.name || i.afaeel)}</strong>${i.name ? `<small>${esc(i.afaeel)}</small>` : ""}</span><span class="vbar"><i style="width:${Math.max(1, (i.verseCount / most) * 100).toFixed(1)}%"></i></span><b>${fa(i.verseCount)}</b></button>`)
      .join("") || `<p class="muted">وزنی با این نام پیدا نشد.</p>`;
  };
  container.querySelector("#vazn-strip").onclick = (e) => {
    const s = e.target.closest("[data-fam]");
    if (!s) return;
    fam = fam === s.dataset.fam ? "" : s.dataset.fam;
    draw();
  };
  listEl.onclick = (e) => {
    const r = e.target.closest("[data-vid]");
    if (r) openMeter(r.dataset.vid);
  };
  qEl.oninput = draw;
  draw();
  if (params.id) openMeter(params.id);
}

/* ==========================================================================
   زیرصفحه ۱: شاعر و آثار (#/poet/:id و #/cat/:id)
   ========================================================================== */
async function poetSubpage(id) {
  landingState.mounted = false;
  loading("شاعر");
  const { data } = await api(`/poet/${id}`);
  const poet = data.poet;
  const cat = data.cat || {};
  const children = cat.children || [];
  const poems = cat.poems || [];
  const img = poet.imageUrl
    ? `<img src="https://api.ganjoor.net${esc(poet.imageUrl)}" alt="">`
    : `<span class="medal">${esc((poet.nickname || poet.name || "؟").slice(0, 1))}</span>`;

  paint(
    poet.nickname || poet.name,
    `<article class="subpage">
       <p class="crumb"><a href="#/">← بازگشت به گنجور نو</a></p>
       <div class="poet-head">
         <figure class="ageshot portrait">${img}</figure>
         <div>
           <h1 style="margin:0 0 4px;color:var(--navy);">${esc(poet.name)}</h1>
           <p class="kicker" style="margin:0;">زاده ${esc(poet.birthPlace || "نامشخص")} ${poet.birthYearInLHijri ? yr(poet.birthYearInLHijri) : "؟"} · درگذشته ${poet.deathYearInLHijri ? yr(poet.deathYearInLHijri) : "؟"} ق${poet.deathYearInLHijri && poet.birthYearInLHijri ? ` · ${fa(poet.deathYearInLHijri - poet.birthYearInLHijri)} سال حیات` : ""}</p>
         </div>
       </div>
       ${poet.description ? `<div class="bio" id="bio">${esc(poet.description)}</div>${poet.description.length > 300 ? `<button class="chip" id="more-bio" type="button">ادامه شرح حال</button>` : ""}` : ""}
       <div class="chips" style="margin:14px 0;">
         ${children[0] ? `<a class="btn primary" href="#/cat/${children[0].id}">شروع از ${esc(children[0].title)}</a>` : ""}
         ${poet.birthYearInLHijri ? `<a class="chip" href="#/tree?poet=${poet.id}">هم‌عصران روی خط زمان</a>` : ""}
         <a class="chip" href="#/bridges/${poet.id}">پل‌های تضمین</a>
         <a class="chip" href="https://ganjoor.net${esc(poet.fullUrl)}" rel="noreferrer">در گنجور اصلی</a>
       </div>
       ${children.length ? `<h2 style="font-size:1.15rem;color:var(--navy);margin:20px 0 8px;">آثار و دفترها</h2><div class="covers">${children.map((b, i) => `<a class="cover c${i % 4}" href="#/cat/${b.id}"><strong>${esc(b.title)}</strong><small>مشاهده ←</small></a>`).join("")}</div>` : ""}
       ${poems.length ? `<h2 style="font-size:1.15rem;color:var(--navy);margin:20px 0 8px;">شعرها</h2><div class="grid">${poems.map((p) => `<a class="hit" href="#/poem/${p.id}"><strong>${esc(p.title)}</strong><p>${esc(p.excerpt || "")}</p></a>`).join("")}</div>` : ""}
     </article>`,
  );
  document.querySelector("#more-bio")?.addEventListener("click", () => document.querySelector("#bio").classList.toggle("open"));
}

async function catSubpage(id, query) {
  landingState.mounted = false;
  loading("فهرست آثار");
  const { data } = await api(`/cat/${id}?poems=true&mainSections=false`);
  const cat = data.cat || data;
  const pageNo = Math.max(1, Number(query.get("p") || 1));
  const size = 24;
  const poems = cat.poems || [];
  const slice = poems.slice((pageNo - 1) * size, pageNo * size);
  const pages = Math.ceil(poems.length / size);
  const children = cat.children || [];
  const crumbs = [`<a href="#/">← گنجور نو</a>`]
    .concat((cat.ancestors || []).map((a) => `<a href="#/cat/${a.id}">${esc(a.title)}</a>`))
    .join(" / ");

  paint(
    cat.title,
    `<article class="subpage">
       <p class="crumb">${crumbs}</p>
       <h1 style="margin:0 0 6px;color:var(--navy);">${esc(cat.title)}</h1>
       <p class="muted small">${poems.length ? `${fa(poems.length)} شعر` : ""}</p>
       ${children.length ? `<div class="covers">${children.map((b, i) => `<a class="cover c${i % 4}" href="#/cat/${b.id}"><strong>${esc(b.title)}</strong><small>مشاهده ←</small></a>`).join("")}</div>` : ""}
       <div class="grid">${slice.map((p) => `<a class="hit" href="#/poem/${p.id}"><strong>${esc(p.title)}</strong><p>${esc(p.excerpt || "")}</p></a>`).join("")}</div>
       ${pages > 1 ? `<div class="chips" style="margin-top:16px;">${pageNo > 1 ? `<a class="chip" href="#/cat/${id}?p=${pageNo - 1}">قبلی</a>` : ""}<span class="chip">صفحه ${fa(pageNo)} از ${fa(pages)}</span>${pageNo < pages ? `<a class="chip" href="#/cat/${id}?p=${pageNo + 1}">بعدی</a>` : ""}</div>` : ""}
     </article>`,
  );
}

/* ==========================================================================
   زیرصفحه ۲: خوانش شعر (#/poem/:id) — اتاق خوانش کامل با صوت، معنی، آرایه، وزن و یادداشت
   ========================================================================== */
function linesOf(poem) {
  const verses = [...(poem.verses || [])].sort((a, b) => a.vOrder - b.vOrder);
  if (verses.length) {
    return verses.map((v) => ({
      order: v.vOrder,
      text: v.text,
      end: v.versePosition === 1 || v.versePosition === 3,
      misra: v.versePosition === 1 || v.versePosition === 3 ? 2 : 1,
      couplet: v.coupletIndex,
      summary: v.coupletSummary || "",
    }));
  }
  return String(poem.plainText || "").split(/\r?\n/).map((t) => t.trim()).filter(Boolean).map((t, i) => ({ order: i, text: t, end: i % 2 === 1, misra: (i % 2) + 1, couplet: Math.floor(i / 2), summary: "" }));
}

function words(text) {
  let n = 0;
  return String(text).split(/(\s+)/).map((p) => (/\s+/.test(p) ? p : `<span class="word" data-w="${++n}">${esc(p)}</span>`)).join("");
}

function marked(text, spans) {
  let n = 0;
  return String(text || "").split(/(\s+)/).map((p) => {
    if (/\s+/.test(p)) return p;
    n += 1;
    const hit = spans.find((s) => n >= s.from && n <= s.to);
    return hit ? `<mark title="${esc(hit.label)}">${esc(p)}</mark>` : esc(p);
  }).join("");
}

async function poemSubpage(id, query) {
  landingState.mounted = false;
  loading("شعر");
  const { data: poem } = await api(`/poem/${id}?catInfo=true&navigation=true&recitations=true&verseDetails=true&comments=false&images=false&songs=false`);
  store.visit(poem.id);
  const saved = store.get();
  const isMarked = saved.marks.includes(poem.id);
  const cat = poem.category?.cat || {};
  const poet = poem.category?.poet || {};
  const recitations = poem.recitations || [];
  const lines = linesOf(poem);
  const section = (poem.sections || [])[0] || {};
  const metre = section.ganjoorMetre;
  const rhyme = section.rhymeLetters || "";
  const quotes = (poem.top6QuotedPoems || []).filter((i) => i.published !== false && i.relatedPoemId);
  const related = section.top6RelatedSections || [];
  const quiet = query.get("quiet") === "1";
  const count = section.coupletsCount || poem.coupletsCount;

  paint(
    poem.title,
    `<article class="read-grid" style="margin-top:20px;">
       <div class="parchment">
         <p class="crumb"><a href="#/">گنجور نو</a> ${poet.id ? `/ <a href="#/poet/${poet.id}">${esc(poet.nickname || poet.name)}</a>` : ""} ${cat.id ? `/ <a href="#/cat/${cat.id}">${esc(cat.title)}</a>` : ""}</p>
         <h1>${esc(poem.title)}</h1>
         <p class="byline">${esc(poet.name || "")}</p>
         <p class="meta">${[
           count ? `${fa(count)} بیت` : "",
           metre ? `<a href="#/vazn?id=${metre.id}">${esc(metre.rhythm)}</a>` : "",
           rhyme ? `قافیه «${esc(rhyme)}»` : "",
           `<a href="https://ganjoor.net${esc(poem.fullUrl)}" rel="noreferrer">در گنجور</a>`,
         ].filter(Boolean).join(" · ")}</p>
         <div class="poem" id="verses">${lines.map((l) => `<p class="verse ${l.end ? "end" : ""}" data-order="${l.order}" data-couplet="${l.couplet}" data-m="${l.misra}">${words(l.text)}</p>`).join("")}</div>
         <p class="muted small" style="text-align:center;">روی هر بیت بزنید تا شرحش بیاید؛ روی واژه بزنید تا در دیوان شاعر جستجو شود.</p>
         <div class="dock">
           ${recitations.length ? `<button class="btn primary" id="listen" type="button">▶ گوش بده</button>` : ""}
           <button class="btn" id="mark" type="button">${isMarked ? "★ نشان شد" : "☆ نشان"}</button>
           <button class="btn" id="quiet" type="button">${quiet ? "بازگشت" : "اتاق خلوت"}</button>
           ${poem.previous ? `<a class="btn" href="#/poem/${poem.previous.id}">قبلی</a>` : ""}
           ${poem.next ? `<a class="btn" href="#/poem/${poem.next.id}">بعدی</a>` : ""}
         </div>
       </div>
       <aside class="tools-aside">
         <div class="panel" id="side">
           <div class="side-head"><strong id="side-title">بیت ۱</strong></div>
           <div class="tabs" id="tabs">
             <button class="chip on" type="button" data-tab="mean">معنی</button>
             <button class="chip" type="button" data-tab="quote">تضمین${quotes.length + related.length ? ` ${fa(quotes.length + related.length)}` : ""}</button>
             <button class="chip" type="button" data-tab="device" id="device-tab">آرایه</button>
             ${metre ? `<button class="chip" type="button" data-tab="kin">هم‌وزن</button>` : ""}
             <button class="chip" type="button" data-tab="music">موسیقی</button>
             <button class="chip" type="button" data-tab="margin">حاشیه</button>
           </div>
           <div id="pane" aria-live="polite"></div>
         </div>
         ${recitations.length ? `<div class="panel player"><label class="small muted">خوانش <select id="reciter">${recitations.map((r, i) => `<option value="${i}">${esc(r.audioArtist || "خوانش")}</option>`).join("")}</select></label><audio id="player" controls preload="none" src="${esc(recitations[0].mp3Url)}"></audio><p class="muted small" id="sync-note" style="margin:6px 0 0;"></p></div>` : ""}
         <label class="panel"><span class="small muted">یادداشت من</span><textarea id="note" rows="3" placeholder="یادداشتی برای این شعر بنویسید…">${esc(saved.notes[poem.id] || "")}</textarea></label>
       </aside>
     </article>`,
    quiet,
  );

  let tab = "mean", activeCouplet = lines[0]?.couplet ?? 0, tagsCache = null;
  const pane = document.querySelector("#pane");
  const markCouplet = () => {
    document.querySelectorAll(".verse").forEach((n) => n.classList.toggle("pick", Number(n.dataset.couplet) === activeCouplet));
    const t = document.querySelector("#side-title");
    if (t) t.textContent = `بیت ${fa(activeCouplet + 1)}`;
  };
  const poemTags = async () => {
    if (!tagsCache) {
      const d = await rootApi(`/ganjoor/literary/poem/${poem.id}/tags`).catch(() => []);
      tagsCache = (Array.isArray(d) ? d : []).sort((a, b) => a.coupletIndex - b.coupletIndex);
    }
    return tagsCache;
  };
  poemTags().then((tags) => {
    const el = document.querySelector("#device-tab");
    if (el && tags.length) el.textContent = `آرایه ${fa(tags.length)}`;
  });

  const renderPane = async () => {
    document.querySelectorAll("#tabs .chip").forEach((n) => n.classList.toggle("on", n.dataset.tab === tab));
    if (tab === "mean") {
      const sum = lines.find((l) => l.couplet === activeCouplet && l.summary)?.summary || "";
      pane.innerHTML = `<p style="margin:0;font-size:0.92rem;">${esc(sum || poem.poemSummary || "شرح این بیت در گنجور ثبت نشده.")}</p>`;
      return;
    }
    if (tab === "quote") {
      const blocks = quotes.map((i) => `<a class="hit" href="#/poem/${i.relatedPoemId}" style="margin-bottom:6px;"><div class="kicker">${esc(i.cachedRelatedPoemPoetName || "")}</div><strong>${esc(i.relatedCoupletVerse2 || i.cachedRelatedPoemFullTitle || "")}</strong><p>${esc(i.coupletVerse1 || "")}</p></a>`)
        .concat(related.map((i) => `<a class="hit" href="#/poem/${i.targetPoemId}" style="margin-bottom:6px;"><div class="kicker">استقبال · ${esc(i.poetName || "")}</div><strong>${esc(i.fullTitle || "")}</strong></a>`));
      pane.innerHTML = blocks.length ? blocks.join("") : `<p class="muted small">تضمین یا استقبالی ثبت نشده.</p>`;
      return;
    }
    if (tab === "device") {
      pane.innerHTML = `<p class="muted small">در حال دریافت آرایه‌ها…</p>`;
      const [list, tags] = await Promise.all([devices(), poemTags()]);
      const names = new Map(list.map((i) => [i.id, i.name]));
      if (!tags.length) { pane.innerHTML = `<p class="muted small">برای این شعر آرایه‌ای ثبت نشده.</p>`; return; }
      const here = tags.filter((t) => t.coupletIndex === activeCouplet);
      const show = here.length ? here : tags;
      pane.innerHTML = show.map((t) => `<button class="hit device-hit" type="button" data-tag="${tags.indexOf(t)}"><div class="kicker">${esc(names.get(t.deviceId) || "آرایه")} · بیت ${fa(t.coupletIndex + 1)}</div><p>${(t.parts || []).map((p) => esc(p.concept?.name || p.text || "")).filter(Boolean).join(" ← ")}</p></button>`).join("");
      pane.querySelectorAll("[data-tag]").forEach((btn) => {
        btn.onclick = () => {
          document.querySelectorAll(".word.hl").forEach((n) => n.classList.remove("hl"));
          const tag = tags[Number(btn.dataset.tag)];
          for (const part of tag.parts || []) {
            if (!part.wordStart || part.coupletIndex < 0) continue;
            const v = document.querySelector(`.verse[data-couplet="${part.coupletIndex}"][data-m="${part.misra}"]`);
            for (let w = part.wordStart; w <= (part.wordEnd || part.wordStart); w++) v?.querySelector(`.word[data-w="${w}"]`)?.classList.add("hl");
          }
        };
      });
      return;
    }
    if (tab === "kin" && metre) {
      pane.innerHTML = `<p class="muted small">در حال جستجوی هم‌وزن‌ها…</p>`;
      const qs = `metre=${encodeURIComponent(metre.rhythm)}${rhyme ? `&rhyme=${encodeURIComponent(rhyme)}` : ""}&PageNumber=1&PageSize=7`;
      const { data: kin } = await api(`/poems/similar?${qs}`).catch(() => ({ data: [] }));
      const list = (Array.isArray(kin) ? kin : []).filter((i) => i.id !== poem.id).slice(0, 6);
      pane.innerHTML = list.length ? list.map((i) => `<a class="hit" href="#/poem/${i.id}" style="margin-bottom:6px;"><div class="kicker">${esc(String(i.fullTitle || "").split("»")[0])}</div><strong>${esc(i.title)}</strong></a>`).join("") : `<p class="muted small">هم‌وزنی پیدا نشد.</p>`;
      return;
    }
    pane.innerHTML = `<p class="muted small">در حال دریافت…</p>`;
    if (tab === "music") {
      const { data: d } = await api(`/poem/${poem.id}?songs=true&verseDetails=false&recitations=false&comments=false&images=false&navigation=false&catInfo=false`).catch(() => ({ data: {} }));
      const songs = d.songs || [];
      pane.innerHTML = songs.length ? songs.slice(0, 6).map((s) => `<p class="small"><a href="${esc(s.trackUrl)}" rel="noreferrer">${esc(s.artistName || "")} — ${esc(s.trackName || s.albumName || "")}</a></p>`).join("") : `<p class="muted small">قطعهٔ موسیقی ثبت نشده.</p>`;
    } else if (tab === "margin") {
      const { data: d } = await api(`/poem/${poem.id}?comments=true&verseDetails=false&recitations=false&songs=false&images=false&navigation=false&catInfo=false`).catch(() => ({ data: {} }));
      const cmts = (d.comments || []).slice(0, 5);
      pane.innerHTML = cmts.length ? cmts.map((c) => { const div = document.createElement("div"); div.innerHTML = c.htmlComment || ""; return `<article class="card" style="margin-bottom:6px;padding:10px;"><div class="kicker">${esc(c.authorName || "خواننده")}</div><p>${esc(div.textContent || "")}</p></article>`; }).join("") : `<p class="muted small">حاشیه‌ای ثبت نشده.</p>`;
    }
  };

  document.querySelector("#tabs").onclick = (e) => { const b = e.target.closest("[data-tab]"); if (b) { tab = b.dataset.tab; renderPane(); } };
  document.querySelector("#verses").onclick = async (e) => {
    const word = e.target.closest(".word");
    const verse = e.target.closest(".verse");
    if (!verse) return;
    activeCouplet = Number(verse.dataset.couplet);
    markCouplet();
    if (word) {
      const term = bare(word.textContent || "");
      pane.innerHTML = `<p class="muted small">جستجوی «${esc(term)}»…</p>`;
      const { data: hits } = await api(`/poems/search?term=${encodeURIComponent(term)}&pageNumber=1&pageSize=5${poet.id ? `&poetId=${poet.id}` : ""}`).catch(() => ({ data: [] }));
      pane.innerHTML = `<p class="small">واژهٔ «${esc(term)}» در آثار ${esc(poet.nickname || poet.name || "")}:</p>` + (Array.isArray(hits) && hits.length ? hits.map((h) => `<a class="hit" href="#/poem/${h.id}" style="margin-bottom:6px;"><strong>${esc(h.title)}</strong></a>`).join("") : `<p class="muted small">یافت نشد.</p>`) + `<p style="margin-top:8px;"><a class="chip" href="#/search?q=${encodeURIComponent(term)}">سنجش در کل گنجور ←</a></p>`;
      return;
    }
    renderPane();
  };
  markCouplet();
  renderPane();

  document.querySelector("#mark").onclick = (e) => {
    store.toggle(poem.id);
    e.currentTarget.textContent = store.get().marks.includes(poem.id) ? "★ نشان شد" : "☆ نشان";
  };
  document.querySelector("#quiet").onclick = () => { location.hash = quiet ? `#/poem/${poem.id}` : `#/poem/${poem.id}?quiet=1`; };
  document.querySelector("#note").onchange = (e) => store.note(poem.id, e.target.value);

  const player = document.querySelector("#player");
  const picker = document.querySelector("#reciter");
  if (player && picker) {
    audioNode = player;
    let times = [];
    const loadSync = async (rec) => {
      times = [];
      const note = document.querySelector("#sync-note");
      if (!rec.inSyncWithText || !rec.xmlText) { if (note) note.textContent = rec.audioArtist ? `خوانش ${rec.audioArtist}` : ""; return; }
      try {
        const xml = await fetch(rec.xmlText.startsWith("http") ? rec.xmlText : `https://api.ganjoor.net${rec.xmlText}`).then((r) => r.text());
        times = [...xml.matchAll(/<VerseOrder>(\d+)<\/VerseOrder>\s*<AudioMiliseconds>(\d+)/g)].map((m) => ({ order: Number(m[1]), at: Number(m[2]) }));
        if (note) note.textContent = "بیت‌ها هم‌زمان با صدا روشن می‌شوند.";
      } catch {}
    };
    picker.onchange = () => { const rec = recitations[Number(picker.value)]; player.src = rec.mp3Url; loadSync(rec); };
    player.ontimeupdate = () => {
      if (!times.length) return;
      const now = player.currentTime * 1000;
      let order = times[0].order;
      for (const m of times) if (m.at <= now) order = m.order;
      document.querySelectorAll(".verse").forEach((n) => n.classList.toggle("on", Number(n.dataset.order) === order));
    };
    const listen = document.querySelector("#listen");
    if (listen) {
      listen.onclick = () => (player.paused ? player.play() : player.pause());
      player.onplay = player.onpause = player.onended = () => { listen.textContent = player.paused ? "▶ گوش بده" : "❚❚ مکث"; };
    }
    loadSync(recitations[0]);
  }
}

/* ==========================================================================
   مودال راهنمای کاربری
   ========================================================================== */
function openGuideModal() {
  let modal = document.querySelector("#g-guide-modal-container");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "g-guide-modal-container";
    modal.innerHTML = `
      <div class="g-guide-overlay" id="g-guide-overlay"></div>
      <div class="g-guide-dialog" role="dialog" aria-modal="true" aria-labelledby="g-guide-title">
        <header class="g-guide-head">
          <h3 id="g-guide-title">راهنمای کاربری گنجور نو</h3>
          <button type="button" class="g-guide-close" id="g-guide-close" aria-label="بستن">×</button>
        </header>
        <div class="g-guide-body">
          <div class="g-guide-step"><span class="g-guide-num">۱</span><div><h4>همهٔ ابزارها در یک صفحه</h4><p>تمام ۷ ابزار پژوهشی (خط زمان هم‌عصران و نقشهٔ زادگاه‌ها، پل‌های تضمین، مردمان شاهنامه، آرایه‌های ادبی، واژه‌سنج، سفر ناصرخسرو و وزن‌ها) یکپارچه روی صفحهٔ اول قرار دارند و بدون پرش به صفحات دیگر درجا کار می‌کنند.</p></div></div>
          <div class="g-guide-step"><span class="g-guide-num">۲</span><div><h4>پیدا کردن سریع هر شاعر (مثل بیدل یا حافظ)</h4><p>نام شاعر را در کادر جستجوی بالای صفحه یا جستجوی خط زمان بنویسید؛ پیشنهاد آنی ظاهر می‌شود و می‌توانید با یک کلیک روی نوار حیاتش در خط زمان فرود بیایید یا مستقیماً وارد دیوانش شوید.</p></div></div>
          <div class="g-guide-step"><span class="g-guide-num">۳</span><div><h4>شناخت هم‌عصران و هم‌پوشانی حیات</h4><p>در خط زمان، روی هر نوار بزنید تا شاعران هم‌دورهٔ او روشن شوند و سال‌های دقیق هم‌پوشانی زیست‌شان در کارت مشخصات نمایش داده شود.</p></div></div>
          <div class="g-guide-step"><span class="g-guide-num">۴</span><div><h4>فقط دو زیرصفحه برای خوانش عمیق</h4><p>با انتخاب هر شاعر وارد صفحهٔ دیوان او، و با انتخاب هر شعر وارد اتاق خوانش (با صوت هم‌زمان، معنی بیت، آرایه‌ها، وزن و یادداشت شخصی) می‌شوید.</p></div></div>
        </div>
        <footer class="g-guide-foot"><button type="button" class="btn primary" id="g-guide-ok">متوجه شدم</button></footer>
      </div>`;
    document.body.appendChild(modal);
    const close = () => (modal.hidden = true);
    modal.querySelector("#g-guide-close").onclick = close;
    modal.querySelector("#g-guide-ok").onclick = close;
    modal.querySelector("#g-guide-overlay").onclick = close;
  }
  modal.hidden = false;
}

/* ==========================================================================
   مسیریاب ساده و هوشمند (۱ لندینگ پیج + فقط ۲ زیرصفحه، با پشتیبانی از لینک‌های قدیم)
   ========================================================================== */
async function render() {
  stopTimers();
  if (audioNode) { audioNode.pause(); audioNode = null; }
  const mine = ++renderToken;
  const hash = location.hash || "#/";
  const [pathPart, queryPart] = hash.split("?");
  const query = new URLSearchParams(queryPart || "");
  const parts = pathPart.replace(/^#\/?/, "").split("/").filter(Boolean);
  const first = parts[0] || "";

  const isSubpage = first === "poet" || first === "cat" || first === "poem";
  document.body.classList.toggle("is-home", !isSubpage);
  if (isSubpage) document.body.classList.remove("scrolled");
  mobile.hidden = true;
  menuBtn.setAttribute("aria-expanded", "false");

  try {
    // زیرصفحه ۱: شاعر و آثار
    if (first === "poet" && parts[1]) return await poetSubpage(parts[1]);
    if (first === "cat" && parts[1]) return await catSubpage(parts[1], query);
    // زیرصفحه ۲: خوانش شعر
    if (first === "poem" && parts[1]) return await poemSubpage(parts[1], query);

    // هر مسیر دیگر → لندینگ پیج یکپارچه با فعال‌سازی خودکار ابزار/بخش متناظر
    if (first === "tree" || first === "sky") return await landingPage({ tool: "tree", params: { poet: query.get("poet"), view: "timeline" }, scrollTo: "studio" });
    if (first === "map") return await landingPage({ tool: "tree", params: { y: query.get("y"), view: "map" }, scrollTo: "studio" });
    if (first === "bridges") return await landingPage({ tool: "bridges", params: { id: parts[1] || 2 }, scrollTo: "studio" });
    if (first === "people") return await landingPage({ tool: "people", params: {}, scrollTo: "studio" });
    if (first === "person" && parts[1]) return await landingPage({ tool: "people", params: { person: parts[1] }, scrollTo: "studio" });
    if (first === "devices") return await landingPage({ tool: "devices", params: {}, scrollTo: "studio" });
    if (first === "device" && parts[1]) return await landingPage({ tool: "devices", params: { device: parts[1], c: query.get("c") }, scrollTo: "studio" });
    if (first === "places") return await landingPage({ tool: "places", params: { all: query.get("all") }, scrollTo: "studio" });
    if (first === "vazn") return await landingPage({ tool: "vazn", params: { id: query.get("id") }, scrollTo: "studio" });
    if (first === "search" || first === "words") return await landingPage({ tool: "words", params: { q: query.get("q") || "عشق" }, scrollTo: "studio" });
    if (first === "poets") return await landingPage({ tool: "tree", scrollTo: "poets-wall" });
    if (first === "library") return await landingPage({ tool: "tree", scrollTo: "my-shelf" });
    return await landingPage({ tool: "tree" });
  } catch (err) {
    if (err === STALE || mine !== renderToken) return;
    failed(err);
  }
}

/* ── رویدادهای سراسری نوار بالا ── */
menuBtn.addEventListener("click", () => {
  const open = mobile.hidden;
  mobile.hidden = !open;
  menuBtn.setAttribute("aria-expanded", String(open));
});

document.addEventListener("click", (e) => {
  if (e.target.closest("[data-action='guide']")) {
    e.preventDefault();
    mobile.hidden = true;
    openGuideModal();
    return;
  }
  const jump = e.target.closest("[data-jump]");
  if (jump) {
    e.preventDefault();
    mobile.hidden = true;
    const targetId = jump.dataset.jump;
    if (document.body.classList.contains("is-home") && document.getElementById(targetId)) {
      document.getElementById(targetId).scrollIntoView({ behavior: "smooth", block: "start" });
    } else {
      location.hash = targetId === "poets-wall" ? "#/poets" : targetId === "my-shelf" ? "#/library" : "#/tree";
    }
  }
});

barForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const q = barInput.value.trim();
  if (!q) return;
  mobile.hidden = true;
  if (document.body.classList.contains("is-home") && landingState.activateTool) {
    document.getElementById("studio")?.scrollIntoView({ behavior: "smooth", block: "start" });
    landingState.activateTool("words", { q });
  } else {
    location.hash = `#/search?q=${encodeURIComponent(q)}`;
  }
});

window.addEventListener("scroll", () => {
  if (!document.body.classList.contains("is-home")) return;
  const heroSearch = document.querySelector("#hero-search-form");
  if (heroSearch) {
    document.body.classList.toggle("scrolled", heroSearch.getBoundingClientRect().bottom < 64);
  } else {
    document.body.classList.toggle("scrolled", window.scrollY > 180);
  }
}, { passive: true });

window.addEventListener("hashchange", render);
render();
