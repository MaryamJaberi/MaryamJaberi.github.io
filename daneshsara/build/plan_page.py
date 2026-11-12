# -*- coding: utf-8 -*-
"""Build simorgh/plan.html — «نقشهٔ کلان سیمرغ»: the whole project in pictures.
Data: data/plan/plan.json (written by data/plan/make_plan.py)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
subprocess.run([sys.executable, f'{R}/data/plan/make_plan.py'], check=True, capture_output=True)
D = json.load(open(f'{R}/data/plan/plan.json', encoding='utf-8'))
DATA = json.dumps(D, ensure_ascii=False)

TPL = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>نقشهٔ کلان سیمرغ | سیمرغ | دانش‌سرا</title>
<meta name="description" content="کل پروژه در یک صفحهٔ تصویری: بازی مافیا و نظریهٔ بازی، علوم لازم، دفتر ویرانی‌ها، سی مرغ، سهم هر نفر، روز آزادی، محصولات و نقشهٔ راه.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
:root{--c:#b7791f;--have:var(--ok);--part:var(--warn);--none:var(--ink-3)}
main{padding-block:var(--s5) var(--s10)}
h1{font-size:var(--h1);margin:var(--s4) 0 var(--s2);line-height:var(--lh-tight);text-wrap:balance}
.lead{color:var(--ink-2);max-width:60ch;line-height:1.9;margin:0 0 var(--s4);font-size:1.05rem}
h2{font-size:var(--h3);margin:0 0 4px;text-wrap:balance}
h2 small{font-size:.8rem;font-weight:400;color:var(--ink-3);margin-inline-start:8px}
.sub{color:var(--ink-3);font-size:.92rem;line-height:1.8;margin:0 0 var(--s4);max-width:62ch}
section{padding-block:var(--s6);border-top:1px solid var(--line);scroll-margin-top:56px}
a{color:var(--primary)}
/* sticky section pills */
.pills{position:sticky;top:0;z-index:20;display:flex;gap:6px;overflow-x:auto;padding:8px 0;background:var(--paper);border-bottom:1px solid var(--line);scrollbar-width:none}
.pills a{flex:none;font-size:.85rem;padding:6px 12px;border-radius:999px;border:1px solid var(--line-strong);color:var(--ink-2);text-decoration:none;background:var(--surface);min-height:36px;display:inline-flex;align-items:center}
.pills a:hover{border-color:var(--c);color:var(--c)}
/* layers picture */
.stack{display:grid;gap:8px;max-width:760px}
.lay{display:grid;grid-template-columns:44px minmax(0,1fr);gap:12px;align-items:center;padding:12px 16px;border-radius:16px;border:1px solid var(--line);background:var(--surface);text-decoration:none;color:inherit;border-inline-start:6px solid var(--k)}
.lay:hover{border-color:var(--k)}
.lay i{font-style:normal;font-weight:700;font-size:1.3rem;color:var(--k);text-align:center}
.lay b{display:block}.lay span{color:var(--ink-2);font-size:.9rem;line-height:1.7}
.up{text-align:center;color:var(--ink-3);font-size:.8rem;margin:-2px 0}
/* cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.card{padding:12px 14px;border-radius:14px;border:1px solid var(--line);background:var(--surface);min-width:0;line-height:1.7;font-size:.92rem;border-top:3px solid var(--k,var(--line-strong))}
.card b{display:block;margin-bottom:2px}
.card p{margin:0;color:var(--ink-2);font-size:.86rem}
.card a.more{font-size:.82rem;text-decoration:none}
details.card summary{cursor:pointer;list-style:none;font-weight:650;display:flex;justify-content:space-between;gap:8px;align-items:center}
details.card summary::-webkit-details-marker{display:none}
details.card summary::after{content:"+";color:var(--ink-3);font-weight:400}
details.card[open] summary::after{content:"–"}
details.card ul{margin:8px 0 0;padding-inline-start:18px;color:var(--ink-2);font-size:.86rem}
.st{font-size:.7rem;padding:1px 8px;border-radius:99px;color:#fff;font-weight:600;white-space:nowrap;background:var(--none)}
.st.have{background:var(--have)}.st.part{background:var(--part)}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.82rem;color:var(--ink-2);margin:0 0 12px}
.meter{display:flex;height:10px;border-radius:99px;overflow:hidden;background:var(--surface-subtle);max-width:420px;margin:0 0 6px}
.meter i{display:block}
/* game table */
.gm{display:grid;gap:8px}
.gmr{display:grid;grid-template-columns:minmax(0,1fr) 28px minmax(0,1fr) minmax(0,.8fr);gap:8px;align-items:center;padding:10px 14px;border-radius:14px;border:1px solid var(--line);background:var(--surface);font-size:.9rem;line-height:1.7}
.gmr .g1{font-weight:650}.gmr .ar{color:var(--ink-3);text-align:center}.gmr .g2{color:var(--ink-2)}
.gmr a{font-size:.82rem;padding:3px 10px;border-radius:99px;border:1px solid var(--c);color:var(--c);text-decoration:none;justify-self:start}
@media (max-width:700px){.gmr{grid-template-columns:minmax(0,1fr)}.gmr .ar{display:none}}
/* simulator */
.sim{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:18px;align-items:start;padding:16px;border-radius:18px;border:1px solid var(--line);background:var(--surface);margin-top:14px}
@media (max-width:760px){.sim{grid-template-columns:minmax(0,1fr)}}
.sim canvas{width:100%;max-width:300px;aspect-ratio:1;border-radius:12px;background:var(--surface-subtle);display:block;margin-inline:auto}
.sim label{display:grid;gap:2px;font-size:.88rem;margin-bottom:12px}
.sim input[type=range]{width:100%;direction:ltr;accent-color:var(--c)}
.sim output{font-weight:700;color:var(--c)}
.res{font-size:1rem;line-height:1.8;padding:10px 12px;border-radius:12px;background:var(--surface-subtle)}
.res b{font-size:1.5rem}
/* me */
.me{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:18px;padding:16px;border-radius:18px;border:2px solid var(--c);background:var(--surface)}
@media (max-width:760px){.me{grid-template-columns:minmax(0,1fr)}}
.me fieldset{border:0;padding:0;margin:0 0 12px}.me legend{font-weight:650;font-size:.9rem;margin-bottom:6px}
.ch{display:flex;flex-wrap:wrap;gap:6px}
.ch button,.flt button{font:inherit;font-size:.85rem;min-height:38px;padding:5px 12px;border-radius:99px;border:1px solid var(--line-strong);background:var(--paper);color:var(--ink);cursor:pointer}
.ch button[aria-pressed=true],.flt button[aria-pressed=true]{background:var(--c);border-color:var(--c);color:#fff;font-weight:650}
.steps{display:grid;gap:8px}
.step{padding:10px 12px;border-radius:12px;background:var(--surface-subtle);border-inline-start:4px solid var(--c);line-height:1.8;font-size:.93rem}
.step small{display:block;color:var(--ink-3);font-size:.78rem}
.flt{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.tk{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:10px;align-items:center;padding:8px 12px;border-radius:12px;border:1px solid var(--line);background:var(--surface);font-size:.9rem}
.tk .w{font-size:.72rem;padding:1px 8px;border-radius:99px;border:1px solid var(--line-strong);color:var(--ink-2);white-space:nowrap}
.tk .bd{font-size:.76rem;color:var(--ink-3);white-space:nowrap}
@media (max-width:560px){.tk{grid-template-columns:minmax(0,1fr)}}
.tks{display:grid;gap:6px}
/* road */
.road{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px}
@media (max-width:860px){.road{grid-template-columns:minmax(0,1fr)}}
.ph{padding:12px;border-radius:14px;border:1px solid var(--line);background:var(--surface);font-size:.86rem;line-height:1.7;display:grid;gap:6px;align-content:start}
.ph.now{border:2px solid var(--c);background:color-mix(in srgb,var(--c) 8%,var(--surface))}
.ph b{font-size:1rem}.ph .gate{margin-top:4px;padding-top:6px;border-top:1px dashed var(--line-strong);color:var(--ink-2);font-size:.8rem}
.ph .gate::before{content:"◆ دروازه: ";color:var(--c)}
.todo{display:grid;gap:8px;max-width:760px}
.todo a{display:grid;grid-template-columns:28px minmax(0,1fr);gap:10px;padding:10px 14px;border-radius:14px;border:1px solid var(--line);background:var(--surface);text-decoration:none;color:inherit;line-height:1.7;font-size:.93rem}
.todo a:hover{border-color:var(--c)}.todo i{font-style:normal;font-weight:700;color:var(--c)}
.todo span{color:var(--ink-3);font-size:.82rem;display:block}
.red{padding:12px 16px;border-radius:14px;border:1.5px dashed var(--err);background:color-mix(in srgb,var(--err) 5%,var(--paper));font-size:.9rem;line-height:1.9;max-width:760px}
.src{font-size:.8rem;color:var(--ink-3);line-height:1.9}.src a{color:var(--ink-2)}
</style>
</head>
<body>
<main class="wrap" id="main">
<h1>نقشهٔ کلان سیمرغ</h1>
<p class="lead">کل پروژه در یک صفحه: با دانش مستند بفهمیم چرا ایران به این حال رسیده، با بازی مافیا ببینیم «شهر» چطور می‌برد، آدم‌ها را دعوت کنیم، با محصولات پول و شبکه بسازیم، و از حالا روشن کنیم روز آزادی هر کس چه می‌کند.</p>
<nav class="pills" aria-label="بخش‌های صفحه">
<a href="#big">تصویر کلی</a><a href="#todo">کارهای گرداننده</a><a href="#game">بازی</a><a href="#me">سهم من</a><a href="#birds">سی مرغ</a><a href="#ledger">ویرانی‌ها</a><a href="#sci">علوم</a><a href="#groups">مردم</a><a href="#day">روز آزادی</a><a href="#risks">خطرها</a><a href="#money">درآمد</a><a href="#tools">ابزارها</a><a href="#road">نقشهٔ راه</a><a href="../core/log.html">دفتر پروژه ↗</a>
</nav>

<section id="big"><h2>تصویر کلی: پنج لایه روی هم</h2><p class="sub">هر لایه از لایهٔ زیرش تغذیه می‌شود. روی هر لایه بزنید.</p>
<div class="stack" id="stack"></div></section>

<section id="todo"><h2>کارهای گرداننده <small>به ترتیب</small></h2><p class="sub">کارهایی که فقط گردانندهٔ پروژه می‌تواند انجام بدهد. هرکدام یک لینک دارد.</p>
<div class="todo" id="todos"></div></section>

<section id="game"><h2>بازی مافیا، به زبان علم</h2><p class="sub">هر قاعدهٔ بازی یک سازوکار واقعی است که پژوهش دارد. راست: بازی. چپ: واقعیت و نام علمی‌اش.</p>
<div class="gm" id="gm"></div>
<div class="sim"><div><canvas id="cv" width="300" height="300" aria-label="شبیه‌سازی شهر"></canvas></div>
<div><b>خودت امتحان کن: شهر کی راه می‌افتد؟</b>
<p class="sub" style="margin:4px 0 12px">چهارصد شهروند. هرکس وقتی می‌پیوندد که ببیند به اندازهٔ «آستانه»‌اش دیگران پیوسته‌اند. مافیا با کنترل راوی نمی‌گذارد همدیگر را ببینند.</p>
<label>ترس (میانگین آستانه): <output id="oF"></output><input type="range" id="sF" min="5" max="70" value="30"></label>
<label>گوناگونی آدم‌ها (چند نفر بی‌باک‌تر): <output id="oS"></output><input type="range" id="sS" min="2" max="30" value="16"></label>
<label>چقدر همدیگر را می‌بینند (ضد سانسور): <output id="oV"></output><input type="range" id="sV" min="10" max="100" value="60"></label>
<div class="res" id="res" aria-live="polite"></div>
<p class="src" style="margin:8px 0 0">مدل سادهٔ آستانه (گرانووتر ۱۹۷۸)؛ ابزار فهم است نه پیش‌بینی. نسخهٔ کامل‌تر در <a href="../soc/tools/lab.html">آزمایشگاه جامعه</a>.</p></div></div>
<div class="red" style="margin-top:14px"><b>خط قرمز:</b> «مافیا» فقط در بازی است. این پروژه هیچ‌گاه به آدم واقعی برچسب مافیا یا جاسوس نمی‌زند، فهرست و پرونده نمی‌سازد، و از کسی که داخل ایران است کار پرخطر نمی‌خواهد.</div>
</section>

<section id="me"><h2>سهم من چیست؟</h2><p class="sub">دو پرسش، سه قدم. چیزی ذخیره یا فرستاده نمی‌شود.</p>
<div class="me"><div>
<fieldset><legend>کار یا مهارتت به کدام نزدیک‌تر است؟</legend><div class="ch" id="qS"></div></fieldset>
<fieldset><legend>کجا هستی؟</legend><div class="ch" id="qL"><button type="button" data-v="in" aria-pressed="false">داخل ایران</button><button type="button" data-v="out" aria-pressed="true">خارج از ایران</button></div></fieldset>
</div><div class="steps" id="steps" aria-live="polite"></div></div>
<p class="sub" style="margin-top:10px">کارت‌های دقیق‌تر برای هر قشر: <a href="https://maryamjaberi.github.io/simorgh/gam.html">۲۳ کارت «قدمِ تو» ↗</a> · برای متخصص‌ها: <a href="../sakht/work.html">میز کار ساخت ایران</a></p>
</section>

<section id="birds"><h2>سی مرغ <small>فهرست زنده</small></h2><p class="sub">هر مرغ یک گروه سازنده با یک هدف. این فهرست ثابت نیست: در طول راه مرغ‌ها کم، زیاد، یکی یا جدا می‌شوند. سه مرغ عمداً برای کسی است که تخصص ندارد.</p>
<div class="grid" id="bg"></div><p class="sub" style="margin-top:10px"><a href="birds.html">کارت هر مرغ را باز کن ←</a></p></section>

<section id="ledger"><h2>دفتر ویرانی‌ها</h2><p class="sub">آنچه باید ساخته شود، در نوزده حوزه. روی هر حوزه بزنید تا ریز آسیب‌ها را ببینید.</p>
<div class="meter" id="lm"></div><div class="legend" id="ll"></div>
<div class="grid" id="lg"></div></section>

<section id="sci"><h2>علوم لازم</h2><p class="sub">هر علم به یک پرسش دربارهٔ ایران جواب می‌دهد.</p>
<div class="meter" id="sm"></div><div class="legend" id="sl"></div>
<div class="grid" id="sg"></div></section>

<section id="groups"><h2>مردم و نیازهایشان</h2><p class="sub">بیست گروه که روی هم می‌افتند (هر کس عضو چند گروه است). فقط در سطح جمعیت؛ هیچ فهرستی از افراد ساخته نمی‌شود.</p>
<div class="grid" id="gg"></div></section>

<section id="day"><h2>روز آزادی و صد روز اول</h2><p class="sub">هر کس، حتی بی‌تخصص، از پیش بداند چه می‌کند.</p>
<div class="flt" id="tf"></div><div class="tks" id="tl"></div>
<h3 style="margin:var(--s5) 0 var(--s2)">جشن‌ها</h3><div class="grid" id="cg"></div>
<p class="sub" style="margin-top:10px" id="cr"></p>
<p class="sub">صفحه‌های کامل‌تر: <a href="../sakht/day.html">روز بعد</a> · <a href="../sakht/">ساخت ایران</a></p></section>

<section id="risks"><h2>خطرهای گذار</h2><p class="sub">پانزده خطر، نشانهٔ هشدار هرکدام و پاسخ از پیش آماده.</p>
<div class="grid" id="rg"></div></section>

<section id="money"><h2>محصولات و درآمد در اروپا</h2><p class="sub">به ترتیب اولویت: هرچه زودتر پول بسازد و سرمایهٔ کمتری بخواهد، بالاتر است. شش‌تای اول قدم اول هم دارند. این ترتیب با هر نتیجهٔ تازه عوض می‌شود.</p>
<div class="flt" id="pf"></div><div class="grid" id="pg"></div>
<p class="sub" style="margin-top:10px">فعلاً هدف فقط نخستین درآمد است. ساختار مالی (نهاد غیرانتفاعی جدا برای سیمرغ، حساب شفاف) وقتی لازم می‌شود که پول واقعی برسد، و آن‌وقت با حسابدار بسته می‌شود؛ این صفحه مشاورهٔ حقوقی یا مالی نیست.</p></section>

<section id="tools"><h2>ابزارها</h2><p class="sub">آنچه هست و آنچه باید ساخته شود.</p><div class="grid" id="tg"></div></section>

<section id="road"><h2>نقشهٔ راه</h2><p class="sub">مرحله‌ها با دروازه پیش می‌روند نه با تاریخ: زمان روز آزادی دست ما نیست، آمادگی هست.</p>
<div class="road" id="rd"></div></section>

<section><h2>منابع این صفحه</h2><div class="src" id="srcs"></div></section>
</main>
<script>
const D = __DATA__;
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const fa = n => String(n).replace(/\d/g, c => "۰۱۲۳۴۵۶۷۸۹"[c]);
const ST = {have: "هست", part: "ناقص", none: "ندارد"};
const FAM = ["--fam-psy", "--fam-bio", "--fam-soc", "--fam-hum", "--fam-hist", "--fam-formal"];
const st = s => `<span class="st ${s}">${ST[s]}</span>`;

// layers
const LK = ["--fam-psy", "--primary", "--c", "--fam-soc", "--ok"];
$("stack").innerHTML = D.layers.map((l, i) => `<a class="lay" href="${l[2]}" style="--k:var(${LK[i]})"><i>${fa(i + 1)}</i><div><b>${esc(l[0])}</b><span>${esc(l[1])}</span></div></a>`).reverse().join('<div class="up">▲</div>');

// todos (project lead)
const TODO = [
 ["این صفحه را مرور کن", "هر جا غلط یا کم است بگو", "#big"],
 ["با «شهر کی راه می‌افتد» بازی کن", "سه دقیقه؛ اصل کل پروژه را نشان می‌دهد", "#game"],
 ["«سهم من» را امتحان کن", "بگو قدم‌ها درست‌اند یا نه", "#me"],
 ["محصول شمارهٔ یک را شروع کن", "اولویت‌ها را من چیده‌ام؛ قدم اول هرکدام نوشته شده", "#money"],
 ["کارت‌های سی مرغ را ورق بزن", "فهرست زنده است؛ هر وقت چیزی کم یا زیاد دیدی بگو", "birds.html"],
 ["یک شب بازی با حلقهٔ خودی", "با اپ میز خدا و نقش‌های مافیای ایران", "https://maryamjaberi.github.io/simorgh/roles.html"],
 ["پروندهٔ امنیت را برای متخصص امنیت بفرست", "دعوت‌نامه با مدل تهدید و ده مسئلهٔ باز", "security.html"],
 ["نخستین مشتری آزمایشی سنجش سازمان", "صفحه‌ای که باید نشانشان بدهی", "../wellbeing/orgsvc.html"],
 ["مدخل‌های تازه را مرور کن", "برگهٔ بازبینی دانش‌سرا", "../core/review.html"],
];
$("todos").innerHTML = TODO.map((t, i) => `<a href="${t[2]}"><i>${fa(i + 1)}</i><div>${esc(t[0])}<span>${esc(t[1])}</span></div></a>`).join("");

// game
$("gm").innerHTML = D.game.map(g => `<div class="gmr"><div class="g1">${esc(g[0])}</div><div class="ar">←</div><div class="g2">${esc(g[1])}</div><a href="${g[3]}">${esc(g[2])}</a></div>`).join("");

// simulator: Granovetter thresholds with limited visibility
(function(){
  const N = 400, cv = $("cv"), cx = cv.getContext("2d");
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const z = Array.from({length: N}, () => { let u = 0; for (let i = 0; i < 6; i++) u += rnd(); return (u - 3) / Math.sqrt(0.5); });
  const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  function run(){
    const F = +$("sF").value, S = +$("sS").value, V = +$("sV").value / 100;
    $("oF").textContent = fa(F) + "٪"; $("oS").textContent = fa(S); $("oV").textContent = fa(Math.round(V * 100)) + "٪";
    const th = z.map(x => F + S * x);
    let joined = 0, on = new Array(N).fill(false);
    for (let it = 0; it < 60; it++) {
      const seen = joined / N * 100 * V; let c = 0;
      for (let i = 0; i < N; i++) { on[i] = th[i] <= seen; if (on[i]) c++; }
      if (c === joined) break; joined = c;
    }
    const a = css("--c") || "#b7791f", q = css("--line-strong") || "#ccc";
    cx.clearRect(0, 0, 300, 300);
    for (let i = 0; i < N; i++) { const x = (i % 20) * 15 + 7.5, y = Math.floor(i / 20) * 15 + 7.5; cx.beginPath(); cx.arc(x, y, 5, 0, 6.3); cx.fillStyle = on[i] ? a : q; cx.fill(); }
    const p = Math.round(joined / N * 100);
    $("res").innerHTML = `<b>${fa(p)}٪</b> شهر به هم پیوست. ` + (p >= 90 ? "موج کامل شد: هر کس دید دیگران هستند، آمد." : p >= 30 ? "موج راه افتاد اما ایستاد: آدم‌های محتاط‌تر هنوز کافی نمی‌بینند." : p > 0 ? "فقط بی‌باک‌ترین‌ها آمدند و تنها ماندند." : "هیچ‌کس اول نشد. همه منتظر دیگری‌اند.") + ` <br><small style="color:var(--ink-3)">نکته: «دیدن همدیگر» را بالا ببر و ببین بی آنکه ترس کم شود چه می‌شود.</small>`;
  }
  ["sF", "sS", "sV"].forEach(id => $(id).addEventListener("input", run)); run();
})();

// me
(function(){
  let skill = Object.keys(D.me).at(-1), loc = "out";
  $("qS").innerHTML = Object.keys(D.me).map(k => `<button type="button" data-v="${esc(k)}" aria-pressed="${k === skill}">${esc(k)}</button>`).join("");
  function show(){
    const m = D.me[skill];
    $("steps").innerHTML = `<div class="step"><small>مرغ‌هایی که با تو جورند</small><b>${m[0].map(b => `<a href="birds.html#${encodeURIComponent(b)}">${esc(b)}</a>`).join(" · ")}</b></div>
      <div class="step"><small>قدم امروز${loc === "in" ? " (داخل ایران: فقط کار کم‌خطر)" : ""}</small>${esc(loc === "in" ? m[2] : m[1])}</div>
      <div class="step"><small>روز آزادی</small>${esc(m[3])}</div>
      <div class="step"><small>صد روز اول</small>${esc(m[4])}</div>`;
  }
  $("qS").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; skill = b.dataset.v; $("qS").querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); show(); });
  $("qL").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; loc = b.dataset.v; $("qL").querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); show(); });
  show();
})();

// birds
$("bg").innerHTML = D.birds.map((f, i) => `<div class="card" style="--k:var(${FAM[i]})"><b>${esc(f[0])}</b><p>${f[1].map(b => `<a class="more" href="birds.html#${encodeURIComponent(b)}">${esc(b)}</a>`).join(" · ")}</p></div>`).join("");

// meters
function meter(list, idx, m, l){
  const c = {have: 0, part: 0, none: 0}; list.forEach(x => c[x[idx]]++);
  $(m).innerHTML = ["have", "part", "none"].map(k => `<i style="width:${c[k] / list.length * 100}%;background:var(--${k})"></i>`).join("");
  $(l).innerHTML = ["have", "part", "none"].map(k => `<span>${st(k)} ${fa(c[k])}</span>`).join("") + `<span>در دانش‌سرا</span>`;
}
meter(D.ledger, 2, "lm", "ll"); meter(D.sciences, 2, "sm", "sl");

// ledger
$("lg").innerHTML = D.ledger.map(d => `<details class="card"><summary><span>${esc(d[0])} <small style="font-weight:400;color:var(--ink-3)">${fa(d[1].length)}</small></span>${st(d[2])}</summary><ul>${d[1].map(x => `<li>${esc(x)}</li>`).join("")}</ul><p style="margin-top:6px">نهاد مسئول: ${esc(d[4])}${d[3] ? ` · <a class="more" href="${d[3]}">داده و ریشه‌یابی ←</a>` : ""}</p></details>`).join("");

// sciences
$("sg").innerHTML = D.sciences.map(s => `<div class="card"><b style="display:flex;justify-content:space-between;gap:6px"><span>${esc(s[0])}</span>${st(s[2])}</b><p>${esc(s[1])}</p>${s[3] ? `<a class="more" href="${s[3]}">باز کن ←</a>` : ""}</div>`).join("");

// groups
$("gg").innerHTML = D.groups.map(g => `<div class="card"><b>${esc(g[0])}</b><p>نیاز: ${esc(g[1])}</p><p style="color:var(--c)">صد روز اول: ${esc(g[2])}</p></div>`).join("");

// tasks
(function(){
  const whens = ["همه", ...new Set(D.tasks.map(t => t[0]))]; let w = "همه", only = false;
  function draw(){
    $("tf").innerHTML = whens.map(x => `<button type="button" data-w="${x}" aria-pressed="${x === w}">${x === "همه" ? "همهٔ زمان‌ها" : x}</button>`).join("") + `<button type="button" id="onlyAll" aria-pressed="${only}">فقط کارهایی که تخصص نمی‌خواهد</button>`;
    const L = D.tasks.filter(t => (w === "همه" || t[0] === w) && (!only || t[2] === "همه"));
    $("tl").innerHTML = L.map(t => `<div class="tk"><span class="w">${esc(t[0])}</span><span>${esc(t[1])}</span><span class="bd">${t[2] === "همه" ? "همه" : t[2] === "مهارت" ? "با مهارت" : "متخصص"} · ${esc(t[3])}</span></div>`).join("") || "<p class='sub'>کاری با این فیلتر نیست.</p>";
  }
  $("tf").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; if (b.id === "onlyAll") only = !only; else w = b.dataset.w; draw(); });
  draw();
})();
$("cg").innerHTML = D.celebrations.map(c => `<div class="card" style="--k:var(--c)"><b>${esc(c[0])}</b><p>${esc(c[1])}</p></div>`).join("");
$("cr").textContent = "نقش‌ها در جشن: " + D.celebration_roles.join("، ");

// risks
$("rg").innerHTML = D.risks.map(r => `<details class="card" style="--k:var(--err)"><summary><span>${esc(r[0])}</span></summary><p style="margin-top:6px"><b style="display:inline">نشانه:</b> ${esc(r[1])}</p><p><b style="display:inline">پاسخ:</b> ${esc(r[2])}</p><p style="color:var(--c)">مرغ مسئول: ${esc(r[3])}</p></details>`).join("");

// products
(function(){
  const sp = ["همه", "زود", "میان", "دیر"]; let s = "همه";
  function draw(){
    $("pf").innerHTML = sp.map(x => `<button type="button" data-s="${x}" aria-pressed="${x === s}">${x === "همه" ? "همه" : x === "زود" ? "زودبازده" : x === "میان" ? "میان‌مدت" : "دیرتر"}</button>`).join("");
    $("pg").innerHTML = D.products.map((p, i) => [p, i]).filter(([p]) => s === "همه" || p[4] === s).map(([p, i]) => `<div class="card" style="--k:var(${p[5] === "have" ? "--ok" : "--c"})"><b style="display:flex;justify-content:space-between;gap:6px"><span>${fa(i + 1)}. ${esc(p[0])}</span>${p[5] === "have" ? st("have") : ""}</b><p>مشتری: ${esc(p[1])}</p><p>درآمد: ${esc(p[2])}</p><p>شبکه: ${esc(p[3])}</p>${p[7] ? `<p style="color:var(--c)">قدم اول: ${esc(p[7])}</p>` : ""}${p[6] ? `<a class="more" href="${p[6]}">صفحه‌اش ←</a>` : ""}</div>`).join("");
  }
  $("pf").addEventListener("click", e => { const b = e.target.closest("button"); if (b) { s = b.dataset.s; draw(); } });
  draw();
})();

// tools
$("tg").innerHTML = D.tools.map(t => `<div class="card"><b style="display:flex;justify-content:space-between;gap:6px"><span>${esc(t[0])}</span>${st(t[2])}</b><p>${esc(t[1])}</p>${t[3] ? `<a class="more" href="${t[3]}">باز کن ←</a>` : ""}</div>`).join("");

// roadmap
$("rd").innerHTML = D.roadmap.map((p, i) => `<div class="ph${i === 0 ? " now" : ""}"><b>${fa(i + 1)} · ${esc(p[0])}</b>${i === 0 ? '<small style="color:var(--c)">اکنون اینجاییم</small>' : ""}<span>${esc(p[1])}</span>${p[2] ? `<span class="gate">${esc(p[2])}</span>` : ""}</div>`).join("");

$("srcs").innerHTML = D.sources.map(s => s[1] ? `<a href="${s[1]}">${esc(s[0])}</a>` : esc(s[0])).join("<br>") + "<br>منابع هر مفهوم در مدخل خودش آمده است.";
</script>
</body>
</html>
'''
os.makedirs(f'{R}/simorgh', exist_ok=True)
open(f'{R}/simorgh/plan.html', 'w', encoding='utf-8').write(TPL.replace('__DATA__', DATA))
print(f'simorgh/plan.html: {len(D["ledger"])} ledger domains, {len(D["sciences"])} sciences, {len(D["tasks"])} tasks, {len(D["products"])} products')
