# -*- coding: utf-8 -*-
"""صفحهٔ «پروندهٔ خشونت»: python3 build/violence_page.py → psy/violence.html
ستون صفحه سیزده پرسش مریم است؛ هر عدد از مدخل‌ها و منابع core/sources.json می‌آید."""
import os, json, glob, html
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..')
E = html.escape
fa = lambda n: str(n).translate(str.maketrans('0123456789.', '۰۱۲۳۴۵۶۷۸۹٫'))
C = {}
for p in glob.glob(f'{R}/data/psy/concepts/*.json'):
    c = json.load(open(p, encoding='utf-8')); C[c['id'].split(':')[1]] = c
SRC = json.load(open(f'{R}/core/sources.json', encoding='utf-8'))
def S(needle):
    """پیوند منبع از روی تکه‌ای از ارجاع؛ اگر پیدا نشود خطا می‌دهد تا عدد بی‌منبع منتشر نشود."""
    for v in SRC.values():
        if needle in v['cite']: return v
    raise SystemExit('منبع پیدا نشد: ' + needle)
def cite(needle, label, grade):
    v = S(needle); u = v.get('url')
    a = f'<a href="{E(u)}" rel="noopener">{E(label)}</a>' if u else E(label)
    return f'<span class="src"><span class="grade {grade}">{grade}</span> {a}</span>'

# پنج ایستگاه نقشه و سیزده پرسش (به همان ترتیبی که پرسیده شد، ولی چیده در مسیر «از ریشه تا راه بیرون»)
STAGES = [
 ("ریشه", "از کجا آمده", "#7A5F22"),
 ("مرز", "چه چیزی خشونت است", "#5B4B8A"),
 ("سازوکار", "در ذهن و نقش چه می‌گذرد", "#0A6B60"),
 ("پخش", "میان آدم‌ها و گروه‌ها", "#A8481A"),
 ("پیامد و راه بیرون", "چه می‌کند، چه چیزی کمش می‌کند", "#2A6F7A"),
]
Q = [
 # (شماره، ایستگاه، پرسش، پاسخ کوتاه، مدخل‌ها)
 (1, 1, "چرا انتظار داریم آدم‌ها به هم خشونت نکنند؟",
  "چون روی یک معامله ایستاده‌ایم: هر کس زورش را زمین می‌گذارد تا امن باشد، و کسی هست که همه را بازخواست کند. این انتظار طبیعی نیست؛ ساخته شده و در تاریخ تازه است.",
  ["violence-why-expect-none"]),
 (2, 0, "خشونت بین موجودات از کجا شروع شد؟",
  "پیش از آدم بود. کشتن هم‌گونه در پستانداران کم است و در شاخهٔ نخستی‌ها بیشتر. آدم در خشونت لحظه‌ای آرام‌تر از خویشاوندانش است و در خشونت برنامه‌ریزی‌شده تواناتر.",
  ["violence-origins", "violence-history-decline"]),
 (3, 1, "چه چیزی را خشونت حساب می‌کنیم؟",
  "بستگی دارد خط را کجا بکشیم: فقط زور بدنی، یا هر به‌کاربردن عمدی قدرت که آسیب بزند، یا هر ساختاری که آدم‌ها را از توانشان پایین‌تر نگه دارد. هر تعریف برای کاری ساخته شده است.",
  ["violence-what-counts"]),
 (4, 4, "چه تأثیراتی دارد؟",
  "بر تن، روان، رابطه و نسل بعد. اثرش پله‌پله است: هرچه بیشتر و زودتر، سنگین‌تر. ولی سرنوشت نیست: بیشتر کودکان آزاردیده بزرگسال خشن نمی‌شوند.",
  ["violence-effects-victim", "violence-cycle"]),
 (5, 4, "بر خود فرد و اطرافیانش، در هر رابطه و هر نقش، چه تأثیری دارد؟",
  "کسی که می‌بیند، کسی که می‌کند و کسی که فقط تماشا می‌کند هر سه سهم می‌برند. کودکِ شاهد تقریباً به اندازهٔ کودکِ کتک‌خورده آسیب می‌بیند، و خشونت‌کردن هم برای بیشتر آدم‌ها زخم می‌گذارد.",
  ["violence-effects-victim", "violence-effects-perpetrator"]),
 (6, 2, "چطور آدم‌ها در یک نقش خیلی خشن‌اند و در نقش دیگر اصلاً نه؟",
  "چون خشونت بیشتر به نقش چسبیده است تا به آدم. نقش می‌گوید این‌جا چه کسی «از ما»ست، چه کاری «وظیفه» است و مسئولیت با کیست. ذهن می‌تواند دو نقش را در دو اتاق جدا نگه دارد.",
  ["violence-roles-switch", "moral-disengagement"]),
 (7, 2, "اخلاق با خشونت چه رابطه‌ای دارد؟",
  "هم ترمز است و هم سوخت. بیشتر کسانی که خشونت می‌کنند در همان لحظه باور دارند کار درست را می‌کنند. پس فقط «آگاه‌کردن» کافی نیست؛ باید خودِ آن «وظیفه» عوض شود.",
  ["virtuous-violence", "moral-disengagement"]),
 (8, 2, "آیا آدم‌هایی هستند که نتوانند خشونت کنند؟",
  "ناتوانیِ مطلق را پژوهشی نشان نداده است. ولی در هر نمونهٔ مستند، اقلیتی هست که وقتی همه می‌کنند و دستور هم هست، نمی‌کند؛ و خشونت رودررو برای بیشتر آدم‌ها سخت است.",
  ["violence-cannot"]),
 (9, 2, "آیا آدم‌هایی هستند که نفهمند دارند خشونت می‌کنند؟",
  "بله، و این حالتِ رایج است. آزارگر ماجرا را کوچک و تمام‌شده به یاد می‌آورد و آزاردیده بزرگ و ادامه‌دار. هنجار هم می‌تواند نام کار را عوض کند: تربیت، غیرت، شوخی.",
  ["violence-unseen-by-doer"]),
 (10, 2, "آیا آدم‌هایی هستند که ندانند مورد خشونت‌اند؟",
  "بله. در یک فراتحلیل، شش نفر از هر ده زنی که تجربه‌شان با تعریف تجاوز می‌خواند نام دیگری روی آن گذاشته بودند. نام‌ها را فرهنگ می‌دهد و نام‌گذاشتن هزینه دارد.",
  ["violence-unseen-by-victim"]),
 (11, 0, "دید تبارشناسی همهٔ این‌ها چطور است؟",
  "دو تبار هست. تبار زیستی می‌گوید خشونت از کدام شاخهٔ درخت جانداران آمده. تبارشناسی به معنای نیچه و فوکو می‌پرسد چه کسی، کی و برای چه مرز خشونت روا و ناروا را کشید؛ و نشان می‌دهد این مرز بارها جابه‌جا شده است.",
  ["violence-genealogy", "violence-origins"]),
 (12, 3, "برای جنسیت‌های مختلف در طول تاریخ چه خشونت‌های پنهان و پیدایی بوده؟ و چرا همه‌گیر شد؟",
  "مردان بیشتر بیرون خانه و به دست مردان دیگر کشته می‌شوند؛ زنان کمتر، ولی در خانه. خشونت پنهان در هر دو سو هنجاری است که یکی را خرج‌شدنی و دیگری را کنترل‌شدنی می‌خواهد. همه‌گیر می‌شود چون هیچ‌کس نمی‌خواهد اولین کسی باشد که نمی‌کند.",
  ["violence-gender-women", "violence-gender-men", "violence-gender-history", "violence-epidemic"]),
 (13, 3, "چطور آپارتاید خشونت‌آمیز ساخته می‌شود؟",
  "با کشتار شروع نمی‌شود؛ با دسته‌بندی شروع می‌شود. خط، قانون، جداسازی، محروم‌سازی، و زور برای نگه‌داشتن همه. هر پله پلهٔ بعد را عادی می‌کند و سکوت تماشاگران رضایت خوانده می‌شود.",
  ["violent-apartheid", "violence-prevention"]),
]
GROUPS = [
 ("ریشه و تبار", "#7A5F22", ["violence-origins", "violence-history-decline", "violence-genealogy"]),
 ("مرز: چه چیزی خشونت است", "#5B4B8A", ["violence-what-counts", "violence-why-expect-none"]),
 ("سازوکار: نقش، وجدان، اخلاق", "#0A6B60", ["violence-roles-switch", "moral-disengagement", "virtuous-violence", "violence-cannot", "violence-unseen-by-doer", "violence-unseen-by-victim"]),
 ("پخش: جنسیت، سرایت، آپارتاید", "#A8481A", ["violence-gender-women", "violence-gender-men", "violence-gender-history", "violence-epidemic", "violent-apartheid"]),
 ("پیامد و راه بیرون", "#2A6F7A", ["violence-effects-victim", "violence-effects-perpetrator", "violence-cycle", "violence-prevention"]),
]
TOOLS = [
 ("violence-line", "خط را کجا می‌کشی؟", "چهارده موقعیت. اول خودت بگو کدام خشونت است؛ بعد ببین سه تعریف (باریک، سازمان جهانی بهداشت، گالتونگ) هر کدام را کجا می‌گذارند."),
 ("violence-switches", "هشت کلید وجدان", "بیست جملهٔ آشنا. هر جمله کدام کلید را می‌زند؟ بازی‌ای برای شنیدن این کلیدها در حرف خودمان."),
 ("violence-spread", "سرایت: چرا همه‌گیر می‌شود", "یک محلهٔ چهارصدنفره. آستانهٔ آدم‌ها، شمار آغازگرها و شمار «زنجیره‌بُرها» را تکان بده و ببین کی همه را می‌گیرد و کی خاموش می‌شود."),
 ("violence-stairs", "پلکان آپارتاید", "ده پله از دسته‌بندی تا انکار، با نمونهٔ آفریقای جنوبی و اینکه در هر پله چه چیزی می‌تواند جلویش را بگیرد."),
]

