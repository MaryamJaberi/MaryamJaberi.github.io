# -*- coding: utf-8 -*-
"""بخش «خودشیفتگی و کنترل» ویکی روان: مدخل‌ها، منابع و چهره‌ها.
python3 build/narc_seed.py     (افزایشی؛ فقط فایل‌های همین بخش را می‌نویسد)"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from seedlib import Seed, R

S = Seed('psy')
t = S.t
def src(c, tier=1, url=None): return S.src(c, tier, url)
def who(latin, fa, years='', note=''): return S.person(latin, fa, years, note)

C = []
def add(id, title, summary, field='narcissism-control', kind='concept', points=(), links=(), people=(),
        explain=None, why=None, examples=(), try_=None, confusions=(), aliases=(), parent=None, status='draft'):
    srcs = sorted({s for p in points for s in p.get('sources', [])})
    c = {'id': 'psy:' + id, 'kind': kind, 'title': title, 'aliases': list(aliases),
         'parent': 'psy:' + (parent or field) if (parent or field) else None,
         'field': 'psy:' + field if field else None,
         'summary': summary, 'points': list(points), 'links': list(links), 'people': list(people),
         'sources': srcs, 'booklets': [], 'origin': 'narcissism-control', 'iran': None, 'wikidata': None,
         'status': status}
    if explain: c['explain'] = explain
    if why: c['why'] = why
    if examples: c['examples'] = list(examples)
    if try_: c['try'] = try_
    if confusions: c['confusions'] = list(confusions)
    C.append(c)
def P(fa, en, srcs=(), flags=()): return {'text': t(fa, en), 'sources': list(srcs), 'flags': list(flags)}
def L(to, rel, fa, en): return {'to': to, 'rel': rel, 'note': t(fa, en)}
def EX(fa, en, kind='everyday', label='illustration', source=None):
    e = {'kind': kind, 'label': label, 'text': t(fa, en)}
    if source: e['source'] = source
    return e

# ---------------- منابع ----------------
s_karp = src("Karpman, S. B. (1968). Fairy Tales and Script Drama Analysis. Transactional Analysis Bulletin, 7(26), 39–43.", 3)
s_ted  = src("Emerald, D. (2015). The Power of TED* (The Empowerment Dynamic). Polaris Publishing.", 3)
s_barb = src("Barber, B. K. (1996). Parental Psychological Control: Revisiting a Neglected Construct. Child Development, 67(6), 3296–3319.", 2)
s_stark= src("Stark, E. (2007). Coercive Control: How Men Entrap Women in Personal Life. Oxford University Press.", 3)
s_sca  = src("Serious Crime Act 2015, section 76: controlling or coercive behaviour in an intimate or family relationship (United Kingdom).", 2, "https://www.legislation.gov.uk/ukpga/2015/9/section/76")
s_sweet= src("Sweet, P. L. (2019). The Sociology of Gaslighting. American Sociological Review, 84(5), 851–875.", 2)
s_darvo= src("Harsey, S. J., & Freyd, J. J. (2020). Deny, Attack, and Reverse Victim and Offender (DARVO): What Is the Influence on Perceived Perpetrator and Victim Credibility? Journal of Aggression, Maltreatment & Trauma, 29(8), 897–916.", 2)
s_gott = src("Gottman, J. M., & Levenson, R. W. (1992). Marital processes predictive of later dissolution. Journal of Personality and Social Psychology, 63(2), 221–233.", 2)
s_brum = src("Brummelman, E., Thomaes, S., Nelemans, S. A., Orobio de Castro, B., Overbeek, G., & Bushman, B. J. (2015). Origins of narcissism in children. PNAS, 112(12), 3659–3662.", 2)
s_brum2= src("Brummelman, E., Thomaes, S., & Sedikides, C. (2016). Separating Narcissism From Self-Esteem. Current Directions in Psychological Science, 25(1), 8–13.", 2)
s_grij = src("Grijalva, E., Harms, P. D., Newman, D. A., Gaddis, B. H., & Fraley, R. C. (2015). Narcissism and Leadership: A Meta-Analytic Review of Linear and Nonlinear Relationships. Personnel Psychology, 68(1), 1–47.", 1)
s_grij2= src("Grijalva, E., Newman, D. A., Tay, L., Donnellan, M. B., Harms, P. D., Robins, R. W., & Yan, T. (2015). Gender differences in narcissism: A meta-analytic review. Psychological Bulletin, 141(2), 261–310.", 1)
s_assor= src("Assor, A., Roth, G., & Deci, E. L. (2004). The emotional costs of parents' conditional regard. Journal of Personality, 72(1), 47–88.", 2)
s_maier= src("Maier, S. F., & Seligman, M. E. P. (2016). Learned helplessness at fifty: Insights from neuroscience. Psychological Review, 123(4), 349–367.", 2)
s_dutt = src("Dutton, D. G., & Painter, S. (1993). Emotional attachments in abusive relationships: A test of traumatic bonding theory. Violence and Victims, 8(2), 105–120.", 2)
s_paul = src("Paulhus, D. L., & Williams, K. M. (2002). The Dark Triad of personality: Narcissism, Machiavellianism, and psychopathy. Journal of Research in Personality, 36(6), 556–563.", 2)
s_icd  = src("World Health Organization (2018/2022). ICD-11, 6B41: Complex post-traumatic stress disorder.", 2, "https://icd.who.int/browse11/l-m/en#/http%3a%2f%2fid.who.int%2ficd%2fentity%2f585833559")
s_dsm  = src("American Psychiatric Association (2013). Diagnostic and Statistical Manual of Mental Disorders, 5th ed.: Narcissistic Personality Disorder.", 3)
s_stin = src("Stinson, F. S., et al. (2008). Prevalence, correlates, disability, and comorbidity of DSM-IV narcissistic personality disorder. Journal of Clinical Psychiatry, 69(7), 1033–1045.", 2)
s_jack = src("Jack, D. C. (1991). Silencing the Self: Women and Depression. Harvard University Press.", 3)
s_back = src("Back, M. D., et al. (2013). Narcissistic admiration and rivalry: Disentangling the bright and dark sides of narcissism. Journal of Personality and Social Psychology, 105(6), 1013–1037.", 2)
s_heyman= src("Heyman, R. E., & Slep, A. M. S. (2001). The hazards of predicting divorce without crossvalidation. Journal of Marriage and Family, 63(2), 473–479.", 2)
s_mill = src("Miller, J. D., Lynam, D. R., Hyatt, C. S., & Campbell, W. K. (2017). Controversies in Narcissism. Annual Review of Clinical Psychology, 13, 291–315.", 2)

# ---------------- چهره‌ها ----------------
p_karp = who("Stephen Karpman", "استیون کارپمن", "۱۹۳۷–", "روان‌پزشک آمریکایی؛ مثلث نمایشی را در ۱۹۶۸ معرفی کرد.")
p_barb = who("Brian Barber", "برایان باربر", "", "پژوهشگر رشد؛ سازهٔ «کنترل روان‌شناختی والدین» را دوباره زنده کرد.")
p_stark= who("Evan Stark", "ایوان استارک", "۱۹۴۲–۲۰۲۴", "مددکار اجتماعی و پژوهشگر؛ مفهوم «کنترل اجباری» را ساخت و بر قانون‌گذاری چند کشور اثر گذاشت.")
p_freyd= who("Jennifer Freyd", "جنیفر فرید", "۱۹۵۷–", "روان‌شناس؛ نظریهٔ «آسیب خیانت» و الگوی DARVO.")
p_gott = who("John Gottman", "جان گاتمن", "۱۹۴۲–", "پژوهشگر زوج؛ مشاهدهٔ آزمایشگاهی گفت‌وگوی زوج‌ها و پیش‌بینی جدایی.")
p_brum = who("Eddie Brummelman", "ادی بروملمن", "", "روان‌شناس رشد؛ پژوهش دربارهٔ ریشهٔ خودشیفتگی در کودکی و تفاوتش با عزت‌نفس.")
p_deci = who("Edward Deci", "ادوارد دسی", "۱۹۴۲–", "از بنیان‌گذاران نظریهٔ خودتعیین‌گری؛ پژوهش دربارهٔ توجه مشروط والدین.")
p_selig= who("Martin Seligman", "مارتین سلیگمن", "۱۹۴۲–", "روان‌شناس؛ «درماندگی آموخته‌شده» و بازنگری پنجاه‌سالهٔ آن.")
p_emer = who("David Emerald", "دیوید امرالد", "", "نویسندهٔ «مثلث توانمندسازی» به‌عنوان راه بیرون از مثلث کارپمن.")
p_jack = who("Dana Crowley Jack", "دانا کرولی جک", "", "روان‌شناس؛ نظریهٔ «خاموش‌کردن خود» و پیوندش با افسردگی زنان.")
p_sweet= who("Paige Sweet", "پیج سوئیت", "", "جامعه‌شناس؛ گازلایتینگ را به‌عنوان پدیده‌ای اجتماعی و نه فقط روان‌شناختی تحلیل کرد.")
p_mill = who("Joshua Miller", "جاشوا میلر", "", "پژوهشگر شخصیت؛ از منتقدان یکپارچه‌دیدن خودشیفتگی.")

# ================= ۱. خودِ پدیده =================
add('narcissism-control', kind='subfield', field=None, parent='psychology',
    title=t("خودشیفتگی، کنترل و رابطه", "Narcissism, control and relationships", "Narcisme, controle en relaties"),
    summary=t("مجموعه‌ای از مدخل‌ها دربارهٔ خودشیفتگی به‌عنوان یک طیف شخصیت، رفتارهای کنترل‌گرانه در هر نقشی که زندگی به ما می‌دهد، ریشه‌هایشان در کودکی، اثرشان بر تن و روان اطرافیان، و راه‌های بیرون آمدن.",
              "Entries on narcissism as a personality spectrum, controlling behaviour across life roles, its childhood roots, its toll on those nearby, and ways out."),
    status='draft')

add('narcissism',
    title=t("خودشیفتگی: یک طیف، نه یک برچسب", "Narcissism: a spectrum, not a label", "Narcisme: een spectrum, geen etiket"),
    aliases=["نارسیسیسم", "نارسیسم", "خودشیفته"],
    summary=t("خودشیفتگی صفتی است که همه کمی از آن داریم: توجه به خود، نیاز به دیده‌شدن، و دفاع از تصویر خود. آنچه فرق می‌کند شدت، انعطاف و هزینه‌ای است که برای دیگران دارد — نه اینکه کسی «خودشیفته هست یا نیست».",
              "Narcissism is a trait everyone has to some degree: self-focus, a need to be seen, and defence of one's self-image. What differs is intensity, flexibility and the cost to others — not whether someone 'is or isn't' a narcissist."),
    points=[
     P("در روان‌شناسی شخصیت، خودشیفتگی یک صفت پیوسته است و در جمعیت عادی توزیعی مثل قد دارد: بیشتر مردم وسط‌اند و کم‌شمارند کسانی که در دو سر طیف می‌ایستند.",
       "In personality psychology narcissism is a continuous trait, distributed in the general population like height.", [s_mill]),
     P("دست‌کم دو چهرهٔ متفاوت دارد که در پژوهش‌ها رفتار متفاوتی نشان می‌دهند: «بزرگ‌منشانه» (آشکار، پرمدعا، مطمئن) و «آسیب‌پذیر» (پنهان، زودرنج، آکنده از شرم). هر دو یک هستهٔ مشترک دارند: احساس استحقاق و حساسیت شدید به تصویر خود.",
       "At least two phenotypes behave differently in research: grandiose and vulnerable narcissism, sharing a core of entitlement and self-image sensitivity.", [s_mill, s_back]),
     P("بک و همکاران نشان دادند دو راهبرد جدا پشت این صفت کار می‌کند: «تحسین‌جویی» که آدم را در آغاز جذاب و پرانرژی نشان می‌دهد، و «رقابت‌جویی» که در تعارض به تحقیر و پرخاش می‌رسد. همین توضیح می‌دهد چرا آشنایی اول درخشان است و ادامه‌اش سخت.",
       "Back et al. separated admiration (initially charming) from rivalry (devaluing in conflict) — explaining the bright first impression and the difficult continuation.", [s_back]),
     P("آنچه در زندگی روزمره آزار می‌دهد معمولاً خود صفت نیست، رفتارهایی است که از آن بیرون می‌آید: کنترل، بی‌اعتبار کردن، تحقیر و وارونه‌کردن تقصیر. این رفتارها را می‌شود دید، شمرد و دربارهٔ آن‌ها تصمیم گرفت؛ درون آدم‌ها را نمی‌شود.",
       "What hurts in daily life is usually not the trait but the behaviours: control, invalidation, contempt, blame reversal — which can be observed, unlike inner states.", [s_barb, s_stark]),
    ],
    links=[L('psy:vulnerable-narcissism', 'part-of', "چهرهٔ پنهان همین صفت", "The hidden face of the same trait"),
           L('psy:narcissism-culture', 'see-also', "آیا این قرن ما را خودشیفته‌تر کرده؟", "Has this century made us more narcissistic?"),
           L('psy:npd', 'contrasts', "صفت در برابر اختلال", "Trait versus disorder"),
           L('psy:healthy-narcissism', 'contrasts', "کجای این صفت سوخت است", "Where the trait is fuel"),
           L('psy:labels-harm', 'see-also', "چرا برچسب‌زدن کار را خراب می‌کند", "Why labelling backfires")],
    people=[p_mill],
    explain=t("تصویر رایج از «خودشیفته» آدمی است که مدام از خودش تعریف می‌کند و جلوی آینه می‌ایستد. این تصویر هم ناقص است هم گمراه‌کننده. هستهٔ این صفت، نیاز شدید به نگه‌داشتن یک تصویر خاص از خود است — و کارهایی که برای نگه‌داشتن آن تصویر انجام می‌شود.\n\nاگر آن تصویر «من بهترینم» باشد، شکل بیرونی‌اش پرمدعا و پرانرژی است. اگر آن تصویر «من خاصم ولی دنیا قدر نمی‌داند» باشد، شکل بیرونی‌اش گوشه‌گیر، زودرنج و طلبکار است. هر دو وقتی تصویرشان تهدید شود واکنش تندی نشان می‌دهند؛ یکی با حمله، یکی با قهر و شکایت.\n\nبرای همین، پرسش مفید «او خودشیفته است یا نه؟» نیست. پرسش‌های مفید این‌هاست: در این رابطه چه رفتارهایی تکرار می‌شود؟ چه چیزی را از من می‌گیرد؟ چه چیزی هنوز دست من است؟",
              "The common image of a narcissist is misleading; the core is an intense need to maintain a particular self-image and what gets done to maintain it."),
    why=t("چون این کلمه در فارسی و در فضای مجازی به فحش تبدیل شده است. وقتی برچسب زده شد، فکر کردن تمام می‌شود: دیگر لازم نیست بفهمیم چه اتفاقی می‌افتد، چه چیزی آن را نگه می‌دارد و چه کاری از ما برمی‌آید. دیدنِ رفتار، برخلاف برچسب، به تصمیم ختم می‌شود.",
          "Because the word has become an insult; once the label is applied, thinking stops, while seeing behaviour leads to decisions."),
    examples=[
     EX("دو همکار در یک جلسه نقد می‌شوند. اولی سرخ می‌شود و بلند می‌گوید «شما اصلاً کار من را نخوانده‌اید»؛ دومی ساکت می‌ماند، جلسه را زود ترک می‌کند و هفته‌ها با کسی حرف نمی‌زند. از بیرون دو آدم کاملاً متفاوت‌اند؛ هر دو ممکن است یک کار می‌کنند: از تصویری که از خود دارند دفاع می‌کنند.",
        "Two colleagues criticised in a meeting: one attacks, one withdraws for weeks — both may be defending a self-image."),
     EX("یک جملهٔ آشنا در خانواده‌های ایرانی: «من که همهٔ عمرم را پای شما گذاشتم.» این جمله لزوماً از خودشیفتگی نمی‌آید؛ ولی اگر هر بار که کسی «نه» می‌گوید تکرار شود، دیگر یک خاطره نیست، یک ابزار است.",
        "A familiar family line that is not necessarily narcissism — unless it appears every time someone says no."),
    ],
    try_={'text': t("به‌جای اینکه فکر کنید طرف مقابل چه هست، یک هفته فقط بشمارید چه می‌کند: هر بار که حرفتان نیمه ماند، هر بار که احساستان غلط اعلام شد، هر بار که بعد از گفت‌وگو به حافظهٔ خودتان شک کردید. همین شمردن، تصویر را روشن‌تر می‌کند از هر تشخیصی.",
                    "Instead of guessing what the other person is, spend a week counting what they do."),
            'tool': 'tools/control-check.html'},
    confusions=[
     t("«خودشیفته» با «خودخواه» یکی نیست. خودخواهی یعنی اولویت‌دادن به منافع خود؛ خودشیفتگی یعنی نیاز به نگه‌داشتن یک تصویر از خود، حتی به قیمت منافع خود.",
       "Narcissism is not the same as selfishness."),
     t("اعتمادبه‌نفس بالا خودشیفتگی نیست. در پژوهش‌ها عزت‌نفس و خودشیفتگی دو چیز جدا هستند و حتی پیامدهای وارونه دارند.",
       "High self-esteem is not narcissism; research separates them."),
     t("هر رفتار کنترل‌گرانه از خودشیفتگی نمی‌آید. ترس، اضطراب، تربیت و فرهنگ هم همان رفتار را می‌سازند؛ و درمانشان فرق می‌کند.",
       "Not every controlling behaviour comes from narcissism."),
    ],
    status='reviewed')

add('npd',
    title=t("اختلال شخصیت خودشیفته (NPD)", "Narcissistic personality disorder", "Narcistische persoonlijkheidsstoornis"),
    aliases=["ان‌پی‌دی"],
    summary=t("تشخیص بالینی‌ای که فقط بخش کوچکی از طیف را دربر می‌گیرد: الگویی پایدار و انعطاف‌ناپذیر از بزرگ‌منشی، نیاز به تحسین و کمبود همدلی که در جاهای مختلف زندگی تکرار می‌شود و رنج یا اختلال کارکرد می‌آورد.",
              "A clinical diagnosis covering only a small part of the spectrum: a pervasive, inflexible pattern of grandiosity, need for admiration and lack of empathy."),
    points=[
     P("DSM-5 نُه ملاک می‌شمارد (از جمله احساس بزرگ‌منشی، اشتغال ذهنی به موفقیت و قدرت، باور به خاص‌بودن، نیاز به تحسین افراطی، احساس استحقاق، بهره‌کشی از دیگران، نبود همدلی، حسادت، و رفتار متکبرانه) و برای تشخیص دست‌کم پنج‌تا لازم است.",
       "DSM-5 lists nine criteria and requires at least five.", [s_dsm]),
     P("در بزرگ‌ترین پیمایش جمعیتی آمریکا، شیوع مادام‌العمر این اختلال حدود ۶ درصد برآورد شد؛ در مردان بیشتر از زنان. یعنی اکثریت کسانی که رفتار کنترل‌گرانه دارند این تشخیص را ندارند.",
       "In the US NESARC survey lifetime prevalence was about 6%, higher in men.", [s_stin]),
     P("فراتحلیل تفاوت جنسیتی نشان داد مردان در میانگین خودشیفتگی کمی بالاترند، و بیشترین تفاوت در «بهره‌کشی و احساس استحقاق» است؛ اما اندازهٔ اثر کوچک است و همپوشانی دو توزیع زیاد.",
       "A meta-analysis found men score slightly higher, mostly on exploitativeness/entitlement, with a small effect size.", [s_grij2]),
     P("تشخیص کار متخصص است و از روی رفتار بیرونی، از راه دور یا از روی شبکه‌های اجتماعی داده نمی‌شود. برای هیچ‌کس هم «حکم» نیست: تشخیص توصیف یک الگوست، نه هویت یک آدم.",
       "Diagnosis is clinical work, not something done from a distance or from social media.", [s_dsm]),
    ],
    links=[L('psy:narcissism', 'part-of', "جای این تشخیص روی طیف", "Where the diagnosis sits on the spectrum"),
           L('psy:personality-disorders', 'part-of', "خانوادهٔ اختلالات شخصیت", "The family of personality disorders"),
           L('psy:labels-harm', 'see-also', "چرا این کلمه را به کار نمی‌بریم", "Why we avoid using the word"),
           L('psy:dx', 'see-also', "طبقه‌بندی و تشخیص", "Classification and diagnosis")],
    explain=t("چیزی که این تشخیص را از صفت جدا می‌کند سه چیز است: پایداری (سال‌هاست، نه در یک دورهٔ سخت)، فراگیری (در کار و خانه و دوستی، نه فقط با یک نفر) و هزینه (برای خود فرد یا اطرافیانش رنج و اختلال کارکرد می‌آورد).\n\nنکتهٔ عملی این است: برای اینکه بدانید در یک رابطه چه می‌گذرد، به این تشخیص نیازی ندارید. رفتارها همان‌قدر آزار می‌دهند، چه تشخیص باشد چه نباشد، و کاری که از شما برمی‌آید هم تقریباً همان است.",
              "Three things separate the disorder from the trait: persistence, pervasiveness and cost. For deciding what to do, the diagnosis is not needed."),
    why=t("چون بیشترین سوءاستفاده از این کلمه همین‌جاست: یک تشخیص نادر و تخصصی تبدیل شده به برچسبی که هر کس به طرف مقابل دعوایش می‌زند.",
          "Because this rare clinical diagnosis has become an everyday insult."),
    status='reviewed')

add('healthy-narcissism',
    title=t("خودشیفتگی سالم: کجا سوخت است، کجا سم", "Healthy narcissism: fuel or poison", "Gezond narcisme"),
    summary=t("همان صفت، در دوز و جای درست، چیزی است که آدم را به میدان می‌فرستد: جرئت خواستن، تاب‌آوری در برابر طرد، و توان رهبری. مشکل از جایی شروع می‌شود که نگه‌داشتن تصویر، مهم‌تر از خود کار و خود آدم‌ها شود.",
              "The same trait in the right dose sends a person into the arena: the nerve to want, resilience to rejection, leadership. The problem starts when protecting the image outweighs the work and the people."),
    points=[
     P("در فراتحلیل گریخالوا و همکاران روی رهبری، رابطهٔ خودشیفتگی با «به رهبری رسیدن» مثبت بود اما با «رهبر خوب بودن» منحنی وارونهٔ U: دوز متوسط بهترین نتیجه را داشت و دوز بالا و پایین هر دو بدتر.",
       "In Grijalva et al.'s meta-analysis narcissism predicted leader emergence positively, but leader effectiveness followed an inverted U.", [s_grij]),
     P("عزت‌نفس و خودشیفتگی دو چیز جدا هستند، نه دو درجه از یک چیز. عزت‌نفس یعنی «من ارزشمندم»؛ خودشیفتگی یعنی «من برترم». اولی با رابطهٔ خوب و سلامت روان همراه است، دومی با پرخاش و تعارض.",
       "Self-esteem ('I am worthy') and narcissism ('I am superior') are distinct constructs with opposite correlates.", [s_brum2]),
     P("در همان پژوهش‌ها، راه ساختن عزت‌نفس هم با راه ساختن خودشیفتگی فرق دارد: گرمای واقعی و پذیرش، عزت‌نفس می‌سازد؛ ارزش‌گذاری اغراق‌آمیز و «تو از بقیه بهتری»، خودشیفتگی.",
       "Warmth builds self-esteem; overvaluation builds narcissism.", [s_brum, s_brum2]),
    ],
    links=[L('psy:narcissism', 'part-of', "همان صفت، از زاویهٔ دیگر", "The same trait, другой angle"),
           L('psy:narcissism-origins', 'explains', "چرا گرما و ارزش‌گذاری اغراق‌آمیز نتیجهٔ متفاوتی دارند", "Why warmth and overvaluation differ"),
           L('psy:assertiveness', 'see-also', "ابراز خود بدون کوچک‌کردن دیگری", "Assertion without diminishing others")],
    people=[p_brum],
    explain=t("سه چیز که از این صفت می‌آید و بدون آن‌ها زندگی سخت‌تر است:\n\n۱. <b>جرئت خواستن.</b> بالا بردن دست برای یک نقش، درخواست افزایش حقوق، شروع کاری که ممکن است شکست بخورد. کسی که هیچ اعتماد اغراق‌آمیزی به خودش ندارد، اغلب شروع هم نمی‌کند.\n\n۲. <b>تاب‌آوری در برابر طرد.</b> در پژوهش‌ها خودشیفتگی بزرگ‌منشانه با نگرانی کمتر از قضاوت دیگران همراه است. همین است که آدم بعد از ده «نه» یازدهمین در را می‌زند.\n\n۳. <b>توان ایستادن جلوی جمع.</b> رهبری در آغاز به کسی می‌رسد که مطمئن به نظر برسد.\n\nو جایی که برمی‌گردد: وقتی حفظ تصویر از کار مهم‌تر می‌شود، خبر بد بالا نمی‌رود، اشتباه پنهان می‌ماند، و آدم‌های اطراف به ابزارِ تأیید تبدیل می‌شوند. معیار ساده: <b>آیا این اعتماد به نفس به کار و آدم‌ها خدمت می‌کند یا آن‌ها به آن؟</b>",
              "Three gifts of the trait — the nerve to want, resilience to rejection, standing in front of a group — and the line where it turns."),
    examples=[
     EX("بنیان‌گذاری که در جلسهٔ سرمایه‌گذاری با اطمینان کامل از محصولی حرف می‌زند که هنوز نصفه است. همین اطمینان پول را جذب می‌کند؛ و اگر جلوی شنیدن خبر بد را هم بگیرد، همان شرکت را زمین می‌زند.",
        "A founder whose confidence attracts investment — and, if it blocks bad news, sinks the company."),
    ],
    try_={'text': t("یک تصمیم اخیرتان را بردارید و بپرسید: اگر هیچ‌کس هرگز نمی‌فهمید که این کار را من کرده‌ام، باز هم همین را انتخاب می‌کردم؟ فاصلهٔ جواب با تصمیم واقعی، اندازهٔ سهم «تصویر» است.",
                    "Take a recent decision and ask: would I choose the same if nobody ever knew it was mine?")},
    status='reviewed')

add('labels-harm',
    title=t("چرا برچسب نمی‌زنیم", "Why we don't use labels", "Waarom we geen etiketten plakken"),
    summary=t("گفتن «او خودشیفته است» حس خوبی دارد و دقیقاً همان‌جا فکر کردن را تمام می‌کند. برچسب، رفتار را توضیح نمی‌دهد، فقط اسم تازه‌ای رویش می‌گذارد — و راه تغییر را برای هر دو طرف می‌بندد.",
              "Saying 'he is a narcissist' feels good and ends the thinking. A label renames behaviour instead of explaining it."),
    points=[
     P("برچسب تشخیصی وقتی از زبان غیرمتخصص و دربارهٔ کسی که معاینه نشده به کار برود، نه اعتبار دارد و نه کمکی می‌کند؛ ولی انگ آن می‌ماند و رفتار اطرافیان را عوض می‌کند.",
       "A diagnostic label used by a non-clinician about an unexamined person carries no validity but real stigma.", [s_dsm]),
     P("جایگزین عملی، زبان رفتاری است: به‌جای «او کنترل‌گر است»، «وقتی دیر می‌کنم تا فردا جواب نمی‌دهد». جملهٔ دوم را می‌شود بررسی کرد، شمرد، و دربارهٔ آن تصمیم گرفت.",
       "The practical alternative is behavioural language, which can be checked, counted and acted on.", [s_barb]),
     P("برچسب برای خودِ آدم هم دام است: اگر رفتار از «ذات» بیاید، پس تغییر ممکن نیست و تلاشی هم لازم نیست. همین باور، هم در کسی که آسیب می‌زند و هم در کسی که آسیب می‌بیند، حرکت را متوقف می‌کند.",
       "Labels imply fixed essence, which stops effort in both parties.", [s_maier]),
    ],
    links=[L('psy:stigma', 'part-of', "انگ و برچسب‌زنی", "Stigma and labelling"),
           L('psy:npd', 'contrasts', "تشخیص واقعی چه شکلی است", "What a real diagnosis looks like"),
           L('psy:control-behaviors', 'explains', "زبان جایگزین: رفتارها", "The alternative language: behaviours")],
    confusions=[
     t("«برچسب نزنیم» یعنی «رفتار بد را نادیده بگیریم»؟ نه. دقیقاً برعکس: رفتار را دقیق‌تر و بی‌تخفیف‌تر نام می‌برد، فقط آدم را به یک کلمه تقلیل نمی‌دهد.",
       "Not labelling does not mean excusing; it means naming behaviour more precisely."),
     t("برای کسی که در رابطه‌ای آسیب دیده، پیدا کردن این کلمه گاهی اولین لحظهٔ آرامش است: «پس دیوانه نبودم.» این تجربه محترم است. نکته این است که کلمه نقطهٔ شروع باشد، نه پایان.",
       "For someone harmed, finding the word can be the first relief; the point is to make it a start, not an end."),
    ],
    status='reviewed')

# ---------------- منابع دستهٔ دوم ----------------
s_day   = src("Day, N. J. S., Townsend, M. L., & Grenyer, B. F. S. (2020). Living with pathological narcissism: a qualitative study. Borderline Personality Disorder and Emotion Dysregulation, 7, 19.", 2)
s_niel18= src("Nielsen, M. B., & Einarsen, S. V. (2018). What we know, what we do not know, and what we should and could have known about workplace bullying. Aggression and Violent Behavior, 42, 71–83.", 2)
s_niel10= src("Nielsen, M. B., Matthiesen, S. B., & Einarsen, S. (2010). The impact of methodological moderators on prevalence rates of workplace bullying: A meta-analysis. Journal of Occupational and Organizational Psychology, 83(4), 955–979.", 1)
s_braun = src("Braun, S. (2017). Leader narcissism and outcomes in organizations: A review at multiple levels of analysis. Frontiers in Psychology, 8, 773.", 2)
s_whitty= src("Whitty, M. T. (2015). Anatomy of the online dating romance scam. Security Journal, 28(4), 443–455.", 2)
s_churn = src("Halpern-Meekin, S., Manning, W. D., Giordano, P. C., & Longmore, M. A. (2013). Relationship Churning in Emerging Adulthood: On/Off Relationships and Sex With an Ex. Journal of Adolescent Research, 28(2), 166–188.", 2)
s_ander = src("Anderson, D. K., & Saunders, D. G. (2003). Leaving an abusive partner: An empirical review of predictors, the process of leaving, and psychological well-being. Trauma, Violence, & Abuse, 4(2), 163–191.", 2)
s_spear = src("Spearman, K. J., Hardesty, J. L., & Campbell, J. (2023). Post-separation abuse: A concept analysis. Journal of Advanced Nursing, 79(4), 1225–1246.", 2)
s_glass = src("Glass, N., Laughon, K., Campbell, J., et al. (2008). Non-fatal strangulation is an important risk factor for homicide of women. Journal of Emergency Medicine, 35(3), 329–335.", 2)
s_monck = src("Monckton-Smith, J. (2020). Intimate Partner Femicide: using Foucauldian analysis to track an eight stage relationship progression to homicide. Violence Against Women, 26(11), 1267–1285.", 2)
s_ho21  = src("Home Office (2021). Review of the Controlling or Coercive Behaviour Offence. London.", 2, "https://assets.publishing.service.gov.uk/media/608bdba28fa8f51b909ca167/review-of-the-controlling-or-coercive-behaviour-offence.pdf")
s_mcq   = src("McQuigg, R. J. A. (2025). Criminalizing Coercive Control: Cross-Jurisdictional Lessons. Statute Law Review, 46(1), hmaf010.", 2)
s_john  = src("Johnson, M. P. (2008). A Typology of Domestic Violence: Intimate Terrorism, Violent Resistance, and Situational Couple Violence. Northeastern University Press.", 3)
s_walk  = src("Walker, L. E. (1979). The Battered Woman. Harper & Row.", 3)
s_namn  = src("Namnyak, M., Tufton, N., Szekely, R., Toal, M., Worboys, S., & Sampson, E. L. (2008). 'Stockholm syndrome': psychiatric diagnosis or urban myth? Acta Psychiatrica Scandinavica, 117(1), 4–11.", 2)
s_strut = src("Strutzenberg, C. C., Wiersma-Mosley, J. D., Jozkowski, K. N., & Becnel, J. N. (2017). Love-bombing: A narcissistic approach to relationship formation. Discovery (University of Arkansas), 18, 81–89.", 4)
s_ameen = src("Ameen, S., et al. (2025). Narcissistic Abuse Cycle Deserves Clinical and Research Attention. Indian Journal of Psychological Medicine.", 4)
s_pill  = src("Pillemer, K. (2020). Fault Lines: Fractured Families and How to Mend Them. Avery.", 3)
s_recz  = src("Reczek, R., Stacey, L., & Thomeer, M. B. (2023). Parent–Adult Child Estrangement in the United States by Gender, Race/Ethnicity, and Sexuality. Journal of Marriage and Family, 85(2), 494–517.", 2)
s_lift  = src("Lifton, R. J. (1961). Thought Reform and the Psychology of Totalism: A Study of 'Brainwashing' in China. W. W. Norton.", 3)
s_lal   = src("Lalich, J. (2004). Bounded Choice: True Believers and Charismatic Cults. University of California Press.", 3)
s_lesi  = src("Lesiak, A., & Gelsthorpe, L. (2025). The Invisible Abuser: Attachment, Victimization, and Perpetrator Perception in Repeat Abuse. Violence Against Women.", 2)
s_bodd  = src("Boddy, C. R. (2011). Corporate Psychopaths, Bullying and Unfair Supervision in the Workplace. Journal of Business Ethics, 100(3), 367–379.", 2)

p_monck = who("Jane Monckton-Smith", "جین مانکتون-اسمیت", "", "جرم‌شناس؛ بازسازی هشت‌مرحله‌ای مسیر رابطه تا قتل همسر.")
p_whit  = who("Monica Whitty", "مونیکا ویتی", "", "روان‌شناس سایبری؛ تشریح مرحله‌به‌مرحلهٔ کلاهبرداری عاشقانهٔ آنلاین.")
p_einar = who("Stale Einarsen", "استال اینارسن", "", "پژوهشگر قلدری در محیط کار.")
p_pill  = who("Karl Pillemer", "کارل پیلمر", "", "جامعه‌شناس خانواده؛ پژوهش ملی دربارهٔ قطع رابطهٔ خانوادگی.")

# ================= ۲. کنترل: رفتارها، نه برچسب‌ها =================
add('control-behaviors',
    title=t("رفتارهای کنترل‌گرانه: فهرستی که می‌شود دید", "Controlling behaviours: a list you can actually see", "Controlerend gedrag"),
    summary=t("کنترل معمولاً با دستور آشکار کار نمی‌کند؛ با نُه دسته رفتار کار می‌کند که هر کدام به‌تنهایی قابل توجیه‌اند: بستن راه حرف، بی‌اعتبار کردن احساس، حملهٔ شخصی، احساس گناه، دریغ محبت، بی‌ثباتی، جداسازی، ریزکنترل، و ترس.",
              "Control rarely works through open orders; it works through nine classes of behaviour, each individually explainable."),
    points=[
     P("باربر در بازخوانی سازهٔ «کنترل روان‌شناختی» نشان داد که کنترل کردن احساس و فکر آدم‌ها از راه گناه، دریغ محبت و بی‌اعتبار کردن، اثری متفاوت و بدتر از کنترل رفتار دارد: اولی با مشکلات درونی‌شده (افسردگی، اضطراب، خودکم‌بینی) همراه است.",
       "Barber showed that psychological control, unlike behavioural control, is linked to internalising problems.", [s_barb]),
     P("استارک همین را در رابطهٔ بزرگسالان دید و نامش را «کنترل اجباری» گذاشت: آسیب اصلی کتک نیست، تنگ‌شدن دایرهٔ آزادی است — پول، وقت، لباس، رفت‌وآمد و ارتباط با آدم‌ها. او این را «جرم علیه آزادی» می‌نامد.",
       "Stark called the adult version coercive control: the harm is the shrinking of liberty, not primarily injury.", [s_stark]),
     P("مزیت نگاه رفتاری این است که قابل بررسی است. «او کنترل‌گر است» را نمی‌شود آزمود؛ «در این ماه چهار بار گوشی‌ام را چک کرد و دو بار قرارم با خواهرم را به هم زد» را می‌شود.",
       "Behavioural language can be checked; labels cannot.", [s_barb, s_stark]),
     P("یک هشدار لازم: هیچ‌کدام از این رفتارها به‌تنهایی نشانهٔ هیچ‌چیز نیست. همه گاهی حرف دیگری را قطع می‌کنیم یا دلخور می‌شویم. آنچه الگو می‌سازد، تکرار است، جهت یک‌طرفهٔ آن، و اینکه با گذشت زمان دایرهٔ انتخاب یک نفر تنگ‌تر شود.",
       "No single behaviour means anything; the pattern is made by repetition, one-sidedness, and a shrinking circle of choice.", [s_stark]),
    ],
    links=[L('psy:psychological-control', 'part-of', "نسخهٔ والد و فرزند", "The parent–child version"),
           L('psy:coercive-control', 'part-of', "نسخهٔ بزرگسالان و قانون", "The adult and legal version"),
           L('psy:gaslighting', 'part-of', "یکی از نُه دسته، از نزدیک", "One of the nine, up close"),
           L('psy:labels-harm', 'explains', "چرا رفتار، نه برچسب", "Why behaviour, not labels")],
    people=[p_barb, p_stark],
    try_={'text': t("نُه دستهٔ این رفتارها را می‌شود در یک رابطهٔ مشخص، از هر دو طرف، پر کرد: یک بار «با من چه می‌شود» و یک بار «من چه می‌کنم».",
                    "The nine classes can be filled in for one relationship, from both sides."),
          'tool': 'tools/control-check.html'},
    confusions=[
     t("مراقبت با کنترل فرق دارد: مراقبت دایرهٔ انتخاب طرف مقابل را باز نگه می‌دارد، کنترل آن را تنگ می‌کند. پرسش محک: «اگر نه بگویم، چه می‌شود؟»",
       "Care widens the other's circle of choice; control narrows it. The test: what happens if I say no?"),
     t("نظارت لازم در کار، ریزکنترل نیست. نظارت به نتیجه نگاه می‌کند و در نقطه‌های روشن؛ ریزکنترل به هر حرکت.",
       "Legitimate oversight looks at outcomes at set points; micro-control looks at every move."),
    ],
    status='reviewed')

add('psychological-control',
    title=t("کنترل روان‌شناختی والدین", "Parental psychological control", "Psychologische controle door ouders"),
    summary=t("شکلی از کنترل که به‌جای رفتار کودک، به دنیای درونی او کار دارد: احساس گناه، دریغ محبت، بی‌اعتبار کردن احساس و حملهٔ شخصی. در پژوهش‌ها با افسردگی، اضطراب و خودکم‌بینی همراه است.",
              "Control aimed at the child's inner world rather than behaviour, linked with depression, anxiety and low self-worth."),
    points=[
     P("باربر (۱۹۹۶) این سازه را که سال‌ها رها شده بود دوباره زنده کرد و نشان داد باید از «کنترل رفتاری» (قاعده گذاشتن، نظارت بر درس و دوستان) جدا شود: کنترل رفتاری با مشکلات بیرونی‌شده کمتر همراه است، ولی کنترل روان‌شناختی با مشکلات درونی‌شده بیشتر.",
       "Barber (1996) revived the construct and separated it from behavioural control.", [s_barb]),
     P("شاخه‌های رفتاری‌اش در همان کار نام‌گذاری شده‌اند: محدود کردن بیان کلامی، بی‌اعتبار کردن احساس، حملهٔ شخصی به کودک، ایجاد احساس گناه، دریغ محبت، و بی‌ثباتی هیجانی.",
       "Its behaviour classes: constraining verbal expression, invalidating feelings, personal attack, guilt induction, love withdrawal, erratic emotional behaviour.", [s_barb]),
     P("نسخهٔ «توجه مشروط» همین است در لباس مهربانی: محبت وقتی هست که کودک آن‌طور باشد که خواسته شده. اسور، روت و دسی نشان دادند این کودکان بعدها خودارزشی نوسانی، شرم بیشتر و خشم پنهان نسبت به والد دارند — حتی وقتی در ظاهر موفق‌اند.",
       "Assor, Roth and Deci showed conditional regard predicts fluctuating self-worth, shame and resentment.", [s_assor]),
    ],
    links=[L('psy:control-behaviors', 'part-of', "همان دسته‌ها در بزرگسالی", "The same classes in adulthood"),
           L('psy:conditional-regard', 'explains', "توجه مشروط", "Conditional regard"),
           L('psy:children-of-narcissists', 'applies-to', "وقتی والد خودشیفته باشد", "When the parent is narcissistic"),
           L('psy:p-dev', 'part-of', "روان‌شناسی رشد", "Developmental psychology")],
    people=[p_barb, p_deci],
    explain=t("فرق کنترل رفتاری و کنترل روان‌شناختی را با یک مثال می‌شود دید.\n\n«ساعت یازده باید خانه باشی» کنترل رفتاری است: قاعده روشن است، دربارهٔ کار است، و بچه می‌تواند با آن مخالف باشد بی‌آنکه رابطه‌اش به خطر بیفتد.\n\n«اگر دوستم داشتی این ساعت بیرون نمی‌ماندی» کنترل روان‌شناختی است: قاعده‌ای در کار نیست، خودِ پیوند گرو گذاشته شده است. بچه یاد می‌گیرد که مخالفت کردن یعنی به خطر انداختن عشق.\n\nنکتهٔ ظریف این است که این شکل دوم معمولاً از سر بی‌مهری نیست؛ بیشتر از ترس و نگرانی والد می‌آید. اثرش اما به نیت بستگی ندارد.",
              "Behavioural control sets rules; psychological control puts the bond itself at stake."),
    status='reviewed')

add('coercive-control',
    title=t("کنترل اجباری", "Coercive control", "Dwingende controle"),
    summary=t("الگویی از ترساندن، جداسازی، تحقیر و تنظیم ریز زندگی روزمره که آزادی آدم را می‌گیرد. ایوان استارک آن را «جرم علیه آزادی» نامید؛ از ۲۰۱۵ در انگلستان و از آن پس در چند کشور دیگر جرم است.",
              "A pattern of intimidation, isolation, degradation and micro-regulation that removes liberty; a criminal offence in several countries since 2015."),
    points=[
     P("استارک (۲۰۰۷) استدلال کرد که سنجیدن خشونت خانگی با شمردن کتک‌ها، اصل ماجرا را از دست می‌دهد: بسیاری از قربانیان از «در قفس بودن» حرف می‌زنند، نه از جراحت. چهار ابزار این قفس: خشونت، ترساندن، جداسازی، و کنترل.",
       "Stark argued counting assaults misses the point: victims describe entrapment, built from violence, intimidation, isolation and control.", [s_stark]),
     P("انگلستان و ولز در مادهٔ ۷۶ قانون جرائم جدی ۲۰۱۵ «رفتار کنترل‌گرانه یا اجباری در رابطهٔ عاطفی یا خانوادگی» را جرم شناختند؛ شرطش تکرار یا پیوستگی رفتار و «اثر جدی» بر قربانی است، و حداکثر مجازات پنج سال.",
       "England and Wales criminalised it in s.76 Serious Crime Act 2015, requiring repeated or continuous behaviour and a serious effect.", [s_sca, s_ho21]),
     P("پس از آن اسکاتلند (۲۰۱۸)، ایرلند (۲۰۱۸)، ایرلند شمالی (۲۰۲۱)، نیو ساوت ولز و کوئینزلند (اجرایی از ۲۰۲۴) و جاهای دیگر قانون مشابه گذاشتند؛ فرانسه و تاسمانی پیش‌تر از همه بودند.",
       "Scotland, Ireland, Northern Ireland, NSW and Queensland followed; France and Tasmania came earlier.", [s_mcq]),
     P("در پیمایش جرم انگلستان و ولز (۲۰۱۷/۱۸)، ۱٫۷ درصد از ۱۶ تا ۵۹ ساله‌ها گفتند در یک سال گذشته شریک یا شریک سابقشان با آن‌ها رفتار کنترل‌گرانه داشته است، و ۰٫۶ درصد دربارهٔ یکی از اعضای خانواده. خود گزارش تأکید می‌کند این برآوردها عدم‌قطعیت زیادی دارند.",
       "In the CSEW 2017/18, 1.7% reported controlling or coercive behaviour by a partner or ex in the past year.", [s_ho21], ['contested']),
     P("جرم‌انگاری همه‌چیز را حل نکرد: جرم‌های ثبت‌شده در انگلستان از حدود ۴٬۲۰۰ مورد (۲۰۱۶/۱۷) به نزدیک ۲۵٬۰۰۰ مورد (۲۰۱۹/۲۰) رسید، در حالی که محکومیت‌ها حدود سیصد مورد ماند. این عدد بیشتر دربارهٔ گزارش‌دهی و رویهٔ پلیس می‌گوید تا دربارهٔ میزان واقعی.",
       "Recorded offences rose roughly sixfold in four years while convictions stayed near 300.", [s_ho21]),
     P("منتقدان هم هستند: اینکه قانون بیشتر، لزوماً راه‌حل نیست؛ که زنان گاه به اشتباه به‌عنوان عامل شناسایی می‌شوند؛ و که در جامعه‌های اقلیت، جرم‌انگاری می‌تواند آسیب تازه بسازد.",
       "Critics argue more law is not the answer, that victims are misidentified as perpetrators, and that criminalisation can harm minority communities.", [s_mcq], ['contested']),
    ],
    links=[L('psy:control-behaviors', 'part-of', "دسته‌های رفتاری", "The behaviour classes"),
           L('psy:relationship-arc', 'explains', "چطور در طول زمان پیش می‌رود", "How it unfolds over time"),
           L('psy:leaving', 'see-also', "خروج و دورهٔ پرخطر", "Leaving and the high-risk period"),
           L('psy:victim-toll', 'explains', "اثرش بر تن و روان", "Its toll on body and mind")],
    people=[p_stark],
    examples=[
     EX("جردن ورث و الکس اسکیل، انگلستان: آشنایی در ۱۶ سالگی، و بعد کنترل تدریجی لباس، گوشی، شبکه‌های اجتماعی و ارتباط با خانواده — تا جایی که پیام‌هایی از گوشی او برای خانواده‌اش فرستاده می‌شد که دیگر تماس نگیرند. در ۲۰۱۸ ورث نخستین زنی شد که به جرم «رفتار کنترل‌گرانه» در انگلستان محکوم شد.",
        "Jordan Worth and Alex Skeel: the first woman convicted under the English coercive-control offence, in 2018.",
        kind='story', label='real', source="BBC News, 16–17 April 2018"),
    ],
    confusions=[
     t("کنترل اجباری با «دعوای زیاد» یکی نیست. مایکل جانسون این دو را جدا کرد: در «تروریسم خانگی» خشونت در دل یک الگوی کنترل است، در «خشونت موقعیتی زوج» دعوای دوطرفه‌ای است که از کنترل نمی‌آید. این تمایز هم مفید است و هم منتقد دارد.",
       "Johnson's distinction between intimate terrorism and situational couple violence is useful and contested."),
    ],
    status='reviewed')

add('gaslighting',
    title=t("گازلایتینگ: دست بردن در واقعیت", "Gaslighting", "Gaslighting"),
    summary=t("وقتی کسی به‌طور تکراری ادراک، حافظه و سلامت عقل شما را زیر سؤال می‌برد تا روایت خودش بماند. نتیجه‌اش شک به خود است: «شاید واقعاً من بد فهمیده‌ام.»",
              "Repeatedly undermining someone's perception, memory or sanity so that one version of reality stands."),
    points=[
     P("نام از نمایشنامه و فیلم «گازلایت» (۱۹۳۸ و ۱۹۴۴) می‌آید که در آن شوهر نور چراغ‌های گازی خانه را کم می‌کند و وقتی زن متوجه می‌شود، انکار می‌کند تا او به ذهن خودش شک کند.",
       "The name comes from the 1938 play and 1944 film Gaslight.", [s_sweet]),
     P("پیج سوئیت در تحلیل جامعه‌شناختی‌اش استدلال کرد که گازلایتینگ فقط یک بازی روانی میان دو نفر نیست: وقتی کار می‌کند که نابرابری واقعی پشتش باشد — جنسیتی، مالی، مهاجرتی — و وقتی کلیشه‌های اجتماعی («زن‌ها احساساتی‌اند»، «او بیمار روانی است») حرف یکی را از پیش بی‌اعتبار کرده باشد.",
       "Sweet argued gaslighting works where real inequality and stereotypes already discredit one party.", [s_sweet]),
     P("نشانهٔ عملی‌اش بیرون از دعواست: بعد از گفت‌وگو به حافظهٔ خودتان شک می‌کنید، برای یادآوری به یادداشت و پیام نیاز پیدا می‌کنید، و پیش از حرف‌زدن در ذهنتان تمرین می‌کنید.",
       "A practical sign: doubting your own memory after conversations and rehearsing before speaking.", [s_sweet]),
    ],
    links=[L('psy:control-behaviors', 'part-of', "یکی از نُه دسته", "One of the nine classes"),
           L('psy:darvo', 'see-also', "وارونه‌کردن نقش قربانی", "Reversing victim and offender"),
           L('psy:self-trust', 'explains', "بازسازی اعتماد به ادراک خود", "Rebuilding epistemic self-trust")],
    people=[p_sweet],
    confusions=[
     t("هر اختلاف حافظه گازلایتینگ نیست. حافظهٔ آدم‌ها واقعاً بد و بازسازی‌شونده است و دو نفر صادق می‌توانند دو روایت متفاوت داشته باشند. آنچه فرق می‌کند جهت و تکرار است: همیشه یک نفر است که باید از ادراک خودش دست بکشد.",
       "Not every memory conflict is gaslighting; what differs is the one-way, repeated pattern."),
     t("«گازلایتینگ» هم مثل «خودشیفته» به کلمه‌ای فرسوده تبدیل شده است. وقتی هر مخالفتی گازلایتینگ خوانده شود، کلمه دیگر چیزی را توصیف نمی‌کند.",
       "The word has been overused to the point of losing meaning."),
    ],
    status='reviewed')

add('darvo',
    title=t("DARVO: انکار، حمله، وارونه‌کردن نقش‌ها", "DARVO", "DARVO"),
    summary=t("الگویی که جنیفر فرید نام‌گذاری کرد: کسی که به او اعتراض شده، اول انکار می‌کند، بعد به معترض حمله می‌کند، و در پایان جای قربانی و متهم را عوض می‌کند — «قربانی واقعی من هستم».",
              "Deny, Attack, Reverse Victim and Offender: the pattern Jennifer Freyd named."),
    points=[
     P("هارسی و فرید در آزمایش نشان دادند که شنیدن همین الگو اثر دارد: کسانی که روایتی با DARVO خواندند، فرد معترض را کم‌اعتبارتر و مقصرتر دیدند و متهم را بی‌گناه‌تر.",
       "Harsey and Freyd showed that exposure to DARVO lowers perceived victim credibility.", [s_darvo]),
     P("در همان کار دیده شد که هدف DARVO معمولاً خودسرزنشی بیشتری تجربه می‌کند: تکرار این الگو آدم را به این نتیجه می‌رساند که «لابد من زیادی بزرگش کردم».",
       "Targets of DARVO report more self-blame.", [s_darvo]),
     P("دانستن نام این الگو خودش اثر دارد: در پژوهش‌های بعدی، کسانی که از پیش DARVO را می‌شناختند کمتر فریبش را خوردند. این یکی از معدود جاهایی است که «آگاهی» به‌تنهایی سپر می‌شود.",
       "Knowing the pattern reduces its effect — rare evidence that awareness alone helps.", [s_darvo]),
    ],
    links=[L('psy:gaslighting', 'see-also', "دست بردن در واقعیت", "Altering reality"),
           L('psy:defensive-reactions', 'part-of', "واکنش‌های دفاعی", "Defensive reactions"),
           L('psy:victim-mindset', 'contrasts', "تفاوتش با نقش قربانی", "How it differs from the victim role")],
    people=[p_freyd],
    explain=t("سه حرکت پشت سر هم:\n\n<b>انکار.</b> «چنین چیزی نشده.» «تو داری خیال می‌کنی.»\n\n<b>حمله.</b> «تو چرا این را حالا می‌گویی؟» «خودت یادت رفته چه کردی؟» معمولاً حمله به انگیزه و شخصیت معترض است، نه به حرفش.\n\n<b>وارونه‌سازی.</b> «من قربانی این ماجرا هستم.» «ببین با من چه کردی.» حالا کسی که اعتراض کرده باید توضیح بدهد و دلجویی کند.\n\nاین الگو مخصوص رابطهٔ دونفره نیست: همین ترتیب در سازمان‌ها هم دیده می‌شود، وقتی به جای رسیدگی به شکایت، به شاکی پرداخته می‌شود.",
              "Three moves: deny, attack, reverse — also seen in organisations that investigate the complainant."),
    status='reviewed')

add('gottman-horsemen',
    title=t("چهار سوار: انتقاد، تحقیر، دفاع، سکوت", "Gottman's four horsemen", "De vier ruiters"),
    summary=t("جان گاتمن با فیلم‌برداری از گفت‌وگوی زوج‌ها چهار الگو را پیدا کرد که جدایی را پیش‌بینی می‌کنند. سمی‌ترینشان تحقیر است. برای هر کدام یک پادزهر ساده هست.",
              "Four communication patterns that predict divorce, the most toxic being contempt — each with an antidote."),
    points=[
     P("گاتمن و لوینسن با مشاهدهٔ گفت‌وگوی زوج‌ها در آزمایشگاه و پیگیری چندساله نشان دادند که الگوی تعامل، و نه موضوع دعوا، جدایی را پیش‌بینی می‌کند.",
       "Gottman and Levenson showed interaction patterns, not topics, predict dissolution.", [s_gott]),
     P("چهار الگو: انتقاد از شخص به‌جای گلایه از رفتار؛ تحقیر (پوزخند، کنایه، مسخره‌کردن)؛ دفاع و وارونه‌کردن؛ و دیوار سکوت.",
       "The four: criticism, contempt, defensiveness and stonewalling.", [s_gott]),
     P("پادزهرها ساده‌اند و در خودِ جمله‌اند: به‌جای انتقاد، گلایهٔ مشخص با «من»؛ به‌جای تحقیر، گفتن چیزی که قدرش را می‌دانی؛ به‌جای دفاع، پذیرفتن سهم کوچک خودت؛ و به‌جای دیوار سکوت، فاصلهٔ کوتاهِ قرارگذاشته‌شده و برگشتن.",
       "The antidotes: specific I-complaints, appreciation, taking a small share of responsibility, and an agreed short break.", [s_gott]),
     P("صادقانه دربارهٔ اعتبارش: عددهای مشهور «پیش‌بینی طلاق با دقت بیش از ۹۰ درصد» بر نمونه‌های کوچک و بدون اعتبارسنجی روی نمونهٔ تازه به دست آمده‌اند و منتقدان نشان داده‌اند چنین دقتی تورمی است. خودِ الگوها از مشاهدهٔ واقعی می‌آیند و مفیدند؛ «پادزهرها» اما توصیهٔ بالینی‌اند، نه مداخله‌ای که جداگانه آزموده شده باشد.",
       "Honestly: the famous >90% divorce-prediction accuracy comes from models fitted and evaluated on the same small samples; the antidotes are clinical prescriptions, not separately trialled.", [s_heyman], ['contested']),
    ],
    links=[L('psy:defensive-reactions', 'explains', "دفاع، از نزدیک", "Defensiveness up close"),
           L('psy:control-behaviors', 'see-also', "نسبتش با رفتارهای کنترل‌گرانه", "Relation to controlling behaviour")],
    people=[p_gott],
    try_={'text': t("پنجاه‌وچند جملهٔ آشنا، با توضیح اینکه هر کدام چه می‌کند و به‌جایش چه می‌شود گفت.", "Over fifty familiar sentences with alternatives."),
          'tool': 'tools/sentences.html'},
    status='reviewed')

add('defensive-reactions',
    title=t("واکنش‌های دفاعی خودمان", "Our own defensive reactions", "Onze eigen verdedigingsreacties"),
    summary=t("وقتی تصویر ما از خودمان تهدید می‌شود، بدن پیش از فکر واکنش نشان می‌دهد: دفاع، حمله، توجیه، قهر یا تسلیم. شناختن واکنشِ پیش‌فرضِ خودمان، بیشتر از شناختن طرف مقابل کار را عوض می‌کند.",
              "When our self-image is threatened the body reacts before thought: defend, attack, justify, withdraw or submit."),
    points=[
     P("هستهٔ مشترک خودشیفتگی، حساسیت شدید به تهدید تصویر خود است؛ اما واکنش دفاعی به تهدیدِ تصویر، چیزی همگانی است. تفاوت در آستانه و شدت است، نه در وجود آن.",
       "Defensive reaction to self-image threat is universal; narcissism differs in threshold and intensity.", [s_mill]),
     P("در گفت‌وگوی زوج‌ها، «دفاع» یکی از چهار الگوی پیش‌بینی‌کنندهٔ جدایی است، چون گلایه را بی‌جواب می‌گذارد و به پروندهٔ متقابل تبدیلش می‌کند.",
       "Defensiveness is one of the four horsemen because it converts a complaint into a counter-case.", [s_gott]),
     P("شکل تندترش DARVO است: انکار، حمله، و وارونه‌کردن نقش قربانی و متهم.",
       "Its sharper form is DARVO.", [s_darvo]),
     P("پادزهر عملی، یک جملهٔ کوچک است: پیدا کردن آن بخش از حرف طرف مقابل که درست است و گفتنش، پیش از هر توضیحی. این کار برانگیختگی هر دو را پایین می‌آورد و گفت‌وگو را باز نگه می‌دارد.",
       "The antidote is naming the part of the complaint that is true before explaining anything.", [s_gott]),
    ],
    links=[L('psy:gottman-horsemen', 'part-of', "چهار سوار", "The four horsemen"),
           L('psy:darvo', 'see-also', "شکل تندتر", "The sharper form"),
           L('psy:self-compassion', 'explains', "چرا شرم، دفاع می‌سازد", "Why shame produces defence")],
    try_={'text': t("جمله‌ای را که آخرین بار در دعوا گفتید بنویسید و ببینید کدام الگو در آن هست، و چه جایگزینی دارد.",
                    "Write the last thing you said in an argument and see which pattern it is."),
          'tool': 'tools/sentences.html'},
    status='reviewed')

add('karpman-triangle',
    title=t("مثلث قربانی، ظالم، ناجی", "The drama triangle and the way out", "Dramadriehoek"),
    summary=t("استیون کارپمن در ۱۹۶۸ دید که دعواهای تکراری روی سه نقش می‌چرخند: قربانی، ظالم، ناجی. نکتهٔ اصلی این است که این‌ها آدم نیستند، نقش‌اند — و نقش‌ها می‌چرخند.",
              "Karpman's 1968 observation that repetitive conflicts rotate through three roles, and that the roles switch."),
    points=[
     P("کارپمن این الگو را در تحلیل داستان‌ها و نمایش‌نامه‌ها دید و به رابطه‌های واقعی آورد: هر سه نقش به هم نیاز دارند و هر کدام سود پنهانی دارند که ماندن در مثلث را ممکن می‌کند.",
       "Karpman drew the pattern from drama analysis; each role has a hidden payoff.", [s_karp]),
     P("چرخش نقش‌ها همان چیزی است که الگو را فرساینده می‌کند: ناجیِ خسته طلبکار می‌شود و به ظالم می‌رسد؛ ظالمِ مچ‌گرفته‌شده خود را قربانی می‌بیند؛ قربانیِ ناامید از ناجی، به او حمله می‌کند.",
       "The role switch is what makes the pattern exhausting.", [s_karp]),
     P("دیوید امرالد برای هر گوشه یک جایگزین گذاشت: قربانی به «خالق» (چه می‌خواهم؟)، ظالم به «چالش‌گر» (این وضع چه می‌خواهد؟)، ناجی به «مربی» (چه کاری از خودت برمی‌آید؟).",
       "Emerald proposed Creator, Challenger and Coach as the alternatives.", [s_ted]),
     P("صادقانه دربارهٔ اعتبارش: این یک چارچوب بالینی از «تحلیل رفتار متقابل» است، نه سازه‌ای که اندازه‌گیری و آزموده شده باشد. فایده‌اش نام‌گذاری الگویی است که آدم‌ها فوراً می‌شناسند.",
       "Honestly: this is a clinical framework from transactional analysis, not a measured construct.", [s_karp, s_ted], ['editor-note']),
    ],
    links=[L('psy:victim-mindset', 'part-of', "گوشهٔ قربانی", "The victim corner"),
           L('psy:rescuing', 'part-of', "گوشهٔ ناجی", "The rescuer corner"),
           L('psy:agency', 'explains', "راه بیرون: حق انتخاب", "The way out: agency")],
    people=[p_karp, p_emer],
    try_={'text': t("یک موقعیت واقعی خودتان را در شش گام از مثلث بیرون بیاورید.", "Take one real situation of yours out of the triangle in six steps."),
          'tool': 'tools/triangle.html'},
    confusions=[
     t("این مدل را نباید به رابطه‌ای که در آن خشونت یا کنترل اجباری هست تعمیم داد. آن‌جا گفتن «تو هم نقشی داری» سهم تقصیر را روی کسی می‌گذارد که در خطر است. قربانیِ خشونت نقش بازی نمی‌کند.",
       "The model must not be applied to violence or coercive control; victims of violence are not playing a role."),
    ],
    status='reviewed')

add('rescuing',
    title=t("ناجی‌گری در برابر کمک واقعی", "Rescuing versus helping", "Redden versus helpen"),
    summary=t("کمکِ نخواسته، کمک نیست. ناجی‌گری طرف مقابل را ناتوان نگه می‌دارد و کمک‌کننده را ضروری؛ و در پایان هر دو طلبکار و خسته‌اند.",
              "Unasked-for help keeps the other incapable and the helper indispensable."),
    points=[
     P("در مثلث کارپمن، ناجی سومین گوشه است و بدون او مثلث نمی‌چرخد: نجات تکراری، این باور را محکم می‌کند که طرف مقابل خودش نمی‌توانست.",
       "The rescuer is the third corner; repeated rescue confirms the other's incapacity.", [s_karp]),
     P("در نظریهٔ خودتعیین‌گری، آنچه انگیزه را زنده نگه می‌دارد حس «خودم انجامش دادم» است. کمکی که این حس را بگیرد، در بلندمدت انگیزه را هم می‌گیرد.",
       "In self-determination theory, autonomy sustains motivation; help that removes it removes motivation.", [s_assor]),
     P("تفاوت عملی در یک پرسش است: «کمک می‌خواهی، یا می‌خواهی فقط گوش بدهم؟» و در یک مرز: «تا این‌جا هستم، از این‌جا به بعد با توست.»",
       "The practical difference is asking first and stating a limit.", [s_karp, s_ted]),
    ],
    links=[L('psy:karpman-triangle', 'part-of', "گوشهٔ سوم", "The third corner"),
           L('psy:self-compassion', 'contrasts', "شفقت بدون ناجی‌گری", "Compassion without rescuing")],
    status='reviewed')

add('public-private',
    title=t("جلوی مردم خوب، در خانه بد", "Charming in public, different at home", "Buiten charmant, thuis anders"),
    summary=t("یکی از سخت‌ترین تجربه‌ها برای کسی که در رابطه‌ای کنترل‌گرانه است: بیرون همه آن آدم را دوست دارند. این تناقض، تنهایی را دوبرابر می‌کند و باور شدن را سخت.",
              "The hardest part for many: outside, everyone likes that person. The contradiction doubles the isolation."),
    points=[
     P("در پژوهش کیفی روی شریک‌ها و خانواده‌های افراد با خودشیفتگی آسیب‌شناختی، همین تضاد یکی از مضمون‌های تکرارشونده بود: چهرهٔ بیرونی جذاب و توانمند، و زندگی خانگی پر از بی‌ثباتی و کنترل.",
       "In a qualitative study of relatives of people with pathological narcissism, this contrast was a recurring theme.", [s_day]),
     P("در ادبیات رهبری، همین دوگانگی عدد هم دارد: خودشیفتگی «به رهبری رسیدن» را بالا می‌برد ولی در طول زمان کیفیت رابطهٔ رهبر و پیرو افت می‌کند — تصویر اول درخشان است و ادامه‌اش نه.",
       "In leadership research narcissism predicts emergence while leader–follower relationships deteriorate over time.", [s_braun, s_grij]),
     P("اثر عملی‌اش بر اطرافیان: کسی که آسیب می‌بیند، وقتی حرف می‌زند باور نمی‌شود، و همین بی‌باوری خودش بخشی از آسیب می‌شود.",
       "The practical effect: the person harmed is not believed, and the disbelief itself becomes part of the harm.", [s_day, s_darvo]),
    ],
    links=[L('psy:darvo', 'see-also', "وقتی روایت وارونه می‌شود", "When the story is reversed"),
           L('psy:victim-toll', 'explains', "چرا باور نشدن آسیب را بیشتر می‌کند", "Why not being believed deepens harm"),
           L('psy:stigma', 'see-also', "مدیریت تصویر در جمع", "Impression management")],
    people=[p_freyd],
    explain=t("چرا این دوگانگی عجیب نیست و حتی انتظار می‌رود؟\n\nبیرونِ خانه، آدم‌ها اختیار دارند: می‌توانند بروند. پس رفتار باید جذاب باشد تا بمانند. درونِ خانه یا در تیمی که کسی نمی‌تواند به‌راحتی ترکش کند، این فشار برداشته می‌شود.\n\nبه زبان ساده: رفتار آدم‌ها جایی عوض می‌شود که هزینهٔ رفتن برای طرف مقابل بالا باشد. برای همین همان شخص با غریبه مهربان است و با نزدیک‌ترین آدمش نه.\n\nاین برای کسی که در آن رابطه است یعنی: اگر دیگران حرفت را باور نکردند، لزوماً اشتباه نمی‌کنی. آن‌ها نسخهٔ دیگری از همان آدم را دیده‌اند، و آن نسخه هم واقعی است.",
              "Behaviour changes where the cost of leaving is high for the other person."),
    status='reviewed')

# ---------------- منابع دستهٔ سوم ----------------
s_felit = src("Felitti, V. J., Anda, R. F., Nordenberg, D., et al. (1998). Relationship of Childhood Abuse and Household Dysfunction to Many of the Leading Causes of Death in Adults: The Adverse Childhood Experiences (ACE) Study. American Journal of Preventive Medicine, 14(4), 245–258.", 2)
s_hughes= src("Hughes, K., Bellis, M. A., Hardcastle, K. A., et al. (2017). The effect of multiple adverse childhood experiences on health: a systematic review and meta-analysis. The Lancet Public Health, 2(8), e356–e366.", 1)
s_spina = src("Spinazzola, J., Hodgdon, H., Liang, L.-J., et al. (2014). Unseen wounds: The contribution of psychological maltreatment to child and adolescent mental health and risk outcomes. Psychological Trauma: Theory, Research, Practice, and Policy, 6(S1), S18–S28.", 2)
s_orov  = src("Orovou, E., Jotautis, V., Vousoura, E., Koutelekos, I., Rigas, N., & Sarantaki, A. (2025). Impact of Parental Narcissistic Personality Disorder on Parent–Child Relationship Quality and Child Well-Being: A Systematic Review. Cureus.", 2)
s_jens  = src("Jensen, A. C., & Thomsen, D. K. (2024). Parental differential treatment of siblings linked with internalizing and externalizing behavior: A meta-analysis. Child Development.", 1)
s_hoop  = src("Hooper, L. M., DeCoster, J., White, N., & Voltz, M. L. (2011). Characterizing the magnitude of the relation between self-reported childhood parentification and adult psychopathology: A meta-analysis. Journal of Clinical Psychology, 67(10), 1028–1043.", 1)
s_thom  = src("Thompson, M. J., Platts, C. R., & Davies, P. T. (2024). Parent–child boundary dissolution and children's psychological difficulties: A meta-analytic review. Psychological Bulletin.", 1)
s_golding=src("Golding, J. M. (1999). Intimate partner violence as a risk factor for mental disorders: A meta-analysis. Journal of Family Violence, 14(2), 99–132.", 1)
s_devr  = src("Devries, K. M., Mak, J. Y., Bacchus, L. J., et al. (2013). Intimate partner violence and incident depressive symptoms and suicide attempts: a systematic review of longitudinal studies. PLoS Medicine, 10(5), e1001439.", 1)
s_dokk  = src("Dokkedahl, S., Kirubakaran, R., Bech-Hansen, D., Kristensen, T. R., & Elklit, A. (2022). The psychological subtype of intimate partner violence and its effect on mental health: a systematic review with meta-analyses. Systematic Reviews, 11, 163.", 1)
s_white = src("White, S. J., Sin, J., Sweeney, A., et al. (2023). Global prevalence and mental health outcomes of intimate partner violence among women: A systematic review and meta-analysis. Trauma, Violence, & Abuse.", 1)
s_cloit = src("Cloitre, M., Hyland, P., Bisson, J. I., et al. (2019). ICD-11 posttraumatic stress disorder and complex posttraumatic stress disorder in the United States: A population-based study. Journal of Traumatic Stress, 32(6), 833–842.", 2)
s_miller= src("Miller, G. E., Chen, E., & Zhou, E. S. (2007). If it goes up, must it come down? Chronic stress and the hypothalamic-pituitary-adrenocortical axis in humans. Psychological Bulletin, 133(1), 25–45.", 1)
s_adam  = src("Adam, E. K., Quinn, M. E., Tavernier, R., et al. (2017). Diurnal cortisol slopes and mental and physical health outcomes: A systematic review and meta-analysis. Psychoneuroendocrinology, 83, 25–41.", 1)
s_mcew  = src("McEwen, B. S. (1998). Protective and damaging effects of stress mediators. New England Journal of Medicine, 338(3), 171–179.", 2)
s_baum  = src("Baumeister, D., Akhtar, R., Ciufolini, S., Pariante, C. M., & Mondelli, V. (2016). Childhood trauma and adulthood inflammation: a meta-analysis of peripheral C-reactive protein, interleukin-6 and tumour necrosis factor-α. Molecular Psychiatry, 21, 642–649.", 1)
s_pig   = src("Pigeon, W. R., Cerulli, C., Richards, H., He, H., Perlis, M., & Caine, E. (2011). Sleep disturbances and their association with mental health among women exposed to intimate partner violence. Journal of Women's Health, 20(12), 1923–1929.", 2)
s_chand = src("Chandan, J. S., Thomas, T., Raza, K., et al. (2020). Association between child maltreatment and central sensitivity syndromes: a systematic review and matched retrospective cohort study. EClinicalMedicine, 23, 100392.", 2)
s_shen  = src("Shen, S., & Kusunoki, Y. (2019). Intimate Partner Violence and Psychological Distress Among Emerging Adult Women: A Bidirectional Relationship. Journal of Women's Health, 28(9), 1172–1179.", 2)
s_jackd = src("Jack, D. C., & Dill, D. (1992). The Silencing the Self Scale: Schemas of intimacy associated with depression in women. Psychology of Women Quarterly, 16(1), 97–106.", 2)
s_jack26= src("Jack, D. C., Brody, L. R., & Sikov, J. (2026). Advancing the next generation of research on self-silencing and depression: a narrative review and synthesis of three decades of research. Sex Roles.", 2)
s_fordg = src("Ford-Gilboe, M., Varcoe, C., Wuest, J., et al. (2022). Longitudinal Impacts of Intimate Partner Violence on Women's Mental Health and Chronic Pain. Journal of Interpersonal Violence.", 2)
s_coven = src("Coventry, P. A., Meader, N., Melton, H., et al. (2020). Psychological and pharmacological interventions for posttraumatic stress disorder and comorbid mental health problems following complex traumatic events: Systematic review and component network meta-analysis. PLoS Medicine, 17(8), e1003262.", 1)
s_karat = src("Karatzias, T., Murphy, P., Cloitre, M., et al. (2019). Psychological interventions for ICD-11 complex PTSD symptoms: systematic review and meta-analysis. Psychological Medicine, 49(11), 1761–1775.", 1)
s_oprel = src("Oprel, D. A. C., Hoeboer, C. M., Schoorl, M., et al. (2021). Effect of prolonged exposure, intensified prolonged exposure and STAIR+PE on PTSD severity and symptoms of complex PTSD: a randomized controlled trial. European Journal of Psychotraumatology, 12, 1851511.", 1)
s_fraz  = src("Frazier, P., Tennen, H., Gavian, M., Park, C., Tomich, P., & Tashiro, T. (2009). Does self-reported posttraumatic growth reflect genuine positive change? Psychological Science, 20(7), 912–919.", 2)
s_mang  = src("Mangelsdorf, J., Eid, M., & Luhmann, M. (2019). Does growth require suffering? A systematic review and meta-analysis on genuine posttraumatic and postecstatic growth. Psychological Bulletin, 145(3), 302–338.", 1)
s_kiec  = src("Kiecolt-Glaser, J. K., Preacher, K. J., MacCallum, R. C., Atkinson, C., Malarkey, W. B., & Glaser, R. (2003). Chronic stress and age-related increases in the proinflammatory cytokine IL-6. PNAS, 100(15), 9090–9095.", 2)
s_barat = src("Baratta, M. V., Seligman, M. E. P., & Maier, S. F. (2023). From helplessness to controllability: toward a neuroscience of resilience. Frontiers in Psychiatry, 14, 1170417.", 2)
s_kurtis= src("Kurtiş, T. (2010). Self-silencing and well-being among Turkish women. University of Kansas (MA thesis).", 4)

p_felit = who("Vincent Felitti", "وینسنت فلیتی", "۱۹۳۱–", "پزشک؛ از طراحان پژوهش تجربه‌های ناگوار کودکی (ACE).")
p_maier = who("Steven Maier", "استیون مایر", "۱۹۴۲–", "عصب‌پژوه؛ با سلیگمن نشان داد آنچه آموخته می‌شود کنترل است، نه درماندگی.")
p_cloit = who("Marylene Cloitre", "مارلین کلویتر", "", "روان‌شناس بالینی؛ از معماران مفهوم اختلال استرس پس از سانحهٔ پیچیده.")
p_jacks = who("Jennifer Jensen", "جنیفر جنسن", "", "پژوهشگر روابط خواهر و برادری و رفتار متفاوت والدین.")

# ================= ۳. ریشه‌ها: کودکی و خانواده =================
add('narcissism-origins',
    title=t("خودشیفتگی از کجا می‌آید", "Where narcissism comes from", "Waar narcisme vandaan komt"),
    summary=t("دو فرضیهٔ قدیمی رو در روی هم بودند: سردی والد، یا ستایش بیش از حد. یک پژوهش طولی روی ۵۶۵ کودک پاسخ روشنی داد: ارزش‌گذاری اغراق‌آمیز خودشیفتگی می‌سازد، و گرما عزت‌نفس.",
              "Two old hypotheses — parental coldness versus overvaluation — were tested: overvaluation predicts narcissism, warmth predicts self-esteem."),
    points=[
     P("بروملمن و همکاران ۵۶۵ کودک ۷ تا ۱۲ ساله و والدینشان را در چهار نوبت با فاصلهٔ شش ماه سنجیدند. «ارزش‌گذاری اغراق‌آمیز» والد (اینکه فرزندم از بچه‌های دیگر خاص‌تر و بااستعدادتر است) خودشیفتگی بعدی کودک را پیش‌بینی کرد؛ کمبود گرمای والد این کار را نکرد.",
       "Brummelman et al. followed 565 children across four waves: parental overvaluation predicted later child narcissism; lack of warmth did not.", [s_brum]),
     P("در همان داده، گرمای والد عزت‌نفس کودک را پیش‌بینی کرد و ارزش‌گذاری اغراق‌آمیز نه. یعنی دو مسیر جدا: ستایش تورمی خودشیفتگی می‌سازد، محبت واقعی عزت‌نفس.",
       "Warmth predicted self-esteem; overvaluation did not — two separate paths.", [s_brum, s_brum2]),
     P("این یافته به سود نظریه‌های یادگیری اجتماعی و به زیان روایت روان‌کاوانهٔ کلاسیک (سردی والد) بود؛ هرچند یک پژوهش، هرچه خوش‌طرح، پروندهٔ یک بحث صدساله را نمی‌بندد.",
       "The finding favours social-learning accounts over the classic psychoanalytic one — though one study does not close a century-old debate.", [s_brum], ['contested']),
     P("مسیر دیگری هم هست که شواهد خوبی دارد: «توجه مشروط». وقتی محبت والد به عملکرد گره بخورد، کودک آن را درونی می‌کند و خودارزشی‌اش نوسانی می‌شود — بالا پس از موفقیت، شرم پس از شکست — همراه با خشمی پنهان نسبت به والد.",
       "Conditional regard leads to introjection, fluctuating self-worth and resentment.", [s_assor]),
     P("در همان پژوهش، انتقال بین‌نسلی هم دیده شد: مادرانی که خودشان توجه مشروط را تجربه کرده بودند، بیشتر همان را با دخترانشان تکرار می‌کردند.",
       "Mothers who had experienced conditional regard were more likely to repeat it.", [s_assor]),
    ],
    links=[L('psy:healthy-narcissism', 'explains', "چرا ستایش و محبت دو چیزند", "Why praise and warmth differ"),
           L('psy:conditional-regard', 'part-of', "توجه مشروط", "Conditional regard"),
           L('psy:children-of-narcissists', 'see-also', "آن طرف ماجرا: فرزندان", "The other side: the children")],
    people=[p_brum, p_deci],
    explain=t("تفاوت گرما و ارزش‌گذاری اغراق‌آمیز، در عمل، در خود جمله‌هاست.\n\n<b>گرما:</b> «دوستت دارم.» «از بودن با تو لذت می‌برم.» «سخت بود و تو ادامه دادی.» پیام: تو ارزشمندی.\n\n<b>ارزش‌گذاری اغراق‌آمیز:</b> «تو از همهٔ بچه‌ها بااستعدادتری.» «تو استثنایی هستی.» «معلمت لیاقت تو را ندارد.» پیام: تو برتری.\n\nپیام اول پایه می‌سازد؛ پیام دوم بدهی می‌سازد. کودکی که یاد گرفته برتر است، باید هر روز آن برتری را ثابت کند، و هر نقد به تهدید هویت تبدیل می‌شود.\n\nاین برای والدی که می‌خواهد کاری کند خبر خوبی است: راه‌حل، سرد شدن نیست. راه‌حل، جابه‌جا کردن ستایش از «تو چه هستی» به «چه کردی و چطور».",
              "Warmth says you are valued; overvaluation says you are superior, which creates a debt to be repaid daily."),
    status='reviewed')

add('children-of-narcissists',
    title=t("بچه‌های والدین خودشیفته", "Children of narcissistic parents", "Kinderen van narcistische ouders"),
    summary=t("این موضوع در اینترنت پر از قطعیت است و در پژوهش تقریباً خالی. آنچه واقعاً شواهد دارد چیز دیگری است: رفتار متفاوت والد با فرزندان، کنترل روان‌شناختی، و توجه مشروط.",
              "A topic full of online certainty and nearly empty of research; what is evidenced is differential treatment, psychological control and conditional regard."),
    points=[
     P("تنها مرور نظام‌مند موجود (۲۰۲۵) در ده سال فقط هشت پژوهش کمّی پیدا کرد و نتیجه‌اش را «پراکنده و از نظر مفهومی ناسازگار» خواند. آنچه دیده شد: وجه «ستیزه‌جویانهٔ» خودشیفتگی والد با رابطهٔ سردتر و پرتعارض‌تر همراه بود، و خودشیفتگی آسیب‌پذیر با ناسازگاری بیشتر فرزند.",
       "The only systematic review (2025) found just eight quantitative studies and called the findings fragmented.", [s_orov], ['unreplicated']),
     P("«فرزند طلایی» و «سپر بلا» در هیچ پژوهش داوری‌شده‌ای به‌عنوان نقش سنجیده نشده‌اند؛ این‌ها ادبیات بالینی و اینترنتی‌اند. اما سازهٔ نزدیکشان پژوهش محکمی دارد: «رفتار متفاوت والد با فرزندان».",
       "'Golden child' and 'scapegoat' have no peer-reviewed empirical base; the adjacent researched construct is parental differential treatment.", [s_jens], ['editor-note']),
     P("فراتحلیل ۲۰۲۴ روی ۴۳ نمونه و بیش از ۲۶ هزار نفر نشان داد فرزندی که کمتر مورد لطف است، هم مشکلات درونی‌شده (افسردگی، اضطراب) و هم بیرونی‌شده بیشتری دارد؛ و هرچه فاصلهٔ رفتار والد با دو فرزند بیشتر باشد، اثر بزرگ‌تر است.",
       "A 2024 meta-analysis (43 samples, N>26,000) found the less-favoured child shows more internalizing and externalizing problems.", [s_jens]),
     P("«والدشدگی» کودک (پدر یا مادرِ والد خود شدن) اثری واقعی ولی کوچک دارد: در فراتحلیل، همبستگی با آسیب روانی بزرگسالی حدود ۰٫۱۴ بود. برخلاف تصویر رایج، این به‌تنهایی سرنوشت‌ساز نیست.",
       "Parentification has a real but small effect: r = .14 with adult psychopathology.", [s_hoop]),
     P("در فراتحلیل دیگری روی ۴۷۸ پژوهش، از میان چهار الگوی «فروریختن مرز والد و فرزند»، بیشترین اثر مال «درهم‌تنیدگی» (کنترل روان‌شناختی و نفوذ به دنیای درونی کودک) بود و کمترین مال والدشدگی.",
       "Across 478 studies, enmeshment had the largest effect and caregiving/parentification the smallest.", [s_thom]),
     P("آنچه بدون ابهام شواهد دارد این است: بدرفتاری روانی کم‌اهمیت‌تر از بدرفتاری جسمی نیست. در داده‌های بیش از پنج هزار نوجوان ارجاع‌شده به درمان، بدرفتاری روانی در هفده شاخص از بیست‌وهفت شاخص بالینی بدتر از سوءاستفادهٔ جنسی و در چند شاخص بدتر از آزار جسمی بود.",
       "Psychological maltreatment is not the lesser harm: in 5,616 clinic-referred youth it was worse than sexual abuse on 17 of 27 indicators.", [s_spina]),
    ],
    links=[L('psy:psychological-control', 'explains', "سازوکار اصلی", "The main mechanism"),
           L('psy:narcissism-origins', 'see-also', "چرخه از کجا می‌آید", "Where the cycle comes from"),
           L('psy:conditional-regard', 'part-of', "توجه مشروط", "Conditional regard"),
           L('psy:breaking-cycle', 'explains', "شکستن چرخه", "Breaking the cycle"),
           L('psy:victim-toll', 'see-also', "اثر بلندمدت", "The long-term toll")],
    people=[p_jacks],
    explain=t("چرا این‌جا این‌قدر محتاطیم؟\n\nچون این موضوع بازار بزرگی دارد. فهرست‌های «ده نشانهٔ مادر خودشیفته» در اینترنت فراوان‌اند و تقریباً هیچ‌کدام پشتوانهٔ پژوهشی ندارند. مشکلشان فقط بی‌دقتی نیست: این فهرست‌ها طوری نوشته شده‌اند که تقریباً هر والدی در آن‌ها جا می‌شود.\n\nو چیزی که به‌جایش می‌شود گفت، هم دقیق‌تر است و هم به کار می‌آید:\n\n۱. اگر در خانه با تو و خواهر و برادرت آشکارا متفاوت رفتار شده، این چیزی است که پژوهش می‌شناسد و اثرش را اندازه گرفته است.\n\n۲. اگر محبت را فقط وقتی گرفته‌ای که آن‌طور بوده‌ای که خواسته شده، این «توجه مشروط» است و پیامدهایش شناخته شده است: خودارزشی نوسانی، شرم پس از شکست، خشم پنهان.\n\n۳. اگر احساست مدام غلط اعلام شده و حرفت نیمه مانده، این «کنترل روان‌شناختی» است و با افسردگی و اضطراب رابطه دارد.\n\nهیچ‌کدام این‌ها به تشخیص والد نیاز ندارد.",
              "Why we are cautious here: the online literature fits almost any parent, while the researched constructs are precise and useful."),
    confusions=[
     t("«والد من خودشیفته بود» ممکن است درست باشد و تجربهٔ شما واقعی است. آنچه این مدخل می‌گوید این است که پژوهش هنوز نمی‌تواند آن را تأیید یا رد کند؛ پس تکیه‌گاه بهتر، خودِ رفتارهاست.",
       "Your experience may be real; the point is that behaviours are a firmer footing than a diagnosis of the parent."),
     t("سرنوشت محتوم نیست. در همین فراتحلیل‌ها اندازهٔ اثرها متوسط و گاهی کوچک‌اند؛ یعنی بسیاری از این بچه‌ها بزرگسالانی سالم می‌شوند، به‌ویژه اگر یک رابطهٔ امن دیگر داشته باشند.",
       "Effect sizes are moderate or small; many of these children become healthy adults."),
    ],
    status='reviewed')

add('conditional-regard',
    title=t("توجه مشروط", "Conditional regard", "Voorwaardelijke waardering"),
    summary=t("محبتی که با عملکرد می‌آید و با شکست می‌رود. کودک آن را درونی می‌کند و بعدها خودش با خودش همین کار را می‌کند.",
              "Affection that arrives with performance and leaves with failure; the child internalises it and later does it to themselves."),
    points=[
     P("اسور، روت و دسی در دو پژوهش روی مادران و دختران و روی دانشجویان نشان دادند توجه مشروط والد، «تنظیم درون‌فکنی‌شده» می‌سازد: آدم کار را از سر اجبار درونی انجام می‌دهد، نه از سر خواستن.",
       "Assor, Roth and Deci showed conditional regard produces introjected regulation.", [s_assor]),
     P("پیامدهایش در داده دیده شد: رضایت کوتاه و زودگذر پس از موفقیت، گناه و شرم پس از شکست، و خودارزشی نوسانی؛ به‌اضافهٔ احساس طردشدگی و خشم نسبت به والد.",
       "Consequences: short-lived satisfaction after success, shame after failure, fluctuating self-worth and resentment.", [s_assor]),
     P("نکتهٔ مهم: این با «انتظار داشتن» فرق دارد. والدی می‌تواند انتظار بالا داشته باشد و در عین حال محبتش ثابت بماند. آنچه آسیب می‌زند، نوسان محبت است، نه بلندی معیار.",
       "This differs from high expectations: what harms is fluctuating affection, not a high standard.", [s_assor]),
    ],
    links=[L('psy:psychological-control', 'part-of', "یکی از شاخه‌های کنترل روان‌شناختی", "A branch of psychological control"),
           L('psy:narcissism-origins', 'explains', "یکی از مسیرها", "One of the paths"),
           L('psy:self-compassion', 'see-also', "پادزهر بزرگسالی", "The adult antidote")],
    people=[p_deci],
    status='reviewed')

add('breaking-cycle',
    title=t("شکستن چرخه", "Breaking the cycle", "De cyclus doorbreken"),
    summary=t("ترس بزرگ کسانی که در چنین خانه‌ای بزرگ شده‌اند این است: «نکند من هم همان شوم؟» خبر خوب این است که همین ترس، خودش نشانهٔ چیزی است که آن الگو را می‌شکند.",
              "The big fear of those raised this way is becoming the same; that fear is itself a sign of what breaks the pattern."),
    points=[
     P("انتقال بین‌نسلی واقعی است اما قطعی نیست: در پژوهش توجه مشروط، مادرانی که خود آن را تجربه کرده بودند بیشتر تکرارش می‌کردند — «بیشتر»، نه «همه».",
       "Intergenerational transmission is real but not deterministic.", [s_assor]),
     P("آنچه در پژوهش‌ها چرخه را می‌شکند بیشتر از آنکه «آگاهی از گذشته» باشد، تمرین رفتار تازه در موقعیت واقعی است: جمله‌ای که به‌جای جملهٔ قدیمی گفته می‌شود، و ترمیم پس از خطا.",
       "What breaks the cycle is practising new behaviour in real situations, plus repair after mistakes.", [s_gott]),
     P("از سوی عصب‌شناسی هم همین را می‌شود گفت: تجربهٔ واقعی کنترل بر موقعیت، در قشر پیش‌پیشانی تغییری پایدار می‌سازد که در برابر فشارهای بعدی سپر می‌شود. یعنی هر بار که کاری می‌کنید و اثرش را می‌بینید، چیزی در شما محکم‌تر می‌شود.",
       "Experienced control produces lasting prefrontal plasticity that buffers later adversity.", [s_barat]),
     P("و یک معیار عملی که از پژوهش زوج می‌آید: مهم‌تر از اینکه هیچ‌وقت خطا نکنید، این است که بعد از خطا ترمیم کنید. بچه‌ها در خانه‌ای که در آن عذرخواهی واقعی دیده می‌شود، چیز دیگری یاد می‌گیرند.",
       "Repair after rupture matters more than never erring.", [s_gott]),
    ],
    links=[L('psy:children-of-narcissists', 'part-of', "از این‌جا شروع شد", "Where it started"),
           L('psy:defensive-reactions', 'explains', "واکنش پیش‌فرض خودم", "My default reaction"),
           L('psy:agency', 'see-also', "حق انتخاب", "Agency")],
    try_={'text': t("یک جملهٔ تکراری از کودکی خودتان را پیدا کنید که حالا از دهان خودتان بیرون می‌آید، و فقط همان یکی را این هفته عوض کنید.",
                    "Find one sentence from your childhood that now comes out of your own mouth, and change only that one this week."),
          'tool': 'tools/sentences.html'},
    status='reviewed')

# ---------------- منابع دستهٔ چهارم ----------------
s_hepp  = src("Hepper, E. G., Hart, C. M., & Sedikides, C. (2014). Moving Narcissus: Can narcissists be empathic? Personality and Social Psychology Bulletin, 40(9), 1079–1091.", 2)
s_bame  = src("Bamelis, L. L. M., Evers, S. M. A. A., Spinhoven, P., & Arntz, A. (2014). Results of a multicenter randomized controlled trial of the clinical effectiveness of schema therapy for personality disorders. American Journal of Psychiatry, 171(3), 305–322.", 1)
s_wein  = src("Weinberg, I., & Ronningstam, E. (2022). Narcissistic personality disorder: progress in understanding and treatment. FOCUS, 20(4).", 2)
s_fayaz = src("Fayaz, I., & Dhankar, S. (2025). A systematic scoping review on exploring effective interventions for narcissistic personality disorder. Current Psychology.", 2)
s_huds  = src("Hudson, N. W., & Fraley, R. C. (2015). Volitional personality trait change: Can people choose to change their personality traits? Journal of Personality and Social Psychology, 109(3), 490–507.", 2)
s_huds19= src("Hudson, N. W., Briley, D. A., Chopik, W. J., & Derringer, J. (2019). You have to follow through: Attaining behavioral change goals predicts volitional personality change. Journal of Personality and Social Psychology.", 2)
s_sedik = src("Sedikides, C., Rudich, E. A., Gregg, A. P., Kumashiro, M., & Rusbult, C. (2004). Are normal narcissists psychologically healthy? Self-esteem matters. Journal of Personality and Social Psychology, 87(3), 400–416.", 2)
s_reis  = src("Reis, S., Huxley, E., Feng, B. E. Y., & Grenyer, B. F. S. (2021). Pathological narcissism and emotional responses to rejection: the impact of adult attachment. Frontiers in Psychology, 12, 679168.", 2)
s_golec = src("Golec de Zavala, A., Cichocka, A., Eidelson, R., & Jayawickreme, N. (2009). Collective narcissism and its social consequences. Journal of Personality and Social Psychology, 97(6), 1074–1096.", 2)
s_lev   = src("Levens, E., Malouff, J. M., & Mynadier, J. (2023). Efficacy of assertiveness training for social anxiety: a meta-analysis of randomised controlled trials.", 2)
s_adri  = src("Adriani, P. A., Hino, P., Taminato, M., et al. (2024). Non-violent communication as a technology in interpersonal relationships in health work: a scoping review. BMC Health Services Research, 24(1).", 2)
s_store = src("Storebø, O. J., et al. (2020). Psychological therapies for people with borderline personality disorder. Cochrane Database of Systematic Reviews, 5, CD012955.", 1)
s_smith = src("Smith, C. P., & Freyd, J. J. (2014). Institutional betrayal. American Psychologist, 69(6), 575–587.", 2)
p_golec = who("Agnieszka Golec de Zavala", "اگنیشکا گولچ د زاوالا", "", "روان‌شناس اجتماعی؛ سازندهٔ مفهوم «خودشیفتگی جمعی».")
p_hepp  = who("Erica Hepper", "اریکا هپر", "", "روان‌شناس؛ نشان داد همدلی در خودشیفتگی «خاموش» است نه غایب.")

# ================= ۴. قوس رابطه =================
add('relationship-arc',
    title=t("قوس رابطه: چطور شروع می‌شود و چطور تمام", "The arc: how it starts, grows and ends", "De boog van de relatie"),
    summary=t("روایت مشهور «ایده‌آل‌سازی، بی‌ارزش‌سازی، دورانداختن» پشتوانهٔ پژوهشی ندارد. اما تک‌تک رفتارهایش در پژوهش‌های دیگر مستندند، و از آن‌ها می‌شود یک قوس نسبتاً قابل‌اتکا ساخت.",
              "The famous idealise–devalue–discard arc has no research base, yet each of its behaviours is separately documented."),
    points=[
     P("نخست یک تذکر: الگوی سه‌مرحله‌ای «ایده‌آل‌سازی، بی‌ارزش‌سازی، دورانداختن» از ادبیات خودیاری و انجمن‌های اینترنتی آمده است، نه از پژوهش. یک تفسیر بالینی در ۲۰۲۵ صریح نوشت که «چرخهٔ آزار خودشیفته» هنوز تعریف استانداردی ندارد.",
       "The three-stage model comes from self-help literature; a 2025 commentary notes it has no standardised definition.", [s_ameen], ['editor-note']),
     P("نزدیک‌ترین کار داوری‌شده به توصیف این قوس، پژوهش کیفی روی شریک‌ها و خانواده‌های افراد با خودشیفتگی آسیب‌شناختی است: بزرگ‌منشی، بی‌ثباتی، کنترل و آسیب. اما همان پژوهش هم ترتیب مرحله‌ها را نیازموده است.",
       "The closest peer-reviewed description is qualitative and did not test a stage sequence.", [s_day], ['unreplicated']),
     P("آنچه در داده‌های واقعی دیده می‌شود، در پژوهش قتل همسر است: مانکتون-اسمیت با بررسی ۳۷۲ پرونده هشت مرحله را بازسازی کرد. مرحلهٔ دوم آشناست: هم‌خانه‌شدن یا بارداری شتاب‌زده، اعلام زودهنگام عشق، فشار برای تعهد سریع، و حسادت زودرس.",
       "Monckton-Smith reconstructed eight stages from 372 femicide cases; stage two is rapid commitment, fast declarations of love and early jealousy.", [s_monck]),
     P("اما این بازسازی از روی پرونده‌هایی است که به قتل رسیده‌اند. نمی‌گوید چه نسبتی از رابطه‌هایی که این نشانه‌ها را دارند جلو می‌روند — نرخ پایه معلوم نیست. این مهم‌ترین نکتهٔ احتیاطی است.",
       "This is retrospective from cases that ended in homicide; the base rate is unknown.", [s_monck], ['contested']),
     P("در محیط کار، مدل‌های مرحله‌ای قلدری هم وجود دارند (لیمان، اینارسن) اما مرور ۲۰۱۸ صریح می‌گوید تشدید در طول زمان بیشتر یک «فرض عمومی» است تا یافته: بیشتر پژوهش‌ها مقطعی‌اند و فقط «عکس فوری» می‌دهند.",
       "Workplace bullying stage models exist, but a 2018 review says escalation is a general assumption, not a finding.", [s_niel18], ['contested']),
     P("یک قوس که شواهد خوبی دارد و درست همین الگو را نشان می‌دهد، در جای دیگری است: کلاهبرداری عاشقانهٔ آنلاین. ویتی با بررسی دویست روایت و بیست مصاحبهٔ طولانی مرحله‌ها را مستند کرد: پروفایل، «آماده‌سازی» هفته‌ها تا ماه‌ها با صمیمیت شدید و اعلام عشق و بیرون‌بردن از بستر عمومی، آزمون‌های کوچک پیروی با هدیه‌های کم‌ارزش، و بعد درخواست اصلی.",
       "Whitty documented the romance-scam arc: profile, grooming with intense intimacy and small compliance tests, then the sting.", [s_whitty]),
     P("و یک عدد که جلوی زیاده‌گویی را می‌گیرد: در جمعیت عمومی جوانان، حدود ۴۴ درصد دست‌کم یک بار جدا شده و برگشته‌اند. پس «رفت‌وبرگشت» به‌تنهایی نشانهٔ هیچ‌چیز نیست.",
       "About 44% of young adults have broken up and reunited at least once — cycling alone means nothing.", [s_churn]),
    ],
    links=[L('psy:love-bombing', 'part-of', "آغاز پرشتاب", "The fast beginning"),
           L('psy:intermittent-bond', 'explains', "موتور ادامه", "The engine that keeps it going"),
           L('psy:leaving', 'part-of', "پایان و خروج", "Ending and leaving"),
           L('psy:coercive-control', 'explains', "آنچه در این مدت ساخته می‌شود", "What is built in the meantime")],
    people=[p_monck, p_whit],
    try_={'text': t("قوس را به تفکیک نقش ببینید: زوج، کار، خانواده، دوستی و فضای مجازی — با نشانه‌های هر مرحله و نقطه‌های خروج.",
                    "See the arc by role, with signs at each stage and the exit points."),
          'tool': 'tools/arc.html'},
    confusions=[
     t("«قوس» یعنی ترتیبی که در بسیاری از روایت‌ها دیده می‌شود، نه قانونی که همه از آن پیروی کنند. بسیاری از رابطه‌ها هیچ‌وقت از مرحلهٔ دوم جلوتر نمی‌روند.",
       "The arc is a frequently reported order, not a law."),
    ],
    status='reviewed')

add('love-bombing',
    title=t("آغاز پرشتاب («بمباران عشق»)", "Love bombing", "Love bombing"),
    summary=t("توجه شدید و بی‌وقفه در آغاز: پیام‌های پیاپی، اعلام زودهنگام عشق، هدیه‌های بزرگ، و حس «انگار همیشه همدیگر را می‌شناختیم». دربارهٔ خودِ این اصطلاح باید محتاط بود.",
              "Intense attention at the start: constant messages, early declarations of love, big gifts — and a term to be cautious about."),
    points=[
     P("تنها پژوهش اولیه‌ای که این اصطلاح را سنجیده، روی ۴۸۴ دانشجو در یک دانشگاه آمریکایی بوده و در یک نشریهٔ دانشجویی چاپ شده است. نتیجه‌اش همبستگی با خودشیفتگی و با عزت‌نفس پایین‌تر بود؛ ولی نمونه بسیار خاص بود و تکرار نشده است.",
       "The only primary study used 484 students and appeared in a student journal; not replicated.", [s_strut], ['unreplicated']),
     P("نکته‌ای که تقریباً هیچ‌وقت گفته نمی‌شود: در همان پژوهش، «بمباران عشق» با دلبستگی ایمن هم همبستگی مثبت داشت. یعنی بسیاری از عاشقان پرشور، فقط عاشق پرشورند.",
       "In that same study love-bombing also correlated positively with secure attachment.", [s_strut]),
     P("شواهد محکم‌تر از جای دیگری می‌آید: در بازسازی پرونده‌های قتل همسر، «اعلام سریع عشق و فشار برای تعهد زودهنگام» یکی از نشانه‌های مرحلهٔ دوم است؛ و در کلاهبرداری عاشقانهٔ آنلاین، همین صمیمیت شدید بخش مستند «آماده‌سازی» است.",
       "Stronger evidence comes from femicide-case reconstruction and from documented romance-fraud grooming.", [s_monck, s_whitty]),
     P("پس معیار عملی، شدت نیست؛ جهت است. پرسش‌های محک: آیا سرعت رابطه را هر دو انتخاب کرده‌اند؟ وقتی «نه» می‌گویید یا کُند می‌کنید چه می‌شود؟ آیا این توجه، دایرهٔ آدم‌های دیگر زندگی‌تان را کوچک می‌کند؟",
       "The test is not intensity but direction: who chose the pace, what happens when you slow it, does your world shrink?", [s_whitty, s_stark]),
    ],
    links=[L('psy:relationship-arc', 'part-of', "جای آن روی قوس", "Its place on the arc"),
           L('psy:coercive-control', 'see-also', "اگر به جداسازی برسد", "If it leads to isolation")],
    examples=[
     EX("شیمون هایوت، معروف به «کلاهبردار تیندر»: آشنایی در تیندر، زندگی پرتجمل، تماس روزانه، و بعد درخواست پول با داستان «تهدید امنیتی». یکی از زنان از ده بانک وام گرفت. روزنامهٔ نروژی VG در ۲۰۱۹ ماجرا را مستند کرد؛ او پیش‌تر در فنلاند هم محکوم شده بود.",
        "Shimon Hayut, the 'Tinder Swindler', documented by the Norwegian paper VG in 2019.",
        kind='story', label='real', source="https://www.vg.no/spesial/2019/tindersvindleren/english/"),
    ],
    confusions=[
     t("هر عشق پرشور بمباران عشق نیست؛ و هر بمباران عشق هم نقشهٔ آگاهانه نیست. بعضی آدم‌ها واقعاً این‌طور عاشق می‌شوند و بعد هم می‌مانند.",
       "Not every intense beginning is a tactic, and not every tactic is conscious."),
    ],
    status='reviewed')

add('intermittent-bond',
    title=t("تقویت نامنظم و پیوند آسیب", "Intermittent reinforcement and trauma bonding", "Intermitterende bekrachtiging"),
    summary=t("چرا ماندن سخت‌تر از رفتن می‌شود: وقتی مهربانی و بدرفتاری نامنظم و پیش‌بینی‌ناپذیر در هم بیایند، دلبستگی قوی‌تر می‌شود، نه ضعیف‌تر.",
              "Why leaving gets harder: unpredictable alternation of kindness and harm strengthens attachment."),
    points=[
     P("داتن و پینتر در ۱۹۸۱ نظریهٔ «پیوند آسیب‌زا» را با دو شرط صورت‌بندی کردند: نابرابری قدرت، و رفتار خوب و بد به‌صورت نامنظم. در آزمون تجربی‌شان روی ۷۵ زنی که تازه رابطه را ترک کرده بودند، نامنظم‌بودن بدرفتاری و تغییر توازن قدرت از قوی‌ترین پیش‌بین‌های دلبستگی پس از جدایی بود.",
       "Dutton and Painter's traumatic bonding theory: power imbalance plus intermittency predicted post-separation attachment in 75 women.", [s_dutt], ['unreplicated']),
     P("اصل یادگیری پشتش قدیمی و محکم است: پاداش نامنظم، رفتار را از پاداش همیشگی مقاوم‌تر می‌کند. اما به‌کاربردنش برای رابطهٔ انسانی یک قیاس است، نه سازوکاری که مستقیم آزموده شده باشد.",
       "Intermittent reinforcement is a solid learning principle, but its application here is an analogy.", [s_dutt], ['editor-note']),
     P("تحلیل تازه‌تری پیشنهاد می‌کند این پیوند را نه ضعف قربانی، بلکه بخشی از سامانهٔ کنترلی که عامل آن را می‌سازد بدانیم. این بازقاب‌بندی برای کسی که از خودش می‌پرسد «چرا نرفتم؟» مهم است.",
       "A recent analysis reframes trauma bonding as part of the perpetrator's coercive system, not a failing of the victim.", [s_lesi]),
     P("یک هشدار: «سندرم استکهلم» که معمولاً کنار این بحث می‌آید، در مرور نظام‌مند تنها دوازده مقاله داشت که بیشترشان گزارش موردی بودند؛ معیار تشخیصی معتبر ندارد و در هیچ طبقه‌بندی بین‌المللی نیست.",
       "Stockholm syndrome has no validated criteria and appears in no classification.", [s_namn], ['contested']),
    ],
    links=[L('psy:relationship-arc', 'part-of', "موتور قوس", "The engine of the arc"),
           L('psy:leaving', 'explains', "چرا خروج چندباره است", "Why leaving takes several attempts"),
           L('psy:victim-toll', 'see-also', "اثرش بر تن و روان", "The toll")],
    explain=t("چرا بی‌ثباتی می‌چسباند و ثبات نه؟\n\nاگر کسی همیشه بد باشد، تصمیم ساده است. اگر همیشه خوب باشد، تصمیمی لازم نیست. آنچه آدم را میخکوب می‌کند، حالت سوم است: گاهی خوب، گاهی بد، بی‌آنکه بدانی کِی.\n\nدر این حالت، ذهن تمام توانش را می‌گذارد روی پیدا کردن قاعده: «اگر آن‌طور بگویم خوب می‌شود؟» و هر بار که دورهٔ خوب برمی‌گردد، این باور تأیید می‌شود که «پس می‌شود درستش کرد». همان دورهٔ خوب، نه دورهٔ بد، چیزی است که ماندن را ممکن می‌کند.\n\nو برای کسی که بیرون ایستاده و می‌پرسد «چرا نمی‌رود؟»: این سؤال، پاسخش در شخصیت آن آدم نیست. در ساختار موقعیت است.",
              "Unpredictable alternation, not constant badness, is what fixes attention and keeps hope alive."),
    status='reviewed')

add('leaving',
    title=t("خروج: چرا سخت است و کِی خطرناک", "Leaving: why it is hard and when it is dangerous", "Weggaan"),
    summary=t("ترک چنین رابطه‌ای معمولاً یک تصمیم نیست، یک فرایند است. و درست برخلاف تصور رایج، خطرناک‌ترین دوره لحظهٔ جدایی و ماه‌های پس از آن است.",
              "Leaving is a process, not a decision — and the most dangerous period is separation and the months after."),
    points=[
     P("مرور تجربی اندرسون و ساندرز نشان داد خروج چندمرحله‌ای است: آدم‌ها ممکن است چند بار بروند و برگردند در حالی که مهارت و منابع جمع می‌کنند. دو خانوادهٔ پیش‌بین: منابع عملی (کار، درآمد) و عوامل روانی-اجتماعی.",
       "Anderson and Saunders showed leaving is multi-phase, predicted by practical resources and social-psychological factors.", [s_ander]),
     P("ادعای رایج «زن‌ها به‌طور میانگین هفت بار برمی‌گردند» منبع پژوهشی ندارد و در سازمان‌های حمایتی بدون ارجاع دست‌به‌دست شده است. آنچه می‌شود گفت: رفت‌وبرگشت رایج است، نه اینکه عددش معلوم باشد.",
       "The 'leaves seven times on average' claim has no research source.", [s_ander], ['contested']),
     P("خطر: در پژوهش‌های قتل همسر، سه ماه نخست و سال نخست پس از جدایی خطرناک‌ترین دوره‌اند؛ و جدایی فیزیکی همراه با اقدام قانونی بیشترین خطر را داشته است. تا ۹۰ درصد زنان از ادامهٔ آزار، تعقیب یا مزاحمت پس از جدایی گزارش می‌دهند.",
       "The first three months and first year after separation are the most lethal; up to 90% report continued post-separation abuse.", [s_spear]),
     P("یک نشانهٔ خطر که در پژوهش عدد روشنی دارد: خفه‌کردن غیرکشنده. در پژوهش یازده‌شهری، سابقهٔ خفه‌کردن در ۱۰ درصد گروه مقایسه دیده شد و در ۴۳ تا ۴۵ درصد پرونده‌های قتل و اقدام به قتل؛ یعنی چند برابر شدن خطر.",
       "Prior non-fatal strangulation appeared in 10% of abused controls versus 43–45% of homicide and attempted-homicide cases.", [s_glass]),
     P("و یک یافتهٔ تلخ اما مهم برای انتظارها: در همان مرورها، بعضی زنان بلافاصله پس از خروج از نظر روانی بدتر از کسانی‌اند که هنوز مانده‌اند. آزار پس از جدایی، سختی مالی و تنهایی دلیلش است — نه اشتباه‌بودن تصمیم.",
       "Some women are psychologically worse off just after leaving, because of post-separation abuse and hardship.", [s_ander, s_spear]),
    ],
    links=[L('psy:relationship-arc', 'part-of', "پایان قوس", "The end of the arc"),
           L('psy:intermittent-bond', 'explains', "چرا برگشتن رایج است", "Why returning is common"),
           L('psy:recovery', 'see-also', "بعدش چه می‌شود", "What comes after")],
    examples=[
     EX("سالی چالن، انگلستان: ازدواجی چهل‌ساله که دادگاه بعدها آن را کنترل، جداسازی و تحقیر توصیف کرد. در ۲۰۱۰ شوهرش را کشت و به حبس ابد محکوم شد؛ در ۲۰۱۹ دادگاه تجدیدنظر حکم قتل عمد را لغو کرد و با پذیرش «مسئولیت کاهش‌یافته» آزاد شد. پرونده‌اش در بریتانیا نقطهٔ عطفی در فهم کنترل اجباری بود.",
        "Sally Challen: her murder conviction was quashed in 2019 after coercive control was recognised as context.",
        kind='story', label='real', source="BBC News / The Guardian, 2019"),
     EX("مونا حیدری، اهواز: در ۱۲ سالگی به عقد پسرعمویش درآمد و در ۱۴ سالگی مادر شد. از خانه گریخت و به ترکیه رفت؛ بستگان او را بازگرداندند و در بهمن ۱۴۰۰ به دست شوهر و برادر شوهرش کشته شد. دیدبان حقوق بشر و رسانه‌های داخلی و خارجی ماجرا را ثبت کردند؛ همسرش در دی ۱۴۰۱ به کمی بیش از هشت سال حبس محکوم شد.",
        "Mona Heydari, Ahvaz: forced early marriage, flight, forced return, and lethal escalation at separation.",
        kind='iran', label='real', source="https://www.hrw.org/news/2022/02/11/gruesome-femicide-iran"),
    ],
    status='reviewed')

# ================= ۵. نقش‌ها =================
add('control-at-work',
    title=t("در محیط کار", "Control at work", "Controle op het werk"),
    summary=t("همان الگوها، با ابزارهای سازمانی: دسترسی، پروژه، ارزیابی و آبرو. در این‌جا تنها جایی است که «درخشان در آغاز، فرساینده در ادامه» عدد و داده دارد.",
              "The same patterns with organisational tools — and the one domain where 'bright at first, corrosive later' has numbers."),
    points=[
     P("فراتحلیل شیوع نشان می‌دهد حدود ۱۵ درصد کارکنان در جهان قلدری در محیط کار را تجربه کرده‌اند؛ عدد با روش سنجش تغییر می‌کند (از ۱۱ تا ۱۸ درصد).",
       "A meta-analysis puts workplace bullying prevalence around 15%, varying with measurement method.", [s_niel10]),
     P("در ادبیات رهبری، خودشیفتگی «به رهبری رسیدن» را پیش‌بینی می‌کند (همبستگی حدود ۰٫۱۶) ولی اثربخشی به‌صورت خطی نه (حدود ۰٫۰۳ و بی‌معنا). شکاف مهم این است: خودشیفته‌ها خودشان را بسیار اثربخش ارزیابی می‌کنند (۰٫۲۹) ولی همکاران چنین نمی‌بینند (۰٫۰۲).",
       "Narcissism predicts leader emergence (ρ=.16) but not effectiveness (ρ=.03); self-ratings .29 versus peer ratings .02.", [s_grij]),
     P("رابطهٔ رهبر و زیردست در طول زمان افت می‌کند و همان جذابیت اولیه کم‌رنگ می‌شود؛ در سطح تیم، رهبران خودشیفته با تبادل اطلاعات کمتر و عملکرد پایین‌تر تیم همراه‌اند.",
       "Leader–follower relationships deteriorate over time; teams show less information exchange and lower performance.", [s_braun]),
     P("مدل‌های مرحله‌ای قلدری (از رفتارهای پراکنده تا انگ‌زنی و در نهایت بیرون‌رفتن از سازمان) وجود دارند، اما مرور ۲۰۱۸ هشدار می‌دهد که تشدید در طول زمان بیشتر فرض است تا یافته. آنچه عدد دارد: میانگین مدت در پژوهش‌های مختلف از شش تا شصت‌ودو ماه، و خطر بالاتر بیکاری و مرخصی طولانی تا دو تا پنج سال بعد.",
       "Stage models exist but escalation is an assumption; durations range from 6 to 62 months with elevated risk 2–5 years later.", [s_niel18], ['contested']),
    ],
    links=[L('psy:public-private', 'explains', "چرا بیرون کسی باور نمی‌کند", "Why outsiders don't believe it"),
           L('psy:control-behaviors', 'applies-to', "دسته‌های رفتاری در کار", "The behaviour classes at work"),
           L('psy:p-io', 'part-of', "روان‌شناسی سازمانی", "Organisational psychology")],
    people=[p_einar],
    examples=[
     EX("برودی پنلاک، ملبورن: نوجوانی که در یک کافه کار می‌کرد و بنا بر یافتهٔ دادگاه «به‌طور نظام‌مند، جسمی و روانی» آزار دید؛ همکاران دخالت کردند و مالک بی‌اعتنا ماند. او در ۲۰۰۶ جانش را از دست داد. در ۲۰۱۰ چهار نفر و یک شرکت به جریمه‌هایی در مجموع ۳۳۵ هزار دلار محکوم شدند و در ۲۰۱۱ قانون ویکتوریا («قانون برودی») آزار جدی را با حداکثر ده سال حبس جرم شناخت.",
        "Brodie Panlock, Melbourne: systematic workplace bullying that led to her death, convictions in 2010 and 'Brodie's Law' in 2011.",
        kind='story', label='real', source="https://www.justice.vic.gov.au/saynotobullying"),
    ],
    status='reviewed')

add('control-in-family',
    title=t("در خانواده و قطع رابطه", "In the family, and estrangement", "In het gezin"),
    summary=t("خانواده جایی است که رفتن سخت‌ترین است. قطع رابطه با یکی از اعضای خانواده بسیار رایج‌تر از چیزی است که تصور می‌شود — و اغلب برگشت‌پذیر.",
              "Family is where leaving is hardest; estrangement is far more common than assumed, and often reversible."),
    points=[
     P("در پیمایش ملی آمریکا با بیش از ۱۳۰۰ بزرگسال، ۲۷ درصد گفتند با یکی از اعضای خانواده قطع رابطه کرده‌اند؛ ۱۰ درصد با والد یا فرزند، ۸ درصد با خواهر یا برادر.",
       "In a US national survey, 27% had cut off contact with a family member.", [s_pill]),
     P("داده‌های طولی تصویر کامل‌تری می‌دهند: ۶ درصد دوره‌ای از قطع رابطه با مادر و ۲۶ درصد با پدر گزارش کردند؛ میانگین سن نخستین قطع رابطه ۲۶ سال (مادر) و ۲۳ سال (پدر) بود. مهم‌تر: ۸۱ درصد قطع‌رابطه‌ها با مادر و ۶۹ درصد با پدر در ادامه پایان یافتند.",
       "Longitudinal data: 6% estranged from mothers, 26% from fathers; most episodes ended.", [s_recz]),
     P("پژوهش قطع رابطه عمدتاً دربارهٔ خودشیفتگی نیست؛ نسبت‌دادن هر قطع رابطه‌ای به «والد خودشیفته» استنتاجی است که این ادبیات نمی‌کند.",
       "Estrangement research is largely not about narcissism; attributing it to a narcissistic parent is an inference the literature does not make.", [s_recz], ['editor-note']),
     P("آنچه در خانواده اثر مستقیم دارد و اندازه‌گیری شده، رفتار متفاوت والد با فرزندان است: فرزندی که کمتر مورد لطف است، مشکلات درونی‌شده و بیرونی‌شدهٔ بیشتری دارد.",
       "Parental differential treatment is measured and matters: the less-favoured child shows more problems.", [s_jens]),
    ],
    links=[L('psy:children-of-narcissists', 'part-of', "بچه‌ها", "The children"),
           L('psy:soc-family', 'part-of', "جامعه‌شناسی خانواده", "Sociology of the family"),
           L('psy:boundaries', 'see-also', "مرز بدون قطع رابطه", "Boundaries short of cutting off")],
    people=[p_pill],
    status='reviewed')

add('control-online',
    title=t("آنلاین و در گروه‌ها", "Online and in groups", "Online en in groepen"),
    summary=t("در فضای مجازی و در گروه‌های بسته، همان الگو با سرعت بیشتر کار می‌کند: صمیمیت شتاب‌زده، جداسازی از منتقدان، و آزمون‌های کوچکِ پیروی که بزرگ‌تر می‌شوند.",
              "Online and in closed groups the same pattern runs faster: fast intimacy, isolation from critics, escalating compliance tests."),
    points=[
     P("ویتی با بررسی دویست روایت قربانی و مصاحبه‌های طولانی، مرحله‌های کلاهبرداری عاشقانه را مستند کرد و نشان داد «هدیه‌های کوچک» در مرحلهٔ آماده‌سازی در واقع آزمون پیروی‌اند، نه ابراز علاقه.",
       "Whitty documented romance-scam stages and showed small gift requests function as compliance tests.", [s_whitty]),
     P("لیفتون در ۱۹۶۱ هشت ویژگی «تمامیت‌خواهی ایدئولوژیک» را فهرست کرد؛ از جمله کنترل محیط اطلاعاتی، اعتراف، زبان ویژه، و «تعیین حق وجود». این فهرست کلاسیک است، اما خودِ مفهوم «شست‌وشوی مغزی» در جامعه‌شناسی دین محل بحث است.",
       "Lifton's eight criteria of ideological totalism remain classic, though 'brainwashing' is contested in sociology of religion.", [s_lift], ['contested']),
     P("لالیش با مقایسهٔ دو گروه مفهوم «انتخاب محدودشده» را پیشنهاد کرد: عضو واقعاً انتخاب می‌کند، اما در سامانه‌ای که خودش گزینه‌ها را تنگ کرده است. این قاب برای فهم «چرا نرفت؟» دقیق‌تر از «فریب خورد» است.",
       "Lalich's bounded choice: members really choose, inside a system that has narrowed the options.", [s_lal]),
     P("نمونهٔ مستند و حقوقی‌اش: در پروندهٔ نکسیوم، گروهی که خود را «خودیاری» و بعد «شبکهٔ راهنمایی زنان» معرفی می‌کرد، از اعضا «وثیقه» می‌گرفت — اعتراف‌های آسیب‌زننده و عکس — تا امکان ترک گروه یا افشاگری را بگیرد. رهبر گروه در ۲۰۲۰ به ۱۲۰ سال زندان محکوم شد.",
       "NXIVM collected 'collateral' from members to prevent leaving; its leader was sentenced to 120 years in 2020.", [s_lal], ),
    ],
    links=[L('psy:love-bombing', 'see-also', "همان آغاز، سریع‌تر", "The same opening, faster"),
           L('psy:coercive-control', 'applies-to', "کنترل بیرون از رابطهٔ عاطفی", "Control outside intimate relationships"),
           L('psy:conspiracy', 'see-also', "باور گروهی و بستگی", "Group belief and closure")],
    examples=[
     EX("لارنس ری و دانشجویان کالج سارا لارنس: او از حدود ۲۰۱۰ در اتاق خوابگاه دخترش ساکن شد و طی سال‌ها بر گروهی از دانشجویان تسلط یافت — بی‌خوابی، تحقیر، تهدید، جداکردن از خانواده، و گرفتن «اعتراف»‌های ساختگی که بعد ابزار اخاذی شد. در ۲۰۲۳ به ۶۰ سال زندان محکوم شد.",
        "Lawrence Ray and Sarah Lawrence College students: sentenced to 60 years in 2023.",
        kind='story', label='real', source="https://www.justice.gov/usao-sdny/pr/lawrence-ray-sentenced-years-long-predatory-crimes-against-students-sarah-lawrence"),
    ],
    status='reviewed')

# ================= ۶. آنچه بر تن و روان می‌گذرد =================
add('victim-toll',
    title=t("آنچه بر تن و روان می‌گذرد", "What it does to body and mind", "Wat het doet met lichaam en geest"),
    summary=t("زندگی طولانی زیر کنترل، فقط «حال بد» نیست. خواب، خلق، حافظه، ایمنی و احساس ارزش را دست می‌زند. اما باید دقیق بود: بیشتر این پژوهش‌ها دربارهٔ خشونت خانگی و بدرفتاری روانی‌اند، نه دربارهٔ «آزار خودشیفته».",
              "Living under long-term control affects sleep, mood, memory, immunity and self-worth — with the caveat that most research is on IPV and psychological abuse."),
    points=[
     P("یک تذکر لازم: «آزار خودشیفته» مقولهٔ تشخیصی یا پژوهشی نیست و دربارهٔ آن ادبیات زیستی-پزشکی وجود ندارد. آنچه هست، پژوهش دربارهٔ استرس مزمن بین‌فردی، خشونت خانگی، و بدرفتاری روانی است.",
       "'Narcissistic abuse' is not a diagnostic or research category; the literature is on chronic interpersonal stress, IPV and psychological maltreatment.", [s_dokk], ['editor-note']),
     P("خلق: در فراتحلیل گلدینگ، میانگین شیوع افسردگی در زنان با سابقهٔ خشونت شریک ۴۷٫۶ درصد، اختلال استرس پس از سانحه ۶۳٫۸ درصد و افکار خودکشی ۱۷٫۹ درصد بود. در مرورهای تازه‌تر روی بیش از ۲۵۰ هزار زن، نسبت شانس افسردگی دو تا سه برابر و خودکشی‌گرایی دو تا پنج برابر است.",
       "Golding's meta-analysis: depression 47.6%, PTSD 63.8%, suicidality 17.9% among women with IPV history.", [s_golding, s_white]),
     P("رابطه دوطرفه است: در مرور مطالعات طولی، خشونت شریک علائم افسردگی بعدی را پیش‌بینی می‌کند (نسبت شانس حدود ۲) و علائم افسردگی هم خشونت بعدی را. پس «افسرده بود، برای همین…» توضیح کاملی نیست.",
       "The relationship is bidirectional in longitudinal studies.", [s_devr]),
     P("و بخش روانیِ آزار، بی‌اثر نیست: در مرور نظام‌مند روی نزدیک دویست پژوهش، خشونت روانی قوی‌ترین پیوند را با اختلال استرس پس از سانحه داشت و کنترل اجباری به‌طور خاص با همین. خودِ نویسندگان قطعیت شواهد را «پایین» درجه‌بندی کردند.",
       "Psychological violence showed the strongest association with PTSD; the authors graded certainty as low.", [s_dokk], ['contested']),
     P("تن: استرس مزمن محور هورمونی استرس را به‌هم می‌ریزد، ولی جهتش یکسان نیست — بسته به مدت، ادامه‌دار بودن و وجود اختلال استرس پس از سانحه، کورتیزول می‌تواند بالا یا پایین باشد. آنچه باثبات‌تر است: مسطح‌شدن شیب روزانهٔ کورتیزول، که با سلامت بدتر همراه است (همبستگی حدود ۰٫۱۵، بیشترین اثر روی شاخص‌های ایمنی و التهاب).",
       "Chronic stress dysregulates the HPA axis in a mixed direction; flatter diurnal slopes track worse health.", [s_miller, s_adam]),
     P("خواب: در نمونه‌ای از ۱۲۱ زن در معرض خشونت شریک، ۴۶ درصد بی‌خوابی بالینی و ۳۲ درصد کابوس داشتند؛ و بی‌خوابی، مستقل از شدت علائم استرس پس از سانحه، با چند برابر شدن شانس افسردگی همراه بود.",
       "Among 121 IPV-exposed women, 46% had clinical insomnia and 32% nightmares.", [s_pig]),
     P("بدن در بلندمدت: تجربه‌های ناگوار کودکی رابطهٔ پلکانی روشنی با بیماری و رنج بزرگسالی دارند؛ در فراتحلیل بیش از ۲۵۰ هزار نفر، کسانی با چهار تجربهٔ ناگوار یا بیشتر، نسبت شانس بالاتری برای افسردگی (۴٫۴)، بیماری تنفسی (۳٫۱) و بیماری قلبی-عروقی (۲٫۱) داشتند.",
       "ACEs show a graded dose-response with adult disease and distress.", [s_felit, s_hughes]),
     P("التهاب: تروماهای کودکی با نشانگرهای التهابی بالاتر در بزرگسالی همراه‌اند، هرچند اندازهٔ اثرها کوچک است. چارچوب توضیحی‌اش «بار آلوستاتیک» مک‌اوئن است: همان سازوکارهایی که در کوتاه‌مدت محافظت می‌کنند، در فعال‌ماندن طولانی فرسایش می‌سازند.",
       "Childhood trauma is linked to higher adult inflammation, with small effect sizes; the frame is allostatic load.", [s_baum, s_mcew]),
     P("درد و نشانه‌های جسمی: در یک همگروه بزرگ مراقبت اولیه با بیش از ۸۰ هزار بزرگسال با سابقهٔ بدرفتاری کودکی، نرخ فیبرومیالژیا حدود دو برابر و کمردرد مزمن حدود دو برابر گروه مقایسه بود؛ ولی برای چند سندرم دیگر تفاوتی دیده نشد.",
       "In a large cohort, maltreatment-exposed adults had about twice the rate of fibromyalgia and chronic back pain — but not of several other syndromes.", [s_chand]),
     P("عزت‌نفس: این ضعیف‌ترین حلقهٔ شواهد است و باید صادق بود. یک پژوهش طولی روی ۷۲۶ زن جوان نشان داد خشونت <b>روانی</b> پیشین، عزت‌نفس پایین بعدی را پیش‌بینی می‌کند، در حالی که خشونت جسمی این کار را نمی‌کند. فراتحلیلی دربارهٔ مسیر عزت‌نفس زیر انتقاد مزمن وجود ندارد.",
       "Past psychological IPV predicted later low self-esteem; physical IPV did not. There is no meta-analysis of self-esteem trajectories.", [s_shen], ['unreplicated']),
    ],
    links=[L('psy:cptsd', 'explains', "وقتی به تشخیص می‌رسد", "When it reaches a diagnosis"),
           L('psy:self-trust', 'part-of', "شک به ادراک خود", "Doubting one's own perception"),
           L('psy:recovery', 'see-also', "بعد از ایمنی چه می‌شود", "What happens after safety"),
           L('psy:n-stress', 'part-of', "استرس و محور HPA", "Stress and the HPA axis")],
    people=[p_felit],
    try_={'text': t("نقشهٔ تن و روان: روی هر دستگاه بزنید و ببینید چه تغییری گزارش شده، با چه اندازه شواهدی، و چه چیزی کمک می‌کند.",
                    "A body-and-mind map: what changes, with what evidence, and what helps."),
          'tool': 'tools/toll.html'},
    confusions=[
     t("«این نشانه‌ها را دارم، پس حتماً آزار دیده‌ام» درست نیست. همین نشانه‌ها از ده‌ها علت دیگر هم می‌آیند. رابطه در جهت دیگر محکم‌تر است: آزار طولانی، این نشانه‌ها را بیشتر می‌کند.",
       "Having these symptoms does not prove abuse; the inference runs the other way."),
    ],
    status='reviewed')

add('cptsd',
    title=t("استرس پس از سانحهٔ پیچیده (CPTSD)", "Complex PTSD", "Complexe PTSS"),
    summary=t("تشخیصی که از ۲۰۱۸ در طبقه‌بندی جهانی بیماری‌ها آمد و دقیقاً برای آسیب‌های طولانی و تکراری ساخته شده است — به‌ویژه وقتی از کسی آمده باشد که باید پناه می‌بود.",
              "A diagnosis added to ICD-11 in 2018 for prolonged, repeated trauma, especially from someone who should have been safety."),
    points=[
     P("سه خوشهٔ استرس پس از سانحه (بازتجربهٔ اکنونی، اجتناب، حس تهدید دائمی) به‌اضافهٔ سه «اختلال در خودسامانی»: دشواری تنظیم هیجان، باور به بی‌ارزشی و شکست‌خوردگی خود، و دشواری در حفظ رابطه و احساس نزدیکی.",
       "The three PTSD clusters plus three disturbances in self-organisation.", [s_icd]),
     P("تفاوت اصلی‌اش با استرس پس از سانحه در همین خوشهٔ سوم است، نه در شدت بیشتر کابوس‌ها.",
       "The difference from PTSD is the self-organisation cluster, not more severe flashbacks.", [s_icd]),
     P("در نمونهٔ جمعیتی آمریکا، شیوع استرس پس از سانحه ۳٫۴ درصد و نوع پیچیده ۳٫۸ درصد بود. تروماهای انباشتهٔ کودکی و به‌ویژه آزار توسط مراقب، با نوع پیچیده رابطهٔ قوی‌تری داشتند.",
       "In a US population sample, PTSD 3.4% and CPTSD 3.8%; caregiver-perpetrated abuse specifically predicted CPTSD.", [s_cloit]),
     P("یک صداقت لازم: مرز این تشخیص با اختلال شخصیت مرزی روشن نیست و همپوشانی زیادی دارند؛ پژوهش‌ها هنوز بر سر این مرز بحث دارند.",
       "Its boundary with borderline personality disorder is genuinely blurred.", [s_cloit], ['contested']),
    ],
    links=[L('psy:victim-toll', 'part-of', "بخشی از اثر", "Part of the toll"),
           L('psy:recovery', 'see-also', "درمان‌هایی که شواهد دارند", "Treatments with evidence"),
           L('psy:ptsd', 'part-of', "استرس پس از سانحه", "PTSD")],
    people=[p_cloit],
    status='reviewed')

# ================= ۷. بیرون آمدن: حق انتخاب و بهبود =================
add('agency',
    title=t("حق انتخاب: درماندگی آموخته نمی‌شود، کنترل آموخته می‌شود", "Agency: helplessness is not learned, control is", "Keuzevrijheid"),
    summary=t("مهم‌ترین تصحیح علمی این حوزه: پنجاه سال فکر می‌کردیم آدم «درماندگی» را یاد می‌گیرد. مایر و سلیگمن نشان دادند وارونه است — بی‌عملی پاسخ پیش‌فرض است و این «کنترل» است که آموخته می‌شود.",
              "The key correction: passivity is the default response to prolonged uncontrollable adversity; what is learned is control."),
    points=[
     P("مایر و سلیگمن در بازنگری پنجاه‌سالهٔ «درماندگی آموخته‌شده» نوشتند نظریهٔ اولیه وارونه بود: بی‌عملی در برابر رنج طولانی، پاسخ نیاموختهٔ پیش‌فرض پستانداران است و با فعالیت هستهٔ رافهٔ پشتی وساطت می‌شود. آنچه یاد گرفته می‌شود، <b>کنترل</b> است، با فعال‌شدن قشر پیش‌پیشانی میانی.",
       "Maier and Seligman: passivity is the unlearned default; control is what gets learned, via medial prefrontal activity.", [s_maier]),
     P("پیامد عملی‌اش بزرگ است: اگر کسی پس از سال‌ها کنترل «نمی‌تواند تکان بخورد»، درس بدی نگرفته و ضعیف نیست؛ در وضعیت پیش‌فرض گیر کرده است. و راه بیرون، قانع‌کردن خود نیست؛ تجربهٔ واقعی اثرگذاری است.",
       "Someone frozen after years of control has not learned a bad lesson; they are in the default state, and the way out is experienced control.", [s_maier, s_barat]),
     P("در پژوهش‌های بعدی نشان داده شد تجربهٔ کنترل، تغییری پایدار در همان مسیر پیش‌پیشانی می‌سازد که در برابر فشارهای بعدی سپر می‌شود. یعنی هر تجربهٔ کوچک اثرگذاری، سرمایه‌گذاری برای دفعهٔ بعد است.",
       "Experienced control produces lasting plasticity that buffers later adversity.", [s_barat]),
     P("و یک یافته دربارهٔ شکل درستِ گام‌ها: در پژوهش‌های تغییر ارادی شخصیت، کسانی که «چالش‌های کوچک را تمام کردند» رشد نشان دادند؛ کسانی که چالش پذیرفتند ولی تمام نکردند، حتی پس‌رفت داشتند. پس تصمیم بزرگ نگیرید؛ گام کوچکِ قطعاً شدنی بردارید.",
       "Completing small challenges predicts growth; accepting but not completing predicts decline.", [s_huds, s_huds19]),
    ],
    links=[L('psy:karpman-triangle', 'explains', "بیرون آمدن از نقش قربانی", "Moving out of the victim role"),
           L('psy:victim-mindset', 'contrasts', "تفاوت قربانی‌شدن و نقش قربانی", "Being victimised versus the victim role"),
           L('psy:recovery', 'part-of', "بخشی از بهبود", "Part of recovery"),
           L('psy:stoicism', 'see-also', "آنچه دست ماست و آنچه نیست", "What is up to us and what is not")],
    people=[p_maier, p_selig],
    explain=t("سه کار که از دل همین یافته بیرون می‌آید:\n\n<b>۱. سه ستون بنویسید.</b> «دست من»، «دست او»، «دست هیچ‌کس». بیشتر انرژی ما خرج ستون دوم می‌شود، که هیچ‌وقت نتیجه نمی‌دهد. ستون اول هیچ‌وقت کاملاً خالی نیست.\n\n<b>۲. گام را آن‌قدر کوچک کنید که شکست ممکن نباشد.</b> نه «رابطه را تمام می‌کنم»، بلکه «فردا به خواهرم زنگ می‌زنم». پژوهش می‌گوید گام تمام‌شده رشد می‌سازد و گام نیمه‌تمام، پس‌رفت.\n\n<b>۳. اثرش را ببینید.</b> همان‌جا بنویسید چه شد. مغز به مدرک نیاز دارد، نه به نیت.\n\nاین با «مثبت‌اندیشی» فرقی اساسی دارد: این‌جا کسی نمی‌گوید اوضاع خوب است یا همه‌چیز دست شماست. می‌گوید عضله‌ای که از کار افتاده، با حرکت برمی‌گردد، نه با حرف.",
              "Three columns, a step too small to fail, and recording the effect."),
    try_={'text': t("شش گام برای بیرون آوردن یک موقعیت واقعی از مثلث، با یک کارت قابل‌کپی در پایان.", "Six steps to take a real situation out of the triangle."),
          'tool': 'tools/triangle.html'},
    status='reviewed')

add('self-trust',
    title=t("بازسازی اعتماد به ادراک خود", "Rebuilding trust in your own perception", "Vertrouwen in je eigen waarneming"),
    summary=t("چیزی که بعد از سال‌ها بی‌اعتبارسازی بیشتر از همه آسیب می‌بیند، توانایی تکیه بر حافظه و قضاوت خود است. این بخش، بازسازی همان است.",
              "What years of invalidation damages most is the ability to rely on one's own memory and judgement."),
    points=[
     P("سوئیت نشان داد گازلایتینگ وقتی کار می‌کند که نابرابری و کلیشه‌های اجتماعی از پیش حرف یک طرف را بی‌اعتبار کرده باشند؛ او وضعیت حاصل را «فراواقعیت» می‌نامد: جایی که آدم دیگر نمی‌داند کدام نسخه از ماجرا را باور کند.",
       "Sweet showed gaslighting works through social inequality, producing a state she calls 'surreality'.", [s_sweet]),
     P("فیلسوف میراندا فریکر همین را از زاویهٔ دیگری نام‌گذاری کرده است: «بی‌عدالتی شهادتی» یعنی باور نشدن به‌خاطر اینکه چه کسی هستی. این فلسفه است، نه پژوهش تجربی، ولی تجربهٔ آدم‌ها را دقیق نام می‌برد.",
       "Fricker's testimonial injustice names the experience, though it is philosophy rather than empirical research.", [s_sweet], ['editor-note']),
     P("یک سازهٔ سنجیدنی در این میانه هست: «شفافیت خودپنداره» — اینکه آدم تصویر روشن و باثباتی از خودش دارد یا نه. در پژوهشی کوچک، همین شفافیت نقش سپر داشت: در کسانی که آن را بالا داشتند، پیوند آسیب گذشته با نشانه‌های جدایی از خود معنادار نبود.",
       "Self-concept clarity buffered the link between abuse and depersonalisation in a small study.", [s_shen], ['unreplicated']),
     P("دانستن نام الگو، خودش سپر است: در آزمایش، کسانی که توضیح کوتاهی دربارهٔ الگوی DARVO خوانده بودند، بعد قربانی را باورپذیرتر ارزیابی کردند.",
       "Being briefly taught the DARVO pattern increased later belief in victims.", [s_darvo]),
    ],
    links=[L('psy:gaslighting', 'part-of', "آنچه این را خراب می‌کند", "What damages it"),
           L('psy:darvo', 'see-also', "نام‌گذاری الگو", "Naming the pattern"),
           L('psy:agency', 'see-also', "گام بعدی", "The next step")],
    explain=t("چهار کار که در عمل کمک می‌کند:\n\n<b>یادداشت ساده و تاریخ‌دار.</b> نه برای اثبات به او — برای خودتان. دو خط: چه شد، چه گفته شد، چه حسی داشتم. وقتی بعداً به حافظه‌تان شک کردید، مدرک دارید.\n\n<b>یک آدم بیرونی.</b> کسی که ماهی یک بار ماجرا را برایش تعریف کنید. نه برای مشورت؛ برای اینکه نسخهٔ شما جایی بیرون از آن رابطه هم وجود داشته باشد.\n\n<b>جدا کردن دو پرسش.</b> «چه شد؟» و «حق با کی بود؟» دومی تلهٔ گفت‌وگوست. اولی را می‌شود نوشت.\n\n<b>بازگرداندن قضاوت‌های کوچک.</b> از چیزهای کم‌خطر شروع کنید: چه بخوریم، چه فیلمی ببینیم، کدام مسیر. اعتماد به قضاوت، مثل هر مهارت دیگر، با تکرار کوچک برمی‌گردد.",
              "Four practical moves: dated notes, an outside person, separating 'what happened' from 'who was right', and rebuilding small judgements."),
    status='reviewed')

add('self-silencing',
    title=t("خاموش کردن خود", "Self-silencing", "Jezelf het zwijgen opleggen"),
    summary=t("عادتِ نگفتن: فرو خوردن خواسته و خشم برای حفظ رابطه. دانا جک نشان داد این الگو با افسردگی رابطه دارد — و اینکه در چه فرهنگی زندگی می‌کنید، فرق می‌گذارد.",
              "The habit of not saying: swallowing wants and anger to preserve a relationship."),
    points=[
     P("جک این سازه را در ۱۹۹۱ صورت‌بندی کرد و با دیل سنجه‌اش را ساخت. ایده: برای نگه‌داشتن رابطه، آدم صدای خودش را خاموش می‌کند و کم‌کم از خودِ واقعی‌اش فاصله می‌گیرد.",
       "Jack formulated self-silencing in 1991 and built a scale with Dill.", [s_jackd]),
     P("در مرور سه دههٔ پژوهش با ۱۲۶ مطالعه، خاموش‌کردن خود بیشتر در محیط‌های نابرابر و آسیب‌زننده و در رابطه‌های پرتعارض و نامتقارن دیده می‌شود، و به‌عنوان حلقهٔ واسط میان شرایط اجتماعی و افسردگی عمل می‌کند.",
       "Across 126 studies, self-silencing is most likely in inequitable, hurtful relationships and links social conditions to depression.", [s_jack26], ['contested']),
     P("یک نکتهٔ مهم برای خوانندهٔ فارسی‌زبان: این پیوند ممکن است وابسته به فرهنگ باشد. در نمونه‌ای ترک، خاموش‌کردن خود و «مراقبت به‌قیمت فداکاری» با رضایت رابطه و افسردگی بی‌ارتباط بود. در فرهنگ‌هایی که خودِ مستقل را کمتر برجسته می‌کنند، معنای همین رفتار فرق می‌کند.",
       "The link may be culture-bound: in a Turkish sample self-silencing was unrelated to satisfaction and depression.", [s_kurtis], ['contested']),
    ],
    links=[L('psy:assertiveness', 'contrasts', "جایگزینش", "The alternative"),
           L('psy:victim-toll', 'part-of', "بخشی از اثر بلندمدت", "Part of the long-term toll")],
    people=[p_jack],
    status='reviewed')

add('assertiveness',
    title=t("ابراز وجود: گفتن بدون کوچک‌کردن", "Assertiveness", "Assertiviteit"),
    summary=t("میان خاموش ماندن و پرخاش، راه سومی هست: گفتن خواسته به‌روشنی، با احترام، و با باز گذاشتن جای «نه». مهارت است و آموختنی.",
              "Between silence and aggression: saying what you want clearly, with respect, leaving room for no."),
    points=[
     P("ساختار عملی‌اش در رفتاردرمانی دیالکتیکی با نام DEAR MAN آموزش داده می‌شود: توصیف موقعیت بدون صفت، گفتن احساس، بیان صریح خواسته، گفتن فایده‌اش برای طرف مقابل، ماندن روی موضوع، ظاهر آرام، و آمادگی برای مذاکره.",
       "DBT teaches the DEAR MAN structure for making a request or saying no.", [s_store]),
     P("صادقانه دربارهٔ شواهد: این مهارت هیچ‌وقت جداگانه آزموده نشده و اعتبارش را از بستهٔ کامل درمان وام می‌گیرد؛ و مرور کاکرین همان بسته را هم با کیفیت شواهد «پایین» درجه‌بندی می‌کند.",
       "DEAR MAN has never been tested in isolation; the package evidence is rated low quality.", [s_store], ['editor-note']),
     P("آموزش ابراز وجود در فراتحلیلی برای اضطراب اجتماعی اثر بزرگی نشان داد، اما فقط شش کارآزمایی داشت و ناهمگونی بسیار بالا بود؛ پیگیری بلندمدت هم تقریباً وجود نداشت.",
       "A meta-analysis of assertiveness training for social anxiety found a large effect from only six trials with very high heterogeneity.", [s_lev], ['unreplicated']),
     P("«ارتباط بدون خشونت» هم پرکاربرد است و هم کم‌پشتوانه: در مرور دامنه‌ای، فقط هفت پژوهش با مجموعاً ۱۸۵ شرکت‌کننده و تنها دو مطالعهٔ تجربی پیدا شد.",
       "Nonviolent Communication rests on seven studies with 185 participants in total.", [s_adri], ['contested']),
    ],
    links=[L('psy:self-silencing', 'contrasts', "آنچه جایش می‌نشیند", "What it replaces"),
           L('psy:gottman-horsemen', 'see-also', "چهار سوار و پادزهرها", "The horsemen and antidotes"),
           L('psy:boundaries', 'part-of', "مرزها", "Boundaries")],
    try_={'text': t("پنجاه‌وچند جملهٔ آماده: به‌جای این، آن.", "Over fifty ready sentences."), 'tool': 'tools/sentences.html'},
    status='reviewed')

add('recovery',
    title=t("بهبود: چه چیزی واقعاً کمک می‌کند", "Recovery: what actually helps", "Herstel"),
    summary=t("خبر صادقانه این است: بهبود واقعی است اما کند و ناکامل؛ در سال‌ها اندازه گرفته می‌شود نه در ماه‌ها. و بعضی از چیزهایی که به آدم وعده می‌دهند، در آزمون دقیق دوام نمی‌آورند.",
              "Recovery is real but slow and partial, measured in years — and some of what is promised does not survive careful testing."),
    points=[
     P("در پژوهشی طولی روی ۳۰۹ زن کانادایی در پنج موج طی چهار سال پس از جدایی، افسردگی، علائم استرس پس از سانحه و درد مزمن ناتوان‌کننده همه به‌طور معنادار بهتر شدند — ولی در موج پنجم هنوز در سطح قابل‌توجهی بودند. هرچه خشونت شدیدتر بوده، اثرش در طول زمان بیشتر انباشته شده است.",
       "Across four years post-separation, depression, PTSD and chronic pain improved significantly but remained substantial.", [s_fordg]),
     P("درمان‌هایی که شواهد دارند: در شبکهٔ فراتحلیلی روی ۹۴ کارآزمایی، مداخله‌های روان‌شناختی در برابر گروه کنترل اثر بزرگی بر علائم استرس پس از سانحه داشتند، و بهترین نتیجه از ترکیب بازسازی شناختی با مواجههٔ تصویری آمد.",
       "In a component network meta-analysis of 94 RCTs, multicomponent cognitive restructuring plus imaginal exposure worked best.", [s_coven]),
     P("و یک باور رایج که شواهد تأییدش نمی‌کنند: اینکه «اول باید تثبیت شوی، بعد به سراغ خاطره بروی». در کارآزمایی روی ۱۴۹ بزرگسال با آسیب کودکی، افزودن مرحلهٔ مهارت‌آموزی پیش از مواجهه، نتیجهٔ بهتری نداد؛ هر سه شیوه بهبود بزرگ ساختند.",
       "The belief that stabilisation must precede trauma processing was not supported in a 149-person trial.", [s_oprel], ['contested']),
     P("«رشد پس از آسیب» را با احتیاط بخوانید. در پژوهشی که رشد را پیش و پس از حادثه سنجید، نمره‌های خودگزارشیِ رشد با تغییر واقعی رابطه‌ای نداشتند؛ و رشد <b>ادراک‌شده</b> با پریشانی بیشتر همراه بود. فراتحلیل بزرگ‌تر هم نشان داد در بیشتر پژوهش‌های دارای گروه کنترل، گروه حادثه‌دیده با گروه کنترل تفاوت معناداری نداشت.",
       "Self-reported post-traumatic growth was unrelated to actual change and perceived growth tracked more distress.", [s_fraz, s_mang], ['contested']),
     P("چیزی که در همان فراتحلیل واقعاً دیده شد: بهبود آینده‌نگر در عزت‌نفس، روابط مثبت و حس تسلط. پس رشد، اگر هست، از جنس «توانستن» است، نه از جنس «معنای تازه».",
       "What did show up prospectively: self-esteem, positive relationships and mastery.", [s_mang]),
     P("آیا بدن هم خوب می‌شود؟ پژوهشی که این را مستقیم در بازماندگان خشونت اندازه گرفته باشد پیدا نشد. نزدیک‌ترین نمونه، پژوهش شش‌ساله روی مراقبان بیماران بود که نشان داد افزایش نشانگر التهابی حتی سال‌ها پس از پایان مراقبت ادامه داشت. پس «بدن فراموش می‌کند» فعلاً یک امید است، نه یک یافته.",
       "No study has measured physiological recovery after reaching safety; the nearest analogue suggests markers do not simply normalise.", [s_kiec], ['editor-note']),
    ],
    links=[L('psy:victim-toll', 'part-of', "آنچه باید ترمیم شود", "What needs repair"),
           L('psy:cptsd', 'see-also', "وقتی تشخیص در کار است", "When there is a diagnosis"),
           L('psy:agency', 'explains', "موتور بهبود", "The engine of recovery")],
    confusions=[
     t("«هنوز حالم بد است» یعنی بهبود شکست خورده؟ نه. داده‌ها می‌گویند بهتر شدن و هم‌زمان هنوز رنج داشتن، حالت معمول چهار سال پس از جدایی است.",
       "Still suffering does not mean recovery failed; partial improvement is the normal picture."),
    ],
    status='reviewed')

add('change-possible',
    title=t("آیا خودشیفتگی عوض می‌شود؟", "Can narcissism change?", "Kan narcisme veranderen?"),
    summary=t("پاسخ کوتاه: صفت کمی، آری؛ الگوی عمیق، کند و با کمک حرفه‌ای؛ و هیچ‌کدام بدون خواستِ خود فرد. و پژوهش در این زمینه به‌طرز ناراحت‌کننده‌ای کم است.",
              "The short answer: the trait somewhat, the deep pattern slowly and with help — and never without the person wanting it."),
    points=[
     P("هیچ کارآزمایی تصادفی‌شده‌ای که درمانی را مخصوص اختلال شخصیت خودشیفته بیازماید وجود ندارد. نزدیک‌ترین کار، کارآزمایی چندمرکزی طرح‌واره‌درمانی روی اختلالات شخصیت بود که خودشیفته را هم در بر می‌گرفت و نتیجهٔ بهتری از درمان معمول داد — ولی این گروه جداگانه و با توان آماری کافی تحلیل نشد.",
       "There is no RCT of a treatment designed specifically for NPD; the closest is a schema-therapy trial that included it as a subgroup.", [s_bame], ['unreplicated']),
     P("مرور دامنه‌ای ۲۰۲۵ در پنج پایگاه داده تنها دوازده پژوهش پیدا کرد. جمع‌بندی مرورهای تخصصی: بیماران می‌توانند بهتر شوند، اما تغییر «تدریجی و کند» است.",
       "A 2025 scoping review found only twelve studies; change is described as gradual and slow.", [s_fayaz, s_wein]),
     P("یک یافتهٔ امیدبخش دربارهٔ سازوکار: در سه مطالعه، وقتی از افراد با خودشیفتگی بالا خواسته شد صریحاً خود را جای دیگری بگذارند، هم همدلی خودگزارشی و هم پاسخ ضربان قلبشان به رنج دیگری تغییر کرد. یعنی همدلی «خاموش» است، نه غایب.",
       "A perspective-taking instruction raised both self-reported empathy and heart-rate response — empathy is unactivated, not absent.", [s_hepp]),
     P("اما همان‌جا باید صادق بود: این‌ها القاهای کوتاه آزمایشگاهی روی دانشجویان‌اند، بدون هیچ شاهدی بر ماندگاری یا تغییر رفتار در زندگی واقعی.",
       "These were brief lab inductions with no evidence of durability.", [s_hepp], ['editor-note']),
     P("و دربارهٔ تغییر ارادی صفت‌ها به‌طور کلی: شدنی است ولی اندازه‌اش کوچک است. در فراتحلیل دوازده مطالعه، هدف‌گذاری برای تغییر، حدود ۰٫۰۵ تا ۰٫۱۶ انحراف معیار رشد بیشتر در چهار ماه آورد — واقعی، ولی نه معجزه.",
       "Volitional trait change is real but small: 0.05–0.16 SD more growth over sixteen weeks.", [s_huds]),
    ],
    links=[L('psy:npd', 'see-also', "تشخیص", "The diagnosis"),
           L('psy:healthy-narcissism', 'see-also', "جهت تغییر", "The direction of change"),
           L('psy:breaking-cycle', 'applies-to', "اگر خودتان نگرانید", "If you are the one worried")],
    people=[p_hepp],
    confusions=[
     t("«او هیچ‌وقت عوض نمی‌شود» و «اگر دوستم داشته باشد عوض می‌شود» هر دو نادرست‌اند. درست‌تر این است: تغییر ممکن ولی کند است، به خواست خودِ فرد و معمولاً به کمک حرفه‌ای نیاز دارد، و هیچ‌کس وظیفه ندارد منتظر بماند.",
       "Change is possible but slow, requires the person's own will, and nobody is obliged to wait."),
    ],
    status='reviewed')

add('collective-narcissism',
    title=t("خودشیفتگی جمعی", "Collective narcissism", "Collectief narcisme"),
    summary=t("همان ساختار، این بار دربارهٔ «ما»: باور به عظمت بی‌مانند گروه خودی که قدرش دانسته نمی‌شود. با پرخاشگری بین‌گروهی رابطه دارد و با عزت‌نفس شخصی رابطه‌ای ندارد.",
              "The same structure applied to 'us': belief in the unparalleled greatness of an in-group that goes unrecognised."),
    points=[
     P("گولچ د زاوالا و همکاران آن را به‌عنوان «سرمایه‌گذاری عاطفی روی باوری غیرواقع‌بینانه دربارهٔ عظمت بی‌مانند گروه خودی» تعریف کردند و سنجهٔ نه‌ماده‌ای ساختند.",
       "Defined as emotional investment in an unrealistic belief about the in-group's unparalleled greatness.", [s_golec]),
     P("در پنج مطالعه، خودشیفتگی جمعی احساس تهدید از گروه بیرونی، ناتوانی در بخشیدن، و ترجیح پرخاش را پیش‌بینی کرد — فراتر از جهت‌گیری سلطه‌جویی اجتماعی و اقتدارگرایی.",
       "It predicted perceived outgroup threat, unforgiveness and preference for aggression beyond SDO and authoritarianism.", [s_golec]),
     P("نکتهٔ مهم: با عزت‌نفس شخصی رابطه‌ای نداشت. یعنی غرور ملی سالم و خودشیفتگی جمعی دو چیزند، همان‌طور که عزت‌نفس و خودشیفتگی فردی دو چیزند.",
       "It was unrelated to personal self-esteem: healthy pride and collective narcissism are distinct.", [s_golec, s_brum2]),
    ],
    links=[L('psy:narcissism', 'see-also', "نسخهٔ فردی", "The individual version"),
           L('psy:ideological-brain', 'see-also', "ایدئولوژی و گروه", "Ideology and group"),
           L('psy:conspiracy', 'see-also', "باور توطئه", "Conspiracy belief")],
    people=[p_golec],
    status='reviewed')

# ---------------- نوشتن ----------------
import glob
os.makedirs(f'{R}/data/psy/concepts', exist_ok=True)
for c in C:
    json.dump(c, open(f"{R}/data/psy/concepts/{c['id'].split(':')[1]}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S.people, open(f'{R}/core/people.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S.sources, open(f'{R}/core/sources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('narcissism section:', len(C), 'concepts;', 'people', len(S.people), 'sources', len(S.sources))

# ---------------- مرزها (افزوده) ----------------
C2 = []
_add_orig = add
C.clear()
add('boundaries',
    title=t("مرزها: حد من کجاست", "Boundaries", "Grenzen"),
    summary=t("مرز، دیوار نیست و تنبیه هم نیست. جمله‌ای است دربارهٔ کاری که خودم می‌کنم، نه دستوری دربارهٔ کاری که دیگری باید بکند. همین تفاوت، مرز را از تهدید جدا می‌کند.",
              "A boundary is a statement about what I will do, not an order about what you must do."),
    points=[
     P("فرق مرز و تهدید در فاعل جمله است: «اگر دوباره سر من داد بزنی، گفت‌وگو را تمام می‌کنم و فردا برمی‌گردم» مرز است؛ «اگر دوباره داد بزنی می‌روم و برنمی‌گردم» معمولاً تهدید است. اولی را می‌شود اجرا کرد، دومی را معمولاً نه.",
       "A boundary names my own action; a threat names the other's punishment.", [s_karp, s_ted]),
     P("مرز بدون اجرا، مرز نیست. در ادبیات تغییر رفتار، آنچه یادگیری می‌سازد پیامد ثابت و قابل‌پیش‌بینی است، نه شدت پیامد.",
       "Consistency, not severity, is what makes a limit work.", [s_huds19]),
     P("در رابطه‌های امن، گفتن مرز رابطه را محکم‌تر می‌کند. در رابطه‌های کنترل‌گرانه، گفتن مرز ممکن است واکنش تندتری بیاورد؛ برای همین در این موقعیت‌ها برنامهٔ ایمنی باید پیش از مرزگذاری آماده باشد، نه بعد از آن.",
       "In safe relationships stating limits strengthens them; under coercive control it can escalate, so safety planning comes first.", [s_spear, s_stark]),
     P("مرز بین شما و خانواده هم بر هم زدن رابطه نیست: داده‌های طولی نشان می‌دهد بیشتر دوره‌های قطع رابطه با والدین بعداً پایان می‌یابند.",
       "Most periods of estrangement from parents later end.", [s_recz]),
    ],
    links=[L('psy:assertiveness', 'part-of', "مهارت گفتنش", "The skill of stating it"),
           L('psy:control-behaviors', 'contrasts', "مرز در برابر کنترل", "Boundary versus control"),
           L('psy:agency', 'see-also', "از همین‌جا شروع می‌شود", "Where it starts")],
    explain=t("چهار جملهٔ مرزی که تقریباً همیشه کار می‌کند:\n\n«وقتی صدا بالا می‌رود، من گفت‌وگو را نگه می‌دارم و یک ساعت بعد برمی‌گردم.»\n\n«دربارهٔ این موضوع با تو حرف نمی‌زنم. دربارهٔ بقیهٔ چیزها بله.»\n\n«تصمیمم همین است. لازم نیست موافق باشی.»\n\n«تا این‌جا می‌توانم کمک کنم؛ از این‌جا به بعد با خودت است.»\n\nهر چهارتا یک ویژگی مشترک دارند: فاعلشان «من» است و هیچ‌کدام از طرف مقابل نمی‌خواهد چیزی را ثابت کند.",
              "Four boundary sentences that usually work, all with 'I' as subject."),
    try_={'text': t("جملهٔ مرزی خودتان را بسازید و ببینید کدام الگو در آن هست.", "Build your own boundary sentence."), 'tool': 'tools/sentences.html'},
    status='reviewed')
for c in C:
    json.dump(c, open(f"{R}/data/psy/concepts/{c['id'].split(':')[1]}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S.sources, open(f'{R}/core/sources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('+ boundaries')
