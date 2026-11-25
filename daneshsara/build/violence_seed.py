# -*- coding: utf-8 -*-
"""بخش «خشونت» ویکی روان: مدخل‌ها، منابع و چهره‌ها.
python3 build/violence_seed.py     (افزایشی؛ فقط فایل‌های همین بخش را می‌نویسد)
برنامه و بازبینی‌های مرحله‌به‌مرحله: data/psy/dossiers/violence.plan.md"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from seedlib import Seed, R

S = Seed('psy')
t = S.t
def src(c, tier=2, url=None): return S.src(c, tier, url)
def who(latin, fa, years='', note=''): return S.person(latin, fa, years, note)

C = []
def add(id, title, summary, field='violence', kind='concept', points=(), links=(), people=(),
        explain=None, why=None, examples=(), confusions=(), aliases=(), parent=None, status='reviewed'):
    srcs = sorted({s for p in points for s in p.get('sources', [])})
    c = {'id': 'psy:' + id, 'kind': kind, 'title': title, 'aliases': list(aliases),
         'parent': 'psy:' + (parent or field) if (parent or field) else None,
         'field': 'psy:' + field if field else None,
         'summary': summary, 'points': list(points), 'links': list(links), 'people': list(people),
         'sources': srcs, 'booklets': [], 'origin': 'violence', 'iran': None, 'wikidata': None,
         'status': status}
    if explain: c['explain'] = explain
    if why: c['why'] = why
    if examples: c['examples'] = list(examples)
    if confusions: c['confusions'] = list(confusions)
    C.append(c)
def P(fa, en, srcs=(), flags=()): return {'text': t(fa, en), 'sources': list(srcs), 'flags': list(flags)}
def L(to, rel, fa): return {'to': to, 'rel': rel, 'note': t(fa, fa)}
def EX(fa, kind='everyday', label='illustration', source=None):
    e = {'kind': kind, 'label': label, 'text': t(fa, fa)}
    if source: e['source'] = source
    return e

# ---------------- منابع ----------------
s_who02 = src("Krug, E. G., Dahlberg, L. L., Mercy, J. A., Zwi, A. B., & Lozano, R. (Eds.) (2002). World Report on Violence and Health. World Health Organization.", 2, "https://www.who.int/publications/i/item/9241545615")
s_galt69 = src("Galtung, J. (1969). Violence, Peace, and Peace Research. Journal of Peace Research, 6(3), 167–191.", 2)
s_galt90 = src("Galtung, J. (1990). Cultural Violence. Journal of Peace Research, 27(3), 291–305.", 2)
s_bourd = src("Bourdieu, P. (2001). Masculine Domination (R. Nice, Trans.). Stanford University Press. (Original work published 1998)", 3)
s_and02 = src("Anderson, C. A., & Bushman, B. J. (2002). Human Aggression. Annual Review of Psychology, 53, 27–51.", 2)
s_coady = src("Coady, C. A. J. (1986). The Idea of Violence. Journal of Applied Philosophy, 3(1), 3–19.", 3)
s_hobbes = src("Hobbes, T. (1651). Leviathan.", 3)
s_weber = src("Weber, M. (1919). Politik als Beruf [Politics as a Vocation].", 3)
s_elias = src("Elias, N. (1939/2000). The Civilizing Process: Sociogenetic and Psychogenetic Investigations (rev. ed.). Blackwell.", 3)
s_udhr = src("United Nations General Assembly (1948). Universal Declaration of Human Rights, Articles 3 and 5.", 2, "https://www.un.org/en/about-us/universal-declaration-of-human-rights")
s_mill = src("Mill, J. S. (1859). On Liberty.", 3)
s_gomez = src("Gómez, J. M., Verdú, M., González-Megías, A., & Méndez, M. (2016). The phylogenetic roots of human lethal violence. Nature, 538, 233–237.", 2, "https://doi.org/10.1038/nature19758")
s_wilson14 = src("Wilson, M. L., Boesch, C., Fruth, B., et al. (2014). Lethal aggression in Pan is better explained by adaptive strategies than human impacts. Nature, 513, 414–417.", 2, "https://doi.org/10.1038/nature13727")
s_wrang18 = src("Wrangham, R. W. (2018). Two types of aggression in human evolution. PNAS, 115(2), 245–253.", 2, "https://doi.org/10.1073/pnas.1713611115")
s_fry = src("Fry, D. P. (Ed.) (2013). War, Peace, and Human Nature: The Convergence of Evolutionary and Cultural Views. Oxford University Press.", 3)
s_eisner = src("Eisner, M. (2003). Long-Term Historical Trends in Violent Crime. Crime and Justice, 30, 83–142.", 2, "https://www.vrc.crim.cam.ac.uk/system/files/documents/manuel-eisner-historical-trends-in-violence.pdf")
s_pinker = src("Pinker, S. (2011). The Better Angels of Our Nature: Why Violence Has Declined. Viking.", 3)
s_schwer = src("Schwerhoff, G., Seebröker, B., Kästner, A., & Voigt, W. (2021). Hard numbers? The long-term decline in violence reassessed. Continuity and Change, 36(1), 1–32.", 2, "https://doi.org/10.1017/S0268416021000096")
s_nietz = src("Nietzsche, F. (1887). Zur Genealogie der Moral [On the Genealogy of Morality], Second Essay.", 3)
s_fouc = src("Foucault, M. (1975/1977). Discipline and Punish: The Birth of the Prison (A. Sheridan, Trans.). Pantheon.", 3)
s_tilly = src("Tilly, C. (1985). War Making and State Making as Organized Crime. In P. Evans, D. Rueschemeyer & T. Skocpol (Eds.), Bringing the State Back In (pp. 169–191). Cambridge University Press.", 3)
s_benj = src("Benjamin, W. (1921). Zur Kritik der Gewalt [Critique of Violence].", 3)
s_felitti = src("Felitti, V. J., Anda, R. F., Nordenberg, D., et al. (1998). Relationship of childhood abuse and household dysfunction to many of the leading causes of death in adults: The Adverse Childhood Experiences (ACE) Study. American Journal of Preventive Medicine, 14(4), 245–258.", 2)
s_kitz = src("Kitzmann, K. M., Gaylord, N. K., Holt, A. R., & Kenny, E. D. (2003). Child witnesses to domestic violence: A meta-analytic review. Journal of Consulting and Clinical Psychology, 71(2), 339–352.", 1)
s_litz = src("Litz, B. T., Stein, N., Delaney, E., et al. (2009). Moral injury and moral repair in war veterans: A preliminary model and intervention strategy. Clinical Psychology Review, 29(8), 695–706.", 2)
s_macn = src("MacNair, R. M. (2002). Perpetration-Induced Traumatic Stress: The Psychological Consequences of Killing. Praeger.", 3)
s_widom = src("Widom, C. S., & Maxfield, M. G. (2001). An Update on the \"Cycle of Violence\". National Institute of Justice, Research in Brief (NCJ 184894).", 2, "https://www.ojp.gov/pdffiles1/nij/184894.pdf")
s_lifton = src("Lifton, R. J. (1986). The Nazi Doctors: Medical Killing and the Psychology of Genocide. Basic Books.", 3)
s_milg = src("Milgram, S. (1963). Behavioral Study of Obedience. Journal of Abnormal and Social Psychology, 67(4), 371–378.", 2)
s_reich = src("Reicher, S. D., Haslam, S. A., & Smith, J. R. (2012). Working Toward the Experimenter: Reconceptualizing Obedience Within the Milgram Paradigm as Identification-Based Followership. Perspectives on Psychological Science, 7(4), 315–324.", 2, "https://www.psychologicalscience.org/publications/observer/obsonline/not-obedience-but-followership.html")
s_letex = src("Le Texier, T. (2019). Debunking the Stanford Prison Experiment. American Psychologist, 74(7), 823–839.", 2)
s_brown = src("Browning, C. R. (1992). Ordinary Men: Reserve Police Battalion 101 and the Final Solution in Poland. HarperCollins.", 3, "https://www.facinghistory.org/resource-library/reserve-police-battalion-101")
s_coll = src("Collins, R. (2008). Violence: A Micro-sociological Theory. Princeton University Press.", 3)
s_band = src("Bandura, A. (1999). Moral Disengagement in the Perpetration of Inhumanities. Personality and Social Psychology Review, 3(3), 193–209.", 2)
s_fiske = src("Fiske, A. P., & Rai, T. S. (2014). Virtuous Violence: Hurting and Killing to Create, Sustain, End, and Honor Social Relationships. Cambridge University Press.", 3)
s_baum97 = src("Baumeister, R. F. (1997). Evil: Inside Human Violence and Cruelty. W. H. Freeman.", 3)
s_baum90 = src("Baumeister, R. F., Stillwell, A., & Wotman, S. R. (1990). Victim and perpetrator accounts of interpersonal conflict: Autobiographical narratives about anger. Journal of Personality and Social Psychology, 59(5), 994–1005.", 2)
s_chen = src("Stephan, M. J., & Chenoweth, E. (2008). Why Civil Resistance Works: The Strategic Logic of Nonviolent Conflict. International Security, 33(1), 7–44.", 2, "https://www.belfercenter.org/sites/default/files/legacy/files/IS3301_pp007-044_Stephan_Chenoweth.pdf")
s_chen20 = src("Chenoweth, E. (2020). The Future of Nonviolent Resistance. Journal of Democracy, 31(3), 69–84.", 2)
s_marsh = src("Marshall, S. L. A. (1947). Men Against Fire: The Problem of Battle Command. William Morrow.", 4)
s_spill = src("Spiller, R. J. (1988). S.L.A. Marshall and the Ratio of Fire. The RUSI Journal, 133(4), 63–71.", 2)
s_blair = src("Blair, R. J. R. (1995). A cognitive developmental approach to morality: Investigating the psychopath. Cognition, 57(1), 1–29.", 2)
s_orobio = src("Orobio de Castro, B., Veerman, J. W., Koops, W., Bosch, J. D., & Monshouwer, H. J. (2002). Hostile attribution of intent and aggressive behavior: A meta-analysis. Child Development, 73(3), 916–934.", 1)
s_undp = src("United Nations Development Programme (2023). 2023 Gender Social Norms Index (GSNI): Breaking down gender biases.", 2, "https://hdr.undp.org/content/2023-gender-social-norms-index-gsni")
s_lil = src("Lilienfeld, S. O. (2017). Microaggressions: Strong Claims, Inadequate Evidence. Perspectives on Psychological Science, 12(1), 138–169.", 2)
s_wm = src("Wilson, L. C., & Miller, K. E. (2016). Meta-Analysis of the Prevalence of Unacknowledged Rape. Trauma, Violence, & Abuse, 17(2), 149–159.", 1, "https://doi.org/10.1177/1524838015576391")
s_who25 = src("World Health Organization (2025). Violence against women prevalence estimates, 2023: global, regional and national prevalence estimates for intimate partner violence against women and non-partner sexual violence against women.", 2, "https://www.who.int/publications/i/item/9789240116962")
s_fem25 = src("UNODC & UN Women (2025). Femicides in 2024: Global Estimates of Intimate Partner/Family Member Femicides. United Nations.", 2, "https://www.unwomen.org/en/digital-library/publications/2025/11/femicides-in-2024-global-estimates-of-intimate-partner-family-member-femicides")
s_gsh = src("UNODC (2023). Global Study on Homicide 2023. United Nations.", 2, "https://www.unodc.org/unodc/en/data-and-analysis/global-study-on-homicide.html")
s_fgm = src("UNICEF (2024). Female Genital Mutilation: A Global Concern. 2024 Update.", 2, "https://data.unicef.org/resources/female-genital-mutilation-a-global-concern/")
s_sen = src("Sen, A. (1990). More Than 100 Million Women Are Missing. The New York Review of Books, 37(20).", 3)
s_levack = src("Levack, B. P. (2016). The Witch-Hunt in Early Modern Europe (4th ed.). Routledge.", 3)
s_whovaw = src("World Health Organization (2026). Violence against women: fact sheet.", 2, "https://www.who.int/news-room/fact-sheets/detail/violence-against-women")
s_green = src("Green, B., Horel, T., & Papachristos, A. V. (2017). Modeling Contagion Through Social Networks to Explain and Predict Gunshot Violence in Chicago, 2006 to 2014. JAMA Internal Medicine, 177(3), 326–333.", 2, "https://isps.yale.edu/research/publications/isps17-02")
s_slut = src("Slutkin, G. (2013). Violence Is a Contagious Disease. In Contagion of Violence: Workshop Summary (pp. 94–111). National Academies Press.", 3)
s_nisb = src("Nisbett, R. E., & Cohen, D. (1996). Culture of Honor: The Psychology of Violence in the South. Westview Press.", 3)
s_vru = src("Scottish Government / Civil Service (2018). Tackling knife crime in Scotland: 10 years on.", 3, "https://civilservice.blog.gov.uk/2018/05/24/tackling-knife-crime-in-scotland-10-years-on/")
s_card = src("Florence, C., Shepherd, J., Brennan, I., & Simon, T. (2011). Effectiveness of anonymised information sharing and use in health service, police, and local government partnership for preventing violence related injury: experimental study and time series analysis. BMJ, 342, d3313.", 2, "https://pmc.ncbi.nlm.nih.gov/articles/PMC3116927")
s_rome = src("Rome Statute of the International Criminal Court (1998), Article 7(1)(j) and 7(2)(h): the crime of apartheid.", 2, "https://www.icc-cpi.int/sites/default/files/RS-Eng.pdf")
s_apconv = src("United Nations General Assembly (1973). International Convention on the Suppression and Punishment of the Crime of Apartheid.", 2)
s_staub = src("Staub, E. (1989). The Roots of Evil: The Origins of Genocide and Other Group Violence. Cambridge University Press.", 3)
s_stanton = src("Stanton, G. H. (2016). The Ten Stages of Genocide. Genocide Watch. (First presented as eight stages, 1996)", 4, "https://www.genocidewatch.com/tenstages")
s_sharp = src("Sharpeville massacre, 21 March 1960. South African History Online; Encyclopaedia Britannica.", 3, "https://www.britannica.com/event/Sharpeville-massacre")
s_hrw26 = src("Human Rights Watch (2026, August 6). One Step Closer to Recognizing Gender Apartheid as an International Crime.", 3, "https://www.hrw.org/news/2026/08/06/one-step-closer-to-recognizing-gender-apartheid-as-an-international-crime")
s_hasl = src("Haslam, N. (2006). Dehumanization: An Integrative Review. Personality and Social Psychology Review, 10(3), 252–264.", 2)
s_john = src("Johnson, M. P. (2008). A Typology of Domestic Violence: Intimate Terrorism, Violent Resistance, and Situational Couple Violence. Northeastern University Press.", 3)

# ---------------- چهره‌ها ----------------
p_galt = who("Johan Galtung", "یوهان گالتونگ", "۱۹۳۰–۲۰۲۴", "جامعه‌شناس نروژی و از بنیان‌گذاران پژوهش صلح؛ «خشونت ساختاری» و «خشونت فرهنگی».")
p_band = who("Albert Bandura", "آلبرت بندورا", "۱۹۲۵–۲۰۲۱", "روان‌شناس؛ یادگیری اجتماعی و «خاموش‌کردن اخلاق».")
p_wrang = who("Richard Wrangham", "ریچارد رنگام", "۱۹۴۸–", "نخستی‌شناس؛ دو گونهٔ پرخاشگری و فرضیهٔ خوداهلی‌سازی انسان.")
p_elias = who("Norbert Elias", "نوربرت الیاس", "۱۸۹۷–۱۹۹۰", "جامعه‌شناس؛ «فرایند متمدن‌شدن».")
p_fiske = who("Alan Fiske", "الن فیسک", "", "انسان‌شناس؛ نظریهٔ مدل‌های رابطه و «خشونت فضیلت‌مندانه».")
p_coll = who("Randall Collins", "رندال کالینز", "۱۹۴۱–", "جامعه‌شناس؛ نظریهٔ خُرد جامعه‌شناختی خشونت.")
p_widom = who("Cathy Spatz Widom", "کتی اسپاتز ویدوم", "", "روان‌شناس؛ پیگیری چنددهه‌ای کودکان آزاردیده و «چرخهٔ خشونت».")
p_slut = who("Gary Slutkin", "گری اسلاتکین", "", "همه‌گیرشناس؛ نگاه به خشونت مثل بیماری واگیر.")
p_staub = who("Ervin Staub", "اروین استاب", "۱۹۳۸–", "روان‌شناس؛ «پیوستار ویرانگری» در خشونت گروهی.")
p_brown = who("Christopher Browning", "کریستوفر براونینگ", "۱۹۴۴–", "تاریخ‌نگار؛ «آدم‌های معمولی».")
p_lifton = who("Robert Jay Lifton", "رابرت جی لیفتون", "۱۹۲۶–۲۰۲۵", "روان‌پزشک؛ پژوهش دربارهٔ پزشکان نازی و «دوپاره‌شدن».")
p_eisner = who("Manuel Eisner", "مانوئل آیزنر", "", "جرم‌شناس؛ روند بلندمدت قتل در اروپا.")
p_baum = who("Roy Baumeister", "روی بامایستر", "۱۹۵۳–", "روان‌شناس اجتماعی؛ «افسانهٔ شرّ ناب» و «شکاف بزرگی».")

# ================= مدخل‌ها =================
add('violence', kind='subfield', field=None, parent='psychology',
    title=t("خشونت", "Violence", "Geweld"),
    summary=t("مجموعه‌ای از مدخل‌ها دربارهٔ خشونت: چه چیزی خشونت است، از کجا آمده، با آدم‌ها و اطرافیانشان چه می‌کند، چرا یک آدم در یک نقش خشن است و در نقش دیگر نه، چه نسبتی با اخلاق دارد، چطور میان جنسیت‌ها پخش شده، چرا همه‌گیر می‌شود و چطور به آپارتاید می‌رسد.",
              "Entries on violence: what counts, where it comes from, what it does, roles, morality, gender, contagion and apartheid."),
    status='draft')

add('violence-what-counts',
    title=t("چه چیزی را خشونت حساب می‌کنیم؟", "What counts as violence?"),
    aliases=["تعریف خشونت", "خشونت ساختاری", "خشونت نمادین", "خشونت فرهنگی"],
    summary=t("تعریف خشونت یک چیز نیست؛ یک طیف است. در سر باریکش فقط زور بدنیِ عمدی است. در سر پهنش هر ساختار و باوری است که آدم‌ها را از آنچه می‌توانستند باشند پایین‌تر نگه می‌دارد. اینکه کجا خط بکشیم، خودش یک تصمیم است و پیامد دارد.",
              "Definitions of violence form a spectrum from intentional physical force to any structure that keeps people below their potential."),
    points=[
     P("سازمان جهانی بهداشت (۲۰۰۲) خشونت را «به‌کاربردن عمدیِ زور بدنی یا قدرت، واقعی یا در حد تهدید» می‌داند، علیه خود، دیگری یا یک گروه، که به آسیب، مرگ، آسیب روانی، بدرشدی یا محرومیت می‌انجامد یا احتمالش زیاد است. سه دسته دارد: علیه خود، میان‌فردی، جمعی؛ و چهار جنس: بدنی، جنسی، روانی، و محروم‌کردن یا غفلت.",
       "WHO (2002): intentional use of physical force or power; self-directed, interpersonal, collective; physical, sexual, psychological, deprivation.", [s_who02]),
     P("در روان‌شناسی «پرخاشگری» هر رفتاری است که به قصد آسیب‌زدن به کسی انجام شود که نمی‌خواهد آسیب ببیند، و «خشونت» سر شدید همان طیف است که آسیب بدنی سنگین هدفش است. پس هر خشونتی پرخاشگری است ولی هر پرخاشگری‌ای خشونت نیست.",
       "In psychology aggression is behaviour intended to harm; violence is its extreme end.", [s_and02]),
     P("گالتونگ (۱۹۶۹) تعریف را بسیار پهن‌تر کرد: خشونت هر جا هست که آدم‌ها چنان زیر اثر باشند که آنچه از تن و ذهنشان برمی‌آید از آنچه می‌توانست برآید کمتر شود. در «خشونت ساختاری» فاعل مشخصی نیست؛ آسیب در خود ساختار است، مثل وقتی که درمان هست ولی به گروهی نمی‌رسد.",
       "Galtung (1969): violence is present when actual realizations fall below potential ones; structural violence has no identifiable actor.", [s_galt69]),
     P("او بعدها «خشونت فرهنگی» را هم افزود: هر بخش از فرهنگ (دین، ایدئولوژی، زبان، هنر، علم) که خشونت مستقیم یا ساختاری را درست یا دست‌کم بی‌اشکال جلوه دهد.",
       "Cultural violence: aspects of culture that legitimise direct or structural violence.", [s_galt90]),
     P("بوردیو «خشونت نمادین» را خشونتی نرم و نادیدنی می‌داند که با همراهی خودِ زیردست کار می‌کند، چون او دنیا را با همان دسته‌بندی‌هایی می‌بیند که سلطه ساخته است.",
       "Bourdieu: symbolic violence is gentle, invisible, exercised with the complicity of the dominated.", [s_bourd]),
     P("منتقدان می‌گویند اگر هر بی‌عدالتی را خشونت بنامیم، کلمه تیزی‌اش را از دست می‌دهد و فرق کتک‌زدن با نابرابری گم می‌شود. طرفداران تعریف پهن جواب می‌دهند که تعریف باریک، آسیب‌های بزرگ و بی‌فاعل را از دید می‌اندازد.",
       "Critics argue wide definitions blur moral distinctions; defenders say narrow ones hide large actor-less harms.", [s_coady, s_galt69], ['contested']),
    ],
    links=[L('psy:coercive-control', 'see-also', "خشونتی که با شمردن کتک دیده نمی‌شود"),
           L('psy:violence-unseen-by-victim', 'explains', "چرا تعریف تعیین می‌کند چه کسی خودش را قربانی بداند"),
           L('psy:violence-genealogy', 'see-also', "معنای این کلمه در طول تاریخ عوض شده است"),
           L('soc:inequality-health', 'bridges', "نمونه‌ای از آسیب ساختاری")],
    people=[p_galt],
    explain=t("یک آزمایش ذهنی کمک می‌کند. شش موقعیت را کنار هم بگذارید: سیلی‌زدن به بچه؛ تهدید به اخراج اگر کسی شکایت کند؛ قهر دوهفته‌ای برای تنبیه همسر؛ قانونی که به نیمی از مردم اجازهٔ کار نمی‌دهد؛ شوخی دائمی با لهجهٔ یک همکار؛ بیمارستانی که در محلهٔ فقیر ساخته نمی‌شود. با تعریف باریک فقط اولی خشونت است. با تعریف سازمان جهانی بهداشت اولی، دومی و سومی. با تعریف گالتونگ هر شش مورد.\n\nهیچ‌کدام از این تعریف‌ها «درست» به معنای علمی نیست؛ هرکدام برای کاری ساخته شده. تعریف باریک به کار قاضی می‌آید، تعریف میانی به کار پزشک و آمارگیر، تعریف پهن به کار کسی که می‌خواهد بفهمد چرا عمر یک گروه ده سال کوتاه‌تر است.",
              "Six situations sorted by three definitions show that each definition serves a different job."),
    confusions=[t("خشونت با خشم یکی نیست. خشم یک هیجان است و می‌تواند بی‌هیچ خشونتی بیاید و برود؛ و خشونت می‌تواند کاملاً خونسرد و بی‌خشم باشد.", "Violence is not anger."),
                t("خشونت با تعارض یکی نیست. تعارض یعنی دو خواستهٔ ناسازگار؛ خشونت یکی از راه‌های حل آن است و معمولاً بدترینش.", "Violence is not conflict.")])

add('violence-why-expect-none',
    title=t("چرا انتظار داریم آدم‌ها به هم خشونت نکنند؟", "Why do we expect non-violence?"),
    summary=t("این انتظار بدیهی نیست و همیشه هم نبوده است. چند ریشه دارد: قراردادی که در آن همه زور را زمین می‌گذارند تا امن باشند، دولتی که زور را انحصاری می‌کند، عادت‌های درونی‌شده، و این ایده که هر آدمی حقی بر تن و جان خودش دارد.",
              "The expectation rests on social contract, state monopoly of force, internalised restraint, and rights to bodily integrity."),
    points=[
     P("هابز (۱۶۵۱) گفت جایی که قدرت مشترکی نباشد که همه از آن حساب ببرند، هر کس از هر کس می‌ترسد و پیش‌دستی می‌کند. آدم‌ها زور خود را واگذار می‌کنند تا در امان باشند. پس انتظار بی‌خشونتی از یک معامله می‌آید: من نمی‌زنم چون تو هم نمی‌زنی و کسی هست که هر دو را بازخواست کند.",
       "Hobbes: without a common power, fear drives pre-emption; people trade force for safety.", [s_hobbes]),
     P("وبر (۱۹۱۹) دولت را جماعتی تعریف کرد که در یک سرزمین، انحصار به‌کاربردن «مشروع» زور بدنی را با موفقیت از آنِ خود کرده است. یعنی خشونت از میان نرفته؛ جمع شده و در یک جا گذاشته شده است.",
       "Weber: the state claims the monopoly of legitimate physical force.", [s_weber]),
     P("الیاس نشان داد در اروپا، هم‌زمان با شکل‌گرفتن دولت‌های مرکزی و درازشدن زنجیرهٔ وابستگی آدم‌ها به هم، خویشتن‌داری کم‌کم از یک اجبار بیرونی به یک عادت درونی تبدیل شد؛ تا جایی که دیدن خشونت برای بسیاری ناخوشایند شد.",
       "Elias: with state formation and interdependence, restraint moved from external constraint to habit.", [s_elias]),
     P("میل (۱۸۵۹) معیار را روشن کرد: تنها دلیلی که می‌شود با آن بر آدمی آزاد، برخلاف خواستش، زور به کار برد جلوگیری از آسیب به دیگران است. اعلامیهٔ جهانی حقوق بشر (۱۹۴۸) همین را حق کرد: حق زندگی، آزادی و امنیت، و اینکه هیچ‌کس نباید شکنجه شود.",
       "Mill's harm principle; UDHR articles 3 and 5.", [s_mill, s_udhr]),
     P("این انتظار در تاریخ بلند آدمی تازه است و هنوز همه‌جا و برای همه یکسان نیست: در بسیاری از جامعه‌ها زدن بچه، زن، برده یا زندانی تا همین اواخر حقِ کسی بود که می‌زد.",
       "The expectation is historically recent and uneven.", [s_elias, s_pinker], ['editor-note']),
    ],
    links=[L('phil:hobbes-three-causes-of-conflict-leviathan', 'bridges', "سه علت نزاع نزد هابز"),
           L('phil:kant-duty-ethics-universal-law', 'bridges', "آدم هدف است نه وسیله"),
           L('soc:consent-theory-of-power', 'bridges', "قدرتی که بر رضایت تکیه دارد"),
           L('psy:violence-history-decline', 'evidence-for', "آیا این انتظار نتیجه داده است؟"),
           L('psy:virtuous-violence', 'contrasts', "جاهایی که اخلاق خودش خشونت می‌خواهد")],
    people=[p_elias],
    explain=t("پرسش را می‌شود برعکس کرد: چرا آدم‌ها بیشتر وقت‌ها به هم خشونت نمی‌کنند؟ در یک قطار شلوغ صدها غریبه، خسته و فشرده، ساعت‌ها کنار هم می‌ایستند و هیچ اتفاقی نمی‌افتد. این آرامش طبیعی نیست؛ ساخته شده است، با قانون، با عادت، با اینکه به هم نیاز داریم. هر جا یکی از این پایه‌ها بشکند (دولت فروبپاشد، گروهی از دایرهٔ «آدم‌هایی که حق دارند» بیرون گذاشته شوند) انتظار هم می‌شکند.",
              "Reverse the question: why are people mostly non-violent? The calm of a crowded train is built, not natural."))

add('violence-origins',
    title=t("خشونت میان موجودات از کجا شروع شد؟", "Where did violence among living beings begin?"),
    aliases=["ریشهٔ تکاملی خشونت", "پرخاشگری واکنشی و حساب‌شده"],
    summary=t("کشتن هم‌گونه در پستانداران کم ولی پراکنده است و در شاخهٔ نخستی‌ها بیشتر. آدم دو چیز را با هم دارد که کمتر گونه‌ای دارد: پرخاشگری لحظه‌ایِ بسیار کم، و توان بالای خشونتِ برنامه‌ریزی‌شده و گروهی.",
              "Conspecific killing is rare in mammals, higher in primates; humans combine low reactive with high proactive aggression."),
    points=[
     P("گومز و همکاران (۲۰۱۶) بیش از چهار میلیون مرگ را در ۱٬۰۲۴ گونهٔ پستاندار بررسی کردند: به‌طور میانگین حدود ۰٫۳ درصد مرگ‌ها به دست هم‌گونه است، ولی برای نیای مشترک نخستی‌ها و برای آدم در آغاز، از روی جایش در درخت تبار، حدود ۲ درصد پیش‌بینی می‌شود. این عدد با یافته‌های باستان‌شناسی از گروه‌های پیش از تاریخ هم می‌خواند.",
       "Gómez et al. (2016): ~0.3% of mammal deaths from conspecifics; ~2% phylogenetically predicted for humans.", [s_gomez]),
     P("همان پژوهش نشان می‌دهد این سهم در تاریخ آدمی ثابت نمانده و با شکل سازمان سیاسی جامعه بالا و پایین رفته است. یعنی تبار یک نقطهٔ شروع می‌دهد، نه یک سرنوشت.",
       "The level has varied with socio-political organisation; phylogeny is a baseline, not a fate.", [s_gomez]),
     P("در پنج دهه مشاهدهٔ ۱۸ گروه شامپانزه و ۴ گروه بونوبو، ۱۵۲ کشتن در شامپانزه‌ها ثبت شد (۵۸ دیده‌شده، بقیه استنباط یا گمان) و یک مورد مشکوک در بونوبوها. ۹۲ درصد حمله‌کنندگان نر بودند. این الگو با دخالت آدم توضیح داده نمی‌شد.",
       "Wilson et al. (2014): 152 chimpanzee killings vs one suspected bonobo killing; 92% of attackers male.", [s_wilson14]),
     P("رنگام دو گونه پرخاشگری را جدا می‌کند که مدارهای عصبی جدا دارند: «واکنشی» (داغ، در جواب تهدید یا ناکامی) و «حساب‌شده» (سرد، برنامه‌ریزی‌شده، برای رسیدن به هدف). به گفتهٔ او آدم در اولی از شامپانزه بسیار آرام‌تر است و در دومی بسیار تواناتر.",
       "Wrangham: reactive vs proactive aggression; humans are low on the first and high on the second.", [s_wrang18]),
     P("گروهی از انسان‌شناسان این تصویر را زیادی جنگ‌محور می‌دانند: شواهد باستان‌شناختی جنگ سازمان‌یافته بیشتر پس از یکجانشینی دیده می‌شود، و همکاری و آشتی هم همان‌قدر در تبار ما ریشه دارد.",
       "Critics hold that organised war is archaeologically recent and that cooperation is equally ancestral.", [s_fry], ['contested']),
    ],
    links=[L('psy:self-domestication', 'explains', "چرا پرخاشگری لحظه‌ای در آدم کم شد"),
           L('tabar:origins-of-war-chagha-sofla', 'bridges', "نخستین نشانه‌های جنگ در باستان‌شناسی"),
           L('phil:war-not-human-nature-russell', 'bridges', "جنگ طبیعت آدمی نیست"),
           L('psy:violence-history-decline', 'see-also', "پس از تبار، تاریخ")],
    people=[p_wrang],
    explain=t("خشونت پیش از آدم بود. جانوران برای خوراک، قلمرو، جفت و جایگاه می‌جنگند، ولی بیشتر این جنگ‌ها نمایش و تهدید است و کمتر به کشتن می‌رسد، چون جنگیدن برای برنده هم خطر دارد. کشتن هم‌گونه جایی بیشتر دیده می‌شود که گونه هم گروهی زندگی کند و هم قلمرو داشته باشد.\n\nچیزی که آدم را جدا می‌کند «بیشتر بودن» خشونت نیست، «شکل» آن است. دو آدم غریبه خیلی راحت‌تر از دو شامپانزهٔ غریبه کنار هم می‌نشینند. ولی آدم می‌تواند با زبان، نقشه و ائتلاف، خشونتی سازمان بدهد که هیچ جانوری نمی‌تواند.",
              "Violence predates humans; what is distinctive in humans is its planned, coalitional form."),
    confusions=[t("«در ژن ماست» با «ناگزیر است» یکی نیست. همان پژوهشی که ریشهٔ تباری را نشان می‌دهد، تغییر چندبرابری آن با شکل جامعه را هم نشان می‌دهد.", "Inherited is not inevitable.")])

add('violence-history-decline',
    title=t("آیا خشونت در تاریخ کم شده است؟", "Has violence declined through history?"),
    summary=t("قتل در اروپای غربی از سده‌های میانه تا سدهٔ بیستم بسیار کم شده است؛ این را بیشتر تاریخ‌نگاران جرم می‌پذیرند. اینکه این یعنی «خشونت» به‌طور کلی کم شده، و چرا، محل بحث است.",
              "Homicide in Western Europe fell greatly from the Middle Ages to the twentieth century; the wider claim is debated."),
    points=[
     P("آیزنر با کنار هم گذاشتن برآوردهای تاریخی نشان داد نرخ قتل در اروپا از حدود ۲۰ در هر صد هزار نفر در سده‌های میانه به حدود ۱۰ در حوالی ۱۶۰۰ و به حدود ۱ در سدهٔ بیستم رسید. بیشترین کاهش در دعواهای مرد با مرد در فضای عمومی و در میان نخبگان بود.",
       "Eisner (2003): roughly 20 → 10 (c.1600) → 1 per 100,000; steepest for male-on-male public fights and elites.", [s_eisner]),
     P("پینکر این روند را به جنگ، شکنجه، برده‌داری و خشونت خانگی هم گسترش داد و آن را به دولت، تجارت، سواد و گسترش دایرهٔ همدلی نسبت داد.",
       "Pinker extended the decline thesis and attributed it to states, commerce, literacy and expanding empathy.", [s_pinker]),
     P("تاریخ‌نگاران منتقد می‌گویند داده‌های پیش از دوران آمار پراکنده و ناهمگون‌اند، برآورد جمعیت آن دوره‌ها بسیار نامطمئن است، و نرخ قتل نمی‌تواند نمایندهٔ همهٔ خشونت باشد.",
       "Historians object that pre-statistical data are patchy, population estimates unreliable, and homicide a poor proxy.", [s_schwer], ['contested']),
     P("در سال ۲۰۲۱ در جهان حدود ۴۵۸ هزار نفر عمداً کشته شدند، یعنی حدود ۵٫۸ در هر صد هزار؛ بیشتر از مجموع کشته‌های جنگ و تروریسم در همان سال.",
       "UNODC: about 458,000 intentional homicides in 2021 (5.8 per 100,000).", [s_gsh]),
    ],
    links=[L('psy:violence-why-expect-none', 'explains', "سازوکارهایی که الیاس و هابز پیشنهاد کردند"),
           L('psy:violence-genealogy', 'contrasts', "خوانش دیگر: خشونت کم نشد، جایش عوض شد")],
    people=[p_eisner, p_elias])

add('violence-genealogy',
    title=t("تبارشناسی خشونت: کلمه و مرزهایش چطور عوض شد", "A genealogy of violence"),
    aliases=["تبارشناسی", "نیچه", "فوکو"],
    summary=t("تبارشناسی، به معنای نیچه و فوکو، نمی‌پرسد خشونت «چیست»؛ می‌پرسد چه کسی، کی و برای چه کاری مرز خشونتِ روا و ناروا را کشید. جواب کوتاه: مرز بارها جابه‌جا شده، و هر بار کسانی که تا دیروز «حق» داشتند بزنند، از امروز «خشن» نامیده شدند.",
              "Genealogy asks who drew the line between legitimate and illegitimate violence, when, and for what."),
    points=[
     P("نیچه در جستار دوم «تبارشناسی اخلاق» می‌گوید خاستگاه یک چیز را نباید با کاری که امروز می‌کند یکی گرفت: کیفر در طول تاریخ بارها معنا عوض کرده است (تلافی، جشن، ترساندن، بازپرداخت بدهی، اصلاح) و معنای امروزش فقط آخرین لایه است.",
       "Nietzsche: the origin of punishment and its present purpose are different things; meanings are layered.", [s_nietz]),
     P("فوکو نشان می‌دهد در اروپا از نیمهٔ سدهٔ هجدهم، شکنجه و اعدام در میدان شهر جای خود را به زندان، برنامهٔ روزانه و نظارت داد. به خوانش او قدرت مهربان‌تر نشد؛ دقیق‌تر شد و از تن به رفتار و روان رسید.",
       "Foucault: public torture gave way to prison, timetable and surveillance; power became more precise, not kinder.", [s_fouc], ['contested']),
     P("بنیامین (۱۹۲۱) دو خشونت را در خودِ قانون می‌بیند: خشونتی که قانون را بنیاد می‌گذارد و خشونتی که آن را نگه می‌دارد. به گفتهٔ او هر نظم حقوقی هر دو را دارد و معمولاً اولی را فراموش می‌کند.",
       "Benjamin: law-making and law-preserving violence.", [s_benj]),
     P("تیلی دولت‌سازی اروپا را به «باج‌گیری حفاظتی» تشبیه کرد: کسانی که بیشترین زور را داشتند رقیبان را از میان برداشتند و در برابر مالیات، امنیت فروختند؛ مشروعیت بعداً آمد.",
       "Tilly: state making resembled a protection racket; legitimacy came later.", [s_tilly]),
     P("جابه‌جایی مرز را می‌شود در قانون دید: تنبیه بدنی کودک، کتک‌زدن همسر، تجاوز در ازدواج و «کنترل اجباری» هرکدام زمانی حق یا امر خصوصی بودند و در دهه‌های اخیر در کشورهایی یکی‌یکی جرم شدند.",
       "The moving line is visible in law: corporal punishment, wife-beating, marital rape and coercive control were each once permitted.", [s_elias, s_who02], ['editor-note']),
    ],
    links=[L('phil:foucault-subjectivation-governmentality-self-ethics', 'bridges', "فوکو و حکومت بر خود"),
           L('psy:coercive-control', 'evidence-for', "تازه‌ترین جابه‌جایی مرز: جرم‌شدن کنترل اجباری"),
           L('psy:violence-what-counts', 'explains', "چرا تعریف‌ها این‌قدر با هم فرق دارند"),
           L('psy:violence-origins', 'contrasts', "تبار به معنای دیگر: ریشهٔ تکاملی")],
    explain=t("«تبار» این‌جا دو معنا دارد و هر دو در این پرونده هست. یکی تبار زیستی است: خشونت در درخت خویشاوندی جانداران از کجا آمده (مدخل «خشونت میان موجودات از کجا شروع شد؟»). دیگری تبارشناسی به معنای فلسفی است: خودِ مفهوم خشونت و مرز روا و ناروایش چه تاریخی دارد.\n\nدومی یک درس عملی دارد. وقتی کسی می‌گوید «این‌که خشونت نیست، همیشه همین‌طور بوده»، تبارشناسی می‌پرسد: برای چه کسی نبوده؟ بیشتر چیزهایی که امروز بی‌تردید خشونت می‌دانیم، روزی همین جمله درباره‌شان گفته می‌شد.",
              "Two senses of lineage: biological descent and conceptual genealogy."))

add('violence-effects-victim',
    title=t("اثر خشونت بر کسی که می‌بیند و اطرافیانش", "Effects on the person harmed and those nearby"),
    summary=t("خشونت فقط همان لحظه و همان آدم را نمی‌زند. بر تن، بر روان، بر رابطه‌ها و بر نسل بعد می‌نشیند؛ و کسی که فقط تماشا کرده هم سهم می‌برد.",
              "Violence reaches body, mind, relationships and the next generation, including those who only witness it."),
    points=[
     P("پژوهش «تجربه‌های ناگوار کودکی» روی بیش از نُه هزار بزرگسال نشان داد هرچه شمار انواع آزار و آشفتگی خانه در کودکی بیشتر باشد، خطر بیماری قلبی، افسردگی، اعتیاد و مرگ زودرس در بزرگسالی پله‌پله بالاتر می‌رود.",
       "ACE study: graded relationship between childhood adversity categories and adult disease.", [s_felitti]),
     P("فراتحلیل ۱۱۸ پژوهش نشان داد کودکانی که فقط شاهد خشونت میان پدر و مادر بوده‌اند، به‌طور میانگین پیامدهای روانی و رفتاری بدتری دارند، تقریباً در همان اندازه که کودکانِ خودْ کتک‌خورده.",
       "Kitzmann et al. (2003): child witnesses fare worse, comparably to physically abused children.", [s_kitz]),
     P("سازمان جهانی بهداشت پیامدهای خشونت علیه زنان را فراتر از جراحت می‌داند: افسردگی، اضطراب، بارداری ناخواسته، بیماری‌های آمیزشی و مشکلات مزمن.",
       "WHO lists depression, anxiety, unintended pregnancy and chronic conditions among consequences.", [s_whovaw]),
     P("اثر در هر نقش فرق می‌کند: در خانه اعتماد پایه را می‌شکند، در مدرسه یادگیری و حضور را، در کار جرئت حرف‌زدن را، و در سطح جامعه اعتماد میان گروه‌ها را برای نسل‌ها.",
       "Effects differ by role: basic trust at home, learning at school, voice at work, intergroup trust in society.", [s_who02], ['editor-note']),
    ],
    links=[L('psy:victim-toll', 'see-also', "آنچه بر تن و روان می‌گذرد"),
           L('psy:cptsd', 'see-also', "آسیب پیچیدهٔ پس از سانحه"),
           L('soc:collective-trauma-justice-revenge', 'bridges', "زخم جمعی، عدالت و انتقام"),
           L('psy:violence-cycle', 'explains', "آیا آسیب‌دیده آسیب‌زن می‌شود؟")])

add('violence-effects-perpetrator',
    title=t("اثر خشونت بر کسی که می‌کند", "Effects on the person who does it"),
    aliases=["آسیب اخلاقی", "moral injury"],
    summary=t("خشونت‌کردن برای بیشتر آدم‌ها بی‌هزینه نیست. بخشی از آسیب روانی جنگ از چیزی می‌آید که آدم کرده یا جلویش را نگرفته، نه از چیزی که بر سرش آمده.",
              "Perpetrating violence is costly for most people; part of war trauma comes from what one did."),
    points=[
     P("لیتز و همکاران «آسیب اخلاقی» را پیامد ماندگار انجام‌دادن، جلوگیری‌نکردن یا دیدنِ کاری می‌دانند که باورهای اخلاقی ریشه‌دار آدم را زیر پا می‌گذارد؛ با شرم، گناه و کناره‌گیری، که با ترسِ معمول در آسیب پس از سانحه فرق دارد.",
       "Litz et al. (2009): moral injury follows perpetrating, failing to prevent or witnessing acts that transgress deep moral beliefs.", [s_litz]),
     P("مک‌نیر شواهدی گرد آورد که کشتن، حتی وقتی قانونی و دستوری است (سرباز، مأمور اعدام، پلیس)، خودش می‌تواند آسیب پس از سانحه بسازد.",
       "MacNair: killing, even when sanctioned, can itself induce traumatic stress.", [s_macn], ['unreplicated']),
     P("در گردان ۱۰۱ پلیس ذخیره، مردانی که در نخستین کشتار تیراندازی کردند شبِ همان روز به گفتهٔ خودشان مست، ساکت و بیمار بودند؛ با تکرار، بیشترشان خو گرفتند.",
       "Browning: after the first massacre the shooters were shaken; with repetition most habituated.", [s_brown]),
    ],
    links=[L('psy:moral-disengagement', 'explains', "کلیدهایی که این هزینه را خاموش می‌کنند"),
           L('psy:violence-roles-switch', 'see-also', "چطور یک آدم دو جور زندگی می‌کند"),
           L('psy:moral-hypocrisy', 'see-also', "فاصلهٔ باور و عمل")])

add('violence-cycle',
    title=t("چرخهٔ خشونت: آیا آسیب‌دیده آسیب‌زن می‌شود؟", "The cycle of violence"),
    summary=t("آزار و غفلت در کودکی خطر خشونت در بزرگسالی را بالا می‌برد، ولی بیشتر کودکان آزاردیده بزرگسال خشن نمی‌شوند. هر دو نیمهٔ این جمله مهم است.",
              "Childhood abuse raises the risk of later violence, yet most abused children do not become violent adults."),
    points=[
     P("ویدوم ۹۰۸ کودک را که آزار یا غفلتشان در دادگاه ثابت شده بود با ۶۶۷ کودک همسان بیست‌وپنج سال دنبال کرد. آزار و غفلت احتمال بازداشت برای جرم خشن را حدود ۳۰ درصد بالا برد.",
       "Widom & Maxfield: 908 substantiated cases vs 667 matched controls; +30% likelihood of violent-crime arrest.", [s_widom]),
     P("ولی حدود ۱۸ درصد از کودکان آزاردیده برای جرم خشن بازداشت شدند؛ یعنی بیش از چهار نفر از هر پنج نفر نه.",
       "About 18% of the abused group were arrested for a violent crime; more than four in five were not.", [s_widom]),
     P("کودکان غفلت‌شده، که کتک نخورده بودند، تقریباً به همان اندازهٔ کودکان کتک‌خورده در خطر بودند. یعنی «خشونت خشونت می‌آورد» توضیح کاملی نیست؛ نبودِ مراقبت هم همان کار را می‌کند.",
       "Neglected children were nearly as much at risk as physically abused ones.", [s_widom]),
    ],
    links=[L('psy:breaking-cycle', 'see-also', "چطور چرخه می‌شکند"),
           L('psy:violence-effects-victim', 'part-of', "یکی از اثرهای خشونت"),
           L('psy:violence-epidemic', 'see-also', "سرایت در شبکه، نه فقط در خانواده")],
    people=[p_widom],
    confusions=[t("«خطر بیشتر» با «سرنوشت» یکی نیست. این جمله که «هر کس کتک خورده، کتک می‌زند» هم نادرست است و هم به کسانی که چرخه را شکسته‌اند ستم می‌کند.", "Higher risk is not destiny.")])

add('violence-roles-switch',
    title=t("یک آدم، چند نقش: چطور در یک نقش خشن و در نقش دیگر مهربان؟", "One person, several roles"),
    aliases=["دوپاره‌شدن", "doubling", "اطاعت", "میلگرام"],
    summary=t("خشونت بیشتر به موقعیت و نقش چسبیده است تا به آدم. نقش به آدم می‌گوید این‌جا چه کسی «از ما»ست، چه کاری «وظیفه» است و مسئولیت با کیست؛ و آدم‌ها می‌توانند دو نقش را در دو اتاق جدا در ذهن نگه دارند.",
              "Violence attaches to situations and roles more than to persons; people can keep two roles in separate mental rooms."),
    points=[
     P("لیفتون در گفت‌وگو با پزشکان اردوگاه‌های نازی سازوکاری دید که آن را «دوپاره‌شدن» نامید: خودِ دومی ساخته می‌شود که در اردوگاه کار می‌کند، با قاعده‌های آن‌جا؛ و خودِ اول شب به خانه می‌رود و پدر و همسر می‌ماند.",
       "Lifton: 'doubling' — a second self that functions in the camp while the first remains husband and father.", [s_lifton]),
     P("در آزمایش میلگرام (۱۹۶۳) ۲۶ نفر از ۴۰ نفر تا آخرین کلید شوک پیش رفتند. آدم‌ها همان آدم‌های بیرون آزمایشگاه بودند؛ چیزی که عوض شده بود موقعیت بود.",
       "Milgram (1963): 26 of 40 went to the maximum shock.", [s_milg]),
     P("بازخوانی‌های تازه می‌گویند این «اطاعت کور» نبود: شرکت‌کنندگان وقتی ادامه می‌دادند که خود را با هدف علمی آزمایشگر یکی می‌دانستند، و درست وقتی دستور مستقیم می‌شنیدند («چارهٔ دیگری ندارید») بیشتر سر باز می‌زدند. نام این خوانش «پیروی درگیرانه» است.",
       "Reicher, Haslam & Smith: identification-based 'engaged followership', not blind obedience.", [s_reich], ['contested']),
     P("آزمایش زندان استنفورد، که سال‌ها نمونهٔ «نقش آدم را عوض می‌کند» بود، با بررسی بایگانی‌ها زیر سؤال رفته است: نگهبان‌ها راهنمایی شده بودند که سخت بگیرند، و روش و گزارش آن اشکال‌های جدی داشت.",
       "Le Texier (2019): archival evidence that guards were coached; the Stanford Prison Experiment is unreliable.", [s_letex], ['contested']),
     P("کالینز از بررسی فیلم و عکس صدها درگیری نتیجه می‌گیرد خشونت به آدم‌ها آسان نمی‌آید: رودررویی تنش و ترس می‌سازد و بیشتر تهدیدها به عمل نمی‌رسد. خشونت وقتی رخ می‌دهد که موقعیت راهی برای دورزدن این تنش بدهد، مثل حمله به ضعیف، حمله از دور، یا داشتن تماشاگرِ همراه.",
       "Collins: confrontational tension makes violence hard; it happens when the situation offers a way round it.", [s_coll]),
     P("در خانه هم همین جداسازی دیده می‌شود. جانسون «تروریسم خانگی» را، که خشونت در دل یک الگوی کنترل است و بیرون خانه دیده نمی‌شود، از «خشونت موقعیتی زوج» جدا می‌کند.",
       "Johnson distinguishes intimate terrorism from situational couple violence.", [s_john], ['contested']),
    ],
    links=[L('psy:moral-disengagement', 'explains', "هشت کلیدی که جداسازی را ممکن می‌کند"),
           L('psy:public-private', 'see-also', "چهرهٔ بیرون و چهرهٔ خانه"),
           L('phil:arendt-obedience-is-support', 'bridges', "اطاعت در سیاست یعنی پشتیبانی"),
           L('phil:arendt-conscience-thinking-nonparticipants', 'bridges', "آن‌ها که شرکت نکردند"),
           L('psy:violence-cannot', 'contrasts', "آن‌ها که در همان نقش نکردند")],
    people=[p_lifton, p_coll, p_brown],
    explain=t("مردی را در نظر بگیرید که در بازجویی سیلی می‌زند و عصر دخترش را با حوصله از مدرسه برمی‌دارد. این دو با هم ناسازگار به نظر می‌رسند فقط اگر فکر کنیم خشونت یک «خصلت» است. اگر آن را چیزی بدانیم که نقش مجاز و حتی واجبش می‌کند، ناسازگاری از میان می‌رود: در اتاق بازجویی او «کارش را می‌کند»، طرف مقابل «دشمن» است و مسئولیت «با بالادست» است. در خانه هیچ‌کدام از این سه برقرار نیست.\n\nبرعکسش هم هست: کسی که در اداره آرام‌ترین همکار است و در خانه همه از او می‌ترسند. آن‌جا هم یک نقش هست («مرد خانه»، «بزرگ‌تر») که به او می‌گوید این‌جا قلمرو اوست و کسی حق بازخواست ندارد.\n\nاین توضیح است، نه عذر. کسی که نقش را می‌پذیرد، مسئول پذیرفتنش است.",
              "A man who strikes in an interrogation room and gently collects his daughter from school: role, not trait, reconciles the two. Explanation is not excuse."))

add('moral-disengagement',
    title=t("خاموش‌کردن وجدان: هشت کلید بندورا", "Moral disengagement"),
    aliases=["خاموشی اخلاقی", "بی‌تعهدی اخلاقی"],
    summary=t("آدم‌ها معمولاً برای آسیب‌زدن معیارهای اخلاقی‌شان را عوض نمی‌کنند؛ آن را موقتاً از مدار بیرون می‌آورند. بندورا هشت راه برای این کار برشمرد.",
              "People rarely change their moral standards to do harm; they disengage them, by eight mechanisms."),
    points=[
     P("سه کلید روی خودِ کار می‌نشیند: «توجیه اخلاقی» (برای هدفی والا است)، «نام‌گذاری پاکیزه» (پاک‌سازی، تأدیب، برخورد) و «مقایسهٔ سودمند» (دیگران بدترش را می‌کنند).",
       "On the act: moral justification, euphemistic labelling, advantageous comparison.", [s_band]),
     P("دو کلید روی مسئولیت: «جابه‌جاکردن مسئولیت» (دستور بود) و «پخش‌کردن مسئولیت» (همه بودیم، من فقط یک تکه‌اش را انجام دادم).",
       "On responsibility: displacement and diffusion.", [s_band]),
     P("یک کلید روی پیامد: «ندیدن یا کوچک‌کردن آسیب» (چیزی‌اش نشد). هرچه فاصلهٔ آدم با نتیجهٔ کارش بیشتر باشد این کلید آسان‌تر زده می‌شود.",
       "On consequences: disregarding or distorting harm.", [s_band]),
     P("دو کلید روی قربانی: «انسانیت‌زدایی» (این‌ها آدم نیستند) و «مقصر دانستن قربانی» (خودش باعث شد).",
       "On the victim: dehumanisation and attribution of blame.", [s_band, s_hasl]),
    ],
    links=[L('psy:dehumanization', 'part-of', "یکی از هشت کلید"),
           L('psy:darvo', 'see-also', "انکار، حمله، وارونه‌کردن قربانی و آزارگر"),
           L('psy:violence-roles-switch', 'explains', "چطور دو نقش کنار هم می‌مانند"),
           L('psy:violent-apartheid', 'applies-to', "همین کلیدها در مقیاس یک کشور")],
    people=[p_band],
    confusions=[t("این کلیدها ویژهٔ «آدم‌های بد» نیست. هر کدام را در حرف‌های روزمرهٔ خودمان می‌شود پیدا کرد: «من که فقط گفتم»، «بقیه بدترند»، «خودش شروع کرد».", "These switches are ordinary, not reserved for villains.")])

add('virtuous-violence',
    title=t("اخلاق و خشونت: دشمن هم یا خویشاوند؟", "Morality and violence"),
    aliases=["خشونت فضیلت‌مندانه", "افسانهٔ شر ناب"],
    summary=t("دوست داریم فکر کنیم خشونت یعنی شکست اخلاق. بخش بزرگی از پژوهش می‌گوید برعکس: بیشتر کسانی که خشونت می‌کنند، در همان لحظه باور دارند کار درست را می‌کنند. اخلاق هم ترمز خشونت است و هم سوختش.",
              "Much violence is morally motivated in the eyes of those who commit it; morality is both brake and fuel."),
    points=[
     P("فیسک و رای با مرور مردم‌نگاری‌ها و تاریخ استدلال می‌کنند بیشتر خشونت‌ها برای «درست‌کردن یک رابطه» انجام می‌شود: تنبیه برای ادب‌کردن، انتقام برای برابرکردن حساب، قتل ناموسی برای بازگرداندن آبرو، جنگ برای وفاداری به گروه. فاعل آن را وظیفه می‌بیند، نه لغزش.",
       "Fiske & Rai: most violence is intended to regulate relationships and feels obligatory to the perpetrator.", [s_fiske], ['contested']),
     P("بامایستر «افسانهٔ شرّ ناب» را توصیف می‌کند: تصویری که در آن آزارگر بی‌دلیل و از سر لذت آسیب می‌زند و قربانی کاملاً بی‌گناه است. به گفتهٔ او این تصویر بیشتر از دید قربانی و قصه‌ها می‌آید و جلوی فهم خشونت واقعی را می‌گیرد.",
       "Baumeister: the 'myth of pure evil' obscures how perpetrators actually understand their acts.", [s_baum97]),
     P("در برابر، سنت‌های اخلاقی بزرگ ترمز می‌سازند: اصل آسیب (میل)، اینکه آدم هیچ‌گاه فقط وسیله نیست (کانت)، و حق هر کس بر تن خودش. بحث «جنگ عادلانه» و «دفاع مشروع» همین‌جاست: کجا خشونت روا می‌شود و چه کسی داور است.",
       "Moral traditions also restrain violence: harm principle, persons as ends, bodily rights.", [s_mill, s_udhr]),
     P("دربارهٔ کارایی هم داده هست: از ۱۹۰۰ تا ۲۰۰۶ کارزارهای بی‌خشونت در ۵۳ درصد موارد به هدف رسیدند و کارزارهای مسلحانه در ۲۶ درصد.",
       "Stephan & Chenoweth: 53% success for nonviolent campaigns vs 26% for violent ones, 1900–2006.", [s_chen]),
     P("خود چنووث بعدتر نشان داد کامیابی کارزارهای بی‌خشونت از دههٔ ۲۰۱۰ پایین آمده است؛ یکی از دلیل‌های پیشنهادی تکیهٔ زیاد بر تظاهرات بزرگ و کم‌شدن سهم مشارکت مردم است.",
       "Chenoweth (2020): success of nonviolent campaigns has fallen since 2010.", [s_chen20], ['contested']),
    ],
    links=[L('phil:explaining-versus-justifying-suspended-judgment', 'bridges', "توضیح‌دادن توجیه‌کردن نیست"),
           L('soc:honor-control-women-reproduction-function', 'bridges', "ناموس و کنترل"),
           L('psy:moral-disengagement', 'contrasts', "دو روایت: اخلاق خاموش می‌شود یا خودش فرمان می‌دهد؟"),
           L('psy:violence-why-expect-none', 'contrasts', "ترمزهای اخلاقی")],
    people=[p_fiske, p_baum],
    explain=t("دو روایت رقیب هست و هر دو شواهد دارند. روایت بندورا: آدم می‌داند کارش بد است و وجدانش را خاموش می‌کند. روایت فیسک و رای: آدم باور دارد کارش خوب است و وجدانش او را هل می‌دهد. پدری که بچه را می‌زند «تا آدم شود» در کدام است؟ احتمالاً در هر دو، در لحظه‌های مختلف.\n\nنتیجهٔ عملی این است که «آگاه‌کردن از بدیِ خشونت» همیشه کافی نیست. اگر کسی خشونتش را وظیفه می‌داند، باید خودِ آن وظیفه و آن تصویر از رابطهٔ درست را عوض کرد؛ کاری که هنجارهای یک گروه می‌کنند، نه نصیحت.",
              "Two rival accounts — disengaged conscience vs. conscience as driver — both have evidence."),
    confusions=[t("فهمیدنِ اینکه فاعل خودش را برحق می‌داند، به معنای برحق دانستن او نیست.", "Understanding a perpetrator's moral view is not endorsing it.")])

add('violence-cannot',
    title=t("آیا آدم‌هایی هستند که نتوانند خشونت کنند؟", "Are there people who cannot be violent?"),
    summary=t("شواهدی از «ناتوانی» به معنای دقیق نیست. آنچه هست یک بازدارندهٔ قوی در بیشتر آدم‌هاست که شدتش فرق می‌کند، و آدم‌هایی که حتی زیر فشار گروه و دستور، نمی‌کنند.",
              "There is no evidence of strict inability; there is a strong inhibition of varying strength, and people who refuse even under pressure."),
    points=[
     P("بلر سازوکاری پیشنهاد کرد که با دیدن نشانه‌های درماندگی (چهرهٔ ترسیده، گریه) حمله را متوقف می‌کند، و گفت در روان‌آزاری همین سازوکار ضعیف است. این یک مدل است و بحث دربارهٔ آن ادامه دارد.",
       "Blair's violence inhibition mechanism: distress cues stop aggression; proposed to be weak in psychopathy.", [s_blair], ['contested']),
     P("به گفتهٔ کالینز بیشتر آدم‌ها در خشونتِ رودررو ناتوان‌اند، نه از سر فضیلت بلکه از تنش: دست می‌لرزد، ضربه خطا می‌رود، و بیشتر درگیری‌ها به داد و هل‌دادن ختم می‌شود. خشونتِ کارآمد کار اقلیتی کوچک است که یاد گرفته‌اند این تنش را مهار کنند.",
       "Collins: most people are incompetent at face-to-face violence because of confrontational tension.", [s_coll]),
     P("در یوزفوف (۱۹۴۲) فرمانده به حدود ۵۰۰ مرد گردان ۱۰۱ گفت هر کس نمی‌تواند کنار برود. حدود دوازده نفر همان اول کنار رفتند و به برآورد براونینگ ۱۰ تا ۲۰ درصد در طول روز از تیراندازی کنار کشیدند. کسی برای این کار مجازات نشد.",
       "Józefów 1942: about a dozen of ~500 stepped out; 10–20% evaded shooting; none was punished.", [s_brown]),
     P("ادعای مشهور مارشال که در جنگ جهانی دوم فقط ۱۵ تا ۲۵ درصد سربازان پیاده شلیک می‌کردند، پشتوانهٔ مستند ندارد: بررسی یادداشت‌های او نشان داد مصاحبه‌هایی که چنین عددی از آن‌ها دربیاید انجام نشده بود.",
       "Marshall's 15–25% 'ratio of fire' lacks documentary support (Spiller, 1988).", [s_marsh, s_spill], ['contested']),
    ],
    links=[L('psy:violence-roles-switch', 'contrasts', "آن‌ها که در همان موقعیت کردند"),
           L('phil:arendt-conscience-thinking-nonparticipants', 'bridges', "آرنت دربارهٔ کسانی که شرکت نکردند"),
           L('psy:violence-origins', 'see-also', "کم‌بودن پرخاشگری لحظه‌ای در آدم")],
    explain=t("پرسش را می‌شود دو جور خواند. اگر یعنی «آدمی هست که در هیچ شرایطی، حتی برای دفاع از بچه‌اش، دست بلند نکند؟»، پژوهشی نیست که چنین گروهی را نشان بدهد. اگر یعنی «آدم‌هایی هستند که وقتی همه می‌کنند و دستور هم هست، نکنند؟»، بله، و در هر نمونهٔ تاریخی که خوب مستند شده دیده می‌شوند. آن‌ها معمولاً قهرمان‌نمایی نمی‌کنند؛ خیلی‌هایشان فقط می‌گویند «نتوانستم».",
              "Two readings of the question: absolute inability (no evidence) vs refusing when everyone else complies (well documented)."))

add('violence-unseen-by-doer',
    title=t("آیا آدم‌هایی هستند که نفهمند دارند خشونت می‌کنند؟", "Violence unseen by the one who does it"),
    summary=t("بله، و این حالتِ رایج است نه استثنا. آزارگر و آزاردیده یک رویداد را با دو اندازهٔ بسیار متفاوت به یاد می‌آورند، و هنجار می‌تواند یک کار را از دستهٔ «خشونت» به‌کل بیرون ببرد.",
              "Common, not exceptional: perpetrators and victims remember the same event at very different sizes, and norms can take an act out of the category altogether."),
    points=[
     P("بامایستر و همکاران از آدم‌ها خواستند یک بار ماجرایی را بنویسند که در آن کسی را عصبانی کرده‌اند و یک بار ماجرایی که خودشان عصبانی شده‌اند. در نقش آزارگر، ماجرا یک رویداد تمام‌شده، قابل‌فهم و کم‌اثر بود؛ در نقش آزاردیده، بی‌دلیل، ادامه‌دار و پراثر. همان آدم‌ها، دو روایت.",
       "Baumeister, Stillwell & Wotman (1990): perpetrator accounts minimise and close the incident; victim accounts extend it.", [s_baum90]),
     P("فراتحلیلی از ده‌ها پژوهش نشان داد کودکان پرخاشگر بیشتر از دیگران رفتار مبهم دیگران را عمدی و دشمنانه می‌خوانند. از دید خودشان آن‌ها «جواب می‌دهند»، شروع نمی‌کنند.",
       "Orobio de Castro et al. (2002): aggressive children show a robust hostile attribution bias.", [s_orobio]),
     P("به گزارش برنامهٔ توسعهٔ ملل متحد، از هر چهار نفر در جهان یک نفر باور دارد کتک‌زدن زن به دست شوهر موجه است. کسی که چنین باوری دارد کار خود را «خشونت» نمی‌نامد.",
       "UNDP GSNI 2023: 25% of people believe it is justified for a man to beat his wife.", [s_undp]),
     P("دربارهٔ «خرده‌پرخاش» (حرف‌ها و رفتارهای کوچک و اغلب ناخواسته که به گروهی کم‌قدرت نیش می‌زند) بحث علمی باز است: منتقدان می‌گویند تعریف و سنجش آن هنوز سست است.",
       "Microaggressions: concept and measurement remain contested (Lilienfeld, 2017).", [s_lil], ['contested']),
    ],
    links=[L('psy:moral-disengagement', 'explains', "ندیدن، با کلیدهای وجدان"),
           L('psy:defensive-reactions', 'see-also', "واکنش دفاعی وقتی کسی می‌گوید آزارم دادی"),
           L('psy:violence-unseen-by-victim', 'contrasts', "روی دیگر: قربانی‌ای که نمی‌داند"),
           L('psy:virtuous-violence', 'see-also', "وقتی خشونت وظیفه دیده می‌شود")],
    people=[p_baum],
    explain=t("سه راهِ ندیدن هست. اول اندازه: کاری که برای من «یک حرف بود» برای تو ده سال مانده. دوم نیت: من «جواب دادم»، تو «حمله کردی». سوم نام: در خانه و محلهٔ من به این کار می‌گویند تربیت، غیرت، شوخی، نظم. هر سه با صداقت کامل همراه‌اند؛ آدم دروغ نمی‌گوید، واقعاً نمی‌بیند.\n\nبرای همین پرسش «قصد داشتی آزار بدهی؟» کمتر به جایی می‌رسد. پرسش‌های بهتر: «او بعدش چه کرد؟ از تو فاصله گرفت؟ ساکت شد؟ چیزی را دیگر نگفت یا نپوشید یا نخواست؟»",
              "Three ways of not seeing: size, intent, name."))

add('violence-unseen-by-victim',
    title=t("آیا آدم‌هایی هستند که ندانند مورد خشونت‌اند؟", "Violence unseen by the one it is done to"),
    aliases=["تجاوز نام‌گذاری‌نشده", "ترجیح سازگارشده"],
    summary=t("بله. آدم می‌تواند دقیقاً آنچه را که تعریف قانونی یا پزشکی خشونت است تجربه کرده باشد و نام دیگری رویش بگذارد. دلیلش نادانی نیست؛ نام‌ها را فرهنگ می‌دهد، و نام‌گذاشتن هزینه دارد.",
              "Yes: people can experience what meets the definition and call it something else, because names are supplied by culture and naming is costly."),
    points=[
     P("فراتحلیل ۲۸ پژوهش با ۵٬۹۱۷ زن که تجربه‌شان با تعریف تجاوز می‌خواند نشان داد ۶۰٫۴ درصد آن را تجاوز نمی‌نامیدند و نام‌هایی مثل «رابطهٔ بد» یا «سوءتفاهم» به کار می‌بردند. ناهمگونی میان پژوهش‌ها زیاد بود و بیشترشان روی دانشجویان آمریکایی.",
       "Wilson & Miller (2016): 60.4% (95% CI 55.0–65.6) of 5,917 female rape survivors did not label the experience rape; high heterogeneity.", [s_wm]),
     P("نتیجهٔ روش‌شناختی همان پژوهش: پرسش‌نامه باید رفتار را توصیف کند («آیا کسی بدون رضایت شما…») نه اینکه برچسب بپرسد («آیا به شما تجاوز شده؟»). عددِ خشونت به شکل پرسش بسته است.",
       "Screening should use behaviourally descriptive items, not labels.", [s_wm]),
     P("بوردیو توضیح می‌دهد چرا: زیردست جهان را با همان دسته‌بندی‌هایی می‌فهمد که سلطه ساخته، پس آنچه بر او می‌رود «طبیعی» به نظرش می‌رسد.",
       "Bourdieu: the dominated perceive through categories produced by domination.", [s_bourd]),
     P("در کنترل اجباری، بسیاری از قربانیان از «در قفس بودن» حرف می‌زنند ولی چون کتکی در کار نیست یا کم است، خود را «خشونت‌دیده» نمی‌دانند.",
       "In coercive control victims describe entrapment yet do not identify as victims of violence.", [s_who02], ['editor-note']),
     P("سازمان جهانی بهداشت می‌گوید شیوع واقعی خشونت علیه زنان به احتمال زیاد از عددهای گزارش‌شده بالاتر است، چون ننگ و ترس جلوی گفتن را می‌گیرد.",
       "WHO: true prevalence is likely higher than reported because of stigma.", [s_whovaw]),
    ],
    links=[L('psy:coercive-control', 'see-also', "قفسی که میله‌هایش دیده نمی‌شود"),
           L('psy:gaslighting', 'explains', "وقتی به حافظهٔ خودت شک می‌کنی"),
           L('soc:preference-falsification', 'bridges', "آنچه می‌گوییم با آنچه می‌خواهیم فرق دارد"),
           L('phil:epistemic-injustice', 'bridges', "وقتی کلمه‌ای برای تجربه‌ات نداری"),
           L('psy:violence-what-counts', 'explains', "تعریف تعیین می‌کند چه کسی خودش را بشمارد")],
    confusions=[t("نام‌نگذاشتن به معنای آسیب‌ندیدن نیست. پژوهش‌ها پیامدهای روانی را در هر دو گروه می‌بینند.", "Not labelling does not mean not harmed."),
                t("این یافته اجازه نمی‌دهد به کسی بگوییم «تو قربانی‌ای و خودت نمی‌دانی». نام‌گذاشتن حق خود آدم است؛ کار دیگران این است که کلمه‌ها و امکان را در دسترس بگذارند.", "It does not license telling someone they are a victim.")])

add('violence-gender-women',
    title=t("خشونت علیه زنان: پیدا و پنهان", "Violence against women"),
    summary=t("زنان کمتر از مردان کشته می‌شوند، ولی جایی کشته می‌شوند که باید امن‌ترین باشد: خانه. و بخش بزرگ خشونت علیه زنان اصلاً به شکل کشتن نیست.",
              "Women are killed less often than men, but mostly at home; and most violence against women is not lethal."),
    points=[
     P("به برآورد سازمان جهانی بهداشت نزدیک به یک‌سوم زنان جهان، حدود ۸۴۰ میلیون نفر، در طول زندگی خشونت بدنی یا جنسی از شریک زندگی یا خشونت جنسی از دیگران دیده‌اند. این سهم از سال ۲۰۰۰ تقریباً عوض نشده است.",
       "WHO: about 840 million women, nearly one in three; barely changed since 2000.", [s_who25]),
     P("فقط در دوازده ماه پیش از سنجش، ۳۱۶ میلیون زن (۱۱ درصد زنان ۱۵ ساله و بالاتر) از شریک زندگی خشونت بدنی یا جنسی دیده بودند.",
       "316 million women (11%) experienced partner violence in the previous 12 months.", [s_who25]),
     P("در سال ۲۰۲۴ حدود ۸۳ هزار زن و دختر عمداً کشته شدند؛ ۵۰ هزار نفرشان، یعنی ۶۰ درصد، به دست شریک زندگی یا خویشاوند. یعنی هر ده دقیقه یک نفر. برای مردان این سهم ۱۱ درصد است.",
       "2024: 83,000 women and girls killed; 50,000 (60%) by partners or family; 11% for male victims.", [s_fem25]),
     P("بیش از ۲۳۰ میلیون دختر و زنِ زنده ناقص‌سازی جنسی شده‌اند؛ ۳۰ میلیون بیشتر از برآورد هشت سال پیش.",
       "UNICEF 2024: over 230 million girls and women alive have undergone FGM.", [s_fgm]),
     P("آمارتیا سن در ۱۹۹۰ حساب کرد اگر نسبت زن به مرد در آسیا و شمال آفریقا مثل جاهایی بود که مراقبت برابر است، بیش از صد میلیون زن بیشتر زنده بودند. این خشونتی است بی‌ضربه: سقط گزینشی، خوراک و درمان کمتر برای دختر.",
       "Sen (1990): more than 100 million women 'missing'.", [s_sen], ['dated']),
    ],
    links=[L('psy:violence-gender-men', 'contrasts', "تصویر مردان"),
           L('psy:violence-gender-history', 'part-of', "در طول تاریخ"),
           L('soc:cultural-signs-gender-control', 'bridges', "نشانه‌های فرهنگی کنترل"),
           L('soc:norms-as-collective-bargains-gender-division-labour', 'bridges', "هنجار به‌عنوان چانه‌زنی جمعی"),
           L('psy:coercive-control', 'see-also', "کنترل اجباری")])

add('violence-gender-men',
    title=t("خشونت علیه مردان: پیدا و پنهان", "Violence against men"),
    summary=t("مردان هم بیشترِ کشندگان‌اند و هم بیشترِ کشته‌شدگان. خشونتی که می‌بینند بیشتر بیرون خانه و به دست مردان دیگر است، و بخشی از آن چنان عادی شده که نامش خشونت نیست: سربازی اجباری، کار مرگبار، و انتظار اینکه دم نزنند.",
              "Men are most of the killers and most of the killed; some of the violence they face is so normalised it is not called violence."),
    points=[
     P("در سال ۲۰۲۱ مردان ۸۱ درصد قربانیان قتل عمد و حدود ۹۰ درصد مظنونان بودند. نرخ قتل برای مردان ۹٫۳ و برای زنان ۲٫۲ در هر صد هزار نفر بود.",
       "UNODC: men were 81% of homicide victims and ~90% of suspects in 2021.", [s_gsh]),
     P("همین الگو در خویشاوندان ما هم هست: در شامپانزه‌ها ۹۲ درصد حمله‌کنندگان و ۷۳ درصد قربانیانِ کشتن نر بودند.",
       "In chimpanzees 92% of attackers and 73% of victims were male.", [s_wilson14]),
     P("آیزنر نشان می‌دهد کاهش بلندمدت قتل در اروپا بیش از همه کاهش دعوای مرد با مرد در فضای عمومی بود: خشونتی که روزگاری برای دفاع از آبرو لازم شمرده می‌شد.",
       "The long European decline was mostly a decline in male-on-male public fights.", [s_eisner]),
     P("نیسبت و کوهن «فرهنگ آبرو» را توصیف کردند: جایی که دولت دور است و دارایی دزدیدنی، مردی که به توهین جواب ندهد همه‌چیزش در خطر است. پس هنجار از مردان خشونت می‌خواهد و مردِ بی‌خشونت را تنبیه می‌کند.",
       "Nisbett & Cohen: cultures of honor require violent responses from men.", [s_nisb], ['contested']),
     P("خشونت جنسی و خانگی علیه مردان کمتر سنجیده شده است؛ پیمایش‌های بزرگ جهانی مثل برآوردهای سازمان جهانی بهداشت فقط زنان را می‌شمارند. این یک جای خالی در داده است، نه نشانهٔ نبودن.",
       "Major global surveys measure only women; violence against men is a data gap.", [s_who25], ['editor-note']),
    ],
    links=[L('psy:violence-gender-women', 'contrasts', "تصویر زنان"),
           L('psy:violence-gender-history', 'part-of', "در طول تاریخ"),
           L('psy:evo-sex', 'see-also', "تفاوت‌های دو جنس از نگاه تکاملی"),
           L('soc:gender-coalition-not-enmity', 'bridges', "ائتلاف، نه دشمنی")],
    confusions=[t("این دو تصویر رقیب هم نیستند. یک نظام هنجاری، مردان را به خشونت در بیرون وامی‌دارد و زنان را در خانه بی‌دفاع می‌گذارد؛ هر دو از یک‌جا آب می‌خورند.", "The two pictures are not rivals; one norm system produces both.")])

add('violence-gender-history',
    title=t("جنسیت و خشونت در طول تاریخ", "Gender and violence through history"),
    summary=t("در بیشتر تاریخِ نوشته‌شده، خشونت بر پایهٔ جنسیت تقسیم کار داشته است: تن مردان برای جنگ و کار خرج شده، تن زنان برای زادوولد و آبرو کنترل شده، و کسانی که در هیچ‌کدام از دو قالب نمی‌گنجیدند مجازات شده‌اند.",
              "Through recorded history violence has been divided by gender: men's bodies spent on war and labour, women's controlled for reproduction and honour, non-conformers punished."),
    points=[
     P("خشونت پیدا علیه زنان: در شکار جادوگران اروپای سده‌های ۱۵ تا ۱۸، به برآورد لواک حدود ۴۵ هزار نفر اعدام شدند و نزدیک سه‌چهارمشان زن بودند.",
       "Levack: roughly 45,000 executions in the European witch-hunts, about three quarters women.", [s_levack], ['contested']),
     P("خشونت پنهان علیه زنان بیشتر در قانون و عرف بود تا در ضربه: نداشتن حق مالکیت، طلاق، درس و رفت‌وآمد؛ ازدواج در کودکی؛ و حق شوهر بر تن زن. این‌ها در تعریف گالتونگ خشونت ساختاری‌اند.",
       "Hidden violence against women lay in law and custom: property, divorce, schooling, movement, child marriage.", [s_galt69, s_who02], ['editor-note']),
     P("خشونت پیدا علیه مردان: جنگ. سربازگیری اجباری تقریباً همیشه و همه‌جا فقط مردان را گرفته است، و امروز هم چهار نفر از هر پنج کشتهٔ قتل عمد مردند.",
       "Open violence against men: war and conscription; four in five homicide victims today are male.", [s_gsh], ['editor-note']),
     P("خشونت پنهان علیه مردان هنجاری است که از آن‌ها خشونت می‌خواهد و ترس و درد را بر آن‌ها ممنوع می‌کند، و مردی را که تن نمی‌دهد با تحقیر مجازات می‌کند.",
       "Hidden violence against men: norms that demand violence and forbid fear.", [s_nisb, s_bourd], ['editor-note']),
     P("برای کسانی که در قالب دو جنس نمی‌گنجند داده‌ها کم ولی سنگین است: مروری نظام‌مند شیوع خشونت بدنی در طول زندگی زنان ترنس را ۴۱ درصد و خشونت جنسی را ۳۰ درصد برآورد کرده است.",
       "A systematic review cited by WHO: 41% lifetime physical and 30% sexual violence among trans women.", [s_whovaw]),
    ],
    links=[L('soc:honor-control-women-reproduction-function', 'bridges', "کارکرد ناموس"),
           L('soc:unveiling-1936-gender-order-and-symbols', 'bridges', "نظم جنسیتی و نشانه‌ها"),
           L('psy:violence-genealogy', 'see-also', "مرزهایی که جابه‌جا شدند"),
           L('psy:violent-apartheid', 'see-also', "وقتی این نظم قانون سراسری می‌شود")],
    explain=t("چهار خانه را تصور کنید: پیدا و پنهان، برای زنان و مردان. خانهٔ «پیدا، زنان» را همه می‌شناسند. خانهٔ «پیدا، مردان» آن‌قدر بزرگ است که دیده نمی‌شود: میدان جنگ. دو خانهٔ «پنهان» سخت‌تر دیده می‌شوند چون ضربه ندارند: یکی قانون و عرفی است که زن را کوچک نگه می‌دارد، دیگری هنجاری است که مرد را سخت و خرج‌شدنی می‌خواهد.\n\nاین جدول برای مسابقهٔ «چه کسی بیشتر کشید» نیست. برای دیدن این است که چهار خانه به هم قفل‌اند: مردی که باید آبرویش را با زور نگه دارد و زنی که آبروی او در تن اوست، دو نیمهٔ یک سازوکارند.",
              "A two-by-two of open/hidden and women/men; the four cells interlock."))

add('violence-epidemic',
    title=t("چرا خشونت مثل همه‌گیری پخش می‌شود؟", "Why violence spreads like an epidemic"),
    aliases=["سرایت خشونت", "واگیر خشونت"],
    summary=t("خشونت خوشه‌ای است: در زمان، در مکان و در شبکهٔ آدم‌ها جمع می‌شود و از یکی به دیگری می‌رسد. سه راه سرایت دارد: تلافی، یادگیری، و هنجار.",
              "Violence clusters in time, place and networks and passes on by retaliation, learning and norms."),
    points=[
     P("در شبکه‌ای از ۱۳۸ هزار نفر در شیکاگو (کسانی که با هم بازداشت شده بودند)، ۶۳ درصد از ۱۱٬۱۲۳ مورد تیرخوردن را می‌شد با سرایت در شبکه توضیح داد. فرد به‌طور میانگین ۱۲۵ روز پس از تیرخوردن «سرایت‌دهنده»‌اش تیر می‌خورد.",
       "Green, Horel & Papachristos (2017): social contagion accounted for 63.1% of 11,123 gunshot episodes; mean lag 125 days.", [s_green]),
     P("اسلاتکین، که همه‌گیرشناس بود، گفت خشونت سه ویژگی بیماری واگیر را دارد: خوشه می‌سازد، از راه تماس پخش می‌شود، و قرارگرفتن در معرضش خطر انجامش را بالا می‌برد. این یک تشبیه کارآمد است، نه ادعایی دربارهٔ میکروب.",
       "Slutkin: violence clusters, spreads and transmits like a contagious disease — a working analogy.", [s_slut], ['contested']),
     P("هنجار هم سرایت می‌کند. در «فرهنگ آبرو» هر کس خشن است چون گمان می‌کند دیگران از او همین را می‌خواهند؛ کافی است هر کس آستانه‌ای داشته باشد («اگر این‌قدر نفر بکنند، من هم می‌کنم») تا یک رفتار کل گروه را بگیرد.",
       "Norms spread too: honor cultures and threshold dynamics.", [s_nisb], ['editor-note']),
     P("اگر سرایت باشد، می‌شود زنجیره را برید. در اسکاتلند پس از ۲۰۰۵ خشونت را مسئلهٔ سلامت عمومی دیدند؛ شمار قتل از ۱۳۷ (۲۰۰۴ تا ۲۰۰۵) در ده سال بعد تقریباً نصف شد و بستری برای زخم چاقو در گلاسگو ۶۲ درصد کم شد. قتل در همان سال‌ها در جاهای دیگر هم کم شد، پس سهم دقیق این برنامه روشن نیست.",
       "Scotland after 2005: homicides roughly halved; sharp-object admissions in Glasgow fell 62%; attribution is uncertain.", [s_vru], ['contested']),
     P("در کاردیف، بیمارستان‌ها جا و زمان زخمی‌شدن را بی‌نام به پلیس و شهرداری دادند. نسبت به چهارده شهر مشابه، بستری به علت خشونت ۴۲ درصد کمتر شد.",
       "Cardiff Model (Florence et al., 2011): 42% relative reduction in violence-related hospital admissions.", [s_card]),
    ],
    links=[L('soc:threshold-models-of-collective-behaviour', 'bridges', "مدل آستانه"),
           L('psy:violence-cycle', 'see-also', "سرایت میان نسل‌ها"),
           L('psy:violent-apartheid', 'see-also', "وقتی دولت خودش ناقل است"),
           L('psy:intergroup-contact', 'see-also', "یکی از راه‌های بریدن زنجیره")],
    people=[p_slut],
    explain=t("چرا در «جامعه‌های زیاد» و به شکل همه‌گیر؟ چون خشونت یک رفتار وابسته به دیگران است. اگر در محله‌ای همه مسلح‌اند، مسلح‌نبودن خطرناک است. اگر در خانواده‌ای همه بچه را می‌زنند، نزدن یعنی «بچه را لوس کردن». اگر در ارتشی همه شلیک می‌کنند، شلیک‌نکردن خیانت است. هر آدم جداگانه شاید نخواهد، ولی هیچ‌کس نمی‌خواهد اولین کسی باشد که نمی‌کند.\n\nاین یعنی خشونتِ همه‌گیر با عوض‌کردن تک‌تک آدم‌ها از میان نمی‌رود؛ با عوض‌کردن آنچه هر کس دربارهٔ دیگران گمان می‌کند از میان می‌رود. و برای همین هم گاهی ناگهان فرو می‌ریزد.",
              "Violence is interdependent behaviour: nobody wants to be the first not to do it."))

add('violent-apartheid',
    title=t("آپارتاید خشونت‌آمیز چطور ساخته می‌شود؟", "How violent apartheid is built"),
    aliases=["آپارتاید", "آپارتاید جنسیتی", "پیوستار ویرانگری"],
    summary=t("آپارتاید با کشتار شروع نمی‌شود؛ با دسته‌بندی شروع می‌شود. پله‌پله ساخته می‌شود: نام، قانون، جداسازی، محروم‌سازی، و زور برای نگه‌داشتن همهٔ این‌ها. هر پله پلهٔ بعد را عادی می‌کند.",
              "Apartheid begins with classification and is built step by step; each step normalises the next."),
    points=[
     P("اساسنامهٔ رم جنایت آپارتاید را کارهای غیرانسانی‌ای می‌داند که «در چارچوب یک رژیم نهادینهٔ ستم و سلطهٔ نظام‌مند یک گروه نژادی بر گروه یا گروه‌های نژادی دیگر و به قصد نگه‌داشتن آن رژیم» انجام شود. پس سه جزء دارد: رژیم نهادینه، سلطهٔ نظام‌مند، و قصد ماندگاری.",
       "Rome Statute 7(2)(h): inhumane acts in an institutionalised regime of systematic oppression and domination by one racial group, intended to maintain that regime.", [s_rome, s_apconv]),
     P("در آفریقای جنوبی پس از ۱۹۴۸ این پله‌ها با قانون چیده شد: ثبت نژاد هر فرد، ممنوعیت ازدواج میان نژادها، تعیین محل زندگی هر گروه، آموزش جدا و فروتر، و دفترچهٔ عبور. در ۲۱ مارس ۱۹۶۰ پلیس در شارپویل به روی معترضان به قانون عبور آتش گشود؛ آمار پلیس ۶۹ کشته بود و پژوهش‌های تازه‌تر شمار را بیشتر می‌دانند.",
       "South Africa after 1948: classification, marriage ban, residential zoning, separate schooling, passes; Sharpeville, 21 March 1960 (69 dead by the police record; later research suggests more).", [s_sharp], ['contested']),
     P("استاب این را «پیوستار ویرانگری» می‌نامد: آسیب‌زدن به یک گروه، آسیب‌زن و تماشاگر را عوض می‌کند. قربانی کم‌ارزش‌تر دیده می‌شود، کارِ بعدی آسان‌تر، و سکوت تماشاگران به‌عنوان رضایت خوانده می‌شود.",
       "Staub: the continuum of destruction — harming changes perpetrators and bystanders; passivity is read as assent.", [s_staub]),
     P("استانتون ده مرحله برشمرده است: دسته‌بندی، نمادگذاری، تبعیض، انسانیت‌زدایی، سازمان‌دهی، دوقطبی‌سازی، آماده‌سازی، آزار، نابودی، انکار. این یک چارچوب آموزشی است؛ مرحله‌ها همیشه به ترتیب نمی‌آیند و توان پیش‌بینی آن آزموده نشده است.",
       "Stanton's ten stages are a teaching framework, not a validated predictive model.", [s_stanton], ['contested', 'unreplicated']),
     P("تعریف حقوقی کنونی فقط «نژاد» را می‌گوید. کارزاری به رهبری زنان افغانستان می‌خواهد «آپارتاید جنسیتی» در پیمان تازهٔ جنایت علیه بشریت بیاید؛ تا اوت ۲۰۲۶ چهارده کشور علناً پشتیبانی کرده‌اند و مذاکرهٔ رسمی متن از ژانویهٔ ۲۰۲۸ آغاز می‌شود.",
       "Campaign to codify gender apartheid in the crimes against humanity treaty: 14 states in support by August 2026; negotiations from January 2028.", [s_hrw26]),
    ],
    links=[L('psy:dehumanization', 'part-of', "پلهٔ چهارم"),
           L('psy:moral-disengagement', 'explains', "همان هشت کلید، در مقیاس یک کشور"),
           L('psy:violence-epidemic', 'see-also', "وقتی دولت ناقل است"),
           L('psy:collective-narcissism', 'see-also', "گروهی که باید برتر دیده شود"),
           L('phil:arendt-obedience-is-support', 'bridges', "بدون همراهی نمی‌ماند"),
           L('soc:preference-falsification', 'bridges', "چرا ناگهان فرو می‌ریزد")],
    people=[p_staub],
    explain=t("آپارتاید سه چیز می‌خواهد که هیچ‌کدام به‌تنهایی خشونتِ پیدا نیست. اول یک خط: چه کسی «ما»ست و چه کسی «آن‌ها»، و راهی برای اینکه هر آدم را در یک نگاه در یکی از دو دسته بگذارند (رنگ پوست، کارت، پوشش). دوم قانون: خط باید از سلیقه به مقررات تبدیل شود تا کارمند معمولی بتواند بی‌کینه اجرایش کند. سوم زور: چون گروه زیردست سر جایش نمی‌ماند، نظام برای ماندن ناچار است هر روز کمی خشونت خرج کند، و هر چند وقت یک بار خیلی زیاد.\n\nخشونتِ پیدا (گلوله، زندان) نوک این بناست. بدنه‌اش اداری است: فرم، مجوز، صف جدا، مدرسهٔ جدا. برای همین است که بیشترِ کسانی که آن را سر پا نگه می‌دارند هیچ‌وقت دست روی کسی بلند نمی‌کنند.",
              "Apartheid needs a line, a law and force; visible violence is only the tip of an administrative structure."),
    confusions=[t("هر تبعیضی آپارتاید نیست. واژهٔ حقوقی برای نظامی است که نهادینه، نظام‌مند و به قصد ماندگاری باشد.", "Not all discrimination is apartheid.")])

add('violence-prevention',
    title=t("چه چیزی خشونت را کم می‌کند؟", "What reduces violence"),
    summary=t("خشونت پیش‌گیری‌پذیر است؛ این جمله شعار نیست، نتیجهٔ ارزیابی‌هاست. آنچه کار کرده معمولاً مجازات سخت‌تر نبوده، بلکه دیدن الگو، بریدن زنجیره و عوض‌کردن هنجار بوده است.",
              "Violence is preventable; what has worked is seeing patterns, interrupting chains and shifting norms."),
    points=[
     P("دادهٔ بی‌نام بیمارستان (کجا، کی، با چه) وقتی به دست شهر برسد، بستری به علت خشونت را کم می‌کند: ۴۲ درصد در کاردیف نسبت به شهرهای مشابه.",
       "Cardiff Model: anonymised emergency-department data shared with police and city reduced admissions by 42%.", [s_card]),
     P("پرسیدنِ رفتار به‌جای برچسب، خشونتی را که دیده نمی‌شد دیدنی می‌کند؛ بدون آن، برنامه‌ها برای مشکلی طراحی می‌شوند که کوچک‌تر از واقعیت شمرده شده است.",
       "Behavioural questions reveal otherwise hidden violence.", [s_wm]),
     P("بیشتر کودکان آزاردیده چرخه را ادامه نمی‌دهند؛ پس پرسش درست این است که چه چیزی به آن اکثریت کمک کرده است.",
       "Most abused children do not continue the cycle.", [s_widom]),
     P("در سطح سیاسی، کارزارهای بی‌خشونت در سدهٔ بیستم دو برابر کارزارهای مسلحانه به نتیجه رسیدند، هرچند این برتری در سال‌های اخیر کم شده است.",
       "Nonviolent campaigns succeeded about twice as often, with a recent decline.", [s_chen, s_chen20]),
    ],
    links=[L('psy:violence-epidemic', 'applies-to', "بریدن زنجیرهٔ سرایت"),
           L('psy:breaking-cycle', 'see-also', "شکستن چرخه در خانواده"),
           L('psy:intergroup-contact', 'see-also', "تماس میان گروه‌ها"),
           L('psy:boundaries', 'see-also', "مرز گذاشتن"),
           L('psy:recovery', 'see-also', "بیرون آمدن")])

# ---------------- نوشتن (افزایشی) ----------------
os.makedirs(f'{R}/data/psy/concepts', exist_ok=True)
for c in C:
    json.dump(c, open(f"{R}/data/psy/concepts/{c['id'].split(':')[1]}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S.people, open(f'{R}/core/people.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(S.sources, open(f'{R}/core/sources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('violence concepts', len(C), 'sources', len({s for c in C for s in c['sources']}))
