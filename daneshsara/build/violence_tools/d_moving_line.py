# -*- coding: utf-8 -*-
import json
from _head import page
TH = {"child": ["تنبیه بدنی کودک", "#A8481A"], "marriage": ["خشونت در ازدواج و خانه", "#9F1239"], "group": ["خشونت علیه یک گروه", "#5B4B8A"], "slave": ["برده‌داری", "#7A5F22"], "all": ["حق همه", "#0A6B60"]}
EV = [
 (1833, "slave", "بریتانیا برده‌داری را در مستعمره‌هایش لغو می‌کند.", "C"),
 (1865, "slave", "آمریکا: متمم سیزدهم قانون اساسی، لغو برده‌داری.", "C"),
 (1888, "slave", "برزیل، آخرین کشور قارهٔ آمریکا، برده‌داری را لغو می‌کند.", "C"),
 (1948, "all", "اعلامیهٔ جهانی حقوق بشر: حق زندگی و امنیت، و اینکه هیچ‌کس نباید شکنجه شود.", "A"),
 (1973, "group", "کنوانسیون سازمان ملل: آپارتاید جنایت است.", "A"),
 (1979, "child", "سوئد نخستین کشوری می‌شود که تنبیه بدنی کودک را همه‌جا، حتی در خانه، ممنوع می‌کند.", "A"),
 (1981, "marriage", "نیو ساوت ولز استرالیا تجاوز در ازدواج را جرم می‌کند.", "B"),
 (1983, "child", "فنلاند دومین کشور با ممنوعیت کامل تنبیه بدنی.", "A"),
 (1991, "marriage", "انگلستان: مجلس اعیان در پروندهٔ R v R معافیت شوهر را برمی‌دارد. تا آن روز، بر پایهٔ رساله‌ای از سال ۱۷۳۶، شوهر نمی‌توانست به تجاوز به همسرش محکوم شود.", "B"),
 (1993, "marriage", "کارولینای شمالی، آخرین ایالت آمریکا، تجاوز در ازدواج را جرم می‌کند.", "B"),
 (1996, "child", "هفده سال پس از سوئد، هنوز فقط پنج کشور ممنوعیت کامل دارند.", "A"),
 (1998, "group", "اساسنامهٔ رم: آپارتاید در فهرست جنایت‌های علیه بشریت دیوان کیفری بین‌المللی.", "A"),
 (2015, "marriage", "انگلستان و ولز «رفتار کنترل‌گرانه یا اجباری» را جرم می‌کنند: خشونتی بدون ضربه.", "A"),
 (2018, "marriage", "اسکاتلند و ایرلند قانون مشابه می‌گذارند.", "B"),
 (2019, "child", "فرانسه، آفریقای جنوبی، گرجستان و کوزوو؛ شمار کشورها به ۵۶ می‌رسد.", "A"),
 (2019, "marriage", "گزارش نهاد زنان ملل متحد: هنوز فقط چهار کشور از هر ده کشور تجاوز در ازدواج را جرم کرده‌اند.", "B"),
 (2020, "child", "ژاپن.", "A"),
 (2024, "child", "۶۷ کشور ممنوعیت کامل دارند.", "A"),
 (2026, "child", "۷۰ کشور. ۲۵ کشور دیگر قول داده‌اند.", "A"),
 (2026, "group", "چهارده کشور از جرم‌شدن «آپارتاید جنسیتی» پشتیبانی می‌کنند.", "B"),
 (2028, "group", "آغاز مذاکرهٔ پیمان جنایت علیه بشریت؛ هنوز تصمیمی نیست.", "B"),
]
css = """
.flt{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 var(--s4)}
.tl{position:relative;max-width:820px;padding-inline-start:26px;border-inline-start:3px solid var(--line-strong)}
.ev{position:relative;padding:0 0 18px}
.ev::before{content:"";position:absolute;inset-inline-start:-35px;top:6px;width:15px;height:15px;border-radius:50%;background:var(--k);border:3px solid var(--paper)}
.ev b{font-size:1.15rem;font-variant-numeric:tabular-nums;color:var(--k);margin-inline-end:10px}
.ev span.t{font-size:var(--chip);color:var(--k);border:1px solid var(--k);border-radius:var(--r-full);padding:1px 9px}
.ev p{margin:4px 0 0;line-height:1.95}
.ev.fut b{opacity:.6}.ev.fut::before{background:var(--paper);border-color:var(--k)}
.gap{margin:0 0 18px;font-size:var(--chip);color:var(--ink-3);padding:4px 0}
.cnt{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;max-width:820px}
.cnt div{border:1px solid var(--line);border-radius:var(--r-lg);padding:12px;background:var(--surface)}
.cnt b{display:block;font-size:.85rem;color:var(--ink-3)}
.dots{display:grid;grid-template-columns:repeat(10,1fr);gap:2px;margin:8px 0 6px;direction:ltr}
.dots i{aspect-ratio:1;border-radius:50%;background:var(--vz)}.dots i.on{background:#A8481A}
.cnt span{font-weight:800;font-size:1.2rem;font-variant-numeric:tabular-nums}
"""
CNT = [(1979, 1), (1996, 5), (2019, 56), (2024, 67), (2026, 70)]
def dots(n): return '<div class="dots">' + ''.join(f'<i class="{"on" if i < n else ""}"></i>' for i in range(70)) + '</div>'
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
body = f'''<h1>مرزی که جابه‌جا شد</h1>
<p class="lead">«این‌که خشونت نیست، همیشه همین بوده.» این جمله دربارهٔ برده‌داری، کتک‌زدن بچه، و تجاوز در ازدواج هم گفته می‌شد. این خط زمان نشان می‌دهد مرزِ «خشونتِ ناروا» کی و کجا جابه‌جا شد؛ و اینکه هنوز دارد جابه‌جا می‌شود.</p>
<div class="note w">این صفحه تاریخ <b>قانون</b> است، نه تاریخ رفتار. قانون همیشه اجرا نمی‌شود، و جرم‌شدنِ یک کار به معنای تمام‌شدنش نیست. ولی قانون نشان می‌دهد یک جامعه رسماً چه چیزی را دیگر «حقِ زننده» نمی‌داند.</div>
<section><h2>یک نمونه با عدد: کشورهایی که تنبیه بدنی کودک را همه‌جا ممنوع کرده‌اند</h2>
<p class="lead">هر نقطه یک کشور است. هفده سال اول تقریباً هیچ اتفاقی نیفتاد؛ بعد شتاب گرفت.</p>
<div class="cnt">{''.join(f'<div><b>{fa(y)}</b>{dots(n)}<span>{fa(n)}</span></div>' for y, n in CNT)}</div>
<p class="note g" style="margin-top:12px">منبع: <a href="https://endcorporalpunishment.org/countdown/" rel="noopener">End Corporal Punishment، شمارش جهانی</a> <span class="grade A">A</span> · عدد ۱۹۹۶ از گفتهٔ مدیر همان نهاد · عدد ۲۰۲۴ از <a href="https://rm.coe.int/enf-vae-2024-06-e-end-corporal-punishment/1680b1ca63" rel="noopener">گزارش شورای اروپا</a>. در جهان نزدیک دویست کشور هست؛ بیشترشان هنوز در این فهرست نیستند.</p></section>
<section><h2>خط زمان</h2>
<div class="flt" id="flt"><button class="pb" data-t="x" aria-pressed="true">همه</button>{''.join(f'<button class="pb" data-t="{k}" aria-pressed="false">{v[0]}</button>' for k, v in TH.items())}</div>
<div class="tl" id="tl"></div>
<p class="note g">درجه‌ها: <span class="grade A">A</span> سند رسمی یا نهاد شمارنده · <span class="grade B">B</span> رویداد حقوقی با چند منبع · <span class="grade C">C</span> تاریخ عمومی که برای این صفحه منبعش را باز نکرده‌ام. منابع: End Corporal Punishment · <a href="https://www.cambridge.org/core/product/192D7A6CCFDAADBBDA8FB028A1ABC2A6/core-reader" rel="noopener">پژوهش میان‌کشوری دربارهٔ جرم‌انگاری تجاوز در ازدواج (Cambridge)</a> · <a href="https://www.theweek.co.uk/98330/when-did-marital-rape-become-a-crime" rel="noopener">The Week دربارهٔ R v R</a> · <a href="../entries.html#violence-genealogy">مدخل: تبارشناسی خشونت</a> · <a href="../entries.html#coercive-control">مدخل: کنترل اجباری</a></p></section>
<section><h2>چه چیزی را ببینی</h2>
<p class="lead">۱. هر جابه‌جایی اول «نشدنی» بود، بعد «زیاده‌روی»، بعد بدیهی. فاصلهٔ اولین کشور تا کشور پنجم، برای تنبیه بدنی، هفده سال بود.</p>
<p class="lead">۲. مرز از بیرون به درون می‌آید: اول میدان و بازار (برده‌داری)، بعد دولت (شکنجه، آپارتاید)، بعد خانه (بچه، همسر)، و تازه‌ترین: خشونتی که اصلاً ضربه ندارد.</p>
<p class="lead">۳. خط تمام نشده است. آخرین سطر هنوز اتفاق نیفتاده.</p></section>
'''
js = r'''
const TH=%s,EV=%s;let cur="x";
function draw(){let last=null;$("tl").innerHTML=EV.filter(e=>cur==="x"||e[1]===cur).map(e=>{let g="";if(last!==null&&e[0]-last>=25)g='<div class="gap">'+fa(e[0]-last)+' سال بعد</div>';last=e[0];
return g+'<div class="ev'+(e[0]>2026?" fut":"")+'" style="--k:'+TH[e[1]][1]+'"><b>'+fa(e[0])+'</b><span class="t">'+TH[e[1]][0]+'</span> <span class="grade '+e[3]+'">'+e[3]+'</span><p>'+e[2]+'</p></div>'}).join("")}
$("flt").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;cur=b.dataset.t;[...$("flt").children].forEach(x=>x.setAttribute("aria-pressed",x===b));draw()});draw();
''' % (json.dumps(TH, ensure_ascii=False), json.dumps(EV, ensure_ascii=False))
page('violence-moving-line', 'مرزی که جابه‌جا شد: خط زمان قانون و خشونت', 'خط زمانِ اینکه برده‌داری، تنبیه بدنی کودک، تجاوز در ازدواج، کنترل اجباری و آپارتاید کی و کجا جرم شدند؛ و شمار کشورهایی که تنبیه بدنی را ممنوع کرده‌اند.', css, body, js)
