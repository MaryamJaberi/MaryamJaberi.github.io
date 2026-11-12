# -*- coding: utf-8 -*-
"""Build core/log.html — «دفتر پروژه»: what exists, what changed and when, what is next.
Reads the git history of this folder (subjects only), core/registry.json stats and data/plan/plan.json,
so the page is up to date after every build without anyone writing it by hand."""
import json, os, subprocess, glob, re
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
out = subprocess.run(['git', 'log', '--date=short', '--pretty=%ad|%s', '-n', '400', '--', '.'], cwd=R, capture_output=True, text=True).stdout
days = {}
for line in out.splitlines():
    d, _, s = line.partition('|')
    s = re.sub(r'^(دانش‌سرا|daneshsara)\s*[:：]\s*', '', s.strip())
    if s: days.setdefault(d, []).append(s)
log = [[d, v] for d, v in sorted(days.items(), reverse=True)]
reg = json.load(open(f'{R}/core/registry.json', encoding='utf-8'))
st = reg.get('stats') or {}
if not st:
    es = reg['entries']
    st = {'concepts': sum(1 for e in es.values() if e.get('type') == 'concept'), 'iran_notes': sum(1 for e in es.values() if e.get('type') == 'iran')}
plan = json.load(open(f'{R}/data/plan/plan.json', encoding='utf-8'))
pages = len([p for p in glob.glob(f'{R}/**/*.html', recursive=True) if '/build/' not in p and 'http-equiv="refresh"' not in open(p, encoding='utf-8').read(3000)])
tiles = [[st.get('concepts', 0), 'مدخل علمی', '../atlas/sitemap.html'], [st.get('sources', 0), 'منبع', 'sources.html'], [st.get('iran_notes', 0), 'یادداشت ایران', '../iran/'],
         [st.get('cross_wiki_links', 0), 'پیوند میان ویکی‌ها', '../atlas/hidden-bridges.html'], [pages, 'صفحه', '../atlas/sitemap.html'], [sum(len(v) for _, v in log), 'تغییر ثبت‌شده', '#log']]