# ---------- واحدهای تصویر ----------
def dots(n_on, n=100, cls='a', label=''):
    return (f'<div class="dots" role="img" aria-label="{E(label)}">' +
            ''.join(f'<i class="{cls if i < n_on else "z"}"></i>' for i in range(n)) + '</div>')
def bar(label, val, mx, txt, cls='a', note=''):
    w = max(1.2, 100 * val / mx)
    return (f'<div class="bar"><span class="bl">{E(label)}</span><span class="bt"><i class="{cls}" style="width:{w:.1f}%"></i></span>'
            f'<span class="bv">{E(txt)}</span>{f"<em>{E(note)}</em>" if note else ""}</div>')
def fig(title, insight, body, sources, note='', id=''):
    return (f'<figure class="fig" id="{id}"><figcaption><b>{E(title)}</b><p>{insight}</p></figcaption>{body}'
            f'<div class="srcs">{"".join(sources)}</div>{f"<p class=cap>{note}</p>" if note else ""}</figure>')

F = []
# ۱. چه کسی کشته می‌شود و کجا
F.append(fig("چه کسی کشته می‌شود، و به دست چه کسی",
 "از هر صد نفری که در جهان عمداً کشته می‌شوند <b>۸۱ نفر مردند</b>. ولی جای خطر فرق دارد: از هر صد <b>زنِ</b> کشته‌شده <b>۶۰ نفر</b> به دست شریک زندگی یا خویشاوند کشته شده‌اند؛ برای مردان <b>۱۱ نفر</b>.",
 '<div class="trio"><div><h4>صد قربانی قتل عمد (۲۰۲۱)</h4>' + ('<div class="dots" role="img" aria-label="۸۱ مرد و ۱۹ زن از هر صد قربانی">' + ''.join(f'<i class="{"m" if i < 81 else "w"}"></i>' for i in range(100)) + '</div>') +
 '<p class="key"><i class="m"></i>مرد ۸۱ <i class="w"></i>زن ۱۹</p></div>'
 '<div><h4>صد زنِ کشته‌شده (۲۰۲۴)</h4>' + dots(60, 100, 'h', '۶۰ نفر از هر صد زن کشته‌شده به دست شریک یا خویشاوند') +
 '<p class="key"><i class="h"></i>به دست شریک یا خویشاوند ۶۰ <i class="z"></i>دیگران ۴۰</p></div>'
 '<div><h4>صد مردِ کشته‌شده (۲۰۲۴)</h4>' + dots(11, 100, 'h', '۱۱ نفر از هر صد مرد کشته‌شده به دست شریک یا خویشاوند') +
 '<p class="key"><i class="h"></i>به دست شریک یا خویشاوند ۱۱ <i class="z"></i>دیگران ۸۹</p></div></div>',
 [cite("Global Study on Homicide 2023", "دفتر مقابله با مواد مخدر و جرم سازمان ملل، بررسی جهانی قتل ۲۰۲۳", "A"),
  cite("Femicides in 2024", "همان دفتر و نهاد زنان ملل متحد، زن‌کشی در ۲۰۲۴", "A")],
 "دو منبع و دو سال جدا هستند: سهم دو جنس از دادهٔ ۲۰۲۱ و سهم خانه از دادهٔ ۲۰۲۴. در بسیاری از کشورها رابطهٔ قاتل و قربانی ثبت نمی‌شود، پس عددهای «خانه» برآوردند.", 'f-who'))
