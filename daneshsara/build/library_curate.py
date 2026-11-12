# -*- coding: utf-8 -*-
"""Curate every readable thing into one library: python3 build/library_curate.py → data/library/library.json
Inputs: data/library/collection.json (catalogued files), books.json (assessed books), build/lectures/*.json (books read and
lecture series), psy/tools/library.html (psy reading list), psy/lessons (course booklets), data/library/halls.json (taxonomy).
Fixes shelving, merges multi-volume sets and duplicate copies into one item, and never publishes Drive ids."""
import json, glob, os, re, collections, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(HERE + '/..')
load = lambda p: json.load(open(p, encoding='utf-8'))
COL = load(f'{R}/data/library/collection.json')
BOOKS = {b['drive']: b for b in load(f'{R}/data/library/books.json')}
HALLS = load(f'{R}/data/library/halls.json')
SHELF_OK = {(h['id'], s['id']) for h in HALLS for d in h['cases'] for s in d['shelves']}

FA_D = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
EN_D = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
ORD = {'اول': 1, 'یکم': 1, 'نخست': 1, 'یک': 1, 'دوم': 2, 'دو': 2, 'سوم': 3, 'سه': 3, 'چهارم': 4, 'پنجم': 5, 'ششم': 6, 'هفتم': 7, 'هشتم': 8, 'نهم': 9, 'دهم': 10,
       'یازدهم': 11, 'دوازدهم': 12, 'سیزدهم': 13, 'چهاردهم': 14, 'پانزدهم': 15, 'شانزدهم': 16, 'هفدهم': 17, 'هجدهم': 18, 'نوزدهم': 19, 'بیستم': 20}
def norm(s):
    s = s.replace('ي', 'ی').replace('ك', 'ک').replace('ۀ', 'ه').replace('ة', 'ه').replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('‌', '').replace('ـ', '').replace('\u0654', '')
    return re.sub(r'[\s_\-–—.,،؛;:!؟?()\[\]«»"\'`☆@]+', '', s).lower()

