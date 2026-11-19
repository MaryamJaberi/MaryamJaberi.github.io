const API = "https://api.ganjoor.net/api/ganjoor";
const ROOT_API = "https://api.ganjoor.net/api";
const DATA_SOURCES = ["https://raw.githubusercontent.com/ganjoor/ganjoor-data/main/", "https://cdn.jsdelivr.net/gh/ganjoor/ganjoor-data@main/"];
const STALE = new Error("stale");
const REALM = { minLon: 43, maxLon: 73.5, minLat: 23, maxLat: 47.6 };

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
const root = document.querySelector("#content");
const bar = document.querySelector("#bar");
const foot = document.querySelector("#foot");
const mobile = document.querySelector("#mobile");
const menuBtn = document.querySelector("#menu");
const form = document.querySelector("#search-form");
const input = document.querySelector("#q");
const cache = new Map();
let renderToken = 0;
let audioNode = null;

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
    data.marks = data.marks.includes(id) ? data.marks.filter((item) => item !== id) : [id, ...data.marks];
    this.set(data);
  },
  note(id, text) {
    const data = this.get();
    data.notes[id] = text;
    this.set(data);
  },
  visit(id) {
    const data = this.get();
    data.history = [id, ...data.history.filter((item) => item !== id)].slice(0, 24);
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

const files = new Map();
async function fileJson(name) {
  if (files.has(name)) return files.get(name);
  const token = renderToken;
  let data = null;
  for (const base of DATA_SOURCES) {
    try {
      const response = await fetch(`${base}${name}`);
      if (!response.ok) continue;
      data = await response.json();
      break;
    } catch {}
  }
  if (data === null) throw new Error(`داده ${name} نیامد`);
  files.set(name, data);
  if (token !== renderToken) throw STALE;
  return data;
}

let localData = null;
async function local() {
  if (localData) return localData;
  const response = await fetch("data.json");
  if (!response.ok) throw new Error("data.json");
  localData = await response.json();
  return localData;
}

async function rootApi(path) {
  const key = `root:${path}`;
  if (cache.has(key)) return cache.get(key).data;
  const token = renderToken;
  const response = await fetch(ROOT_API + path);
  if (!response.ok) throw new Error(String(response.status));
  const data = await response.json();
  cache.set(key, { data, total: 0 });
  if (token !== renderToken) throw STALE;
  return data;
}

async function placesOnVerses(poet) {
  const slug = String(poet.fullUrl || "").replace(/^\//, "");
  if (!slug) return [];
  const [geo, locations] = await Promise.all([fileJson("geotags.json"), fileJson("locations.json")]);
  const dated = geo.filter((item) => item.LunarYear);
  const buckets = [...new Set(dated.map((item) => Math.floor(item.PoemId / 2000)))];
  const index = {};
  for (const bucket of buckets) Object.assign(index, await fileJson(`index/poems-by-id/${bucket}.json`));
  const byId = new Map(locations.map((item) => [item.Id, item]));
  const seen = new Set();
  const stops = [];
  for (const item of dated) {
    const url = index[String(item.PoemId)] || "";
    if (!url.startsWith(`/${slug}/`)) continue;
    const place = byId.get(item.LocationId);
    if (!place) continue;
    const key = `${item.LunarYear}-${place.Name}`;
    if (seen.has(key)) continue;
    seen.add(key);
    stops.push({
      year: item.LunarYear,
      place: place.Name,
      poemId: item.PoemId,
      lat: place.Latitude,
      lon: place.Longitude,
      verified: Boolean(item.VerifiedDate),
    });
  }
  return stops.sort((a, b) => a.year - b.year);
}

function portrait(poet) {
  const img = poet.imageUrl
    ? `<img src="https://api.ganjoor.net${esc(poet.imageUrl)}" alt="">`
    : `<span class="medal t1">${esc((poet.nickname || poet.name || "؟").slice(0, 1))}</span>`;
  return `<figure class="ageshot portrait">${img}</figure>`;
}

function centuryOf(year) {
  if (!year) return 0;
  return Math.floor((year - 1) / 100) + 1;
}

async function api(path) {
  if (cache.has(path)) return cache.get(path);
  const token = renderToken;
  const response = await fetch(API + path);
  if (!response.ok) throw new Error(String(response.status));
  const data = await response.json();
  const total = pagingTotal(response);
  const packed = { data, total };
  cache.set(path, packed);
  if (token !== renderToken) throw STALE;
  return packed;
}

function pagingTotal(response) {
  const raw = response.headers.get("paging-headers");
  if (raw) {
    try {
      const info = JSON.parse(raw);
      if (info.totalCount != null) return Number(info.totalCount);
    } catch {}
  }
  return Number(response.headers.get("items-count") || 0);
}

const fa = (value) => Number(value || 0).toLocaleString("fa-IR");
const TOOL_ROUTES = new Set(["discover", "map", "places", "tree", "bridges", "people", "person", "vazn", "devices", "device", "words", "layers"]);

function routeName() {
  return (location.hash || "#/").replace(/^#\/?/, "").split(/[/?]/)[0];
}

const PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
const SKIP_DIGITS = new Set(["TEXTAREA", "INPUT", "SCRIPT", "STYLE", "CODE"]);
function persianDigits(node) {
  const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, {
    acceptNode: (text) => (/[0-9]/.test(text.nodeValue) && !SKIP_DIGITS.has(text.parentNode?.nodeName) && !text.parentNode?.closest?.(".latin") ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT),
  });
  const list = [];
  while (walker.nextNode()) list.push(walker.currentNode);
  for (const text of list) text.nodeValue = text.nodeValue.replace(/[0-9]/g, (digit) => PERSIAN_DIGITS[digit]);
}
new MutationObserver((records) => {
  for (const record of records) {
    if (record.type === "characterData") persianDigits(record.target.parentNode || record.target);
    else record.addedNodes.forEach((added) => (added.nodeType === 3 ? persianDigits(added.parentNode) : added.nodeType === 1 && persianDigits(added)));
  }
}).observe(document.body, { childList: true, subtree: true, characterData: true });
persianDigits(document.body);

function paint(title, html, quiet = false) {
  document.title = `${title} — گنجور نو`;
  document.body.classList.toggle("quiet", quiet);
  bar.hidden = quiet;
  foot.hidden = quiet;
  const route = routeName();
  const back = TOOL_ROUTES.has(route) && route !== "discover" && !html.trimStart().startsWith('<p class="crumb">') ? `<p class="crumb"><a href="#/discover">ابزارها</a></p>` : "";
  root.innerHTML = `<div class="sheet">${back}${html}</div>`;
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
    `<section class="empty-state"><h1>${offline ? "اینترنت وصل نیست" : "ارتباط برقرار نشد"}</h1>
     <p>${offline ? "اتصال را برقرار کن و دوباره امتحان کن." : "گنجور الان جواب نداد. چند لحظه بعد دوباره امتحان کن."}</p>
     <p class="chips"><button class="btn primary" type="button" id="retry">دوباره</button><a class="chip" href="#/">خانه</a></p>
     <p class="muted">${esc(error.message)}</p></section>`,
  );
  document.querySelector("#retry").onclick = () => {
    cache.clear();
    render();
  };
}

function opening(poem) {
  if (!poem?.id) return "";
  const lines = String(poem.plainText || "")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(0, 4);
  if (!lines.length) return "";
  const poet = poem.category?.poet;
  return `<h2 class="section">برای شروع</h2><a class="opening" href="#/poem/${poem.id}"><div class="kicker">${esc(poet?.nickname || poet?.name || "")}</div>${lines.map((line) => `<p>${esc(line)}</p>`).join("")}<span class="muted">${esc(poem.title || "")}</span></a>`;
}

function poetFace(poet) {
  const letter = esc((poet.nickname || poet.name || "؟").slice(0, 1));
  const img = poet.imageUrl ? `<img alt="" src="https://api.ganjoor.net${esc(poet.imageUrl)}" onerror="this.remove()" />` : "";
  const years = poet.birthYearInLHijri ? `<bdi dir="ltr">${poet.birthYearInLHijri}–${poet.deathYearInLHijri || "؟"}</bdi>` : "";
  return `<a class="face" href="#/poet/${poet.id}"><span class="medal">${img}<b>${letter}</b></span><strong>${esc(poet.nickname || poet.name)}</strong><small>${esc(poet.birthPlace || "")}${years ? " · " + years : ""}</small></a>`;
}

const ROSETTE = (() => {
  const petals = Array.from({ length: 16 }, (_, i) => `<path d="M100 100 L100 18 Q112 52 100 100" transform="rotate(${i * 22.5} 100 100)" />`).join("");
  const star = (r, rot) =>
    Array.from({ length: 16 }, (_, i) => {
      const a = ((i * 22.5 + rot) * Math.PI) / 180;
      const rr = i % 2 ? r * 0.72 : r;
      return `${(100 + Math.sin(a) * rr).toFixed(1)},${(100 - Math.cos(a) * rr).toFixed(1)}`;
    }).join(" ");
  return `<svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="96" class="ro-ring" /><circle cx="100" cy="100" r="88" class="ro-ring thin" /><g class="ro-petals">${petals}</g><polygon class="ro-star" points="${star(64, 0)}" /><polygon class="ro-star2" points="${star(40, 11.25)}" /><circle cx="100" cy="100" r="16" class="ro-core" /></svg>`;
})();

const FAMOUS = ["فردوسی", "رودکی", "خیام", "مولانا", "سعدی", "حافظ", "عطار", "نظامی", "سنایی", "ناصرخسرو", "جامی", "صائب", "پروین", "شهریار", "ایرج", "وحشی"];

async function home() {
  loading("خانه");
  const [{ data: poets }, bit] = await Promise.all([
    api("/poets"),
    fetch(`${API}/poem/random?poetId=2`).then((response) => (response.ok ? response.json() : null)).catch(() => null),
  ]);
  const pinned = [...poets].filter((poet) => poet.pinOrder).sort((a, b) => a.pinOrder - b.pinOrder);
  const pinnedIds = new Set(pinned.map((poet) => poet.id));
  const everyone = pinned.concat(
    poets
      .filter((poet) => !pinnedIds.has(poet.id))
      .sort((a, b) => (a.birthYearInLHijri || 9999) - (b.birthYearInLHijri || 9999) || (a.nickname || "").localeCompare(b.nickname || "", "fa")),
  );
  paint(
    "خانه",
    `<section class="welcome">
       <div>
         <p class="kicker">خواندن شعر فارسی</p>
         <h1>به جهان شعر پارسی خوش آمدید</h1>
         <p class="lead">همه شاعران و شعرهای منتشرشده گنجور اینجاست. متن را بخوان، صوت را بشنو، و نشان را برای خودت نگه دار.</p>
         <form class="big-search" id="home-search">
           <input name="q" placeholder="بیت، واژه یا نام شاعر…" aria-label="جستجو" />
           <button class="btn primary" type="submit">جستجو</button>
         </form>
         <p class="chips">
           <button class="chip on" id="random" type="button">یک شعر تصادفی</button>
           <a class="chip" href="#/poets">همه شاعران</a>
           <a class="chip" href="#/discover">همه ابزارها</a>
         </p>
       </div>
       <div class="rosette" aria-hidden="true">${ROSETTE}</div>
     </section>
     ${opening(bit)}
     <h2 class="section">ابزارها</h2>
     <div class="toolbelt">${HOME_TOOLS.map(([href, title, text, icon]) => `<a class="tool" href="${href}"><span class="tool-icon" aria-hidden="true">${icon}</span><strong>${title}</strong><small>${text}</small></a>`).join("")}</div>
     <p><a href="#/discover">همه ابزارها، دسته به دسته</a></p>
     <h2 class="section">شاعران نامدار</h2>
     <div class="faces">${FAMOUS.map((name) => poets.find((poet) => poet.nickname === name) || poets.find((poet) => (poet.nickname || poet.name || "").startsWith(name)))
       .filter(Boolean)
       .slice(0, 12)
       .map(poetFace)
       .join("")}</div>
     <p class="more"><a class="btn" href="#/poets">همه ${fa(everyone.length)} شاعر</a></p>
     <p class="note">متن و صوت از <a href="https://ganjoor.net" rel="noreferrer">گنجور</a> می‌آید. این سایت رسمی گنجور نیست؛ طراحی و ساختش با مریم جابری است.</p>`,
  );
  document.querySelector("#home-search").onsubmit = (event) => {
    event.preventDefault();
    const q = new FormData(event.currentTarget).get("q") || "";
    location.hash = `#/search?q=${encodeURIComponent(String(q).trim())}`;
  };
  document.querySelector("#random").onclick = async () => {
    document.querySelector("#random").textContent = "می‌آورم…";
    try {
    const response = await fetch(`${API}/poem/random`);
    if (!response.ok) throw new Error(String(response.status));
    const data = await response.json();
    location.hash = `#/poem/${data.id}`;
    } catch (error) {
      failed(error);
    }
  };
}

async function poetsPage(query) {
  loading("شاعران");
  const { data: poets } = await api("/poets");
  const century = Number(query.get("c") || 0);
  const centuries = [...new Set(poets.map((poet) => centuryOf(poet.birthYearInLHijri)).filter(Boolean))].sort((a, b) => a - b);
  paint(
    "شاعران",
    `<h1>شاعران</h1>
     <p class="lead">${poets.length} شاعر منتشرشده.</p>
     <div class="cents">${[`<a class="cent ${century ? "" : "on"}" href="#/poets">همه</a>`].concat(centuries.map((item) => `<a class="cent ${century === item ? "on" : ""}" href="#/poets?c=${item}">قرن ${item}</a>`)).join("")}</div>
     <form class="big-search" id="poet-filter"><input id="poet-q" placeholder="نام را بنویس" aria-label="پالایش نام" /></form>
     <div class="faces" id="poet-list"></div>`,
  );
  const box = document.querySelector("#poet-q");
  const list = document.querySelector("#poet-list");
  const draw = () => {
    const q = box.value.trim();
    const shown = poets.filter((poet) => {
      const yearOk = !century || centuryOf(poet.birthYearInLHijri) === century;
      const text = `${poet.name} ${poet.nickname} ${poet.birthPlace || ""}`;
      return yearOk && (!q || text.includes(q));
    });
    list.innerHTML = shown.length ? shown.map(poetFace).join("") : `<p class="muted">کسی با این نام در این قرن نیست.</p>`;
  };
  box.oninput = draw;
  draw();
}

async function poetPage(id) {
  loading("شاعر");
  const { data } = await api(`/poet/${id}`);
  const poet = data.poet;
  const cat = data.cat || {};
  const children = cat.children || [];
  const poems = cat.poems || [];
  const books = children
    .map((book, index) => `<a class="cover c${index % 4}" href="#/cat/${book.id}"><strong>${esc(book.title)}</strong><small>خواندن ←</small></a>`)
    .join("");
  const loose = poems
    .map((poem) => `<a class="hit" href="#/poem/${poem.id}"><strong>${esc(poem.title)}</strong><p>${esc(poem.excerpt || "")}</p></a>`)
    .join("");
  paint(
    poet.nickname || poet.name,
    `<p class="crumb"><a href="#/poets">شاعران</a></p>
     <div class="poet-head">
       ${portrait(poet)}
       <div>
         <h1>${esc(poet.name)}</h1>
         <p class="kicker">زاده ${esc(poet.birthPlace || "جای نامشخص")} <bdi dir="ltr">${poet.birthYearInLHijri || "؟"}</bdi> · درگذشته ${esc(poet.deathPlace || poet.birthPlace || "")} <bdi dir="ltr">${poet.deathYearInLHijri || "؟"}</bdi> ق${poet.deathYearInLHijri && poet.birthYearInLHijri ? ` · ${fa(poet.deathYearInLHijri - poet.birthYearInLHijri)} سال` : ""}</p>
       </div>
     </div>
     <div class="bio" id="bio">${esc(poet.description || "")}</div>
     ${(poet.description || "").length > 320 ? `<button class="btn" id="more" type="button">ادامه شرح</button>` : ""}
     <p class="chips">
       ${children[0] ? `<a class="btn primary" href="#/cat/${children[0].id}">شروع از ${esc(children[0].title)}</a>` : ""}
       <a class="chip" href="https://ganjoor.net${esc(poet.fullUrl)}" rel="noreferrer">در گنجور</a>
       ${poet.birthYearInLHijri ? `<a class="chip" href="#/map?y=${Math.round(((poet.birthYearInLHijri || 0) + (poet.deathYearInLHijri || poet.birthYearInLHijri)) / 2)}">هم‌عصران این سال‌ها</a>` : ""}
       <a class="chip" href="#/bridges/${poet.id}">پل‌های ثبت‌شده</a><a class="chip" href="#/tree?poet=${poet.id}">جای او در درخت</a>
     </p>
     ${books ? `<h2 class="section">آثار</h2><div class="covers">${books}</div>` : ""}
     ${loose ? `<h2 class="section">شعرها</h2><div class="grid">${loose}</div>` : ""}`,
  );
  document.querySelector("#more")?.addEventListener("click", () => document.querySelector("#bio").classList.toggle("open"));
}

async function catPage(id, query) {
  loading("فهرست");
  const { data } = await api(`/cat/${id}?poems=true&mainSections=false`);
  const cat = data.cat || data;
  const pageNo = Math.max(1, Number(query.get("p") || 1));
  const size = 24;
  const poems = cat.poems || [];
  const slice = poems.slice((pageNo - 1) * size, pageNo * size);
  const pages = Math.ceil(poems.length / size);
  const children = (cat.children || [])
    .map((book, index) => `<a class="cover c${index % 4}" href="#/cat/${book.id}"><strong>${esc(book.title)}</strong></a>`)
    .join("");
  const crumbs = [`<a href="#/poets">شاعران</a>`]
    .concat((cat.ancestors || []).map((item) => `<a href="#/cat/${item.id}">${esc(item.title)}</a>`))
    .join(" / ");
  paint(
    cat.title,
    `<p class="crumb">${crumbs}</p>
     <h1>${esc(cat.title)}</h1>
     <p class="muted">${poems.length ? `${poems.length} شعر` : ""}</p>
     ${children ? `<div class="covers">${children}</div>` : ""}
     <div class="grid">${slice.map((poem) => `<a class="hit" href="#/poem/${poem.id}"><strong>${esc(poem.title)}</strong><p>${esc(poem.excerpt || "")}</p></a>`).join("")}</div>
     ${pages > 1 ? `<p class="chips">${pageNo > 1 ? `<a class="chip" href="#/cat/${id}?p=${pageNo - 1}">قبلی</a>` : ""}<span class="chip">صفحه ${pageNo} از ${pages}</span>${pageNo < pages ? `<a class="chip" href="#/cat/${id}?p=${pageNo + 1}">بعدی</a>` : ""}</p>` : ""}`,
  );
}

function linesOf(poem) {
  const verses = [...(poem.verses || [])].sort((a, b) => a.vOrder - b.vOrder);
  if (verses.length) {
    return verses.map((verse) => ({
      order: verse.vOrder,
      text: verse.text,
      end: verse.versePosition === 1 || verse.versePosition === 3,
      misra: verse.versePosition === 1 || verse.versePosition === 3 ? 2 : 1,
      couplet: verse.coupletIndex,
      summary: verse.coupletSummary || "",
    }));
  }
  return String(poem.plainText || "")
    .split(/\r?\n/)
    .map((text) => text.trim())
    .filter(Boolean)
    .map((text, index) => ({ order: index, text, end: index % 2 === 1, misra: (index % 2) + 1, couplet: Math.floor(index / 2), summary: "" }));
}

function words(text) {
  let n = 0;
  return String(text)
    .split(/(\s+)/)
    .map((part) => {
      if (!part.trim()) return esc(part);
      n += 1;
      return `<button class="word" type="button" data-w="${n}">${esc(part)}</button>`;
    })
    .join("");
}

function marked(text, spans) {
  const parts = String(text || "").split(/(\s+)/);
  let n = 0;
  return parts
    .map((part) => {
      if (!part.trim()) return esc(part);
      n += 1;
      const hit = spans.find((span) => n >= span.from && n <= span.to);
      return hit ? `<mark title="${esc(hit.label)}">${esc(part)}</mark>` : esc(part);
    })
    .join("");
}

let deviceList = null;
async function devices() {
  if (!deviceList) deviceList = await rootApi("/ganjoor/literary/devices");
  return deviceList;
}

const DEVICE_GROUP = { 0: "بیان", 1: "بدیع لفظی", 2: "بدیع معنوی", Bayan: "بیان", BadiLafzi: "بدیع لفظی", BadiManavi: "بدیع معنوی" };

async function poemPage(id, query) {
  loading("شعر");
  const { data: poem } = await api(
    `/poem/${id}?catInfo=true&navigation=true&recitations=true&verseDetails=true&comments=false&images=false&songs=false`,
  );
  store.visit(poem.id);
  const saved = store.get();
  const marked = saved.marks.includes(poem.id);
  const cat = poem.category?.cat || {};
  const poet = poem.category?.poet || {};
  const recitations = poem.recitations || [];
  const lines = linesOf(poem);
  const section = (poem.sections || [])[0] || {};
  const metre = section.ganjoorMetre;
  const rhyme = section.rhymeLetters || "";
  const quotes = (poem.top6QuotedPoems || []).filter((item) => item.published !== false && item.relatedPoemId);
  const related = section.top6RelatedSections || [];
  const quiet = query.get("quiet") === "1";
  const count = section.coupletsCount || poem.coupletsCount;
  const brief = String(poem.poemSummary || "");
  paint(
    poem.title,
    `<article class="read stage">
       <div class="parchment">
         <p class="crumb">${poet.id ? `<a href="#/poet/${poet.id}">${esc(poet.nickname || poet.name)}</a>` : ""} ${cat.id ? `/ <a href="#/cat/${cat.id}">${esc(cat.title)}</a>` : ""}</p>
         <h1>${esc(poem.title)}</h1>
         <div class="ornament" aria-hidden="true"></div>
         <p class="byline">${esc(poet.name || "")}</p>
         <p class="meta">${[
           count ? `${fa(count)} بیت` : "",
           metre ? `<a href="#/vazn?id=${metre.id}" title="همه شعرهای این وزن">${esc(metre.rhythm)}</a>` : "",
           rhyme ? `قافیه «${esc(rhyme)}»` : "",
           poem.sourceName ? `منبع: ${esc(poem.sourceName)}` : "",
           `<a href="https://ganjoor.net${esc(poem.fullUrl)}" rel="noreferrer">در گنجور</a>`,
         ]
           .filter(Boolean)
           .join(`<span aria-hidden="true"> · </span>`)}</p>
         ${brief ? `<p class="lead summary">${esc(brief.length > 220 ? `${brief.slice(0, 220)}…` : brief)}</p>` : ""}
         <div class="poem" id="verses">${lines
           .map(
             (line) =>
               `<p class="verse ${line.end ? "end" : ""}" data-order="${line.order}" data-couplet="${line.couplet}" data-m="${line.misra}">${words(line.text)}</p>`,
           )
           .join("")}</div>
         <p class="muted hint">روی بیت بزن تا شرحش بیاید؛ روی واژه بزن تا جای دیگرش را ببینی.</p>
         <div class="dock">
           ${recitations.length ? `<button class="btn primary" id="listen" type="button" aria-pressed="false">▶ گوش بده</button>` : ""}
           <button class="btn" id="mark" type="button" aria-pressed="${marked}">${marked ? "★ نشان شد" : "☆ نشان"}</button>
           <button class="btn" id="quiet" type="button">${quiet ? "بازگشت" : "اتاق خلوت"}</button>
           ${poem.previous ? `<a class="btn" href="#/poem/${poem.previous.id}">قبلی</a>` : ""}
           ${poem.next ? `<a class="btn" href="#/poem/${poem.next.id}">بعدی</a>` : ""}
         </div>
       </div>
       <aside class="tools">
         <nav class="rail">
           ${poet.id ? `<a href="#/poet/${poet.id}">${esc(poet.nickname || poet.name)}</a>` : ""}
           ${cat.id ? `<a href="#/cat/${cat.id}">فهرست ${esc(cat.title || "")}</a>` : ""}
           <a href="https://ganjoor.net${esc(poem.fullUrl)}" rel="noreferrer">متن در گنجور</a>
           ${poem.previous ? `<a href="#/poem/${poem.previous.id}">قبلی</a>` : ""}
           ${poem.next ? `<a href="#/poem/${poem.next.id}">بعدی</a>` : ""}
         </nav>
         <div class="panel" id="side">
           <div class="side-head"><strong id="side-title">بیت ۱</strong><button class="close" id="side-close" type="button" aria-label="بستن">×</button></div>
           <div class="tabs" id="tabs">
             <button class="chip on" type="button" data-tab="mean">معنی</button>
             <button class="chip" type="button" data-tab="quote">تضمین${quotes.length + related.length ? ` ${quotes.length + related.length}` : ""}</button>
             <button class="chip" type="button" data-tab="music">موسیقی</button>
             <button class="chip" type="button" data-tab="margin">حاشیه</button>
             <button class="chip" type="button" data-tab="mirror">آینه</button>
             <button class="chip" type="button" data-tab="device" id="device-tab">آرایه</button>
             ${metre ? `<button class="chip" type="button" data-tab="kin">هم‌وزن</button>` : ""}
           </div>
           <div id="pane" aria-live="polite"></div>
         </div>
         ${
           recitations.length
             ? `<div class="panel player">
                  <label>خوانش <select id="reciter">${recitations.map((item, index) => `<option value="${index}">${esc(item.audioArtist || "خوانش")}</option>`).join("")}</select></label>
                  <audio id="player" controls preload="none" src="${esc(recitations[0].mp3Url)}"></audio>
                  <p class="muted" id="sync-note"></p>
                </div>`
             : `<p class="muted">برای این شعر در گنجور خوانش ثبت نشده.</p>`
         }
         <label class="panel block">یادداشت من <textarea id="note" rows="4">${esc(saved.notes[poem.id] || "")}</textarea></label>
       </aside>
     </article>`,
    quiet,
  );
  let tab = "mean";
  let activeCouplet = lines[0]?.couplet ?? 0;
  const pane = document.querySelector("#pane");
  const side = document.querySelector("#side");
  const narrow = () => window.matchMedia("(max-width: 959px)").matches;
  function showAboveSheet(node) {
    if (!node || !side.classList.contains("open")) return;
    const box = node.getBoundingClientRect();
    const room = window.innerHeight - side.getBoundingClientRect().height;
    if (box.top < 70 || box.bottom > room - 8) window.scrollBy({ top: box.top - Math.max(70, (room - box.height) / 2), behavior: "smooth" });
  }
  function openSheet() {
    if (!narrow()) return;
    side.classList.add("open");
    document.body.classList.add("sheet-on");
    showAboveSheet(document.querySelector(".verse.pick"));
  }
  function closeSheet() {
    side.classList.remove("open");
    document.body.classList.remove("sheet-on");
  }
  document.querySelector("#side-close").onclick = closeSheet;
  document.onkeydown = (event) => {
    if (event.key === "Escape") closeSheet();
  };
  function markCouplet() {
    document.querySelectorAll(".verse").forEach((node) => node.classList.toggle("pick", Number(node.dataset.couplet) === activeCouplet));
    const title = document.querySelector("#side-title");
    if (title) title.textContent = `بیت ${fa(activeCouplet + 1)}`;
  }
  let tagsCache = null;
  async function poemTags() {
    if (!tagsCache) {
      const data = await rootApi(`/ganjoor/literary/poem/${poem.id}/tags`);
      tagsCache = (Array.isArray(data) ? data : []).sort((a, b) => a.coupletIndex - b.coupletIndex);
    }
    return tagsCache;
  }
  function lightTag(tag) {
    document.querySelectorAll(".word.hl").forEach((node) => node.classList.remove("hl"));
    for (const part of tag.parts || []) {
      if (!part.wordStart || part.coupletIndex < 0) continue;
      const verse = document.querySelector(`.verse[data-couplet="${part.coupletIndex}"][data-m="${part.misra}"]`);
      if (!verse) continue;
      for (let w = part.wordStart; w <= (part.wordEnd || part.wordStart); w += 1) verse.querySelector(`.word[data-w="${w}"]`)?.classList.add("hl");
      if (side.classList.contains("open")) showAboveSheet(verse);
      else verse.scrollIntoView({ block: "nearest" });
    }
  }
  poemTags()
    .then((tags) => {
      const label = document.querySelector("#device-tab");
      if (label && tags.length) label.textContent = `آرایه ${tags.length}`;
    })
    .catch(() => {});
  function summaryOf(index) {
    return lines.find((line) => line.couplet === index && line.summary)?.summary || "";
  }
  async function renderPane() {
    document.querySelectorAll("#tabs .chip").forEach((node) => node.classList.toggle("on", node.dataset.tab === tab));
    if (tab === "mean") {
      pane.innerHTML = `<p>${esc(summaryOf(activeCouplet) || poem.poemSummary || "شرح این بیت در گنجور ثبت نشده.")}</p>`;
      return;
    }
    if (tab === "quote") {
      const blocks = quotes
        .map(
          (item) =>
            `<a class="hit" href="#/poem/${item.relatedPoemId}"><div class="kicker">${esc(item.cachedRelatedPoemPoetName || "")}</div><strong>${esc(item.relatedCoupletVerse2 || item.cachedRelatedPoemFullTitle || "")}</strong><p>${esc(item.coupletVerse1 || "")}</p></a>`,
        )
        .concat(
          related.map(
            (item) =>
              `<a class="hit" href="#/poem/${item.targetPoemId}"><div class="kicker">استقبال · ${esc(item.poetName || "")}</div><strong>${esc(item.fullTitle || "")}</strong></a>`,
          ),
        );
      pane.innerHTML = blocks.length ? blocks.join("") : `<p class="muted">تضمین یا استقبالی برای این شعر ثبت نشده.</p>`;
      return;
    }
    if (tab === "mirror") {
      pane.innerHTML = `<p class="muted">یک واژه از شعر را بزن.</p>`;
      return;
    }
    if (tab === "device") {
      pane.innerHTML = `<p class="muted">می‌آورم…</p>`;
      try {
        const [list, tags] = await Promise.all([devices(), poemTags()]);
        const names = new Map(list.map((item) => [item.id, item.name]));
        if (!tags.length) {
          pane.innerHTML = `<p class="muted">برای این شعر هنوز آرایه‌ای در گنجور ثبت نشده.</p><p><a href="#/devices">آرایه‌ها در همه گنجور</a></p>`;
          return;
        }
        const here = tags.filter((tag) => tag.coupletIndex === activeCouplet);
        const show = here.length ? here : tags;
        pane.innerHTML =
          `<p class="muted">${here.length ? "آرایه‌های همین بیت." : `${tags.length} آرایه در این شعر. روی بیتی بزن تا فقط آرایه‌های همان بیت بیاید.`}</p>` +
          show
            .map(
              (tag, index) =>
                `<button class="hit device-hit" type="button" data-tag="${tags.indexOf(tag)}"><div class="kicker">${esc(names.get(tag.deviceId) || "آرایه")} · بیت ${tag.coupletIndex + 1}${tag.uncertain ? " · نامطمئن" : ""}</div><p>${(tag.parts || [])
                  .map((part) => esc(part.concept?.name || part.text || ""))
                  .filter(Boolean)
                  .join(" ← ")}</p></button>`,
            )
            .join("") +
          `<p><a href="#/devices">آرایه‌ها در همه گنجور</a></p>`;
        pane.querySelectorAll("[data-tag]").forEach((node) => {
          node.onclick = () => lightTag(tags[Number(node.dataset.tag)]);
        });
      } catch (error) {
        if (error === STALE) return;
        pane.innerHTML = `<p class="muted">آرایه‌ها نیامد. ${esc(error.message)}</p>`;
      }
      return;
    }
    if (tab === "kin") {
      pane.innerHTML = `<p class="muted">می‌آورم…</p>`;
      try {
        const qs = `metre=${encodeURIComponent(metre.rhythm)}${rhyme ? `&rhyme=${encodeURIComponent(rhyme)}` : ""}&PageNumber=1&PageSize=9`;
        const { data, total } = await api(`/poems/similar?${qs}`);
        const kin = (Array.isArray(data) ? data : []).filter((item) => item.id !== poem.id).slice(0, 8);
        pane.innerHTML =
          `<p class="muted">شعرهایی با همین وزن${rhyme ? " و قافیه" : ""}${total ? ` · ${Math.max(total - 1, 0)} شعر` : ""}. جای خوبی برای پیدا کردن استقبال و جواب.</p>` +
          (kin.length
            ? kin
                .map((item) => {
                  const first = String(item.plainText || "").split(/\r?\n/).find((line) => line.trim()) || "";
                  return `<a class="hit" href="#/poem/${item.id}"><div class="kicker">${esc(String(item.fullTitle || "").split("»")[0])}</div><strong>${esc(item.title)}</strong><p>${esc(first)}</p></a>`;
                })
                .join("")
            : `<p class="muted">شعر دیگری با همین وزن و قافیه پیدا نشد.</p>`) +
          `<p><a href="#/vazn?id=${metre.id}">همه شعرهای این وزن</a></p>`;
      } catch (error) {
        if (error === STALE) return;
        pane.innerHTML = `<p class="muted">${esc(error.message)}</p>`;
      }
      return;
    }
    pane.innerHTML = `<p class="muted">می‌آورم…</p>`;
    try {
      if (tab === "music") {
        const { data } = await api(`/poem/${poem.id}?songs=true&verseDetails=false&recitations=false&comments=false&images=false&navigation=false&catInfo=false`);
        const songs = data.songs || [];
        pane.innerHTML = songs.length
          ? songs
              .slice(0, 8)
              .map(
                (song) =>
                  `<p><a href="${esc(song.trackUrl)}" rel="noreferrer">${esc(song.artistName || "قطعه")} — ${esc(song.trackName || song.albumName || "")}</a></p>`,
              )
              .join("")
          : `<p class="muted">قطعه موسیقی ثبت نشده.</p>`;
      }
      if (tab === "margin") {
        const { data } = await api(`/poem/${poem.id}?comments=true&verseDetails=false&recitations=false&songs=false&images=false&navigation=false&catInfo=false`);
        const comments = (data.comments || [])
          .filter((item) => item.coupletIndex == null || item.coupletIndex === -1 || item.coupletIndex === activeCouplet)
          .slice(0, 6);
        const rows = comments
          .map((item) => {
            const box = document.createElement("div");
            box.innerHTML = item.htmlComment || "";
            return `<article class="card"><div class="kicker">${esc(item.authorName || "خواننده")}</div><p>${esc(box.textContent || "")}</p></article>`;
          })
          .join("");
        pane.innerHTML =
          (rows || `<p class="muted">حاشیه‌ای برای این بیت نیست.</p>`) +
          `<p><a href="https://ganjoor.net${esc(poem.fullUrl)}" rel="noreferrer">نوشتن حاشیه در گنجور</a></p>`;
      }
    } catch (error) {
      pane.innerHTML = `<p class="muted">این بخش نیامد. ${esc(error.message)}</p>`;
    }
  }
  document.querySelector("#tabs").onclick = (event) => {
    const button = event.target.closest("[data-tab]");
    if (!button) return;
    tab = button.dataset.tab;
    renderPane();
  };
  document.querySelector("#verses").onclick = async (event) => {
    const word = event.target.closest(".word");
    const verse = event.target.closest(".verse");
    if (!verse) return;
    activeCouplet = Number(verse.dataset.couplet);
    markCouplet();
    openSheet();
    if (word) {
      tab = "mirror";
      const term = bare(word.textContent || "");
      pane.innerHTML = `<p class="muted">می‌گردم…</p>`;
      document.querySelectorAll("#tabs .chip").forEach((node) => node.classList.toggle("on", node.dataset.tab === "mirror"));
      try {
        const poetFilter = poet.id ? `&poetId=${poet.id}` : "";
        const { data, total } = await api(`/poems/search?term=${encodeURIComponent(term)}&pageNumber=1&pageSize=5${poetFilter}`);
        const hits = (Array.isArray(data) ? data : [])
          .map((item) => {
            const first = String(item.plainText || "").split(/\r?\n/).find((line) => line.trim()) || "";
            return `<a class="hit" href="#/poem/${item.id}"><strong>${esc(item.title)}</strong><p>${esc(first)}</p></a>`;
          })
          .join("");
        pane.innerHTML = `<p>واژه «${esc(term)}» در آثار ${esc(poet.nickname || poet.name || "این شاعر")}${total ? `، ${total} شعر` : ""}</p>${hits || `<p class="muted">در آثار همین شاعر نیامد.</p>`}<p><a href="#/search?q=${encodeURIComponent(term)}">در همه گنجور</a></p>`;
      } catch (error) {
        pane.innerHTML = `<p class="muted">${esc(error.message)}</p>`;
      }
      return;
    }
    if (!["device", "margin"].includes(tab)) tab = "mean";
    renderPane();
  };
  markCouplet();
  renderPane();
  document.querySelector("#mark").onclick = (event) => {
    store.toggle(poem.id);
    const on = store.get().marks.includes(poem.id);
    event.currentTarget.textContent = on ? "★ نشان شد" : "☆ نشان";
    event.currentTarget.setAttribute("aria-pressed", String(on));
  };
  document.querySelector("#quiet").onclick = () => {
    location.hash = quiet ? `#/poem/${poem.id}` : `#/poem/${poem.id}?quiet=1`;
  };
  document.querySelector("#note").onchange = (event) => store.note(poem.id, event.target.value);
  const player = document.querySelector("#player");
  const picker = document.querySelector("#reciter");
  if (player && picker) {
    audioNode = player;
    let times = [];
    async function loadSync(rec) {
      times = [];
      const note = document.querySelector("#sync-note");
      if (!rec.inSyncWithText || !rec.xmlText) {
        if (note) note.textContent = rec.audioArtist ? `خوانش ${rec.audioArtist}` : "";
        return;
      }
      try {
        const xml = await fetch(rec.xmlText.startsWith("http") ? rec.xmlText : `https://api.ganjoor.net${rec.xmlText}`).then((response) => response.text());
        times = [...xml.matchAll(/<VerseOrder>(\d+)<\/VerseOrder>\s*<AudioMiliseconds>(\d+)/g)].map((match) => ({
          order: Number(match[1]),
          at: Number(match[2]),
        }));
        if (note) note.textContent = "بیت با صدای خواننده پیش می‌رود.";
      } catch {
        if (note) note.textContent = "صوت هست؛ هم‌زمانی بیت‌ها نیامد.";
      }
    }
    picker.onchange = () => {
      const rec = recitations[Number(picker.value)];
      player.src = rec.mp3Url;
      loadSync(rec);
    };
    player.ontimeupdate = () => {
      if (!times.length) return;
      const now = player.currentTime * 1000;
      let order = times[0].order;
      for (const mark of times) if (mark.at <= now) order = mark.order;
      document.querySelectorAll(".verse").forEach((node) => {
        const on = Number(node.dataset.order) === order;
        if (on && !node.classList.contains("on")) node.scrollIntoView({ block: "nearest" });
        node.classList.toggle("on", on);
      });
    };
    const listen = document.querySelector("#listen");
    const syncListen = () => {
      if (!listen) return;
      listen.textContent = player.paused ? "▶ گوش بده" : "❚❚ مکث";
      listen.setAttribute("aria-pressed", String(!player.paused));
    };
    if (listen) listen.onclick = () => (player.paused ? player.play() : player.pause());
    player.onplay = syncListen;
    player.onpause = syncListen;
    player.onended = syncListen;
    loadSync(recitations[0]);
  }
}

async function searchPage(query) {
  const q = (query.get("q") || "").trim();
  const pageNo = Math.max(1, Number(query.get("p") || 1));
  const poetId = Number(query.get("poet") || 0);
  const poetPart = poetId ? `&poet=${poetId}` : "";
  if (!q) {
    paint(
      "جستجو",
      `<h1>جستجو</h1><p class="lead">یک واژه یا تکه‌ای از بیت را بنویس.</p>
       <form class="big-search" id="page-search"><input name="q" placeholder="مثلاً سرو، یا: بشنو از نی" aria-label="جستجو" autofocus /><button class="btn primary" type="submit">جستجو</button></form>
       <p class="chips">${["بشنو از نی", "سرو", "مستی", "توانا بود", "رند"].map((word) => `<a class="chip" href="#/search?q=${encodeURIComponent(word)}">${word}</a>`).join("")}</p>`,
    );
    if (input) input.value = "";
    document.querySelector("#page-search").onsubmit = (event) => {
      event.preventDefault();
      const value = String(new FormData(event.currentTarget).get("q") || "").trim();
      if (value) location.hash = `#/search?q=${encodeURIComponent(value)}`;
    };
    return;
  }
  loading("جستجو");
  const { data, total } = await api(`/poems/search?term=${encodeURIComponent(q)}&pageNumber=${pageNo}&pageSize=8${poetId ? `&poetId=${poetId}` : ""}`);
  const rows = (Array.isArray(data) ? data : [])
    .map((poem) => {
      const first = String(poem.plainText || "")
        .split(/\r?\n/)
        .map((line) => line.trim())
        .filter(Boolean)
        .slice(0, 2)
        .join(" / ");
      const poet = poem.category?.poet;
      return `<a class="hit" href="#/poem/${poem.id}"><div class="kicker">${esc(poet?.nickname || poet?.name || "")}</div><strong>${esc(poem.fullTitle || poem.title)}</strong><p>${esc(first)}</p></a>`;
    })
    .join("");
  const pages = total ? Math.ceil(total / 8) : 0;
  paint(
    "جستجو",
    `<h1>جستجو</h1>
     <p class="lead">نتیجه «${esc(q)}»${poetId ? " در آثار یک شاعر" : ""}${total ? ` · ${total} شعر` : ""}</p>
     <p class="chips"><a class="chip" href="#/words?q=${encodeURIComponent(q)}">بسامد این واژه نزد شاعران</a>${poetId ? `<a class="chip" href="#/search?q=${encodeURIComponent(q)}">در همه گنجور</a>` : ""}</p>
     ${rows ? `<div class="grid">${rows}</div>` : `<p>چیزی پیدا نشد.</p>`}
     ${pages > 1 ? `<p class="chips">${pageNo > 1 ? `<a class="chip" href="#/search?q=${encodeURIComponent(q)}${poetPart}&p=${pageNo - 1}">قبلی</a>` : ""}<span class="chip">${pageNo} از ${pages}</span>${pageNo < pages ? `<a class="chip" href="#/search?q=${encodeURIComponent(q)}${poetPart}&p=${pageNo + 1}">بعدی</a>` : ""}</p>` : ""}`,
  );
  if (input) input.value = q;
}

// A map you first see whole, then wander in: drag to pan, wheel or two fingers to zoom.
// Pins keep one screen size; labels that would collide are hidden, biggest first wins.
function atlasStage(atlas) {
  const stage = document.createElement("div");
  stage.className = "atlas-stage";
  stage.tabIndex = 0;
  stage.setAttribute("aria-label", "نقشه؛ با کشیدن جابه‌جا شو، با چرخ یا دو انگشت بزرگ‌نمایی کن، صفر برای نمای کل");
  atlas.replaceWith(stage);
  stage.append(atlas);
  stage.insertAdjacentHTML(
    "beforeend",
    `<div class="stage-ctl" role="toolbar" aria-label="بزرگ‌نمایی"><button type="button" data-zoom="in" aria-label="بزرگ‌تر">+</button><button type="button" data-zoom="out" aria-label="کوچک‌تر">−</button><button type="button" data-zoom="fit">نمای کل</button></div>`,
  );
  let k = 1;
  let tx = 0;
  let ty = 0;
  let frame = 0;
  const size = () => ({ w: stage.clientWidth || 1, h: stage.clientHeight || 1 });
  const clamp = () => {
    const { w, h } = size();
    k = Math.min(Math.max(k, 1), 8);
    tx = Math.min(0, Math.max(w - w * k, tx));
    ty = Math.min(0, Math.max(h - h * k, ty));
  };
  const declutter = () => {
    const box = stage.getBoundingClientRect();
    // a label may not cover another label or another city's dot
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
  const render = () => {
    clamp();
    atlas.style.transform = `translate(${tx.toFixed(1)}px,${ty.toFixed(1)}px) scale(${k.toFixed(4)})`;
    atlas.style.setProperty("--inv", (1 / k).toFixed(4));
    stage.classList.toggle("zoomed", k > 1.02);
    declutter();
  };
  const draw = () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(render);
  };
  const zoomAt = (sx, sy, factor) => {
    const next = Math.min(Math.max(k * factor, 1), 8);
    tx = sx - ((sx - tx) * next) / k;
    ty = sy - ((sy - ty) * next) / k;
    k = next;
    draw();
  };
  const pointers = new Map();
  let travelled = 0;
  let pinch = 0;
  stage.addEventListener("pointerdown", (event) => {
    if (event.target.closest(".stage-ctl")) return;
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    travelled = 0;
    if (pointers.size === 2) {
      const [a, b] = [...pointers.values()];
      pinch = Math.hypot(a.x - b.x, a.y - b.y);
    }
  });
  stage.addEventListener("pointermove", (event) => {
    const last = pointers.get(event.pointerId);
    if (!last) return;
    const now = { x: event.clientX, y: event.clientY };
    const box = stage.getBoundingClientRect();
    if (pointers.size === 1) {
      travelled += Math.abs(now.x - last.x) + Math.abs(now.y - last.y);
      if (travelled > 6) {
        if (!stage.hasPointerCapture(event.pointerId)) stage.setPointerCapture(event.pointerId);
        stage.classList.add("grab");
        tx += now.x - last.x;
        ty += now.y - last.y;
        draw();
      }
      pointers.set(event.pointerId, now);
    } else if (pointers.size === 2) {
      pointers.set(event.pointerId, now);
      const [a, b] = [...pointers.values()];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      travelled += 20;
      if (pinch > 0) zoomAt((a.x + b.x) / 2 - box.left, (a.y + b.y) / 2 - box.top, d / pinch);
      pinch = d;
    }
  });
  const lift = (event) => {
    pointers.delete(event.pointerId);
    if (pointers.size < 2) pinch = 0;
    if (!pointers.size) stage.classList.remove("grab");
  };
  stage.addEventListener("pointerup", lift);
  stage.addEventListener("pointercancel", lift);
  // a drag must not count as a click on a pin
  stage.addEventListener(
    "click",
    (event) => {
      if (travelled > 6 && !event.target.closest(".stage-ctl")) {
        event.preventDefault();
        event.stopPropagation();
      }
    },
    true,
  );
  stage.addEventListener(
    "wheel",
    (event) => {
      event.preventDefault();
      const box = stage.getBoundingClientRect();
      zoomAt(event.clientX - box.left, event.clientY - box.top, Math.exp(-event.deltaY * (event.ctrlKey ? 0.01 : 0.0018)));
    },
    { passive: false },
  );
  stage.addEventListener("dblclick", (event) => {
    event.preventDefault();
    const box = stage.getBoundingClientRect();
    zoomAt(event.clientX - box.left, event.clientY - box.top, 2);
  });
  const reset = () => {
    k = 1;
    tx = 0;
    ty = 0;
    draw();
  };
  stage.querySelector(".stage-ctl").addEventListener("click", (event) => {
    const button = event.target.closest("[data-zoom]");
    if (!button) return;
    const { w, h } = size();
    if (button.dataset.zoom === "in") zoomAt(w / 2, h / 2, 1.6);
    else if (button.dataset.zoom === "out") zoomAt(w / 2, h / 2, 1 / 1.6);
    else reset();
  });
  stage.addEventListener("keydown", (event) => {
    const { w, h } = size();
    const moves = { ArrowLeft: [80, 0], ArrowRight: [-80, 0], ArrowUp: [0, 80], ArrowDown: [0, -80] };
    if (moves[event.key]) {
      event.preventDefault();
      tx += moves[event.key][0];
      ty += moves[event.key][1];
      draw();
    } else if (event.key === "+" || event.key === "=") zoomAt(w / 2, h / 2, 1.4);
    else if (event.key === "-") zoomAt(w / 2, h / 2, 1 / 1.4);
    else if (event.key === "0" || event.key === "۰") reset();
  });
  const watch = new ResizeObserver(() => (document.body.contains(stage) ? draw() : watch.disconnect()));
  watch.observe(stage);
  // fly to a point given in percent of the map
  const focusOn = (px, py, zoom = 2.6) => {
    const { w, h } = size();
    k = Math.max(k, zoom);
    tx = w / 2 - (px / 100) * w * k;
    ty = h / 2 - (py / 100) * h * k;
    draw();
  };
  draw();
  document.fonts?.ready.then(draw);
  return { refresh: draw, reset, focusOn };
}

async function mapPage(query) {
  loading("نقشه");
  const { data: poets } = await api("/poets");
  const placed = poets.filter((poet) => poet.birthPlaceLatitude && poet.birthPlaceLongitude && poet.birthYearInLHijri && poet.deathYearInLHijri);
  const min = Math.min(...placed.map((poet) => poet.birthYearInLHijri));
  const max = Math.max(...placed.map((poet) => poet.deathYearInLHijri));
  let year = Number(query.get("y") || 750);
  if (year < min) year = min;
  if (year > max) year = max;

  // every birthplace of every age, so the whole picture is always there in faint
  const cities = new Map();
  for (const poet of placed) {
    const point = project(poet.birthPlaceLongitude, poet.birthPlaceLatitude);
    if (point.x < 0 || point.x > 100 || point.y < 0 || point.y > 100) continue;
    const city = cityOf(poet);
    if (!cities.has(city)) cities.set(city, point);
  }
  const ghosts = [...cities.values()].map((point) => `<i class="ghost" style="left:${point.x}%;top:${point.y}%"></i>`).join("");

  // how many poets were alive in each decade, drawn behind the slider
  const decades = [];
  for (let y = Math.floor(min / 10) * 10; y <= max; y += 10) decades.push({ y, n: placed.filter((poet) => poet.birthYearInLHijri <= y + 5 && poet.deathYearInLHijri >= y + 5).length });
  const peak = Math.max(1, ...decades.map((item) => item.n));
  const spark = `<svg class="spark" viewBox="0 0 1000 40" preserveAspectRatio="none" aria-hidden="true"><path d="M0,40 ${decades
    .map((item) => `L${(((item.y + 5 - min) / (max - min)) * 1000).toFixed(1)},${(40 - (item.n / peak) * 36).toFixed(1)}`)
    .join(" ")} L1000,40 Z"/></svg>`;
  const ticks = [];
  for (let mark = Math.ceil(min / 100) * 100; mark < max; mark += 100) ticks.push(mark);

  paint(
    "نقشه",
    `<h1>هم‌عصران</h1>
     <p class="lead">هر سال را که برگزینی، شاعرانی که آن سال زنده بودند در زادگاهشان روشن می‌شوند. نقطه‌های کم‌رنگ زادگاه همه شاعران همه دوره‌هاست. اندازه نقطه، شمار شاعران زنده آن شهر است. بکش، بزرگ کن، یا دکمه پخش را بزن تا زمان راه بیفتد.</p>
     <div class="year">
       <div class="year-top"><button type="button" class="play" id="play" aria-label="پخش">▶</button><span>سفر در زمان</span><strong id="year-label"></strong></div>
       <div class="scale">${spark}
         <input id="year" type="range" min="${min}" max="${max}" value="${year}" aria-label="سال هجری" />
         <div class="ticks">${ticks.map((mark) => `<span class="${mark % 200 ? "minor" : ""}" style="left:${((mark - min) / (max - min)) * 100}%">${mark}</span>`).join("")}</div>
       </div>
     </div>
     <div class="atlas realm" id="atlas" aria-label="گستره شهرهای شعر فارسی"><div class="ghosts">${ghosts}</div><div id="pins"></div></div>
     <p class="muted" id="alive-count"></p>
     <div class="grid" id="city-list"></div>
     <div id="far"></div>`,
  );
  const atlas = document.querySelector("#atlas");
  const view = atlasStage(atlas);
  const pinsBox = document.querySelector("#pins");
  const slider = document.querySelector("#year");
  const label = document.querySelector("#year-label");
  const count = document.querySelector("#alive-count");
  const list = document.querySelector("#city-list");
  const farBox = document.querySelector("#far");

  const drawYear = (value) => {
    year = Number(value);
    const alive = placed.filter((poet) => poet.birthYearInLHijri <= year && poet.deathYearInLHijri >= year);
    const groups = new Map();
    const far = [];
    for (const poet of alive) {
      const point = project(poet.birthPlaceLongitude, poet.birthPlaceLatitude);
      if (point.x < 0 || point.x > 100 || point.y < 0 || point.y > 100) {
        far.push(poet);
        continue;
      }
      const city = cityOf(poet);
      const group = groups.get(city) || { city, x: point.x, y: point.y, poets: [], noted: city === "توس" };
      group.poets.push(poet);
      groups.set(city, group);
    }
    const most = Math.max(1, ...[...groups.values()].map((group) => group.poets.length));
    label.textContent = `سال ${yr(year)} هجری · حدود ${yr(toGregorian(year))} میلادی`;
    pinsBox.innerHTML = [...groups.values()]
      .map((group, index) => {
        const people = group.poets.map((poet) => poet.nickname || poet.name).join("، ");
        const note = group.noted ? " — گنجور مشهد نوشته" : "";
        const size = Math.round(10 + Math.sqrt(group.poets.length / most) * 16);
        const n = group.poets.length;
        return `<a class="pin" data-city="${index}" data-w="${n}" style="left:${group.x}%;top:${group.y}%" href="#/map?y=${year}" title="${esc(group.city)}: ${esc(people)}${esc(note)}"><span>${esc(group.city)}${n > 1 ? ` <b>${fa(n)}</b>` : ""}</span><i style="width:${size}px;height:${size}px"></i></a>`;
      })
      .join("") || `<p class="muted empty-map">در این سال کسی در این گستره نیست.</p>`;
    count.textContent = `${fa(alive.length)} شاعر در این سال، در ${fa(groups.size)} شهر این گستره.`;
    list.innerHTML = [...groups.values()]
      .map(
        (group, index) =>
          `<article class="card" id="city-${index}"><strong>${esc(group.city)}</strong>${group.noted ? `<p class="muted">گنجور این زادگاه را مشهد نوشته. در روزگار این شاعران شهر توس بوده، کنار همان نقطه.</p>` : ""}<p class="chips">${group.poets
            .map((poet) => `<a class="chip" href="#/poet/${poet.id}">${esc(poet.nickname || poet.name)}</a>`)
            .join("")}</p></article>`,
      )
      .join("");
    farBox.innerHTML = far.length
      ? `<p class="muted">زادگاه این‌ها دورتر است، در هند یا آناتولی یا شام، و روی این صفحه جا نشده:</p><div class="chips">${far.map((poet) => `<a class="chip" href="#/poet/${poet.id}">${esc(poet.nickname || poet.name)} · ${esc(poet.birthPlace || "")}</a>`).join("")}</div>`
      : "";
    history.replaceState(null, "", `#/map?y=${year}`);
    view.refresh();
  };

  let timer = 0;
  const play = document.querySelector("#play");
  const stop = () => {
    clearInterval(timer);
    timer = 0;
    play.textContent = "▶";
    play.setAttribute("aria-label", "پخش");
  };
  play.onclick = () => {
    if (timer) return stop();
    if (year >= max - 5) slider.value = min;
    play.textContent = "❚❚";
    play.setAttribute("aria-label", "ایست");
    timer = setInterval(() => {
      if (!document.body.contains(play)) return stop();
      const next = Math.min(max, Number(slider.value) + 5);
      slider.value = next;
      drawYear(next);
      if (next >= max) stop();
    }, 180);
  };
  slider.oninput = () => {
    stop();
    drawYear(slider.value);
  };
  pinsBox.addEventListener("click", (event) => {
    const pin = event.target.closest(".pin[data-city]");
    if (!pin) return;
    event.preventDefault();
    const card = document.getElementById(`city-${pin.dataset.city}`);
    card?.scrollIntoView({ block: "nearest", behavior: "smooth" });
    card?.classList.add("flash");
    setTimeout(() => card?.classList.remove("flash"), 1200);
  });
  drawYear(year);
}

async function libraryPage() {
  const data = store.get();
  const block = async (ids, empty) => {
    if (!ids.length) return `<p class="muted">${empty}</p>`;
    const cards = await Promise.all(
      ids.slice(0, 12).map(async (id) => {
        try {
          const { data: poem } = await api(`/poem/${id}?catInfo=true&verseDetails=false&recitations=false&navigation=false&comments=false&images=false&songs=false`);
          const poet = poem.category?.poet;
          return `<a class="card" href="#/poem/${id}"><div class="kicker">${esc(poet?.nickname || "")}</div><strong>${esc(poem.title)}</strong></a>`;
        } catch (error) {
          if (error === STALE) throw error;
          return "";
        }
      }),
    );
    return `<div class="grid">${cards.join("")}</div>`;
  };
  loading("کتابخانه");
  const notes = Object.entries(data.notes).filter(([, text]) => String(text).trim());
  const [marksHtml, historyHtml] = await Promise.all([
    block(data.marks, "هنوز شعری را نشان نکرده‌ای. در صفحه هر شعر دکمه «نشان» را بزن."),
    block(data.history, "هنوز شعری نخوانده‌ای."),
  ]);
  const noteHtml = notes.length
    ? `<div class="grid">${notes
        .slice(0, 12)
        .map(([id, text]) => `<article class="card"><a href="#/poem/${id}">یادداشت شعر</a><p class="muted">${esc(text)}</p></article>`)
        .join("")}</div>`
    : `<p class="muted">یادداشتی نیست.</p>`;
  paint(
    "کتابخانه",
    `<h1>کتابخانه من</h1>
     <p class="lead">نشان و یادداشت فقط روی همین دستگاه می‌ماند.</p>
     <div class="stats"><div class="stat"><b>${data.marks.length}</b>نشان</div><div class="stat"><b>${notes.length}</b>یادداشت</div><div class="stat"><b>${data.history.length}</b>خوانده‌شده</div></div>
     <h2 class="section">نشان‌ها</h2>${marksHtml}
     <h2 class="section">یادداشت‌ها</h2>${noteHtml}
     <h2 class="section">خاطره‌نگار</h2>${historyHtml}`,
  );
}

async function bridgesPage(id) {
  loading("پل‌ها");
  const [{ data }, { data: quoted }] = await Promise.all([api(`/poet/${id}`), api(`/quoted?poetId=${id}&published=true`)]);
  const poet = data.poet;
  const links = new Map();
  for (const item of Array.isArray(quoted) ? quoted : []) {
    if (!item.relatedPoetId || item.relatedPoetId === poet.id || item.rejected) continue;
    const row = links.get(item.relatedPoetId) || {
      id: item.relatedPoetId,
      name: item.cachedRelatedPoemPoetName || "شاعر",
      died: item.cachedRelatedPoemPoetDeathYearInLHijri || 0,
      n: 0,
      before: 0,
      after: 0,
      both: 0,
      samples: [],
    };
    row.n += 1;
    if (item.isPriorToRelated) row.before += 1;
    else row.after += 1;
    if (item.claimedByBothPoets) row.both += 1;
    if (row.samples.length < 3)
      row.samples.push({
        mine: item.poemId,
        theirs: item.relatedPoemId,
        line: [item.coupletVerse1, item.coupletVerse2].filter(Boolean).join(" / "),
        other: [item.relatedCoupletVerse1, item.relatedCoupletVerse2].filter(Boolean).join(" / "),
        title: item.cachedRelatedPoemFullTitle || "",
      });
    links.set(item.relatedPoetId, row);
  }
  const rows = [...links.values()].sort((a, b) => b.n - a.n);
  // every linked poet on one time axis: bubbles above (area = links), arcs below (who came first)
  const most = Math.max(1, ...rows.map((row) => row.n));
  const own = poet.deathYearInLHijri || 0;
  const dated = rows.filter((row) => row.died);
  const undated = rows.filter((row) => !row.died);
  const years = [...dated.map((row) => row.died), ...(own ? [own] : [])];
  const lo = Math.floor((Math.min(...years, own || Infinity) - 20) / 50) * 50;
  const hi = Math.ceil((Math.max(...years, own || -Infinity) + 20) / 50) * 50;
  const GW = Math.round(Math.min(1000, Math.max(540, (root.clientWidth || 1000) * 1.5)));
  const AXIS = 330;
  const EDGE = 40;
  const span = undated.length ? GW - EDGE * 2 - 70 : GW - EDGE * 2;
  const gx = (year) => GW - EDGE - ((year - lo) / Math.max(1, hi - lo)) * span;
  const radius = (row) => 4 + Math.sqrt(row.n / most) * 20;
  const tone = (row) => (row.before && !row.after ? "late" : row.after && !row.before ? "early" : "both");
  const placedB = [];
  const bubbles = [...rows]
    .sort((a, b) => b.n - a.n)
    .map((row) => {
      const r = radius(row);
      const cx = row.died ? gx(row.died) : EDGE + 30;
      let cy = AXIS - r - 6;
      for (let tries = 0; tries < 400; tries++) {
        if (!placedB.some((o) => Math.hypot(o.cx - cx, o.cy - cy) < o.r + r + 2)) break;
        cy -= 2;
      }
      const item = { ...row, r, cx, cy };
      placedB.push(item);
      return item;
    });
  const ox = own ? gx(own) : GW / 2;
  // a name is written only where it covers no other name and no other bubble; the rest show on hover
  const boxes = [{ l: ox - 60, r: ox + 60, t: AXIS - 34, b: AXIS - 6 }];
  const meets = (a, b) => a.l < b.r && a.r > b.l && a.t < b.b && a.b > b.t;
  const hitsBubble = (box, self) => bubbles.some((o) => o !== self && o.cx + o.r * 0.7 > box.l && o.cx - o.r * 0.7 < box.r && o.cy + o.r * 0.7 > box.t && o.cy - o.r * 0.7 < box.b);
  const labels = new Map();
  for (const item of bubbles.slice(0, 30)) {
    const text = `${item.name} ${fa(item.n)}`;
    const wide = text.length * 6.6 + 4;
    const spots = [
      { x: item.cx - item.r - 3, y: item.cy + 4 },
      { x: item.cx + item.r + 3 + wide, y: item.cy + 4 },
      { x: item.cx + wide / 2, y: item.cy - item.r - 5 },
      { x: item.cx - item.r * 0.5, y: item.cy - item.r * 0.7 - 2 },
      { x: item.cx + item.r * 0.5 + wide, y: item.cy - item.r * 0.7 - 2 },
    ];
    for (const spot of spots) {
      const x = spot.x;
      const box = { l: x - wide, r: x, t: spot.y - 13, b: spot.y + 3 };
      if (box.l < 2 || box.r > GW - 2) continue;
      if (boxes.some((o) => meets(o, box)) || hitsBubble(box, item)) continue;
      boxes.push(box);
      labels.set(item.id, { x, y: spot.y, text });
      break;
    }
  }
  // the biggest names that found no room get a callout above the swarm, with a thin leader line
  const swarmTop = Math.min(...bubbles.map((item) => item.cy - item.r));
  const rowsY = [swarmTop - 14, swarmTop - 34, swarmTop - 54];
  const callouts = [];
  for (const item of bubbles.slice(0, 10)) {
    if (labels.has(item.id)) continue;
    const text = `${item.name} ${fa(item.n)}`;
    const wide = text.length * 6.6 + 4;
    for (const y of rowsY) {
      const x = Math.min(GW - 4, Math.max(wide + 4, item.cx + wide / 2));
      const box = { l: x - wide, r: x, t: y - 13, b: y + 3 };
      if (boxes.some((o) => meets(o, box))) continue;
      boxes.push(box);
      callouts.push({ x, y, text, cx: item.cx, cy: item.cy - item.r });
      break;
    }
  }
  const gTicks = [];
  for (let year = lo; year <= hi; year += hi - lo > 600 ? 100 : 50) gTicks.push(year);
  const top = Math.min(...bubbles.map((item) => item.cy - item.r), ...callouts.map((item) => item.y - 16)) - 10;
  const graph = rows.length
    ? `<div class="bridge-map"><svg class="bridge-svg" viewBox="0 ${top} ${GW} ${AXIS + 150 - top}" role="img" aria-label="پل‌های ${esc(poet.nickname || poet.name)} با ${fa(rows.length)} شاعر روی خط زمان">
        <g class="b-axis">${gTicks.map((year) => `<line x1="${gx(year)}" x2="${gx(year)}" y1="${top}" y2="${AXIS}"/><text x="${gx(year)}" y="${AXIS + 136}">${yr(year)} ق</text>`).join("")}<line class="base" x1="${EDGE}" x2="${GW - EDGE}" y1="${AXIS}" y2="${AXIS}"/></g>
        ${undated.length ? `<text class="b-note" x="${EDGE + 30}" y="${AXIS + 136}">بی‌تاریخ</text>` : ""}
        <g class="b-arcs">${bubbles
          .map((item) => {
            const lift = Math.min(118, 14 + Math.abs(item.cx - ox) * 0.32);
            return `<path class="${tone(item)}" d="M${ox.toFixed(1)},${AXIS} Q${((ox + item.cx) / 2).toFixed(1)},${(AXIS + lift * 2).toFixed(1)} ${item.cx.toFixed(1)},${AXIS}" style="stroke-width:${(0.8 + (item.n / most) * 5).toFixed(1)}"/>`;
          })
          .join("")}</g>
        <g class="b-dots">${bubbles
          .map(
            (item) =>
              `<a href="#/bridges/${item.id}"><circle class="${tone(item)}" cx="${item.cx.toFixed(1)}" cy="${item.cy.toFixed(1)}" r="${item.r.toFixed(1)}"><title>${esc(item.name)} · ${fa(item.n)} پیوند${item.died ? ` · درگذشت ${yr(item.died)} ق` : ""}</title></circle>${labels.has(item.id) ? `<text x="${labels.get(item.id).x.toFixed(1)}" y="${labels.get(item.id).y.toFixed(1)}">${esc(labels.get(item.id).text)}</text>` : ""}</a>`,
          )
          .join("")}</g>
        <g class="b-call">${callouts.map((item) => `<line x1="${item.cx.toFixed(1)}" x2="${item.cx.toFixed(1)}" y1="${(item.y + 4).toFixed(1)}" y2="${item.cy.toFixed(1)}"/><text x="${item.x.toFixed(1)}" y="${item.y.toFixed(1)}">${esc(item.text)}</text>`).join("")}</g>
        <g class="b-self"><line x1="${ox}" x2="${ox}" y1="${AXIS - 8}" y2="${AXIS + 8}"/><circle cx="${ox}" cy="${AXIS}" r="7"/><text x="${ox}" y="${AXIS - 14}">${esc(poet.nickname || poet.name)}</text></g>
      </svg></div>
      <p class="key muted b-key"><span class="sw late"></span> شعر ${esc(poet.nickname || poet.name)} پیش‌تر ثبت شده <span class="sw early"></span> شعر آن شاعر پیش‌تر است <span class="sw both"></span> هر دو سو. هر حباب یک شاعر است در سال درگذشتش؛ مساحت حباب و ضخامت کمان، شمار پیوندهاست. روی حباب بزن تا پل‌های آن شاعر باز شود.</p>`
    : "";
  const direction = (row) => {
    if (row.before && !row.after) return `${esc(poet.nickname || poet.name)} پیش‌تر است`;
    if (row.after && !row.before) return `${esc(row.name)} پیش‌تر است`;
    return "دوسویه";
  };
  paint(
    "پل‌ها",
    `<p class="crumb"><a href="#/poet/${poet.id}">${esc(poet.nickname || poet.name)}</a></p>
     <h1>پل‌های ثبت‌شده</h1>
     <p class="lead">همه تضمین‌ها و بیت‌های مشترکی که گنجور برای ${esc(poet.nickname || poet.name)} ثبت و منتشر کرده: ${fa(quoted.length)} پیوند با ${fa(rows.length)} شاعر. همه روی خط زمان: چه کسانی پیش از او بودند و چه کسانی پس از او.</p>
     ${graph}
     ${
       rows.length
         ? `<div class="grid">${rows
             .map(
               (row) =>
                 `<article class="card"><div class="kicker">${fa(row.n)} پیوند · ${direction(row)}${row.both ? ` · ${fa(row.both)} بیت در دیوان هر دو` : ""}</div><strong><a href="#/bridges/${row.id}">${esc(row.name)}</a></strong>${row.samples
                   .map(
                     (sample) =>
                       `<p><a href="#/poem/${sample.mine}">${esc(sample.line)}</a>${sample.other && sample.other !== sample.line ? `<br><a class="muted" href="#/poem/${sample.theirs}">${esc(sample.other)}</a>` : ""}</p>`,
                   )
                   .join("")}</article>`,
             )
             .join("")}</div>`
         : `<p>برای این شاعر تضمین یا بیت مشترکی منتشر نشده.</p>`
     }
     <p class="muted">«پیش‌تر» یعنی شعر کدام شاعر در گنجور مقدم ثبت شده است. استقبال‌ها (هم‌وزن و هم‌قافیه) را در زبانه «هم‌وزن» صفحه هر شعر ببین.</p>
     <p><a class="chip" href="#/poet/${poet.id}">بازگشت به شاعر</a></p>`,
  );
  const map = document.querySelector(".bridge-map");
  if (map) {
    atlasStage(map);
    map.parentElement.classList.add("bridge-stage");
  }
}

async function vaznPage(query) {
  loading("وزن");
  const { data } = await api("/rhythms?sortOnVerseCount=true");
  const selected = Number(query.get("id") || 0);
  const pageNo = Math.max(1, Number(query.get("p") || 1));
  const rhythms = [...data].sort((a, b) => b.verseCount - a.verseCount);
  const current = rhythms.find((item) => item.id === selected);
  let poemsHtml = "";
  if (current) {
    const size = 12;
    const { data: poems, total } = await api(`/poems/similar?metre=${encodeURIComponent(current.rhythm)}&PageNumber=${pageNo}&PageSize=${size}`);
    const list = Array.isArray(poems) ? poems : [];
    const pages = total ? Math.ceil(total / size) : list.length === size ? pageNo + 1 : pageNo;
    poemsHtml = `<h2 class="section">شعرهای این وزن${total ? ` · ${fa(total)}` : ""}</h2>
      <div class="grid">${list
        .map((item) => {
          const first = String(item.plainText || "").split(/\r?\n/).filter((line) => line.trim()).slice(0, 2).join(" / ");
          return `<a class="hit" href="#/poem/${item.id}"><div class="kicker">${esc(String(item.fullTitle || "").split("»")[0])}</div><strong>${esc(item.title)}</strong><p>${esc(first)}</p></a>`;
        })
        .join("")}</div>
      <p class="chips">${pageNo > 1 ? `<a class="chip" href="#/vazn?id=${selected}&p=${pageNo - 1}">قبلی</a>` : ""}<span class="chip">صفحه ${pageNo}${total ? ` از ${pages}` : ""}</span>${pageNo < pages ? `<a class="chip" href="#/vazn?id=${selected}&p=${pageNo + 1}">بعدی</a>` : ""}</p>`;
  }
  const most = Math.max(1, ...rhythms.map((item) => item.verseCount || 0));
  paint(
    "وزن",
    `<h1>وزن‌ها</h1>
     <p class="lead">${fa(rhythms.length)} وزن ثبت‌شده در گنجور. عدد، شمار مصراع‌ها در آن وزن است. وزن را بزن تا شعرهایش بیاید.</p>
     ${current ? `<p class="panel"><strong>${esc(current.rhythm)}</strong><br><span class="muted">${fa(current.verseCount)} مصراع</span></p>${poemsHtml}` : ""}
     <h2 class="section">همه وزن‌ها</h2>
     <form class="big-search" id="vazn-filter"><input id="vazn-q" placeholder="نام بحر یا افاعیل، مثلاً هزج یا مفاعیلن" aria-label="پالایش وزن" /></form>
     <div class="bars" id="vazn-list"></div>`,
  );
  const box = document.querySelector("#vazn-q");
  const list = document.querySelector("#vazn-list");
  const draw = () => {
    const q = box.value.trim();
    const shown = rhythms.filter((item) => !q || item.rhythm.includes(q)).slice(0, q ? 80 : 40);
    list.innerHTML = shown.length
      ? shown
          .map(
            (item) =>
              `<a class="barrow ${item.id === selected ? "on" : ""}" href="#/vazn?id=${item.id}"><span>${esc(item.rhythm)}</span><i style="width:${Math.max(1, (item.verseCount / most) * 100).toFixed(1)}%"></i><b>${fa(item.verseCount)}</b></a>`,
          )
          .join("") + (q ? "" : `<p class="muted">چهل وزن پرکاربرد. برای بقیه نام وزن را بنویس.</p>`)
      : `<p class="muted">وزنی با این نام نیست.</p>`;
  };
  box.oninput = draw;
  document.querySelector("#vazn-filter").onsubmit = (event) => event.preventDefault();
  draw();
}

const REGIONS = [
  { key: "rum", name: "روم و عراق", color: "#7a3b5c" },
  { key: "azar", name: "آذربایجان و غرب", color: "#9a7433" },
  { key: "center", name: "عراق عجم و شمال", color: "#1c39bb" },
  { key: "fars", name: "فارس و کرمان", color: "#b2532f" },
  { key: "khorasan", name: "خراسان و فرارود", color: "#0a6b60" },
  { key: "hind", name: "هند", color: "#5b6b1f" },
  { key: "none", name: "بی‌نشان", color: "#8a8174" },
];

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

const yr = (value) => Number(value || 0).toLocaleString("fa-IR", { useGrouping: false });
const toGregorian = (hijri) => Math.round(hijri * 0.970229 + 621.5643);

function timelinePoets(list) {
  return list
    .filter((poet) => poet.published !== false && (poet.birthYearInLHijri || poet.deathYearInLHijri))
    .map((poet) => {
      let b = poet.birthYearInLHijri || poet.deathYearInLHijri - 60;
      let d = poet.deathYearInLHijri || poet.birthYearInLHijri + 60;
      const broken = d < b;
      if (broken) [b, d] = [d, b];
      return {
        ...poet,
        b,
        d,
        broken,
        sureB: Boolean(poet.birthYearInLHijri && poet.validBirthDate && !broken),
        sureD: Boolean(poet.deathYearInLHijri && poet.validDeathDate && !broken),
        region: regionOf(poet),
        label: poet.nickname || poet.name,
      };
    })
    .sort((x, y) => x.b - y.b || x.d - y.d);
}

function yearsText(poet) {
  return `${poet.birthYearInLHijri ? yr(poet.birthYearInLHijri) : ""}${poet.sureB ? "" : "؟"}–${poet.deathYearInLHijri ? yr(poet.deathYearInLHijri) : ""}${poet.sureD ? "" : "؟"} ق`;
}

async function treePage(query) {
  loading("خط زمان شاعران");
  const [{ data }, learn] = await Promise.all([api("/poets"), local().catch(() => ({}))]);
  const poets = timelinePoets(data);
  const byId = new Map(poets.map((poet) => [String(poet.id), poet]));
  const regionInfo = new Map(REGIONS.map((region) => [region.key, region]));
  const used = REGIONS.filter((region) => poets.some((poet) => poet.region === region.key));

  // content space: time runs right to left, like the reading
  const PX = 0.86;
  const from = Math.floor(Math.min(...poets.map((poet) => poet.b)) / 100) * 100;
  const to = Math.ceil(Math.max(...poets.map((poet) => poet.d)) / 100) * 100;
  const PAD = 18;
  const W = Math.round((to - from) * PX + PAD * 2);
  const x = (year) => W - PAD - (year - from) * PX;
  const yearAt = (cx) => from + (W - PAD - cx) / PX;

  // lanes: each bar plus its name, packed so nothing overlaps
  // names keep one screen size at every zoom, so lanes are packed for the zoom where names appear (KREF)
  const ROW = 14;
  const KREF = 1.4;
  const labelYears = (poet) => (poet.label.length * (poet.pinOrder ? 7.6 : 6.8) + 12) / (PX * KREF);
  const laneEnd = [];
  for (const poet of poets) {
    let lane = laneEnd.findIndex((end) => end < poet.b - 3);
    if (lane < 0) lane = laneEnd.length;
    laneEnd[lane] = poet.d + labelYears(poet);
    poet.lane = lane;
  }
  const H = laneEnd.length * ROW + 16;
  const yOf = (poet) => poet.lane * ROW + 4;

  // how many poets were alive in each decade
  const decades = [];
  for (let year = from; year <= to; year += 10) decades.push({ year, n: poets.filter((poet) => poet.b <= year + 5 && poet.d >= year + 5).length });
  const peak = decades.reduce((best, item) => (item.n > best.n ? item : best), decades[0]);

  // moments in history (data.json, Gregorian) placed on the Hijri axis
  const toHijri = (greg) => Math.round((greg - 621.5643) / 0.970229);
  const eras = (learn.events || []).map((item) => ({ ...item, h: toHijri(item.year) })).filter((item) => item.h >= from && item.h <= to);

  const gradients = used
    .map((region) =>
      [
        ["b", "1", "0.3", "1", "0.6"],
        ["d", "0.3", "1", "0.4", "1"],
        ["bd", "0.3", "0.3", "0.35", "0.65"],
      ]
        .map(
          ([kind, left, right, a, z]) =>
            `<linearGradient id="g-${region.key}-${kind}"><stop offset="0" stop-color="${region.color}" stop-opacity="${left}"/><stop offset="${a}" stop-color="${region.color}"/><stop offset="${z}" stop-color="${region.color}"/><stop offset="1" stop-color="${region.color}" stop-opacity="${right}"/></linearGradient>`,
        )
        .join(""),
    )
    .join("");
  const fill = (poet) => {
    const kind = (poet.sureB ? "" : "b") + (poet.sureD ? "" : "d");
    return kind ? `url(#g-${poet.region}-${kind})` : regionInfo.get(poet.region).color;
  };
  const bar = (poet) => {
    const y = yOf(poet);
    const x1 = x(poet.d);
    const width = Math.max(3, x(poet.b) - x1);
    const strong = poet.pinOrder ? " famous" : "";
    return `<g class="life${strong}" data-id="${poet.id}" data-region="${poet.region}" tabindex="0" role="button" aria-label="${esc(poet.label)}، ${esc(yearsText(poet))}"><title>${esc(poet.name)} · ${esc(yearsText(poet))}${poet.birthPlace ? ` · ${esc(poet.birthPlace)}` : ""}</title><rect class="hit" x="${(x1 - (poet.label.length * 7 + 10) / KREF).toFixed(1)}" y="${y}" width="${(width + (poet.label.length * 7 + 12) / KREF).toFixed(1)}" height="${ROW}"/><rect class="span" x="${x1.toFixed(1)}" y="${y + (poet.pinOrder ? 4 : 5)}" width="${width.toFixed(1)}" height="${poet.pinOrder ? 6 : 4}" rx="2" fill="${fill(poet)}"/><text x="${(x1 - 3).toFixed(1)}" y="${y + 7}">${esc(poet.label)}</text></g>`;
  };
  const centuries = [];
  for (let year = from; year <= to; year += 100) centuries.push(year);
  const MINI_W = 168;
  const MINI_H = Math.max(60, Math.min(120, Math.round((MINI_W * H) / W)));
  const mx = MINI_W / W;
  const my = MINI_H / H;

  const uncertain = poets.filter((poet) => !poet.sureB || !poet.sureD).length;
  paint(
    "خط زمان شاعران",
    `<h1>خط زمان شاعران</h1>
     <p class="lead">زندگی ${fa(poets.length)} شاعر گنجور، همه در یک نگاه. هر نوار از سال تولد تا سال درگذشت است و زمان از راست به چپ می‌رود. بکش تا در زمان گردش کنی، بزرگ کن تا نام‌ها پیدا شوند، و روی یک شاعر بزن تا هم‌عصران و تضمین‌هایش روشن شوند.</p>
     <div class="tree-tools">
       <form class="big-search" id="tree-filter"><input id="tree-q" placeholder="نام شاعر یا شهر، مثلاً شیراز" aria-label="پیدا کردن شاعر" autocomplete="off" /></form>
       <p class="chips" id="tree-regions" aria-label="سرزمین زادگاه"><button class="chip on" type="button" data-region="">همه سرزمین‌ها</button>${used
         .map((region) => `<button class="chip" type="button" data-region="${region.key}" style="--tone:${region.color}"><i class="dot"></i>${region.name} · ${fa(poets.filter((poet) => poet.region === region.key).length)}</button>`)
         .join("")}</p>
     </div>
     <div class="stage" id="stage" tabindex="0" aria-label="خط زمان؛ با کشیدن جابه‌جا شو، با چرخ یا دو انگشت بزرگ‌نمایی کن، دکمه صفر برای نمای کل">
       <svg class="stage-head" id="shead" aria-hidden="true"></svg>
       <svg class="chrono" id="chrono" role="group" aria-label="خط زمان زندگی ${fa(poets.length)} شاعر">
         <defs>${gradients}</defs>
         <g id="view">
           <g class="axis">${centuries.map((year) => `<line x1="${x(year)}" x2="${x(year)}" y1="0" y2="${H}"/>`).join("")}</g>
           <g class="eras">${eras.map((item) => `<line x1="${x(item.h)}" x2="${x(item.h)}" y1="0" y2="${H}"/>`).join("")}</g>
           <rect class="band" id="band" y="0" height="${H}" hidden/>
           <g id="arcs"></g>
           <g id="lives">${poets.map(bar).join("")}</g>
         </g>
         <g id="tags" aria-hidden="true"></g>
       </svg>
       <div class="stage-ctl" role="toolbar" aria-label="بزرگ‌نمایی">
         <button type="button" data-zoom="in" title="بزرگ‌تر (+)" aria-label="بزرگ‌تر">+</button>
         <button type="button" data-zoom="out" title="کوچک‌تر (−)" aria-label="کوچک‌تر">−</button>
         <button type="button" data-zoom="fit" title="نمای کل (۰)">نمای کل</button>
         <button type="button" data-zoom="full" title="تمام‌صفحه">تمام‌صفحه</button>
       </div>
       <svg class="mini" id="mini" viewBox="0 0 ${MINI_W} ${MINI_H}" width="${MINI_W}" height="${MINI_H}" role="img" aria-label="نقشه کوچک؛ بزن تا به آن نقطه بروی">
         ${poets.map((poet) => `<rect x="${(x(poet.d) * mx).toFixed(1)}" y="${(yOf(poet) * my).toFixed(1)}" width="${Math.max(1, (x(poet.b) - x(poet.d)) * mx).toFixed(1)}" height="${Math.max(1, 4 * my).toFixed(1)}" fill="${regionInfo.get(poet.region).color}"/>`).join("")}
         <rect class="lens" id="lens"/>
       </svg>
       <p class="stage-hint" id="stage-hint">بکش تا جابه‌جا شوی · چرخ یا دو انگشت برای بزرگ‌نمایی · دوبار بزن تا نزدیک شوی</p>
       <div class="focus" id="tree-focus" hidden></div>
     </div>
     <p class="key muted"><span class="sw solid"></span> سال ثبت‌شده <span class="sw fade"></span> سال تقریبی؛ سر کم‌رنگ نوار یعنی گنجور آن سال را قطعی نمی‌داند (${fa(uncertain)} شاعر از ${fa(poets.length)}). نوار ضخیم‌تر: شاعران برگزیده گنجور، که نامشان در نمای دور هم پیداست.</p>
     <p class="muted">بالای نمودار: شمار شاعران زنده در هر دهه (بیشترین ${fa(peak.n)} شاعر، حدود ${yr(peak.year)} ق). خط‌های طلایی عمودی چند رخداد تاریخی است که سال میلادی‌شان به هجری قمری برگردانده شده. سرزمین از مختصات زادگاهی که گنجور ثبت کرده ساخته شده و سال میلادی تقریبی است. کمان‌های طلایی پیوندهای تضمین و بیت مشترک است که گنجور منتشر کرده؛ ضخامت، شمار پیوند. جزئیاتش در <a href="#/bridges/2">پل‌های تضمین</a>.</p>`,
  );

  const stage = document.querySelector("#stage");
  const chart = document.querySelector("#chrono");
  const view = chart.querySelector("#view");
  const tags = chart.querySelector("#tags");
  const headSvg = document.querySelector("#shead");
  const lens = document.querySelector("#lens");
  const mini = document.querySelector("#mini");
  const lives = [...chart.querySelectorAll(".life")];
  const band = chart.querySelector("#band");
  const arcs = chart.querySelector("#arcs");
  const focus = document.querySelector("#tree-focus");
  const box = document.querySelector("#tree-q");
  let region = "";
  let picked = null;
  let ask = 0;
  let linkedIds = new Set();

  // ── pan and zoom: screen = t + k * content ──
  let k = 1;
  let tx = 0;
  let ty = 0;
  let fitK = 1;
  let fitted = true;
  let frame = 0;
  let flight = 0;
  const size = () => ({ w: chart.clientWidth || 1, h: chart.clientHeight || 1 });
  const clampAxis = (t, span, room) => {
    const margin = 40;
    if (span + margin * 2 <= room) return (room - span) / 2;
    return Math.min(margin, Math.max(room - span - margin, t));
  };
  const clamp = () => {
    const { w, h } = size();
    k = Math.min(Math.max(k, fitK * 0.8), 9);
    tx = clampAxis(tx, W * k, w);
    ty = clampAxis(ty, H * k, h);
  };
  const fit = () => {
    const { w, h } = size();
    fitK = Math.min(w / W, h / H) * 0.97;
    k = fitK;
    tx = (w - W * k) / 2;
    ty = (h - H * k) / 2;
    fitted = true;
    draw();
  };
  const zoomAt = (sx, sy, factor) => {
    const next = Math.min(Math.max(k * factor, fitK * 0.8), 9);
    tx = sx - ((sx - tx) * next) / k;
    ty = sy - ((sy - ty) * next) / k;
    k = next;
    fitted = false;
    draw();
  };
  const draw = () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(render);
  };
  const near = () => k >= KREF * 0.9;
  const render = () => {
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

  // axis, density and history moments, drawn in screen space so they stay readable
  const HEAD = 92;
  const renderHead = () => {
    const { w } = size();
    headSvg.setAttribute("viewBox", `0 0 ${w} ${HEAD}`);
    const sx = (year) => tx + k * x(year);
    const left = yearAt(-tx / k);
    const right = yearAt((w - tx) / k);
    const lo = Math.min(left, right);
    const hi = Math.max(left, right);
    const step = [10, 20, 25, 50, 100, 200].find((item) => item * PX * k >= 74) || 200;
    const ticks = [];
    for (let year = Math.ceil(Math.max(lo, from) / step) * step; year <= Math.min(hi, to); year += step) ticks.push(year);
    const top = 22;
    const base = 58;
    const dy = (n) => base - (n / peak.n) * (base - top);
    const area = `M${sx(from).toFixed(1)},${base} ${decades.map((item) => `L${sx(item.year + 5).toFixed(1)},${dy(item.n).toFixed(1)}`).join(" ")} L${sx(to).toFixed(1)},${base} Z`;
    const placed = [];
    const eraTags = eras
      .map((item) => ({ ...item, at: sx(item.h) }))
      .filter((item) => item.at > 0 && item.at < w)
      .sort((a, b) => b.at - a.at)
      .filter((item) => {
        const wide = item.title.length * 6.4 + 12;
        if (placed.some((other) => other.at - item.at < other.wide)) return false;
        if (item.at - wide < 0) return false;
        placed.push({ at: item.at, wide });
        return true;
      });
    const px = sx(peak.year + 5);
    const peakTag = px > 90 && px < w - 10 ? `<line x1="${px.toFixed(1)}" x2="${px.toFixed(1)}" y1="${dy(peak.n).toFixed(1)}" y2="${base}"/><text x="${(px - 4).toFixed(1)}" y="${base - 5}">اوج: ${fa(peak.n)} شاعر زنده</text>` : "";
    headSvg.innerHTML = `<g class="dens"><path d="${area}"/>${peakTag}</g>
      <g class="eras">${eras.map((item) => `<line x1="${sx(item.h).toFixed(1)}" x2="${sx(item.h).toFixed(1)}" y1="16" y2="${HEAD}"/>`).join("")}${eraTags
        .map((item) => `<text x="${(item.at - 3).toFixed(1)}" y="12"><title>${esc(item.text)}</title>${esc(item.title)}</text>`)
        .join("")}</g>
      <g class="axis">${ticks
        .map(
          (year) =>
            `<line x1="${sx(year).toFixed(1)}" x2="${sx(year).toFixed(1)}" y1="${base}" y2="${base + 5}"/><text x="${sx(year).toFixed(1)}" y="${base + 18}">${yr(year)} ق</text><text class="greg" x="${sx(year).toFixed(1)}" y="${base + 31}">${yr(toGregorian(year))} م</text>`,
        )
        .join("")}</g>`;
  };

  // in the far view the names would be unreadable dots: write the chosen few in screen space instead
  const renderTags = () => {
    if (near()) {
      tags.innerHTML = "";
      return;
    }
    const { w, h } = size();
    const boxes = [];
    const want = poets
      .filter((poet) => poet.pinOrder || poet === picked || linkedIds.has(String(poet.id)))
      .sort((a, b) => (b === picked) - (a === picked) || (a.pinOrder || 99) - (b.pinOrder || 99));
    const out = [];
    for (const poet of want) {
      const ax = tx + k * (x(poet.d) - 3);
      const ay = ty + k * (yOf(poet) + 7) + 4.5;
      const wide = poet.label.length * 7.6 + 8;
      const rect = { l: ax - wide, r: ax, t: ay - 12, b: ay + 4 };
      if (rect.l < 2 || rect.r > w - 2 || rect.t < 2 || rect.b > h - 2) continue;
      if (boxes.some((o) => rect.l < o.r && rect.r > o.l && rect.t < o.b && rect.b > o.t)) continue;
      boxes.push(rect);
      const cls = poet === picked ? "picked" : linkedIds.has(String(poet.id)) ? "linked" : "";
      out.push(`<text class="${cls}" x="${ax.toFixed(1)}" y="${ay.toFixed(1)}" data-id="${poet.id}">${esc(poet.label)}</text>`);
    }
    tags.innerHTML = out.join("");
  };

  // fly smoothly to a place in content space
  const flyTo = (cx, cy, targetK, at) => {
    const { w, h } = size();
    const spot = at || { x: w / 2, y: h / 2 };
    const start = { k, tx, ty };
    const endK = Math.min(Math.max(targetK, fitK), 9);
    const end = { k: endK, tx: spot.x - cx * endK, ty: spot.y - cy * endK };
    const t0 = performance.now();
    fitted = false;
    const step = (now) => {
      const p = Math.min(1, (now - t0) / 520);
      const e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      k = start.k + (end.k - start.k) * e;
      tx = start.tx + (end.tx - start.tx) * e;
      ty = start.ty + (end.ty - start.ty) * e;
      render();
      if (p < 1) flight = requestAnimationFrame(step);
    };
    cancelAnimationFrame(flight);
    flight = requestAnimationFrame(step);
  };
  const scrollTo = (poet) => {
    // aim at the part of the stage the open card does not cover
    const { w, h } = size();
    const open = !focus.hidden;
    const narrow = w < 640;
    const spot = {
      x: open && !narrow ? Math.min(w - 120, focus.offsetWidth + 20 + (w - focus.offsetWidth - 20) / 2) : w / 2,
      y: open && narrow ? Math.max(60, (h - focus.offsetHeight - 60) / 2) : h / 2,
    };
    flyTo((x(poet.b) + x(poet.d)) / 2 - 20, yOf(poet) + 7, Math.max(k, KREF * 1.6), spot);
  };

  // pointer: one finger or mouse pans, two fingers pinch
  const pointers = new Map();
  let travelled = 0;
  let pinch = null;
  chart.addEventListener("pointerdown", (event) => {
    cancelAnimationFrame(flight);
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    travelled = 0;
    if (pointers.size === 2) {
      const [a, b] = [...pointers.values()];
      pinch = { d: Math.hypot(a.x - b.x, a.y - b.y) };
    }
  });
  chart.addEventListener("pointermove", (event) => {
    const last = pointers.get(event.pointerId);
    if (!last) return;
    const now = { x: event.clientX, y: event.clientY };
    const box = chart.getBoundingClientRect();
    if (pointers.size === 1) {
      const dx = now.x - last.x;
      const dy = now.y - last.y;
      travelled += Math.abs(dx) + Math.abs(dy);
      if (travelled > 6) {
        if (!chart.hasPointerCapture(event.pointerId)) chart.setPointerCapture(event.pointerId);
        chart.classList.add("grab");
        tx += dx;
        ty += dy;
        fitted = false;
        draw();
      }
    } else if (pointers.size === 2 && pinch) {
      pointers.set(event.pointerId, now);
      const [a, b] = [...pointers.values()];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      const midX = (a.x + b.x) / 2 - box.left;
      const midY = (a.y + b.y) / 2 - box.top;
      travelled += 20;
      if (pinch.d > 0) zoomAt(midX, midY, d / pinch.d);
      pinch.d = d;
      return;
    }
    pointers.set(event.pointerId, now);
  });
  const lift = (event) => {
    pointers.delete(event.pointerId);
    if (pointers.size < 2) pinch = null;
    if (!pointers.size) chart.classList.remove("grab");
  };
  chart.addEventListener("pointerup", lift);
  chart.addEventListener("pointercancel", lift);
  chart.addEventListener(
    "wheel",
    (event) => {
      event.preventDefault();
      cancelAnimationFrame(flight);
      const box = chart.getBoundingClientRect();
      if (!event.ctrlKey && Math.abs(event.deltaX) > Math.abs(event.deltaY)) {
        tx -= event.deltaX;
        fitted = false;
        draw();
        return;
      }
      const speed = event.ctrlKey ? 0.01 : 0.0018;
      zoomAt(event.clientX - box.left, event.clientY - box.top, Math.exp(-event.deltaY * speed));
    },
    { passive: false },
  );
  chart.addEventListener("dblclick", (event) => {
    event.preventDefault();
    const box = chart.getBoundingClientRect();
    zoomAt(event.clientX - box.left, event.clientY - box.top, 2.2);
  });
  const goMini = (event) => {
    const box = mini.getBoundingClientRect();
    const cx = ((event.clientX - box.left) / box.width) * W;
    const cy = ((event.clientY - box.top) / box.height) * H;
    const { w, h } = size();
    if (k <= fitK * 1.05) k = fitK * 2.5;
    tx = w / 2 - cx * k;
    ty = h / 2 - cy * k;
    fitted = false;
    draw();
  };
  mini.addEventListener("pointerdown", (event) => {
    event.stopPropagation();
    mini.setPointerCapture(event.pointerId);
    goMini(event);
    mini.onpointermove = (move) => goMini(move);
  });
  mini.addEventListener("pointerup", () => (mini.onpointermove = null));
  stage.querySelector(".stage-ctl").addEventListener("click", (event) => {
    const button = event.target.closest("[data-zoom]");
    if (!button) return;
    const { w, h } = size();
    const kind = button.dataset.zoom;
    if (kind === "in") zoomAt(w / 2, h / 2, 1.6);
    else if (kind === "out") zoomAt(w / 2, h / 2, 1 / 1.6);
    else if (kind === "fit") fit();
    else if (kind === "full") {
      if (document.fullscreenElement) document.exitFullscreen();
      else stage.requestFullscreen?.().catch(() => stage.classList.toggle("wide"));
    }
  });
  stage.addEventListener("keydown", (event) => {
    if (event.target.closest("input, textarea")) return;
    const { w, h } = size();
    const moves = { ArrowLeft: [80, 0], ArrowRight: [-80, 0], ArrowUp: [0, 80], ArrowDown: [0, -80] };
    if (moves[event.key]) {
      event.preventDefault();
      tx += moves[event.key][0];
      ty += moves[event.key][1];
      fitted = false;
      draw();
    } else if (event.key === "+" || event.key === "=") zoomAt(w / 2, h / 2, 1.4);
    else if (event.key === "-") zoomAt(w / 2, h / 2, 1 / 1.4);
    else if (event.key === "0" || event.key === "۰") fit();
  });
  const watch = new ResizeObserver(() => {
    if (!document.body.contains(stage)) return watch.disconnect();
    if (fitted) fit();
    else {
      const { w, h } = size();
      fitK = Math.min(w / W, h / H) * 0.97;
      draw();
    }
  });
  watch.observe(stage);

  const paintState = () => {
    const q = box.value.trim();
    const peers = picked ? new Set(poets.filter((other) => other.b <= picked.d && other.d >= picked.b).map((other) => String(other.id))) : null;
    chart.classList.toggle("dim", Boolean(q || region || picked));
    for (const node of lives) {
      const poet = byId.get(node.dataset.id);
      const text = `${poet.nickname || ""} ${poet.name || ""} ${poet.birthPlace || ""} ${poet.deathPlace || ""}`;
      const match = (!q || text.includes(q)) && (!region || poet.region === region) && (!peers || peers.has(node.dataset.id));
      node.classList.toggle("on", match);
      node.classList.toggle("picked", picked?.id === poet.id);
    }
    renderTags();
  };
  const drawLinks = (links) => {
    if (!picked) return;
    const most = Math.max(1, ...links.map((link) => link.n));
    const cx = (poet) => (x(poet.b) + x(poet.d)) / 2;
    linkedIds = new Set(links.slice(0, 12).map((link) => String(link.id)));
    arcs.innerHTML = links
      .slice(0, 12)
      .map((link) => {
        const other = byId.get(String(link.id));
        if (!other) return "";
        const ax = cx(picked);
        const ay = yOf(picked) + 7;
        const bx = cx(other);
        const by = yOf(other) + 7;
        const lift = Math.min(ay > by ? by : ay, Math.min(160, 30 + Math.abs(ax - bx) * 0.25));
        return `<path d="M${ax.toFixed(1)},${ay} Q${((ax + bx) / 2).toFixed(1)},${(Math.min(ay, by) - lift).toFixed(1)} ${bx.toFixed(1)},${by}" style="stroke-width:${(1 + (link.n / most) * 4).toFixed(1)}"><title>${esc(other.label)} · ${fa(link.n)} پیوند</title></path>`;
      })
      .join("");
    for (const link of links.slice(0, 12)) chart.querySelector(`.life[data-id="${link.id}"]`)?.classList.add("on", "linked");
    renderTags();
  };
  const select = async (id, jump = false) => {
    const poet = byId.get(String(id));
    if (!poet) return;
    picked = poet;
    linkedIds = new Set();
    lives.forEach((node) => node.classList.remove("linked"));
    arcs.innerHTML = "";
    band.removeAttribute("hidden");
    band.setAttribute("x", x(poet.d));
    band.setAttribute("width", Math.max(3, x(poet.b) - x(poet.d)));
    paintState();
    const peers = poets.filter((other) => other.id !== poet.id && other.b <= poet.d && other.d >= poet.b);
    const known = peers.filter((other) => other.pinOrder).sort((a, b) => a.pinOrder - b.pinOrder);
    const peerChip = (other) => `<button class="chip" type="button" data-pick="${other.id}">${esc(other.label)}</button>`;
    focus.hidden = false;
    focus.innerHTML = `<button type="button" class="focus-x" id="tree-clear" aria-label="بستن">×</button><div class="focus-body">
      <strong>${esc(poet.label)}</strong> <span class="muted">${esc(poet.name)}${poet.birthPlace ? ` · زاده ${esc(poet.birthPlace)}` : ""} · ${esc(yearsText(poet))}${poet.broken ? " · سال‌ها در گنجور ناسازگارند" : ""}</span>
      <p>${fa(peers.length)} هم‌عصر (روشن روی نمودار)${known.length ? `، از برگزیدگان: ${known.map(peerChip).join("")}` : ""}</p>
      <p id="tree-links" class="muted">پیوندهای تضمین را از گنجور می‌آورم…</p>
      <p class="chips"><a class="btn primary" href="#/poet/${poet.id}">صفحه شاعر</a><a class="chip" href="#/bridges/${poet.id}">همه پل‌ها</a><a class="chip" href="#/map?y=${Math.round((poet.b + poet.d) / 2)}">روی نقشه</a><button class="chip" type="button" data-go="${poet.id}">برو سراغش</button></p></div>`;
    history.replaceState(null, "", `#/tree?poet=${poet.id}`);
    if (jump) scrollTo(poet);
    const token = ++ask;
    let links = [];
    try {
      const { data: quoted } = await api(`/quoted?poetId=${poet.id}&published=true`);
      const count = new Map();
      for (const item of Array.isArray(quoted) ? quoted : []) {
        if (!item.relatedPoetId || item.relatedPoetId === poet.id || item.rejected) continue;
        count.set(item.relatedPoetId, (count.get(item.relatedPoetId) || 0) + 1);
      }
      links = [...count].map(([other, n]) => ({ id: other, n })).sort((a, b) => b.n - a.n);
    } catch (error) {
      if (token !== ask) return;
      const note = document.querySelector("#tree-links");
      if (note) note.textContent = "پیوندهای تضمین از گنجور نیامد؛ بعداً دوباره بزن.";
      return;
    }
    if (token !== ask || picked !== poet) return;
    drawLinks(links);
    const note = document.querySelector("#tree-links");
    if (note)
      note.innerHTML = links.length
        ? `پیوند تضمین یا بیت مشترک با ${fa(links.length)} شاعر${links.length > 12 ? "؛ دوازده تای پرشمار روی نمودار" : ""}: ${links
            .slice(0, 6)
            .map((link) => `<button class="chip" type="button" data-pick="${link.id}">${esc(byId.get(String(link.id))?.label || "شاعر")} · ${fa(link.n)}</button>`)
            .join("")}`
        : "گنجور برای این شاعر تضمین یا بیت مشترکی منتشر نکرده.";
  };
  const clear = () => {
    picked = null;
    linkedIds = new Set();
    ask++;
    band.setAttribute("hidden", "");
    arcs.innerHTML = "";
    lives.forEach((node) => node.classList.remove("linked"));
    focus.hidden = true;
    history.replaceState(null, "", "#/tree");
    paintState();
  };

  chart.addEventListener("click", (event) => {
    if (travelled > 6) return;
    const node = event.target.closest(".life, #tags text");
    if (node) select(node.dataset.id);
  });
  chart.addEventListener("keydown", (event) => {
    const node = event.target.closest(".life");
    if (node && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      event.stopPropagation();
      select(node.dataset.id, true);
    }
  });
  focus.addEventListener("pointerdown", (event) => event.stopPropagation());
  focus.addEventListener("click", (event) => {
    if (event.target.closest("#tree-clear")) return clear();
    const go = event.target.closest("[data-go]");
    if (go) return scrollTo(byId.get(go.dataset.go));
    const chip = event.target.closest("[data-pick]");
    if (chip) select(chip.dataset.pick, true);
  });
  box.oninput = paintState;
  document.querySelector("#tree-filter").onsubmit = (event) => {
    event.preventDefault();
    const q = box.value.trim();
    const hit = q && poets.find((poet) => `${poet.nickname || ""} ${poet.name || ""} ${poet.birthPlace || ""}`.includes(q));
    if (hit) {
      box.value = "";
      select(hit.id, true);
    }
  };
  document.querySelector("#tree-regions").onclick = (event) => {
    const chip = event.target.closest("[data-region]");
    if (!chip) return;
    region = chip.dataset.region;
    document.querySelectorAll("#tree-regions .chip").forEach((node) => node.classList.toggle("on", node === chip));
    paintState();
  };
  fit();
  const start = query.get("poet");
  if (start) select(start, true);
}

const HOME_TOOLS = [
  ["#/map", "نقشه هم‌عصران", "چه کسانی هم‌زمان می‌زیستند", "◎"],
  ["#/devices", "آرایه‌ها", "لب ← لعل، ابرو ← کمان", "✦"],
  ["#/people", "مردمان شعر", "خاندان و پیوندهای شاهنامه", "♙"],
  ["#/words", "واژه‌سنج", "کدام شاعر بیشتر گفته", "≋"],
  ["#/vazn", "وزن‌ها", "بحرها و شعرهایشان", "♪"],
  ["#/bridges/2", "پل‌های تضمین", "چه کسی از چه کسی گرفت", "⇄"],
];

const TOOL_GROUPS = [
  {
    title: "زمان و مکان",
    about: "شاعران و شعرها روی نقشه و در گذر سال‌ها.",
    tools: [
      ["#/map", "نقشه هم‌عصران", "سال را جابه‌جا کن و زادگاه شاعران زنده آن سال را ببین.", "◎"],
      ["#/places", "جای‌ها در شعر", "شهرها و سال‌هایی که روی بیت‌ها برچسب خورده، روی یک نقشه.", "⌖"],
      ["#/tree", "خط زمان شاعران", "زندگی همه شاعران روی یک خط زمان؛ روی هر نام بزن تا هم‌عصرانش و تضمین‌هایش پیدا شوند.", "❦"],
    ],
  },
  {
    title: "پیوندها",
    about: "چه کسی از چه کسی گرفت، و آدم‌های درون شعر با هم چه نسبتی دارند.",
    tools: [
      ["#/bridges/2", "پل‌های تضمین", "تضمین‌ها و بیت‌های مشترک هر شاعر با دیگران، با شمار واقعی.", "⇄"],
      ["#/people", "مردمان شعر", "۶۶۲ شخصیت، بیشتر از شاهنامه: خاندان، پیوندها و بیت‌هایی که از آن‌ها نام برده‌اند.", "♙"],
    ],
  },
  {
    title: "زبان و صناعت",
    about: "وزن، واژه و آرایه؛ ابزار کسی که می‌خواهد ببیند شعر چطور ساخته شده.",
    tools: [
      ["#/vazn", "وزن‌ها", "همه بحرها با شمار مصراع، و شعرهای هر وزن.", "♪"],
      ["#/devices", "آرایه‌ها", "تشبیه، استعاره، کنایه و ایهام، با نمونه‌های واقعی و جفت‌های «این به آن مانند شده».", "✦"],
      ["#/words", "واژه‌سنج", "یک واژه، و اینکه کدام شاعر بیشتر از همه گفته‌اش.", "≋"],
      ["#/layers", "خوانش دولایه", "چند شعر نامدار با معنی ساده و معنی رمزی هر بیت، کنار قالب‌ها و واژه‌های کلیدی.", "◐"],
    ],
  },
  {
    title: "خواندن",
    about: "راه‌های سبک برای رسیدن به یک شعر.",
    tools: [
      ["#/search", "جستجو", "واژه یا تکه‌ای از بیت در همه شعرها.", "⌕"],
      ["#/library", "کتابخانه من", "نشان‌ها، یادداشت‌ها و شعرهای خوانده‌شده روی همین دستگاه.", "☆"],
    ],
  },
];

function discoverPage() {
  paint(
    "ابزارها",
    `<h1>ابزارها</h1>
     <p class="lead">راه‌های دیدن گنجینه، غیر از خواندن خطی. هر ابزار از داده باز گنجور ساخته شده؛ فهرستش در <a href="#/about">درباره</a> هست.</p>
     ${TOOL_GROUPS.map(
       (group) => `<h2 class="section">${group.title}</h2><p class="muted">${group.about}</p>
         <div class="toolbelt wide">${group.tools.map(([href, title, text, icon]) => `<a class="tool" href="${href}"><span class="tool-icon" aria-hidden="true">${icon || "•"}</span><strong>${title}</strong><small>${text}</small></a>`).join("")}</div>`,
     ).join("")}
     <p class="note">داخل صفحه هر شعر هم ابزار هست: معنی بیت، تضمین، هم‌وزن، آرایه، موسیقی، حاشیه و آینه واژه. روی بیت یا واژه بزن.</p>`,
  );
}

async function dataPage() {
  loading("داده‌ها");
  let manifest = null;
  try {
    manifest = await fileJson("manifest.json");
  } catch (error) {
    if (error === STALE) throw error;
  }
  const n = (key) => (manifest && manifest[key] != null ? Number(manifest[key]).toLocaleString("fa-IR") : "؟");
  const row = (name, what, count, used) => `<tr><th>${name}</th><td data-label="چه دارد">${what}</td><td data-label="اندازه">${count}</td><td data-label="کجا">${used}</td></tr>`;
  paint(
    "درباره",
    `<h1>درباره گنجور نو</h1>
     <p class="lead">یک خوانش‌خانه برای شعر فارسی: شعر را از رابط گنجور می‌گیرد و با چیدمان خودش نشان می‌دهد.</p>
     <p>متن، فهرست و فایل صوتی مال گنجور است و همان‌جا می‌ماند. نشان، یادداشت و اتاق خلوت روی دستگاه تو ذخیره می‌شود و به جایی فرستاده نمی‌شود. کنار خواندن، <a href="#/discover">ابزارهایی</a> هست برای دیدن شعر از راه‌های دیگر.</p>
     <p class="chips"><a class="chip" href="https://ganjoor.net" rel="noreferrer">گنجور</a><a class="chip" href="https://github.com/maryamjaberi/ganjoor-no-new" rel="noreferrer">کد این سایت</a></p>
     <h2 class="section" id="data">داده‌ها</h2>
     <p>هر چه اینجا می‌بینی از سه سرچشمه می‌آید. این بخش آن‌ها را دسته‌بندی می‌کند و می‌گوید هر ابزار از کدام داده ساخته شده.</p>
     ${manifest ? `<p class="muted">برون‌داد باز گنجور، به‌روز شده در ${esc(new Date(manifest.GeneratedAtUtc).toLocaleDateString("fa-IR", { year: "numeric", month: "long", day: "numeric" }))}.</p>` : ""}
     <h2 class="section">۱. متن و آثار</h2>
     <div class="table"><table><thead><tr><th>داده</th><th>چه دارد</th><th>اندازه</th><th>کجا به کار رفته</th></tr></thead><tbody>
       ${row("شاعران", "نام، تخلص، سال زاد و مرگ هجری، زادگاه با مختصات، چهره", n("PoetsCount"), `<a href="#/poets">شاعران</a>، <a href="#/map">نقشه</a>، <a href="#/tree">درخت</a>`)}
       ${row("بخش‌ها و کتاب‌ها", "فهرست درختی آثار هر شاعر", "—", "صفحه شاعر و فهرست")}
       ${row("شعرها", "متن، بیت‌ها، جایگاه مصراع، شرح بیت، منبع", n("PoemsCount"), "صفحه شعر، جستجو")}
       ${row("وزن و قافیه", "بحر عروضی هر بخش و حروف قافیه", "۲۱۲ وزن", `<a href="#/vazn">وزن‌ها</a>، زبانه هم‌وزن`)}
     </tbody></table></div>
     <h2 class="section">۲. صدا، موسیقی و گفتگو</h2>
     <div class="table"><table><thead><tr><th>داده</th><th>چه دارد</th><th>اندازه</th><th>کجا به کار رفته</th></tr></thead><tbody>
       ${row("خوانش‌ها", "فایل صوتی و زمان‌بندی هر بیت", "زنده از گنجور", "پخش‌کننده صفحه شعر، بیت هم‌گام")}
       ${row("موسیقی", "آهنگ‌هایی که روی شعر ساخته شده", "زنده", "زبانه موسیقی")}
       ${row("حاشیه‌ها", "یادداشت خوانندگان روی شعر یا بیت", "زنده", "زبانه حاشیه")}
     </tbody></table></div>
     <h2 class="section">۳. پیوند میان شعرها</h2>
     <div class="table"><table><thead><tr><th>داده</th><th>چه دارد</th><th>اندازه</th><th>کجا به کار رفته</th></tr></thead><tbody>
       ${row("تضمین و بیت مشترک", "بیت این شاعر و بیت شاعر دیگر، با جهت پیش و پس", "زنده", `<a href="#/bridges/2">پل‌ها</a>، زبانه تضمین`)}
       ${row("استقبال", "بخش‌های هم‌وزن و هم‌قافیه", "زنده", "زبانه هم‌وزن و تضمین")}
       ${row("شمار واژه", "بسامد هر واژه در آثار هر شاعر", "زنده", `<a href="#/words">واژه‌سنج</a>`)}
     </tbody></table></div>
     <h2 class="section">۴. آدم‌ها و جای‌ها</h2>
     <div class="table"><table><thead><tr><th>داده</th><th>چه دارد</th><th>اندازه</th><th>کجا به کار رفته</th></tr></thead><tbody>
       ${row("مردمان", "نام، نام‌های دیگر، شرح کوتاه", n("PeopleCount"), `<a href="#/people">مردمان شعر</a>`)}
       ${row("خویشاوندی", "پدر و فرزند، نیا، همسر، خواهر و برادر؛ با بیت گواه و کتاب", "۳۲۷", "صفحه هر شخص، خاندان")}
       ${row("پیوندهای دیگر", "کشنده، سپهسالار، وزیر، جانشین، هم‌پیمان…", "۳۲۴", "صفحه هر شخص")}
       ${row("نام‌بردن از اشخاص", "بیت‌هایی که شخص در آن حاضر است یا به او اشاره شده", n("PersonTagsCount"), "صفحه هر شخص")}
       ${row("جای‌ها", "نام شهر با مختصات", n("LocationsCount"), `<a href="#/places">جای‌ها در شعر</a>`)}
       ${row("برچسب جا و تاریخ", "بیتی که به یک شهر و گاهی یک سال قمری بسته شده", n("GeoTagsCount"), `<a href="#/places">جای‌ها در شعر</a>، صفحه شاعر`)}
     </tbody></table></div>
     <h2 class="section">۵. آرایه‌های ادبی</h2>
     <div class="table"><table><thead><tr><th>داده</th><th>چه دارد</th><th>اندازه</th><th>کجا به کار رفته</th></tr></thead><tbody>
       ${row("آرایه‌ها", "تعریف، نمونه و جایگاه‌های هر آرایه", n("LiteraryDevicesCount"), `<a href="#/devices">آرایه‌ها</a>`)}
       ${row("مفهوم‌ها", "چیزهایی که در تشبیه و استعاره به کار رفته: زلف، شمع، ماه…", n("LiteraryConceptsCount"), `<a href="#/devices">آرایه‌ها</a>`)}
       ${row("برچسب آرایه", "آرایه روی بیت، با جای دقیق واژه‌ها", n("LiteraryTagsCount"), "صفحه آرایه، زبانه آرایه شعر")}
     </tbody></table></div>
     <h2 class="section">۶. لایه آموزشی خود این سایت</h2>
     <div class="table"><table><thead><tr><th>داده</th><th>چه دارد</th><th>اندازه</th><th>کجا به کار رفته</th></tr></thead><tbody>
       ${row("شعرهای نمونه", "معنی ساده و معنی رمزی هر بیت، مناسبت، نسخه‌بدل", "۱۵ شعر از ۷ شاعر", `<a href="#/layers">خوانش دولایه</a>`)}
       ${row("واژه‌نامه کوچک", "ساقی، می، رند، نی، خرد…", "۱۱ واژه", `<a href="#/layers">خوانش دولایه</a>`)}
       ${row("قالب‌ها", "غزل، قصیده، مثنوی، رباعی، قطعه", "۵", `<a href="#/layers">خوانش دولایه</a>`)}
       ${row("لحظه‌های تاریخ و پل‌های آموزشی", "رویدادها و نسبت‌های تأثیر، تقریبی", "۶ رویداد، ۸ پل", `<a href="#/layers">خوانش دولایه</a>`)}
     </tbody></table></div>
     <h2 class="section">سرچشمه‌ها</h2>
     <p><strong>رابط زنده گنجور</strong> (api.ganjoor.net): متن، صوت، حاشیه، تضمین، وزن، شمار واژه، آرایه و مردمان. هر بار زنده خوانده می‌شود.</p>
     <p><strong>برون‌داد باز گنجور</strong> (<a href="https://github.com/ganjoor/ganjoor-data" rel="noreferrer">ganjoor-data</a>): پرونده‌های ثابت آدم‌ها، جای‌ها، برچسب‌ها و آرایه‌ها، مستقیم از گیت‌هاب.</p>
     <p><strong>data.json همین مخزن</strong>: لایه آموزشی و دست‌نوشته؛ معنی‌ها ساده‌اند و شرح انتقادی نیستند.</p>
     <p class="muted">بخشی از آرایه‌های غزل‌های حافظ از «پیکره متن ادبی فارسی» (Raji و همکاران، ۲۰۲۳، مجوز MIT) آمده: <a href="https://doi.org/10.5281/zenodo.7923612" rel="noreferrer">doi.org/10.5281/zenodo.7923612</a>. برخی برچسب‌ها با کمک هوش مصنوعی ساخته و به دست ویراستار گنجور بازبینی شده‌اند.</p>`,
  );
}

async function wordsPage(query) {
  const q = (query.get("q") || "").trim();
  if (!q) {
    paint(
      "واژه‌سنج",
      `<h1>واژه‌سنج</h1>
       <p class="lead">یک واژه بنویس تا ببینی کدام شاعر بیشتر از همه به کارش برده، هم به عدد و هم به نسبت کل واژه‌های دیوانش.</p>
       <form class="big-search" id="word-form"><input name="q" placeholder="مثلاً عشق، خرد، شب، سرو" aria-label="واژه" /><button class="btn primary" type="submit">بسنج</button></form>
       <p class="chips">${["عشق", "خرد", "می", "رند", "شب", "سرو", "دل", "ایران"].map((word) => `<a class="chip" href="#/words?q=${encodeURIComponent(word)}">${word}</a>`).join("")}</p>`,
    );
  } else {
    loading("واژه‌سنج");
    const [{ data }, totalRow] = await Promise.all([
      api(`/wordcounts/bycat?term=${encodeURIComponent(q)}&PageNumber=1&PageSize=40`),
      api(`/wordcounts/bycat/count?term=${encodeURIComponent(q)}`).catch((error) => {
        if (error === STALE) throw error;
        return { data: null };
      }),
    ]);
    const rows = (Array.isArray(data) ? data : []).filter((row) => row.count > 0);
    const most = Math.max(1, ...rows.map((row) => row.count));
    const rate = (row) => (row.totalWordCount ? (row.count / row.totalWordCount) * 10000 : 0);
    const byRate = [...rows].filter((row) => row.totalWordCount > 2000).sort((a, b) => rate(b) - rate(a)).slice(0, 12);
    const topRate = Math.max(0.0001, ...byRate.map(rate));
    const total = totalRow?.data?.count;
    paint(
      "واژه‌سنج",
      `<h1>واژه «${esc(q)}»</h1>
       <p class="lead">${total ? `${Number(total).toLocaleString("fa-IR")} بار در همه گنجور. ` : ""}شمارش واژه کامل است، نه پاره‌ای از واژه دیگر.</p>
       <form class="big-search" id="word-form"><input name="q" value="${esc(q)}" aria-label="واژه" /><button class="btn primary" type="submit">بسنج</button></form>
       ${
         rows.length
           ? `<h2 class="section">بیشترین شمار</h2><div class="bars">${rows
               .slice(0, 20)
               .map(
                 (row) =>
                   `<a class="barrow" href="#/search?q=${encodeURIComponent(q)}&poet=${row.poetId}"><span>${esc(row.name)}</span><i style="width:${((row.count / most) * 100).toFixed(1)}%"></i><b>${row.count.toLocaleString("fa-IR")}</b></a>`,
               )
               .join("")}</div>
             <h2 class="section">بیشترین نسبت</h2>
             <p class="muted">چند بار در هر ده هزار واژه. شاعرانی که کمتر از دو هزار واژه در گنجور دارند حساب نشده‌اند.</p>
             <div class="bars">${byRate
               .map(
                 (row) =>
                   `<a class="barrow lapis" href="#/search?q=${encodeURIComponent(q)}&poet=${row.poetId}"><span>${esc(row.name)}</span><i style="width:${((rate(row) / topRate) * 100).toFixed(1)}%"></i><b>${rate(row).toLocaleString("fa-IR", { maximumFractionDigits: 1 })}</b></a>`,
               )
               .join("")}</div>`
           : `<p>این واژه در شمارش گنجور نیامد. شکل دیگرش را امتحان کن.</p>`
       }
       <p class="chips"><a class="chip" href="#/search?q=${encodeURIComponent(q)}">شعرهای این واژه</a><a class="chip" href="#/words">واژه دیگر</a></p>`,
    );
  }
  document.querySelector("#word-form").onsubmit = (event) => {
    event.preventDefault();
    const value = String(new FormData(event.currentTarget).get("q") || "").trim();
    location.hash = `#/words?q=${encodeURIComponent(value)}`;
  };
}

const RELATION = {
  0: ["فرزند", "پدر یا مادر"],
  1: ["خواهر یا برادر", "خواهر یا برادر"],
  2: ["همسر", "همسر"],
  3: ["نواده", "نیا"],
};
const TIE = {
  0: ["وزیرِ", "وزیرش"],
  1: ["رایزنِ", "رایزنش"],
  2: ["درباریِ", "درباری‌اش"],
  3: ["پشتیبانِ", "پشتیبانش"],
  4: ["هم‌پیمانِ", "هم‌پیمانش"],
  5: ["دشمنِ", "دشمنش"],
  6: ["خدمتگزارِ", "خدمتگزارش"],
  7: ["همراهِ", "همراهش"],
  8: ["جانشینِ", "جانشینش"],
  9: ["پیوند مدح با", "پیوند مدح با"],
  10: ["پیوند هجو با", "پیوند هجو با"],
  11: ["سپهسالارِ", "سپهسالارش"],
  12: ["پهلوانِ", "پهلوانش"],
  13: ["هم‌روزگارِ", "هم‌روزگارش"],
  14: ["کُشنده‌ی", "کشته به دستِ"],
  15: ["دلداده‌ی", "دلداده‌اش"],
  99: ["پیوند با", "پیوند با"],
};

async function peoplePage() {
  loading("مردمان شعر");
  const [people, roots, graph] = await Promise.all([rootApi("/people"), rootApi("/people/familytrees"), rootApi("/people/graph")]);
  const degree = new Map();
  for (const edge of graph.edges || []) {
    degree.set(edge.person1Id, (degree.get(edge.person1Id) || 0) + 1);
    degree.set(edge.person2Id, (degree.get(edge.person2Id) || 0) + 1);
  }
  const weight = new Map((graph.nodes || []).map((node) => [node.id, node.importance || 0]));
  const list = [...people].sort((a, b) => (weight.get(b.id) || 0) - (weight.get(a.id) || 0) || (degree.get(b.id) || 0) - (degree.get(a.id) || 0));
  paint(
    "مردمان شعر",
    `<h1>مردمان شعر</h1>
     <p class="lead">${people.length.toLocaleString("fa-IR")} شخصیت که روی بیت‌های گنجور برچسب خورده‌اند؛ بیشترشان از شاهنامه. خویشاوندی و پیوند هر کدام از خود بیت‌ها گواه دارد.</p>
     ${roots.length ? `<h2 class="section">خاندان‌ها</h2><p class="chips">${roots.map((person) => `<a class="chip on" href="#/person/${person.id}">${esc(person.familyTreeCaption || person.name)}</a>`).join("")}</p>` : ""}
     <form class="big-search" id="people-filter"><input id="people-q" placeholder="نام یا شرح، مثلاً رستم یا پادشاه" aria-label="پالایش نام" /></form>
     <div class="grid" id="people-list"></div>`,
  );
  const box = document.querySelector("#people-q");
  const area = document.querySelector("#people-list");
  const draw = () => {
    const q = box.value.trim();
    const shown = list.filter((person) => !q || `${person.name} ${person.description || ""} ${(person.aliases || []).join?.(" ") || person.aliases || ""}`.includes(q));
    area.innerHTML = shown.length
      ? shown
          .slice(0, q ? 120 : 60)
          .map(
            (person) =>
              `<a class="card" href="#/person/${person.id}"><strong>${esc(person.name)}</strong>${degree.get(person.id) ? `<div class="kicker">${fa(degree.get(person.id))} پیوند</div>` : ""}<div class="muted">${esc(person.description || "")}</div></a>`,
          )
          .join("") + (!q && shown.length > 60 ? `<p class="muted">شصت نام پرپیوند. برای بقیه نام را بنویس.</p>` : "")
      : `<p class="muted">کسی با این نام نیست.</p>`;
  };
  box.oninput = draw;
  document.querySelector("#people-filter").onsubmit = (event) => event.preventDefault();
  draw();
}

function familyTree(tree, focus) {
  const persons = new Map((tree.persons || []).map((person) => [person.id, person]));
  const kids = new Map();
  const hasParent = new Set();
  const spouses = new Map();
  for (const edge of tree.relations || []) {
    if (edge.relationType === 0) {
      if (!kids.has(edge.person1Id)) kids.set(edge.person1Id, []);
      if (!kids.get(edge.person1Id).includes(edge.person2Id)) kids.get(edge.person1Id).push(edge.person2Id);
      hasParent.add(edge.person2Id);
    }
    if (edge.relationType === 2) {
      for (const [a, b] of [
        [edge.person1Id, edge.person2Id],
        [edge.person2Id, edge.person1Id],
      ]) {
        if (!spouses.has(a)) spouses.set(a, []);
        spouses.get(a).push(b);
      }
    }
  }
  const seen = new Set();
  const node = (id, depth) => {
    if (seen.has(id) || depth > 14) return "";
    seen.add(id);
    const person = persons.get(id);
    if (!person) return "";
    const wives = (spouses.get(id) || []).map((other) => persons.get(other)?.name).filter(Boolean);
    const children = (kids.get(id) || []).map((child) => node(child, depth + 1)).join("");
    return `<li><a href="#/person/${id}" class="${id === focus ? "here" : ""}">${esc(person.name)}</a>${wives.length ? `<small> · همسر: ${esc(wives.join("، "))}</small>` : ""}${children ? `<ul>${children}</ul>` : ""}</li>`;
  };
  const roots = [tree.rootId, ...[...persons.keys()].filter((id) => !hasParent.has(id) && kids.has(id))];
  return `<ul class="kin">${roots.map((id) => node(id, 0)).join("")}</ul>`;
}

// the whole family as one tree you can wander in: generations run right to left, everyone keeps a readable name
function familyMap(tree, focus) {
  const persons = new Map((tree.persons || []).map((person) => [person.id, person]));
  const kids = new Map();
  const parents = new Map();
  const spouses = new Map();
  const all = new Map();
  for (const edge of tree.relations || []) {
    if (edge.relationType === 0) {
      if (!kids.has(edge.person1Id)) kids.set(edge.person1Id, []);
      if (!kids.get(edge.person1Id).includes(edge.person2Id)) kids.get(edge.person1Id).push(edge.person2Id);
      if (!all.has(edge.person2Id)) all.set(edge.person2Id, []);
      all.get(edge.person2Id).push(edge.person1Id);
    }
    if (edge.relationType === 2) {
      for (const [a, b] of [
        [edge.person1Id, edge.person2Id],
        [edge.person2Id, edge.person1Id],
      ]) {
        if (!spouses.has(a)) spouses.set(a, []);
        spouses.get(a).push(b);
      }
    }
  }
  // each person hangs under one parent (the father where Ganjoor records one); the other parent gets a dashed link
  for (const [child, list] of all) parents.set(child, list.find((id) => persons.get(id)?.gender === 1) ?? list[0]);
  // start from the true ancestors, so the person sits inside their own line, not as a lonely root
  const roots = [...[...persons.keys()].filter((id) => !parents.has(id) && kids.has(id)), tree.rootId];
  const seen = new Set();
  const nodes = [];
  const edges = [];
  let slot = 0;
  let depthMax = 0;
  const place = (id, depth) => {
    if (seen.has(id) || !persons.has(id) || depth > 30) return null;
    seen.add(id);
    const node = { id, depth, person: persons.get(id), size: 1 };
    depthMax = Math.max(depthMax, depth);
    const children = (kids.get(id) || []).filter((child) => parents.get(child) === id).map((child) => place(child, depth + 1)).filter(Boolean);
    if (children.length) {
      node.slot = (children[0].slot + children[children.length - 1].slot) / 2;
      node.size += children.reduce((sum, child) => sum + child.size, 0);
      for (const child of children) edges.push([node, child]);
    } else node.slot = slot++;
    nodes.push(node);
    return node;
  };
  for (const root of roots) {
    if (place(root, 0)) slot += 0.6;
  }
  const byNode = new Map(nodes.map((node) => [node.id, node]));
  const second = [];
  for (const [child, list] of all) for (const parent of list) if (parent !== parents.get(child) && byNode.has(parent) && byNode.has(child) && (child === focus || parent === focus)) second.push([byNode.get(parent), byNode.get(child)]);
  const line = new Set();
  for (let id = focus; id != null && !line.has(id); id = parents.get(id)) line.add(id);
  const GEN = 150;
  const ROW = 24;
  const W = (depthMax + 1) * GEN + 40;
  const H = Math.max(1, slot) * ROW + 30;
  const nx = (node) => W - 20 - node.depth * GEN - 8;
  const ny = (node) => 20 + node.slot * ROW;
  const weight = (node) => (node.id === focus ? 9999 : line.has(node.id) ? 5000 : 0) + (node.person.importance || 0) * 50 + node.size;
  const svg = `<svg class="kin-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="درخت خاندان ${fa(nodes.length)} نفر">
    <g class="kin-edges">${edges
      .map(([a, b]) => {
        const ax = nx(a);
        const bx = nx(b);
        const mid = ax - GEN * 0.45;
        return `<path class="${line.has(a.id) && line.has(b.id) ? "line" : ""}" d="M${ax},${ny(a)} H${mid} V${ny(b)} H${bx}"/>`;
      })
      .join("")}${second
      .map(([a, b]) => `<path class="other" d="M${nx(a)},${ny(a)} C${nx(a) - GEN * 0.6},${ny(a)} ${nx(b) + GEN * 0.6},${ny(b)} ${nx(b)},${ny(b)}"><title>${esc(a.person.name)} → ${esc(b.person.name)}</title></path>`)
      .join("")}</g>
    <g class="kin-nodes">${nodes
      .map((node) => {
        const wives = (spouses.get(node.id) || []).map((other) => persons.get(other)?.name).filter(Boolean);
        const cls = node.id === focus ? "pin here" : line.has(node.id) ? "pin line" : "pin";
        return `<a class="${cls}" data-w="${weight(node)}" href="#/person/${node.id}"><title>${esc(node.person.name)}${wives.length ? ` · همسر: ${esc(wives.join("، "))}` : ""}${node.person.familyTreeCaption ? ` · ${esc(node.person.familyTreeCaption)}` : ""}</title><circle cx="${nx(node)}" cy="${ny(node)}" r="${node.id === focus ? 6 : wives.length ? 4.5 : 3.5}" class="${wives.length ? "wed" : ""}"/><text x="${nx(node) - 8}" y="${ny(node)}">${esc(node.person.name)}</text></a>`;
      })
      .join("")}</g></svg>`;
  return { svg, count: nodes.length, ratio: W / H };
}

async function personPage(id) {
  loading("شخص");
  const info = await rootApi(`/people/${id}/relations?evidenceLimit=1`);
  const [mentions, tree] = await Promise.all([
    rootApi(`/people/${id}/poems`).catch((error) => {
      if (error === STALE) throw error;
      return [];
    }),
    rootApi(`/people/${id}/familytree`).catch((error) => {
      if (error === STALE) throw error;
      return null;
    }),
  ]);
  const person = info.person || {};
  const evidence = (item) => {
    const proof = (item.evidence || [])[0];
    if (!proof) return item.note ? `<p class="muted">${esc(item.note)}</p>` : "";
    return `<p class="muted"><a href="#/poem/${proof.poemId}">«${esc(proof.coupletText || "بیت گواه")}»</a>${proof.masterCatTitle ? ` · ${esc(proof.masterCatTitle)}` : ""}${item.evidenceCount > 1 ? ` · ${item.evidenceCount} گواه` : ""}</p>`;
  };
  const kin = (info.relations || [])
    .map((item) => {
      const label = (RELATION[item.relationType] || ["خویش", "خویش"])[item.subjectIsPerson1 ? 0 : 1];
      return `<article class="card"><div class="kicker">${label}</div><strong><a href="#/person/${item.otherPersonId}">${esc(item.otherPersonName)}</a></strong>${evidence(item)}</article>`;
    })
    .join("");
  const ties = (info.affiliations || [])
    .map((item) => {
      const label = (TIE[item.affiliationType] || TIE[99])[item.subjectIsPerson1 ? 0 : 1];
      const name = `<a href="#/person/${item.otherPersonId}">${esc(item.otherPersonName)}</a>`;
      const line = item.subjectIsPerson1 || label.endsWith("ِ") || label.endsWith("با") ? `${label} ${name}` : `${label}: ${name}`;
      return `<article class="card"><strong>${line}</strong>${evidence(item)}</article>`;
    })
    .join("");
  const rows = Array.isArray(mentions) ? mentions : [];
  const present = rows.filter((row) => row.personMention === 0);
  const allusion = rows.filter((row) => row.personMention !== 0);
  const mentionList = (list) =>
    list
      .slice(0, 24)
      .map(
        (row) =>
          `<a class="hit" href="#/poem/${row.poemId}"><div class="kicker">${esc(String(row.poem?.fullTitle || "").split("»").slice(0, 2).join(" » "))}</div><strong>${esc(row.poem?.title || "")}</strong>${row.coupletText ? `<p>${esc(row.coupletText)}</p>` : ""}</a>`,
      )
      .join("");
  const treeSize = tree ? (tree.persons || []).length : 0;
  const family = treeSize > 1 ? familyMap(tree, Number(id)) : null;
  const treeHtml = family
    ? `<p class="muted">${fa(treeSize)} نفر در این خاندان. نسل‌ها از راست به چپ می‌آیند و خط طلایی، تبار همین شخص تا ریشه است. بکش و بزرگ کن تا نام همه پیدا شود؛ روی هر نام بزن تا به صفحه‌اش بروی.</p><div class="kin-map" style="aspect-ratio:${Math.max(0.9, Math.min(2.4, family.ratio)).toFixed(2)}">${family.svg}</div><details class="tree-box"><summary>همین خاندان به صورت فهرست</summary>${familyTree(tree, Number(id))}</details>`
    : "";
  paint(
    person.name || "شخص",
    `<p class="crumb"><a href="#/people">مردمان شعر</a></p>
     <h1>${esc(person.name || "")}</h1>
     ${person.description ? `<p class="lead">${esc(person.description)}</p>` : ""}
     ${person.aliases ? `<p class="muted">نام‌های دیگر: ${esc([].concat(person.aliases).join("، "))}</p>` : ""}
     ${person.wikiUrl ? `<p><a class="chip" href="${esc(person.wikiUrl)}" rel="noreferrer">ویکی‌پدیا</a></p>` : ""}
     ${kin ? `<h2 class="section">خویشان</h2><div class="grid">${kin}</div>` : ""}
     ${ties ? `<h2 class="section">پیوندها</h2><div class="grid">${ties}</div>` : ""}
     ${treeHtml ? `<h2 class="section">خاندان${tree.books?.length ? ` · ${esc(tree.books.map((book) => book.title).join("، "))}` : ""}</h2>${treeHtml}` : ""}
     ${present.length ? `<h2 class="section">حاضر در روایت · ${fa(present.length)}</h2><div class="grid">${mentionList(present)}</div>` : ""}
     ${allusion.length ? `<h2 class="section">اشاره در شعر شاعران · ${fa(allusion.length)}</h2><div class="grid">${mentionList(allusion)}</div>` : ""}
     ${!kin && !ties && !rows.length ? `<p class="muted">برای این شخص هنوز پیوند یا بیتی ثبت نشده.</p>` : ""}
     <p class="muted">پیوندها و برچسب‌ها در گنجور بخشی با کمک هوش مصنوعی ساخته و به دست ویراستار بازبینی شده‌اند. هر کدام بیت گواه دارد؛ آن را بخوان.</p>`,
  );
  const map = document.querySelector(".kin-map");
  if (map) {
    const view = atlasStage(map);
    map.parentElement.classList.add("kin-stage");
    // svg units → screen px, so names stay one size whatever the tree's size
    const box = map.querySelector("svg").viewBox.baseVal;
    const fitText = () => {
      if (!map.clientWidth) return;
      map.style.setProperty("--fit", Math.max(box.width / map.clientWidth, box.height / map.clientHeight).toFixed(4));
      view.refresh();
    };
    fitText();
    new ResizeObserver(fitText).observe(map);
  }
}

async function devicesPage() {
  loading("آرایه‌ها");
  const [list, overview] = await Promise.all([devices(), rootApi("/ganjoor/literary/stats/overview")]);
  const stats = new Map((overview.devices || []).map((item) => [item.deviceId, item]));
  const shown = list.filter((item) => stats.get(item.id)?.tagCount || item.isCore);
  const groups = [...new Set(shown.map((item) => item.category))];
  paint(
    "آرایه‌ها",
    `<h1>آرایه‌ها</h1>
     <p class="lead">${Number(overview.totalTags || 0).toLocaleString("fa-IR")} آرایه روی ${Number(overview.totalPoems || 0).toLocaleString("fa-IR")} شعر، با جای دقیق واژه‌ها. بیشترشان در غزل‌های حافظ است. آرایه را بزن تا نمونه‌ها و مفهوم‌هایش بیاید.</p>
     ${groups
       .map(
         (group) => `<h2 class="section">${DEVICE_GROUP[group] || group}</h2><div class="grid">${shown
           .filter((item) => item.category === group)
           .map((item) => {
             const stat = stats.get(item.id);
             return `<a class="card" href="#/device/${item.id}"><div class="kicker">${stat?.tagCount ? `${stat.tagCount.toLocaleString("fa-IR")} نمونه در ${stat.poemCount.toLocaleString("fa-IR")} شعر` : "هنوز نمونه‌ای نیست"}</div><strong>${esc(item.name)}</strong><p class="muted">${esc(item.definition || "")}</p></a>`;
           })
           .join("")}</div>`,
       )
       .join("")}
     ${(overview.topConcepts || []).length ? `<h2 class="section">مفهوم‌های پرکاربرد</h2><p class="chips">${overview.topConcepts.slice(0, 30).map((item) => `<span class="chip">${esc(item.name)} · ${fa(item.usageCount)}</span>`).join("")}</p>` : ""}
     <p class="muted">بخشی از آرایه‌های غزل‌های حافظ از «پیکره متن ادبی فارسی» (Raji و همکاران، ۲۰۲۳، مجوز MIT) به گنجور آمده. <a href="#/about">درباره داده‌ها</a></p>`,
  );
}

async function devicePairs(id) {
  const [meta, concepts, tags] = await Promise.all([fileJson("literary-devices.json"), fileJson("literary-concepts.json"), fileJson(`index/literary-tags/${id}.json`)]);
  const device = meta.find((item) => item.Id === Number(id));
  if (!device) return [];
  const order = new Map(device.Slots.map((slot) => [slot.Id, slot.Order]));
  const names = new Map(concepts.map((item) => [item.Id, item.Name]));
  const pairs = new Map();
  for (const tag of tags) {
    const parts = (tag.Parts || []).filter((part) => part.ConceptId).sort((a, b) => (order.get(a.SlotId) ?? 0) - (order.get(b.SlotId) ?? 0));
    if (parts.length < 2) continue;
    const key = `${parts[0].ConceptId}-${parts[1].ConceptId}`;
    const row = pairs.get(key) || { a: parts[0].ConceptId, b: parts[1].ConceptId, n: 0 };
    row.n += 1;
    pairs.set(key, row);
  }
  return [...pairs.values()]
    .map((row) => ({ ...row, aName: names.get(row.a) || "", bName: names.get(row.b) || "" }))
    .sort((x, y) => y.n - x.n);
}

async function devicePage(id, query) {
  loading("آرایه");
  const concept = Number(query.get("c") || 0);
  const pageNo = Math.max(1, Number(query.get("p") || 1));
  const size = 12;
  const [list, top, page] = await Promise.all([
    devices(),
    rootApi(`/ganjoor/literary/stats/device/${id}/top-concepts?take=40`),
    rootApi(`/ganjoor/literary/stats/tags?deviceId=${id}${concept ? `&conceptId=${concept}` : ""}&skip=${(pageNo - 1) * size}&take=${size}`),
  ]);
  let pairs = [];
  try {
    pairs = await devicePairs(id);
  } catch (error) {
    if (error === STALE) throw error;
  }
  const device = list.find((item) => item.id === Number(id)) || {};
  const items = page.items || [];
  const pages = Math.ceil((page.total || 0) / size);
  const conceptName = concept ? top.find((item) => item.conceptId === concept)?.name || pairs.find((row) => row.a === concept)?.aName || pairs.find((row) => row.b === concept)?.bName || "" : "";
  const here = (p) => `#/device/${id}?${concept ? `c=${concept}&` : ""}p=${p}`;
  const pairLink = (row) =>
    `<a class="pair ${concept === row.a ? "on" : ""}" href="#/device/${id}?c=${row.a}"><b>${esc(row.aName)}</b><span aria-hidden="true">←</span><b>${esc(row.bName)}</b><small>${fa(row.n)}</small></a>`;
  const card = (item) => {
    const spans = (misra) =>
      (item.parts || [])
        .filter((part) => part.misra === misra && part.wordStart)
        .map((part) => ({ from: part.wordStart, to: part.wordEnd || part.wordStart, label: part.slotName }));
    return `<article class="card"><div class="kicker">${esc(item.poemFullTitle || "")}</div>
      <p class="couplet">${marked(item.hemistich1, spans(1))}<br>${marked(item.hemistich2, spans(2))}</p>
      <p class="muted">${(item.parts || [])
        .map((part) => `${esc(part.slotName)}: ${part.conceptId ? `<a href="#/device/${id}?c=${part.conceptId}">${esc(part.conceptName || part.words || "")}</a>` : esc(part.words || part.conceptName || "")}`)
        .join(" · ")}${item.uncertain ? " · نامطمئن" : ""}</p>
      ${item.note ? `<p class="muted">${esc(item.note)}</p>` : ""}
      <a href="#/poem/${item.poemId}">خواندن شعر</a></article>`;
  };
  paint(
    device.name || "آرایه",
    `<p class="crumb"><a href="#/devices">آرایه‌ها</a></p>
     <h1>${esc(device.name || "")}${conceptName ? ` · ${esc(conceptName)}` : ""}</h1>
     <p class="lead">${esc(device.definition || "")}</p>
     ${device.example ? `<p class="panel">${esc(device.example)}</p>` : ""}
     ${
       pairs.length
         ? `<h2 class="section">${Number(id) === 1 ? "چه چیز به چه مانند شده" : "جفت‌های پرتکرار"}</h2>
            <div class="pairs">${pairs.slice(0, 8).map(pairLink).join("")}</div>
            ${pairs.length > 8 ? `<details class="more-box"><summary>${fa(Math.min(pairs.length, 40) - 8)} جفت دیگر</summary><div class="pairs">${pairs.slice(8, 40).map(pairLink).join("")}</div></details>` : ""}`
         : ""
     }
     ${
       top.length
         ? `<details class="more-box" ${concept ? "open" : ""}><summary>پالایش با مفهوم${conceptName ? `: ${esc(conceptName)}` : ""}</summary><p class="chips"><a class="chip ${concept ? "" : "on"}" href="#/device/${id}">همه</a>${top.map((item) => `<a class="chip ${item.conceptId === concept ? "on" : ""}" href="#/device/${id}?c=${item.conceptId}">${esc(item.name)} · ${fa(item.usageCount)}</a>`).join("")}</p></details>`
         : ""
     }
     <h2 class="section" id="samples">نمونه‌ها${conceptName ? ` با «${esc(conceptName)}»` : ""} · ${fa(page.total || 0)}</h2>
     ${items.length ? `<div class="grid">${items.map(card).join("")}</div>` : `<p class="muted">نمونه‌ای ثبت نشده.</p>`}
     ${pages > 1 ? `<p class="chips">${pageNo > 1 ? `<a class="chip" href="${here(pageNo - 1)}">قبلی</a>` : ""}<span class="chip">صفحه ${pageNo} از ${pages}</span>${pageNo < pages ? `<a class="chip" href="${here(pageNo + 1)}">بعدی</a>` : ""}</p>` : ""}`,
  );
  if (concept || pageNo > 1) document.querySelector("#samples")?.scrollIntoView();
}

async function placesPage() {
  loading("جای‌ها در شعر");
  const [geo, locations, manifest] = await Promise.all([fileJson("geotags.json"), fileJson("locations.json"), fileJson("manifest.json")]);
  const buckets = [...new Set(geo.map((item) => Math.floor(item.PoemId / 2000)))];
  const index = {};
  const shards = await Promise.all(buckets.map((bucket) => fileJson(`index/poems-by-id/${bucket}.json`).catch((error) => {
    if (error === STALE) throw error;
    return {};
  })));
  for (const shard of shards) Object.assign(index, shard);
  const poetBySlug = new Map((manifest.Poets || []).map((poet) => [poet.FullUrl, poet]));
  const byId = new Map(locations.map((item) => [item.Id, item]));
  const groups = new Map();
  const dated = [];
  for (const tag of geo) {
    const place = byId.get(tag.LocationId);
    if (!place) continue;
    const url = index[String(tag.PoemId)] || "";
    const poet = poetBySlug.get(`/${url.split("/")[1] || ""}`);
    const entry = { poemId: tag.PoemId, poet: poet?.Nickname || "", year: tag.LunarYear || 0, place: place.Name };
    const group = groups.get(place.Id) || { place, tags: [] };
    if (!group.tags.some((item) => item.poemId === entry.poemId)) group.tags.push(entry);
    groups.set(place.Id, group);
    if (entry.year && !dated.some((item) => item.poemId === entry.poemId && item.place === entry.place)) dated.push(entry);
  }
  const all = [...groups.values()].sort((a, b) => b.tags.length - a.tags.length);
  const inside = [];
  const outside = [];
  for (const group of all) {
    const point = project(group.place.Longitude, group.place.Latitude);
    if (point.x < 0 || point.x > 100 || point.y < 0 || point.y > 100) outside.push(group);
    else inside.push({ ...group, point });
  }
  const most = Math.max(1, ...inside.map((group) => group.tags.length));
  const card = (group) => {
    const poets = [...new Set(group.tags.map((item) => item.poet).filter(Boolean))];
    return `<article class="card" id="place-${group.place.Id}"><strong>${esc(group.place.Name)}</strong><div class="kicker">${fa(group.tags.length)} شعر${poets.length ? ` · ${esc(poets.join("، "))}` : ""}</div><p class="chips">${group.tags
      .slice(0, 8)
      .map((item) => `<a class="chip" href="#/poem/${item.poemId}">${esc(item.poet || "شعر")}${item.year ? ` · ${fa(item.year)}` : ""}</a>`)
      .join("")}</p></article>`;
  };
  dated.sort((a, b) => a.year - b.year);
  paint(
    "جای‌ها در شعر",
    `<h1>جای‌ها در شعر</h1>
     <p class="lead">${geo.length.toLocaleString("fa-IR")} بیت در گنجور به یک شهر بسته شده و ${dated.length.toLocaleString("fa-IR")} تا سال هم دارد. این نقشه زادگاه شاعر نیست؛ جایی است که خود شعر از آن حرف می‌زند. اندازه نقطه، شمار شعرهاست. بکش و بزرگ کن تا نام شهرهای کوچک‌تر هم پیدا شود.</p>
     <div class="atlas realm dense">${inside
       .map((group) => {
         const size = Math.round(8 + Math.sqrt(group.tags.length / most) * 18);
         return `<a class="pin" style="left:${group.point.x}%;top:${group.point.y}%" href="#/places" data-place="${group.place.Id}" data-w="${group.tags.length}" title="${esc(group.place.Name)}: ${group.tags.length} شعر"><span>${esc(group.place.Name)}</span><i style="width:${size}px;height:${size}px"></i></a>`;
       })
       .join("")}</div>
     ${
       dated.length
         ? `<h2 class="section">خط زمان · سال قمری</h2><ol class="ages">${dated
             .map((item) => `<li><a href="#/poem/${item.poemId}"><b>${fa(item.year)}</b> · ${esc(item.place)}${item.poet ? ` · ${esc(item.poet)}` : ""}</a></li>`)
             .join("")}</ol>`
         : ""
     }
     <h2 class="section">شهرها</h2>
     <div class="grid">${inside.map(card).join("")}</div>
     ${outside.length ? `<h2 class="section">بیرون از این نقشه</h2><p class="muted">مکه، بیت‌المقدس، روم و جاهای دورتر.</p><div class="grid">${outside.map(card).join("")}</div>` : ""}`,
  );
  atlasStage(document.querySelector(".atlas.realm.dense"));
  document.querySelectorAll(".pin[data-place]").forEach((pin) => {
    pin.onclick = (event) => {
      event.preventDefault();
      document.getElementById(`place-${pin.dataset.place}`)?.scrollIntoView({ block: "center" });
    };
  });
}

async function layersPage(id) {
  const data = await local();
  const poems = data.poets.flatMap((poet) => poet.books.flatMap((book) => book.poems.map((poem) => ({ ...poem, poet, book }))));
  const formOf = (name) => data.forms.find((form) => form.name === name);
  if (id) {
    const poem = poems.find((item) => item.id === id);
    if (!poem) {
      paint("نیست", `<h1>این شعر در لایه آموزشی نیست</h1><p><a href="#/layers">بازگشت</a></p>`);
      return;
    }
    const words = data.lexicon.filter((entry) => poem.verses.some((verse) => entry.aliases.some((alias) => verse.text.split(/\s+/).includes(alias))));
    const form = formOf(poem.form);
    const links = data.tazmin.filter((item) => item.from === poem.id || item.to === poem.id);
    paint(
      poem.title,
      `<p class="crumb"><a href="#/layers">خوانش دولایه</a></p>
       <p class="kicker">${esc(poem.poet.name)} · ${esc(poem.book.title)}</p>
       <h1>${esc(poem.title)}</h1>
       <p class="chips"><span class="chip">${esc(poem.form)}</span><span class="chip">${esc(poem.meter)}</span>${(poem.topics || []).map((topic) => `<span class="chip">${esc(topic)}</span>`).join("")}</p>
       ${poem.occasion ? `<p class="lead">${esc(poem.occasion)}</p>` : ""}
       <div class="tabs" id="layer-tabs"><button class="chip on" data-layer="both" type="button">هر دو لایه</button><button class="chip" data-layer="plain" type="button">فقط معنی ساده</button><button class="chip" data-layer="mystic" type="button">فقط معنی رمزی</button><button class="chip" data-layer="none" type="button">فقط شعر</button></div>
       <div class="layers" id="layers" data-show="both">${poem.verses
         .map(
           (verse, index) =>
             `<div class="layer ${index % 2 ? "end" : ""}"><p class="verse">${esc(verse.text)}</p><p class="plain">${esc(verse.plain || "")}</p><p class="mystic">${esc(verse.mystic || "")}</p></div>`,
         )
         .join("")}</div>
       ${(poem.versions || []).length ? `<h2 class="section">نسخه‌بدل</h2>${poem.versions.map((line) => `<p>${esc(line)}</p>`).join("")}` : ""}
       ${form ? `<h2 class="section">قالب: ${esc(form.name)}</h2><p>${esc(form.about)}</p>` : ""}
       ${words.length ? `<h2 class="section">واژه‌های کلیدی</h2><div class="grid">${words.map((entry) => `<article class="card"><strong><a href="#/words?q=${encodeURIComponent(entry.word)}">${esc(entry.word)}</a></strong><p class="muted">${esc(entry.meaning)}</p></article>`).join("")}</div>` : ""}
       ${links.length ? `<h2 class="section">هم‌سخن</h2><div class="grid">${links
         .map((item) => {
           const other = poems.find((entry) => entry.id === (item.from === poem.id ? item.to : item.from));
           return other ? `<a class="card" href="#/layers/${other.id}"><div class="kicker">${esc(item.kind)}</div><strong>${esc(other.poet.name)} · ${esc(other.title)}</strong><p class="muted">${esc(item.note)}</p></a>` : "";
         })
         .join("")}</div>` : ""}
       <p class="chips"><a class="btn primary" href="#/search?q=${encodeURIComponent(poem.verses[0].text)}">متن کامل در گنجور</a></p>
       <p class="muted">${esc(data.note)}</p>`,
    );
    document.querySelector("#layer-tabs").onclick = (event) => {
      const button = event.target.closest("[data-layer]");
      if (!button) return;
      document.querySelector("#layers").dataset.show = button.dataset.layer;
      document.querySelectorAll("#layer-tabs .chip").forEach((node) => node.classList.toggle("on", node === button));
    };
    return;
  }
  const poetName = (pid) => data.poets.find((poet) => poet.id === pid)?.name || pid;
  paint(
    "خوانش دولایه",
    `<h1>خوانش دولایه</h1>
     <p class="lead">چند شعر نامدار که بیت به بیت دو معنی دارند: یکی ساده و نزدیک به متن، یکی رمزی و تأویلی. این لایه آموزشی و دست‌نوشته همین سایت است، نه شرح انتقادی.</p>
     ${data.poets
       .map(
         (poet) => `<h2 class="section">${esc(poet.name)}</h2><p class="muted">${esc(poet.style)}</p><div class="grid">${poet.books
           .flatMap((book) => book.poems)
           .map((poem) => `<a class="card" href="#/layers/${poem.id}"><div class="kicker">${esc(poem.form)}</div><strong>${esc(poem.title)}</strong><p class="muted">${esc(poem.verses[0].text)}</p></a>`)
           .join("")}</div>`,
       )
       .join("")}
     <h2 class="section">قالب‌ها</h2>
     <div class="grid">${data.forms.map((form) => `<article class="card"><strong>${esc(form.name)}</strong><p class="muted">${esc(form.about)}</p></article>`).join("")}</div>
     <h2 class="section">واژه‌نامه کوچک</h2>
     <div class="grid">${data.lexicon.map((entry) => `<article class="card"><strong><a href="#/words?q=${encodeURIComponent(entry.word)}">${esc(entry.word)}</a></strong><p class="muted">${esc(entry.meaning)}</p></article>`).join("")}</div>
     <h2 class="section">لحظه‌های تاریخ</h2>
     <ol class="ages">${data.events
       .map((event) => {
         const poem = poems.find((item) => item.id === event.poem);
         return `<li><b>${event.year} م</b> · ${esc(event.title)} — ${esc(event.text)}${poem ? ` <a href="#/layers/${poem.id}">${esc(poem.title)}</a>` : ""}</li>`;
       })
       .join("")}</ol>
     <h2 class="section">پل‌های آموزشی</h2>
     <div class="grid">${data.bridges.map((item) => `<article class="card"><div class="kicker">${esc(item.kind)}</div><strong>${esc(poetName(item.from))} ← ${esc(poetName(item.to))}</strong><p class="muted">${esc(item.note)}</p></article>`).join("")}</div>
     <p class="muted">${esc(data.note)}</p>`,
  );
}

async function render() {
  if (audioNode) {
    audioNode.pause();
    audioNode = null;
  }
  const mine = ++renderToken;
  const hash = location.hash || "#/";
  const [pathPart, queryPart] = hash.split("?");
  const query = new URLSearchParams(queryPart || "");
  const parts = pathPart.replace(/^#\/?/, "").split("/").filter(Boolean);
  const path = `#/${parts.join("/")}`;
  mobile.hidden = true;
  menuBtn.setAttribute("aria-expanded", "false");
  if (input && parts[0] !== "search" && document.activeElement !== input) input.value = "";
  document.querySelectorAll(".desk a, .mobile a, .footlinks a").forEach((link) => {
    const href = link.getAttribute("href") || "";
    const on = href === path || (href !== "#/" && path.startsWith(href)) || (href === "#/discover" && TOOL_ROUTES.has(parts[0] || ""));
    if (on) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  try {
    if (!parts.length) await home();
    else if (parts[0] === "poets") await poetsPage(query);
    else if (parts[0] === "poet" && parts[1]) await poetPage(parts[1]);
    else if (parts[0] === "bridges" && parts[1]) await bridgesPage(parts[1]);
    else if (parts[0] === "cat" && parts[1]) await catPage(parts[1], query);
    else if (parts[0] === "poem" && parts[1]) await poemPage(parts[1], query);
    else if (parts[0] === "search") await searchPage(query);
    else if (parts[0] === "map") await mapPage(query);
    else if (parts[0] === "tree" || parts[0] === "sky") await treePage(query);
    else if (parts[0] === "vazn") await vaznPage(query);
    else if (parts[0] === "discover") discoverPage();
    else if (parts[0] === "data") await dataPage();
    else if (parts[0] === "faal") location.replace("#/");
    else if (parts[0] === "words") await wordsPage(query);
    else if (parts[0] === "people") await peoplePage();
    else if (parts[0] === "person" && parts[1]) await personPage(parts[1]);
    else if (parts[0] === "devices") await devicesPage();
    else if (parts[0] === "device" && parts[1]) await devicePage(parts[1], query);
    else if (parts[0] === "places") await placesPage();
    else if (parts[0] === "layers") await layersPage(parts[1]);
    else if (parts[0] === "library") await libraryPage();
    else if (parts[0] === "about") await dataPage();
    else paint("نیست", `<section class="empty-state"><h1>این صفحه نیست</h1><p>شاید نشانی عوض شده باشد.</p><p class="chips"><a class="btn primary" href="#/">خانه</a><a class="chip" href="#/discover">ابزارها</a><a class="chip" href="#/search">جستجو</a></p></section>`);
  } catch (error) {
    if (error === STALE || mine !== renderToken) return;
    failed(error);
  }
}

menuBtn.addEventListener("click", () => {
  const open = mobile.hidden;
  mobile.hidden = !open;
  menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
});
mobile.addEventListener("click", () => {
  mobile.hidden = true;
});
form.addEventListener("submit", (event) => {
  event.preventDefault();
  mobile.hidden = true;
  location.hash = `#/search?q=${encodeURIComponent(input.value.trim())}`;
});
window.addEventListener("hashchange", render);
render();
