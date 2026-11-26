# -*- coding: utf-8 -*-
"""تکمیل مدخل «تغییر ممکن است» با قوی‌ترین شواهدی که در پژوهش پیدا شد
و در دور اول جا مانده بود: ارزیابی تصادفی‌شدهٔ برنامهٔ Drive، افت خودشیفتگی
در طول عمر، و مطالعهٔ طولی ۲۳ساله. افزایشی — فقط نقطه اضافه می‌کند."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from seedlib import Seed, R

S = Seed('psy'); t = S.t
drive = S.src("Hester, M., Eisenstadt, N., Ortega-Avila, A., Morgan, K., Walker, S.-J., & Bell, J. (2019/2020). "
              "Evaluation of the Drive Project — a three-year pilot to address high-risk, high-harm perpetrators of domestic abuse. "
              "University of Bristol.", 1, "https://www.bristol.ac.uk/news/2020/january/drive-programme-success.html")
orth  = S.src("Orth, U., Krauss, S., & Back, M. D. (2024). Development of narcissism across the life span: "
              "A meta-analytic review of longitudinal studies. Psychological Bulletin, 150(6), 643–665.", 1,
              "https://boris.unibe.ch/198932/1/2025-00409-001.pdf")
wet20 = S.src("Wetzel, E., Grijalva, E., Robins, R. W., & Roberts, B. W. (2020). You're still so vain: Changes in narcissism "
              "from young adulthood to middle age. Journal of Personality and Social Psychology, 119(2), 479–496.", 2,
              "https://escholarship.org/content/qt2sq3950p/qt2sq3950p.pdf")

NEW = [
 ({'fa': "قوی‌ترین شاهد موجود دربارهٔ خودِ رفتار کنترل‌گرانه از برنامه‌ای در انگلستان و ولز می‌آید که روی کسانی کار کرد که بیشترین "
         "آسیب را می‌زدند و تکرار می‌کردند: مدیریت فشردهٔ فردیِ هر پرونده، همراه با پاسخ هماهنگ میان خدمات قربانیان، پلیس، مراقبت "
         "اجتماعی کودکان، مسکن، درمان اعتیاد و سلامت روان. ارزیابی دانشگاه بریستول با طرح کنترل تصادفی و ۵۰۶ نفر میان ۱۷ تا ۸۱ سال: "
         "در میان کسانی که هر رفتار را در سطح بالا انجام می‌دادند، رفتارهای حسادت‌آمیز و کنترل‌گرانه ۷۳٪ کاهش یافت "
         "(آزار جسمی ۸۲٪، آزار جنسی ۸۸٪، تعقیب و مزاحمت ۷۵٪).", 'en': ''}, [drive], []),
 ({'fa': "دقت کنید این عدد مخصوصِ خودِ کنترل است، نه فقط خشونت جسمی — و این کمیاب است. و آنچه کار کرد یک کلاس آموزشی نبود؛ "
         "پاسخ هماهنگ میان چند نهاد بود.", 'en': ''}, [drive], []),
 ({'fa': "در مقیاس زندگی هم خودشیفتگی کاهش می‌یابد. فراتحلیل مطالعه‌های طولی با ۵۱ نمونه و ۳۷٬۲۴۷ نفر: از ۸ تا ۷۷ سالگی هر سه وجه "
         "پایین می‌روند — وجه کنش‌گرانه d=۰٫۲۸-، وجه ستیزه‌جویانه d=۰٫۴۱- و وجه روان‌رنجور d=۰٫۵۵-. آهنگ کاهش تقریباً خطی است و "
         "با سن تفاوت معناداری نمی‌کند.", 'en': ''}, [orth], []),
 ({'fa': "ولی همان فراتحلیل نیمهٔ دوم را هم می‌گوید: ثبات رتبه‌ای در بازهٔ میانگین ۱۱ سال بالا می‌ماند (۰٫۷۳، ۰٫۶۸ و ۰٫۶۰). "
         "یعنی همه پایین می‌آیند، ولی ترتیب آدم‌ها نسبت به هم تا حد زیادی همان می‌ماند. هر دو نیمه درست است.", 'en': ''}, [orth], []),
 ({'fa': "یک مطالعهٔ طولی ۲۳ساله (از ۱۸ تا ۴۱ سالگی) همین را در سطح فرد نشان داد: کاهش کلی d=۰٫۷۹- و فقط حدود ۳٪ شرکت‌کنندگان "
         "افزایش داشتند. و جالب‌تر اینکه کاهش با نقش اجتماعی گره خورده بود: سرپرستی دیگران و مشاغل کارآفرینانه با کاهش کمتر همراه "
         "بود، و بودن در یک رابطهٔ جدی با کاهش بیشتر.", 'en': ''}, [wet20], []),
 ({'fa': "پس جمع‌بندی صادقانه این است: «این آدم‌ها عوض نمی‌شوند» با شواهد نمی‌خواند. ولی تغییر خودبه‌خود، سریع یا در پاسخ به "
         "درخواستِ طرف مقابل اتفاق نمی‌افتد — در تنها جایی که اندازه گرفته شده، نتیجهٔ یک مداخلهٔ فشرده و چندنهادی بود.", 'en': ''},
  [drive, orth], ['editor-note']),
]

p = f'{R}/data/psy/concepts/change-possible.json'
c = json.load(open(p, encoding='utf-8'))
have = {q['text']['fa'][:50] for q in c['points']}
added = 0
for txt, srcs, flags in NEW:
    if txt['fa'][:50] in have: continue
    c['points'].append({'text': txt, 'sources': list(srcs), 'flags': list(flags)})
    added += 1
c['sources'] = sorted(set(c['sources']) | {s for _, ss, _ in NEW for s in ss})
json.dump(c, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S.sources, open(f'{R}/core/sources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'change-possible: +{added} points, {len(c["points"])} total, {len(c["sources"])} sources')