# ---------------------------------------------------------------- manual knowledge
# index → hall:shelf for items the old catalogue put on the wrong shelf, or that had no shelf
MOVE = {
 7: 'adab:novel', 59: 'honar:skills', 62: 'adab:criticism', 168: 'phil:modern', 173: 'tarikh:islamic-dyn', 197: 'adab:satire', 198: 'tarikh:islamic-early',
 608: 'tarikh:modern-pahlavi', 749: 'tarikh:world-c20', 628: 'adab:poetry', 313: 'honar:art', 545: 'phil:nietzsche', 259: 'tarikh:world-civ',
 712: 'soc:ideology', 713: 'soc:dictatorship', 732: 'adab:novel', 600: 'tarikh:islamic-early', 227: 'tarikh:islamic-early', 161: 'tarikh:islamic-early',
 167: 'psy:psychoanalysis', 221: 'soc:culture', 176: 'phil:political', 475: 'soc:democracy', 562: 'adab:novel', 566: 'adab:novel', 22: 'din:mystic',
 59: 'honar:skills', 242: 'phil:contemporary', 212: 'tarikh:world-regions', 292: 'tarikh:modern-constitutional', 427: 'phil:nietzsche', 448: 'adab:novel', 664: 'psy:popular',
 692: 'zaban:lang', 513: 'honar:skills', 325: 'psy:popular', 298: 'soc:gender', 88: 'tarikh:memoir', 23: 'phil:nietzsche', 164: 'tarikh:memoir',
 658: 'psy:popular', 743: 'din:world', 335: 'tarikh:world-regions', 550: 'tarikh:world-regions', 580: 'tarikh:memoir', 681: 'tabar:evolution',
 705: 'tarikh:world-civ', 721: 'tarikh:modern-kasravi', 744: 'tarikh:general-social', 718: 'adab:novel', 443: 'adab:novel', 512: 'adab:criticism',
 217: 'tarikh:memoir', 625: 'adab:novel', 341: 'tarikh:world-civ', 103: 'honar:art', 120: 'honar:art', 31: 'miyan:sciencehist', 56: 'tabar:evolution',
 28: 'miyan:bighist', 667: 'miyan:bighist', 110: 'miyan:bighist', 520: 'phil:contemporary', 277: 'phil:contemporary', 219: 'phil:modern',
 186: 'soc:ideology', 578: 'din:myth', 631: 'tarikh:world-civ', 649: 'tarikh:general-social', 747: 'tarikh:world-regions', 386: 'tarikh:world-civ',
 70: 'tarikh:world-regions', 94: 'tarikh:travel', 153: 'tarikh:travel', 318: 'tabar:evolution', 69: 'tarikh:world-civ', 659: 'tarikh:world-civ',
 138: 'tarikh:ancient-empires', 204: 'tarikh:ancient-empires', 238: 'tarikh:ancient-empires', 392: 'tarikh:modern-pahlavi', 185: 'tarikh:modern-pahlavi',
 157: 'tarikh:modern-revolution', 485: 'tarikh:modern-pahlavi', 486: 'tarikh:modern-pahlavi', 487: 'tarikh:modern-pahlavi', 488: 'tarikh:modern-pahlavi',
 490: 'tarikh:modern-pahlavi', 492: 'tarikh:modern-pahlavi', 496: 'tarikh:modern-pahlavi', 498: 'tarikh:modern-pahlavi', 268: 'din:world', 717: 'din:world',
 662: 'honar:skills', 676: 'honar:skills', 738: 'honar:skills', 48: 'soc:gender', 281: 'soc:gender', 554: 'soc:gender', 750: 'soc:gender', 728: 'adab:shahnameh',
 746: 'din:quran', 139: 'tarikh:ancient-empires', 272: 'tarikh:ancient-empires', 243: 'tarikh:ancient-empires', 26: 'adab:novel', 455: 'din:superst',
 395: 'psy:popular', 273: 'din:mystic', 381: 'adab:shahnameh', 90: 'phil:logic', 408: 'phil:contemporary', 389: 'phil:political', 415: 'psy:social',
 627: 'din:mystic', 576: 'tarikh:modern-revolution', 134: 'soc:dictatorship', 465: 'tarikh:modern-pahlavi', 559: 'tabar:genetics', 561: 'tabar:genetics',
 594: 'din:shia', 573: 'din:myth', 18: 'phil:logic', 241: 'psy:popular', 257: 'psy:popular', 451: 'honar:skills', 694: 'phil:political',
 8: 'soc:democracy', 108: 'phil:modern', 175: 'soc:ideology', 205: 'soc:culture', 236: 'tarikh:travel', 321: 'tarikh:travel', 323: 'tarikh:travel',
 585: 'tarikh:modern-pahlavi', 592: 'soc:dictatorship', 618: 'tarikh:modern-pahlavi', 619: 'miyan:cosmos', 624: 'soc:econ', 641: 'phil:contemporary',
 646: 'din:quran', 704: 'din:quran', 707: 'adab:novel', 719: 'soc:gender', 734: 'honar:skills', 130: 'din:shia', 224: 'phil:contemporary',
 52: 'phil:political', 225: 'phil:political', 226: 'phil:contemporary', 419: 'phil:political', 6: 'psy:cognition', 654: 'psy:cognition', 5: 'psy:bodymind',
 27: 'psy:bodymind', 81: 'psy:bodymind', 182: 'psy:bodymind', 682: 'psy:bodymind', 684: 'psy:bodymind', 685: 'psy:bodymind', 383: 'psy:therapy', 660: 'psy:emotion',
 211: 'psy:compassion', 653: 'psy:popular', 666: 'psy:therapy', 688: 'psy:cognition', 689: 'psy:social', 284: 'psy:popular', 442: 'psy:popular',
 99: 'psy:popular', 105: 'psy:bodymind', 65: 'psy:culture', 12: 'psy:bodymind', 13: 'psy:bodymind', 15: 'psy:bodymind', 302: 'psy:popular', 500: 'psy:psychoanalysis',
 111: 'psy:psychoanalysis', 245: 'psy:psychoanalysis', 330: 'psy:psychoanalysis', 473: 'psy:psychoanalysis', 569: 'psy:cognition',
 66: 'tabar:bio', 184: 'tabar:bio', 621: 'tabar:bio', 223: 'tabar:bio', 206: 'miyan:sciencehist', 21: 'zaban:lang',
 115: None, 33: 'dup:25', 404: 'dup:50', 471: 'dup:57', 633: 'dup:266', 597: 'dup:457', 634: 'dup:477', 727: 'dup:693', 659: 'dup:69', 667: 'dup:28',
 474: 'dup:24', 308: 'dup:25', 272: 'dup:139', 243: 'dup:139', 155: 'dup:23', 688: 'psy:cognition',
}
# indices with no usable title/content: kept in the reception, not in halls
UNKNOWN = {3, 86, 151, 158, 235, 270, 274, 291, 338, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 739, 751}
# manual series: base key → (title, author); items are matched by index → (series key, volume)
SER = {
 'durant': ('تاریخ تمدن', 'ویل دورانت'), 'copleston': ('تاریخ فلسفه', 'فردریک کاپلستون'), 'capital': ('سرمایه', 'کارل مارکس'),
 'zarrin-after': ('تاریخ ایران بعد از اسلام', 'عبدالحسین زرین‌کوب'), 'jame': ('تاریخ جامع ایران', 'گروهی از نویسندگان (مرکز دائرةالمعارف بزرگ اسلامی)'),
 'chardin': ('سیاحت‌نامهٔ شاردن', 'ژان شاردن'), 'sokhan': ('فرهنگ بزرگ سخن', 'حسن انوری'), 'tosifi': ('فرهنگ توصیفی تاریخ ایران', ''),
 'tf-iran': ('تاریخ و فرهنگ ایران', ''), 'dah-hezar': ('تاریخ ده هزار ساله ایران', 'عبدالعظیم رضایی'), 'iran-ingilis': ('تاریخ روابط سیاسی ایران و انگلیس', 'محمود محمود'),
 'satarkhan': ('حماسهٔ ستارخان', ''), 'sharq': ('شرق بهشت', 'جان اشتاین‌بک'), 'teatr': ('تاریخ تئاتر جهان', 'اسکار براکت'), 'ghool': ('چگونه انسان غول شد', 'م. ایلین و ی. سگال'),
 'takamol': ('داستان تکامل انسان', ''), 'jahan-bastan': ('تاریخ جهان باستان', ''), 'donya-ghadim': ('تاریخ دنیای قدیم', ''), 'kamel': ('تاریخ کامل ابن اثیر', 'ابن اثیر'),
 'salibi': ('تاریخ جنگ‌های صلیبی', ''), 'mad': ('تاریخ ماد و هخامنشی', 'سرفراز'), 'kord': ('حرکت تاریخی کرد به خراسان', 'کلیم‌الله توحدی'),
 'khorasan-bakhtiari': ('از خراسان تا بختیاری', 'هانری رنه دالمانی'), 'zist-pasnegar': ('روان‌شناسی زیست پس‌نگر', ''), 'physicists': ('فیزیکدانان بزرگ', ''),
 'kohan-diar': ('کهن دیار', 'علی حصوری'), 'khanlari': ('تاریخ زبان فارسی', 'پرویز ناتل خانلری'), 'elam': ('تاریخ و تمدن عیلام', 'یوسف مجیدزاده'),
 'zell': ('خاطرات ظل‌السلطان', 'مسعود میرزا ظل‌السلطان'), 'reich': ('ظهور و سقوط رایش سوم', 'ویلیام شایرر'), 'herodot': ('تاریخ هرودوت', 'هرودوت'),
 'yaqubi': ('تاریخ یعقوبی', 'ابن واضح یعقوبی'), 'farhangname': ('فرهنگ‌نامهٔ شعری', 'رحیم عفیفی'), 'tire': ('تیره‌های ایرانی', ''), 'ayat': ('آیات شیطانی', 'سلمان رشدی'),
 'tanha': ('تنها پیامبر', ''), 'tragedy-dem': ('تراژدی دموکراسی در ایران', ''), 'fascism': ('فاشیسم و دیکتاتوری', 'نیکوس پولانزاس'), 'marz-vahshat': ('در مرز وحشت', ''),
 'genocide': ('نسل‌کشی ایرانیان', ''), 'mohammad-sazi': ('پروژهٔ محمدسازی', ''), 'razha': ('رازهای سرزمین من', 'رضا براهنی'), 'goft': ('گفت و شنید', 'احمد کسروی'),
 'khaterat-man': ('کتاب خاطرات من یا روشن شدن تاریخ صد ساله', ''), 'yahud': ('تاریخ یهود ایران', 'حبیب لوی'), 'totalitar': ('توتالیتاریسم', 'هانا آرنت'),
 'qowm': ('قوم‌های کهن ایرانی', ''), 'dabestan-iran': ('دانشنامهٔ ایران باستان', 'هاشم رضی'),
}
SERIDX = {}
def ser(key, pairs):
    for i, v in pairs: SERIDX[i] = (key, v)
