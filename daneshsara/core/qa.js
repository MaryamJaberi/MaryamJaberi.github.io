/* دانش‌سرا — ابزار بازبینی (QA): روی هر بخش صفحه کامنت بگذار و برچسب بزن.
   همه‌چیز در مرورگر خودت می‌ماند (localStorage). خروجی: متن برای فرستادن به Claude یا فایل JSON. */
(() => {
if (window.__dsQA) return; window.__dsQA = 1;

/* In the private copy pages live inside a frame. A link to another page of the site that
   opens in a new tab lands on the bare frame address, which the browser blocks.
   So internal links always open in the same frame; outside links still open in a new tab. */
const internal = href => { try { const u = new URL(href, location.href); return u.origin === location.origin; } catch (e) { return false; } };
document.addEventListener("click", e => {
  const a = e.target.closest && e.target.closest("a[href]");
  if (!a || !internal(a.href)) return;
  if (a.target && a.target !== "_self") a.removeAttribute("target");
  if (e.ctrlKey || e.metaKey || e.shiftKey || e.button === 1) { e.preventDefault(); location.href = a.href; }
}, true);
document.addEventListener("auxclick", e => {
  const a = e.target.closest && e.target.closest("a[href]");
  if (a && e.button === 1 && internal(a.href)) { e.preventDefault(); location.href = a.href; }
}, true);
const _open = window.open;
window.open = function (url, name, feat) {
  if (url && internal(String(url))) { location.href = new URL(url, location.href).href; return window; }
  return _open.apply(window, arguments);
};

const KEY = "ds-qa-v1";
const LABELS = [
  ["beauty", "زیبایی", "#d9468f"],
  ["ux", "تجربهٔ کاربری", "#7b5cd6"],
  ["content", "محتوایی", "#2f80c9"],
  ["use", "کاربردی", "#1f9a6b"],
  ["tech", "فنی", "#c77a12"],
  ["idea", "ایده", "#c9a400"],
];
const LMAP = Object.fromEntries(LABELS.map(l => [l[0], l]));
const fa = n => String(n).replace(/\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[d]);

let memory = [];          // fallback if storage is blocked
let storageOK = true;
function load() {
  try { const r = localStorage.getItem(KEY); return r ? JSON.parse(r) : []; }
  catch (e) { storageOK = false; return memory; }
}
function save(list) {
  memory = list;
  try { localStorage.setItem(KEY, JSON.stringify(list)); storageOK = true; }
  catch (e) { storageOK = false; }
}
const page = () => location.pathname.replace(/^.*?\/(?=[^/]*\/[^/]*$|[^/]*$)/, "") + location.hash;
const pageKey = () => location.pathname + location.hash;

/* ---------- selector of a clicked element ---------- */
function cssPath(el) {
  const parts = [];
  while (el && el.nodeType === 1 && el !== document.body) {
    if (el.id && !/^\d/.test(el.id)) { parts.unshift("#" + CSS.escape(el.id)); break; }
    let i = 1, s = el;
    while ((s = s.previousElementSibling)) if (s.tagName === el.tagName) i++;
    parts.unshift(el.tagName.toLowerCase() + ":nth-of-type(" + i + ")");
    el = el.parentElement;
  }
  return parts.join(" > ");
}
function find(sel) { try { return document.querySelector(sel); } catch (e) { return null; } }
const snippet = el => (el.innerText || el.alt || el.title || el.tagName).replace(/\s+/g, " ").trim().slice(0, 90);

/* ---------- UI in a shadow root so site styles don't leak ---------- */
const host = document.createElement("div");
host.id = "ds-qa-host";
host.style.cssText = "all:initial;position:fixed;inset:auto;z-index:2147483000";
const root = host.attachShadow({ mode: "open" });
root.innerHTML = `
<style>
:host{all:initial}
*{box-sizing:border-box;font-family:Vazirmatn,Tahoma,"Segoe UI",sans-serif}
.fab{position:fixed;left:16px;bottom:16px;background:#1d2433;color:#fff;border:0;border-radius:24px;padding:10px 16px;font-size:14px;cursor:pointer;box-shadow:0 4px 14px #0004;display:flex;gap:8px;align-items:center}
.fab.on{background:#d9468f}
.fab .n{background:#fff3;border-radius:10px;padding:0 7px;font-size:12px}
.bar{position:fixed;left:50%;top:10px;transform:translateX(-50%);background:#d9468f;color:#fff;padding:7px 14px;border-radius:18px;font-size:13px;direction:rtl;display:none;box-shadow:0 3px 10px #0003}
.bar.show{display:block}
.box{position:fixed;width:min(340px,92vw);background:#fff;color:#1d2433;border-radius:12px;box-shadow:0 10px 30px #0004;padding:12px;direction:rtl;display:none;font-size:14px}
.box.show{display:block}
.box .tgt{font-size:12px;color:#667;background:#f3f4f8;border-radius:6px;padding:6px 8px;margin-bottom:8px;max-height:3.6em;overflow:hidden}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 8px}
.chip{border:1.5px solid var(--c);color:var(--c);background:#fff;border-radius:14px;padding:3px 10px;font-size:12.5px;cursor:pointer}
.chip.sel{background:var(--c);color:#fff}
textarea{width:100%;min-height:80px;border:1px solid #ccd;border-radius:8px;padding:8px;font-size:14px;direction:rtl;resize:vertical}
.row{display:flex;gap:8px;justify-content:flex-start;margin-top:8px;align-items:center;flex-wrap:wrap}
.btn{border:0;border-radius:8px;padding:7px 12px;font-size:13px;cursor:pointer;background:#e9ebf2;color:#1d2433}
.btn.pri{background:#1d2433;color:#fff}
.btn.red{background:#fde8ee;color:#b0244f}
.sev{font-size:12px;color:#667;display:flex;gap:6px;align-items:center}
.sev select{font-size:12px;border-radius:6px;border:1px solid #ccd;padding:2px}
.panel{position:fixed;left:0;top:0;bottom:0;width:min(400px,100vw);background:#fafbfd;box-shadow:4px 0 20px #0003;direction:rtl;display:none;flex-direction:column;color:#1d2433}
.panel.show{display:flex}
.ph{padding:12px;border-bottom:1px solid #e3e5ec;display:flex;flex-direction:column;gap:8px}
.ph h3{margin:0;font-size:16px;display:flex;justify-content:space-between;align-items:center}
.list{overflow:auto;flex:1;padding:8px 12px}
.item{background:#fff;border:1px solid #e3e5ec;border-radius:10px;padding:9px 10px;margin-bottom:8px;font-size:13.5px}
.item.done{opacity:.5}
.item .meta{font-size:11.5px;color:#778;margin-bottom:4px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.item .q{font-size:12px;color:#556;border-right:3px solid #dde;padding-right:6px;margin:4px 0}
.tag{color:#fff;background:var(--c);border-radius:10px;padding:0 7px;font-size:11px}
.item .acts{display:flex;gap:10px;margin-top:6px;font-size:12px}
.item .acts a{color:#2f80c9;cursor:pointer;text-decoration:none}
.warn{font-size:12px;background:#fff4d6;color:#7a5a00;padding:6px 8px;border-radius:6px}
.empty{color:#889;font-size:13px;padding:20px 4px;text-align:center}
.toast{position:fixed;left:50%;bottom:70px;transform:translateX(-50%);background:#1d2433;color:#fff;padding:8px 14px;border-radius:8px;font-size:13px;direction:rtl;display:none}
.toast.show{display:block}
</style>
<button class="fab" part="fab"><span>بازبینی</span><span class="n">۰</span></button>
<div class="bar">حالت بازبینی: روی هر بخش کلیک کن تا کامنت بگذاری · Esc برای خروج</div>
<div class="box">
  <div class="tgt"></div>
  <div class="chips"></div>
  <textarea placeholder="چه دیدی؟ چه باید عوض شود؟"></textarea>
  <div class="row">
    <label class="sev">اهمیت <select><option value="low">کم</option><option value="mid" selected>متوسط</option><option value="high">زیاد</option></select></label>
  </div>
  <div class="row"><button class="btn pri save">ذخیره</button><button class="btn cancel">انصراف</button><button class="btn red del" hidden>حذف</button></div>
</div>
<div class="panel">
  <div class="ph">
    <h3><span>کامنت‌های بازبینی</span><button class="btn close">✕</button></h3>
    <div class="chips filt"></div>
    <div class="row">
      <label class="sev"><input type="checkbox" class="onlyhere"> فقط این صفحه</label>
      <label class="sev"><input type="checkbox" class="hidedone"> پنهان کردن انجام‌شده‌ها</label>
    </div>
    <div class="row">
      <button class="btn pri pick">+ کامنت تازه</button>
      <button class="btn copy">کپی برای Claude</button>
      <button class="btn dl">دانلود JSON</button>
      <button class="btn imp">بارگذاری JSON</button>
    </div>
    <div class="warn" hidden>این مرورگر اجازهٔ ذخیره نمی‌دهد؛ کامنت‌ها با بستن صفحه پاک می‌شوند. قبل از بستن «کپی برای Claude» را بزن.</div>
  </div>
  <div class="list"></div>
</div>
<div class="toast"></div>
<input type="file" accept=".json,application/json" hidden>
`;
const $ = s => root.querySelector(s);
const fab = $(".fab"), bar = $(".bar"), box = $(".box"), panel = $(".panel"), list = $(".list");

/* overlay for hover outline and pins (in light DOM so it can sit over elements) */
const outline = document.createElement("div");
outline.style.cssText = "position:fixed;pointer-events:none;border:2px dashed #d9468f;background:#d9468f14;border-radius:4px;z-index:2147482999;display:none";
const pinLayer = document.createElement("div");
pinLayer.style.cssText = "position:absolute;left:0;top:0;width:0;height:0;z-index:2147482998";

function mount() {
  document.body.appendChild(host);
  document.body.appendChild(outline);
  document.body.appendChild(pinLayer);
  renderPins(); updateCount();
}
if (document.body) mount(); else document.addEventListener("DOMContentLoaded", mount);

function toast(t) { const el = $(".toast"); el.textContent = t; el.classList.add("show"); clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove("show"), 2200); }

/* ---------- picking mode ---------- */
let picking = false;
function setPicking(on) {
  picking = on;
  fab.classList.toggle("on", on);
  bar.classList.toggle("show", on);
  outline.style.display = "none";
  document.documentElement.style.cursor = on ? "crosshair" : "";
}
const isOurs = el => el === host || el === outline || pinLayer.contains(el);
document.addEventListener("mousemove", e => {
  if (!picking) return;
  const el = e.target;
  if (isOurs(el) || el === document.body || el === document.documentElement) { outline.style.display = "none"; return; }
  const r = el.getBoundingClientRect();
  Object.assign(outline.style, { display: "block", left: r.left + "px", top: r.top + "px", width: r.width + "px", height: r.height + "px" });
}, true);
document.addEventListener("click", e => {
  if (!picking || isOurs(e.target)) return;
  e.preventDefault(); e.stopPropagation();
  const el = e.target;
  const sel = String(getSelection() || "").trim().slice(0, 200);
  setPicking(false);
  openBox({ sel: cssPath(el), snip: snippet(el), quote: sel }, e.clientX, e.clientY);
}, true);
document.addEventListener("keydown", e => {
  if (e.key === "Escape") { if (picking) setPicking(false); box.classList.remove("show"); }
});

/* ---------- comment box ---------- */
let draft = null, chosen = new Set();
const chipsBox = $(".box .chips");
LABELS.forEach(([k, t, c]) => {
  const b = document.createElement("button");
  b.className = "chip"; b.textContent = t; b.style.setProperty("--c", c); b.dataset.k = k;
  b.onclick = () => { chosen.has(k) ? chosen.delete(k) : chosen.add(k); b.classList.toggle("sel"); };
  chipsBox.appendChild(b);
});
function openBox(d, x, y) {
  draft = d;
  chosen = new Set(d.labels || []);
  chipsBox.querySelectorAll(".chip").forEach(b => b.classList.toggle("sel", chosen.has(b.dataset.k)));
  $(".box .tgt").textContent = (d.quote ? "«" + d.quote + "»" : d.snip) || "بخشی از صفحه";
  $(".box textarea").value = d.text || "";
  $(".box select").value = d.sev || "mid";
  $(".box .del").hidden = !d.id;
  box.classList.add("show");
  const w = box.offsetWidth, h = box.offsetHeight;
  box.style.left = Math.max(8, Math.min(innerWidth - w - 8, x - w / 2)) + "px";
  box.style.top = Math.max(8, Math.min(innerHeight - h - 8, y + 14)) + "px";
  setTimeout(() => $(".box textarea").focus(), 0);
}
$(".box .cancel").onclick = () => box.classList.remove("show");
$(".box .save").onclick = () => {
  const text = $(".box textarea").value.trim();
  if (!text && !chosen.size) { toast("یک جمله بنویس یا یک برچسب بزن"); return; }
  const all = load();
  if (draft.id) {
    const c = all.find(c => c.id === draft.id);
    if (c) Object.assign(c, { text, labels: [...chosen], sev: $(".box select").value, edited: new Date().toISOString() });
  } else {
    all.push({
      id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
      page: pageKey(), title: document.title, sel: draft.sel, snip: draft.snip, quote: draft.quote || "",
      text, labels: [...chosen], sev: $(".box select").value, done: false, at: new Date().toISOString(),
    });
  }
  save(all); box.classList.remove("show");
  toast(storageOK ? "ذخیره شد" : "ذخیره شد (فقط تا بستن صفحه)");
  renderPins(); updateCount(); if (panel.classList.contains("show")) renderList();
};
$(".box .del").onclick = () => {
  save(load().filter(c => c.id !== draft.id)); box.classList.remove("show");
  renderPins(); updateCount(); renderList();
};

/* ---------- pins on the page ---------- */
function renderPins() {
  pinLayer.innerHTML = "";
  const here = load().filter(c => c.page === pageKey() && !c.done);
  here.forEach((c, i) => {
    const el = find(c.sel); if (!el) return;
    const r = el.getBoundingClientRect();
    const p = document.createElement("button");
    const col = (LMAP[c.labels[0]] || [0, 0, "#1d2433"])[2];
    p.textContent = fa(i + 1);
    p.title = c.text;
    p.style.cssText = `position:absolute;left:${r.left + scrollX - 10}px;top:${r.top + scrollY - 10}px;width:22px;height:22px;border-radius:50%;border:2px solid #fff;background:${col};color:#fff;font:bold 11px Tahoma;cursor:pointer;box-shadow:0 2px 6px #0004;padding:0`;
    p.onclick = ev => { ev.stopPropagation(); openBox(c, ev.clientX, ev.clientY); };
    pinLayer.appendChild(p);
  });
}
let rt; addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(renderPins, 150); });
addEventListener("hashchange", () => { renderPins(); updateCount(); });
setTimeout(renderPins, 1200);  // pages that render late

