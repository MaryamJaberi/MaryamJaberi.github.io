import { ProjectCardContent, AtlasView, TimelineEpoch, IranStateHighlight } from '../types';

export const GITHUB_REPO_URL = 'https://github.com/MaryamJaberi/chrono-atlas';
export const LIVE_DEMO_URL = 'https://ais-pre-dteccvvwazpazpci3vjfiu-959375435927.europe-west2.run.app';
export const GITHUB_PAGES_URL = 'https://maryamjaberi.github.io/chrono-atlas/';
export const CREATE_GITHUB_REPO_URL = 'https://github.com/new?name=chrono-atlas&description=Interactive+atlas+of+Earth+through+time';
export const PORTFOLIO_REPO_URL = 'https://github.com/MaryamJaberi/MaryamJaberi.github.io';

export const PROJECT_CONTENTS: Record<'en' | 'fa' | 'nl', ProjectCardContent> = {
  en: {
    lang: 'en',
    dir: 'ltr',
    title: 'Chrono Atlas',
    tagline: 'An interactive atlas of Earth through time, from the Big Bang to 1,000 years ahead.',
    summary: 'Drag one timeline and the whole planet responds: continents drift, ice sheets grow and retreat, life appears and goes extinct, civilizations rise and fall. Built as a single self-contained HTML file with no build step and no external data calls, so it loads instantly and works offline.',
    highlights: [
      'Five views: Earth, Life, Civilizations, Iran, and Sources',
      'Logarithmic deep-time scale plus a linear history scale, because one scale cannot serve both 13.8 billion years and the last 6,000',
      '60 major groups of life with first appearances, extinctions, and the Big Five mass extinctions',
      '78 civilizations across every inhabited continent, each with government, economy, language, beliefs, achievements, decline, legacy, and contemporaries',
      'Iran pilot: 28 states from Elam to today with approximate borders, 98 dated events, and panels for inventions, language, religion, crops, and wildlife',
      'Catalog of 83 scholarly data sources, with licence and access notes',
    ],
    craft: 'Product and research choices: every claim carries a confidence level; future layers are labelled as scenarios, not predictions; data-coverage gaps are shown on screen so empty regions read as missing research rather than an empty past.',
    meta: 'Role: concept, product design, research, and build · Tech: vanilla HTML, CSS, SVG, JavaScript',
    liveDemoUrl: LIVE_DEMO_URL,
    sourceCodeUrl: GITHUB_REPO_URL,
    portfolioRepoUrl: PORTFOLIO_REPO_URL,
  },
  fa: {
    lang: 'fa',
    dir: 'rtl',
    title: 'کرونو اطلس',
    tagline: 'اطلس تعاملی زمین در گذر زمان، از مهبانگ تا هزار سال آینده.',
    summary: 'با کشیدن یک نوار زمان، کل سیاره واکنش نشان می‌دهد: قاره‌ها جابه‌جا می‌شوند، یخ‌ها پیش و پس می‌روند، گونه‌ها پدید می‌آیند و منقرض می‌شوند و تمدن‌ها شکل می‌گیرند و از میان می‌روند. همه‌چیز در یک فایل HTML مستقل ساخته شده، بدون مرحلهٔ بیلد و بدون فراخوانی داده از بیرون؛ بنابراین سریع بالا می‌آید و آفلاین هم کار می‌کند.',
    highlights: [
      'پنج نما: زمین، حیات، تمدن‌ها، ایران و منابع',
      'دو مقیاس زمان: لگاریتمی برای زمان عمیق و خطی برای تاریخ، چون یک مقیاس نمی‌تواند هم ۱۳٫۸ میلیارد سال و هم شش هزار سال اخیر را نشان دهد',
      '۶۰ گروه اصلی حیات با زمان پیدایش، انقراض و پنج انقراض بزرگ',
      '۷۸ تمدن از همهٔ قاره‌ها، هرکدام با حکومت، اقتصاد، زبان، باورها، دستاوردها، افول، میراث و هم‌عصرها',
      'نمای ایران: ۲۸ حکومت از عیلام تا امروز با مرزهای تقریبی، ۹۸ رویداد تاریخ‌دار و بخش‌هایی برای اختراع‌ها، زبان، دین، کشاورزی و حیات وحش',
      'کاتالوگ ۸۳ پایگاه دادهٔ علمی، همراه با وضعیت مجوز و دسترسی',
    ],
    craft: 'تصمیم‌های محصولی و پژوهشی: هر ادعا میزان قطعیت دارد؛ لایه‌های آینده سناریو هستند نه پیش‌بینی؛ و کمبود پوشش داده روی صفحه نشان داده می‌شود تا نبودِ داده به معنی نبودِ انسان خوانده نشود.',
    meta: 'نقش: ایده، طراحی محصول، پژوهش و ساخت · فناوری: HTML، CSS، SVG و جاوااسکریپت خالص',
    liveDemoUrl: LIVE_DEMO_URL,
    sourceCodeUrl: GITHUB_REPO_URL,
    portfolioRepoUrl: PORTFOLIO_REPO_URL,
  },
  nl: {
    lang: 'nl',
    dir: 'ltr',
    title: 'Chrono Atlas',
    tagline: 'Een interactieve atlas van de aarde door de tijd, van de oerknal tot 1.000 jaar vooruit.',
    summary: 'Verschuif één tijdlijn en de hele planeet verandert mee: continenten drijven uiteen, ijskappen groeien en krimpen, soorten ontstaan en sterven uit, beschavingen komen op en verdwijnen. Gebouwd als één zelfstandig HTML-bestand, zonder buildstap en zonder externe dataverzoeken, dus het laadt direct en werkt offline.',
    highlights: [
      'Vijf weergaven: Aarde, Leven, Beschavingen, Iran en Bronnen',
      'Een logaritmische schaal voor diepe tijd naast een lineaire schaal voor geschiedenis',
      '60 grote groepen van het leven, met eerste verschijning, uitsterven en de vijf grote massa-uitstervingen',
      '78 beschavingen van alle bewoonde continenten, met bestuur, economie, taal, geloof, prestaties, verval, erfenis en tijdgenoten',
      'Iran als pilot: 28 staten van Elam tot nu met benaderende grenzen, 98 gedateerde gebeurtenissen en panelen voor uitvindingen, taal, religie, gewassen en dieren',
      'Catalogus van 83 wetenschappelijke databronnen, met licentie- en toegangsinformatie',
    ],
    craft: 'Product- en onderzoekskeuzes: elke bewering heeft een betrouwbaarheidsniveau, toekomstlagen zijn scenario\'s en geen voorspellingen, en hiaten in de data worden zichtbaar gemaakt, zodat een lege kaart ontbrekend onderzoek betekent en geen leeg verleden.',
    meta: 'Rol: concept, productontwerp, onderzoek en bouw · Techniek: pure HTML, CSS, SVG en JavaScript',
    liveDemoUrl: LIVE_DEMO_URL,
    sourceCodeUrl: GITHUB_REPO_URL,
    portfolioRepoUrl: PORTFOLIO_REPO_URL,
  },
};