ser('durant', [(46, 1), (44, 2), (43, 3), (45, 4)])
ser('copleston', [(369, 1), (371, 2), (376, 3), (4, 4), (394, 5), (398, 6), (399, 7), (401, 8), (400, 9)])
ser('capital', [(107, 1), (101, 2), (71, 3), (60, 4)])
ser('zarrin-after', [(126, 1), (123, 2), (128, 3), (118, 4), (124, 5), (122, 6), (119, 7)])
ser('jame', [(49, 1), (135, 2), (144, 3), (140, 4), (160, 5), (163, 6), (166, 7), (169, 8), (171, 9), (170, 10), (174, 11), (180, 12), (193, 13), (190, 14), (192, 15), (195, 16), (196, 17), (208, 18), (511, 19), (516, 20)])
ser('chardin', [(237, 1), (239, 2), (252, 3), (240, 4), (253, 5), (247, 6), (249, 7), (244, 8), (248, 9), (246, 10)])
ser('sokhan', [(327, 1), (454, 2), (462, 3), (479, 4), (467, 5), (481, 6), (464, 7), (483, 8), (328, 9)])
ser('tosifi', [(353, 1), (352, 2), (351, 3), (350, 4), (349, 5)])
ser('tf-iran', [(357, 1), (356, 2), (358, 3), (361, 4), (362, 5), (360, 6)])
ser('dah-hezar', [(507, 1), (505, 2), (504, 3), (508, 4)])
ser('iran-ingilis', [(492, 1), (485, 2), (488, 3), (490, 4), (486, 5), (487, 6), (498, 7), (496, 8)])
ser('satarkhan', [(334, 1), (421, 2), (429, 3), (450, 4)])
ser('sharq', [(536, 1), (540, 2), (537, 3)])
ser('teatr', [(345, 1), (343, 2), (339, 3)])
ser('ghool', [(136, 1), (131, 2), (133, 3)])
ser('takamol', [(220, 1), (222, 2), (216, 3)])
ser('jahan-bastan', [(85, 1), (84, 2), (87, 3), (89, 4)])
ser('donya-ghadim', [(72, 1), (73, 2), (63, 3)])
ser('kamel', [(304, 1), (307, 2), (309, 3)])
ser('salibi', [(229, 1), (262, 2), (255, 3)])
ser('mad', [(282, 1), (484, 2), (316, 3), (278, 4), (482, 5)])
ser('kord', [(300, 4), (305, 5), (310, 6)])
ser('khorasan-bakhtiari', [(297, 1), (301, 2)])
ser('zist-pasnegar', [(15, 1), (13, 2), (12, 3)])
ser('physicists', [(82, 1), (83, 2)])
ser('kohan-diar', [(150, 1), (152, 2)])
ser('khanlari', [(93, 1), (97, 2), (98, 3)])
ser('elam', [(209, 1), (210, 3)])
ser('zell', [(156, 1), (147, 2)])
ser('reich', [(595, 1), (601, 2)])
ser('herodot', [(635, 1), (639, 2)])
ser('yaqubi', [(374, 1), (370, 2)])
ser('farhangname', [(647, 1), (643, 2), (638, 3)])
ser('tire', [(559, 1), (561, 2)])
ser('ayat', [(562, 1), (566, 2)])
ser('tanha', [(644, 1), (706, 2)])
ser('tragedy-dem', [(607, 1), (606, 2)])
ser('fascism', [(699, 1), (695, 2), (691, 0)])
ser('marz-vahshat', [(543, 3), (541, 4), (538, 5)])
ser('genocide', [(279, 1), (289, 2)])
ser('mohammad-sazi', [(16, 1), (17, 2)])
ser('razha', [(355, 1), (402, 2)])
ser('goft', [(742, 1), (745, 2)])
ser('khaterat-man', [(613, 1), (593, 2)])
ser('yahud', [(575, 1)])
ser('dabestan-iran', [(14, 1)])

