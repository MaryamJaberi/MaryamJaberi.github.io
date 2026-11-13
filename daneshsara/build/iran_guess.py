# -*- coding: utf-8 -*-
"""Build iran/tools/guess.html — «اول حدس بزن: ایران در عدد». Twelve questions; each answer is the
number already recorded in an iran/*.json note (grade, year, source and critique are read from the note)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
# note, question, min, max, step, answer, unit, one-line reveal
Q = [
 ['urbanization', 'از هر ۱۰۰ ایرانی چند نفر شهرنشین‌اند؟', 0, 100, 1, 74, 'نفر از ۱۰۰', 'سرشماری ۱۳۹۵. در ۱۳۳۵ حدود ۳۱ بود.'],
 ['fertility', 'هر زن ایرانی در دههٔ ۱۴۰۰ به‌طور میانگین چند فرزند می‌آورد؟', 0, 7, 0.1, 1.7, 'فرزند', 'در اوایل دههٔ ۱۳۶۰ حدود ۶٫۵ بود؛ یکی از تندترین افت‌های جهان.'],
 ['consanguinity', 'از هر ۱۰۰ ازدواج چندتا خویشاوندی است؟', 0, 100, 1, 38.6, 'ازدواج از ۱۰۰', 'نمونهٔ ملی اوایل دههٔ ۱۳۸۰؛ روند کاهشی گزارش شده.'],
 ['mental-disorder-prevalence', 'از هر ۱۰۰ بزرگسال، چند نفر در یک سال دست‌کم یک اختلال روانی داشته‌اند؟', 0, 100, 1, 23.6, 'نفر از ۱۰۰', 'پیمایش ملی سلامت روان ۱۳۹۰، با مصاحبهٔ تشخیصی.'],
 ['social-trust', 'از هر ۱۰۰ نفر چند نفر می‌گویند «به بیشتر مردم می‌شود اعتماد کرد»؟', 0, 100, 1, 12.5, 'نفر از ۱۰۰', 'پیمایش جهانی ارزش‌ها: حدود ۱۰ تا ۱۵؛ ردهٔ کشورهای کم‌اعتماد.'],
 ['poverty-rate', 'از هر ۱۰۰ نفر چند نفر زیر خط فقر ۶٫۸۵ دلار در روز زندگی می‌کنند؟', 0, 100, 1, 19.9, 'نفر از ۱۰۰', 'بانک جهانی، ۱۴۰۲؛ اوج ۲۹٫۳ در ۱۳۹۹.'],
 ['child-marriage', 'از هر ۱۰۰ زن چند نفر پیش از ۱۸ سالگی ازدواج کرده‌اند؟', 0, 100, 1, 17, 'نفر از ۱۰۰', 'داده‌های یونیسف؛ حدود ۳ نفر پیش از ۱۵ سالگی.'],
 ['suicide-rate', 'نرخ خودکشی در ایران از میانگین جهانی (حدود ۹ در صد هزار) بیشتر است یا کمتر؟ عدد ایران را حدس بزن.', 0, 30, 0.5, 5, 'در صد هزار نفر', 'برآورد سازمان جهانی بهداشت ۲۰۱۹؛ ثبت ناقص عدد را پایین می‌آورد.'],
 ['happiness-rank', 'ایران در رده‌بندی شادکامی میان ۱۴۳ کشور چندم است؟', 1, 143, 1, 100, 'از ۱۴۳', 'گزارش جهانی شادکامی ۲۰۲۴.'],
 ['political-attitudes-2026', 'در نظرسنجی آنلاین تیر ۱۴۰۵، از هر ۱۰۰ پاسخ‌دهنده چند نفر «تغییر نظام» را شرط تغییر دانستند؟', 0, 100, 1, 47, 'نفر از ۱۰۰', 'نمونهٔ آنلاین از راه فیلترشکن؛ جهت‌نماست نه دقیق.'],
 ['land-subsidence', 'تندترین فرونشست زمین در ایران سالی چند سانتی‌متر است؟', 0, 60, 1, 35, 'سانتی‌متر در سال', 'دشت رفسنجان، «بیش از ۳۵»؛ سنجش ماهواره‌ای ۲۰۱۴–۲۰۲۰.'],
 ['air-pollution-deaths', 'هر روز چند مرگ در ایران به آلودگی هوا نسبت داده می‌شود؟', 0, 400, 1, 161, 'مرگ در روز', 'برآورد رسمی سال ۱۴۰۳؛ روش محاسبه منتشر نشده است.'],
 ['electricity-deficit', 'در اوج مصرف تابستان، از هر ۱۰۰ واحد برقِ لازم چندتا کم بود؟', 0, 100, 1, 25, 'واحد از ۱۰۰', '۲۰ هزار مگاوات کسری از حدود ۸۰ هزار مگاوات نیاز، تابستان ۱۴۰۳.'],
 ['zagros-oak-decline', 'جنگل‌های زاگرس چند درصد پوشش جنگلی ایران‌اند؟', 0, 100, 1, 44, 'درصد', 'حدود ۶ میلیون هکتار؛ در لرستان نزدیک نیمی از پهنه نشانهٔ خشکیدگی دارد.'],
 ['road-deaths', 'نرخ مرگ جاده‌ای ایران در اوج خود (۱۳۸۴) چند نفر در صد هزار بود؟', 0, 80, 1, 40, 'در صد هزار نفر', 'تا ۱۳۹۸ به ۱۸٫۴ پایین آمد؛ در سال‌های اخیر دوباره بالا رفته.'],
 ['inflation', 'تورم ایران در سال ۲۰۲۵ چند درصد بود؟', 0, 100, 1, 42.2, 'درصد', 'بانک جهانی؛ از ۲۰۱۹ هر سال بالای ۳۰٪.'],
 ['executions-2025', 'از هر ۱۰۰ اعدام سال ۲۰۲۵، چندتا را منابع رسمی اعلام کردند؟', 0, 100, 1, 7, 'اعدام از ۱۰۰', '۱۱۳ مورد از دست‌کم ۱٬۶۳۹؛ یعنی کمتر از ۷.'],
 ['out-of-school-children', 'از هر ۱۰۰ نوجوان سن متوسطهٔ دوم چند نفر در مدرسه نیستند؟', 0, 100, 1, 16.1, 'نفر از ۱۰۰', 'آمار رسمی ۱۴۰۲–۱۴۰۳؛ شمارش مستقل بالاتر است.'],
 ['press-freedom', 'ایران در آزادی رسانه میان ۱۸۰ کشور چندم است؟ (۱ آزادترین)', 1, 180, 1, 177, 'از ۱۸۰', 'گزارشگران بدون مرز، ۲۰۲۶.'],
 ['corruption-perceptions', 'نمرهٔ ایران در شاخص ادراک فساد از ۱۰۰ چند است؟ (۱۰۰ یعنی بسیار پاک)', 0, 100, 1, 23, 'از ۱۰۰', 'شفافیت بین‌الملل؛ رتبهٔ ۱۵۳ از ۱۸۲.'],
 ['deserted-villages', 'از هر ۱۰۰ آبادی ثبت‌شدهٔ ایران چندتا خالی از سکنه است؟', 0, 100, 1, 45, 'آبادی از ۱۰۰', '۳۱ هزار از ۶۹ هزار، به گفتهٔ مقام رسمی؛ آبادی‌های بسیار کوچک را هم می‌شمارد.'],
 ['world-heritage', 'ایران چند اثر ثبت‌شده در میراث جهانی یونسکو دارد؟', 0, 60, 1, 30, 'اثر', '۵۷ اثر دیگر در فهرست موقت است.'],
 ['lake-urmia', 'دریاچهٔ ارومیه پس از دو دهه چند درصد مساحت اوجش را از دست داد؟', 0, 100, 1, 90, 'درصد', 'از اوج ۱۳۷۴؛ عدد تقریبی به نقل از ناسا.'],
]
out = []
for q in Q:
    d = json.load(open(f'{R}/iran/{q[0]}.json', encoding='utf-8'))
    out.append(q + [d['grade'], d['year'], d['source'][0]['title'], (d.get('critique') or '')[:220]])
TPL = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>اول حدس بزن: ایران در عدد | دانش‌سرا</title>
<meta name="description" content="بیست‌وسه پرسش دربارهٔ ایران: اول حدس بزن، بعد عدد، منبع و ردهٔ اعتبارش را ببین.">
<link rel="stylesheet" href="../../core/design/tokens.css">
<style>
main{padding-block:var(--s5) var(--s10);max-width:720px}
h1{font-size:var(--h1);margin:var(--s4) 0 var(--s2);line-height:var(--lh-tight)}
.lead{color:var(--ink-2);line-height:1.9;margin:0 0 var(--s4)}
.top{display:flex;justify-content:space-between;align-items:center;font-size:.86rem;color:var(--ink-2)}
.dots{display:flex;gap:4px;direction:ltr;flex-wrap:wrap}.dots i{width:10px;height:10px;border-radius:50%;background:var(--line-strong)}
.dots i.g{background:var(--ok)}.dots i.m{background:var(--warn)}.dots i.b{background:var(--err)}.dots i.c{outline:2px solid var(--primary);outline-offset:1px}
.q{margin-top:12px;padding:20px;border-radius:20px;border:1px solid var(--line-strong);background:var(--surface);display:grid;gap:14px}
.q h2{margin:0;font-size:1.25rem;line-height:1.8}
.val{font-size:2.2rem;font-weight:700;color:var(--primary);text-align:center;font-variant-numeric:tabular-nums}.val small{font-size:.9rem;font-weight:400;color:var(--ink-2)}
input[type=range]{width:100%;direction:ltr;accent-color:var(--primary);min-height:36px}
.sc{position:relative;height:34px;direction:ltr;border-radius:99px;background:var(--line)}
.sc i{position:absolute;top:-4px;width:4px;height:42px;border-radius:2px;transform:translateX(-50%)}
.sc .me{background:var(--primary)}.sc .tr{background:var(--ink)}
.sc span{position:absolute;top:44px;transform:translateX(-50%);font-size:.74rem;white-space:nowrap;direction:rtl}
.rev{display:grid;gap:10px;padding-top:6px}
.rev .big{font-size:1.1rem;line-height:1.9}
.g{display:inline-block;min-width:1.6em;text-align:center;padding:1px 8px;border-radius:8px;color:#fff;font-weight:700;background:var(--k)}
.rev small{color:var(--ink-3);line-height:1.8}
.crit{padding:10px 14px;border-radius:12px;background:var(--surface-subtle);font-size:.88rem;line-height:1.9}
.btn{font:inherit;padding:10px 20px;border-radius:99px;border:0;background:var(--primary);color:#fff;cursor:pointer;min-height:44px;justify-self:start}
.btn.o{background:none;color:var(--primary);border:1px solid var(--primary)}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.end{display:grid;gap:10px;line-height:1.9}
</style>
</head>
<body>
<main class="wrap" id="main">
<h1>اول حدس بزن: ایران در عدد</h1>
<p class="lead">بیست‌وسه پرسش. لغزنده را بگذار، بعد عدد واقعی، منبع و ردهٔ اعتبارش را ببین. هدف امتیاز نیست؛ دیدن فاصلهٔ تصور ما با داده است.</p>
<div class="top"><span id="cnt"></span><span class="dots" id="dots"></span></div>
<div class="q" id="q" aria-live="polite"></div>
</main>
<script>
const Q = __DATA__, $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const fa = n => String(n).replace(/\d/g, c => "۰۱۲۳۴۵۶۷۸۹"[c]).replace(".", "٫");
const GR = {A: "--grade-a", B: "--grade-b", C: "--grade-c", D: "--grade-d"};
let i = 0, res = [], shown = false;
const pos = (q, v) => 100 * (v - q[2]) / (q[3] - q[2]);
function dots(){ $("cnt").textContent = `پرسش ${fa(Math.min(i + 1, Q.length))} از ${fa(Q.length)}`; $("dots").innerHTML = Q.map((_, j) => `<i class="${res[j] || ""} ${j === i ? "c" : ""}"></i>`).join(""); }
function ask(){
  if (i >= Q.length) return end();
  const q = Q[i], mid = (q[2] + q[3]) / 2; shown = false;
  $("q").innerHTML = `<h2>${esc(q[1])}</h2><div class="val"><span id="v">${fa(mid)}</span> <small>${esc(q[6])}</small></div>
  <input type="range" id="r" min="${q[2]}" max="${q[3]}" step="${q[4]}" value="${mid}" aria-label="حدس تو"><div id="rev"><button class="btn" id="go" type="button">ببینم</button></div>`;
  dots();
}
function reveal(){
  const q = Q[i], g = +$("r").value, err = Math.abs(g - q[5]) / (q[3] - q[2]); shown = true;
  res[i] = err <= 0.07 ? "g" : err <= 0.2 ? "m" : "b"; $("r").disabled = true;
  const a = pos(q, g), b = pos(q, q[5]);
  $("rev").innerHTML = `<div class="rev"><div class="sc"><i class="me" style="left:${a}%"></i><i class="tr" style="left:${b}%"></i><span style="left:${Math.max(8, Math.min(92, a))}%;color:var(--primary)">تو: ${fa(g)}</span><span style="left:${Math.max(8, Math.min(92, b))}%;top:-24px"><b>داده: ${fa(q[5])}</b></span></div>
  <div class="big" style="margin-top:26px">${res[i] === "g" ? "نزدیک بودی." : g > q[5] ? "بیشتر از داده حدس زدی." : "کمتر از داده حدس زدی."} ${esc(q[7])}</div>
  <div><span class="g" style="--k:var(${GR[q[8]]})">${q[8]}</span> <small>ردهٔ اعتبار · سال ${fa(q[9])}</small></div>
  ${q[11] ? `<div class="crit"><b>چقدر می‌شود به این عدد تکیه کرد؟</b> ${esc(q[11])}${q[11].length >= 220 ? "…" : ""}</div>` : ""}
  <small dir="auto">منبع: ${esc(q[10])}</small>
  <div class="row"><button class="btn" id="nx" type="button">${i + 1 < Q.length ? "بعدی" : "پایان"}</button><a href="../#${q[0]}">یادداشت کامل ←</a></div></div>`;
  dots();
}
function end(){
  const n = k => res.filter(x => x === k).length; dots();
  const over = Q.filter((q, j) => res[j] !== "g").length;
  $("q").innerHTML = `<div class="end"><h2>تمام شد</h2><div>نزدیک: <b>${fa(n("g"))}</b> · کمی دور: <b>${fa(n("m"))}</b> · دور: <b>${fa(n("b"))}</b></div><div>جاهایی که دور بودی همان‌جاهایی است که ارزش دوباره خواندن دارد. و یادت باشد: خود این عددها هم ردهٔ اعتبار دارند؛ ردهٔ C و D را با احتیاط بگیر.</div><div class="row"><button class="btn" id="again" type="button">از نو</button><a href="../">همهٔ آمار ایران ←</a><a href="../../simorgh/plan.html#ledger">دفتر ویرانی‌ها ←</a></div></div>`;
}
$("q").addEventListener("input", e => { if (e.target.id === "r") $("v").textContent = fa(+e.target.value); });
$("q").addEventListener("click", e => { if (e.target.id === "go") reveal(); else if (e.target.id === "nx") { i++; ask(); } else if (e.target.id === "again") { i = 0; res = []; ask(); } });
ask();
</script>
</body>
</html>
'''
open(f'{R}/iran/tools/guess.html', 'w', encoding='utf-8').write(TPL.replace('__DATA__', json.dumps(out, ensure_ascii=False)))
print(f'iran/tools/guess.html: {len(out)} questions')