export const ATLAS_VIEWS: AtlasView[] = [
  {
    id: 'earth',
    nameEn: 'Earth & Geology',
    nameFa: 'زمین و زمین‌شناسی',
    nameNl: 'Aarde & Geologie',
    icon: 'Globe2',
    headlineEn: 'Continental drift, tectonic plates & glaciation cycles',
    headlineFa: 'حرکت قاره‌ها، صفحات زمین‌ساختی و چرخه‌های یخچالی',
    metrics: '13.8B yr → Present',
    descriptionEn: 'Simulates continental movements from Pangaea and Rodinia through historical epochs with atmospheric CO2 indicators and glaciations.',
    descriptionFa: 'شبیه‌سازی رانش قاره‌ها از ابرقاره‌های رودینیا و پانگه‌آ تا دوران معاصر همراه با شاخص‌های اقلیمی و پیشروی یخ‌ها.',
    tags: ['Paleogeography', 'Plate Tectonics', 'Ice Ages', 'Continental Drift'],
  },
  {
    id: 'life',
    nameEn: 'Tree of Life & Extinctions',
    nameFa: 'درخت حیات و انقراض‌ها',
    nameNl: 'Stamboom van het Leven',
    icon: 'Dna',
    headlineEn: '60 major clades with the Big 5 Mass Extinctions',
    headlineFa: '۶۰ راسته و شاخهٔ اصلی حیات همراه با ۵ انقراض بزرگ',
    metrics: '60 Groups · 5 Die-offs',
    descriptionEn: 'Tracks early multicellular organisms, Cambrian explosion, dinosaurs, hominids, and extinction boundary horizons.',
    descriptionFa: 'ردیابی موجودات پرسلولی، انفجار کامبرین، خزندگان کهن، هومونیدها و خطوط افق انقراض‌های پنج‌گانه.',
    tags: ['Paleobiology', 'Phylogeny', 'Mass Extinctions', 'Speciation'],
  },
  {
    id: 'civilizations',
    nameEn: '78 Global Civilizations',
    nameFa: '۷۸ تمدن سراسر جهان',
    nameNl: '78 Wereldbeschavingen',
    icon: 'Landmark',
    headlineEn: 'Deep cultural, economic, and sociopolitical taxonomy',
    headlineFa: 'طبقه‌بندی ژرف فرهنگی، اقتصادی و سیاسی',
    metrics: '78 Polities across 6 Continents',
    descriptionEn: 'Each civilization features 8 structured facets: governance, economy, language, belief systems, engineering feats, causes of decline, enduring legacy, and contemporaries.',
    descriptionFa: 'هر تمدن دارای ۸ زاویهٔ تحلیلی است: حکومت، اقتصاد، خط و زبان، نظام باورها، دستاوردها، دلایل فروپاشی، میراث ماندگار و هم‌عصران.',
    tags: ['Governance', 'Trade Networks', 'Linguistics', 'Material Culture'],
  },
  {
    id: 'iran',
    nameEn: 'Iran Pilot Deep-Dive',
    nameFa: 'بخش ویژهٔ فلات ایران',
    nameNl: 'Iran Pilotverdieping',
    icon: 'Crown',
    headlineEn: '28 polities from Elam (3200 BCE) to modern era with 98 dated events',
    headlineFa: '۲۸ حکومت از تمدن عیلام تا عصر حاضر همراه با ۹۸ رویداد مستند',
    metrics: '28 Dynasties · 98 Events',
    descriptionEn: 'Detailed spatial borders, invention timelines (qanats, post, astronomy), linguistic evolution from Old Persian & Avestan, and endemic ecosystems.',
    descriptionFa: 'نقشه‌های مرزی تخمینی، گاه‌شمار ابداعات کهن (قنات، چاپار، نجوم)، سیر تطور زبان و خط، و اکوسیستم‌های طبیعی بومی فلات.',
    tags: ['Elam', 'Achaemenid', 'Sasanian', 'Safavid', 'Material Heritage'],
  },
  {
    id: 'sources',
    nameEn: 'Scholarly Sources Catalog',
    nameFa: 'کاتالوگ مراجع و داده‌های علمی',
    nameNl: 'Wetenschappelijke Bronnen',
    icon: 'Library',
    headlineEn: '83 peer-reviewed & academic data repositories',
    headlineFa: '۸۳ منبع علمی و پایگاه داده با مجوزهای دسترسی باز',
    metrics: '83 Databases Cataloged',
    descriptionEn: 'Documenting datasets such as EarthByte paleomap reconstructions, Paleobiology Database, HYDE land use, Pleiades ancient places, and open licenses.',
    descriptionFa: 'مستندسازی پایگاه‌های داده معتبر نظیر بازسازی‌های پالئوژئوگرافی EarthByte، پایگاه دیرینه‌شناسی PBDB و داده‌های باستانی Pleiades.',
    tags: ['Open Data', 'Paleobiology DB', 'HYDE', 'Peer-Reviewed'],
  },
];

