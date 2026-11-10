# -*- coding: utf-8 -*-
"""«میز کار» لایهٔ ساخت ایران — جاهای خالی متخصص‌ها، مسئله‌های باز، پیشرفت.
Reads data/sakht/work.json (+ sakht.json, registry, git log), writes sakht/work.html.
No names, no form, nothing collected: the page only hands the visitor a text to send to whoever invited them."""
import os, json, html, subprocess
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.chdir(R)
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
W = json.load(open('data/sakht/work.json', encoding='utf-8'))
SK = json.load(open('data/sakht/sakht.json', encoding='utf-8'))
reg = json.load(open('core/registry.json', encoding='utf-8'))['stats']
SIM = 'https://maryamjaberi.github.io/simorgh/'
ST = {'open': ('جای خالی', 'o'), 'talk': ('در گفت‌وگو', 't'), 'has': ('یک نفر هست؛ نفر دوم خوش‌آمد', 'h')}
AT = {'organs': 'نهادهای ضروری', 'transition': 'دوران گذار', 'risks': 'دفتر ریسک', 'digital': 'زیرساخت دیجیتال', 'ideas': 'ایده‌ها', 'links': 'پیوند به ویکی‌ها', 'legacy': 'میراث ناکارآمد', 'sources': 'منابع'}
seats = W['seats']; ntask = sum(len(s['tasks']) for s in seats)
cnt = {k: sum(1 for s in seats if s['st'] == k) for k in ST}

try:
    log = subprocess.run(['git', 'log', '-8', '--date=short', '--format=%ad|%s', '--', '.'], capture_output=True, text=True, cwd=R).stdout.strip().split('\n')
    log = [l.split('|', 1) for l in log if '|' in l]
except Exception:
    log = []

seatmap = ''.join(f'<a class="sm {ST[s["st"]][1]}" href="#{s["id"]}"><b>{E(s["k"])}</b><span>{ST[s["st"]][0].split("؛")[0]}</span><em>{fa(len(s["tasks"]))} مسئله</em></a>' for s in seats)
def task(t, s):
    at = f'<a href="index.html#{t["at"]}">{AT[t["at"]]} ←</a>' if t.get('at') else ''
    tpl = f'سلام، می‌خواهم روی مسئلهٔ {t["id"]} ({t["t"]}) کمک کنم.\nتخصص من: \nچه کاری می‌توانم بکنم: \nچقدر وقت دارم: \nکسی یا ایده‌ای که معرفی می‌کنم: '
    return f'''<article class="task{" first" if s.get("first") == t["id"] else ""}" id="{t["id"]}"><header><code>{t["id"]}</code>{"<span class=fs>قدم اول</span>" if s.get("first") == t["id"] else ""}<h4>{E(t["t"])}</h4><span class="sz">{E(t["size"])}</span></header>
<dl><dt>مسئله</dt><dd>{E(t["prob"])}</dd><dt>چه داریم</dt><dd>{E(t["have"])} {at}</dd><dt>چه می‌خواهیم</dt><dd>{E(t["need"])}</dd></dl>
<button type="button" class="cp" data-t="{E(tpl)}">این را برمی‌دارم: کپی متن آماده</button></article>'''
briefs = ''.join(f'''<section class="seat" id="{s["id"]}"><div class="sh"><h3>{E(s["k"])}</h3><span class="st {ST[s["st"]][1]}">{ST[s["st"]][0]}</span></div>
<p class="who">{E(s["who"])}</p><p class="why">{E(s["why"])}</p><p class="fst">از کجا شروع کنم؟ <a href="#{s["first"]}">{s["first"]} · {E(next(t["t"] for t in s["tasks"] if t["id"] == s["first"]))}</a> کوچک‌ترین و مستقل‌ترین مسئلهٔ این صندلی است. نقش شما در سیمرغ: <a href="{SIM}gam.html#{s["sim"]["a"]}">کارت «{E(s["sim"]["t"])}» ↗</a>، و اگر خارج از ایران‌اید <a href="{SIM}gam.html#mohajer">«مهاجر و خارج‌نشین» ↗</a>.</p><div class="tasks">{''.join(task(t, s) for t in s["tasks"])}</div></section>''' for s in seats)
NS = len(W['stages']) - 1
streams = ''.join(f'<li><span>{E(x["k"])}</span><span class="bar" role="img" aria-label="{W["stages"][x["stage"]]}">{"".join(f"<i class={chr(34)}on{chr(34)}></i>" if i <= x["stage"] and x["stage"] > 0 and i > 0 else "<i></i>" for i in range(1, NS + 1))}</span><em>{W["stages"][x["stage"]]}</em></li>' for x in W['streams'])
changes = ''.join(f'<li><time>{fa(d)}</time>{E(m)}</li>' for d, m in log)

page = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>میز کار | ساخت ایران | دانش‌سرا</title>
<meta name="description" content="کجای پروژهٔ ساخت ایران به چه متخصصی نیاز دارد: {fa(len(seats))} صندلی، {fa(ntask)} مسئلهٔ باز، هر کدام با شرح مسئله، داشته‌ها و خروجی مورد انتظار.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
:root{{--c:var(--ok)}}
h1{{font-size:var(--h1);margin:var(--s8) 0 var(--s4);line-height:var(--lh-tight);max-width:20ch;text-wrap:balance}}
p.lead{{color:var(--ink-2);max-width:47em;line-height:2;margin:0 0 var(--s5);font-size:1.05rem}}
section.b{{padding-block:var(--s6);border-top:1px solid var(--line)}}
h2{{font-size:var(--h3);margin:0 0 var(--s2)}}
p.sub{{color:var(--ink-3);font-size:var(--small);line-height:1.9;margin:0 0 var(--s4);max-width:46em}}
.nums{{display:flex;flex-wrap:wrap;gap:var(--s3);margin-bottom:var(--s5)}}
.nums div{{display:grid;min-width:104px;padding:var(--s3) var(--s4);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);border-top:3px solid var(--c)}}
.nums b{{font-size:1.7rem;line-height:1.15}}.nums span{{font-size:var(--chip);color:var(--ink-3)}}
.seatmap{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,170px),1fr));gap:var(--s3)}}
.sm{{display:grid;gap:2px;padding:var(--s3) var(--s4);border-radius:var(--r-lg);text-decoration:none;color:inherit;border:1.5px solid var(--line-strong);background:var(--surface)}}
.sm b{{font-size:var(--small)}}.sm span{{font-size:var(--chip);font-weight:600}}.sm em{{font-style:normal;font-size:var(--chip);color:var(--ink-3)}}
.sm.o{{border-style:dashed;border-color:var(--err);background:color-mix(in srgb,var(--err) 7%,var(--surface))}}.sm.o span,.st.o{{color:var(--err)}}
.sm.t{{border-color:var(--warn)}}.sm.t span,.st.t{{color:var(--warn)}}
.sm.h span,.st.h{{color:var(--ok)}}
.sm:hover{{box-shadow:var(--shadow-md)}}
.leg{{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:var(--chip);color:var(--ink-3);margin-top:var(--s3)}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));gap:var(--s3);counter-reset:s;padding:0;margin:0;list-style:none}}
.steps li{{counter-increment:s;padding:var(--s4);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);font-size:var(--small);line-height:1.9;color:var(--ink-2)}}
.steps li::before{{content:counter(s,persian);display:grid;place-items:center;width:1.9em;height:1.9em;border-radius:50%;background:var(--c);color:var(--paper);font-weight:650;margin-bottom:6px}}
.steps b{{color:var(--ink)}}
.note{{padding:var(--s3) var(--s4);border-radius:var(--r-md);background:color-mix(in srgb,var(--warn) 9%,var(--paper));border:1px solid color-mix(in srgb,var(--warn) 40%,var(--line));font-size:var(--small);line-height:1.9;color:var(--ink-2);max-width:60em;margin:var(--s4) 0 0}}
.seat{{padding-block:var(--s5);border-top:1px dashed var(--line-strong);scroll-margin-top:8px}}
.seat:target{{background:color-mix(in srgb,var(--c) 6%,transparent);box-shadow:0 0 0 12px color-mix(in srgb,var(--c) 6%,transparent);border-radius:var(--r-md)}}
.sh{{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}}.sh h3{{margin:0;font-size:var(--h4)}}
.st{{font-size:var(--chip);font-weight:600;padding:1px 10px;border-radius:var(--r-full);border:1px solid currentColor}}
.who{{margin:4px 0 0;font-size:var(--chip);color:var(--ink-3)}}.why{{margin:var(--s2) 0 var(--s3);color:var(--ink-2);line-height:1.95;max-width:46em}}
.fst{{margin:0 0 var(--s3);font-size:var(--small);color:var(--ink-2)}}.fst a{{color:var(--c);font-weight:650}}
.task.first{{border-color:var(--c)}}.fs{{font-size:var(--chip);font-weight:650;color:var(--paper);background:var(--c);border-radius:var(--r-full);padding:0 9px}}
.tasks{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,310px),1fr));gap:var(--s3)}}
.task{{padding:var(--s4);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);display:grid;gap:var(--s2);align-content:start;min-width:0;scroll-margin-top:8px}}
.task:target{{border-color:var(--c);box-shadow:0 0 0 2px var(--c)}}
.task header{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
.task code{{font:650 var(--chip) ui-monospace,monospace;background:var(--ink);color:var(--paper);padding:1px 8px;border-radius:var(--r-sm);direction:ltr}}
.task h4{{margin:0;font-size:var(--small);flex:1 1 10em}}
.sz{{font-size:var(--chip);color:var(--ink-3);border:1px solid var(--line-strong);border-radius:var(--r-full);padding:0 9px}}
.task dl{{margin:0;display:grid;gap:2px}}.task dt{{font-size:var(--chip);font-weight:650;color:var(--c);margin-top:4px}}
.task dd{{margin:0;font-size:var(--small);line-height:1.85;color:var(--ink-2)}}.task dd a{{color:var(--c);white-space:nowrap}}
.cp{{justify-self:start;margin-top:var(--s2);font:inherit;font-size:var(--chip);padding:5px 14px;border-radius:var(--r-full);border:1px solid var(--c);background:none;color:var(--c);cursor:pointer}}
.cp:hover,.cp.ok{{background:var(--c);color:var(--paper)}}
ul.str{{list-style:none;margin:0;padding:0;display:grid;gap:10px;max-width:44em}}
ul.str li{{display:grid;grid-template-columns:minmax(0,11em) minmax(0,1fr) auto;gap:10px;align-items:center;font-size:var(--small)}}
.bar{{display:grid;grid-template-columns:repeat({NS},1fr);gap:3px}}.bar i{{height:9px;border-radius:5px;background:var(--surface-subtle);border:1px solid var(--line)}}.bar i.on{{background:var(--c);border-color:var(--c)}}
ul.str em{{font-style:normal;font-size:var(--chip);color:var(--ink-3);min-width:6.5em}}
ul.log{{list-style:none;margin:0;padding:0;display:grid;gap:6px;font-size:var(--small);color:var(--ink-2);max-width:60em}}
ul.log time{{font-size:var(--chip);color:var(--ink-3);margin-inline-end:10px;font-variant-numeric:tabular-nums}}
.go{{display:flex;flex-wrap:wrap;gap:8px;margin-top:var(--s4)}}
.go a{{font-size:var(--small);padding:4px 13px;border:1px solid var(--line-strong);border-radius:var(--r-full);color:var(--ink-2);text-decoration:none}}.go a:hover{{border-color:var(--c)}}
#out{{position:fixed;inset:auto 0 0 0;z-index:20;background:var(--surface);border-top:2px solid var(--c);box-shadow:var(--shadow-lg);padding:var(--s3) max(16px,env(safe-area-inset-left,0px)) calc(var(--s3) + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-right,0px));display:grid;gap:8px}}
#out[hidden]{{display:none}}#out p{{margin:0;font-size:var(--small);color:var(--ink-2)}}
#out textarea{{width:100%;min-height:7.5em;font:inherit;font-size:var(--small);padding:8px;border:1px solid var(--line-strong);border-radius:var(--r-md);background:var(--paper);color:var(--ink);box-sizing:border-box}}
#out button{{justify-self:start;border:1px solid var(--line-strong);background:none;color:var(--ink-2);border-radius:var(--r-full);padding:2px 12px;cursor:pointer;font:inherit}}
footer.f{{border-top:1px solid var(--line);padding-block:var(--s5);font-size:var(--small);color:var(--ink-3)}}footer.f a{{color:var(--ink-2);margin-inline-end:var(--s4)}}
</style>
</head>
<body>
<main class="wrap">
<h1>میز کار: کجا به شما نیاز داریم</h1>
<p class="lead">ساخت ایران کار داوطلبانه و غیرانتفاعی است. اینجا می‌بینید هر تخصص کجای کار می‌نشیند، مسئله دقیقاً چیست، چه داریم و از شما چه می‌خواهیم. هر مسئله یک کد دارد؛ اگر یکی به کار شما می‌خورد، همان را بردارید.</p>
<div class="nums"><div><b>{fa(len(seats))}</b><span>صندلی تخصصی</span></div><div><b>{fa(cnt["open"])}</b><span>جای خالی</span></div><div><b>{fa(ntask)}</b><span>مسئلهٔ باز</span></div><div><b>{fa(len(SK["risks"]))}</b><span>ریسک در دفتر</span></div><div><b>{fa(reg["concepts"])}</b><span>مفهوم در لایهٔ علم</span></div></div>

<section class="b" id="seats">
<h2>صندلی‌ها</h2>
<p class="sub">روی هر صندلی بزنید تا مسئله‌هایش را ببینید. نشانی هر صندلی را می‌شود جدا برای یک متخصص فرستاد.</p>
<div class="seatmap">{seatmap}</div>
<div class="leg"><span style="color:var(--err)">┅ جای خالی</span><span style="color:var(--warn)">━ در گفت‌وگو</span><span style="color:var(--ok)">━ یک نفر هست</span></div>
</section>

<section class="b" id="how">
<h2>چطور کمک کنم</h2>
<ol class="steps">
<li><b>مسئله را پیدا کنید.</b> صندلی خودتان را باز کنید و ببینید کدام مسئله به کارتان می‌خورد. اگر مسئلهٔ مهم‌تری می‌بینید که اینجا نیست، همان را بگویید.</li>
<li><b>متن آماده را کپی کنید.</b> دکمهٔ زیر هر مسئله متنی می‌سازد با کد مسئله و چند جای خالی برای تخصص و وقت شما.</li>
<li><b>برای کسی که شما را دعوت کرده بفرستید.</b> همان‌جا می‌توانید فرد یا ایدهٔ دیگری را هم معرفی کنید.</li>
</ol>
<p class="sub" style="margin-top:var(--s4)">این میز برای آماده‌کردنِ «روز بعد» است. برای اینکه امروز، در جایگاه خودتان، چه قدمی شدنی است، کارت‌های <a href="{SIM}gam.html">«قدمِ تو» در پَرِ سیمرغ ↗</a> را ببینید؛ بخش «خطر» همان صفحه را رد نکنید.</p>
<p class="note">این صفحه هیچ نام و اطلاعاتی جمع نمی‌کند و فرمی ندارد. اگر در ایران هستید، دربارهٔ این کار در جای عمومی و با نام واقعی ننویسید و فقط از راه امنی که با دعوت‌کننده‌تان قرار گذاشته‌اید پیام بدهید.</p>
</section>

<section class="b" id="briefs">
<h2>مسئله‌ها به تفکیک صندلی</h2>
<p class="sub">اندازه‌ها تقریبی است: کوچک یعنی چند ساعت، متوسط چند روز، بزرگ چند هفته.</p>
{briefs}
</section>

<section class="b" id="progress">
<h2>کل پروژه کجاست</h2>
<p class="sub">هیچ بخشی هنوز از بازبینی متخصص نگذشته است؛ همه‌چیز پیش‌نویس است.</p>
<ul class="str">{streams}</ul>
<div class="go"><a href="day.html">روز بعد ←</a><a href="../atlas/coverage.html">نقشهٔ پوشش و نقشهٔ راه ←</a><a href="index.html">صفحهٔ ساخت ایران ←</a><a href="../atlas/story.html">داستان کل پروژه و کمبودها ←</a><a href="../atlas/sitemap.html">نقشهٔ سایت ←</a></div>
</section>

<section class="b" id="log">
<h2>آخرین تغییرها</h2>
<p class="sub">از تاریخچهٔ خود مخزن خوانده می‌شود.</p>
<ul class="log">{changes}</ul>
</section>
</main>
<div id="out" hidden><p>این متن را کپی کنید، جاهای خالی را پر کنید و برای دعوت‌کننده‌تان بفرستید.</p><textarea readonly></textarea><button type="button">بستن</button></div>
<footer class="f"><div class="wrap"><a href="../">دانش‌سرا</a><a href="index.html">ساخت ایران</a><a href="../atlas/sitemap.html">نقشهٔ سایت</a></div></footer>
<script>
(() => {{
const out = document.getElementById("out"), ta = out.querySelector("textarea");
document.addEventListener("click", e => {{
  const b = e.target.closest(".cp");
  if (b) {{ ta.value = b.dataset.t; out.hidden = false; ta.select(); const done = () => {{ b.classList.add("ok"); b.textContent = "کپی شد ✓"; }}; try {{ navigator.clipboard.writeText(b.dataset.t).then(done, () => {{}}); }} catch (_) {{}} return; }}
  if (e.target.closest("#out button")) out.hidden = true;
}});
}})();
</script>
</body>
</html>
'''
open('sakht/work.html', 'w', encoding='utf-8').write(page)
print(f'sakht/work.html: {len(seats)} seats ({cnt}), {ntask} tasks, {len(log)} log lines')