# clean titles for files whose catalogue title is a transliterated filename, and titles the assessment corrected
TITLE = {
 91: 'اندیشه‌ورزی‌ها', 117: 'نبرد دین با علم', 146: 'پیدایش دولت صفوی', 161: 'فرایند اسلامی شدن ایران', 207: 'ایران و ایرانیان', 223: 'مهندسی انسان',
 265: 'فرگشت انسان', 273: 'روش‌های تائو', 290: 'فرهنگ پارسی و فرهنگ تازی', 317: 'اسرارنامهٔ عطار', 393: 'خودآموز علوم غریبه', 405: 'ایران‌زمین',
 409: 'نگاهی به زبان', 422: 'فلسفهٔ گردش هستی', 456: 'اسطورهٔ دولت', 463: 'پیدایش فاشیسم', 470: 'خاک آشنا', 518: 'کاروند کسروی', 534: 'تاریخ سامانیان: عصر طلایی ایران بعد از اسلام',
 544: 'تاریخ روم باستان', 568: 'پیش‌درآمدی بر اندیشهٔ سیاسی ایرانشهری', 602: 'نادرشاه', 611: 'زمان، مکان، جهان', 617: 'فرهنگ ایرانی در سمرقند', 625: 'خانوادهٔ آرتامانف',
 636: 'تراوش اندیشه در پیرامون فرهنگ', 649: 'تحقیقات سرحدیه', 67: 'افسانه‌های اوکراینی', 143: 'یادداشت‌های مارکز', 184: 'فیزیولوژی', 48: 'جنسیت و روان‌شناسی اجتماعی',
 0: 'چرندیات پست‌مدرن', 1: 'فلسفه در عصر تراژیک یونانیان', 40: 'آشنایی با انواع رایج مغالطه', 18: 'راز و رمز استدلال و مجاب کردن دیگران', 165: 'نبرد الیگارش‌ها',
 75: 'محاکمات نورنبرگ', 318: 'ساپینس: تاریخ مصور تولد انسان', 300: 'حرکت تاریخی کرد به خراسان', 692: 'آذری یا زبان باستان آذربایجان', 410: 'سیر غزل در شعر فارسی',
 213: 'آشنایی با مکتب‌های ادبی', 211: 'رهایی از کمال‌گرایی', 525: 'نبرد من', 41: 'تاریخ عضدی', 520: 'آینده بشر', 469: 'دموکراسی و صلح', 8: 'کتاب‌سوزی',
 108: 'مولوی، نیچه و اقبال', 175: 'توطئه‌گران بین‌المللی', 205: 'فوتبال علیه دشمن', 236: 'دیدار بلوچ', 321: 'سفرنامهٔ مازندران', 323: 'سفرنامهٔ خوزستان و مازندران',
 585: 'قحطی بزرگ', 592: 'تبت در انقلاب مائوئیستی', 618: 'دو مقاله', 619: 'این کتاب را بکارید', 624: 'از انحصارطلبی', 641: 'باغ شعور (فروهر)', 646: 'علی قتال العرب',
 704: 'دو گفتار', 707: 'گورستان زنان خیانتکار', 719: 'زنان پرده‌نشین و نخبگان جوشن‌پوش', 734: 'آشنایی با تحلیل بنیادی', 224: 'نفرین صندلی راحتی', 691: 'فاشیسم و دیکتاتوری (بخش دیگر)', 25: 'توتالیتاریسم', 139: 'قوم‌های کهن ایرانی',
}

PSY_TOPIC_HINT = {}  # filled from MOVE