export const TIMELINE_EPOCHS: TimelineEpoch[] = [
  {
    labelEn: 'Big Bang',
    labelFa: 'مهبانگ (انفجار بزرگ)',
    timeDisplay: '13.8 Ga',
    yearsAgo: 13800000000,
    scaleType: 'log',
    category: 'cosmos',
    descriptionEn: 'Origin of spacetime, matter, and cosmic background radiation.',
    descriptionFa: 'پیدایش فضا-زمان، ماده و تابش زمینه کیهانی.',
  },
  {
    labelEn: 'Formation of Earth',
    labelFa: 'پیدایش کرهٔ زمین',
    timeDisplay: '4.54 Ga',
    yearsAgo: 4540000000,
    scaleType: 'log',
    category: 'geology',
    descriptionEn: 'Accretion from the solar nebula, differentiation of mantle and core.',
    descriptionFa: 'تجمع غبارهای سحابی خورشیدی و تشکیل هسته و گوشتهٔ زمین.',
  },
  {
    labelEn: 'Cambrian Explosion',
    labelFa: 'انفجار زیستی کامبرین',
    timeDisplay: '541 Ma',
    yearsAgo: 541000000,
    scaleType: 'log',
    category: 'biology',
    descriptionEn: 'Rapid diversification of major animal phyla and hard skeletal parts.',
    descriptionFa: 'گسترش شگفت‌انگیز شاخه‌های اصلی جانداران و اسکلت‌های سخت.',
  },
  {
    labelEn: 'Permian-Triassic Extinction',
    labelFa: 'بزرگ‌ترین انقراض حیات (پرمین)',
    timeDisplay: '252 Ma',
    yearsAgo: 252000000,
    scaleType: 'log',
    category: 'biology',
    descriptionEn: 'The Great Dying: ~96% of marine species and 70% of terrestrial vertebrates extinct.',
    descriptionFa: 'مرگ بزرگ: انقراض حدود ۹۶٪ گونه‌های دریایی و ۷۰٪ مهره‌داران خشکی.',
  },
  {
    labelEn: 'K-Pg Boundary (Asteroid)',
    labelFa: 'برخورد شهاب‌سنگ و انقراض دایناسورها',
    timeDisplay: '66 Ma',
    yearsAgo: 66000000,
    scaleType: 'log',
    category: 'biology',
    descriptionEn: 'Chicxulub impact, collapse of non-avian dinosaurs, rise of mammals.',
    descriptionFa: 'اصابت شهاب‌سنگ چیکشلوب، پایان عصر دایناسورها و شکوفایی پستانداران.',
  },
  {
    labelEn: 'Anatomically Modern Humans',
    labelFa: 'پیدایش انسان خردمند (هومو ساپینس)',
    timeDisplay: '300 ka',
    yearsAgo: 300000,
    scaleType: 'log',
    category: 'biology',
    descriptionEn: 'Homo sapiens emergence in Africa, symbolic thought, tools.',
    descriptionFa: 'ظهور هومو ساپینس در آفریقا، تفکر نمادین و ابزارسازی پیشرفته.',
  },
  {
    labelEn: 'Elam & Sumer (First Cities)',
    labelFa: 'عیلام و سومر (نخستین شهرها و خط)',
    timeDisplay: '3200 BCE',
    yearsAgo: 5200,
    scaleType: 'linear',
    category: 'civilization',
    descriptionEn: 'Proto-Elamite and cuneiform writing, urban centralization, monumental ziggurats.',
    descriptionFa: 'آغاز پیدایش خط نیاعیلامی و میخی، شهرنشینی و زیگورات‌های شوش و چغازنبیل.',
  },
  {
    labelEn: 'Achaemenid Empire & Global Roads',
    labelFa: 'امپراتوری هخامنشی و شاهراه شاهی',
    timeDisplay: '550 BCE',
    yearsAgo: 2570,
    scaleType: 'linear',
    category: 'civilization',
    descriptionEn: 'Cyrus Cylinder human rights declaration, Royal Road, Persepolis administration.',
    descriptionFa: 'منشور حقوق بشر کوروش، احداث چاپارخانه و شاهراه شاهی، معماری تخت جمشید.',
  },
  {
    labelEn: 'Scientific & Digital Revolutions',
    labelFa: 'عصر علم و انقلاب دیجیتال',
    timeDisplay: 'Present',
    yearsAgo: 0,
    scaleType: 'linear',
    category: 'civilization',
    descriptionEn: 'Global telecommunications, space exploration, Earth system observations.',
    descriptionFa: 'ارتباطات جهانی آنی، کاوش فضا، هوش مصنوعی و پایش ماهواره‌ای زمین.',
  },
  {
    labelEn: 'Future Earth Scenarios',
    labelFa: 'سناریوهای آیندهٔ زمین',
    timeDisplay: '+1,000 Years',
    yearsAgo: -1000,
    scaleType: 'linear',
    category: 'future',
    descriptionEn: 'Climate mitigation pathways, bio-regeneration, planetary stewardship models.',
    descriptionFa: 'مدل‌های زیست‌بومی، سناریوهای تغییر اقلیم و الگوهای تداوم تمدن.',
  },
];

