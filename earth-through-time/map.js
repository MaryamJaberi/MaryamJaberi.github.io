/* Atlas maps. Modern-era maps use real coastlines (Natural Earth, via land.js) in an equirectangular
   projection. Deep-time maps are schematic teaching sketches and are labeled that way. */
(function () {
  var W = 800, H = 440, TOP = 20, SPAN = 400;
  function px(lon, lat) { return [(lon + 180) / 360 * W, (90 - lat) / 180 * SPAN + TOP]; }
  function f1(n) { return Math.round(n * 10) / 10; }
  function pts(ring) { return ring.map(function (p) { var q = px(p[0], p[1]); return f1(q[0]) + " " + f1(q[1]); }); }
  function poly(ring) { return "M" + pts(ring).join(" L") + " Z"; }


  function cont(k, dlon, dlat, rot, sc) {
    var c = window.CONT && window.CONT[k]; if (!c) return "";
    var cp = px(c.c[0], c.c[1]), ox = dlon / 360 * W, oy = -dlat / 180 * SPAN;
    var d = c.p.map(function (r) { return poly(r); }).join(" ");
    return '<path d="' + d + '" transform="translate(' + f1(ox) + " " + f1(oy) + ") rotate(" + (rot || 0) + " " + f1(cp[0]) + " " + f1(cp[1]) + ") translate(" + f1(cp[0]) + " " + f1(cp[1]) + ") scale(" + (sc || 1) + ") translate(" + f1(-cp[0]) + " " + f1(-cp[1]) + ')" fill="' + LAND_FILL + '" fill-opacity=".92" stroke="' + LAND_STROKE + '" stroke-width=".8" stroke-linejoin="round"/>';
  }
  function assemble(P) { return ocean() + graticule() + Object.keys(P).map(function (k) { var a = P[k]; return cont(k, a[0], a[1], a[2], a[3]); }).join(""); }
  /* Schematic positions: each modern continent moved and turned as a rigid piece. Approximate, for teaching. */
  var PANGAEA = { Afr: [0, 8, 0, 1], SAm: [48, 22, -35, 1], NAm: [62, -26, 28, 0.95], Eur: [14, -14, 10, 0.95], Asia: [-4, -22, 0, 0.88], Ind: [-12, -40, 0, 1], Ant: [30, 62, 0, 1], Aus: [-58, 55, 0, 1] };
  var PANGAEA_EARLY = { Afr: [0, 6, 0, 1], SAm: [42, 20, -30, 1], NAm: [52, -22, 22, 0.95], Eur: [10, -12, 8, 0.95], Asia: [-14, -18, 0, 0.9], Ind: [-8, -38, 0, 1], Ant: [26, 58, 0, 1], Aus: [-50, 50, 0, 1] };
  var JURASSIC = { Afr: [4, 5, 0, 1], SAm: [30, 16, -22, 1], NAm: [32, -18, 14, 0.97], Eur: [8, -8, 4, 0.97], Asia: [-6, -14, 0, 0.92], Ind: [-8, -34, 0, 1], Ant: [14, 50, 0, 1], Aus: [-38, 44, 0, 1] };


  function shape(d) { return '<path d="' + d + '" fill="' + LAND_FILL + '" fill-opacity=".95" stroke="' + LAND_STROKE + '" stroke-width="1.2" stroke-linejoin="round"/>'; }
  var PANG_EARLY = "M300 120 C360 90 440 100 480 150 C520 200 500 260 470 310 C440 370 380 390 330 360 C270 330 250 270 270 220 C280 170 280 140 300 120 Z";
  var LAURASIA = "M150 110 C220 70 330 80 400 100 C470 90 560 100 620 130 C650 160 600 190 540 185 C470 200 400 190 340 200 C280 205 230 190 190 175 C150 160 120 130 150 110 Z";
  var GONDWANA = "M250 235 C310 215 380 225 430 245 C480 235 520 260 510 310 C500 360 440 400 380 395 C330 405 290 380 275 340 C240 310 225 260 250 235 Z";
  var INDIA_J = "M520 330 C545 322 560 345 548 372 C535 385 518 365 520 330 Z";

  var landCache = null;
  function landPath() {
    if (landCache) return landCache;
    var d = [];
    var feats = (window.LAND && window.LAND.features) || [];
    feats.forEach(function (ft) {
      var g = ft.geometry; if (!g) return;
      var polys = g.type === "Polygon" ? [g.coordinates] : g.coordinates;
      polys.forEach(function (p) { p.forEach(function (ring) { d.push(poly(ring)); }); });
    });
    landCache = d.join(" ");
    return landCache;
  }

  var LAND_FILL = "#c4a074", LAND_STROKE = "#8a6a45";
  function ocean() {
    return '<rect x="0" y="0" width="' + W + '" height="' + H + '" fill="#0b1c2c"/>' +
           '<rect x="0" y="0" width="' + W + '" height="' + H + '" fill="#16344f" opacity=".55"/>';
  }
  function graticule() {
    var out = "";
    [[0, "equator"], [23.4, ""], [-23.4, ""]].forEach(function (r) {
      var y = px(0, r[0])[1];
      out += '<line x1="0" x2="' + W + '" y1="' + f1(y) + '" y2="' + f1(y) + '" stroke="#8bb4d6" stroke-opacity="' + (r[0] === 0 ? ".22" : ".12") + '" stroke-dasharray="3 5"/>';
    });
    var x0 = px(0, 0)[0];
    out += '<line y1="' + TOP + '" y2="' + (TOP + SPAN) + '" x1="' + f1(x0) + '" x2="' + f1(x0) + '" stroke="#8bb4d6" stroke-opacity=".12" stroke-dasharray="3 5"/>';
    return out;
  }
  function realLand(opacity, dashed) {
    return '<path d="' + landPath() + '" fill="' + (dashed ? "none" : LAND_FILL) + '" fill-opacity="' + (opacity || 1) +
           '" stroke="' + LAND_STROKE + '" stroke-width=".7" ' + (dashed ? 'stroke-dasharray="3 3" stroke-opacity=".8"' : "") + '/>';
  }
  function blob(cx, cy, rx, ry, rot) {
    return '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx + '" ry="' + ry + '" transform="rotate(' + rot + " " + cx + " " + cy +
           ')" fill="' + LAND_FILL + '" stroke="' + LAND_STROKE + '" stroke-width="1"/>';
  }
  function pangaeaPath() {
    return "M330 80 C380 70 430 90 450 140 C500 150 530 190 520 240 C560 270 540 330 500 360 C470 410 390 420 340 390 C280 400 240 350 250 300 C200 260 220 190 260 160 C270 120 300 90 330 80 Z";
  }
  function ice(ring, op) { return '<path d="' + poly(ring) + '" fill="#d7e6f5" fill-opacity="' + (op || 0.85) + '" stroke="#eaf3fb" stroke-opacity=".7" stroke-width=".8"/>'; }

  /* Approximate last-glacial-maximum ice (rough outlines for orientation only). */
  var ICE = [
    [[-128, 60], [-124, 69], [-108, 73], [-88, 74], [-72, 71], [-62, 63], [-59, 55], [-66, 47], [-75, 43], [-90, 41], [-102, 45], [-114, 49], [-124, 53]],
    [[-8, 54], [-2, 59], [6, 62], [4, 70], [18, 72], [38, 69], [60, 69], [62, 60], [46, 55], [32, 53], [18, 52], [8, 53]],
    [[-74, -55], [-69, -41], [-72, -38], [-75, -47]],
    [[-50, 61], [-42, 60], [-20, 70], [-18, 82], [-58, 83], [-70, 77]]
  ];
  /* Western Interior Seaway (rough). */
  var WIS = [[-113, 57], [-101, 58], [-95, 49], [-96, 37], [-101, 29], [-107, 33], [-110, 43]];

  /* Low-lying coasts and deltas often named in sea-level risk work. Markers, not a flood map. */
  var RISK = {
    bd: { ll: [90, 22.5], en: "Ganges–Brahmaputra delta", fa: "دلتای گنگ و براهماپوترا", dx: 9, dy: 4, a: "start" },
    nile: { ll: [31, 31], en: "Nile delta", fa: "دلتای نیل", dx: -9, dy: -7, a: "end" },
    mekong: { ll: [105.8, 10], en: "Mekong delta", fa: "دلتای مکونگ", dx: 9, dy: 14, a: "start" },
    yangtze: { ll: [121.5, 31.2], en: "Yangtze delta", fa: "دلتای یانگ‌تسه", dx: 9, dy: -2, a: "start" },
    nl: { ll: [4.5, 52.5], en: "Netherlands & North Sea", fa: "هلند و دریای شمال", dx: -9, dy: -6, a: "end" },
    gulf: { ll: [-88, 29.5], en: "US Gulf coast & Florida", fa: "کرانهٔ خلیج مکزیک و فلوریدا", dx: -9, dy: 4, a: "end" },
    khz: { ll: [48.5, 30.2], en: "Shatt al-Arab & Khuzestan", fa: "اروندرود و خوزستان", dx: 9, dy: -7, a: "start" },
    mald: { ll: [73, 3.2], en: "Maldives & atolls", fa: "مالدیو و جزیره‌های مرجانی", dx: -9, dy: 16, a: "end" },
    jkt: { ll: [106.8, -6.2], en: "Jakarta", fa: "جاکارتا", dx: 9, dy: 4, a: "start" },
    niger: { ll: [6, 5], en: "Niger delta", fa: "دلتای نیجر", dx: -9, dy: 4, a: "end" }
  };
  function markers(keys, r, halo, lang) {
    var out = "";
    keys.forEach(function (k) {
      var m = RISK[k], p = px(m.ll[0], m.ll[1]);
      if (halo) out += '<circle cx="' + f1(p[0]) + '" cy="' + f1(p[1]) + '" r="' + halo + '" fill="#2d8fd6" fill-opacity=".28"/>';
      out += '<circle cx="' + f1(p[0]) + '" cy="' + f1(p[1]) + '" r="' + r + '" fill="#4aa8e8" stroke="#d6ecff" stroke-width="1.2"/>';
      out += '<text x="' + f1(p[0] + m.dx) + '" y="' + f1(p[1] + m.dy) + '" text-anchor="' + m.a + '" fill="#d6e6f5" font-size="11" paint-order="stroke" stroke="#0b1c2c" stroke-width="3" stroke-linejoin="round">' + (lang === "fa" ? m.fa : m.en) + "</text>";
    });
    return out;
  }

  var LABELS = {
    cosmos: ["No Earth yet — expanding space", "هنوز زمینی نیست؛ فضا در حال گسترش است"],
    molten: ["Magma ocean after accretion and the Moon-forming impact", "اقیانوس مذاب پس از انباشت و برخوردی که ماه را ساخت"],
    archean: ["Small protocontinents in a global ocean — schematic", "قاره‌های کوچک نوپا در اقیانوسی سراسری — طرح"],
    kenorland: ["Kenorland-style clustering — schematic, not a survey map", "چیدمان به‌سبک کنورلند — طرح، نه نقشهٔ برداشت‌شده"],
    columbia: ["Columbia / Nuna assembled — schematic", "ابرقارهٔ کلمبیا / نونا — طرح"],
    rodinia: ["Rodinia clustered — schematic reconstruction", "رودینیا گرد هم آمده — بازسازی طرح‌وار"],
    pannotia: ["Pannotia / Greater Gondwana gathering — schematic", "گردآمدن پانوتیا / گندوانای بزرگ — طرح"],
    cambrian: ["Gondwana south; Laurentia, Baltica, Siberia separate — schematic", "گندوانا در جنوب؛ لورنشیا، بالتیکا و سیبری جدا — طرح"],
    devonian: ["Gondwana and Euramerica approaching — schematic", "نزدیک‌شدن گندوانا و اورامریکا — طرح"],
    "pangaea-early": ["Pangaea assembling — schematic C-shape beginning", "شکل‌گیری پانگه‌آ؛ آغاز شکل C — طرح"],
    pangaea: ["Pangaea, one supercontinent around 250 million years ago — schematic outline, not real coastlines", "پانگه‌آ، ابرقاره‌ای یکپارچه حدود ۲۵۰ میلیون سال پیش — طرح کلی، نه کرانه‌های واقعی"],
    jurassic: ["Two great landmasses, Laurasia (north) and Gondwana (south), with the Tethys Sea between — schematic outline", "دو توده‌ی بزرگ خشکی: لوراسیا (شمال) و گندوانا (جنوب)، با دریای تتیس میانشان — طرح کلی"],
    cretaceous: ["Dashed lines are today's coasts, for orientation only; high seas flooded the continents (blue: Western Interior Seaway)", "خطچین‌ها کرانه‌های امروزند، فقط برای جهت‌یابی؛ دریاهای بلند بخش‌هایی از قاره‌ها را پوشانده بودند (آبی: دریای درونیِ غرب آمریکای شمالی)"],
    paleocene: ["Dashed lines are today's coasts, for orientation only; India was still crossing the Indian Ocean", "خطچین‌ها کرانه‌های امروزند، فقط برای جهت‌یابی؛ هند هنوز اقیانوس هند را می‌پیمود"],
    eocene: ["Dashed lines are today's coasts, for orientation only; the Himalayan collision is beginning", "خطچین‌ها کرانه‌های امروزند، فقط برای جهت‌یابی؛ برخورد هیمالیا آغاز می‌شود"],
    iceage: ["Today's coasts with rough ice-sheet outlines; sea level was about 120 m lower, so shelves and land bridges were dry", "کرانه‌های امروز با طرح تقریبی ورقه‌های یخی؛ سطح دریا حدود ۱۲۰ متر پایین‌تر بود و فلات‌ها و پل‌های خشکی بیرون بودند"],
    modern: ["Modern coastlines (Natural Earth)", "کرانه‌های امروز (داده‌های نقشهٔ طبیعی-زمین)"],
    "future-near": ["Same map. The change is in climate and living systems, not in continents.", "همین نقشه. تغییر در اقلیم و نظام‌های زنده است، نه در قاره‌ها."],
    "future-century": ["Blue dots: low coasts and deltas most exposed to higher seas. Markers, not a flood map.", "نقطه‌های آبی: کرانه‌ها و دلتاهای کم‌ارتفاعی که بیش از همه در معرض بالا آمدن دریا هستند. نشانه‌گذاری است، نه نقشهٔ سیل."],
    "future-far": ["Blue halos: coastal zones that could be reshaped over centuries on a high-emission path. How far the sea reaches here is unknown; this is not a flood map.", "هاله‌های آبی: پهنه‌های ساحلی که در مسیر پرانتشار طی سده‌ها ممکن است دگرگون شوند. اینکه دریا تا کجا می‌رسد نامعلوم است؛ این نقشهٔ سیل نیست."]
  };
  var NOTE = {
    real: ["Natural Earth coastlines. Educational map, not a survey.", "خط‌های ساحلی طبیعی-زمین. نقشهٔ آموزشی است، نه نقشهٔ برداشت‌شده."],
    sketch: ["Teaching sketch, not a surveyed paleomap.", "طرح آموزشی است، نه نقشهٔ دیرین‌جغرافیایی برداشت‌شده."]
  };
  var REAL = { cretaceous: 1, paleocene: 1, eocene: 1, iceage: 1, modern: 1, "future-near": 1, "future-century": 1, "future-far": 1 };

  var DRAW = {
    cosmos: function () {
      return '<rect width="800" height="440" fill="#070b14"/>' +
        '<circle cx="200" cy="200" r="3" fill="#fff"/><circle cx="320" cy="140" r="2" fill="#fff"/><circle cx="520" cy="220" r="2.4" fill="#fff"/><circle cx="610" cy="90" r="1.6" fill="#fff"/><circle cx="140" cy="80" r="1.8" fill="#fff"/>' +
        '<ellipse cx="400" cy="210" rx="70" ry="28" fill="none" stroke="#8bb4d6" stroke-opacity=".45"/><ellipse cx="400" cy="210" rx="120" ry="48" fill="none" stroke="#8bb4d6" stroke-opacity=".25"/>' +
        '<circle cx="400" cy="210" r="10" fill="#f0d9b0"/>';
    },
    molten: function () {
      return ocean() + '<ellipse cx="400" cy="220" rx="210" ry="200" fill="#6a2a1e"/><ellipse cx="380" cy="200" rx="160" ry="150" fill="#a43b22"/><ellipse cx="360" cy="190" rx="70" ry="50" fill="#e07a3a"/>';
    },
    archean: function () { return ocean() + blob(300, 210, 70, 40, 12) + blob(470, 250, 55, 32, -20) + blob(520, 160, 40, 24, 30); },
    kenorland: function () { return ocean() + blob(360, 200, 140, 80, -15) + blob(500, 260, 70, 40, 20); },
    columbia: function () { return ocean() + blob(390, 210, 170, 95, -8) + blob(250, 280, 50, 30, 10); },
    rodinia: function () { return ocean() + blob(410, 200, 160, 110, 18) + blob(300, 160, 55, 35, -30); },
    pannotia: function () { return ocean() + blob(420, 260, 150, 100, -25) + blob(280, 160, 60, 40, 10) + blob(560, 150, 45, 30, 0); },
    cambrian: function () { return ocean() + blob(430, 300, 180, 90, -20) + blob(280, 170, 70, 45, 15) + blob(520, 150, 50, 32, -10) + blob(610, 200, 36, 24, 25); },
    devonian: function () { return ocean() + blob(440, 300, 175, 95, -18) + blob(300, 180, 100, 50, 8) + blob(560, 160, 40, 28, 0); },
    "pangaea-early": function () { return ocean() + graticule() + shape(PANG_EARLY); },
    pangaea: function () { return ocean() + graticule() + shape(pangaeaPath()); },
    jurassic: function () { return ocean() + graticule() + shape(LAURASIA) + shape(GONDWANA) + shape(INDIA_J); },
    cretaceous: function () {
      return ocean() + graticule() + realLand(0.28, false) + realLand(1, true) +
        '<path d="' + poly(WIS) + '" fill="#2d8fd6" fill-opacity=".6"/>';
    },
    paleocene: function () { return ocean() + graticule() + realLand(0.28, false) + realLand(1, true); },
    eocene: function () { return ocean() + graticule() + realLand(0.34, false) + realLand(1, true); },
    iceage: function () {
      return ocean() + graticule() + realLand(1, false) + ICE.map(function (r) { return ice(r); }).join("");
    },
    modern: function () { return ocean() + graticule() + realLand(1, false); },
    "future-near": function () { return ocean() + graticule() + realLand(1, false); },
    "future-century": function (lang) {
      return ocean() + graticule() + realLand(1, false) + markers(["bd", "nile", "mekong", "yangtze", "nl", "gulf", "khz", "mald"], 4.5, 0, lang);
    },
    "future-far": function (lang) {
      return ocean() + graticule() + realLand(1, false) + markers(["bd", "nile", "mekong", "yangtze", "nl", "gulf", "khz", "mald", "jkt", "niger"], 4.5, 15, lang);
    }
  };

  window.EarthMaps = {
    render: function (era, lang) {
      var key = DRAW[era.map] ? era.map : "modern";
      var li = lang === "fa" ? 1 : 0;
      var label = (LABELS[key] || LABELS.modern)[li];
      var note = NOTE[REAL[key] ? "real" : "sketch"][li];
      return { svg: DRAW[key](lang), label: label, note: note };
    }
  };
})();
