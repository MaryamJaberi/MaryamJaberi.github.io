# -*- coding: utf-8 -*-
"""«نقشهٔ من» — خودسنجی دوبعدی (دو محور، چهار خانه، یک یا چند نقطه).
One generic page per data/selfmaps/*.json.  python3 build/selfmap.py
Nothing is stored or sent: scoring happens in the page and dies with it."""
import os, json, glob, html
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.chdir(R)
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
WV = {'روان': '--fam-psy', 'جامعه': '--fam-soc', 'فلسفه': '--fam-hum', 'تاریخ': '--fam-hist', 'تبار': '--fam-bio', 'ایران': '--primary'}

TPL = '''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>__TITLE__ | دانش‌سرا</title>
<meta name="description" content="__DESC__">
<link rel="stylesheet" href="__UP__core/design/tokens.css">
<style>
:root{--c:var(__COLOR__)}
h1{font-size:var(--h1);margin:var(--s8) 0 var(--s3);line-height:var(--lh-tight);text-wrap:balance}
p.lead{color:var(--ink-2);max-width:46em;line-height:2;margin:0 0 var(--s4);font-size:1.05rem}
.note{padding:var(--s3) var(--s4);border-radius:var(--r-md);font-size:var(--small);line-height:1.9;color:var(--ink-2);max-width:60em;margin:0 0 var(--s3)}
.note.w{background:color-mix(in srgb,var(--warn) 9%,var(--paper));border:1px solid color-mix(in srgb,var(--warn) 40%,var(--line))}
.note.p{background:color-mix(in srgb,var(--ok) 8%,var(--paper));border:1px solid color-mix(in srgb,var(--ok) 35%,var(--line))}
section{padding-block:var(--s5);border-top:1px solid var(--line)}
h2{font-size:var(--h3);margin:0 0 var(--s3)}
.tg{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:var(--s4)}
.tg[hidden]{display:none}
.tg label{font-size:var(--small);color:var(--ink-2)}
.tg select{font:inherit;padding:6px 12px;border-radius:var(--r-md);border:1px solid var(--line-strong);background:var(--surface);color:var(--ink)}
.prog{height:6px;border-radius:4px;background:var(--surface-subtle);overflow:hidden;margin-bottom:var(--s4);max-width:44em;display:flex}
.prog i{background:var(--c);transition:width .2s}
ol.q{list-style:none;margin:0;padding:0;display:grid;gap:var(--s3);max-width:44em;counter-reset:q}
ol.q li{counter-increment:q;padding:var(--s4);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface)}
ol.q li.done{border-color:color-mix(in srgb,var(--c) 45%,var(--line))}
ol.q p{margin:0 0 var(--s3);line-height:1.9}ol.q p::before{content:counter(q,persian) ". ";color:var(--c);font-weight:650}
.sc{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:5px;direction:ltr}
.sc label{position:relative;display:grid;place-items:center;height:40px;border-radius:var(--r-md);border:1px solid var(--line-strong);cursor:pointer;font-size:var(--small);font-variant-numeric:tabular-nums;background:var(--paper)}
.sc input{position:absolute;opacity:0;inset:0;cursor:pointer;margin:0}
.sc label:has(input:checked){background:var(--c);border-color:var(--c);color:var(--paper);font-weight:650}
.sc label:has(input:focus-visible){outline:2px solid var(--c);outline-offset:2px}
.ends{display:flex;justify-content:space-between;font-size:var(--chip);color:var(--ink-3);margin-top:5px;direction:ltr}
.act{display:flex;flex-wrap:wrap;gap:10px;margin-top:var(--s4);align-items:center}
button.b{font:inherit;padding:9px 22px;border-radius:var(--r-full);border:1px solid var(--c);background:var(--c);color:var(--paper);cursor:pointer;font-weight:650}
button.b[disabled]{opacity:.45;cursor:not-allowed}
button.g{font:inherit;padding:8px 18px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:none;color:var(--ink-2);cursor:pointer}
.left{font-size:var(--small);color:var(--ink-3)}
.res{display:grid;grid-template-columns:minmax(0,440px) minmax(0,1fr);gap:var(--s6);align-items:start}
@media (max-width:860px){.res{grid-template-columns:minmax(0,1fr)}}
svg.map{width:100%;height:auto;display:block;direction:ltr}
svg.map text{font:500 12px inherit;fill:var(--ink-2)}
svg.map .ql{font-size:13px;fill:var(--ink-2);text-anchor:middle}
svg.map .tk{font-size:11px;fill:var(--ink-3);text-anchor:middle}
svg.map .ax{font-size:13px;font-weight:650;fill:var(--ink);text-anchor:middle}
svg.map .end{font-size:10.5px;fill:var(--ink-3)}
svg.map .grid{stroke:var(--line);stroke-width:1}
svg.map .mid{stroke:var(--ink-3);stroke-width:1.2;stroke-dasharray:5 4}
svg.map .dot{stroke:var(--paper);stroke-width:2.5}
svg.map .dl{font-size:12px;font-weight:650;fill:var(--ink);paint-order:stroke;stroke:var(--surface);stroke-width:4px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:var(--s3)}
.chips span{padding:6px 14px;border-radius:var(--r-md);background:var(--surface);border:1px solid var(--line);font-size:var(--small)}
.chips b{font-variant-numeric:tabular-nums}
.who{margin:0 0 var(--s2);font-size:var(--h4);font-weight:650}
.who i{font-style:normal;display:inline-block;width:12px;height:12px;border-radius:50%;margin-inline-end:8px;vertical-align:-1px}
.desc{margin:0 0 var(--s3);line-height:2;color:var(--ink-2);max-width:40em}
.near{font-size:var(--small);color:var(--warn);margin:0 0 var(--s3)}
ul.pts{margin:0 0 var(--s3);padding:0;list-style:none;display:grid;gap:6px}
ul.pts li{font-size:var(--small);color:var(--ink-2)}
ul.nt{margin:0;padding-inline-start:1.2em;display:grid;gap:6px;font-size:var(--small);color:var(--ink-2);line-height:1.9;max-width:46em}
.wls{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.wl{display:inline-flex;align-items:center;gap:6px;font-size:var(--chip);padding:2px 10px 2px 3px;border-radius:var(--r-full);border:1px solid color-mix(in srgb,var(--w) 45%,var(--line));color:var(--ink-2);text-decoration:none;background:color-mix(in srgb,var(--w) 7%,var(--surface))}
.wl i{font-style:normal;font-weight:650;color:var(--paper);background:var(--w);border-radius:var(--r-full);padding:0 8px}
ol.src{padding-inline-start:1.6em;display:grid;gap:8px;font-size:var(--small);color:var(--ink-2);line-height:1.8;max-width:60em}
ol.src em{font-style:normal;color:var(--ink-3)}
.tier{font-size:var(--chip);padding:0 8px;border-radius:var(--r-full);border:1px solid var(--line-strong);margin-inline-end:6px;white-space:nowrap}
footer.f{border-top:1px solid var(--line);padding-block:var(--s5);font-size:var(--small);color:var(--ink-3)}footer.f a{color:var(--ink-2);margin-inline-end:var(--s4)}
</style>
</head>
<body>
<main class="wrap">
<h1>__TITLE__</h1>
<p class="lead">__LEAD__</p>
<p class="note w">__WARN__</p>
<p class="note p">__PRIVACY__</p>

<section id="ask">
<h2>پرسش‌ها</h2>
<div class="tg" id="tg" hidden><label for="target">__TLABEL__</label><select id="target"></select></div>
<div class="prog"><i id="bar" style="width:0"></i></div>
<ol class="q" id="qs"></ol>
<div class="act"><button class="b" id="go" disabled>نقشه‌ام را نشان بده</button><span class="left" id="left"></span></div>
</section>

<section id="result" hidden>
<h2>نقشهٔ شما</h2>
<div class="res">
<figure style="margin:0"><div id="map"></div></figure>
<div>
<div id="out"></div>
<div class="act"><button class="g" id="again"></button><button class="g" id="copy">کپی نتیجه به‌صورت متن</button><button class="g" id="wipe">پاک کردن همه</button></div>
</div>
</div>
</section>

<section id="read">
<h2>چطور بخوانیم</h2>
<ul class="nt">__NOTES__</ul>
<div class="wls" style="margin-top:var(--s4)"><span style="font-size:var(--chip);color:var(--ink-3)">در ویکی‌ها:</span>__WIKI__</div>
</section>

<section id="sources">
<h2>منابع</h2>
<p style="font-size:var(--small);color:var(--ink-3);margin:0 0 var(--s3)">الگوی دوبعدی از این پژوهش‌ها آمده است. خودِ جمله‌ها از این منابع نیستند.</p>
<ol class="src">__SRC__</ol>
</section>
</main>
<footer class="f"><div class="wrap"><a href="__UP__">دانش‌سرا</a><a href="./">ابزارهای این ویکی</a><a href="__UP__atlas/sitemap.html">نقشهٔ سایت</a></div></footer>
<script>
(() => {
const D = __DATA__;
const fa = n => String(n).replace(/\\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[d]).replace(".", "٫");
const $ = id => document.getElementById(id);
const PAL = ["--c", "--warn", "--fam-hum", "--err", "--fam-bio", "--fam-formal"];
const multi = !!D.targets;
let results = [];
// questions
$("qs").innerHTML = D.items.map((it, i) => `<li data-i="${i}"><p>${it.t}</p><div class="sc" role="radiogroup" aria-label="${it.t}">` +
  [1,2,3,4,5,6,7].map(v => `<label><input type="radio" name="q${i}" value="${v}" aria-label="${fa(v)} از ۷">${fa(v)}</label>`).join("") +
  `</div><div class="ends"><span>${D.scale[0]}</span><span>${D.scale[1]}</span></div></li>`).join("");
if (multi) { $("tg").hidden = false; $("target").innerHTML = D.targets.map((t, i) => `<option value="${i}">${t}</option>`).join(""); }
$("again").textContent = multi ? "یک رابطهٔ دیگر" : "از نو";
const answers = () => D.items.map((_, i) => { const r = document.querySelector(`input[name=q${i}]:checked`); return r ? +r.value : null; });
function tick() {
  const a = answers(), n = a.filter(v => v != null).length;
  document.querySelectorAll("#qs li").forEach((li, i) => li.classList.toggle("done", a[i] != null));
  $("bar").style.width = (n / a.length * 100) + "%"; $("go").disabled = n < a.length;
  $("left").textContent = n < a.length ? fa(a.length - n) + " پرسش مانده" : "";
}
$("qs").addEventListener("change", tick); tick();
const score = (a, axis) => { const v = D.items.map((it, i) => it.a === axis ? (it.r ? 8 - a[i] : a[i]) : null).filter(x => x != null); return v.reduce((s, x) => s + x, 0) / v.length; };
const quad = (x, y) => (x > 4 ? "h" : "l") + (y > 4 ? "h" : "l");
// map
const X0 = 44, Y0 = 26, W = 300, H = 300, px = v => X0 + (v - 1) / 6 * W, py = v => Y0 + H - (v - 1) / 6 * H;
function draw() {
  const q = (k, x, y) => `<rect x="${x}" y="${y}" width="${W / 2}" height="${H / 2}" style="fill:color-mix(in srgb,var(${D.quads[k].v}) 11%,var(--surface))"/>`;
  const lab = (k, x, y) => { const parts = D.quads[k].k.split(" ("); return `<text class="ql" x="${x}" y="${y}">${parts[0]}</text>` + (parts[1] ? `<text class="ql" x="${x}" y="${y + 17}" style="font-size:11px">(${parts[1]}</text>` : ""); };
  let s = `<svg class="map" viewBox="0 0 390 392" role="img" aria-label="نقشهٔ دوبعدی: ${D.x.k} و ${D.y.k}">` +
    q("lh", X0, Y0) + q("hh", X0 + W / 2, Y0) + q("ll", X0, Y0 + H / 2) + q("hl", X0 + W / 2, Y0 + H / 2);
  for (let v = 1; v <= 7; v++) s += `<line class="grid" x1="${px(v)}" y1="${Y0}" x2="${px(v)}" y2="${Y0 + H}"/><line class="grid" x1="${X0}" y1="${py(v)}" x2="${X0 + W}" y2="${py(v)}"/>` +
    `<text class="tk" x="${px(v)}" y="${Y0 + H + 16}">${fa(v)}</text><text class="tk" x="${X0 + W + 14}" y="${py(v) + 4}">${fa(v)}</text>`;
  s += `<line class="mid" x1="${px(4)}" y1="${Y0}" x2="${px(4)}" y2="${Y0 + H}"/><line class="mid" x1="${X0}" y1="${py(4)}" x2="${X0 + W}" y2="${py(4)}"/>` +
    lab("lh", X0 + W / 4, Y0 + 20) + lab("hh", X0 + 3 * W / 4, Y0 + 20) + lab("ll", X0 + W / 4, Y0 + H - 28) + lab("hl", X0 + 3 * W / 4, Y0 + H - 28) +
    `<text class="ax" x="${X0 + W / 2}" y="${Y0 + H + 40}">${D.x.k}</text><text class="end" x="${X0}" y="${Y0 + H + 56}" text-anchor="start">${D.x.lo} ←</text><text class="end" x="${X0 + W}" y="${Y0 + H + 56}" text-anchor="end">→ ${D.x.hi}</text>` +
    `<text class="ax" transform="translate(${X0 - 26},${Y0 + H / 2}) rotate(-90)">${D.y.k}</text><text class="end" transform="translate(${X0 - 10},${Y0 + H}) rotate(-90)" text-anchor="start">${D.y.lo} ←</text><text class="end" transform="translate(${X0 - 10},${Y0}) rotate(-90)" text-anchor="end">→ ${D.y.hi}</text>`;
  results.forEach((r, i) => { const cx = px(r.x), cy = py(r.y);
    s += `<circle class="dot" cx="${cx}" cy="${cy}" r="9" style="fill:var(${PAL[i % PAL.length]})"/>` + (results.length > 1 || multi ? `<text class="dl" x="${cx}" y="${cy < Y0 + 60 ? cy + 26 : cy - 15}" text-anchor="${cx < X0 + 50 ? "start" : cx > X0 + W - 50 ? "end" : "middle"}">${r.name}</text>` : ""); });
  $("map").innerHTML = s + "</svg>";
}
function text() {
  const r = results[results.length - 1], k = quad(r.x, r.y), near = Math.abs(r.x - 4) < 0.5 || Math.abs(r.y - 4) < 0.5;
  $("out").innerHTML = `<div class="chips"><span>${D.x.k}: <b>${fa(r.x.toFixed(2))}</b> از ۷</span><span>${D.y.k}: <b>${fa(r.y.toFixed(2))}</b> از ۷</span></div>` +
    `<p class="who"><i style="background:var(${PAL[(results.length - 1) % PAL.length]})"></i>${multi ? r.name + ": " : ""}${D.quads[k].k}</p><p class="desc">${D.quads[k].d}</p>` +
    (near ? `<p class="near">نقطهٔ شما نزدیک خط وسط است؛ این برچسب را سفت نگیرید.</p>` : "") +
    (results.length > 1 ? `<ul class="pts">` + results.map((p, i) => `<li><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:var(${PAL[i % PAL.length]});margin-inline-end:8px"></i>${p.name}: ${D.quads[quad(p.x, p.y)].k} (${fa(p.x.toFixed(1))}، ${fa(p.y.toFixed(1))})</li>`).join("") + `</ul>` : "");
}
$("go").addEventListener("click", () => {
  const a = answers(); if (a.some(v => v == null)) return;
  const name = multi ? D.targets[+$("target").value] : "شما";
  const r = {name, x: score(a, "x"), y: score(a, "y")};
  const i = results.findIndex(p => p.name === name); if (i >= 0) results[i] = r; else results.push(r);
  if (i >= 0) results.push(results.splice(i, 1)[0]);
  $("result").hidden = false; draw(); text(); $("result").scrollIntoView({behavior: "smooth", block: "start"});
});
const clear = () => { document.querySelectorAll("#qs input:checked").forEach(r => r.checked = false); tick(); };
$("again").addEventListener("click", () => { clear(); if (multi) { const used = results.map(r => r.name), nx = D.targets.findIndex(t => !used.includes(t)); if (nx >= 0) $("target").value = nx; } else { results = []; $("result").hidden = true; } $("ask").scrollIntoView({behavior: "smooth"}); });
$("wipe").addEventListener("click", () => { results = []; clear(); $("result").hidden = true; $("ask").scrollIntoView({behavior: "smooth"}); });
$("copy").addEventListener("click", e => {
  const t = D.title + "\\n" + results.map(r => `${multi ? r.name + ": " : ""}${D.quads[quad(r.x, r.y)].k} — ${D.x.k} ${fa(r.x.toFixed(2))}، ${D.y.k} ${fa(r.y.toFixed(2))} (از ۷)`).join("\\n") + "\\nابزار آموزشی، نه آزمون معتبر.";
  const b = e.currentTarget, ok = () => { b.textContent = "کپی شد ✓"; setTimeout(() => b.textContent = "کپی نتیجه به‌صورت متن", 1600); };
  try { navigator.clipboard.writeText(t).then(ok, () => {}); } catch (_) {}
});
})();
</script>
</body>
</html>
'''
made = []
for p in sorted(glob.glob('data/selfmaps/*.json')):
    D = json.load(open(p, encoding='utf-8'))
    out = D['out']; up = '../' * out.count('/')
    nx = sum(1 for i in D['items'] if i['a'] == 'x'); ny = sum(1 for i in D['items'] if i['a'] == 'y')
    assert nx == ny and all(k in D['quads'] for k in ('ll', 'hl', 'lh', 'hh')), p
    for u, _w, _t in D['wiki_links']: assert os.path.exists(u.split('#')[0]), u
    wiki = ''.join(f'<a class="wl" style="--w:var({WV[w]})" href="{up}{u}"><i>{w}</i>{E(t)}</a>' for u, w, t in D['wiki_links'])
    src = ''.join(f'<li><span class="tier">ردهٔ {fa(s["t"])}</span> {E(s["c"])}، {fa(s["y"])}. <em>برای: {E(s["for"])}</em></li>' for s in D['sources'])
    notes = ''.join(f'<li>{E(n)}</li>' for n in D['notes'])
    data = {k: D[k] for k in ('title', 'scale', 'x', 'y', 'items', 'quads') }
    if D.get('targets'): data['targets'] = D['targets']
    page = (TPL.replace('__TITLE__', E(D['title'])).replace('__DESC__', E(D['lead'][:150])).replace('__UP__', up).replace('__COLOR__', D['color'])
            .replace('__LEAD__', E(D['lead'])).replace('__WARN__', E(D['warn'])).replace('__PRIVACY__', E(D['privacy']))
            .replace('__TLABEL__', E(D.get('target_label', ''))).replace('__NOTES__', notes).replace('__WIKI__', wiki).replace('__SRC__', src)
            .replace('__DATA__', json.dumps(data, ensure_ascii=False)))
    open(out, 'w', encoding='utf-8').write(page); made.append(out)
print('selfmaps:', ', '.join(made))
