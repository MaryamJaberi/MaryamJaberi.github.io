# -*- coding: utf-8 -*-
"""داستان‌های واقعی «پروندهٔ خشونت»: python3 build/violence_stories.py → psy/stories/violence.html و violence.json"""
import os, json, html
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..'); E = html.escape
TYPES = {'news': 'خبر و تاریخ', 'study': 'پژوهش و آزمایش', 'book': 'کتاب و خاطره'}
ST = [
 dict(id='jozefow', claims=['violence-cannot', 'violence-roles-switch'], type='book', grade='B',
  title="صبحی در یوزفوف", where="یوزفوف، لهستانِ اشغال‌شده · ۱۳ ژوئیهٔ ۱۹۴۲",
  text="گردان ۱۰۱ پلیس ذخیره حدود پانصد مرد داشت، بیشترشان میانسال، کارگر و کاسب اهل هامبورگ؛ پیرتر از آن که به جبهه بروند. سپیده‌دم فرمانده‌شان، سرگرد تراپ، با حالی آشفته گفت دستور رسیده یهودیان روستا را بکشند، و بعد چیزی گفت که در چنین دستورهایی شنیده نمی‌شد: هر کس از مردان مسن‌تر که خود را برای این کار توانا نمی‌بیند می‌تواند کنار برود. حدود دوازده نفر جلو آمدند. بقیه ماندند و تا شب نزدیک هزار و پانصد نفر را کشتند. در طول روز شماری دیگر خود را کنار کشیدند یا گم‌وگور کردند؛ تاریخ‌نگار سهم همهٔ آن‌ها را ده تا بیست درصد برآورد می‌کند. کسی برای کنار رفتن مجازات نشد.",
  why="دو گزاره را با هم نشان می‌دهد. اول: خشونت به نقش و گروه چسبیده است؛ آن مردان نه گزینش‌شده بودند، نه متعصب‌تر از دیگران، و بهای نکردن هم فقط جداافتادن از هم‌قطاران بود. دوم: حتی آن‌جا اقلیتی نکرد.",
  note="⚑ منبع بازجویی‌های دادگاهی دو سه دهه بعد است. دانیل گلدهاگن همین پرونده‌ها را جور دیگری خواند و نقش یهودستیزی را بسیار پررنگ‌تر دانست.",
  sources=[["Facing History & Ourselves: Reserve Police Battalion 101", "https://www.facinghistory.org/resource-library/reserve-police-battalion-101"], ["Browning (1992), Ordinary Men — archive.org", "https://archive.org/details/ordinarymenreser0000brow"]], viz='f-jozefow'),
 dict(id='milgram', claims=['violence-roles-switch'], type='study', grade='A',
  title="چهل مرد و یک دستگاه شوک", where="نیوهِیون، آمریکا · ۱۹۶۱ تا ۱۹۶۲",
  text="استنلی میلگرام به داوطلبان گفت در پژوهشی دربارهٔ اثر تنبیه بر یادگیری شرکت می‌کنند. کارشان این بود که با هر پاسخ غلطِ «شاگرد» اتاق کناری، شوک قوی‌تری بدهند. شوکی در کار نبود و شاگرد بازیگر بود، ولی داوطلبان نمی‌دانستند. در نسخهٔ پایه، بیست‌وشش نفر از چهل نفر تا آخرین کلید رفتند. نیم قرن بعد پژوهشگرانی که بایگانی را دوباره خواندند چیز دیگری دیدند: آدم‌ها وقتی ادامه می‌دادند که آزمایشگر از «نیاز پژوهش» حرف می‌زد، و درست وقتی دستور خشک می‌شنیدند که چاره‌ای ندارند، بیشترشان سر باز می‌زدند.",
  why="نشان می‌دهد موقعیت و نقش می‌تواند آدم معمولی را به آسیب‌زدن برساند؛ و بازخوانی تازه نشان می‌دهد سازوکارش «اطاعت کور» نیست، یکی‌شدن با هدفی است که خوب دیده می‌شود.",
  note="⚑ خوانش «پیروی درگیرانه» هم منتقد دارد: تحلیلی از مصاحبه‌های پس از آزمایش می‌گوید بسیاری از شرکت‌کنندگان شک داشتند کسی واقعاً آسیب ببیند.",
  sources=[["Association for Psychological Science: Not Obedience But Followership", "https://www.psychologicalscience.org/publications/observer/obsonline/not-obedience-but-followership.html"], ["British Psychological Society, Research Digest", "https://bps.org.uk/research-digest/new-analysis-suggests-most-milgram-participants-realised-obedience-experiments-were"]]),
 dict(id='sharpeville', claims=['violent-apartheid'], type='news', grade='B',
  title="دفترچه‌ای که باید همیشه در جیب می‌بود", where="شارپویل، آفریقای جنوبی · ۲۱ مارس ۱۹۶۰",
  text="هر آفریقاییِ سیاه باید دفترچهٔ عبور همراه می‌داشت و هر پلیسی هر لحظه می‌توانست آن را بخواهد؛ نداشتنش یعنی بازداشت. آن دوشنبه چند هزار نفر بی‌دفترچه جلوی کلانتری شارپویل جمع شدند تا خود را برای بازداشت معرفی کنند: اگر همه بی‌دفترچه باشند، زندان جا ندارد. پلیس آتش گشود. آمار رسمی پلیس ۶۹ کشته و ۱۸۰ زخمی بود. دولت به‌جای عقب‌نشینی حالت فوق‌العاده اعلام کرد و سازمان‌های مخالف را ممنوع کرد. سی‌وشش سال بعد، قانون اساسی تازهٔ کشور در همان شهر امضا شد.",
  why="پلکان را در یک روز نشان می‌دهد: خشونتِ پیدا (گلوله) برای نگه‌داشتن خشونتِ اداری (دفترچه) لازم شد، و پس از آن پله‌های بعدی (ممنوعیت، حالت فوق‌العاده) آمد.",
  note="⚑ شمار کشتگان محل بحث است: عدد ۶۹ از پروندهٔ پلیس است و پژوهش‌های تازه‌تر آن را بیشتر می‌دانند.",
  sources=[["Encyclopaedia Britannica: Sharpeville massacre", "https://www.britannica.com/event/Sharpeville-massacre"], ["Canadian Museum for Human Rights: The Sharpeville Massacre", "https://humanrights.ca/node/501"], ["African Studies Centre Leiden", "https://ascleiden.nl/content/library-weekly/sharpeville-massacre"]]),
 dict(id='chicago', claims=['violence-epidemic'], type='study', grade='A',
  title="صد و بیست و پنج روز", where="شیکاگو · ۲۰۰۶ تا ۲۰۱۴",
  text="سه پژوهشگر شبکه‌ای ساختند از ۱۳۸ هزار نفر که در هشت سال در شیکاگو بازداشت شده بودند؛ هر دو نفری که با هم برای یک جرم بازداشت شده بودند به هم وصل شدند. بعد دیدند تیرخوردن در این شبکه چطور جابه‌جا می‌شود. از یازده هزار و صد و بیست و سه مورد، شصت‌وسه درصد را می‌شد با سرایت از یک آدم به آدمِ کناری توضیح داد. فاصلهٔ میانگین میان تیرخوردن یک نفر و تیرخوردن کسی که از او «گرفته بود» صد و بیست و پنج روز بود.",
  why="نشان می‌دهد خشونت تصادفی پخش نمی‌شود و فقط به محله و فقر هم نمی‌چسبد: از راه رابطه‌ها می‌رود، مثل بیماری‌ای که با تماس منتقل شود. پس می‌شود دانست نفر بعد کیست و پیش از آن رسید.",
  note="شبکه فقط بازداشت‌شدگان را دارد، بیشترشان مردان جوان سیاه‌پوست؛ این خودش بازتاب این است که پلیس چه کسی را بازداشت می‌کند.",
  sources=[["Yale ISPS: Modeling Contagion Through Social Networks", "https://isps.yale.edu/research/publications/isps17-02"], ["PBS NewsHour / STAT", "https://www.pbs.org/newshour/nation/gun-violence-infectious-disease-research"]], viz='f-spread'),
 dict(id='glasgow', claims=['violence-epidemic', 'violence-prevention'], type='news', grade='B',
  title="جراحی که از بخیه‌زدن خسته شد", where="گلاسگو · از ۲۰۰۵",
  text="کریستین گودال جراح فک و صورت بود و سالی صدها صورتِ بریده را می‌دوخت. یک بار باید به جوانی می‌گفت جای زخم روی صورتش می‌ماند و نگران واکنشش بود؛ جوان اهمیتی نداد. عصر که دوستانش به دیدنش آمدند جراح فهمید چرا: همه‌شان یکی داشتند. در همان سال‌ها گلاسگو را «پایتخت قتل اروپا» می‌نامیدند. در ۲۰۰۵ یک تحلیلگر پلیس، کارین مک‌کلاسکی، نوشت که پلیس‌گریِ معمول خشونت را کم نکرده است، و واحدی ساخته شد که با خشونت مثل بیماری واگیر رفتار می‌کرد. ده سال بعد شمار قتل در اسکاتلند نصف شده بود.",
  why="زخمی که همه دارند دیگر زخم نیست، نشانِ عضویت است: هنجار. و وقتی هنجار و زنجیرهٔ تلافی هدف گرفته شد، نه فقط مجرم، عدد پایین آمد.",
  note="⚑ قتل در همان دوره در جاهای دیگر بریتانیا هم کم شد؛ سهم دقیق این واحد را نمی‌شود جدا کرد.",
  sources=[["World Economic Forum / Mosaic (S. Shackle)", "https://www.weforum.org/stories/2018/07/violent-crime-is-like-infectious-disease-and-we-know-how-to-stop-it-spreading/"], ["UK Civil Service blog: Tackling knife crime in Scotland", "https://civilservice.blog.gov.uk/2018/05/24/tackling-knife-crime-in-scotland-10-years-on/"]], viz='f-spread'),
 dict(id='cardiff', claims=['violence-prevention'], type='study', grade='A',
  title="آنچه پلیس نمی‌دانست و پذیرش بیمارستان می‌دانست", where="کاردیف، ولز · دههٔ ۲۰۰۰",
  text="جاناتان شپرد، جراح، متوجه شد بخش بزرگی از کسانی که با زخم خشونت به اورژانس می‌آیند هیچ‌وقت به پلیس گزارش نمی‌دهند. پس از کارمندان پذیرش خواست از هر زخمی سه چیز بپرسند: کجا بود، کی بود، با چه. نام حذف می‌شد و فهرست، هر چند هفته به پلیس و شهرداری می‌رسید. با همین فهرست جای گشت‌ها عوض شد، و خیابانی پر از میخانه آخر هفته‌ها پیاده‌راه شد. ارزیابی نشان داد بستری به علت خشونت نسبت به چهارده شهر مشابه چهل‌ودو درصد کمتر شده است.",
  why="نشان می‌دهد بخشی از خشونت دیده نمی‌شود چون جایی شمرده می‌شود که کسی از آن خبر ندارد؛ و دیدنِ الگو، بدون شناختن یا مجازات یک نفر هم، می‌تواند کمش کند.",
  sources=[["Florence et al. (2011), BMJ — PubMed Central", "https://pmc.ncbi.nlm.nih.gov/articles/PMC3116927"], ["Cardiff University: Reducing violent crime", "https://www.cardiff.ac.uk/dentistry/research/our-global-impact/reducing-violent-crime2"]], viz='f-spread'),
 dict(id='unnamed', claims=['violence-unseen-by-victim'], type='study', grade='A',
  title="«رابطهٔ بد»", where="بیست‌وهشت پژوهش، بیشتر در آمریکا · تا ۲۰۱۴",
  text="مری کاس در دههٔ ۱۹۸۰ به چیز عجیبی برخورد: زنانی که در پرسش‌نامه به پرسش‌های رفتاری جواب «بله» می‌دادند (کسی به‌زور یا وقتی توان مخالفت نداشتی با تو رابطه داشته؟) ولی به پرسش «آیا به تو تجاوز شده؟» جواب «نه». لورا ویلسون و کاترین میلر سی سال بعد همهٔ پژوهش‌های این‌چنینی را جمع کردند: نزدیک شش هزار زن در بیست‌وهشت پژوهش. شش نفر از هر ده نفر تجربهٔ خود را تجاوز نمی‌نامیدند؛ نام‌هایی که می‌دادند چیزهایی بود مثل رابطهٔ بد یا سوءتفاهم.",
  why="مستقیم‌ترین پاسخ به این پرسش که آیا کسی می‌تواند نداند مورد خشونت است. و یک درس روش: اگر برچسب بپرسی عدد یک چیز است، اگر رفتار بپرسی چیز دیگر.",
  note="این یافته اجازه نمی‌دهد به کسی بگوییم «تو قربانی‌ای و نمی‌دانی». نام‌گذاشتن حق خود آدم است.",
  sources=[["Wilson & Miller (2016), Trauma, Violence, & Abuse", "https://doi.org/10.1177/1524838015576391"], ["University of Mary Washington expert note", "https://expertfile.com/spotlight/6076/women-often-dont-label-their-sexual-assaults-as-rape-our-experts-can-explain"]], viz='f-unseen'),
 dict(id='home', claims=['violence-gender-women', 'violence-gender-men'], type='news', grade='A',
  title="هر ده دقیقه", where="جهان · ۲۰۲۴",
  text="گزارش سالانهٔ دو نهاد سازمان ملل در ۲۵ نوامبر ۲۰۲۵ منتشر شد. در سال ۲۰۲۴ هشتادوسه هزار زن و دختر عمداً کشته شده بودند و پنجاه هزار نفرشان به دست شریک زندگی یا خویشاوند: پدر، برادر، عمو، مادر. یعنی روزی صد و سی‌وهفت نفر، هر ده دقیقه یک نفر. همان گزارش عدد دیگری هم دارد که کمتر نقل می‌شود: حدود هشتاد درصد همهٔ کشته‌شدگانِ قتل در جهان مردند، و از آن‌ها فقط یازده درصد به دست نزدیکان کشته شده‌اند.",
  why="دو نیمهٔ یک تصویر را کنار هم می‌گذارد: مردان بیرون خانه و به دست مردان دیگر کشته می‌شوند، زنان در خانه. هر کدام را جدا نقل کنی، نیمی از ماجرا گم می‌شود.",
  note="خود گزارش می‌گوید عدد واقعی به احتمال زیاد بیشتر است، چون بسیاری از کشورها رابطهٔ قاتل و قربانی را ثبت نمی‌کنند.",
  sources=[["UNODC press release, 25 November 2025", "https://www.unodc.org/unodc/en/press/releases/2025/November/137-women-and-girls-killed-every-day-by-intimate-partners-or-family-members-in-2024.html"], ["UN Women", "https://www.unwomen.org/en/news-stories/press-release/2025/11/every-day-137-women-and-girls-are-killed-by-intimate-partners-or-family-members"]], viz='f-who'),
 dict(id='gender-apartheid', claims=['violent-apartheid', 'violence-genealogy'], type='news', grade='B',
  title="واژه‌ای که هنوز در قانون نیست", where="نیویورک و کابل · ۲۰۲۳ تا ۲۰۲۶",
  text="تعریف حقوقی آپارتاید فقط از «گروه نژادی» حرف می‌زند. گروهی از زنان مدافع حقوق بشر در افغانستان گفتند آنچه بر آن‌ها می‌رود (کنارگذاشتن نظام‌مند و قانونی از درس، کار و رفت‌وآمد) همان ساختار را دارد و نامی در قانون ندارد. هم‌زمان سازمان ملل داشت نخستین پیمان جهانی جنایت علیه بشریت را آماده می‌کرد. کارزار خواست «آپارتاید جنسیتی» در آن بیاید. در ژوئن ۲۰۲۶ نخستین دورِ پیشنهادهای رسمی اصلاح متن منتشر شد و چند کشور از چهار منطقهٔ جهان آن را پیشنهاد کردند؛ تا اوت ۲۰۲۶ چهارده کشور علناً پشتیبانی کرده‌اند. مذاکرهٔ متن از ژانویهٔ ۲۰۲۸ آغاز می‌شود.",
  why="تبارشناسی را در زمان حال نشان می‌دهد: مرز «خشونتِ نام‌دار» همین حالا دارد جابه‌جا می‌شود، و جابه‌جاکنندگانش کسانی‌اند که کلمه‌ای برای تجربهٔ خود نداشتند.",
  note="⚑ دربارهٔ اینکه جرم تازه لازم است یا «آزار جنسیتی» که هم‌اکنون جرم است کفایت می‌کند، میان حقوق‌دانان بحث هست.",
  sources=[["Human Rights Watch, 6 August 2026", "https://www.hrw.org/news/2026/08/06/one-step-closer-to-recognizing-gender-apartheid-as-an-international-crime"], ["Opinio Juris, 10 March 2026", "https://opiniojuris.org/2026/03/10/taking-stock-of-the-proposal-to-codify-gender-apartheid-in-the-crimes-against-humanity-convention/"]]),
]
C = {s: json.load(open(f'{R}/data/psy/concepts/{s}.json', encoding='utf-8')) for st in ST for s in st['claims']}
json.dump(ST, open(f'{R}/psy/stories/violence.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
ICON = '<svg viewBox="0 0 64 64" role="img" aria-label="نشان داستان و تصویرسازی داده" width="56" height="56"><path d="M32 16 C24 11 14 11 6 13 V51 C14 49 24 49 32 54 Z" fill="var(--story-soft)" stroke="var(--story)" stroke-width="2.2" stroke-linejoin="round"/><path d="M32 16 C40 11 50 11 58 13 V51 C50 49 40 49 32 54 Z" fill="var(--fam-soc-soft)" stroke="var(--fam-soc)" stroke-width="2.2" stroke-linejoin="round"/><path d="M38 19 h14 a3 3 0 0 1 3 3 v7 a3 3 0 0 1 -3 3 h-8 l-4 4 v-4 h-2 a3 3 0 0 1 -3 -3 v-7 a3 3 0 0 1 3 -3z" fill="var(--story)"/><circle cx="41.5" cy="25.5" r="1.3" fill="#fff"/><circle cx="45.5" cy="25.5" r="1.3" fill="#fff"/><circle cx="49.5" cy="25.5" r="1.3" fill="#fff"/><rect x="11" y="36" width="4" height="8" rx="1" fill="var(--fam-soc)"/><rect x="17.5" y="30" width="4" height="14" rx="1" fill="var(--fam-soc)"/><rect x="24" y="22" width="4" height="22" rx="1" fill="var(--story)"/></svg>'
def card(s):
    cl = ''.join(f'<a href="../entries.html#{c}">{E(C[c]["title"]["fa"])}</a>' for c in s['claims'])
    srcs = ' · '.join(f'<a href="{E(u)}" rel="noopener">{E(t)}</a>' for t, u in s['sources'])
    viz = f'<a class="vz" href="../violence.html#{s["viz"]}">تصویر دادهٔ این داستان ←</a>' if s.get('viz') else ''
    return (f'<article class="sty" data-t="{s["type"]}" id="{s["id"]}"><div class="mt"><span class="grade {s["grade"]}">{s["grade"]}</span><span>{TYPES[s["type"]]}</span><span>{E(s["where"])}</span></div>'
            f'<h2>{E(s["title"])}</h2><p>{E(s["text"])}</p><div class="why"><b>چرا این داستان؟</b>{E(s["why"])}</div>'
            + (f'<p class="nt">{E(s["note"])}</p>' if s.get('note') else '') +
            f'<div class="cl"><span>گزاره‌هایی که نشان می‌دهد:</span>{cl}</div>{viz}<p class="sr">منبع: {srcs}</p></article>')
out = f"""<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>داستان‌های واقعی پروندهٔ خشونت | ویکی روان‌شناسی | دانش‌سرا</title>
<meta name="description" content="نُه روایت مستند دربارهٔ خشونت، از یوزفوف و شارپویل تا گلاسگو و کاردیف؛ هر کدام با «چرا این داستان؟»، درجهٔ اعتبار و منبع.">
<link rel="stylesheet" href="../../core/design/tokens.css">
<style>
h1{{font-size:var(--h1);margin:var(--s4) 0 var(--s3);line-height:var(--lh-tight)}}
.hd{{display:flex;gap:16px;align-items:center;margin-top:var(--s8)}}
p.lead{{color:var(--ink-2);max-width:46em;line-height:2;margin:0 0 var(--s4);font-size:1.05rem}}
.note{{padding:var(--s3) var(--s4);border-radius:var(--r-md);font-size:var(--small);line-height:1.9;color:var(--ink-2);max-width:60em;margin:0 0 var(--s4);background:var(--surface);border:1px solid var(--line)}}
.flt{{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 var(--s5)}}
.flt button{{font:inherit;font-size:var(--small);padding:7px 16px;border-radius:var(--r-full);border:1px solid var(--line-strong);background:var(--paper);color:var(--ink-2);cursor:pointer}}
.flt button[aria-pressed=true]{{background:var(--story);border-color:var(--story);color:#fff;font-weight:650}}
.list{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,460px),1fr));gap:16px}}
.sty{{border:1px solid var(--line);border-top:4px solid var(--story);border-radius:var(--r-lg);background:var(--surface);padding:20px;scroll-margin-top:80px}}
.sty.off{{display:none}}
.mt{{display:flex;gap:10px;flex-wrap:wrap;align-items:center;font-size:var(--chip);color:var(--ink-3)}}
.sty h2{{font-size:1.3rem;margin:10px 0 8px;line-height:1.6}}.sty p{{line-height:2.05;margin:0 0 12px}}
.why{{background:var(--story-soft);border-radius:var(--r-md);padding:12px 14px;line-height:1.95;font-size:var(--small);margin-bottom:12px}}
.why b{{display:block;color:var(--story);margin-bottom:2px}}
.nt{{font-size:var(--small);color:var(--ink-2)}}
.cl{{display:flex;gap:6px;flex-wrap:wrap;align-items:center;font-size:var(--chip);color:var(--ink-3);margin-bottom:10px}}
.cl a{{padding:3px 10px;border-radius:var(--r-full);border:1px solid var(--line-strong);text-decoration:none}}
.vz{{display:inline-block;font-size:var(--small);margin-bottom:10px}}
.sr{{font-size:var(--chip);color:var(--ink-3);line-height:1.9;margin:0!important;padding-top:10px;border-top:1px dashed var(--line-strong)}}
.back{{display:inline-block;margin:var(--s5) 0;font-size:var(--small)}}
</style>
</head>
<body>
<main class="wrap">
<div class="hd">{ICON}<h1>داستان‌های واقعی پروندهٔ خشونت</h1></div>
<p class="lead">نُه روایت مستند. هر کدام برای این آمده که یک گزارهٔ پرونده را بدون تعریف فهمیدنی کند، و زیر هر کدام نوشته شده چرا.</p>
<div class="note"><b>درجه‌ها.</b> <span class="grade A">A</span> پژوهش داوری‌شده یا آمار رسمی · <span class="grade B">B</span> رویداد تاریخی با چند منبع مستقل · <span class="grade C">C</span> روایت شخصی تأییدنشده. همه بازگویی با کلمات خودم است، نه ترجمه. داستانی از شبکه‌های اجتماعی این‌جا نیست، چون هیچ‌کدام را نتوانستم راستی‌آزمایی کنم. بعضی روایت‌ها دربارهٔ کشتار و تجاوزند.</div>
<div class="flt" id="flt"><button data-t="all" aria-pressed="true">همه</button>{''.join(f'<button data-t="{k}" aria-pressed="false">{v}</button>' for k, v in TYPES.items())}</div>
<div class="list">{''.join(card(s) for s in ST)}</div>
<a class="back" href="../violence.html">→ بازگشت به پروندهٔ خشونت</a>
</main>
<script>
document.getElementById("flt").addEventListener("click",function(e){{var b=e.target.closest("button");if(!b)return;
this.querySelectorAll("button").forEach(function(x){{x.setAttribute("aria-pressed",x===b)}});
document.querySelectorAll(".sty").forEach(function(s){{s.classList.toggle("off",b.dataset.t!=="all"&&s.dataset.t!==b.dataset.t)}})}});
</script>
</body>
</html>
"""
open(f'{R}/psy/stories/violence.html', 'w', encoding='utf-8').write(out)
print('stories', len(ST))
