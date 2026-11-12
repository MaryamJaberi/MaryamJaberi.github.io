# -*- coding: utf-8 -*-
"""Build soc/tools/path.html and phil/tools/path.html — «از کجا شروع کنم»: guided reading paths
(a question, then 5–8 entries in order) and an idea timeline (entries by the year of their oldest source)."""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
SRC = json.load(open(f'{R}/core/sources.json', encoding='utf-8'))
PATHS = {
 'soc': ('جامعه', '--fam-soc', [
  ['چرا مردم ناراضی سکوت می‌کنند، و چرا ناگهان همه با هم بلند می‌شوند؟', ['preference-falsification', 'collective-action', 'threshold-models-of-collective-behaviour', 'coordination-focal-points', 'self-organized-criticality', 'critical-transitions-early-warning', 'civil-resistance-success-rates']],
  ['حکومت که رفت، چه می‌شود؟', ['pacted-transitions', 'security-defection-credible-commitment', 'dissolving-army-and-purges-iraq-lesson', 'transitional-justice-options', 'collective-trauma-justice-revenge', 'transition-design-focal-point', 'gradual-democratization-own-model', 'analogy-and-reference-class']],
  ['چرا بعضی کشورها ثروتمند می‌شوند و بعضی فقیر می‌مانند؟', ['institutions', 'institutions-inclusive', 'nogales-one-city-two-institutions', 'growth-under-extractive-institutions', 'authoritarian-growth-appeal-and-limits', 'structural-corruption-causes-iran', 'institutional-drift-contingency-limits-of-prediction']],
  ['اعتماد و همکاری چطور ساخته می‌شود؟', ['generalized-trust', 'social-capital', 'repeated-games-cooperation', 'network-structure-robustness', 'legitimacy-trust-function', 'arendt-totalitarian-isolation-and-trust', 'misbelief-distrust-spiral']],
  ['جامعه‌شناسی از کجا آمد؟ سه پایه‌گذار و یک پیشگام', ['sociological-imagination', 'asabiyya-ibn-khaldun-modern-respect', 'durkheim-social-facts-suicide', 'anomie', 'marx-historical-materialism', 'class-consciousness', 'secularization']],
  ['ملت چیست و چه چیزی آن را کنار هم نگه می‌دارد؟', ['nation-making-gellner-anderson-iran', 'nation-as-umbrella-idea-iran', 'nation-myths-symbols-cohesion-and-limits', 'persian-language-iran-identity-ethnicity-debate', 'national-myth-solidarity-vs-ethnic-division-debate', 'nation-regime-society-three-spheres-and-authority']],
  ['نابرابری از کجا می‌آید و چه می‌کند؟', ['inequality', 'gini-inequality', 'inequality-health', 'landlord-class-formation-iran', 'oil-revenue-accounting-gaps', 'structural-corruption-three-dimensions']],
 ]),
 'phil': ('فلسفه', '--fam-hum', [
  ['چرا باید از حکومت اطاعت کنیم، و کی دیگر نباید؟', ['hobbes-fear-sovereign-minimal-morality', 'locke-natural-rights-social-contract', 'locke-tyranny-resistance-and-limited-government', 'montesquieu-law-liberty-separation-of-powers', 'arendt-obedience-is-support', 'living-in-truth']],
  ['آزادی یعنی چه و مرزش کجاست؟', ['mill-liberty-individuality-harm-principle', 'freedom-of-expression-between-belief-and-action', 'berlin-value-conflict-liberty-equality', 'hayek-rule-of-law-justice-liberty', 'locke-toleration-church-state', 'liberty-limits-and-moral-order']],
  ['آدم‌های معمولی چطور در ظلم شریک می‌شوند؟', ['normalization-banality-of-evil', 'arendt-lesser-evil-argument', 'arendt-personal-responsibility-no-collective-guilt', 'arendt-conscience-thinking-nonparticipants', 'arendt-dark-times-isolation-and-public-speech', 'epistemic-injustice']],
  ['از کجا بدانم چیزی درست است؟', ['skepticism-cogito', 'locke-empiricism-tabula-rasa', 'rationalism-empiricism-kant-narrative', 'falsification', 'paradigms', 'james-pragmatic-truth', 'biruni-truth-seeking']],
  ['چطور باید زندگی کرد؟', ['stoicism', 'kant-duty-ethics-universal-law', 'utilitarianism-bentham-mill-earthly-ethics', 'free-will', 'absurd-meaning', 'nietzsche-god-is-dead-nihilism']],
  ['اصلاح یا انقلاب؟ عقل تا کجا می‌تواند جامعه را از نو بسازد؟', ['kant-enlightenment-reform-not-revolution', 'hayek-vs-popper-reason-and-piecemeal-engineering', 'hayek-knowledge-problem-calculation', 'plato-aristotle-popper-political-philosophy-origins', 'berlin-power-of-ideas-romantic-roots', 'democracy-promotion-limits']],
 ]),
}
ERAS = [[-3000, 1799, 'پیش از ۱۸۰۰'], [1800, 1899, 'سدهٔ نوزدهم'], [1900, 1949, '۱۹۰۰ تا ۱۹۴۹'], [1950, 1979, '۱۹۵۰ تا ۱۹۷۹'], [1980, 1999, '۱۹۸۰ تا ۱۹۹۹'], [2000, 2014, '۲۰۰۰ تا ۲۰۱۴'], [2015, 2100, '۲۰۱۵ تا امروز']]
TPL = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>از کجا شروع کنم؟ | __NAME__ | دانش‌سرا</title>
<meta name="description" content="مسیرهای راهنما در ویکی __NAME__: با یک پرسش شروع کن و مدخل‌ها را به ترتیب بخوان. به‌همراه خط زمانی ایده‌ها.">
<link rel="stylesheet" href="../../core/design/tokens.css">
<style>
:root{--k:var(__FAM__)}
main{padding-block:var(--s5) var(--s10)}
h1{font-size:var(--h1);margin:var(--s4) 0 var(--s2);line-height:var(--lh-tight)}
h2{font-size:var(--h3);margin:var(--s8) 0 var(--s2)}
.lead{color:var(--ink-2);max-width:62ch;line-height:1.9;margin:0 0 var(--s4)}
.qs{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}
.q{font:inherit;text-align:start;padding:14px 16px;border-radius:16px;border:1px solid var(--line-strong);border-inline-start:5px solid var(--k);background:var(--surface);color:var(--ink);cursor:pointer;line-height:1.8;font-size:1rem;font-weight:600;min-height:64px}
.q small{display:block;font-weight:400;color:var(--ink-3);font-size:.78rem}
.q[aria-pressed=true]{background:var(--k);color:#fff;border-color:var(--k)}.q[aria-pressed=true] small{color:#fff;opacity:.85}
.path{margin-top:16px;display:grid;gap:0;max-width:760px}
.st{display:grid;grid-template-columns:44px minmax(0,1fr);gap:12px;position:relative;padding-bottom:14px}
.st::before{content:"";position:absolute;inset-inline-start:21px;top:40px;bottom:0;width:2px;background:var(--line-strong)}
.st:last-child::before{display:none}
.st .n{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--k);color:#fff;font-weight:700;z-index:1}
.st.done .n{background:var(--ok)}
.st a.c{display:block;padding:12px 14px;border-radius:14px;border:1px solid var(--line);background:var(--surface);text-decoration:none;color:var(--ink);line-height:1.8}
.st a.c:hover{border-color:var(--k)}
.st a.c b{display:block;font-size:1.02rem}.st a.c span{color:var(--ink-2);font-size:.88rem}
.st label{display:inline-flex;gap:6px;align-items:center;font-size:.8rem;color:var(--ink-3);margin-top:4px;min-height:32px}
.prog{font-size:.86rem;color:var(--ink-2);margin:10px 0}
.eras{display:flex;gap:6px;align-items:flex-end;height:150px;direction:ltr;margin-top:10px}
.era{flex:1;display:grid;gap:4px;align-content:end;justify-items:center;font:inherit;background:none;border:0;cursor:pointer;color:var(--ink-2);padding:0;height:100%}
.era i{display:block;width:100%;border-radius:8px 8px 0 0;background:color-mix(in srgb,var(--k) 45%,transparent);min-height:4px}
.era[aria-pressed=true] i{background:var(--k)}.era b{font-size:.8rem}
.era span{font-size:.68rem;line-height:1.3;min-height:2.6em;direction:rtl;text-align:center}
.el{margin-top:12px;display:flex;flex-wrap:wrap;gap:6px}
.el a{padding:5px 12px;border-radius:99px;border:1px solid var(--line);background:var(--surface);text-decoration:none;color:var(--ink);font-size:.86rem}
.el a:hover{border-color:var(--k);color:var(--k)}.el a small{color:var(--ink-3)}
.note{font-size:.8rem;color:var(--ink-3);max-width:62ch;line-height:1.8}
</style>
</head>
<body>
<main class="wrap" id="main">
<h1>از کجا شروع کنم؟</h1>
<p class="lead">یک پرسش را بردار. مدخل‌ها به ترتیبی چیده شده‌اند که هر کدام زمینهٔ بعدی را می‌سازد. هر کدام را خواندی تیک بزن.</p>
<div class="qs" id="qs"></div>
<p class="prog" id="prog"></p>
<div class="path" id="path"></div>
<h2>خط زمانی ایده‌ها</h2>
<p class="lead">هر ستون یک دوره است و بلندی‌اش شمار مدخل‌هایی که قدیمی‌ترین منبعشان از آن دوره است. روی ستون بزن.</p>
<div class="eras" id="eras"></div>
<div class="el" id="el"></div>
<p class="note">جای هر مدخل بر پایهٔ سال قدیمی‌ترین منبع ثبت‌شده‌اش است، نه لزوماً سال پیدایش خود ایده؛ مدخل‌هایی که فقط منبع تازه دارند دیرتر از جای واقعی‌شان می‌افتند.</p>
</main>
<script>
const D = __DATA__, $ = id => document.getElementById(id), W = "__W__";
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const fa = n => String(n).replace(/\d/g, c => "۰۱۲۳۴۵۶۷۸۹"[c]);
let done = {}; try { done = JSON.parse(localStorage.getItem("ds-path-" + W) || "{}") || {}; } catch (_) {}
let sel = 0, era = D.eras.length - 3;
const href = s => `../#${s}`;
function qs(){ $("qs").innerHTML = D.paths.map((p, i) => { const k = p[1].filter(e => done[e[0]]).length; return `<button type="button" class="q" data-i="${i}" aria-pressed="${i === sel}">${esc(p[0])}<small>${fa(p[1].length)} مدخل${k ? " · " + fa(k) + " خوانده" : ""}</small></button>`; }).join(""); }
function path(){
  const p = D.paths[sel], k = p[1].filter(e => done[e[0]]).length;
  $("prog").textContent = `${fa(k)} از ${fa(p[1].length)} خوانده شده`;
  $("path").innerHTML = p[1].map((e, i) => `<div class="st ${done[e[0]] ? "done" : ""}"><div class="n">${done[e[0]] ? "✓" : fa(i + 1)}</div><div><a class="c" href="${href(e[0])}"><b>${esc(e[1])}</b><span>${esc(e[2])}</span></a><label><input type="checkbox" data-s="${e[0]}" ${done[e[0]] ? "checked" : ""}> خواندم</label></div></div>`).join("");
}
$("qs").addEventListener("click", e => { const b = e.target.closest("[data-i]"); if (b) { sel = +b.dataset.i; qs(); path(); $("prog").scrollIntoView({behavior: "smooth", block: "start"}); } });
$("path").addEventListener("change", e => { const s = e.target.dataset.s; if (!s) return; if (e.target.checked) done[s] = 1; else delete done[s]; try { localStorage.setItem("ds-path-" + W, JSON.stringify(done)); } catch (_) {} qs(); path(); });
function eras(){
  const mx = Math.max(...D.eras.map(x => x[1].length));
  $("eras").innerHTML = D.eras.map((x, i) => `<button type="button" class="era" data-e="${i}" aria-pressed="${i === era}" aria-label="${esc(x[0])}"><b>${fa(x[1].length)}</b><i style="height:${Math.round(100 * x[1].length / mx)}px"></i><span>${esc(x[0])}</span></button>`).join("");
  const L = D.eras[era][1];
  $("el").innerHTML = L.slice(0, 36).map(e => `<a href="${href(e[0])}">${esc(e[1])} <small>${fa(e[2])}</small></a>`).join("") + (L.length > 36 ? `<a href="../entries.html">و ${fa(L.length - 36)} مدخل دیگر ←</a>` : "");
}
$("eras").addEventListener("click", e => { const b = e.target.closest("[data-e]"); if (b) { era = +b.dataset.e; eras(); } });
qs(); path(); eras();
</script>
</body>
</html>
'''
def short(t, n=110):
    t = t.strip(); 
    if len(t) <= n: return t
    cut = t[:n]; i = max(cut.rfind('؛'), cut.rfind('.'), cut.rfind('،'))
    return (cut[:i] if i > 50 else cut[:cut.rfind(' ')]) + '…'
for w, (name, fam, paths) in PATHS.items():
    C = {}
    for f in glob.glob(f'{R}/data/{w}/concepts/*.json'):
        d = json.load(open(f, encoding='utf-8')); C[os.path.basename(f)[:-5]] = d
    out = []
    for q, slugs in paths:
        L = [[s, C[s]['title']['fa'], short(C[s]['summary']['fa'])] for s in slugs if s in C]
        miss = [s for s in slugs if s not in C]
        if miss: print('  missing in', w, miss)
        out.append([q, L])
    eras = [[lab, []] for _, _, lab in ERAS]
    for s, d in C.items():
        ys = [SRC[k].get('year') for k in d.get('sources', []) if k in SRC and isinstance(SRC[k].get('year'), int)]
        if not ys: continue
        y = min(ys)
        for i, (a, b, _) in enumerate(ERAS):
            if a <= y <= b: eras[i][1].append([s, d['title']['fa'], y]); break
    for e in eras: e[1].sort(key=lambda x: x[2])
    data = json.dumps({'paths': out, 'eras': eras}, ensure_ascii=False)
    html = TPL.replace('__DATA__', data).replace('__NAME__', name).replace('__FAM__', fam).replace('__W__', w)
    open(f'{R}/{w}/tools/path.html', 'w', encoding='utf-8').write(html)
    print(f'{w}/tools/path.html: {len(out)} paths, {sum(len(e[1]) for e in eras)} dated entries')