DATA = json.dumps({'log': log, 'tiles': tiles, 'tools': plan['tools'], 'road': plan['roadmap'], 'ledger': [[d[0], d[2]] for d in plan['ledger']], 'sci': [[s[0], s[2]] for s in plan['sciences']], 'backlog': plan['backlog']}, ensure_ascii=False)
TPL = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>دفتر پروژه | دانش‌سرا</title>
<meta name="description" content="دفتر زندهٔ پروژه: چه ساخته شده، هر روز چه تغییری کرده و قدم بعدی چیست. با هر به‌روزرسانی سایت خودکار تازه می‌شود.">
<link rel="stylesheet" href="design/tokens.css">
<style>
main{padding-block:var(--s5) var(--s10)}
h1{font-size:var(--h1);margin:var(--s4) 0 var(--s2);line-height:var(--lh-tight)}
.lead{color:var(--ink-2);max-width:60ch;line-height:1.9;margin:0 0 var(--s5)}
h2{font-size:var(--h3);margin:0 0 var(--s3)}
section{padding-block:var(--s6);border-top:1px solid var(--line);scroll-margin-top:8px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}
.tiles a{display:grid;padding:14px;border-radius:14px;border:1px solid var(--line);background:var(--surface);text-decoration:none;color:inherit;border-top:3px solid var(--primary)}
.tiles b{font-size:1.7rem;line-height:1.2}.tiles span{font-size:.85rem;color:var(--ink-3)}
.now{padding:14px 16px;border-radius:16px;border:2px solid var(--primary);background:var(--surface);max-width:760px;line-height:1.9}
.now small{color:var(--ink-3);display:block}
.bars{display:grid;gap:10px;max-width:760px}
.bar{display:grid;gap:4px;font-size:.9rem}.bar div{display:flex;height:12px;border-radius:99px;overflow:hidden;background:var(--surface-subtle)}
.bar i{display:block}.bar small{color:var(--ink-3)}
.day{display:grid;grid-template-columns:120px minmax(0,1fr);gap:14px;padding:12px 0;border-bottom:1px dashed var(--line)}
@media (max-width:600px){.day{grid-template-columns:minmax(0,1fr);gap:4px}}
.day time{font-weight:650;color:var(--primary)}.day time small{display:block;font-weight:400;color:var(--ink-3);font-size:.78rem}
.day ul{margin:0;padding-inline-start:18px;line-height:1.9;font-size:.92rem;color:var(--ink-2)}
#more{font:inherit;margin-top:14px;min-height:44px;padding:8px 18px;border-radius:99px;border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);cursor:pointer}
.nx{display:grid;gap:6px;max-width:760px}.nx div{padding:8px 12px;border-radius:12px;border:1px solid var(--line);background:var(--surface);font-size:.92rem;display:flex;justify-content:space-between;gap:10px}
.nx small{color:var(--ink-3)}
</style>
</head>
<body>
<main class="wrap" id="main">
<h1>دفتر پروژه</h1>
<p class="lead">این صفحه خودش را می‌نویسد: هر بار که سایت به‌روز می‌شود، شمارها، وضعیت و فهرست تغییرها از خود پروژه خوانده می‌شود. تصویر کامل هدف و برنامه در <a href="../simorgh/plan.html">نقشهٔ کلان سیمرغ</a> است.</p>
<div class="tiles" id="tiles"></div>
<section><h2>اکنون کجاییم</h2><div class="now" id="now"></div></section>
<section><h2>چقدر ساخته شده</h2><div class="bars" id="bars"></div></section>
<section id="backlog"><h2>فهرست کارها، به ترتیب اولویت</h2><div class="nx" id="bl"></div></section>
<section><h2>ابزارهایی که هنوز ساخته نشده</h2><div class="nx" id="nx"></div></section>
<section id="log"><h2>چه تغییر کرد، روز به روز</h2><div id="days"></div><button type="button" id="more">روزهای قدیمی‌تر</button></section>
</main>
<script>
const D = __DATA__, $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const fa = n => Number(n).toLocaleString("en-US").replace(/,/g, "٬").replace(/\d/g, c => "۰۱۲۳۴۵۶۷۸۹"[c]);
$("tiles").innerHTML = D.tiles.map(t => `<a href="${t[2]}"><b>${fa(t[0])}</b><span>${esc(t[1])}</span></a>`).join("");
$("now").innerHTML = `<small>مرحلهٔ ۱ از ${fa(D.road.length)} در نقشهٔ راه</small><b>${esc(D.road[0][0])}</b>: ${esc(D.road[0][1])}<small>دروازهٔ این مرحله: ${esc(D.road[0][2])}</small>`;
function bar(name, list, href){
  const c = {have: 0, part: 0, none: 0}; list.forEach(x => c[x.at(-1) === undefined ? "none" : x[x.length - 1]] !== undefined && c[x[x.length - 1]]++);
  const n = list.length || 1;
  return `<div class="bar"><span><a href="${href}">${name}</a> <small>${fa(c.have)} آماده، ${fa(c.part)} ناقص، ${fa(c.none)} مانده</small></span><div><i style="width:${c.have / n * 100}%;background:var(--ok)"></i><i style="width:${c.part / n * 100}%;background:var(--warn)"></i></div></div>`;
}
$("bars").innerHTML = bar("دفتر ویرانی‌ها", D.ledger, "../simorgh/plan.html#ledger") + bar("علوم لازم", D.sci, "../simorgh/plan.html#sci") + bar("ابزارها", D.tools.map(t => [t[0], t[2]]), "../simorgh/plan.html#tools");
$("nx").innerHTML = D.tools.filter(t => t[2] !== "have").map(t => `<div><span>${esc(t[0])} <small>${esc(t[1])}</small></span><small>${t[2] === "part" ? "ناقص" : "ساخته نشده"}</small></div>`).join("");
const PN = ["۰ فوری", "۱ زیاد", "۲ متوسط", "۳ بعداً"], SN = {done: "انجام شد", doing: "در حال انجام", todo: "مانده"}, SC = {done: "var(--ok)", doing: "var(--warn)", todo: "var(--ink-3)"};
$("bl").innerHTML = D.backlog.map(b => `<div style="border-inline-start:4px solid ${SC[b[2]]}"><span><small>${PN[b[0]]}</small> ${b[3] ? `<a href="${b[3]}">${esc(b[1])}</a>` : esc(b[1])}</span><small style="color:${SC[b[2]]};white-space:nowrap">${SN[b[2]]}</small></div>`).join("");
let shown = 7;
function days(){
  $("days").innerHTML = D.log.slice(0, shown).map(([d, items]) => { const dt = new Date(d + "T12:00:00Z"); let j = d; try { j = dt.toLocaleDateString("fa-IR-u-ca-persian", {day: "numeric", month: "long", year: "numeric", timeZone: "UTC"}); } catch (_) {}
    return `<div class="day"><time datetime="${d}">${esc(j)}<small>${fa(items.length)} تغییر</small></time><ul>${items.map(s => `<li>${esc(s)}</li>`).join("")}</ul></div>`; }).join("");
  $("more").hidden = shown >= D.log.length;
}
$("more").addEventListener("click", () => { shown += 14; days(); }); days();
</script>
</body>
</html>
'''
open(f'{R}/core/log.html', 'w', encoding='utf-8').write(TPL.replace('__DATA__', DATA))
print(f'core/log.html: {len(log)} days, {sum(len(v) for _, v in log)} changes')