# ۲. تبار
F.append(fig("سهم کشته‌شدن به دست هم‌گونه، در درخت تبار",
 "از روی جای آدم در درخت پستانداران، انتظار می‌رود حدود <b>۲ درصد</b> مرگ‌ها به دست آدم دیگر باشد؛ نزدیک هفت برابر میانگین پستانداران. این نقطهٔ شروع است، نه سرنوشت.",
 '<div class="bars">' + bar("میانگین پستانداران", 0.3, 2.4, "۰٫۳٪", 'z2') + bar("نیای مشترک نخستی‌ها", 2.3, 2.4, "۲٫۳٪", 'a') +
 bar("آدم، پیش‌بینی از روی تبار", 2.0, 2.4, "۲٪", 'h') + '</div>'
 '<div class="pair"><div><b>۱۵۲</b><span>کشتن ثبت‌شده در شامپانزه‌ها (۱۸ گروه، پنج دهه)</span></div><div><b>۱</b><span>مورد مشکوک در بونوبوها (۴ گروه)</span></div></div>',
 [cite("phylogenetic roots of human lethal violence", "گومز و همکاران ۲۰۱۶، Nature", "A"), cite("Lethal aggression in Pan", "ویلسون و همکاران ۲۰۱۴، Nature", "A")],
 "عدد ۲٫۳ درصد برای نیای نخستی‌ها از گزارش‌های خبری همان مقاله است. از ۱۵۲ مورد شامپانزه، ۵۸ مورد دیده شده و بقیه استنباط یا گمان است.", 'f-root'))
# ۳. تاریخ
F.append(fig("قتل در اروپا، از سده‌های میانه تا سدهٔ بیستم",
 "نرخ قتل در اروپای غربی در حدود هفت سده نزدیک <b>بیست برابر</b> کم شد. بیشترِ این کاهش، کم‌شدن دعوای مرد با مرد در کوچه و میدان بود.",
 '<div class="bars">' + bar("سده‌های میانه", 20, 20, "حدود ۲۰", 'h') + bar("حوالی ۱۶۰۰", 10, 20, "حدود ۱۰", 'a') +
 bar("سدهٔ بیستم", 1, 20, "حدود ۱", 'z2') + bar("جهان، ۲۰۲۱", 5.8, 20, "۵٫۸", 'm', "برای مقایسه؛ روش و جغرافیا فرق دارد") + '</div><p class="unit">قتل در هر صد هزار نفر در سال</p>',
 [cite("Long-Term Historical Trends in Violent Crime", "آیزنر ۲۰۰۳", "B"), cite("Global Study on Homicide 2023", "بررسی جهانی قتل ۲۰۲۳", "A"), cite("Hard numbers?", "نقد: شورهوف و همکاران ۲۰۲۱", "B")],
 "⚑ محل بحث: داده‌های پیش از دوران آمار پراکنده‌اند و برآورد جمعیت آن دوره‌ها نامطمئن است. عددها گردشده و تقریبی‌اند.", 'f-hist'))
