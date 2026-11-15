/* The living layer: relative times, Rotterdam's sky behind the home screen, and the loom. */
(() => {
  const lang = document.documentElement.lang || "en";
  const DAY = 864e5;

  // "2 hours ago" for every <time data-rel>
  const rtf = window.Intl && Intl.RelativeTimeFormat ? new Intl.RelativeTimeFormat(lang, { numeric: "auto" }) : null;
  if (rtf) document.querySelectorAll("time[data-rel]").forEach(el => {
    const t = Date.parse(el.getAttribute("datetime"));
    if (isNaN(t)) return;
    const min = Math.round((t - Date.now()) / 6e4);
    if (min > 5) return;
    const [v, u] = Math.abs(min) < 60 ? [min, "minute"] : Math.abs(min) < 1440 ? [Math.round(min / 60), "hour"]
      : Math.abs(min) < 43200 ? [Math.round(min / 1440), "day"] : [null];
    if (v !== null) el.textContent = rtf.format(v, u);
  });

  // Sun altitude over Rotterdam, in degrees
  function sunAltitude(date, lat = 51.92, lon = 4.48) {
    const r = Math.PI / 180, d = date / DAY + 2440587.5 - 2451545;
    const g = (357.529 + 0.98560028 * d) * r, q = 280.459 + 0.98564736 * d;
    const L = (q + 1.915 * Math.sin(g) + 0.02 * Math.sin(2 * g)) * r, e = (23.439 - 3.6e-7 * d) * r;
    const ra = Math.atan2(Math.cos(e) * Math.sin(L), Math.cos(L)), dec = Math.asin(Math.sin(e) * Math.sin(L));
    const gmst = ((18.697374558 + 24.06570982441908 * d) % 24) * 15;
    const H = (gmst + lon) * r - ra;
    return Math.asin(Math.sin(lat * r) * Math.sin(dec) + Math.cos(lat * r) * Math.cos(dec) * Math.cos(H)) / r;
  }
  const home = document.querySelector("[data-sky]");
  if (home) {
    const a = sunAltitude(Date.now());
    const sky = a < -12 ? ["#191335", "#33245C", 1] : a < -4 ? ["#262563", "#7B4F93", 1]
      : a < 4 ? ["#F0B6A4", "#D9C2EC", 0] : a < 18 ? ["#EADFF6", "#FAE0DD", 0] : ["#E4E6FA", "#F6E4EE", 0];
    home.style.background = `linear-gradient(165deg,${sky[0]},${sky[1]})`;
    if (sky[2]) {
      home.classList.add("night");
      const ns = "http://www.w3.org/2000/svg", svg = document.createElementNS(ns, "svg");
      svg.setAttribute("class", "stars"); svg.setAttribute("aria-hidden", "true");
      svg.setAttribute("viewBox", "0 0 100 100"); svg.setAttribute("preserveAspectRatio", "none");
      let s = 7;
      const rnd = () => (s = (s * 9301 + 49297) % 233280) / 233280;
      for (let i = 0; i < 26; i++) {
        const c = document.createElementNS(ns, "circle");
        c.setAttribute("cx", (rnd() * 100).toFixed(1)); c.setAttribute("cy", (rnd() * 100).toFixed(1));
        c.setAttribute("r", (0.18 + rnd() * 0.32).toFixed(2)); c.setAttribute("opacity", (0.3 + rnd() * 0.6).toFixed(2));
        svg.appendChild(c);
      }
      home.prepend(svg);
    }
    const cap = home.querySelector(".sky-cap");
    if (cap) cap.hidden = false;
  }

  // The loom: move the shuttle to this week, and weave once when it comes into view
  const fig = document.querySelector(".loom-fig");
  if (!fig) return;
  const sh = fig.querySelector(".shuttle");
  if (sh) {
    const start = Date.parse(sh.dataset.start + "T00:00:00");
    const i = Math.floor((Date.now() - start) / (7 * DAY)) - +sh.dataset.w0;
    if (i >= 0 && i < 52) {
      const x0 = +sh.dataset.x0, cw = +sh.dataset.cw, w = +sh.dataset.w;
      const cx = sh.dataset.rtl === "1" ? w - x0 - i * cw - cw / 2 : x0 + i * cw + cw / 2;
      sh.firstElementChild.setAttribute("transform", `translate(${cx} 0)`);
    }
  }
  // A label that follows the cursor (or the finger) over the knots
  const tip = document.createElement("div");
  tip.className = "knot-tip"; tip.setAttribute("aria-hidden", "true");
  fig.appendChild(tip);
  fig.querySelectorAll(".knot").forEach(k => {
    const ttl = k.querySelector("title");
    if (ttl) { k.dataset.tip = ttl.textContent; k.setAttribute("aria-label", ttl.textContent); ttl.remove(); }
  });
  const place = e => {
    const r = fig.getBoundingClientRect();
    tip.style.left = Math.min(Math.max(e.clientX - r.left, 90), r.width - 90) + "px";
    tip.style.top = (e.clientY - r.top) + "px";
  };
  fig.addEventListener("pointerover", e => {
    const k = e.target.closest(".knot");
    if (!k) return;
    tip.textContent = k.dataset.tip; place(e); tip.classList.add("on");
  });
  fig.addEventListener("pointermove", e => { if (tip.classList.contains("on")) place(e); });
  fig.addEventListener("pointerout", e => { if (e.target.closest(".knot")) tip.classList.remove("on"); });

  if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  fig.classList.add("js");
  const io = new IntersectionObserver(es => {
    if (es.some(e => e.isIntersecting)) { fig.classList.add("in"); io.disconnect(); }
  }, { threshold: 0.35 });
  io.observe(fig);
})();