def default_shelf(i, x):
    t = x['title'] + ' ' + x['file']; w, sh = x['wiki'], x['shelf']
    has = lambda *ks: any(k in t for k in ks)
    if w == 'phil' and sh == 'فلسفه و منطق':
        if has('کاپلستون', 'تاریخ فلسفه', 'فلاسفه بزرگ', 'داستان فلسفه', 'سیر اندیشه', 'الفبای فلسفه', 'کتاب کوچک فلسفه', 'شش ساعت'): return 'phil:history'
        if has('نیچه', 'زایش تراژدی', 'غروب بتها', 'سودمندی'): return 'phil:nietzsche'
        if has('مغالطه', 'استدلال', 'خطاهای ساختاری', 'تفکر زائد'): return 'phil:logic'
        if has('کانت', 'سنجش خرد', 'هگل', 'اسپینوزا', 'لاک', 'شوپنهاور', 'تاملات', 'فهم بشری', 'معیار ذوق', 'عقل در تاریخ', 'اراسموس', 'روشنگری'): return 'phil:modern'
        if has('فارابی', 'ابن سینا', 'بیرونی', 'احصاء', 'التفهیم', 'ضیافت', 'افلاطون', 'یونانیان'): return 'phil:classic'
        if has('هایک', 'باستیا', 'عدالت', 'دموکراسی', 'سندل', 'پول', 'تورم', 'خرد سیاسی', 'Kherade'): return 'phil:political'
        if has('زیست شناسی', 'واقعیت', 'یک جهان', 'zaman'): return 'phil:science'
        return 'phil:contemporary'
    if w == 'phil':
        if has('قرآن', 'محمد', 'پیامبر', 'نبی', 'غدیر', 'فرقان', 'اعداد', 'معجزات', 'نیل تا فرات', 'Omolketab', 'quran', 'qoran', 'mohamad', 'islam', 'اسلام', 'عرب قبل', 'الاصنام', 'بتهای عرب', 'آپولوژی'):
            return 'din:quran' if not has('آپولوژی') else 'phil:classic'
        if has('شیعه', 'امام زمان', 'ولایت', 'روحانی', 'آخوند', 'rohanion', 'shii', 'اسرار هزار', 'hezar'): return 'din:shia'
        if has('خدا', 'خداناباور', 'بی‌خدا', 'بیخدا', 'دین برای', 'برهان', 'طلسم', 'لاییسیته', 'nabard', 'عقاید', 'تراژدی'): return 'din:atheism'
        if has('اسطوره', 'ضحاک', 'آزتک', 'نوروز', 'اهورامزدا', 'تجسد'): return 'din:myth'
        if has('میترا', 'مزدا', 'زرتشت', 'زروان', 'مانی', 'دین ایرانی', 'خسروانی', 'Ahremane'): return 'din:iranrel'
        if has('تصوف', 'صوفیه', 'عرفان', 'تانترا', 'هرمتیک', 'Hermetic', 'غریبه', 'Gharibeh', 'کربن', 'جاودانگی', 'طلای خدایان', 'ترفند خدایان', 'پیشگویی'): return 'din:mystic'
        if has('روانشناسی دین', 'دین و روان', 'موسی', 'فروید'): return 'din:psyrel'
        if has('خرافات', 'خرافه', 'امامزاده', 'حلقه'): return 'din:superst'
        if has('ادیان'): return 'din:world'
        return 'din:atheism'
    if w == 'tarikh':
        if sh == 'ایران باستان و باستان‌شناسی':
            if has('باستان شناسی', 'پارینه', 'پیش از تاریخ', 'تپه', 'کاوش', 'زاگرس', 'سفال', 'کتیبه', 'گیرشمن', 'پاسارگارد', 'پوشاک', 'رودبار'): return 'tarikh:ancient-arch'
            if has('اساطیر', 'اژدها', 'کیانیان', 'فریدون', 'عرفان', 'ارداویراف', 'دین در ایران', 'زروان', 'مانی', 'آیین'): return 'din:iranrel'
            if has('مصر', 'چین', 'عثمانی', 'جهان باستان'): return 'tarikh:world-civ'
            return 'tarikh:ancient-empires'
        if sh == 'تاریخ ایران پس از اسلام':
            if has('عباس', 'علی', 'تازیان', 'بغداد', 'مرو', 'سامان', 'طاهر', 'صفار', 'غزنو'): return 'tarikh:islamic-early'
            return 'tarikh:islamic-dyn'
        if sh == 'تاریخ معاصر و مشروطه':
            if has('کسروی'): return 'tarikh:modern-kasravi'
            if has('مشروطه', 'ستارخان', 'اختناق', 'میرزا رضا'): return 'tarikh:modern-constitutional'
            return 'tarikh:modern-pahlavi'
        if sh == 'تاریخ ایران':
            if has('جامع', 'فرهنگ توصیفی', 'ده هزار', 'تاریخ و فرهنگ ایران', 'زرین کوب', 'روزگاران', 'iran-o', 'iran-zamin', 'تاریخ ایران.pdf'): return 'tarikh:general-survey'
            if has('هردوت', 'یعقوبی', 'عضدی'): return 'tarikh:classical'
            if has('عباس', 'تازیان', 'سامان', 'بغداد', 'samany'): return 'tarikh:islamic-early'
            if has('نادر', 'بابر', 'تبریز', 'سکه', 'سمرقند'): return 'tarikh:islamic-dyn'
            if has('انگلستان', 'المان'): return 'tarikh:world-regions'
            if has('کسروی', 'karvand', 'چاره'): return 'tarikh:modern-kasravi'
            return 'tarikh:general-social'
        if sh == 'تاریخ جهان و تمدن':
            if has('هیتلر', 'نازی', 'رایش', 'نورنبرگ', 'استالین', 'شوروی', 'پرده آهنین', 'اوپنهایمر', 'کالیگاری', 'آرلوف'): return 'tarikh:world-c20'
            if has('Kamel', 'کامل', 'salibi', 'Salibi'): return 'tarikh:classical'
            if has('ارمن', 'ارمنستان', 'آسیا', 'kord', 'پناهندگان', 'Tahgegat'): return 'tarikh:world-regions'
            return 'tarikh:world-civ'
        if sh == 'سفرنامه، خاطرات و اسناد':
            return 'tarikh:travel' if has('سفر', 'سیاحت', 'مسافرت') else 'tarikh:memoir'
    if w == 'soc':
        if sh == 'اقتصاد و طبقه':
            return 'soc:dictatorship' if has('کره شمالی', 'پیونگ') else 'soc:econ'
        if sh == 'جامعه، فرهنگ و مردم‌شناسی':
            if has('زن', 'جنس'): return 'soc:gender'
            if has('شهر', 'قوم', 'بختیاری', 'هویت قومی'): return 'soc:city'
            return 'soc:culture'
        if has('دیکتاتور', 'توتالیتار', 'توتاليتار', 'فاش', 'استبداد', 'استالین', 'طالبان', 'شوروی', 'لویاتان', 'Fashism', 'جنگل', 'اولیگارش'): return 'soc:dictatorship'
        if has('کمونیسم', 'لوتا', 'نولیبرال', 'مارکس', 'چپ', 'ایدئولوژ', 'دانستنی', 'Genocide', 'نسل کشی'): return 'soc:ideology'
        if has('چرا ملت', 'عقب ماند', 'توسعه', 'فساد', 'بازار', 'markets', 'نشانه'): return 'soc:development'
        return 'soc:democracy'
    if w == 'psy': return 'psy:popular'
    if w == 'tabar': return 'tabar:bio' if has('پزشکی', 'فیزیولوژ', 'تنفس', 'physiology') else 'tabar:evolution'
    if w == 'miyan':
        if has('دانشمندان', 'تاریخ علم', 'فیزیکدانان', 'هاوکینگ', 'انیشتین', 'تجربه'): return 'miyan:sciencehist'
        if has('سرآغاز', 'همه', 'تصویر بزرگ', 'خلقت', 'اندازه'): return 'miyan:bighist'
        return 'miyan:cosmos'
    if w == 'adab':
        if has('دیوان', 'حافظ', 'صائب', 'عطار', 'غزل', 'شعری', 'attar'): return 'adab:poetry'
        if has('فردوسی', 'شاهنامه', 'نامورنامه'): return 'adab:shahnameh'
        if has('نقد', 'مکتب', 'خانلری', 'بازتاب'): return 'adab:criticism'
        if has('معراج', 'نسین'): return 'adab:satire'
        if has('فرماندهان', 'یگان'): return 'soc:ideology'
        if has('جغرافیای نظامی'): return 'tarikh:modern-pahlavi'
        if has('امام زمان'): return 'din:shia'
        return 'adab:novel'
    if w == 'zaban': return 'phil:contemporary' if has('رمزپردازی') else 'zaban:lang'
    if w == 'marja': return 'zaban:dict'
    if w == 'other': return 'honar:art' if sh.startswith('هنر') and not has('ارتباط', 'نویسندگی', 'تجسم', 'شهود', 'استدلال') else 'honar:skills'
    return None

