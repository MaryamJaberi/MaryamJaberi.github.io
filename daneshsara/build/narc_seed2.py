# -*- coding: utf-8 -*-
"""بخش «خودشیفتگی و کنترل»، دستهٔ دوم: نقش‌های باقی‌مانده، نیروی محرکه، و اطرافیان.
python3 build/narc_seed2.py   (افزایشی)"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from seedlib import Seed, R

S = Seed('psy')
t = S.t
src = lambda c, tier=1, url=None: S.src(c, tier, url)
who = lambda l, fa, y='', n='': S.person(l, fa, y, n)
C = []
def add(id, title, summary, field='narcissism-control', points=(), links=(), people=(),
        explain=None, why=None, examples=(), try_=None, confusions=(), aliases=(), status='reviewed'):
    srcs = sorted({s for p in points for s in p.get('sources', [])})
    c = {'id': 'psy:' + id, 'kind': 'concept', 'title': title, 'aliases': list(aliases),
         'parent': 'psy:' + field, 'field': 'psy:' + field, 'summary': summary,
         'points': list(points), 'links': list(links), 'people': list(people),
         'sources': srcs, 'booklets': [], 'origin': 'narcissism-control', 'iran': None,
         'wikidata': None, 'status': status}
    for k, v in (('explain', explain), ('why', why), ('examples', list(examples)),
                 ('try', try_), ('confusions', list(confusions))):
        if v: c[k] = v
    C.append(c)
P = lambda fa, en, s=(), f=(): {'text': t(fa, en), 'sources': list(s), 'flags': list(f)}
L = lambda to, rel, fa, en: {'to': to, 'rel': rel, 'note': t(fa, en)}
def EX(fa, en, kind='everyday', label='illustration', source=None):
    e = {'kind': kind, 'label': label, 'text': t(fa, en)}
    if source: e['source'] = source
    return e

s_barb = src("Barber, B. K. (1996). Parental Psychological Control: Revisiting a Neglected Construct. Child Development, 67(6), 3296–3319.", 2)
s_stark= src("Stark, E. (2007). Coercive Control: How Men Entrap Women in Personal Life. Oxford University Press.", 3)
s_john = src("Johnson, M. P. (2008). A Typology of Domestic Violence: Intimate Terrorism, Violent Resistance, and Situational Couple Violence. Northeastern University Press.", 3)
s_gott = src("Gottman, J. M., & Levenson, R. W. (1992). Marital processes predictive of later dissolution. Journal of Personality and Social Psychology, 63(2), 221–233.", 2)
s_assor= src("Assor, A., Roth, G., & Deci, E. L. (2004). The emotional costs of parents' conditional regard. Journal of Personality, 72(1), 47–88.", 2)
s_brum = src("Brummelman, E., Thomaes, S., Nelemans, S. A., Orobio de Castro, B., Overbeek, G., & Bushman, B. J. (2015). Origins of narcissism in children. PNAS, 112(12), 3659–3662.", 2)
s_jens = src("Jensen, A. C., & Thomsen, D. K. (2024). Parental differential treatment of siblings linked with internalizing and externalizing behavior: A meta-analysis. Child Development.", 1)
s_karp = src("Karpman, S. B. (1968). Fairy Tales and Script Drama Analysis. Transactional Analysis Bulletin, 7(26), 39–43.", 3)
s_day  = src("Day, N. J. S., Townsend, M. L., & Grenyer, B. F. S. (2020). Living with pathological narcissism: a qualitative study. Borderline Personality Disorder and Emotion Dysregulation, 7, 19.", 2)
s_smith= src("Smith, C. P., & Freyd, J. J. (2014). Institutional betrayal. American Psychologist, 69(6), 575–587.", 2)
s_grij = src("Grijalva, E., Harms, P. D., Newman, D. A., Gaddis, B. H., & Fraley, R. C. (2015). Narcissism and Leadership: A Meta-Analytic Review of Linear and Nonlinear Relationships. Personnel Psychology, 68(1), 1–47.", 1)
s_sedik= src("Sedikides, C., Rudich, E. A., Gregg, A. P., Kumashiro, M., & Rusbult, C. (2004). Are normal narcissists psychologically healthy? Self-esteem matters. Journal of Personality and Social Psychology, 87(3), 400–416.", 2)
s_hepp = src("Hepper, E. G., Hart, C. M., & Sedikides, C. (2014). Moving Narcissus: Can narcissists be empathic? Personality and Social Psychology Bulletin, 40(9), 1079–1091.", 2)
s_huds = src("Hudson, N. W., Briley, D. A., Chopik, W. J., & Derringer, J. (2019). You have to follow through: Attaining behavioral change goals predicts volitional personality change. Journal of Personality and Social Psychology.", 2)
s_deci = src("Deci, E. L., & Ryan, R. M. (2000). The 'what' and 'why' of goal pursuits: Human needs and the self-determination of behavior. Psychological Inquiry, 11(4), 227–268.", 1)
s_dutt = src("Dutton, D. G., & Painter, S. (1993). Emotional attachments in abusive relationships: A test of traumatic bonding theory. Violence and Victims, 8(2), 105–120.", 2)
p_john = who("Michael P. Johnson", "مایکل پی. جانسون", "", "جامعه‌شناس؛ جداکردن «تروریسم خانگی» از «خشونت موقعیتی زوج».")
p_day  = who("Nicholas Day", "نیکلاس دی", "", "پژوهشگر بالینی؛ پژوهش کیفی روی زندگی اطرافیان افراد با خودشیفتگی آسیب‌شناختی.")

add('control-in-couple',
    title=t("در رابطهٔ زوج", "Control in a couple", "Controle in een relatie"),
    summary=t("نزدیک‌ترین رابطه، بیشترین دسترسی را می‌دهد: به وقت، پول، بدن، خواب و آبروی آدم. برای همین کنترل این‌جا بیش از هر جای دیگری کار می‌کند — و تشخیصش از «رابطهٔ پرتنش» سخت‌تر است.",
              "The closest relationship gives the most access, so control works here best and is hardest to tell from an ordinary tense relationship."),
    points=[
     P("مایکل جانسون نشان داد همهٔ خشونت‌های خانگی یک چیز نیستند: در «تروریسم خانگی» خشونت در دل یک الگوی کنترل است و تقریباً همیشه یک‌طرفه و تشدیدشونده؛ در «خشونت موقعیتی زوج» دعوایی دوطرفه است که از کنترل نمی‌آید. این دو پیامد، مسیر و راه‌حل متفاوتی دارند.",
       "Johnson distinguished intimate terrorism from situational couple violence.", [s_john], ['contested']),
     P("تفاوت عملی‌شان در یک پرسش است، نه در شدت دعوا: «اگر مخالفت کنم، چه می‌شود؟» در رابطهٔ پرتنشِ معمولی، جواب «دعوا می‌شود». در رابطهٔ کنترل‌گرانه، جواب «بعدش تاوان دارد».",
       "The practical test is not the intensity of fights but what happens when you disagree.", [s_stark]),
     P("نشانه‌های زودهنگامی که در پژوهش بیشتر از بقیه برجسته‌اند: حسادت زودرس که «نشانهٔ عشق» خوانده می‌شود، فشار برای تعهد سریع، و کم‌شدن تدریجی رفت‌وآمد با خانواده و دوستان.",
       "Early markers: early jealousy framed as love, pressure for fast commitment, and shrinking outside contact.", [s_stark]),
     P("و آنچه در رابطه‌های سالم هم هست و نباید با کنترل اشتباه گرفت: دعوا، دلخوری، و حتی چهار سوار گاتمن. تفاوت در ترمیم است — در زوج‌هایی که دوام می‌آورند، بعد از خطا تلاش ترمیمی می‌آید و پذیرفته می‌شود.",
       "Healthy couples also fight; the difference is repair after rupture.", [s_gott]),
    ],
    links=[L('psy:coercive-control', 'part-of', "الگوی کلی", "The overall pattern"),
           L('psy:relationship-arc', 'explains', "چطور پیش می‌رود", "How it unfolds"),
           L('psy:gottman-horsemen', 'contrasts', "آنچه در رابطهٔ سالم هم هست", "What healthy couples also do"),
           L('psy:boundaries', 'see-also', "مرز در رابطهٔ نزدیک", "Boundaries up close")],
    people=[p_john],
    try_={'text': t("همان بیست‌وپنج جمله را برای این رابطه، یک بار از هر طرف، پر کنید.", "Fill the same twenty-five items for this relationship, once from each side."),
          'tool': 'tools/control-check.html'},
    confusions=[
     t("«هر دو مقصریم» گاهی درست است و گاهی تلهٔ خطرناکی. وقتی یک نفر از دیگری می‌ترسد، تقسیم مساوی تقصیر، بار را روی کسی می‌گذارد که کمتر قدرت دارد.",
       "'We are both to blame' is sometimes true and sometimes a dangerous trap."),
    ])

add('control-in-parenting',
    title=t("در نقش والد", "Control in parenting", "Controle in het ouderschap"),
    summary=t("سخت‌ترین نقش برای دیدن خود، چون نیت تقریباً همیشه خوب است. تفاوت در این است که قاعده می‌گذاریم یا خودِ پیوند را گرو می‌گذاریم.",
              "The hardest role to see yourself in, because the intention is almost always good."),
    points=[
     P("قاعده گذاشتن و نظارت کردن، کنترل روان‌شناختی نیست و در پژوهش‌ها با مشکلات کمتر همراه است. آنچه آسیب می‌زند، کنترلی است که به دنیای درونی کودک کار دارد: احساس گناه، دریغ محبت، بی‌اعتبار کردن احساس، و حملهٔ شخصی.",
       "Behavioural control is not psychological control; the latter targets the child's inner world.", [s_barb]),
     P("ستایش هم دو نوع است. گرما («دوستت دارم، از بودن با تو لذت می‌برم») عزت‌نفس می‌سازد؛ ارزش‌گذاری اغراق‌آمیز («تو از همهٔ بچه‌ها بهتری») خودشیفتگی. این دو در یک پژوهش طولی روی ۵۶۵ کودک، دو مسیر کاملاً جدا بودند.",
       "Warmth builds self-esteem; overvaluation builds narcissism — two separate paths.", [s_brum]),
     P("توجه مشروط، یعنی محبتی که با عملکرد می‌آید و با شکست می‌رود، در فرزندان خودارزشی نوسانی و خشم پنهان می‌سازد. نکته این است که انتظار بالا مشکلی ندارد؛ نوسانِ محبت مشکل دارد.",
       "Conditional regard, not high expectations, produces fluctuating self-worth and resentment.", [s_assor]),
     P("و چیزی که والدها کمتر به آن فکر می‌کنند: تفاوت رفتار با فرزندان. در فراتحلیل ۴۳ نمونه، فرزندی که کمتر مورد لطف است مشکلات بیشتری دارد، و هرچه فاصلهٔ رفتار بیشتر باشد اثر بزرگ‌تر است.",
       "Parental differential treatment: the less-favoured child shows more problems.", [s_jens]),
    ],
    links=[L('psy:psychological-control', 'part-of', "سازوکار", "The mechanism"),
           L('psy:narcissism-origins', 'explains', "ستایش در برابر گرما", "Praise versus warmth"),
           L('psy:breaking-cycle', 'see-also', "اگر خودتان این‌طور بزرگ شده‌اید", "If you were raised this way"),
           L('psy:children-of-narcissists', 'see-also', "از نگاه فرزند", "From the child's side")],
    explain=t("سه جملهٔ جایگزین که کل فرق را نشان می‌دهد:\n\n«اگر دوستم داشتی این کار را نمی‌کردی» ← «این کار را دوست ندارم و باید دربارهٔ آن حرف بزنیم. ناراحتی من ربطی به دوست‌داشتنت ندارد.»\n\n«تو از همهٔ بچه‌ها بااستعدادتری» ← «سخت بود و تو ادامه دادی.»\n\n«تا نمره‌ات درست نشود با تو حرف نمی‌زنم» ← «از این نمره نگرانم. بنشینیم ببینیم کجایش سخت بود.»\n\nهیچ‌کدام از این‌ها سهل‌گیری نیست. در هر سه، قاعده و انتظار سر جایش است؛ آنچه برداشته شده، گرو گذاشتنِ خودِ رابطه است.",
              "Three replacement sentences that show the whole difference."),
    try_={'text': t("یک جملهٔ تکراری خودتان را پیدا کنید و فقط همان را این هفته عوض کنید.", "Find one of your own repeated sentences and change only that this week."),
          'tool': 'tools/sentences.html'},
    confusions=[
     t("هیچ والدی همهٔ این‌ها را رعایت نمی‌کند و لازم هم نیست. در پژوهش زوج و خانواده، آنچه اهمیت دارد نسبت ترمیم به خطاست، نه نبود خطا.",
       "No parent avoids all of this; what matters is the ratio of repair to rupture."),
    ])

add('control-in-helping',
    title=t("در نقش کمک‌کننده", "Control in the helping role", "Controle in de helpende rol"),
    summary=t("درمانگر، معلم، مربی، پزشک، بزرگ‌تر خانواده، یا دوستی که همیشه مشاور است. این نقش قدرت پنهانی دارد و راحت‌ترین راه برای کنترل‌کردن بدون اینکه شبیه کنترل باشد.",
              "Therapist, teacher, coach, doctor, family elder — a role with hidden power and an easy route to control that does not look like control."),
    points=[
     P("در مثلث کارپمن، «ناجی» گوشهٔ سوم است و بدون او مثلث نمی‌چرخد: کمکِ نخواسته، این باور را محکم می‌کند که طرف مقابل خودش نمی‌توانست.",
       "The rescuer corner: unasked-for help confirms the other's incapacity.", [s_karp]),
     P("در نظریهٔ خودتعیین‌گری، سه نیاز پایه انگیزه را زنده نگه می‌دارند: خودمختاری، شایستگی و تعلق. کمکی که خودمختاری را بگیرد، در بلندمدت انگیزه را هم می‌گیرد — حتی وقتی کوتاه‌مدت کارساز است.",
       "Help that removes autonomy removes motivation, even when it works in the short term.", [s_deci]),
     P("نشانهٔ عملی در خودِ کمک‌کننده: اگر از پیشرفتِ مستقلِ طرف مقابل احساس خوبی ندارید، یا اگر نیاز دارید بدانید «بدون من چه می‌کرد»، نقش از کمک به چیز دیگری لغزیده است.",
       "A practical sign in the helper: discomfort at the other's independent progress.", [s_karp]),
     P("در سازمان‌ها همین با نام دیگری برمی‌گردد: «خیانت نهادی» یعنی وقتی نهادی که باید پشتیبان باشد، به‌جای رسیدگی به شکایت، به شاکی می‌پردازد. اثرش از خودِ آزار اولیه هم می‌تواند بیشتر باشد.",
       "Institutional betrayal: when the body that should protect turns on the complainant.", [s_smith]),
    ],
    links=[L('psy:rescuing', 'part-of', "ناجی‌گری", "Rescuing"),
           L('psy:karpman-triangle', 'part-of', "مثلث", "The triangle"),
           L('psy:boundaries', 'see-also', "مرز کمک‌کننده", "The helper's limit")],
    explain=t("چهار پرسش که این نقش را سالم نگه می‌دارد. پیش از کمک کردن:\n\n«کمک می‌خواهی یا می‌خواهی فقط گوش بدهم؟» ساده‌ترین و کم‌استفاده‌ترین جملهٔ دنیا.\n\n«تا حالا چه چیزی را امتحان کرده‌ای؟» به‌جای دادن راه‌حل، برگرداندن مسئله به دست صاحبش.\n\n«تا این‌جا من، از این‌جا تو.» مرز، نه ترک کردن.\n\n«اگر این کار را نکنم، چه حسی به من دست می‌دهد؟» این یکی برای خودتان است. اگر جواب «بی‌فایده بودن» باشد، کمک دارد نیاز شما را برآورده می‌کند، نه نیاز او را.",
              "Four questions that keep the helping role healthy."),
    examples=[
     EX("مادری که هر بار قبض فرزند بزرگسالش را می‌پردازد، چون «او بلد نیست». ده سال بعد، فرزند واقعاً بلد نیست — و مادر از این بابت هم خسته است و هم دلخور. هیچ‌کس نقشهٔ بدی نکشیده بود.",
        "A mother who always pays the bill because 'he can't' — and ten years later he genuinely cannot."),
    ])

add('drive-not-control',
    title=t("از کنترل به نیروی محرکه", "From control to drive", "Van controle naar drijfkracht"),
    summary=t("همان انرژی‌ای که در کنترل خرج می‌شود — پیگیری، دقت، جاه‌طلبی، نخواستنِ شکست — جای دیگری می‌تواند سوخت باشد. فرق در این است که روی چه چیزی اعمال شود: روی کار، یا روی آدم‌ها.",
              "The same energy spent on control — persistence, precision, ambition — can be fuel elsewhere; the difference is what it is applied to."),
    points=[
     P("در فراتحلیل رهبری، خودشیفتگی «به رهبری رسیدن» را پیش‌بینی می‌کند ولی اثربخشی را نه؛ و رابطه‌اش با اثربخشی منحنی وارونهٔ U است: دوز متوسط بهترین نتیجه را دارد.",
       "Narcissism predicts leader emergence but not effectiveness, with an inverted-U for effectiveness.", [s_grij]),
     P("یافتهٔ تندتری هم هست: وقتی عزت‌نفس را کنار بگذاریم، آنچه از «خودشیفتگی سازگارانه» باقی می‌ماند بسیار کم است. یعنی بخش مفیدِ ماجرا، بیشترش همان عزت‌نفس است، نه برتری‌جویی.",
       "Once self-esteem is controlled for, little of 'adaptive narcissism' remains.", [s_sedik]),
     P("و خبر عملی: همدلی در خودشیفتگی خاموش است، نه غایب. در سه آزمایش، دستور صریح «خودت را جای او بگذار» هم همدلی خودگزارشی و هم پاسخ ضربان قلب را تغییر داد. پس این عضله هست؛ فقط به کار گرفته نمی‌شود.",
       "A perspective-taking instruction raised both self-reported empathy and heart-rate response.", [s_hepp], ['unreplicated']),
     P("و دربارهٔ اینکه چطور عوض می‌شود: در پژوهش تغییر ارادی شخصیت، کسانی که چالش‌های کوچک را تمام کردند رشد نشان دادند و کسانی که پذیرفتند ولی تمام نکردند پس‌رفت. پس تصمیم بزرگ، نه؛ گام کوچکِ تمام‌شدنی، بله.",
       "Completing small challenges predicts growth; accepting but not completing predicts decline.", [s_huds]),
    ],
    links=[L('psy:healthy-narcissism', 'part-of', "کجا سوخت است", "Where it is fuel"),
           L('psy:change-possible', 'explains', "آیا عوض می‌شود", "Can it change"),
           L('psy:agency', 'see-also', "عاملیت به‌جای کنترل", "Agency instead of control")],
    explain=t("چهار جابه‌جایی که همان انرژی را نگه می‌دارد و جهتش را عوض می‌کند:\n\nپیگیریِ آدم‌ها ← پیگیریِ کار. همان دقتی که صرف چک‌کردن گوشی می‌شود، صرف یک پروژه شود.\n\n«باید درست انجام شود» ← «باید درست تعریف شود.» ریزکنترل معمولاً از مبهم‌بودن خواسته می‌آید. وقتی نتیجه روشن تعریف شود، نیازی به نظارت بر هر حرکت نیست.\n\nتحسین‌جویی ← کارِ تحسین‌برانگیز. یکی را دیگران می‌دهند یا نمی‌دهند؛ دیگری دست خودتان است.\n\nبرنده‌شدن در بحث ← برنده‌شدن مسئله. ساده‌ترین آزمونش: در پایان گفت‌وگو، چیزی حل شد یا فقط کسی کوتاه آمد؟",
              "Four shifts that keep the energy and change its direction."),
    try_={'text': t("شش نقش، و برای هر کدام تله‌های همان نقش و یک آزمایش کوچک برای این هفته.", "Six roles, each with its own traps and one small experiment."),
          'tool': 'tools/roles.html'})

add('around-them',
    title=t("اطرافیان: وقتی کسی که دوستش داریم این‌طور است", "The people around them", "De mensen eromheen"),
    summary=t("خواهر، دوست، همکار، فرزند بزرگسال. کسانی که نه در آن رابطه‌اند و نه بیرونش؛ می‌بینند و نمی‌دانند چه کنند. این مدخل برای آن‌هاست.",
              "Siblings, friends, colleagues, adult children: those who see it and do not know what to do."),
    points=[
     P("در پژوهش کیفی روی شریک‌ها و خانواده‌های افراد با خودشیفتگی آسیب‌شناختی، مضمون‌های تکراری این‌ها بودند: بی‌ثباتی و راه‌رفتن روی تخم‌مرغ، تضاد چهرهٔ بیرونی و خانگی، و تنهایی ناشی از اینکه دیگران باور نمی‌کنند.",
       "A qualitative study of relatives found recurring themes of instability, the public/private contrast, and isolation from not being believed.", [s_day]),
     P("مؤثرترین کاری که از یک اطرافی برمی‌آید، نصیحت نیست: باز نگه‌داشتن در است. کنترل با تنهایی کار می‌کند؛ هر پل بیرونی که زنده بماند، یک منبع واقعیت و یک راه برگشت است.",
       "The most useful thing an outsider can do is keep the door open, because control works through isolation.", [s_stark]),
     P("و چیزی که معمولاً نتیجهٔ عکس می‌دهد: اولتیماتوم («یا او یا ما»). این دقیقاً همان کاری است که خودِ الگو می‌کند — تنگ‌کردن دایرهٔ انتخاب — و معمولاً به قطع رابطه با شما ختم می‌شود، نه با او.",
       "Ultimatums replicate the pattern itself and usually end contact with you, not with them.", [s_stark, s_dutt]),
     P("پرسیدنِ «چرا نمی‌روی؟» هم همین اثر را دارد: پاسخش در شخصیت آن آدم نیست، در ساختار موقعیت است؛ و این پرسش فقط شرم را بیشتر می‌کند.",
       "'Why don't you leave?' adds shame; the answer lies in the structure of the situation.", [s_dutt]),
    ],
    links=[L('psy:public-private', 'explains', "چرا باور نمی‌شود", "Why it is not believed"),
           L('psy:intermittent-bond', 'explains', "چرا نمی‌رود", "Why they do not leave"),
           L('psy:leaving', 'see-also', "وقتی تصمیم گرفت", "When they decide")],
    people=[p_day],
    explain=t("پنج جمله که از یک اطرافی کاری می‌سازد:\n\n«هر وقت خواستی، من هستم.» و بعد واقعاً باشید — حتی اگر این بار هم برگشت.\n\n«آنچه تعریف کردی به نظرم سخت بود.» باور کردن، خودش مداخله است؛ در پژوهش، باور نشدن بخشی از آسیب است.\n\n«یادت هست پارسال چه گفتی؟» کمک به حافظه، بدون بحث بر سر اینکه حق با کیست.\n\n«دوست داری دربارهٔ راه‌ها حرف بزنیم یا فقط گوش بدهم؟» اجازه گرفتن پیش از مشورت.\n\nو یکی که نباید گفت: «من که گفته بودم.»",
              "Five sentences that make an outsider useful — and one that is not."),
    confusions=[
     t("باور کردن، به‌معنی قضاوت نهایی دربارهٔ آدم غایب نیست. می‌شود گفت «تجربهٔ تو را باور دارم» بدون اینکه حکمی دربارهٔ کسی صادر کنید.",
       "Believing someone's experience is not a verdict about the absent person."),
    ])

import glob
for c in C:
    json.dump(c, open(f"{R}/data/psy/concepts/{c['id'].split(':')[1]}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S.people, open(f'{R}/core/people.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S.sources, open(f'{R}/core/sources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('batch 2:', len(C), 'concepts')