# ۴. دیده‌نشدن
F.append(fig("خشونتی که نام ندارد",
 "دو عدد کنار هم: از هر صد زنی که تجربه‌شان با تعریف تجاوز می‌خواند، <b>۶۰ نفر</b> نام دیگری روی آن گذاشته بودند. و از هر صد نفر در جهان، <b>۲۵ نفر</b> کتک‌زدن زن به دست شوهر را موجه می‌دانند.",
 '<div class="trio two"><div><h4>نامش را تجاوز نگذاشتند</h4>' + dots(60, 100, 'h', '۶۰ از ۱۰۰') +
 '<p class="key"><i class="h"></i>۶۰٫۴٪ (بازهٔ اطمینان ۵۵ تا ۶۵٫۶)</p></div>'
 '<div><h4>کتک‌زدن زن را موجه می‌دانند</h4>' + dots(25, 100, 'a', '۲۵ از ۱۰۰') + '<p class="key"><i class="a"></i>۲۵٪ مردم جهان</p></div></div>',
 [cite("Unacknowledged Rape", "ویلسون و میلر ۲۰۱۶، فراتحلیل ۲۸ پژوهش", "A"), cite("Gender Social Norms Index", "برنامهٔ توسعهٔ ملل متحد ۲۰۲۳", "A")],
 "فراتحلیل بیشتر روی دانشجویان آمریکایی است و ناهمگونی میان پژوهش‌ها زیاد بود. عدد دوم از پیمایش ارزش‌های جهانی است.", 'f-unseen'))
# ۵. یک‌سوم
F.append(fig("یک‌سوم، و بیست‌وچند سال بی‌تغییر",
 "نزدیک <b>۸۴۰ میلیون</b> زن در طول زندگی خشونت بدنی یا جنسی از شریک زندگی یا خشونت جنسی از دیگران دیده‌اند. این سهم از سال ۲۰۰۰ تقریباً تکان نخورده است.",
 '<div class="trio two"><div><h4>در طول زندگی</h4>' + dots(32, 100, 'h', 'حدود ۳۲ از ۱۰۰') + '<p class="key"><i class="h"></i>نزدیک یک نفر از هر سه نفر</p></div>'
 '<div><h4>فقط در دوازده ماه گذشته، از شریک زندگی</h4>' + dots(11, 100, 'a', '۱۱ از ۱۰۰') + '<p class="key"><i class="a"></i>۱۱٪ یعنی ۳۱۶ میلیون زن</p></div></div>',
 [cite("Violence against women prevalence estimates, 2023", "سازمان جهانی بهداشت ۲۰۲۵، ۱۶۸ کشور", "A")],
 "این پیمایش‌ها فقط زنان را می‌شمارند؛ برای مردان برآورد جهانی هم‌سنگ وجود ندارد. خود گزارش می‌گوید شیوع واقعی به احتمال زیاد بالاتر است.", 'f-third'))
# ۶. آن‌ها که نکردند
F.append(fig("یوزفوف، ۱۳ ژوئیهٔ ۱۹۴۲: حدود پانصد مرد معمولی",
 "فرمانده گفت هر کس نمی‌تواند کنار برود. <b>حدود دوازده نفر</b> همان اول کنار رفتند. به برآورد تاریخ‌نگار، در طول روز <b>۱۰ تا ۲۰ درصد</b> از تیراندازی کنار کشیدند. هیچ‌کس برای این کار مجازات نشد.",
 '<div class="dots d500" role="img" aria-label="۵۰۰ نقطه: ۱۲ نفر کنار رفتند، تا ۱۰۰ نفر کنار کشیدند">' +
 ''.join(f'<i class="{"h" if i < 12 else ("r" if i < 50 else ("r2" if i < 100 else "z"))}"></i>' for i in range(500)) + '</div>'
 '<p class="key"><i class="h"></i>همان اول کنار رفتند (حدود ۱۲) <i class="r"></i>در طول روز کنار کشیدند: کران پایین ۱۰٪ <i class="r2"></i>کران بالا ۲۰٪ <i class="z"></i>ماندند</p>',
 [cite("Ordinary Men", "براونینگ ۱۹۹۲، «آدم‌های معمولی»", "B")],
 "از روی بازجویی‌های دههٔ ۱۹۶۰ و ۱۹۷۰؛ شمار دقیق دانسته نیست و بازه همان بازهٔ خود نویسنده است.", 'f-jozefow'))
# ۷. چرخه
F.append(fig("چرخه هست، سرنوشت نیست",
 "از هر صد کودکی که آزار یا غفلتشان در دادگاه ثابت شده بود، بیست‌وپنج سال بعد <b>۱۸ نفر</b> برای جرم خشن بازداشت شده بودند. <b>۸۲ نفر نه.</b>",
 dots(18, 100, 'h', '۱۸ از ۱۰۰') + '<p class="key"><i class="h"></i>بازداشت برای جرم خشن ۱۸ <i class="z"></i>بدون چنین بازداشتی ۸۲</p>',
 [cite('Update on the \\"Cycle of Violence\\"'.replace('\\', ''), "ویدوم و مکسفیلد ۲۰۰۱؛ ۹۰۸ کودک و ۶۶۷ همسان", "A")],
 "خطر نسبت به گروه همسان حدود ۳۰ درصد بیشتر بود. «بازداشت» همهٔ خشونت را نمی‌گیرد، و نمونه از یک منطقهٔ آمریکا در دههٔ ۱۹۶۰ است.", 'f-cycle'))
# ۸. سرایت و بریدن زنجیره
F.append(fig("سرایت، و بریدن زنجیره",
 "در شبکه‌ای از ۱۳۸ هزار نفر در شیکاگو، <b>۶۳ درصد</b> تیرخوردن‌ها را می‌شد با سرایت از آدم به آدم توضیح داد. و جایی که زنجیره را دیدند و بریدند، خشونت کم شد.",
 '<div class="bars">' + bar("تیرخوردن‌های قابل‌توضیح با سرایت", 63.1, 100, "۶۳٪", 'h') +
 bar("کاردیف: کاهش بستری به علت خشونت", 42, 100, "۴۲٪ کمتر", 'ok', "نسبت به ۱۴ شهر مشابه") +
 bar("گلاسگو: کاهش بستری با زخم چاقو", 62, 100, "۶۲٪ کمتر", 'ok', "در ده سال؛ سهم برنامه روشن نیست") + '</div>',
 [cite("Modeling Contagion Through Social Networks", "گرین، هورل و پاپاکریستوس ۲۰۱۷", "A"), cite("Effectiveness of anonymised information sharing", "فلورنس و همکاران ۲۰۱۱، BMJ", "A"), cite("Tackling knife crime in Scotland", "دولت اسکاتلند ۲۰۱۸", "C")],
 "سه عدد سه چیز متفاوت را می‌سنجند و کنار هم فقط برای دیدن «سرایت ← بریدن» آمده‌اند. شبکهٔ شیکاگو فقط بازداشت‌شدگان را دارد.", 'f-spread'))
