#!/usr/bin/env python3
"""Builds the portfolio in English (/) and Persian (/fa/) from one source.

Run from the repo root:  python3 tools/build.py
Edit the copy in the EN and FA dictionaries below, never the generated HTML.
Screenshots live in assets/img/en and assets/img/fa, one set per language.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPRITE = (ROOT / "assets/icons.svg").read_text(encoding="utf-8")
LI = "https://www.linkedin.com/in/maryam-jaberi-05b988140/"
GH = "https://github.com/MaryamJaberi"
MAIL = "m.jaberi1212@gmail.com"
SITE = "https://maryamjaberi.github.io/"

# Product links (same for both languages; the apps pick their own language).
URL = {
    "tw": "wellbeing-check/", "planet": SITE + "earth-through-time/", "tik": SITE + "Dour/",
    "poly": SITE + "Language-Learning-Party-Game/", "bazaar": "daneshsara/", "night": "mafia/",
    "birds": SITE + "simorgh/", "verse": SITE + "ganjoor-no/",
}
CODE = {
    "planet": GH + "/earth-through-time", "tik": GH + "/Dour", "poly": GH + "/Language-Learning-Party-Game",
    "night": GH + "/Mafia", "birds": GH + "/simorgh", "verse": GH + "/ganjoor-no",
}

EN = dict(
    lang="en", dir="ltr", other="fa", other_label="فا", other_name="فارسی",
    title="Maryam Jaberi — Product Manager & Product Designer, Rotterdam",
    desc="Maryam Jaberi, Product Manager and Product Designer in Rotterdam. Six years in product at search, streaming and education platforms with millions of users; nine products of her own.",
    skip="Skip to selected work",
    nav=dict(work="Work", how="How I work", xp="Experience", cv="CV", contact="Contact"),
    names=dict(tw="Teamweather", planet="Once Upon a Planet", tik="Tik-Tak", poly="Polyglot Party",
               bazaar="Knowledge Bazaar", night="Night Shift", birds="Thirty Birds", verse="Slow Verse", side="Side by Side"),
    kicker="Product Manager & Product Designer in Rotterdam",
    h1="I turn fuzzy ideas into products people can use.",
    lede="Six years in product at search, streaming and education platforms with millions of users. These days I also build the first version myself, so a team can test an idea instead of debating it.",
    cta_work="See selected work", cta_cv="Download CV",
    avail="Open to Product Owner, Product Manager and Product Designer roles in the Netherlands or remote. EU work permit, no sponsorship needed.",
    home_caption="My home screen. I made every app on it.",
    proof=[("6 years in product", "Product Owner and Product Manager, 2016–2022"),
           ("60K to 5M+ users", "on the streaming product I helped grow"),
           ("Scrum, introduced", "at Shaya; agile rituals across 12 services at MCI"),
           ("MSc Industrial Engineering", "Iran University of Science and Technology"),
           ("Persian, English, Dutch", "native, B2 and B1")],
    work_h="Selected work",
    work_p="Early-stage, and honest about it: tested by me and shown to experts, not yet used at scale. The case studies include what I would change.",
    case="Case study", read_case="Read the case study", open_product="Open the product",
    play="Play", open="Open", code="Code", soon="In progress",
    labels=dict(role="Role", built="Built", status="Status", decision="Decision"),
    aka="Live as",
    features=[
        dict(key="tw", aka="Workplace Wellbeing Check", tags=["B2B service"], case="case/wellbeing-check.html",
             p="A weather report for a team's inner climate. Employees answer anonymously; HR gets a forecast by job level and a plan of workshops.",
             facts=[("role", "Founder: problem framing, service design, scoring method"),
                    ("built", "Survey in 9 languages, report by job level, workshop plan, absence-cost calculator"),
                    ("status", "Shown to psychologists and HR managers; looking for first pilot organisations")]),
        dict(key="tik", aka="Dour and Dour: Language", tags=["Games", "Learning"], case="case/dour.html", phones=True,
             p="Tik-Tak is a pass-the-phone word game a group can start in ten seconds, offline, in nine languages. Polyglot Party turns the same loop into language practice.",
             facts=[("role", "Game and product design, spec, QA, release"),
                    ("built", "Installable offline web app; CEFR-levelled learning spin-off with three modes"),
                    ("status", "Live; playtests with real groups are next")]),
        dict(key="planet", aka="Chrono Atlas", tags=["Education", "Data"],
             p="Drag a timeline from the Big Bang to 1,000 years ahead and watch continents, life and societies change under your cursor.",
             facts=[("role", "Product vision, release roadmap, data principles"),
                    ("built", "Map and timeline, a catalogue of scholarly databases, a data-coverage view"),
                    ("decision", "Every claim carries its source; missing data is shown as missing, never as empty land")]),
    ],
    more_h="More projects",
    more_p="Smaller, stranger or more personal. Each one taught me something the bigger ones needed.",
    more=[
        ("bazaar", "Daneshsara", "Five Persian wikis that talk to each other: psychology, sociology, genetics, philosophy and linguistics, joined by 25 mapped bridges. Every source graded."),
        ("night", "Miz Khoda", "The Mafia narrator's assistant: deal roles, run the night, count the votes. Rules are data, so a new scenario needs no developer."),
        ("birds", "Par-e Simorgh", "Contemporary Iran as a multi-round Mafia table, named after Attar's thirty birds: 37 roles, 7 nights, 76 sourced claims."),
        ("verse", "Ganjoor No", "Persian poetry, read slowly: a calmer redesign of the best-known online poetry archive."),
        ("side", "Hamrah", "Find someone to work, learn or go out with. MVP built; the next six releases are specified."),
    ],
    how_h="How I work",
    how_p="The same five steps for a team of twenty or a team of one. AI writes most of my code now; the judgement is in the framing, the spec and the testing.",
    steps=[("Frame the problem", "Who is stuck, how often, and what it costs them. One sentence I can test."),
           ("Research", "People, evidence and what already exists. For Teamweather: Dutch absence data and validated scales."),
           ("Write the spec", "User stories with acceptance criteria, a data model and open questions, so anyone can build from it."),
           ("Build the first version", "With AI coding tools (Claude, Google AI Studio, Antigravity), one milestone at a time."),
           ("Test and iterate", "Against my own checklist first, then with experts and users. Tik-Tak has a 10-scenario release checklist.")],
    xp_h="Experience",
    skills=[("Product", ["Roadmaps and backlog ownership", "Discovery and prioritisation", "Stakeholder management", "Agile and Scrum", "Metrics and A/B testing"]),
            ("Design", ["UX research and usability testing", "Information architecture", "Service and game design", "Prototyping"]),
            ("Education", ["MSc Industrial Engineering, 2023", "Google UX Design certificate", "IBM Product Manager certificate", "Agile and Scrum, IBM / SkillUp"])],
    jobs=[("2022 – now", "Independent product and game designer", "Rotterdam",
           "Shipped nine products of my own, eight of them live. Founded SoloNovate to offer Teamweather to Dutch organisations. Reached Dutch B1 along the way."),
          ("2020 – 2022", "Product Manager, Search", "Hamrahe Aval (MCI), 1,000+ people",
           "Led the shopping-search roadmap. Started Persian speech recognition from zero with 3,000 hours of validated audio. Onboarded 1,000+ retailers, launched answer boxes on 20+ services (+10% correct clicks) and cut cross-team release errors by 10%."),
          ("2018 – 2020", "Associate Product Manager", "Arshan Media (GapFilm)",
           "Owned video-on-demand across Android, Android TV, web, kids and CMS. Grew users from 60,000 to over 5 million, added about five minutes to average sessions and scaled the CMS to 100+ admins."),
          ("2016 – 2018", "Product Owner", "Shaya Smart Technologies",
           "Introduced Scrum (about 10% fewer bugs) and owned the backlog for Payame Noor University's platform, 19 million students. Co-launched MediaAd, later Iran's second-largest native advertising platform.")],
    contact_h="Looking for a product person who also ships?",
    contact_p="Rotterdam. Authorised to work in the Netherlands and the EU.",
    footer="Made in Rotterdam, between Dutch lessons.",
)

FA = dict(
    lang="fa", dir="rtl", other="en", other_label="EN", other_name="English",
    title="مریم جابری — مدیر محصول و طراح محصول، روتردام",
    desc="مریم جابری، مدیر محصول و طراح محصول در روتردام. شش سال کار محصول در جست‌وجو، ویدیوی آنلاین و آموزش با میلیون‌ها کاربر؛ و نُه محصول از خودش.",
    skip="رفتن به نمونه‌کارها",
    nav=dict(work="کارها", how="روش کار", xp="سابقه", cv="رزومه", contact="تماس"),
    names=dict(tw="هوای تیم", planet="روزی روزگاری، زمین", tik="تیک‌تاک", poly="مهمانی زبان‌ها",
               bazaar="بازارچهٔ دانش", night="شب‌گردان", birds="سی مرغ", verse="شعرِ آهسته", side="شانه‌به‌شانه"),
    kicker="مدیر محصول و طراح محصول در روتردام",
    h1="ایده‌های مبهم را به محصولی تبدیل می‌کنم که آدم‌ها واقعاً از آن استفاده کنند.",
    lede="شش سال کار محصول در جست‌وجو، ویدیوی آنلاین و آموزش، با میلیون‌ها کاربر. این روزها نسخهٔ اول را هم خودم می‌سازم تا تیم به‌جای بحث دربارهٔ ایده، خودِ ایده را آزمایش کند.",
    cta_work="دیدن نمونه‌کارها", cta_cv="دانلود رزومه",
    avail="آمادهٔ همکاری در نقش‌های Product Owner، مدیر محصول و طراح محصول در هلند یا دورکاری. اجازهٔ کار در اروپا دارم و به اسپانسر نیاز ندارم.",
    home_caption="صفحهٔ اول گوشی‌ام؛ همهٔ این اپ‌ها را خودم ساخته‌ام.",
    proof=[("شش سال کار محصول", "Product Owner و مدیر محصول، ۲۰۱۶ تا ۲۰۲۲"),
           ("از ۶۰ هزار به ۵ میلیون کاربر", "در سرویس ویدیویی‌ای که در رشدش نقش داشتم"),
           ("راه‌اندازی اسکرام", "در شایا؛ و یکسان‌سازی آیین‌های اجایل در ۱۲ سرویس همراه اول"),
           ("کارشناسی ارشد مهندسی صنایع", "دانشگاه علم و صنعت ایران"),
           ("فارسی، انگلیسی، هلندی", "زبان مادری، B2 و B1")],
    work_h="نمونه‌کارهای برگزیده",
    work_p="هنوز در مرحلهٔ اول‌اند و این را پنهان نمی‌کنم: خودم تستشان کرده‌ام و به متخصص‌ها نشانشان داده‌ام، ولی هنوز کاربر واقعی در مقیاس ندارند. در کیس‌استادی‌ها نوشته‌ام چه چیزی را عوض می‌کردم.",
    case="کیس‌استادی", read_case="خواندن کیس‌استادی", open_product="باز کردن محصول",
    play="بازی کنید", open="باز کردن", code="کد", soon="در حال ساخت",
    labels=dict(role="نقش من", built="ساخته‌شده", status="وضعیت", decision="تصمیم"),
    aka="نام محصول",
    features=[
        dict(key="tw", aka="Workplace Wellbeing Check", tags=["خدمت سازمانی"], case="case/wellbeing-check.html",
             p="پیش‌بینی هوای درونی تیم. کارکنان ناشناس پاسخ می‌دهند؛ منابع انسانی گزارشی به تفکیک ردهٔ شغلی و برنامهٔ کارگاه می‌گیرد.",
             facts=[("role", "بنیان‌گذار: تعریف مسئله، طراحی خدمت، روش امتیازدهی"),
                    ("built", "پرسش‌نامه به ۹ زبان، گزارش به تفکیک رده، برنامهٔ کارگاه، ماشین‌حساب هزینهٔ غیبت"),
                    ("status", "به روان‌شناس‌ها و مدیران منابع انسانی نشان داده شده؛ دنبال اولین سازمان‌ها برای اجرای آزمایشی")]),
        dict(key="tik", aka="دور و دور: زبان", tags=["بازی", "یادگیری"], case="case/dour.html", phones=True,
             p="تیک‌تاک بازی کلمه‌ای است که با یک گوشیِ دست‌به‌دست، در ده ثانیه، بدون اینترنت و به نُه زبان شروع می‌شود. مهمانی زبان‌ها همین حلقه را به تمرین زبان تبدیل می‌کند.",
             facts=[("role", "طراحی بازی و محصول، مستندات، تست، انتشار"),
                    ("built", "وب‌اپ نصب‌شدنی و آفلاین؛ نسخهٔ آموزشی با سطح‌بندی CEFR و سه حالت بازی"),
                    ("status", "منتشر شده؛ قدم بعدی بازی‌آزمایی با گروه‌های واقعی")]),
        dict(key="planet", aka="Chrono Atlas", tags=["آموزش", "داده"],
             p="نوار زمان را از مهبانگ تا هزار سال بعد بکشید و ببینید قاره‌ها، زندگی و جامعه‌ها زیر دستتان چطور عوض می‌شوند.",
             facts=[("role", "چشم‌انداز محصول، نقشهٔ راه انتشار، اصول داده"),
                    ("built", "نقشه و نوار زمان، فهرست پایگاه‌های داده‌ای علمی، نمای پوشش داده"),
                    ("decision", "هر ادعا منبع دارد؛ جای خالیِ داده، خالی نشان داده می‌شود، نه سرزمین خالی")]),
    ],
    more_h="پروژه‌های دیگر",
    more_p="کوچک‌تر، عجیب‌تر یا شخصی‌تر. هر کدام چیزی یادم داد که پروژه‌های بزرگ‌تر لازمش داشتند.",
    more=[
        ("bazaar", "دانش‌سرا", "پنج ویکی فارسی که با هم حرف می‌زنند: روان‌شناسی، جامعه‌شناسی، ژنتیک، فلسفه و زبان‌شناسی، با ۲۵ پلِ مشخص میانشان. هر منبع درجه‌بندی شده."),
        ("night", "میز خدا", "دستیار گردانندهٔ مافیا: پخش نقش، اجرای شب، شمارش رأی. قانون‌ها داده‌اند، پس سناریوی تازه برنامه‌نویس لازم ندارد."),
        ("birds", "پرِ سیمرغ", "ایران امروز به‌شکل یک میز مافیای چنددوره‌ای، به یاد سی مرغ عطار: ۳۷ نقش، ۷ شب، ۷۶ ادعای مستند."),
        ("verse", "گنجور نو", "شعر فارسی را آهسته بخوانید: بازطراحی آرام‌ترِ شناخته‌شده‌ترین آرشیو آنلاین شعر فارسی."),
        ("side", "همراه", "کسی را پیدا کنید که با او کار کنید، یاد بگیرید یا بیرون بروید. نسخهٔ اول ساخته شده؛ شش انتشار بعدی مستند شده‌اند."),
    ],
    how_h="روش کار من",
    how_p="همین پنج قدم، چه تیم بیست نفر باشد چه یک نفر. این روزها بیشتر کد را هوش مصنوعی می‌نویسد؛ قضاوت در تعریف مسئله، مستندات و تست است.",
    steps=[("تعریف مسئله", "چه کسی گیر کرده، چند وقت یک بار، و چه هزینه‌ای برایش دارد. یک جمله که بشود آزمودش."),
           ("پژوهش", "آدم‌ها، شواهد، و آنچه از قبل هست. برای هوای تیم: آمار غیبت در هلند و پرسش‌نامه‌های معتبر."),
           ("نوشتن مستندات", "داستان‌های کاربری با معیار پذیرش، مدل داده و پرسش‌های باز، تا هر کسی بتواند از رویش بسازد."),
           ("ساختن نسخهٔ اول", "با ابزارهای کدنویسی هوش مصنوعی (Claude، Google AI Studio، Antigravity)، یک مرحله در هر بار."),
           ("تست و بهبود", "اول با چک‌لیست خودم، بعد با متخصص‌ها و کاربرها. تیک‌تاک یک چک‌لیست ۱۰ سناریویی برای هر انتشار دارد.")],
    xp_h="سابقه",
    skills=[("مهارت‌های محصول", ["مالکیت نقشهٔ راه و بک‌لاگ", "کشف و اولویت‌بندی", "مدیریت ذی‌نفعان", "اجایل و اسکرام", "معیارها و تست A/B"]),
            ("مهارت‌های طراحی", ["پژوهش کاربر و تست کاربردپذیری", "معماری اطلاعات", "طراحی خدمت و بازی", "نمونه‌سازی"]),
            ("تحصیلات", ["کارشناسی ارشد مهندسی صنایع، ۲۰۲۳", "گواهی طراحی UX گوگل", "گواهی مدیر محصول IBM", "اجایل و اسکرام، IBM / SkillUp"])],
    jobs=[("۲۰۲۲ تا امروز", "طراح مستقل محصول و بازی", "روتردام",
           "نُه محصول از خودم ساخته‌ام که هشت‌تایش منتشر شده. SoloNovate را راه انداختم تا هوای تیم را به سازمان‌های هلندی عرضه کنم. در این مسیر هلندی‌ام به B1 رسید."),
          ("۲۰۲۰ تا ۲۰۲۲", "مدیر محصول جست‌وجو", "همراه اول، بیش از ۱۰۰۰ نفر",
           "نقشهٔ راه جست‌وجوی خرید را رهبری کردم. تشخیص گفتار فارسی را از صفر با ۳۰۰۰ ساعت صدای اعتبارسنجی‌شده شروع کردم. بیش از ۱۰۰۰ فروشنده را وارد کردم، جعبه‌های پاسخ را در بیش از ۲۰ سرویس راه انداختم (۱۰٪ کلیک درست بیشتر) و خطاهای انتشار بین‌تیمی را ۱۰٪ کم کردم."),
          ("۲۰۱۸ تا ۲۰۲۰", "Associate Product Manager", "آرشان مدیا (گپ‌فیلم)",
           "مالک ویدیوی درخواستی در اندروید، اندروید تی‌وی، وب، کودک و CMS بودم. کاربران را از ۶۰ هزار به بیش از ۵ میلیون رساندیم، میانگین نشست حدود پنج دقیقه بیشتر شد و CMS برای بیش از ۱۰۰ ادمین بزرگ شد."),
          ("۲۰۱۶ تا ۲۰۱۸", "Product Owner", "شایا فناوری‌های هوشمند",
           "اسکرام را راه انداختم (حدود ۱۰٪ باگ کمتر) و بک‌لاگ سامانهٔ دانشگاه پیام نور با ۱۹ میلیون دانشجو را مدیریت کردم. در راه‌اندازی مدیااد سهم داشتم که بعدها دومین پلتفرم بزرگ تبلیغات بومی ایران شد.")],
    contact_h="دنبال آدم محصولی هستید که خودش هم می‌سازد؟",
    contact_p="روتردام. اجازهٔ کار در هلند و اتحادیهٔ اروپا.",
    footer="ساخته‌شده در روتردام، بین کلاس‌های هلندی.",
)

PROOF_ICONS = [
    '<rect x="4" y="10" width="26" height="18" rx="3"/><path d="M12 10V7a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v3M4 17h26"/>',
    '<circle cx="13" cy="12" r="5"/><path d="M4 28c0-5 4-9 9-9s9 4 9 9"/><circle cx="24" cy="11" r="4"/><path d="M24 19c3.5 0 6 3 6 7"/>',
    '<path d="M27 13a11 11 0 0 0-19-4M7 21a11 11 0 0 0 19 4"/><path d="M8 4v5h5M26 30v-5h-5"/>',
    '<path d="M3 13 17 6l14 7-14 7z"/><path d="M9 16v7c0 2 4 4 8 4s8-2 8-4v-7M31 13v8"/>',
    '<circle cx="17" cy="17" r="12"/><path d="M5 17h24M17 5c4 4 4 20 0 24M17 5c-4 4-4 20 0 24"/>',
]
MARK = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M7 27C9 17 15 8 26 5c-1 9-7 16-16 18"/><path d="M7 27 21 11M12 20h6M15 15.5h6"/></svg>'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=Young+Serif&family=Vazirmatn:wght@400;600;700;800&display=swap" rel="stylesheet">'


def icon(key, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{key}"/></svg>'


def head(t, title, desc, rel, path, og_img):
    """rel: prefix to the site root ('' or '../' or '../../'). path: page path for alternates, e.g. '' or 'case/dour.html'."""
    other = "fa/" if t["lang"] == "en" else ""
    en_url, fa_url = SITE + path, SITE + "fa/" + path
    canon = en_url if t["lang"] == "en" else fa_url
    return f'''<!DOCTYPE html>
<html lang="{t["lang"]}" dir="{t["dir"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="fa" href="{fa_url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5F3FA">
<link rel="icon" href="{rel}assets/mark.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{rel}assets/site.css">
'''


def nav(t, rel, home, switch_href, full=True):
    n = t["nav"]
    links = (f'<a class="l" href="{home}#work">{n["work"]}</a>\n<a class="l opt" href="{home}#how">{n["how"]}</a>\n<a class="l opt" href="{home}#experience">{n["xp"]}</a>\n'
             if full else f'<a class="l" href="{home}#work">{n["work"]}</a>\n')
    return f'''<nav class="nav" aria-label="Main">
<div class="wrap">
<a class="brand" href="{home}">{MARK}{"Maryam Jaberi" if t["lang"] == "en" else "مریم جابری"}</a>
{links}<a class="l" href="{rel}cv.pdf">{n["cv"]}</a>
<a class="lang" href="{switch_href}" hreflang="{t["other"]}" lang="{t["other"]}" title="{t["other_name"]}">{t["other_label"]}</a>
<a class="btn sm" href="{home}#contact">{n["contact"]}</a>
</div>
</nav>'''


SCRIPT = "<script>const n=document.querySelector('.nav');addEventListener('scroll',()=>n.classList.toggle('scrolled',scrollY>8),{passive:true});</script>"


def home_page(t):
    L = t["lang"]
    rel = "" if L == "en" else "../"
    img = f"{rel}assets/img/{L}/"
    names = t["names"]
    out = [head(t, t["title"], t["desc"], rel, "", "assets/og.jpg" if L == "en" else "assets/og-fa.jpg")]
    out.append('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Person","name":"Maryam Jaberi","jobTitle":"Product Manager & Product Designer","address":{"@type":"PostalAddress","addressLocality":"Rotterdam","addressCountry":"NL"},"email":"mailto:' + MAIL + '","url":"' + SITE + '","sameAs":["' + LI + '","' + GH + '"],"knowsLanguage":["fa","en","nl"]}</script>\n</head>\n<body>')
    out.append(SPRITE)
    out.append(f'<a class="skip" href="#work">{t["skip"]}</a>')
    out.append(nav(t, rel, "./", "fa/" if L == "en" else "../"))
    # hero
    order = ["tw", "planet", "tik", "poly", "bazaar", "night", "birds", "verse", "side"]
    def app_href(k):
        if k == "tw": return "#work"
        if k == "side": return "#more"
        u = URL[k]
        return u if u.startswith("http") else rel + u
    apps = "\n".join(f'<li class="app"><a href="{app_href(k)}">{icon(k)}<span>{names[k]}</span></a></li>' for k in order)
    out.append(f'''<header class="hero">
<div class="wrap">
<div>
<p class="kicker">{t["kicker"]}</p>
<h1>{t["h1"]}</h1>
<p class="lede">{t["lede"]}</p>
<div class="links"><a class="btn solid" href="#work">{t["cta_work"]}</a><a class="btn" href="{rel}cv.pdf" download>{t["cta_cv"]}</a></div>
<p class="avail"><i aria-hidden="true"></i>{t["avail"]}</p>
</div>
<div class="home">
<ul class="apps">
{apps}
</ul>
<p>{t["home_caption"]}</p>
</div>
</div>
</header>''')
    proof = "\n".join(f'<li><svg viewBox="0 0 34 34" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">{PROOF_ICONS[i]}</svg><span><b>{b}</b>{s}</span></li>' for i, (b, s) in enumerate(t["proof"]))
    out.append(f'<section class="proof" aria-label="Highlights"><div class="wrap"><ul>\n{proof}\n</ul></div></section>\n<main>')
    # selected work
    rows = []
    lab = t["labels"]
    for f in t["features"]:
        k = f["key"]
        if f.get("phones"):
            shot = f'<div class="shot phones"><img src="{img}dour.webp" alt="{names["tik"]}" loading="lazy" width="390" height="780"><img src="{img}lang.webp" alt="{names["poly"]}" loading="lazy" width="390" height="780"></div>'
            title = f'{names["tik"]} & {names["poly"]}' if L == "en" else f'{names["tik"]} و {names["poly"]}'
            icons = icon("tik", "ic lg") + icon("poly", "ic lg")
        else:
            src = "wb-report" if k == "tw" else "atlas"
            shot = f'<div class="shot"><img src="{img}{src}.webp" alt="{names[k]}" loading="lazy" width="1200" height="750"></div>'
            title, icons = names[k], icon(k, "ic lg")
        pills = ("".join(f'<span class="pill case">{t["case"]}</span>' for _ in [1] if f.get("case"))
                 + "".join(f'<span class="pill">{x}</span>' for x in f["tags"]))
        facts = "".join(f'<li><span>{lab[a]}</span>{b}</li>' for a, b in f["facts"])
        if f.get("case"):
            links = f'<a class="btn sm solid" href="{f["case"]}">{t["read_case"]}</a><a class="textlink" href="{rel + URL[k] if not URL[k].startswith("http") else URL[k]}">{t["open_product"] if k == "tw" else t["play"]}</a>'
        else:
            links = f'<a class="btn sm" href="{URL[k]}">{t["open"]}</a><a class="textlink" href="{CODE[k]}">{t["code"]}</a>'
        rows.append(f'''<article class="feature">
{shot}
<div>
<div class="meta">{pills}</div>
<div class="title-row">{icons}<h3>{title}</h3></div>
<p class="aka">{t["aka"]}: <span class="ltr">{f["aka"]}</span></p>
<p>{f["p"]}</p>
<ul class="facts">{facts}</ul>
<div class="links">{links}</div>
</div>
</article>''')
    out.append(f'''<section class="sec" id="work" aria-labelledby="work-h">
<div class="wrap">
<div class="sec-head"><h2 id="work-h">{t["work_h"]}</h2><p>{t["work_p"]}</p></div>
{chr(10).join(rows)}
</div>
</section>''')
    # more projects
    items = []
    for k, aka, p in t["more"]:
        if k == "side":
            links = f'<span class="soon">{t["soon"]}</span>'
        else:
            u = URL[k] if URL[k].startswith("http") else rel + URL[k]
            links = f'<a class="textlink" href="{u}">{t["open"]}</a>' + (f'<a class="textlink" href="{CODE[k]}">{t["code"]}</a>' if k in CODE else "")
        items.append(f'<li>{icon(k, "ic lg")}<div><h3>{names[k]}</h3><p class="aka" style="margin:0">{t["aka"]}: {aka}</p><p>{p}</p><div class="links">{links}</div></div></li>')
    out.append(f'''<section class="sec" id="more" aria-labelledby="more-h">
<div class="wrap">
<div class="sec-head"><h2 id="more-h">{t["more_h"]}</h2><p>{t["more_p"]}</p></div>
<ul class="mlist">
{chr(10).join(items)}
</ul>
</div>
</section>''')
    steps = "".join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a, b in t["steps"])
    out.append(f'''<section class="dark" id="how" aria-labelledby="how-h">
<div class="wrap">
<div class="sec-head"><h2 id="how-h">{t["how_h"]}</h2><p>{t["how_p"]}</p></div>
<ol class="process">{steps}</ol>
</div>
</section>''')
    side = "".join(f'<h3>{h}</h3><ul>{"".join(f"<li>{x}</li>" for x in xs)}</ul>' for h, xs in t["skills"])
    jobs = "".join(f'<div class="job"><div class="yr">{y}</div><div><h3>{a}</h3><p class="co">{c}</p><p>{d}</p></div></div>' for y, a, c, d in t["jobs"])
    out.append(f'''<section class="sec" id="experience" aria-labelledby="xp-h">
<div class="wrap xp">
<div class="side"><h2 id="xp-h">{t["xp_h"]}</h2>{side}</div>
<div>{jobs}</div>
</div>
</section>
</main>''')
    out.append(f'''<section class="contact" id="contact" aria-labelledby="contact-h">
<div class="wrap">
<div><h2 id="contact-h">{t["contact_h"]}</h2></div>
<div>
<p><a class="mail ltr" href="mailto:{MAIL}">{MAIL}</a></p>
<p class="small">{t["contact_p"]}</p>
<div class="links" style="margin-top:22px"><a class="btn solid" href="{rel}cv.pdf" download>{t["cta_cv"]}</a><a class="btn" href="{LI}">LinkedIn</a><a class="textlink" href="{GH}">GitHub</a></div>
</div>
</div>
</section>
<footer><div class="wrap"><span>© 2026 {"Maryam Jaberi" if L == "en" else "مریم جابری"}</span><span>{t["footer"]}</span></div></footer>
{SCRIPT}
</body>
</html>
''')
    return "\n".join(out)


# ---------------- case studies ----------------
CASES = {
    "wellbeing-check": dict(
        icon="tw",
        en=dict(
            title="Teamweather — case study — Maryam Jaberi",
            desc="Case study: an anonymous psychological-wellbeing check for Dutch organisations that ends in a plan, not just a score.",
            h1="A weather report for a team's inner climate",
            lede="How I designed Teamweather, an anonymous wellbeing assessment for Dutch organisations: validated science for employees, a clear report for HR, and a plan for whoever holds the budget.",
            aka="Live as Workplace Wellbeing Check",
            overview=[("My role", "Founder: problem framing, service design, scoring method, product"), ("When", "2026"),
                      ("Built with", "My spec, AI coding tools, published scientific questionnaires"), ("Status", "Pilot-ready; looking for first organisations")],
            cover=("wb-home", "Teamweather home page with a sample organisation report of eight scores"),
            primary=("Open the product", "wellbeing-check/"), secondary=("See the sample report", "wellbeing-check/#report"),
            chapters=[
                ("The problem", '''<p>Psychological health shows up on the balance sheet. In the Netherlands it is measurable, and large:</p>
<div class="stat-row"><div><b>1 in 5</b><span>Dutch employees report burnout complaints (20.7% in 2025). RIVM / NEA, CBS & TNO</span></div><div><b>€4.9 bn</b><span>absence cost from psychosocial workload in 2023. TNO Arbobalans 2024</span></div><div><b>RI&E</b><span>Dutch employers must assess psychosocial workload in their risk inventory</span></div></div>
<p>Yet when an organisation tries to measure it, three things go wrong:</p>
<ul><li><b>The questions are home-made</b>, so the numbers can't be compared or trusted.</li><li><b>Employees fear being identified</b>, so they answer politely instead of honestly.</li><li><b>A score doesn't say what to do next</b>, so the report ends up in a drawer.</li></ul>
<p class="quote">How might we give an organisation an honest picture of its people's psychological health, without exposing anyone, and turn it into action?</p>'''),
                ("Research and insights", '''<p>I studied the published questionnaires and the meta-analyses behind workplace interventions; Dutch and European rules (GDPR, Arbowet, the RI&E and the works council's right of consent); and who actually decides to buy a staff survey.</p>
<h3>Three users, not one</h3><p>The employee answers, HR reads, a manager pays. The employee needs safety and something in return; HR needs clarity; the budget holder needs a reason in euros.</p>
<h3>Anonymity has to be structural</h3><p>A privacy promise in the footer is not enough. If a team of three is visible in the report, people hold back. The rule has to live in the product.</p>
<h3>In the Netherlands, rules sell</h3><p>A survey like this usually goes past the works council (WOR art. 27). Arriving with the documents ready can save weeks.</p>'''),
                ("Decisions", '''<p>Every decision traded something away. These shaped the product most.</p>
<div class="decision"><div><b>Validated questionnaires only</b>Eight published scales, one per dimension, each with its source.</div><div class="no"><b>Instead of</b>Custom questions that read better but can't be compared or defended to a psychologist.</div></div>
<div class="decision"><div><b>Groups under 5 are never shown</b>Minimum 20 participants, 5 per job level, no names collected.</div><div class="no"><b>Instead of</b>Team-level detail, which managers ask for and which breaks trust.</div></div>
<div class="decision"><div><b>Give before you take</b>Every participant sees a personal summary and two tips straight away. Nothing goes to management.</div><div class="no"><b>Instead of</b>A one-way survey where honesty brings the person nothing.</div></div>
<div class="decision"><div><b>A rule that turns scores into priorities</b>A dimension is a priority below 55 out of 100, or when more than 25% are in "needs attention".</div><div class="no"><b>Instead of</b>A ranked chart that leaves HR to guess what matters.</div></div>
<div class="decision"><div><b>Each priority maps to a workshop</b>Goals, audience, duration and evidence, run by a qualified partner in the Netherlands.</div><div class="no"><b>Instead of</b>A list of generic wellbeing tips.</div></div>
<div class="decision"><div><b>Nine languages, 8 to 18 minutes</b>Dutch workforces are multilingual; a short core check keeps participation high.</div><div class="no"><b>Instead of</b>Dutch and English only, which quietly excludes part of the staff.</div></div>
<figure><img src="{img}wb-report.webp" alt="Organisation report with sample data for 180 respondents in four job levels" loading="lazy" width="1200" height="750"><figcaption>The organisation report with sample data: four numbers first, then a plain-language summary, then detail by job level.</figcaption></figure>
<figure><img src="{img}wb-workshops.webp" alt="Workshop catalogue with audience, duration, goals and evidence for each workshop" loading="lazy" width="1200" height="750"><figcaption>Each workshop states who it's for, how long it takes, its goals and the research behind it.</figcaption></figure>
<p>Then I wrapped it as a service a manager can say yes to: a four-week pilot (set up, collect, report, debrief), ready-made documents for the works council, staff and data processing, and an absence-cost calculator that shows what a small improvement is worth in euros.</p>'''),
                ("Result so far", '''<p>A complete, working pilot in English, Dutch and Persian: survey, personal summary, organisation report, workshop catalogue, method and sources, and the pilot documents. It is offered through SoloNovate, my company in Rotterdam.</p>
<p>It has no real users yet. Psychologists, HR managers and managers of large organisations have seen it, and I am looking for the first pilot organisations.</p>
<h3>What I'll measure in the first pilot</h3><ul><li>Participation per job level: is the anonymity trusted?</li><li>Time from report to first workshop booked: does the report lead to action?</li><li>Change per dimension at the repeat measurement after 3 to 6 months.</li></ul>'''),
                ("What I'd do differently", '''<p><b>Talk to buyers earlier.</b> I built the full report and nine languages before asking five HR managers how they buy. A one-page concept and a sample report would have tested the riskiest assumption, willingness to pay, in a week.</p>
<p><b>Start narrower.</b> Eight dimensions is thorough, but a first pilot with three would be quicker to explain and run.</p>
<p><b>Check licences first.</b> Some validated questionnaires have usage terms; listing them up front would have saved rework.</p>'''),
            ],
            next=("dour.html", "A party game that starts in ten seconds"),
        ),
        fa=dict(
            title="هوای تیم — کیس‌استادی — مریم جابری",
            desc="کیس‌استادی: سنجش ناشناس سلامت روانی کارکنان برای سازمان‌های هلندی که به برنامهٔ عمل می‌رسد، نه فقط به یک عدد.",
            h1="پیش‌بینی هوای درونی یک تیم",
            lede="چطور «هوای تیم» را طراحی کردم: سنجش ناشناس سلامت روانی برای سازمان‌های هلندی، با علم معتبر برای کارمند، گزارشی روشن برای منابع انسانی، و برنامه‌ای برای کسی که بودجه دستش است.",
            aka="نام محصول: Workplace Wellbeing Check",
            overview=[("نقش من", "بنیان‌گذار: تعریف مسئله، طراحی خدمت، روش امتیازدهی، محصول"), ("زمان", "۲۰۲۶"),
                      ("ابزار", "مستندات خودم، ابزارهای کدنویسی هوش مصنوعی، پرسش‌نامه‌های علمی منتشرشده"), ("وضعیت", "آمادهٔ اجرای آزمایشی؛ دنبال اولین سازمان‌ها")],
            cover=("wb-home", "صفحهٔ اول هوای تیم با نمونهٔ گزارش سازمان و هشت امتیاز"),
            primary=("باز کردن محصول", "wellbeing-check/"), secondary=("دیدن نمونهٔ گزارش", "wellbeing-check/#report"),
            chapters=[
                ("مسئله", '''<p>سلامت روانی در ترازنامهٔ سازمان دیده می‌شود. در هلند این را می‌شود اندازه گرفت، و بزرگ است:</p>
<div class="stat-row"><div><b>۱ از ۵</b><span>کارمند هلندی علائم فرسودگی شغلی گزارش می‌کند (۲۰٫۷٪ در ۲۰۲۵). RIVM / NEA، CBS و TNO</span></div><div><b>۴٫۹ میلیارد یورو</b><span>هزینهٔ غیبت ناشی از فشار روانی-اجتماعی در ۲۰۲۳. TNO Arbobalans 2024</span></div><div><b>RI&E</b><span>کارفرمای هلندی باید فشار روانی-اجتماعی را در ارزیابی ریسک بسنجد</span></div></div>
<p>اما وقتی سازمانی می‌خواهد آن را بسنجد، سه چیز خراب می‌شود:</p>
<ul><li><b>پرسش‌ها دست‌ساز است</b>، پس عددها نه قابل مقایسه‌اند نه قابل اعتماد.</li><li><b>کارمند می‌ترسد شناخته شود</b>، پس مؤدبانه جواب می‌دهد، نه صادقانه.</li><li><b>عدد نمی‌گوید قدم بعدی چیست</b>، پس گزارش در کشو می‌ماند.</li></ul>
<p class="quote">چطور می‌شود تصویری صادقانه از سلامت روانی کارکنان به سازمان داد، بی‌آنکه کسی لو برود، و آن را به عمل تبدیل کرد؟</p>'''),
                ("پژوهش و یافته‌ها", '''<p>پرسش‌نامه‌های منتشرشده و فراتحلیل‌های پشت مداخله‌های محیط کار را خواندم؛ قوانین هلند و اروپا را (GDPR، قانون شرایط کار، ارزیابی ریسک و حق موافقت شورای کار)؛ و اینکه چه کسی واقعاً تصمیم به خرید یک نظرسنجی کارکنان می‌گیرد.</p>
<h3>سه کاربر، نه یکی</h3><p>کارمند پاسخ می‌دهد، منابع انسانی می‌خواند، مدیر پول می‌دهد. کارمند امنیت و چیزی در عوض می‌خواهد؛ منابع انسانی وضوح؛ صاحب بودجه دلیلی به یورو.</p>
<h3>ناشناس‌ماندن باید در ساختار باشد</h3><p>قول حریم خصوصی در پایین صفحه کافی نیست. اگر تیمی سه‌نفره در گزارش دیده شود، آدم‌ها خودشان را نگه می‌دارند. قاعده باید در خود محصول باشد.</p>
<h3>در هلند، قانون می‌فروشد</h3><p>چنین نظرسنجی‌ای معمولاً از شورای کار می‌گذرد (مادهٔ ۲۷ قانون شوراهای کار). آمدن با مدارک آماده می‌تواند هفته‌ها جلو بیندازد.</p>'''),
                ("تصمیم‌ها", '''<p>هر تصمیم چیزی را قربانی کرد. این‌ها بیشترین اثر را روی محصول داشتند.</p>
<div class="decision"><div><b>فقط پرسش‌نامه‌های معتبر</b>هشت مقیاس منتشرشده، یکی برای هر بُعد، هرکدام با منبع.</div><div class="no"><b>به‌جای</b>پرسش‌های دلخواه که خوش‌خوان‌ترند ولی نه قابل مقایسه‌اند نه قابل دفاع پیش روان‌شناس.</div></div>
<div class="decision"><div><b>گروه زیر ۵ نفر هرگز نشان داده نمی‌شود</b>حداقل ۲۰ شرکت‌کننده، ۵ نفر در هر رده، بدون گرفتن نام.</div><div class="no"><b>به‌جای</b>جزئیات در سطح تیم، که مدیران می‌خواهند و اعتماد را می‌شکند.</div></div>
<div class="decision"><div><b>اول بده، بعد بگیر</b>هر شرکت‌کننده فوراً خلاصهٔ شخصی و دو توصیه می‌بیند. چیزی به مدیریت نمی‌رسد.</div><div class="no"><b>به‌جای</b>نظرسنجی یک‌طرفه که صداقت برای پاسخ‌دهنده سودی ندارد.</div></div>
<div class="decision"><div><b>قاعده‌ای که عدد را به اولویت تبدیل می‌کند</b>یک بُعد اولویت است اگر زیر ۵۵ از ۱۰۰ باشد، یا بیش از ۲۵٪ در «نیازمند توجه» باشند.</div><div class="no"><b>به‌جای</b>نموداری رتبه‌بندی‌شده که حدس‌زدن را به منابع انسانی می‌سپارد.</div></div>
<div class="decision"><div><b>هر اولویت یک کارگاه دارد</b>با هدف، مخاطب، مدت و شواهد، به اجرای یک همکار متخصص در هلند.</div><div class="no"><b>به‌جای</b>فهرستی از توصیه‌های کلی.</div></div>
<div class="decision"><div><b>نُه زبان، ۸ تا ۱۸ دقیقه</b>نیروی کار هلند چندزبانه است؛ نسخهٔ کوتاه مشارکت را بالا نگه می‌دارد.</div><div class="no"><b>به‌جای</b>فقط هلندی و انگلیسی، که بی‌صدا بخشی از کارکنان را کنار می‌گذارد.</div></div>
<figure><img src="{img}wb-report.webp" alt="گزارش سازمان با دادهٔ نمونه برای ۱۸۰ پاسخ‌دهنده در چهار ردهٔ شغلی" loading="lazy" width="1200" height="750"><figcaption>گزارش سازمان با دادهٔ نمونه: اول چهار عدد، بعد خلاصه به زبان ساده، بعد جزئیات به تفکیک رده.</figcaption></figure>
<figure><img src="{img}wb-workshops.webp" alt="فهرست کارگاه‌ها با مخاطب، مدت، هدف و شواهد" loading="lazy" width="1200" height="750"><figcaption>هر کارگاه می‌گوید برای چه کسی است، چقدر طول می‌کشد، هدفش چیست و چه پژوهشی پشتش است.</figcaption></figure>
<p>بعد آن را به شکل خدمتی درآوردم که مدیر بتواند به آن «بله» بگوید: اجرای آزمایشی چهارهفته‌ای (راه‌اندازی، جمع‌آوری، گزارش، جلسهٔ جمع‌بندی)، مدارک آماده برای شورای کار، کارکنان و پردازش داده، و ماشین‌حساب هزینهٔ غیبت که نشان می‌دهد یک بهبود کوچک چند یورو می‌ارزد.</p>'''),
                ("نتیجه تا امروز", '''<p>یک نسخهٔ آزمایشیِ کامل و کارا به انگلیسی، هلندی و فارسی: پرسش‌نامه، خلاصهٔ شخصی، گزارش سازمان، فهرست کارگاه‌ها، روش و منابع، و مدارک اجرای آزمایشی. از طریق SoloNovate، شرکتم در روتردام، عرضه می‌شود.</p>
<p>هنوز کاربر واقعی ندارد. روان‌شناس‌ها، مدیران منابع انسانی و مدیران سازمان‌های بزرگ آن را دیده‌اند و دنبال اولین سازمان‌ها برای اجرای آزمایشی هستم.</p>
<h3>آنچه در اولین اجرا می‌سنجم</h3><ul><li>نرخ مشارکت در هر رده: آیا به ناشناس‌ماندن اعتماد شده؟</li><li>فاصلهٔ گزارش تا رزرو اولین کارگاه: آیا گزارش به عمل می‌رسد؟</li><li>تغییر هر بُعد در سنجش دوباره بعد از ۳ تا ۶ ماه.</li></ul>'''),
                ("اگر دوباره می‌ساختم", '''<p><b>زودتر با خریدار حرف می‌زدم.</b> گزارش کامل و نُه زبان را ساختم و بعد از پنج مدیر منابع انسانی پرسیدم چطور خرید می‌کنند. یک مفهوم یک‌صفحه‌ای و یک نمونه‌گزارش می‌توانست پرریسک‌ترین فرض، یعنی تمایل به پرداخت، را در یک هفته بیازماید.</p>
<p><b>کوچک‌تر شروع می‌کردم.</b> هشت بُعد کامل است، ولی اجرای اول با سه بُعد سریع‌تر توضیح داده و اجرا می‌شود.</p>
<p><b>اول مجوزها را بررسی می‌کردم.</b> بعضی پرسش‌نامه‌های معتبر شرایط استفاده دارند؛ فهرست‌کردنشان از اول، دوباره‌کاری را کم می‌کرد.</p>'''),
            ],
            next=("dour.html", "بازی مهمانی‌ای که در ده ثانیه شروع می‌شود"),
        ),
    ),
    "dour": dict(
        icon="tik",
        en=dict(
            title="Tik-Tak — case study — Maryam Jaberi",
            desc="Case study: a pass-the-phone party game a group can start in ten seconds, offline, in nine languages, and the language-learning game that grew out of it.",
            h1="A party game that starts in ten seconds",
            lede="How I designed Tik-Tak, a word-guessing game for one phone passed around the room, and then reused its core loop so language practice feels like a game night.",
            aka="Live as Dour and Dour: Language",
            overview=[("My role", "Game and product design, spec, QA, release"), ("Platform", "Installable web app (PWA), works offline"),
                      ("Languages", "Nine, from Persian to Ukrainian"), ("Status", "Live; playtests with real groups next")],
            phones=True,
            primary=("Play Tik-Tak", "https://maryamjaberi.github.io/Dour/"), secondary=("Play Polyglot Party", "https://maryamjaberi.github.io/Language-Learning-Party-Game/"),
            chapters=[
                ("The problem", '''<p>Word-guessing card games are a staple of family evenings and parties, Iranian homes included. But the box of cards speaks one language, and most app versions assume everyone reads English, want an account and a connection, and fall apart the moment someone taps the wrong button mid-round.</p>
<p class="quote">How might any group start a round in seconds, in the language they actually speak at that table?</p>'''),
                ("Constraints", '''<ul><li><b>One device for everyone.</b> Not everyone at a party will install an app; the host's phone has to be enough.</li><li><b>Mixed tables.</b> Different ages and languages in the same room.</li><li><b>No reliable Wi-Fi.</b> Gardens, trips, a relative's living room.</li><li><b>Noise and excitement.</b> People shout, grab the phone and tap the wrong thing. The game has to forgive that.</li></ul>'''),
                ("Decisions", '''<div class="decision"><div><b>Teams sit opposite each other</b>The phone always passes to the other team, so nobody needs telling whose turn it is.</div><div class="no"><b>Instead of</b>A turn indicator nobody reads mid-round.</div></div>
<div class="decision"><div><b>Undo without pausing</b>A floating undo button fixes an accidental tap while the clock keeps running.</div><div class="no"><b>Instead of</b>A pause-and-confirm dialog that kills the round's energy.</div></div>
<div class="decision"><div><b>Sound that doesn't stress</b>A soft wooden tick through the round (hence the name), and a short alarm only in the last five seconds.</div><div class="no"><b>Instead of</b>A constant beep that makes people anxious.</div></div>
<div class="decision"><div><b>Difficulty as content</b>Easy single words, medium two-word terms, hard proverbs and idioms.</div><div class="no"><b>Instead of</b>Shorter timers for "hard", which only makes it frantic.</div></div>
<div class="decision"><div><b>No account needed</b>Open and play. Cloud sign-in is optional, for keeping history.</div><div class="no"><b>Instead of</b>Sign-up first, which loses the group before round one.</div></div>'''),
                ("Build and test", '''<p>I wrote rules, screens and edge cases as a spec, built it with AI coding tools, and tested every release against my own ten-scenario checklist: startup, sound, no repeated words, timer, turn handover, winner screen, mobile layout, pause and reset, install, and offline play.</p>
<p>Writing the checklist before the build meant every bug report pointed to a scenario, and every fix could be checked against the same one.</p>'''),
                ("Polyglot Party", '''<p>Guessing a word from a teammate's description is exactly what a language learner needs to practise. So I rebuilt the loop as Polyglot Party:</p>
<ul><li>Cards with real vocabulary and phrases, levelled by CEFR from A1 to C1.</li><li>Up to four learning languages at once, so a mixed group can play together.</li><li>Group, two-player duel and solo modes, with spaced review of mistakes.</li><li>A freemium model where the free version keeps most features; I wrote the revenue model and the epics with user stories.</li></ul>
<p>The next design problem is difficulty: I'm specifying an adaptive algorithm that makes cards harder or easier per player, so rounds stay close.</p>'''),
                ("Result and next", '''<p>Both games are live as installable web apps. Neither has real users yet. Next come structured playtests with real groups, measuring:</p>
<ul><li>Rounds per session, and how many groups play again within a week.</li><li>How often undo is used, and where: a map of where taps go wrong.</li><li>The round where players stop, to tune length and difficulty.</li></ul>
<h3>What I'd do differently</h3><p>I added nine languages before testing with a single group, and word lists of uneven quality are now a risk. Next time I'd prove the loop in one or two languages first, then expand.</p>'''),
            ],
            next=("wellbeing-check.html", "A weather report for a team's inner climate"),
        ),
        fa=dict(
            title="تیک‌تاک — کیس‌استادی — مریم جابری",
            desc="کیس‌استادی: بازی کلمه‌ای با یک گوشیِ دست‌به‌دست که در ده ثانیه، بدون اینترنت و به نُه زبان شروع می‌شود، و بازی آموزش زبانی که از دلش درآمد.",
            h1="بازی مهمانی‌ای که در ده ثانیه شروع می‌شود",
            lede="چطور «تیک‌تاک» را طراحی کردم، بازی حدس کلمه برای یک گوشی که دور اتاق می‌چرخد، و بعد همان حلقه را دوباره به کار بردم تا تمرین زبان حس شب‌نشینی بدهد.",
            aka="نام محصول: دور و دور: زبان",
            overview=[("نقش من", "طراحی بازی و محصول، مستندات، تست، انتشار"), ("سکو", "وب‌اپ نصب‌شدنی (PWA)، آفلاین"),
                      ("زبان‌ها", "نُه زبان، از فارسی تا اوکراینی"), ("وضعیت", "منتشر شده؛ بعدی: بازی‌آزمایی با گروه‌های واقعی")],
            phones=True,
            primary=("بازی تیک‌تاک", "https://maryamjaberi.github.io/Dour/"), secondary=("بازی مهمانی زبان‌ها", "https://maryamjaberi.github.io/Language-Learning-Party-Game/"),
            chapters=[
                ("مسئله", '''<p>بازی‌های کارتی حدس کلمه پای ثابت شب‌نشینی‌ها و مهمانی‌هاست، در خانه‌های ایرانی هم. اما جعبهٔ کارت فقط یک زبان بلد است، و بیشتر نسخه‌های اپی فرض می‌کنند همه انگلیسی می‌خوانند، حساب کاربری و اینترنت می‌خواهند، و همین که کسی وسط دور دکمهٔ اشتباه را بزند، به هم می‌ریزند.</p>
<p class="quote">چطور هر جمعی بتواند در چند ثانیه، به همان زبانی که سر آن میز حرف می‌زند، دور را شروع کند؟</p>'''),
                ("محدودیت‌ها", '''<ul><li><b>یک گوشی برای همه.</b> همه در مهمانی اپ نصب نمی‌کنند؛ گوشی میزبان باید کافی باشد.</li><li><b>جمع‌های ناهمگون.</b> سن‌ها و زبان‌های مختلف در یک اتاق.</li><li><b>اینترنت مطمئن نیست.</b> باغ، سفر، خانهٔ فامیل.</li><li><b>سروصدا و هیجان.</b> داد می‌زنند، گوشی را می‌قاپند و دکمهٔ اشتباه را می‌زنند. بازی باید ببخشد.</li></ul>'''),
                ("تصمیم‌ها", '''<div class="decision"><div><b>تیم‌ها روبه‌روی هم می‌نشینند</b>گوشی همیشه به تیم مقابل می‌رسد و لازم نیست کسی بگوید نوبت کیست.</div><div class="no"><b>به‌جای</b>نشانگر نوبت که وسط دور کسی نمی‌خواندش.</div></div>
<div class="decision"><div><b>برگرداندن بدون توقف</b>دکمهٔ شناورِ برگشت، ضربهٔ اشتباه را درست می‌کند و ساعت ادامه می‌دهد.</div><div class="no"><b>به‌جای</b>پنجرهٔ توقف و تأیید که هیجان دور را می‌کُشد.</div></div>
<div class="decision"><div><b>صدایی که استرس نمی‌دهد</b>تیک‌تاک آرام چوبی در طول دور (اسمش هم از همین‌جاست) و فقط در پنج ثانیهٔ آخر یک زنگ کوتاه.</div><div class="no"><b>به‌جای</b>بوق مداوم که آدم را مضطرب می‌کند.</div></div>
<div class="decision"><div><b>سختی از جنس محتوا</b>آسان: یک کلمه؛ متوسط: دو کلمه؛ سخت: ضرب‌المثل و اصطلاح.</div><div class="no"><b>به‌جای</b>زمان کمتر برای «سخت»، که فقط بازی را هول‌هولکی می‌کند.</div></div>
<div class="decision"><div><b>بدون حساب کاربری</b>باز کن و بازی کن. ورود ابری اختیاری است، برای نگه‌داشتن تاریخچه.</div><div class="no"><b>به‌جای</b>ثبت‌نام اول کار، که جمع را قبل از دور اول از دست می‌دهد.</div></div>'''),
                ("ساخت و تست", '''<p>قانون‌ها، صفحه‌ها و حالت‌های مرزی را به شکل مستندات نوشتم، با ابزارهای کدنویسی هوش مصنوعی ساختم و هر انتشار را با چک‌لیست ده سناریویی خودم تست کردم: شروع، صدا، تکرارنشدن کلمه‌ها، تایمر، دست‌به‌دست شدن نوبت، صفحهٔ برنده، نمایش موبایل، توقف و از نو، نصب، و بازی آفلاین.</p>
<p>نوشتن چک‌لیست پیش از ساخت یعنی هر گزارش باگ به یک سناریو اشاره می‌کرد و هر رفع باگ با همان سناریو بررسی می‌شد.</p>'''),
                ("مهمانی زبان‌ها", '''<p>حدس‌زدن کلمه از روی توضیح هم‌تیمی دقیقاً همان تمرینی است که زبان‌آموز لازم دارد. پس حلقه را دوباره ساختم و شد «مهمانی زبان‌ها»:</p>
<ul><li>کارت‌هایی با واژه و عبارت واقعی، سطح‌بندی‌شده با CEFR از A1 تا C1.</li><li>تا چهار زبان یادگیری هم‌زمان، تا جمع چندزبانه با هم بازی کند.</li><li>حالت گروهی، دوئل دونفره و تک‌نفره، با مرور فاصله‌دار اشتباه‌ها.</li><li>مدل فریمیوم که نسخهٔ رایگانش بیشتر امکانات را دارد؛ مدل درآمدی و اپیک‌ها را با داستان‌های کاربری نوشتم.</li></ul>
<p>مسئلهٔ طراحی بعدی سختی است: دارم الگوریتمی تطبیقی را مستند می‌کنم که کارت‌ها را برای هر بازیکن سخت‌تر یا آسان‌تر کند تا دورها نزدیک بمانند.</p>'''),
                ("نتیجه و قدم بعد", '''<p>هر دو بازی به شکل وب‌اپ نصب‌شدنی منتشر شده‌اند و هنوز کاربر واقعی ندارند. قدم بعدی بازی‌آزمایی منظم با گروه‌های واقعی است، با این سنجه‌ها:</p>
<ul><li>تعداد دور در هر نشست، و چند گروه در همان هفته دوباره بازی می‌کنند.</li><li>چند بار و کجا دکمهٔ برگشت زده می‌شود: نقشه‌ای از جاهایی که ضربه‌ها اشتباه می‌روند.</li><li>دوری که بازیکن‌ها در آن دست می‌کشند، برای تنظیم طول و سختی.</li></ul>
<h3>اگر دوباره می‌ساختم</h3><p>نُه زبان را پیش از تست با حتی یک گروه اضافه کردم و حالا کیفیت ناهمسان فهرست کلمه‌ها یک ریسک است. دفعهٔ بعد اول حلقه را با یک یا دو زبان ثابت می‌کنم، بعد گسترش می‌دهم.</p>'''),
            ],
            next=("wellbeing-check.html", "پیش‌بینی هوای درونی یک تیم"),
        ),
    ),
}


def case_page(slug, L):
    c = CASES[slug]
    t = EN if L == "en" else FA
    d = c[L]
    rel = "../" if L == "en" else "../../"
    img = f"{rel}assets/img/{L}/"
    switch = f"../../case/{slug}.html" if L == "fa" else f"../fa/case/{slug}.html"
    back_label = "Back to all work" if L == "en" else "بازگشت به همهٔ کارها"
    next_label = "Next case study" if L == "en" else "کیس‌استادی بعدی"
    read = "Read it" if L == "en" else "بخوانید"
    skip = "Skip to the case study" if L == "en" else "رفتن به کیس‌استادی"
    out = [head(t, d["title"], d["desc"], rel, f"case/{slug}.html", f"assets/img/{L}/" + ("wb-report.webp" if slug == "wellbeing-check" else "dour.webp")), "</head>\n<body>", SPRITE,
           f'<a class="skip" href="#main">{skip}</a>', nav(t, rel, "../", switch, full=False)]
    ov = "".join(f'<div><span>{a}</span>{b}</div>' for a, b in d["overview"])
    if d.get("phones"):
        cover = f'<div class="phones-fig" style="margin-top:40px"><img src="{img}dour.webp" alt="{t["names"]["tik"]}" width="390" height="780"><img src="{img}lang.webp" alt="{t["names"]["poly"]}" width="390" height="780"></div>'
    else:
        cover = f'<figure class="cover"><img src="{img}{d["cover"][0]}.webp" alt="{d["cover"][1]}" width="1200" height="750"></figure>'
    def link(u): return u if u.startswith("http") or u.startswith("#") else rel + u
    out.append(f'''<main id="main">
<header class="case-hero">
<div class="wrap">
<a class="back" href="../">{back_label}</a>
<div class="title-row" style="margin-top:22px">{icon(c["icon"], "ic lg")}<p class="aka" style="margin:0">{d["aka"]}</p></div>
<h1>{d["h1"]}</h1>
<p class="lede">{d["lede"]}</p>
<div class="overview">{ov}</div>
{cover}
<div class="links" style="margin-top:20px"><a class="btn solid sm" href="{link(d["primary"][1])}">{d["primary"][0]}</a><a class="textlink" href="{link(d["secondary"][1])}">{d["secondary"][0]}</a></div>
</div>
</header>
<div class="wrap">''')
    for i, (h, body) in enumerate(d["chapters"], 1):
        out.append(f'<section class="chapter" aria-labelledby="c{i}"><h2 id="c{i}">{h}</h2><div class="body">{body.replace("{img}", img)}</div></section>')
    nh, nt = d["next"]
    out.append(f'''<div class="next-case"><p class="small">{next_label}</p><h2 style="margin:0 0 16px"><a href="{nh}" style="text-decoration:none">{nt}</a></h2><a class="textlink" href="{nh}">{read}</a></div>
</div>
</main>
<footer style="margin-top:80px"><div class="wrap"><span>© 2026 {"Maryam Jaberi" if L == "en" else "مریم جابری"}</span><a class="textlink ltr" href="mailto:{MAIL}">{MAIL}</a></div></footer>
{SCRIPT}
</body>
</html>
''')
    return "\n".join(out)


def main():
    (ROOT / "fa/case").mkdir(parents=True, exist_ok=True)
    (ROOT / "case").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(home_page(EN), encoding="utf-8")
    (ROOT / "fa/index.html").write_text(home_page(FA), encoding="utf-8")
    for slug in CASES:
        (ROOT / f"case/{slug}.html").write_text(case_page(slug, "en"), encoding="utf-8")
        (ROOT / f"fa/case/{slug}.html").write_text(case_page(slug, "fa"), encoding="utf-8")
    print("built: index.html, fa/index.html, case/*, fa/case/*")


if __name__ == "__main__":
    main()