export const IRAN_STATES_SAMPLE: IranStateHighlight[] = [
  {
    nameEn: 'Proto-Elamite & Elamite Kingdoms',
    nameFa: 'تمدن و پادشاهی‌های عیلام',
    period: '3200 – 539 BCE',
    capital: 'Susa / Anshan',
    notableAchievement: 'Early linear script, bronze metallurgy, and Chogha Zanbil UNESCO ziggurat.',
  },
  {
    nameEn: 'Achaemenid Empire',
    nameFa: 'شاهنشاهی هخامنشی',
    period: '550 – 330 BCE',
    capital: 'Pasargadae, Persepolis, Susa',
    notableAchievement: 'First global satrapy administrative network, Royal Post System (Chapar Khaneh), Cyrus Charter.',
  },
  {
    nameEn: 'Parthian Empire (Arsacid)',
    nameFa: 'شاهنشاهی اشکانی',
    period: '247 BCE – 224 CE',
    capital: 'Hecatompylos, Ctesiphon',
    notableAchievement: 'Silk Road backbone connection between Han China and Rome, mobile cavalry tactics.',
  },
  {
    nameEn: 'Sasanian Empire',
    nameFa: 'شاهنشاهی ساسانی',
    period: '224 – 651 CE',
    capital: 'Ctesiphon, Istakhr',
    notableAchievement: 'Gundeshapur Academy of Medicine & Philosophy, master vaulted iwan architecture, rock reliefs.',
  },
  {
    nameEn: 'Safavid Empire',
    nameFa: 'دولت صفوی',
    period: '1501 – 1736 CE',
    capital: 'Tabriz, Qazvin, Isfahan',
    notableAchievement: 'Isfahan urban masterpiece (Naqsh-e Jahan), world diplomacy, renaissance of carpet & ceramic art.',
  },
];