# ۹. بی‌خشونت
F.append(fig("کدام بیشتر به نتیجه رسید؟",
 "از ۱۹۰۰ تا ۲۰۰۶ کارزارهای بی‌خشونت <b>دو برابر</b> کارزارهای مسلحانه به هدف رسیدند.",
 '<div class="bars">' + bar("کارزار بی‌خشونت", 53, 100, "۵۳٪", 'ok') + bar("کارزار مسلحانه", 26, 100, "۲۶٪", 'h') + '</div>',
 [cite("Why Civil Resistance Works", "استفان و چنووث ۲۰۰۸", "A"), cite("Future of Nonviolent Resistance", "چنووث ۲۰۲۰", "B")],
 "⚑ خود چنووث نشان داده کامیابی کارزارهای بی‌خشونت از دههٔ ۲۰۱۰ پایین آمده است.", 'f-nonviolent'))

# ---------- چهار خانه (تصویر مفهوم) ----------
QUAD = ('<div class="quad" role="table" aria-label="چهار خانه: پیدا و پنهان، برای زنان و مردان">'
 '<div class="qh"></div><div class="qh">علیه زنان</div><div class="qh">علیه مردان</div>'
 '<div class="qs">پیدا</div>'
 '<div class="qc w"><b>در خانه</b>کتک، تجاوز، زن‌کشی، ناقص‌سازی، ازدواج در کودکی، شکار جادوگر</div>'
 '<div class="qc m"><b>در میدان</b>جنگ، سربازگیری، دعوای آبرو، قتل در خیابان</div>'
 '<div class="qs">پنهان</div>'
 '<div class="qc w dash"><b>قانون و عرف</b>نداشتن حق مالکیت، طلاق، درس و رفت‌وآمد؛ دختری که کمتر خوراک و درمان می‌گیرد</div>'
 '<div class="qc m dash"><b>هنجار سختی</b>«مرد گریه نمی‌کند»، «مرد جواب می‌دهد»؛ تنِ خرج‌شدنی و ترسِ ممنوع</div>'
 '<div class="ql">یک قفل: آبروی مرد در زورش است و آبروی او در تن زن. هر دو نیمه با هم می‌چرخند، و هر کس در هیچ‌کدام از دو قالب نگنجد مجازات می‌شود.</div></div>')

# ---------- کنار هم ----------
def card(slug):
    c = C[slug]; n = len(c.get('points', []))
    return (f'<a class="ent" href="entries.html#{slug}"><b>{E(c["title"]["fa"])}</b><span>{E(c["summary"]["fa"][:140])}…</span>'
            f'<i>{fa(n)} گزاره · {fa(len(c.get("sources", [])))} منبع</i></a>')
slugs = [s for g in GROUPS for s in g[2]]
allsrc = sorted({x for s in slugs for x in C[s].get('sources', [])})
tiers = {}
for s in allsrc: tiers[SRC[s]['tier']] = tiers.get(SRC[s]['tier'], 0) + 1
gaps = [(C[s]['title']['fa'], s, pt['text']['fa']) for s in slugs for pt in C[s]['points'] if set(pt.get('flags', [])) & {'contested', 'unreplicated', 'dated'}]

map_html = ''.join(
 f'<div class="st" style="--k:{k}"><div class="sth"><b>{E(n)}</b><span>{E(d)}</span></div>' +
 ''.join(f'<a href="#q{q[0]}"><i>{fa(q[0])}</i>{E(q[2])}</a>' for q in Q if q[1] == i) + '</div>'
 for i, (n, d, k) in enumerate(STAGES))
q_html = ''.join(
 f'<article class="q" id="q{n}" style="--k:{STAGES[st][2]}"><div class="qn">{fa(n)}</div><div><h3>{E(qq)}</h3><p>{E(ans)}</p>'
 f'<div class="ql2">{"".join(f"""<a href="entries.html#{s}">{E(C[s]["title"]["fa"])}</a>""" for s in es)}</div></div></article>'
 for n, st, qq, ans, es in Q)
groups_html = ''.join(f'<section class="grp" style="--k:{k}"><header><h2>{E(n)}</h2></header><div class="ents">{"".join(card(s) for s in ss)}</div></section>' for n, k, ss in GROUPS)
tools_html = ''.join(f'<a class="tool" href="tools/{a}.html"><b>{E(b)}</b><span>{E(d)}</span></a>' for a, b, d in TOOLS)
gaps_html = ''.join(f'<li><a href="entries.html#{s}">{E(t)}</a>: {E(x[:170])}…</li>' for t, s, x in gaps)
plan = open(f'{R}/data/psy/dossiers/violence.plan.html', encoding='utf-8').read()