function updateCount() {
  const n = load().filter(c => !c.done).length;
  $(".fab .n").textContent = fa(n);
}

/* ---------- panel ---------- */
const filt = $(".filt"); const fsel = new Set();
LABELS.forEach(([k, t, c]) => {
  const b = document.createElement("button");
  b.className = "chip"; b.textContent = t; b.style.setProperty("--c", c);
  b.onclick = () => { fsel.has(k) ? fsel.delete(k) : fsel.add(k); b.classList.toggle("sel"); renderList(); };
  filt.appendChild(b);
});
$(".onlyhere").onchange = renderList; $(".hidedone").onchange = renderList;
fab.onclick = () => {
  if (picking) { setPicking(false); return; }
  panel.classList.toggle("show");
  if (panel.classList.contains("show")) renderList();
};
$(".close").onclick = () => panel.classList.remove("show");
$(".pick").onclick = () => { panel.classList.remove("show"); setPicking(true); };

function visible() {
  let all = load();
  if ($(".onlyhere").checked) all = all.filter(c => c.page === pageKey());
  if ($(".hidedone").checked) all = all.filter(c => !c.done);
  if (fsel.size) all = all.filter(c => c.labels.some(l => fsel.has(l)));
  return all;
}
const SEV = { low: "کم", mid: "متوسط", high: "زیاد" };
function renderList() {
  $(".warn").hidden = storageOK;
  const items = visible();
  list.innerHTML = items.length ? "" : '<div class="empty">هنوز کامنتی نیست. «+ کامنت تازه» را بزن و روی بخشی از صفحه کلیک کن.</div>';
  items.slice().reverse().forEach(c => {
    const d = document.createElement("div");
    d.className = "item" + (c.done ? " done" : "");
    const tags = c.labels.map(l => `<span class="tag" style="--c:${LMAP[l][2]}">${LMAP[l][1]}</span>`).join("");
    d.innerHTML = `<div class="meta">${tags}<span>اهمیت: ${SEV[c.sev] || ""}</span><span>· ${esc(c.title || c.page)}</span></div>
      ${c.quote || c.snip ? `<div class="q">${esc(c.quote || c.snip)}</div>` : ""}
      <div>${esc(c.text)}</div>
      <div class="acts"><a class="go">نشانم بده</a><a class="ed">ویرایش</a><a class="dn">${c.done ? "برگرداندن" : "انجام شد"}</a><a class="rm">حذف</a></div>`;
    d.querySelector(".go").onclick = () => {
      if (c.page !== pageKey()) { location.href = c.page; return; }
      const el = find(c.sel); if (!el) { toast("این بخش دیگر در صفحه پیدا نشد"); return; }
      panel.classList.remove("show");
      el.scrollIntoView({ behavior: "smooth", block: "center" });
      const r = () => { const b = el.getBoundingClientRect(); Object.assign(outline.style, { display: "block", left: b.left + "px", top: b.top + "px", width: b.width + "px", height: b.height + "px" }); };
      setTimeout(r, 450); setTimeout(() => { outline.style.display = "none"; }, 2600);
    };
    d.querySelector(".ed").onclick = ev => { panel.classList.remove("show"); openBox(c, innerWidth / 2, innerHeight / 3); };
    d.querySelector(".dn").onclick = () => { const all = load(); const x = all.find(y => y.id === c.id); x.done = !x.done; save(all); renderList(); renderPins(); updateCount(); };
    d.querySelector(".rm").onclick = () => { save(load().filter(y => y.id !== c.id)); renderList(); renderPins(); updateCount(); };
    list.appendChild(d);
  });
}
function esc(s) { return String(s || "").replace(/[&<>"]/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m])); }

/* ---------- export / import ---------- */
function asText(items) {
  const byPage = {};
  items.forEach(c => (byPage[c.title || c.page] ||= []).push(c));
  let out = "کامنت‌های بازبینی دانش‌سرا (" + fa(items.length) + " مورد)\n";
  for (const [p, cs] of Object.entries(byPage)) {
    out += "\n## " + p + "\n";
    cs.forEach((c, i) => {
      out += `${fa(i + 1)}. [${c.labels.map(l => LMAP[l][1]).join("، ") || "بدون برچسب"} · اهمیت ${SEV[c.sev]}]${c.done ? " (انجام شد)" : ""}\n`;
      if (c.quote || c.snip) out += `   روی: «${c.quote || c.snip}»\n`;
      out += `   ${c.text}\n   (صفحه: ${c.page} · جای دقیق: ${c.sel})\n`;
    });
  }
  return out;
}
$(".copy").onclick = async () => {
  const t = asText(visible());
  try { await navigator.clipboard.writeText(t); toast("کپی شد؛ در گفت‌وگو با Claude بچسبان"); }
  catch (e) {
    const ta = document.createElement("textarea"); ta.value = t; root.appendChild(ta); ta.select();
    try { document.execCommand("copy"); toast("کپی شد"); } catch (e2) { toast("کپی نشد؛ JSON را دانلود کن"); }
    ta.remove();
  }
};
$(".dl").onclick = () => {
  const blob = new Blob([JSON.stringify(load(), null, 1)], { type: "application/json" });
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
  a.download = "qa-daneshsara-" + new Date().toISOString().slice(0, 10) + ".json";
  root.appendChild(a); a.click(); a.remove();
};
const fileIn = root.querySelector('input[type=file]');
$(".imp").onclick = () => fileIn.click();
fileIn.onchange = async () => {
  const f = fileIn.files[0]; if (!f) return;
  try {
    const inc = JSON.parse(await f.text()); const all = load(); const ids = new Set(all.map(c => c.id));
    let n = 0; inc.forEach(c => { if (c && c.id && !ids.has(c.id)) { all.push(c); n++; } });
    save(all); renderList(); renderPins(); updateCount(); toast(fa(n) + " کامنت اضافه شد");
  } catch (e) { toast("فایل خوانده نشد"); }
  fileIn.value = "";
};
})();