def vol_from(title, file):
    m = re.search(r'(?:جلد|ج|بخش|vol\.?|part)\s*[\(\[]?\s*([0-9۰-۹]+)', title + ' ' + file, re.I)
    if m: return int(m.group(1).translate(EN_D))
    for k, v in sorted(ORD.items(), key=lambda kv: -len(kv[0])):
        if re.search(r'جلد\s*' + k + r'\b', title): return v
    m = re.search(r'[\s_\-]([0-9۰-۹]{1,2})\s*(?:\(\d\))?\.\w+$', file)
    return int(m.group(1).translate(EN_D)) if m else None

def clean_title(i, x):
    if i in TITLE: return TITLE[i]
    b = BOOKS.get(x['id'])
    t = b['title'] if b else x['title']
    t = re.split(r'\s*\((?:عنوان از نام فایل|عنوان فایل|عنوان دقیق|نام فایل)', t)[0]
    t = re.sub(r'\s*(AVAYEBUF|avayebuf|Tarikhema|tarikhem|karnil|bookhapdf|www\.\S+|کتابکده سلامت روان)[\w. ]*', '', t)
    t = re.sub(r'^\d{3,}\s*(کتاب)?\s*', '', t).strip(' -_.')
    return t

items = {}   # key → item
order = []
def add(key, it):
    if key not in items: items[key] = it; order.append(key)
    return items[key]