CSS = """
:root{--c:var(--fam-psy);--vm:#4E6E8E;--vw:#A8481A;--vh:#9F1239;--va:#B45309;--vz:color-mix(in srgb,var(--ink-3) 22%,var(--paper));--vr:#2F6B4F}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--vm:#8FB0D0;--vw:#E08A5E;--vh:#F0708C;--va:#E8A04A;--vr:#6FBF95}}
:root[data-theme=dark]{--vm:#8FB0D0;--vw:#E08A5E;--vh:#F0708C;--va:#E8A04A;--vr:#6FBF95}
h1{font-size:clamp(2rem,5vw,3.1rem);margin:var(--s8) 0 var(--s3);line-height:1.3;text-wrap:balance}
p.lead{color:var(--ink-2);max-width:46em;line-height:2.05;margin:0 0 var(--s4);font-size:1.07rem}
.note{padding:var(--s4);border-radius:var(--r-md);font-size:var(--small);line-height:1.95;color:var(--ink-2);max-width:60em;margin:0 0 var(--s3)}
.note.w{background:color-mix(in srgb,var(--warn) 10%,var(--paper));border:1px solid color-mix(in srgb,var(--warn) 45%,var(--line))}
.note.r{background:color-mix(in srgb,var(--err) 8%,var(--paper));border:1px solid color-mix(in srgb,var(--err) 38%,var(--line))}
.note.g{background:var(--surface);border:1px solid var(--line)}
.stats{display:flex;gap:26px;flex-wrap:wrap;margin:var(--s5) 0;padding:var(--s4) 0;border-block:1px solid var(--line)}
.stats div b{display:block;font-size:1.8rem;color:var(--c);line-height:1.1;font-variant-numeric:tabular-nums}
.stats div span{font-size:var(--small);color:var(--ink-3)}
h2.sec{font-size:var(--h2);margin:var(--s10) 0 var(--s2);line-height:1.5}
p.sub{color:var(--ink-2);max-width:48em;line-height:1.95;margin:0 0 var(--s5)}
/* نقشهٔ کل */
.map{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:var(--s4) 0 var(--s3);position:relative}
.st{border:1px solid var(--line);border-top:5px solid var(--k);border-radius:var(--r-lg);background:var(--surface);padding:12px;display:flex;flex-direction:column;gap:8px;position:relative}
.st:not(:last-child)::after{content:"←";position:absolute;inset-inline-end:-12px;top:14px;color:var(--ink-3);font-size:14px;z-index:2;background:var(--paper);border-radius:50%;width:14px;text-align:center}
.sth b{display:block;color:var(--k);font-size:1.05rem}.sth span{font-size:var(--chip);color:var(--ink-3)}
.st a{display:flex;gap:8px;align-items:flex-start;font-size:.86rem;line-height:1.7;color:var(--ink);text-decoration:none;padding:7px 8px;border-radius:var(--r-md);background:color-mix(in srgb,var(--k) 8%,var(--paper))}
.st a:hover{background:color-mix(in srgb,var(--k) 18%,var(--paper))}
.st a i{font-style:normal;flex:none;width:22px;height:22px;border-radius:50%;background:var(--k);color:#fff;font-size:.72rem;display:grid;place-items:center;font-weight:700;margin-top:2px}
@media (max-width:900px){.map{grid-template-columns:1fr}.st:not(:last-child)::after{content:"↓";inset-inline-end:auto;inset-inline-start:50%;top:auto;bottom:-13px}}
/* پرسش‌ها */
.qs13{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,430px),1fr));gap:14px}
.q{display:flex;gap:14px;padding:18px;border:1px solid var(--line);border-inline-start:5px solid var(--k);border-radius:var(--r-lg);background:var(--surface);scroll-margin-top:80px}
.q:target{outline:3px solid color-mix(in srgb,var(--k) 55%,transparent)}
.qn{flex:none;width:38px;height:38px;border-radius:50%;background:var(--k);color:#fff;display:grid;place-items:center;font-weight:800;font-size:1.05rem}
.q h3{margin:2px 0 8px;font-size:1.06rem;line-height:1.7}.q p{margin:0 0 10px;line-height:2;color:var(--ink-2);font-size:.97rem}
.ql2{display:flex;gap:6px;flex-wrap:wrap}.ql2 a{font-size:var(--chip);padding:3px 10px;border-radius:var(--r-full);border:1px solid var(--line-strong);text-decoration:none;color:var(--k)}
.ql2 a:hover{background:color-mix(in srgb,var(--k) 10%,var(--paper))}
/* تصویرها */
.figs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,520px),1fr));gap:16px}
.fig{margin:0;padding:20px;border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);min-width:0}
.fig figcaption b{display:block;font-size:var(--chip);letter-spacing:.02em;color:var(--ink-3);font-weight:650;margin-bottom:6px}
.fig figcaption p{margin:0 0 16px;font-size:1.08rem;line-height:1.95;color:var(--ink);text-wrap:pretty}
.fig figcaption p b{display:inline;font-size:inherit;color:var(--vh);font-weight:800;letter-spacing:0}
.dots{display:grid;grid-template-columns:repeat(20,1fr);gap:3px;max-width:340px}
.dots i{aspect-ratio:1;border-radius:50%;background:var(--vz)}
.dots.d500{grid-template-columns:repeat(50,1fr);gap:2px;max-width:none}
i.m{background:var(--vm)!important}i.w{background:var(--vw)!important}i.h{background:var(--vh)!important}i.a{background:var(--va)!important}
i.r{background:var(--vr)!important}i.r2{background:color-mix(in srgb,var(--vr) 45%,var(--vz))!important}i.ok{background:var(--vr)!important}i.z2{background:var(--ink-3)!important}
.dots .z{background:var(--vz)}
.trio{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.trio.two{grid-template-columns:repeat(2,1fr)}
.trio h4{margin:0 0 8px;font-size:.86rem;font-weight:650;color:var(--ink-2);line-height:1.6;min-height:2.8em}
@media (max-width:560px){.trio,.trio.two{grid-template-columns:1fr}.trio h4{min-height:0}}
.key{font-size:var(--chip);color:var(--ink-2);margin:8px 0 0;line-height:2}
.key i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-inline:8px 4px;vertical-align:-1px}
.key i:first-child{margin-inline-start:0}.key i.z{background:var(--vz)}
.bars{display:grid;gap:12px}
.bar{display:grid;grid-template-columns:1fr auto;gap:2px 10px;align-items:center}
.bar .bl{font-size:.9rem;color:var(--ink-2);grid-column:1/-1}
.bar .bt{height:18px;border-radius:9px;background:var(--vz);overflow:hidden;display:block}
.bar .bt i{display:block;height:100%;border-radius:9px;background:var(--va)}
.bar .bv{font-weight:800;font-variant-numeric:tabular-nums;font-size:.95rem;min-width:4.2em;text-align:end}
.bar em{grid-column:1/-1;font-style:normal;font-size:var(--chip);color:var(--ink-3)}
.unit{font-size:var(--chip);color:var(--ink-3);margin:8px 0 0}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
.pair div{border:1px solid var(--line);border-radius:var(--r-md);padding:12px}
.pair b{display:block;font-size:2rem;line-height:1.1;color:var(--vh);font-variant-numeric:tabular-nums}.pair span{font-size:var(--chip);color:var(--ink-2);line-height:1.8}
.srcs{display:flex;gap:6px 14px;flex-wrap:wrap;margin-top:16px;padding-top:12px;border-top:1px dashed var(--line-strong)}
.src{font-size:var(--chip);color:var(--ink-2)}.src a{color:var(--ink-2)}
.cap{font-size:var(--chip);color:var(--ink-3);line-height:1.9;margin:8px 0 0}
/* چهار خانه */
.quad{display:grid;grid-template-columns:auto 1fr 1fr;gap:8px;max-width:900px}
.qh{font-weight:700;text-align:center;font-size:.92rem;color:var(--ink-2);padding:4px}
.qs{writing-mode:vertical-rl;text-align:center;font-weight:700;font-size:.92rem;color:var(--ink-2);padding:4px}
.qc{border:2px solid var(--kq);border-radius:var(--r-lg);padding:14px;font-size:.92rem;line-height:1.95;color:var(--ink-2);background:color-mix(in srgb,var(--kq) 7%,var(--paper))}
.qc b{display:block;color:var(--kq);margin-bottom:4px}.qc.w{--kq:var(--vw)}.qc.m{--kq:var(--vm)}.qc.dash{border-style:dashed}
.ql{grid-column:2/-1;text-align:center;font-size:.92rem;line-height:1.95;padding:12px;border-radius:var(--r-lg);background:var(--surface);border:1px solid var(--line-strong)}
/* مدخل‌ها و ابزارها */
section.grp{padding-block:var(--s6);border-top:1px solid var(--line)}
section.grp h2{font-size:var(--h3);margin:0 0 var(--s4);color:var(--k)}
.ents{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:14px}
.ent{display:block;padding:16px 18px;border:1px solid var(--line);border-inline-start:4px solid var(--k);border-radius:var(--r-lg);background:var(--surface);text-decoration:none;color:inherit}
.ent:hover{border-color:var(--k)}.ent b{display:block;font-size:1.02rem;margin-bottom:7px;line-height:1.6}
.ent span{display:block;font-size:var(--small);color:var(--ink-2);line-height:1.9;margin-bottom:8px}.ent i{font-style:normal;font-size:var(--chip);color:var(--ink-3)}
.tools{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,270px),1fr));gap:14px}
.tool{display:block;padding:18px 20px;border:1px solid var(--line);border-radius:var(--r-lg);background:color-mix(in srgb,var(--fam-psy) 7%,var(--paper));text-decoration:none;color:inherit}
.tool:hover{border-color:var(--c)}.tool b{display:block;font-size:1.08rem;color:var(--c);margin-bottom:7px}.tool span{font-size:var(--small);color:var(--ink-2);line-height:1.9}
.tool.st2{background:color-mix(in srgb,var(--story) 9%,var(--paper))}.tool.st2 b{color:var(--story)}
ul.gaps{margin:0;padding-inline-start:1.1em;display:grid;gap:9px;max-width:56em}ul.gaps li{font-size:var(--small);color:var(--ink-2);line-height:1.9}
details.plan{border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);padding:14px 18px;max-width:60em}
details.plan summary{cursor:pointer;font-weight:700}details.plan h4{margin:16px 0 6px}details.plan li,details.plan p{font-size:var(--small);line-height:1.95;color:var(--ink-2)}
"""

