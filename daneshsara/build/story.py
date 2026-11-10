# -*- coding: utf-8 -*-
"""«داستان پروژه» — what happened, where it stands, what is still missing.
Numbers come from the data, so the page cannot go stale: python3 build/story.py"""
import os, json, glob, html, re
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.chdir(R)
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
reg = json.load(open('core/registry.json', encoding='utf-8'))['stats']
books = len(json.load(open('data/library/books.json', encoding='utf-8')))
iran = [json.load(open(p, encoding='utf-8')) for p in glob.glob('iran/*.json')]
iran_viz = sum(1 for n in iran if (n.get('viz') or {}).get('kind') not in (None, 'none'))
iran_dom = {n['domain'] for n in iran}
pages = len([p for p in glob.glob('**/*.html', recursive=True)
             if not p.startswith('build/') and 'http-equiv="refresh"' not in open(p, encoding='utf-8', errors='ignore').read()])
tier = {}
for s in json.load(open('core/sources.json', encoding='utf-8')).values() if isinstance(json.load(open('core/sources.json', encoding='utf-8')), dict) else []:
    t = s.get('tier')
    if t: tier[t] = tier.get(t, 0) + 1

S = lambda k: fa(reg.get(k, 0))
SK = json.load(open('data/sakht/sakht.json', encoding='utf-8'))
LAYERS = [
 ('۱', 'علم', 'var(--fam-psy)',
  'چهار ویکی به هم پیوسته: روان‌شناسی، جامعه، فلسفه، تبار و ژنتیک. هر مفهوم خانهٔ خودش را دارد و منبعش کنارش است. '
  'ویکی پنجمی هم هست که کارش فقط نشان دادن پیوند میان این علم‌هاست.',
  [(S('concepts'), 'مفهوم'), (S('concepts_with_sources'), 'مفهوم با منبع'), (S('sources'), 'منبع'),
   (S('people'), 'چهره'), (S('cross_wiki_links'), 'پیوند میان ویکی‌ها'), (S('bridges'), 'پل میان‌رشته‌ای')],
  [('ویکی روان‌شناسی', '../psy/'), ('ویکی جامعه', '../soc/'), ('ویکی فلسفه', '../phil/'),
   ('ویکی تبار و ژنتیک', '../tabar/'), ('ویکی ارتباط رشته‌ها', '../miyan/')]),
 ('۲', 'ایران', 'var(--primary)',
  'همان مفهوم‌ها، این بار در ایران: عدد و آمار واقعی با سال و روش و ردهٔ کیفیت، ریشه‌یابی، و شرح وضع موجود. '
  'جایی که ایران چیزی را اندازه نگرفته، همین نبودن نوشته می‌شود.',
  [(fa(len(iran)), 'یادداشت'), (fa(iran_viz), 'نمودار از دادهٔ واقعی'), (fa(len(iran_dom)), 'حوزه')],
  [('ویکی ایران', '../iran/')]),
 ('۳', 'سیمرغ', '#b7791f',
  'همان پروژهٔ «پَرِ سیمرغ»: میز مافیای ایران، نقش‌ها، قدم هر قشر و نقشهٔ مشکل‌ها. در سایت جداگانه ساخته شده و از اینجا به آن راه هست؛ '
  'پیوند مدخل به مدخل میان دو سایت هنوز ساخته نشده.',
  [('۴۷', 'نقش اجتماعی'), ('۱۸', 'کارت قدمِ تو'), ('۲۴', 'مشکل روی نقشه')],
  [('درگاه سیمرغ', '../simorgh/'), ('سایت پَرِ سیمرغ', 'https://maryamjaberi.github.io/simorgh/')]),
 ('۴', 'ساخت ایران', '#2f6b3a',
  'روز بعد چه باید آماده باشد: نهادهای ضروری کشورداری، درس‌های دوران گذار در کشورهای دیگر، دفتر ریسک و زیرساخت دیجیتال. '
  'تازه شروع شده و بر پایهٔ گزارش‌های رسمی و پژوهش‌های گذار است، نه دادهٔ خود ایران.',
  [(fa(len(SK['organs'])), 'کارکرد ضروری'), (fa(len(SK['transition'])), 'درس گذار'), (fa(len(SK['risks'])), 'ریسک'), (fa(len(SK['sources'])), 'منبع')],
  [('ساخت ایران', '../sakht/')]),
]
GAPS = [
 ('ویکی زبان‌شناسی هنوز ساخته نشده', 'در صفحهٔ اول به‌صورت «به‌زودی» نشان داده می‌شود و هیچ مدخلی ندارد.'),
 ('لایهٔ ایران برای فلسفه یادداشتی ندارد', f'از {fa(len(iran))} یادداشت، هیچ‌کدام از حوزهٔ فلسفه نیست.'),
 ('بیشتر یادداشت‌های ایران سری زمانی ندارند', f'فقط {fa(iran_viz)} یادداشت نمودار دارد؛ بقیه یک عدد برای یک سال‌اند یا عدد قابل‌رسمی ندارند.'),
 ('«ریشه‌یابی» و «وضع موجود» هنوز بخش جدا نیستند', 'فعلاً در متن یافته و نقد آمده‌اند، نه به‌صورت ساختار.'),
 ('سیمرغ و دانش‌سرا هنوز مدخل به مدخل وصل نیستند', '«پَرِ سیمرغ» در سایت جداگانه ساخته شده؛ نقش‌ها و مشکل‌هایش هنوز به مفهوم‌ها و یادداشت‌های اینجا پیوند ندارند.'),
 ('نسخهٔ انگلیسی و هلندی ناقص است', 'صفحهٔ اول و اطلس‌های تازه فقط فارسی‌اند.'),
 ('نقشه‌های دوران‌های بسیار دور در اطلس زمان دقیق نیستند', 'برای کامبرین و دونین و رودینیا هنوز دادهٔ واقعی زمین‌شناسی نداریم و شکل‌ها تقریبی‌اند؛ همین‌جا هم نوشته شده.'),
 ('روی گوشی کمتر آزموده شده', 'بررسی‌ها با مرورگر خودکار روی عرض گوشی انجام شده، ولی لمس واقعی روی دستگاه آزمایش نشده.'),
]
HOW = [
 ('هر عدد سال و روش و ردهٔ کیفیت دارد', 'ردهٔ ۱ یعنی فراتحلیل یا یافتهٔ تکرارشده، ۴ یعنی سرنخ یا جدل. هیچ عددی بدون منبع وارد نمی‌شود.'),
 ('یافتهٔ تکرارنشده برچسب می‌خورد', 'اگر مطالعه‌ای تکرار نشده یا محل مناقشه است، همان‌جا نوشته می‌شود، نه در پانویس.'),
 ('نبودن داده هم یک یافته است', 'اگر ایران چیزی را اندازه نگرفته، به‌جای پر کردن جای خالی با تقریب، همین نبودن نوشته می‌شود.'),
 ('نمودار دروغ نمی‌گوید', 'جایی که روش اندازه‌گیری عوض شده، خط به دو تکه شکسته می‌شود تا تغییر روش به‌جای تغییر واقعیت خوانده نشود.'),
 ('هر صفحه مسیرش را نشان می‌دهد', 'از خرده‌نان بالای هر صفحه معلوم است کجاییم و از کجا به کجا می‌شود رفت.'),
]
P = lambda t: E(t)
page = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>داستان پروژه | دانش‌سرا</title>
<meta name="description" content="دانش‌سرا چیست، از کجا شروع شد، الان کجاست و چه چیزی هنوز در آن نیست — با عددهای واقعی و فهرست صریح کمبودها.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>
h1{{font-size:var(--h1);margin:var(--s8) 0 var(--s4);line-height:var(--lh-tight);max-width:18ch}}
p.lead{{color:var(--ink-2);max-width:47em;line-height:2;margin:0 0 var(--s6);font-size:1.05rem}}
section{{padding-block:var(--s6);border-top:1px solid var(--line)}}
h2{{font-size:var(--h3);margin:0 0 var(--s2)}}
p.sub{{color:var(--ink-3);font-size:var(--small);line-height:1.9;margin:0 0 var(--s4);max-width:46em}}
.lay{{display:grid;gap:var(--s4);margin-bottom:var(--s4);padding:var(--s4) var(--s5);border:1px solid var(--line);border-radius:var(--r-lg);background:var(--paper);border-inline-start:4px solid var(--c)}}
.lay h3{{margin:0;font-size:var(--h4)}}.lay h3 b{{color:var(--c)}}
.lay p{{margin:0;color:var(--ink-2);line-height:1.95;max-width:46em}}
.nums{{display:flex;flex-wrap:wrap;gap:var(--s5)}}
.nums div{{display:grid}}.nums b{{font-size:1.5rem;color:var(--ink);line-height:1.2}}
.nums span{{font-size:var(--chip);color:var(--ink-3)}}
.go{{display:flex;flex-wrap:wrap;gap:8px}}
.go a{{font-size:var(--small);padding:4px 13px;border:1px solid var(--line-strong);border-radius:var(--r-full);color:var(--ink-2);text-decoration:none}}
.go a:hover{{border-color:var(--c);color:var(--ink)}}
dl{{margin:0;display:grid;gap:var(--s3);max-width:52em}}
dt{{font-weight:650;color:var(--ink)}}
dd{{margin:3px 0 0;color:var(--ink-2);font-size:var(--small);line-height:1.9}}
.gap dt::before{{content:"○ ";color:#b7791f}}
.how dt::before{{content:"✓ ";color:#1f7a4d}}
footer.f{{border-top:1px solid var(--line);padding-block:var(--s5);font-size:var(--small);color:var(--ink-3)}}
footer.f a{{color:var(--ink-2);margin-inline-end:var(--s4)}}
</style>
</head>
<body>
<main class="wrap">
<h1>چه شد که این‌طور شد، و حالا چه کنیم</h1>
<p class="lead">دانش‌سرا برای یک پرسش ساخته شده: اگر بخواهیم بفهمیم ایران چرا به اینجا رسیده و از اینجا به کجا می‌شود رفت، به چه چیزی نیاز داریم؟ جواب این پروژه چهار لایه است. اول باید بدانیم آدم و جامعه چطور کار می‌کنند و این دانش را از کجا می‌دانیم. بعد همان را در ایران بسنجیم، با عدد واقعی نه با حدس. تنها بعد از آن می‌شود از راه‌حل حرف زد، و در آخر از اینکه روز بعد چه نهادها و ابزارهایی باید آماده باشد.</p>

<section>
<h2>چهار لایه</h2>
<p class="sub">هر لایه روی لایهٔ زیرش می‌ایستد. لایهٔ بالاتر بدون لایهٔ پایین‌تر حرف بی‌پشتوانه است.</p>
{''.join(f"""<div class="lay" style="--c:{c}"><h3><b>لایهٔ {i}</b> · {P(n)}</h3><p>{P(d)}</p>
<div class="nums">{''.join(f'<div><b>{v}</b><span>{P(l)}</span></div>' for v,l in nums)}</div>
<div class="go">{''.join(f'<a href="{u}">{P(t)} ←</a>' for t,u in links)}</div></div>""" for i,n,c,d,nums,links in LAYERS)}
</section>

<section>
<h2>الان کجاییم</h2>
<p class="sub">این عددها از خود داده‌های سایت خوانده می‌شوند، نه دستی نوشته شده‌اند؛ پس کهنه نمی‌شوند.</p>
<div class="nums">
<div><b>{fa(pages)}</b><span>صفحه</span></div>
<div><b>{S('concepts')}</b><span>مفهوم</span></div>
<div><b>{S('sources')}</b><span>منبع</span></div>
<div><b>{S('people')}</b><span>چهره</span></div>
<div><b>{S('cross_wiki_links')}</b><span>پیوند میان ویکی‌ها</span></div>
<div><b>{S('fields')}</b><span>رشته در اطلس</span></div>
<div><b>{fa(books)}</b><span>کتاب در کتابخانه</span></div>
<div><b>{fa(len(iran))}</b><span>یادداشت ایران</span></div>
</div>
</section>

<section class="how">
<h2>قاعده‌هایی که رعایت می‌شوند</h2>
<p class="sub">این‌ها تصمیم‌های سخت پروژه‌اند؛ رعایتشان کار را کندتر می‌کند ولی نتیجه را قابل اتکا نگه می‌دارد.</p>
<dl>{''.join(f'<dt>{P(t)}</dt><dd>{P(d)}</dd>' for t,d in HOW)}</dl>
</section>

<section class="gap">
<h2>چه چیزی هنوز اینجا نیست</h2>
<p class="sub">این فهرست عمداً صریح است. اگر جایی خالی است، بهتر است خوانندهٔ آن را بداند تا اینکه با چیزی تقریبی پر شود.</p>
<dl>{''.join(f'<dt>{P(t)}</dt><dd>{P(d)}</dd>' for t,d in GAPS)}</dl>
</section>

<section>
<h2>قدم بعدی</h2>
<p class="sub">کارِ پیشِ رو به ترتیب اهمیت: کامل کردن لایهٔ ایران (ریشه‌یابی و وضع موجود برای هر یادداشت، و یادداشت برای حوزه‌هایی که خالی‌اند)، بعد ساختن لایهٔ سیمرغ روی همان، و در کنارشان افزودن منابع تازه به لایهٔ علم با همان قاعدهٔ اعتبارسنجی.</p>
<div class="go"><a href="sitemap.html">نقشهٔ سایت و ساختار پیشنهادی ←</a><a href="../core/contribute.html">راهنمای مشارکت ←</a><a href="../core/sources.html">همهٔ منابع ←</a></div>
</section>
</main>
<footer class="f"><div class="wrap"><a href="../">دانش‌سرا</a><a href="sitemap.html">نقشهٔ سایت</a><a href="../core/contribute.html">مشارکت</a></div></footer>
</body>
</html>
'''
open('atlas/story.html', 'w', encoding='utf-8').write(page)
print('atlas/story.html written —', pages, 'pages,', len(GAPS), 'gaps listed')