unknown = []; excluded = []
for i, x in enumerate(COL):
    mv = MOVE.get(i, 'auto') if i in MOVE else 'auto'
    if i in MOVE and MOVE[i] is None: excluded.append(x['title']); continue
    if x['ext'] not in ('pdf', 'epub', 'PDF', 'Pdf') and x['ext'].lower() not in ('pdf', 'epub', 'djvu'): excluded.append(x['title']); continue
    if i in UNKNOWN: unknown.append({'t': x['title'] or x['file'], 'f': x['file']}); continue
    b = BOOKS.get(x['id'])
    if isinstance(mv, str) and mv.startswith('dup:'): continue
    shelf = mv if mv != 'auto' else default_shelf(i, x)
    hall = shelf.split(':')[0] if shelf else 'reception'
    if i in SERIDX:
        sk, v = SERIDX[i]; st, au = SER[sk]
        it = add(sk, {'id': sk, 't': st, 'a': au, 'hall': hall, 'shelf': shelf, 'kind': 'set', 'vols': [], 'wiki': x['wiki']})
        vt = clean_title(i, x) if b else (f'{st}، جلد {str(v).translate(FA_D)}' if v else f'{st} (بخش دیگر)')
        it['vols'].append({'v': v, 'title': vt, 'read': bool(b), 'mb': round(x['size'] / 1024 / 1024, 1), 'i': i})
        if b and not it.get('tier'): it['tier'] = b['tier']
        if b: it.setdefault('assess', []).append(i)
        continue
    key = f'c{i}'
    it = add(key, {'id': hashlib.md5(x['id'].encode()).hexdigest()[:8], 't': clean_title(i, x), 'a': (b or {}).get('author', ''), 'hall': hall, 'shelf': shelf, 'kind': 'book',
                   'vols': [], 'wiki': x['wiki'], 'mb': round(x['size'] / 1024 / 1024, 1), 'i': i})
    if b: it['tier'] = b['tier']; it['assess'] = [i]

# duplicates as extra copies
for i, mv in MOVE.items():
    if isinstance(mv, str) and mv.startswith('dup:'):
        t = int(mv[4:]); key = SERIDX[t][0] if t in SERIDX else f'c{t}'
        if key in items: items[key]['copies'] = items[key].get('copies', 1) + 1
        b = BOOKS.get(COL[i]['id'])
        if b and key in items: items[key].setdefault('assess', []).append(i)

# assessment details from books.json
def assessment(i):
    b = BOOKS.get(COL[i]['id'])
    if not b: return None
    ents = [[e['t'], e['u']] for e in b['entries'] if os.path.exists(f"{R}/data/{e['u'].split('/')[0]}/concepts/{e['id']}.json")][:10]
    return {'y': b['year'], 'ty': b['type'], 'tier': b['tier'], 'dec': b['decision'], 'lab': b['label'], 'best': b['best'], 'cau': b['cautions'][:3], 'why': b.get('why', ''), 'en': ents}
for it in items.values():
    if not it: continue
    if it.get('assess'):
        a = assessment(it['assess'][0])
        if a: it['as'] = a
        it['en'] = sorted({tuple(e) for i in it['assess'] for e in (assessment(i) or {}).get('en', [])})[:12]
    it['vols'].sort(key=lambda v: v['v'])
    for v in it['vols']: v.pop('i', None)
    it.pop('assess', None); it.pop('i', None)
    if it['a'] in ('نامشخص', None): it['a'] = ''

# ---------------------------------------------------------------- psy reading list (from psy/tools/library.html)
s = open(f'{R}/psy/tools/library.html', encoding='utf-8').read()
body = s[s.index('window.BOOKS ='):]; body = body[:body.index('];') + 1]
body = re.sub(r'/\*.*?\*/', '', body[body.index('['):], flags=re.S)
body = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', body)
body = re.sub(r',\s*([\]}])', r'\1', body)
PSYB = json.loads(body)
psy_by_norm = {}
for b in PSYB:
    key = 'p-' + b['k']
    it = add(key, {'id': key, 't': b['fa'], 'en': b.get('en', ''), 'a': b.get('au', ''), 'hall': 'psy', 'shelf': 'psy:' + b['t'], 'kind': 'book', 'vols': [], 'wiki': 'psy',
                   'y': b.get('y'), 'lv': b.get('lv'), 'pk': b.get('kind'), 'd': b.get('d', ''), 'page': b.get('p')})
    psy_by_norm[norm(b['fa'])] = key
# drive copies of psy-list books become copies, not separate books
for k in list(order):
    it = items.get(k)
    if it and it['hall'] == 'psy' and not k.startswith('p-') and norm(it['t']) in psy_by_norm:
        tgt = items[psy_by_norm[norm(it['t'])]]; tgt['inrepo'] = True
        if it.get('as'): tgt['as'] = it['as']
        items[k] = None

# ---------------------------------------------------------------- psy course booklets
LES = []
for f in sorted(glob.glob(f'{R}/psy/lessons/s*.html'), key=lambda p: int(re.search(r's(\d+)', p).group(1))):
    n = int(re.search(r's(\d+)', f).group(1)); tt = re.search(r'<title>([^<|]+)', open(f, encoding='utf-8').read()).group(1).strip()
    LES.append({'v': n, 'title': tt, 'u': f'../psy/lessons/s{n}.html'})