out = f"""<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>پروندهٔ خشونت | ویکی روان‌شناسی | دانش‌سرا</title>
<meta name="description" content="سیزده پرسش دربارهٔ خشونت، از ریشهٔ تکاملی تا آپارتاید: {fa(len(slugs))} مدخل، نُه تصویر داده، چهار ابزار و بازی، و داستان‌های واقعی. هر عدد با منبع و درجه.">
<link rel="stylesheet" href="../core/design/tokens.css">
<style>{CSS}</style>
</head>
<body>
<main class="wrap">
<h1>پروندهٔ خشونت</h1>
<p class="lead">این پرونده از سیزده پرسش شروع شد: چرا انتظار داریم آدم‌ها به هم خشونت نکنند، خشونت از کجا آمد، چه چیزی خشونت است، با آدم‌ها چه می‌کند، چطور یک آدم در یک نقش خشن است و در نقش دیگر نه، و چطور به همه‌گیری و آپارتاید می‌رسد.</p>
<h2 class="sec" id="map" style="margin-top:var(--s5)">نقشهٔ کل: از ریشه تا راه بیرون</h2>
<p class="sub">سیزده پرسش در پنج ایستگاه. از راست بخوانید: خشونت از کجا آمد، مرزش کجاست، در ذهن و نقش چه می‌گذرد، چطور پخش می‌شود، و چه می‌کند و چه چیزی کمش می‌کند. روی هر پرسش بزنید تا به پاسخ کوتاهش بروید.</p>
<div class="map">{map_html}</div>

<div class="note w"><b>سه قاعدهٔ این پرونده.</b><br>
۱. <b>توضیح‌دادن توجیه‌کردن نیست.</b> فهمیدن اینکه چرا کسی خشونت می‌کند، او را بی‌مسئولیت نمی‌کند.<br>
۲. <b>هر عدد با منبع و درجه.</b> A یعنی پژوهش داوری‌شده یا آمار رسمی، B رویداد تاریخی یا برآورد با چند منبع، C گزارش تأییدنشده. هر جا محل بحث است، نشان ⚑ دارد.<br>
۳. <b>هیچ ابزاری کسی را برچسب نمی‌زند.</b> ابزارها برای دیدنِ سازوکارند، نه برای تشخیص آدم‌ها. چیزی هم ذخیره یا فرستاده نمی‌شود.</div>
<div class="note r"><b>اگر همین حالا در خطر هستید</b> یا کسی کنار شما در خطر است، خواندن این صفحه کار اول نیست: با شمارهٔ اضطراری جایی که هستید تماس بگیرید و خود را به آدمی مطمئن برسانید. بخش‌هایی از این پرونده دربارهٔ کشتار، تجاوز و آزار کودک است؛ هر جا سنگین شد، ببندید.</div>
<div class="stats">
 <div><b>{fa(len(Q))}</b><span>پرسش</span></div>
 <div><b>{fa(len(slugs))}</b><span>مدخل</span></div>
 <div><b>{fa(len(allsrc))}</b><span>منبع</span></div>
 <div><b>{fa(len(F))}</b><span>تصویر داده</span></div>
 <div><b>{fa(len(TOOLS))}</b><span>ابزار و بازی</span></div>
 <div><b>{fa(tiers.get(1, 0) + tiers.get(2, 0))}</b><span>منبع داوری‌شده یا رسمی</span></div>
</div>

<h2 class="sec" id="answers">سیزده پرسش، سیزده پاسخ کوتاه</h2>
<p class="sub">هر پاسخ دو سه جمله است و زیرش مدخل‌هایی که همان را با منبع باز می‌کنند.</p>
<div class="qs13">{q_html}</div>

<h2 class="sec" id="data">عددها</h2>
<p class="sub">هر تصویر یک جمله می‌گوید و زیرش منبع، درجه و محدودیتش آمده. هر نقطه در نقطه‌چین‌ها یک نفر از صد نفر است.</p>
<div class="figs">{''.join(F)}</div>

<h2 class="sec" id="quad">چهار خانه: پیدا و پنهان، برای زنان و مردان</h2>
<p class="sub">این یک نمودار عددی نیست؛ نقشهٔ یک سازوکار است. خط‌چین یعنی خشونتی که ضربه ندارد و برای همین کمتر شمرده شده است.</p>
{QUAD}
<p class="cap" style="max-width:900px">الگو از گالتونگ (۱۹۶۹)، بوردیو (۱۹۹۸)، نیسبت و کوهن (۱۹۹۶) و مدخل «جنسیت و خشونت در طول تاریخ» همین پرونده. برای کسانی که در قالب دو جنس نمی‌گنجند داده بسیار کم است؛ همان اندک در مدخل آمده.</p>
</main>

<main class="wrap" style="padding-top:0">
<section class="grp" style="--k:var(--fam-psy)">
<header><h2>ابزارها و بازی‌ها</h2></header>
<div class="tools">{tools_html}<a class="tool st2" href="stories/violence.html"><b>داستان‌های واقعی</b><span>نُه روایت مستند، از یوزفوف تا گلاسگو، هر کدام با «چرا این داستان؟» و منبع.</span></a></div>
</section>
{groups_html}
<section class="grp" style="--k:#8a6d3b">
<header><h2>جاهای نازک</h2></header>
<p class="sub">گزاره‌هایی که در خود مدخل‌ها نشان «محل بحث»، «تکرارنشده» یا «قدیمی» دارند.</p>
<ul class="gaps">{gaps_html}</ul>
<p class="note g" style="margin-top:var(--s4)"><b>چیزهایی که این‌جا نیست.</b> عددهای ایران در این صفحه نیامده‌اند؛ جایشان لایهٔ ایران است و باید با سال، روش و درجه بیایند. برای خشونت علیه مردان و علیه کسانی که در قالب دو جنس نمی‌گنجند برآورد جهانیِ هم‌سنگ وجود ندارد. داستانی از شبکه‌های اجتماعی هم نگذاشتم، چون نتوانستم هیچ‌کدام را راستی‌آزمایی کنم.</p>
</section>
<section class="grp" style="--k:var(--ink-3)">
<header><h2>این پرونده چطور ساخته شد</h2></header>
<details class="plan"><summary>برنامه، نقد برنامه و بازبینی پس از هر مرحله</summary>{plan}</details>
<p class="lead" style="font-size:1rem;margin-top:var(--s4)">متن‌ها خلاصه‌ای آموزشی از منابع نام‌برده‌اند، نه مشاوره، درمان یا نظر حقوقی. پیوندهای این پرونده به ویکی جامعه، فلسفه و تبار در خود مدخل‌ها آمده است.</p>
</section>
</main>
</body>
</html>
"""
open(f'{R}/psy/violence.html', 'w', encoding='utf-8').write(out)
print('violence.html', len(slugs), 'entries', len(allsrc), 'sources', len(F), 'figures', len(gaps), 'flagged')
