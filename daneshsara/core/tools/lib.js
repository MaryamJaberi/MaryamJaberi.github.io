/* دانش‌سرا — کتابخانهٔ مشترک ابزارها. استفاده: <script src="../../core/tools/lib.js"></script> سپس await DS.load() */
(function () {
  const SRC = (document.currentScript && document.currentScript.src) || "";
  const DS = {};
  DS.faDigits = s => String(s).replace(/\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[d]);
  DS.esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  /* یکسان‌سازی متن فارسی برای جستجو: ی/ک عربی، نیم‌فاصله، اعراب، حروف بزرگ و کوچک */
  DS.norm = s => String(s || "").toLowerCase().replace(/ي/g, "ی").replace(/ك/g, "ک").replace(/[‌‏‎]/g, " ").replace(/[ً-ٰٟ]/g, "").replace(/[۰-۹]/g, d => "۰۱۲۳۴۵۶۷۸۹".indexOf(d)).replace(/\s+/g, " ").trim();
  DS.TIER = { 1: "فراتحلیل/تکرار", 2: "مقالهٔ داوری‌شده/آمار رسمی", 3: "کتاب یا سخنرانی", 4: "سرنخ", 0: "بی‌منبع" };
  DS.FLAG = { unreplicated: "تکرارنشده", contested: "محل بحث", dated: "قدیمی", "editor-note": "یادداشت سردبیر" };
  DS.WIKI = { psy: "روان", soc: "جامعه", phil: "فلسفه", tabar: "تبار", tarikh: "تاریخ" };
  DS.REL = { "part-of": "بخشی از", explains: "توضیح می‌دهد", "evidence-for": "شاهدِ", "evidence-against": "شاهد علیه", contrasts: "در برابر", prerequisite: "پیش‌نیاز", "same-as": "همان", "applies-to": "کاربرد در", "measured-by": "سنجش با", critiques: "نقد", bridges: "پل به", "see-also": "ببینید" };
  let _p = null;
  /* بارگذاری داده؛ نتیجه را با نمایه‌ها برمی‌گرداند */
  DS.load = function () {
    if (_p) return _p;
    const base = SRC;
    _p = fetch(new URL("data.json", base || location.href).href).then(r => r.json()).then(d => {
      d.byId = {}; d.concepts.forEach(c => { c.text = DS.norm([c.t.fa, c.t.en, (c.al || []).join(" "), c.s.fa, c.s.en].join(" ")); d.byId[c.id] = c; });
      d.fieldById = {}; d.fields.forEach(f => d.fieldById[f.id] = f);
      d.root = new URL("../../", new URL("data.json", base || location.href)).href;   // ریشهٔ دانش‌سرا
      return d;
    });
    return _p;
  };
  /* ردهٔ بهترین منبع یک مدخل (کمینهٔ عدد = قوی‌تر) و سهم گزاره‌های محل‌بحث */
  DS.stats = c => {
    const n = c.pts.length || 0; const best = n ? Math.min(...c.pts.map(p => p.tier || 9)) : 9;
    const tiers = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0 }; c.pts.forEach(p => tiers[p.tier || 0]++);
    const fl = { unreplicated: 0, contested: 0, dated: 0, "editor-note": 0 }; c.pts.forEach(p => p.f.forEach(f => { if (f in fl) fl[f]++; }));
    return { n, best: best === 9 ? 0 : best, tiers, flags: fl, strong: n ? (tiers[1] + tiers[2]) / n : 0, contested: n ? (fl.contested + fl.unreplicated + fl.dated) / n : 0 };
  };
  /* برچسب اعتبار کل مدخل: A قوی، B خوب، C کتاب/سخنرانی، D ضعیف یا بی‌منبع */
  DS.grade = c => { const s = DS.stats(c); if (!s.n) return "D"; if (s.strong >= 0.6 && s.contested < 0.35) return "A"; if (s.strong >= 0.3) return "B"; if (s.tiers[0] + s.tiers[4] > s.n * 0.4) return "D"; return "C"; };
  DS.GRADE = { A: "پشتوانهٔ قوی", B: "پشتوانهٔ خوب", C: "عمدتاً کتاب/سخنرانی", D: "پشتوانهٔ ضعیف" };
  DS.url = (d, c) => c && c.u ? d.root + c.u : "#";
  DS.chipTier = t => `<span class="ev t${t}">${DS.esc(DS.TIER[t])}</span>`;
  DS.chipFlag = f => `<span class="flag ${f}">${DS.esc(DS.FLAG[f] || f)}</span>`;
  DS.chipGrade = g => `<span class="gr g${g}">${DS.esc(DS.GRADE[g])}</span>`;
  /* جستجو: همهٔ واژه‌ها باید در متن باشند؛ نتیجه با امتیاز مرتب می‌شود */
  DS.search = (d, q, filter) => {
    const w = DS.norm(q).split(" ").filter(Boolean); if (!w.length) return [];
    return d.concepts.filter(c => (!filter || filter(c)) && w.every(x => c.text.includes(x)))
      .map(c => ({ c, s: w.reduce((a, x) => a + (DS.norm(c.t.fa).includes(x) ? 3 : 0) + (DS.norm(c.t.en).includes(x) ? 2 : 0) + (c.al || []).some(a => DS.norm(a).includes(x)) * 2 + 1, 0) }))
      .sort((a, b) => b.s - a.s).map(x => x.c);
  };
  /* وضعیت در hash برای اشتراک‌گذاری پیوند: DS.hash.get()/set({a:1}) */
  DS.hash = { get() { try { return Object.fromEntries(new URLSearchParams(location.hash.slice(1))); } catch (_) { return {}; } }, set(o) { try { history.replaceState(null, "", "#" + new URLSearchParams(o).toString()); } catch (_) {} } };
  window.DS = DS;
})();