add('psy-course', {'id': 'psy-course', 't': 'جزوهٔ دورهٔ مهارت‌های فردی و انسانی', 'a': 'ویکی روان (از درس‌گفتارهای دوره)', 'hall': 'psy', 'shelf': 'psy:course', 'kind': 'booklet', 'vols': LES, 'wiki': 'psy'})

# ---------------------------------------------------------------- lectures and books read in the wikis (build/lectures)
WMAP = {'soc': 'soc', 'phil': 'phil', 'psy': 'psy', 'tabar': 'tabar', 'tarikh': 'tarikh'}
series = collections.OrderedDict()
SRCS = load(f'{R}/core/sources.json')
NS = {k: norm(v['cite']) for k, v in SRCS.items()}
BYSRC = collections.defaultdict(list); CT = {}
for f in glob.glob(f'{R}/data/*/concepts/*.json'):
    c = load(f); w0, sl = c['id'].split(':'); CT[c['id']] = (c['title']['fa'], f'{w0}/#{sl}')
    for k in c.get('sources') or []: BYSRC[k].append(c['id'])
by_norm = {norm(it['t']): k for k, it in items.items() if it}
attached = 0
for f in sorted(glob.glob(f'{R}/build/lectures/*.json')):
    d = load(f); ents = d.get('entries') or []
    ws = collections.Counter(e.get('wiki') for e in ents if e.get('wiki') in WMAP)
    links = [[e['title']['fa'], f"{e['wiki']}/#{e['id']}"] for e in ents if e.get('wiki') in WMAP and os.path.exists(f"{R}/data/{e['wiki']}/concepts/{e['id']}.json")][:8]
    if d.get('book'):
        bt = d['book'].get('title', ''); nb = norm(re.split(r'\s*\(', bt)[0])
        k = by_norm.get(nb) or next((kk for nn, kk in by_norm.items() if nb and len(nb) > 6 and (nb in nn or nn in nb)), None)
        if k and items.get(k):
            it = items[k]; it['en'] = sorted({tuple(e) for e in (it.get('en') or [])} | {tuple(e) for e in links})[:12]; attached += 1
        continue
    title = d.get('lecture', '').strip()
    head = norm(title.split('|')[0])[:28]
    ks = [k for k, v in NS.items() if head and head in v]
    if ks:
        wc = collections.Counter(w for k in ks for w in SRCS[k].get('wikis', []) if w in WMAP)
        cs = sorted({c for k in ks for c in BYSRC.get(k, [])})
        links = [[CT[c][0], CT[c][1]] for c in cs][:10]
        w = wc.most_common(1)[0][0] if wc else (ws.most_common(1)[0][0] if ws else 'soc')
    else:
        w = ws.most_common(1)[0][0] if ws else 'tabar'
    if not ks and not ws:   # a paper or scholarly book summarised for the tabar wiki
        add('P-' + hashlib.md5(title.encode()).hexdigest()[:8], {'id': 'P-' + hashlib.md5(title.encode()).hexdigest()[:8], 't': title, 'a': d.get('speaker', ''), 'hall': 'tabar', 'shelf': 'tabar:papers',
            'kind': 'paper', 'vols': [], 'wiki': 'tabar', 'd': (d.get('summary_of_lecture_fa') or '')[:300], 'en': links})
        continue
    base = re.split(r'\s*\(', title.split('|')[0])[0]
    base = re.sub(r'[\s،,:]*(?:جلسه|قسمت|بخش|اپیزود)[\s\S]*$', '', base)
    base = re.sub(r'[\s0-9۰-۹]+$', '', base).strip(' ،,–-') or title
    sk = 'L-' + hashlib.md5(norm(base).replace('ی', '').encode()).hexdigest()[:8]
    S = series.setdefault(sk, {'id': sk, 't': base, 'a': d.get('speaker', ''), 'hall': w, 'shelf': f'{w}:lectures', 'kind': 'lecture', 'vols': [], 'wiki': w, 'ch': d.get('channel', ''), 'en': []})
    S['vols'].append({'v': len(S['vols']) + 1, 'title': title, 'sum': (d.get('summary_of_lecture_fa') or '')[:260]})
    S['en'] = [list(x) for x in dict.fromkeys(tuple(e) for e in S['en'] + links)][:14]
for k, S in series.items():
    if S['hall'] == 'tarikh' and ('tarikh', 'lectures') not in SHELF_OK: S['shelf'] = 'tarikh:lectures'
    add(k, S)

# ---------------------------------------------------------------- write
out = [it for k in order for it in [items.get(k)] if it]
bad = [(it['t'], it['shelf']) for it in out if tuple((it['shelf'] or ':').split(':')) not in SHELF_OK]
assert not bad, bad[:20]
json.dump({'items': out, 'reception': unknown, 'excluded': len(excluded), 'source_files': len(COL)}, open(f'{R}/data/library/library.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
c = collections.Counter(it['kind'] for it in out)
print(f'library: {len(out)} items from {len(COL)} files ({dict(c)}), reception {len(unknown)}, excluded {len(excluded)}, lecture readings attached {attached}')
