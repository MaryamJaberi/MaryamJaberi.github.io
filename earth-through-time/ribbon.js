/* Time ribbon: the whole of time in one band above the slider.
   Log scale so that both billions of years and the last centuries are visible; geological eons as bands;
   a second, true-to-scale strip shows how thin the human part really is. Click a dot to go to that stop. */
(function () {
  var eras = window.EARTH_ERAS || [];
  var slider = document.getElementById("time-slider");
  var rail = document.querySelector(".rail");
  if (!slider || !rail || !eras.length) return;
  var NOW = 2026;
  function lang() { try { return localStorage.getItem("earth-time-lang") === "en" ? "en" : "fa"; } catch (e) { return "fa"; } }
  function faNum(s) { return lang() === "fa" ? String(s).replace(/\d/g, function (d) { return "۰۱۲۳۴۵۶۷۸۹"[d]; }) : String(s); }

  // years before 2026 (negative = future), read from the English year label
  function yearsAgo(era) {
    var y = era.yearLabel || "";
    var m = y.match(/([\d.,]+)\s*(billion|million)?\s*years ago/i);
    if (m) return parseFloat(m[1].replace(/,/g, "")) * (m[2] ? (/billion/i.test(m[2]) ? 1e9 : 1e6) : 1);
    m = y.match(/(\d+)\s*BCE/i);
    if (m) return NOW + Number(m[1]);
    m = y.match(/(\d+)\s*CE/i);
    if (m) return NOW - Number(m[1]);
    return 0;
  }
  // position 0..1, left = beginning of time; past is log-scaled, "now" sits at 0.84, the future takes the rest
  var NOWX = 0.84;
  var LMAX = Math.log10(13.8e9);
  function px(ya) {
    if (ya > 0) return NOWX * (1 - Math.log10(ya + 1) / LMAX);
    if (ya < 0) return NOWX + (1 - NOWX) * (Math.log10(-ya + 1) / 3);
    return NOWX;
  }
  // ICS eons and eras (years ago); labels in both languages
  var BANDS = [
    { a: 13.8e9, b: 4.54e9, fa: "کیهان پیش از زمین", en: "Before Earth", c: "#26324a" },
    { a: 4.54e9, b: 4.0e9, fa: "هادئن", en: "Hadean", c: "#5a2a22" },
    { a: 4.0e9, b: 2.5e9, fa: "آرکئن", en: "Archean", c: "#6b3d4f" },
    { a: 2.5e9, b: 538.8e6, fa: "پروتروزوئیک", en: "Proterozoic", c: "#71455f" },
    { a: 538.8e6, b: 251.9e6, fa: "پالئوزوئیک", en: "Paleozoic", c: "#3d6b62" },
    { a: 251.9e6, b: 66e6, fa: "مزوزوئیک", en: "Mesozoic", c: "#4f7a43" },
    { a: 66e6, b: 7e6, fa: "سنوزوئیک", en: "Cenozoic", c: "#8a7a3a" },
    { a: 7e6, b: 0, fa: "داستان انسان", en: "Human story", c: "#a8743c" },
  ];
  var CAT = { cosmos: "#8bb4d6", geology: "#c99a6b", life: "#7fbf8f", climate: "#79b8c9", humans: "#e0a96d", science: "#c9a7e0", present: "#f0d9b0", future: "#9aa3b2" };

  var box = document.createElement("div");
  box.className = "ribbon";
  rail.parentNode.insertBefore(box, rail);
  var W = 1000;
  var ys = eras.map(yearsAgo);

  function draw() {
    W = Math.max(300, box.clientWidth || 1000);
    aria();
    var i = Number(slider.value) || 0;
    var en = lang() === "en";
    var bands = BANDS.map(function (b) {
      var x1 = px(b.a) * W, x2 = px(b.b) * W, w = x2 - x1, name = en ? b.en : b.fa;
      var fits = w > name.length * (en ? 6.4 : 6.8) + 8;
      return '<rect x="' + x1.toFixed(1) + '" y="14" width="' + w.toFixed(1) + '" height="20" fill="' + b.c + '"><title>' + name + "</title></rect>" +
        (fits ? '<text class="band" x="' + ((x1 + x2) / 2).toFixed(1) + '" y="28">' + name + "</text>" : "");
    }).join("");
    var future = '<rect x="' + (NOWX * W).toFixed(1) + '" y="14" width="' + ((1 - NOWX) * W).toFixed(1) + '" height="20" fill="url(#rb-future)"/>' +
      '<text class="band" x="' + ((NOWX + (1 - NOWX) / 2) * W).toFixed(1) + '" y="28">' + (en ? "Projection" : "پیش‌بینی") + "</text>";
    // a few scale marks so the log scale is honest about itself
    var marks = [[1e9, en ? "1 bn" : "۱ میلیارد"], [1e8, en ? "100 m" : "۱۰۰ میلیون"], [1e7, en ? "10 m" : "۱۰ میلیون"], [1e6, en ? "1 m" : "۱ میلیون"], [1e5, en ? "100 k" : "۱۰۰ هزار"], [1e4, en ? "10 k" : "۱۰ هزار"], [1e3, en ? "1 k" : "هزار"], [1e2, en ? "100 y" : "صد سال"]]
      .filter(function (m, k, all) { return W > 700 || k % 2 === 0; })
      .map(function (m) { var x = px(m[0]) * W; return '<line class="mk" x1="' + x.toFixed(1) + '" x2="' + x.toFixed(1) + '" y1="34" y2="40"/><text class="mk" x="' + x.toFixed(1) + '" y="50">' + m[1] + "</text>"; }).join("");
    var dots = eras.map(function (era, k) {
      var x = px(ys[k]) * W, on = k === i, c = CAT[era.category] || "#d4b88c";
      var label = (era.titleFa && !en ? era.titleFa : era.title) + " · " + (en ? era.yearLabel : (era.yearLabelFa || era.yearLabel));
      return '<g class="rb-dot' + (on ? " on" : "") + '" data-i="' + k + '" tabindex="-1"><title>' + label.replace(/</g, "&lt;") + '</title><line x1="' + x.toFixed(1) + '" x2="' + x.toFixed(1) + '" y1="6" y2="14" stroke="' + c + '"/><circle cx="' + x.toFixed(1) + '" cy="6" r="' + (on ? 5.5 : 3.2) + '" fill="' + c + '"/></g>';
    }).join("");
    var nowX = NOWX * W;
    var now = '<line class="now" x1="' + nowX + '" x2="' + nowX + '" y1="10" y2="40"/><text class="now" x="' + nowX + '" y="62">' + (en ? "now" : "اکنون") + "</text>";

    // true-to-scale strip: on a linear clock the whole human story is a hairline
    var span = 4.54e9;
    var cur = ys[i];
    var lin = cur > span ? 0 : cur > 0 ? 1 - cur / span : 1;
    var humanW = Math.max(0.6, (7e6 / span) * W);
    var strip = '<g class="lin" transform="translate(0,80)"><text class="lin-t" x="' + (W / 2) + '" y="-4">' + (en ? "True scale: Earth's 4.54 billion years" : "مقیاس واقعی: ۴٫۵۴ میلیارد سال زمین") + "</text>" + '<rect x="0" y="0" width="' + W + '" height="7" rx="3.5" class="lin-bg"/><rect x="' + (W - humanW).toFixed(2) + '" y="0" width="' + humanW.toFixed(2) + '" height="7" class="lin-human"/>' +
      '<line x1="' + (lin * W).toFixed(1) + '" x2="' + (lin * W).toFixed(1) + '" y1="-3" y2="10" class="lin-cur"/></g>';
    var sapiensSec = Math.round((300e3 / span) * 86400);
    var note = en
      ? "Top: log scale, so billions of years and the last centuries both fit. Bottom bar: Earth's 4.54 billion years at true scale; the gold sliver at the end is the whole human story. On a 24-hour clock of Earth, Homo sapiens (about 300,000 years) takes the last " + sapiensSec + " seconds."
      : "بالا: مقیاس لگاریتمی، تا هم میلیاردها سال و هم چند قرن اخیر جا شوند. نوار پایین: ۴٫۵۴ میلیارد سال زمین به مقیاس واقعی؛ آن باریکهٔ طلایی ته نوار، کل داستان انسان است. اگر تاریخ زمین ۲۴ ساعت بود، انسان خردمند (حدود ۳۰۰ هزار سال) فقط " + faNum(sapiensSec) + " ثانیهٔ آخر را می‌گرفت.";
    box.innerHTML = '<svg viewBox="0 -6 ' + W + ' 98" role="img" aria-label="' + (en ? "All of time on one band" : "همهٔ زمان روی یک نوار") + '"><defs><linearGradient id="rb-future"><stop offset="0" stop-color="#9aa3b2" stop-opacity=".45"/><stop offset="1" stop-color="#9aa3b2" stop-opacity=".05"/></linearGradient></defs>' +
      bands + future + marks + now + dots + strip + "</svg><details class=\"rb-note\"><summary>" + (en ? "How to read this band" : "این نوار را چطور بخوانم؟") + "</summary>" + note + "</details>";
  }
  // the band itself is the control: tap, or drag along it, and it snaps to the nearest stop
  function go(k) {
    if (String(k) === slider.value) return;
    slider.value = String(k);
    slider.dispatchEvent(new Event("input"));
    slider.dispatchEvent(new Event("change"));
  }
  function nearest(clientX) {
    var svg = box.querySelector("svg");
    var r = svg.getBoundingClientRect(), x = (clientX - r.left) / r.width, best = 0, d = 9;
    ys.forEach(function (ya, k) { var dd = Math.abs(px(ya) - x); if (dd < d) { d = dd; best = k; } });
    return best;
  }
  var dragging = false;
  box.addEventListener("pointerdown", function (ev) {
    if (!ev.target.closest("svg")) return;
    dragging = true;
    box.setPointerCapture(ev.pointerId);
    go(nearest(ev.clientX));
  });
  box.addEventListener("pointermove", function (ev) { if (dragging) go(nearest(ev.clientX)); });
  box.addEventListener("pointerup", function () { dragging = false; });
  box.addEventListener("pointercancel", function () { dragging = false; });
  box.tabIndex = 0;
  box.setAttribute("role", "slider");
  box.addEventListener("keydown", function (ev) {
    var i = Number(slider.value) || 0;
    if (ev.key === "ArrowLeft" || ev.key === "ArrowDown") { ev.preventDefault(); go(Math.max(0, i - 1)); }
    else if (ev.key === "ArrowRight" || ev.key === "ArrowUp") { ev.preventDefault(); go(Math.min(eras.length - 1, i + 1)); }
    else if (ev.key === "Home") { ev.preventDefault(); go(0); }
    else if (ev.key === "End") { ev.preventDefault(); go(eras.length - 1); }
  });
  function aria() {
    var era = eras[Number(slider.value) || 0];
    box.setAttribute("aria-valuemin", "0");
    box.setAttribute("aria-valuemax", String(eras.length - 1));
    box.setAttribute("aria-valuenow", slider.value);
    box.setAttribute("aria-valuetext", (lang() === "en" ? era.yearLabel : era.yearLabelFa || era.yearLabel) + " · " + (lang() === "en" ? era.title : era.titleFa || era.title));
    box.setAttribute("aria-label", lang() === "en" ? "Time" : "زمان");
  }
  ["input", "change"].forEach(function (ev) { slider.addEventListener(ev, function () { setTimeout(draw, 0); }); });
  document.addEventListener("click", function (ev) { if (ev.target.closest && ev.target.closest("button")) setTimeout(draw, 0); });
  var last = 0;
  window.addEventListener("resize", function () { if (Math.abs((box.clientWidth || 0) - last) > 4) { last = box.clientWidth; draw(); } });
  draw();
})();
