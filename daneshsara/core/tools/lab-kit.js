/* Shared helpers for the wiki labs. A page defines LAB = {wiki, labels, exps:{key:[tab, title, why, fn]}, first}
   and calls LabKit.start(LAB). Nothing is stored or sent. */
(function () {
  const K = {};
  K.fa = (x, d = 0) => {
    const s = (typeof x === "number") ? x.toLocaleString("en-US", {maximumFractionDigits: d, minimumFractionDigits: 0}) : String(x);
    return s.replace(/,/g, "٬").replace(/\./g, "٫").replace(/-/g, "−").replace(/\d/g, c => "۰۱۲۳۴۵۶۷۸۹"[c]);
  };
  K.css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim() || "#888";
  K.esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
  let LAB = null, cur = null;
  /* links to wiki entries: "slug" (this wiki) or "wiki:slug" (another wiki) */
  K.lk = ks => `<div class="links">${ks.map(k => {
    const [w, s] = k.includes(":") ? k.split(":") : [LAB.wiki, k];
    const href = w === LAB.wiki ? `../#${s}` : `../../${w}/#${s}`;
    return `<a href="${href}">${K.esc((LAB.labels || {})[k] || s)}</a>`;
  }).join("")}</div>`;
  K.$ = s => document.querySelector(s);
  K.open = k => {
    if (!LAB.exps[k]) k = LAB.first;
    cur = k;
    document.querySelectorAll("#tabs button").forEach(b => b.setAttribute("aria-pressed", b.dataset.k === k));
    const [, h, why, fn] = LAB.exps[k];
    document.getElementById("exp").innerHTML = `<h2>${h}</h2><p class="why">${why}</p><div class="panel" id="pn"></div><div id="out"></div>`;
    fn(document.getElementById("pn"), document.getElementById("out"));
    try { history.replaceState(null, "", "#" + k); } catch (_) {}
  };
  K.start = lab => {
    LAB = lab;
    const tabs = document.getElementById("tabs");
    tabs.innerHTML = Object.entries(lab.exps).map(([k, v]) => `<button type="button" data-k="${k}">${v[0]}</button>`).join("");
    tabs.addEventListener("click", e => { const b = e.target.closest("[data-k]"); if (b) K.open(b.dataset.k); });
    K.open((location.hash || "").slice(1) || lab.first);
    window.addEventListener("hashchange", () => { const k = location.hash.slice(1); if (k !== cur && lab.exps[k]) K.open(k); });
  };
  /* "guess first": Q = [[question, min, max, step, answer, explanation, unit, links, source]] */
  K.guess = Q => pn => {
    pn.innerHTML = Q.map((q, i) => `<div class="q"><p>${K.fa(i + 1)}. ${q[0]}</p><label class="field">حدس شما: <b id="gv${i}"></b><input type="range" id="g${i}" min="${q[1]}" max="${q[2]}" step="${q[3]}" value="${(q[1] + q[2]) / 2}"></label><div><button type="button" class="btn ghost" data-i="${i}">پاسخ</button></div><div id="ga${i}"></div></div>`).join("");
    Q.forEach((q, i) => { const r = pn.querySelector("#g" + i), o = pn.querySelector("#gv" + i); const u = () => o.textContent = K.fa(+r.value, 1) + q[6]; r.addEventListener("input", u); u(); });
    pn.addEventListener("click", e => {
      const b = e.target.closest("[data-i]"); if (!b) return;
      const i = +b.dataset.i, q = Q[i], g = +pn.querySelector("#g" + i).value, off = Math.abs(g - q[4]) / (q[2] - q[1]);
      pn.querySelector("#ga" + i).innerHTML = `<div class="ans"><b>${off < .08 ? "تقریباً درست!" : off < .25 ? "نزدیک بود." : "دور بود — و بیشتر مردم هم دور حدس می‌زنند."}</b> پاسخ: حدود ${K.fa(q[4], 1)}${q[6]}. ${q[5]}${q[8] ? `<span class="src">منبع: ${q[8]}</span>` : ""}${K.lk(q[7])}</div>`;
      b.remove();
    });
  };
  window.LabKit = K;
})();