export const RAW_PORTFOLIO_HTML = `<!-- ============ ENGLISH ============ -->
<article class="project-card" data-lang="en">
  <h3 class="project-title">Chrono Atlas</h3>
  <p class="project-tagline">An interactive atlas of Earth through time, from the Big Bang to 1,000 years ahead.</p>

  <p class="project-summary">
    Drag one timeline and the whole planet responds: continents drift, ice sheets grow and retreat,
    life appears and goes extinct, civilizations rise and fall. Built as a single self-contained
    HTML file with no build step and no external data calls, so it loads instantly and works offline.
  </p>

  <ul class="project-highlights">
    <li>Five views: Earth, Life, Civilizations, Iran, and Sources</li>
    <li>Logarithmic deep-time scale plus a linear history scale, because one scale cannot serve both 13.8 billion years and the last 6,000</li>
    <li>60 major groups of life with first appearances, extinctions, and the Big Five mass extinctions</li>
    <li>78 civilizations across every inhabited continent, each with government, economy, language, beliefs, achievements, decline, legacy, and contemporaries</li>
    <li>Iran pilot: 28 states from Elam to today with approximate borders, 98 dated events, and panels for inventions, language, religion, crops, and wildlife</li>
    <li>Catalog of 83 scholarly data sources, with licence and access notes</li>
  </ul>

  <p class="project-craft">
    <strong>Product and research choices:</strong> every claim carries a confidence level; future layers are
    labelled as scenarios, not predictions; data-coverage gaps are shown on screen so empty regions read as
    missing research rather than an empty past.
  </p>

  <p class="project-meta">Role: concept, product design, research, and build · Tech: vanilla HTML, CSS, SVG, JavaScript</p>

  <p class="project-links">
    <a class="btn" href="https://maryamjaberi.github.io/chrono-atlas/">Live demo</a>
    <a class="btn" href="https://github.com/MaryamJaberi/chrono-atlas">Source code</a>
  </p>
</article>

<!-- ============ فارسی (RTL) ============ -->
<article class="project-card" data-lang="fa" dir="rtl" lang="fa">
  <h3 class="project-title">کرونو اطلس</h3>
  <p class="project-tagline">اطلس تعاملی زمین در گذر زمان، از مهبانگ تا هزار سال آینده.</p>

  <p class="project-summary">
    با کشیدن یک نوار زمان، کل سیاره واکنش نشان می‌دهد: قاره‌ها جابه‌جا می‌شوند، یخ‌ها پیش و پس می‌روند،
    گونه‌ها پدید می‌آیند و منقرض می‌شوند و تمدن‌ها شکل می‌گیرند و از میان می‌روند. همه‌چیز در یک فایل
    HTML مستقل ساخته شده، بدون مرحلهٔ بیلد و بدون فراخوانی داده از بیرون؛ بنابراین سریع بالا می‌آید و آفلاین هم کار می‌کند.
  </p>

  <ul class="project-highlights">
    <li>پنج نما: زمین، حیات، تمدن‌ها، ایران و منابع</li>
    <li>دو مقیاس زمان: لگاریتمی برای زمان عمیق و خطی برای تاریخ، چون یک مقیاس نمی‌تواند هم ۱۳٫۸ میلیارد سال و هم شش هزار سال اخیر را نشان دهد</li>
    <li>۶۰ گروه اصلی حیات با زمان پیدایش، انقراض و پنج انقراض بزرگ</li>
    <li>۷۸ تمدن از همهٔ قاره‌ها، هرکدام با حکومت، اقتصاد، زبان، باورها، دستاوردها، افول، میراث و هم‌عصرها</li>
    <li>نمای ایران: ۲۸ حکومت از عیلام تا امروز با مرزهای تقریبی، ۹۸ رویداد تاریخ‌دار و بخش‌هایی برای اختراع‌ها، زبان، دین، کشاورزی و حیات وحش</li>
    <li>کاتالوگ ۸۳ پایگاه دادهٔ علمی، همراه با وضعیت مجوز و دسترسی</li>
  </ul>

  <p class="project-craft">
    <strong>تصمیم‌های محصولی و پژوهشی:</strong> هر ادعا میزان قطعیت دارد؛ لایه‌های آینده سناریو هستند نه پیش‌بینی؛
    و کمبود پوشش داده روی صفحه نشان داده می‌شود تا نبودِ داده به معنی نبودِ انسان خوانده نشود.
  </p>

  <p class="project-meta">نقش: ایده، طراحی محصول، پژوهش و ساخت · فناوری: HTML، CSS، SVG و جاوااسکریپت خالص</p>

  <p class="project-links">
    <a class="btn" href="https://maryamjaberi.github.io/chrono-atlas/">نسخهٔ زنده</a>
    <a class="btn" href="https://github.com/MaryamJaberi/chrono-atlas">کد منبع</a>
  </p>
</article>

<!-- ============ NEDERLANDS ============ -->
<article class="project-card" data-lang="nl" lang="nl">
  <h3 class="project-title">Chrono Atlas</h3>
  <p class="project-tagline">Een interactieve atlas van de aarde door de tijd, van de oerknal tot 1.000 jaar vooruit.</p>

  <p class="project-summary">
    Verschuif één tijdlijn en de hele planeet verandert mee: continenten drijven uiteen, ijskappen groeien
    en krimpen, soorten ontstaan en sterven uit, beschavingen komen op en verdwijnen. Gebouwd als één
    zelfstandig HTML-bestand, zonder buildstap en zonder externe dataverzoeken, dus het laadt direct en werkt offline.
  </p>

  <ul class="project-highlights">
    <li>Vijf weergaven: Aarde, Leven, Beschavingen, Iran en Bronnen</li>
    <li>Een logaritmische schaal voor diepe tijd naast een lineaire schaal voor geschiedenis</li>
    <li>60 grote groepen van het leven, met eerste verschijning, uitsterven en de vijf grote massa-uitstervingen</li>
    <li>78 beschavingen van alle bewoonde continenten, met bestuur, economie, taal, geloof, prestaties, verval, erfenis en tijdgenoten</li>
    <li>Iran als pilot: 28 staten van Elam tot nu met benaderende grenzen, 98 gedateerde gebeurtenissen en panelen voor uitvindingen, taal, religie, gewassen en dieren</li>
    <li>Catalogus van 83 wetenschappelijke databronnen, met licentie- en toegangsinformatie</li>
  </ul>

  <p class="project-craft">
    <strong>Product- en onderzoekskeuzes:</strong> elke bewering heeft een betrouwbaarheidsniveau, toekomstlagen
    zijn scenario's en geen voorspellingen, en hiaten in de data worden zichtbaar gemaakt, zodat een lege kaart
    ontbrekend onderzoek betekent en geen leeg verleden.
  </p>

  <p class="project-meta">Rol: concept, productontwerp, onderzoek en bouw · Techniek: pure HTML, CSS, SVG en JavaScript</p>

  <p class="project-links">
    <a class="btn" href="https://maryamjaberi.github.io/chrono-atlas/">Live demo</a>
    <a class="btn" href="https://github.com/MaryamJaberi/chrono-atlas">Broncode</a>
  </p>
</article>`;

export const ENHANCED_CSS_SNIPPET = `/* High-Craft styling for MaryamJaberi.github.io project cards */
.project-card {
  position: relative;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.project-card:hover {
  border-color: rgba(217, 119, 6, 0.35);
  box-shadow: 0 12px 36px -4px rgba(217, 119, 6, 0.12);
  transform: translateY(-2px);
}

.project-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.6), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.project-card:hover::before {
  opacity: 1;
}

.project-title {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #f8fafc;
  margin-bottom: 8px;
}

.project-tagline {
  font-size: 1.1rem;
  color: #fbbf24;
  font-weight: 500;
  margin-bottom: 16px;
  line-height: 1.5;
}

.project-summary {
  font-size: 1rem;
  line-height: 1.7;
  color: #cbd5e1;
  margin-bottom: 24px;
}

.project-highlights {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
  display: grid;
  gap: 10px;
}

.project-highlights li {
  position: relative;
  padding-left: 24px;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #94a3b8;
}

[dir="rtl"] .project-highlights li {
  padding-left: 0;
  padding-right: 24px;
}

.project-highlights li::before {
  content: '✦';
  position: absolute;
  left: 0;
  color: #f59e0b;
  font-size: 0.75rem;
  top: 4px;
}

[dir="rtl"] .project-highlights li::before {
  left: auto;
  right: 0;
}

.project-craft {
  background: rgba(245, 158, 11, 0.05);
  border-left: 3px solid #f59e0b;
  padding: 14px 18px;
  border-radius: 6px;
  font-size: 0.92rem;
  line-height: 1.6;
  color: #e2e8f0;
  margin-bottom: 20px;
}

[dir="rtl"] .project-craft {
  border-left: none;
  border-right: 3px solid #f59e0b;
}

.project-meta {
  font-size: 0.85rem;
  color: #64748b;
  font-family: monospace;
  margin-bottom: 24px;
  border-top: 1px dashed rgba(255, 255, 255, 0.1);
  padding-top: 16px;
}

.project-links {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.project-links .btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 22px;
  border-radius: 9999px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.project-links .btn:first-child {
  background: #f59e0b;
  color: #0f172a;
}
.project-links .btn:first-child:hover {
  background: #fbbf24;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.project-links .btn:last-child {
  background: rgba(255, 255, 255, 0.08);
  color: #f1f5f9;
  border: 1px solid rgba(255, 255, 255, 0.15);
}
.project-links .btn:last-child:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}`;
