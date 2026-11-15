// Comprehensive dataset for Chrono Atlas
export interface PaleogeographyState {
  epochId: string;
  yearDisplay: string;
  yearsAgo: number;
  periodNameEn: string;
  periodNameFa: string;
  co2Ppm: number;
  tempAnomalyC: number;
  seaLevelM: number;
  iceCoverPct: number;
  supercontinent: string;
  descriptionEn: string;
  descriptionFa: string;
  majorTectonicEventEn: string;
  majorTectonicEventFa: string;
  svgContinents: {
    name: string;
    path: string;
    fill: string;
  }[];
}

export interface CladeLifeGroup {
  id: string;
  nameEn: string;
  nameFa: string;
  cladeCategory: 'microbe' | 'invertebrate' | 'plant' | 'fish' | 'reptile' | 'dinosaur' | 'mammal' | 'hominid';
  appearedYearsAgo: number; // e.g. 530000000
  extinctYearsAgo?: number; // undefined if extant
  appearedLabelEn: string;
  appearedLabelFa: string;
  extinctLabelEn?: string;
  extinctLabelFa?: string;
  iconType: string;
  descriptionEn: string;
  descriptionFa: string;
  isBigFiveVictim?: boolean;
}

export interface MassExtinctionEvent {
  id: string;
  nameEn: string;
  nameFa: string;
  yearsAgo: number;
  timeLabel: string;
  killCurvePct: number;
  victimsEn: string;
  victimsFa: string;
  triggersEn: string;
  triggersFa: string;
  recoveryYearsEn: string;
  recoveryYearsFa: string;
}

export interface CivilizationRecord {
  id: string;
  nameEn: string;
  nameFa: string;
  region: 'Middle East' | 'Asia' | 'Europe' | 'Africa' | 'Americas' | 'Oceania';
  regionFa: string;
  startBce: number; // positive = BCE, negative = CE
  endBce: number;
  periodLabel: string;
  capitalEn: string;
  capitalFa: string;
  // 8 Structured Facets
  governmentEn: string;
  governmentFa: string;
  economyEn: string;
  economyFa: string;
  languageEn: string;
  languageFa: string;
  beliefsEn: string;
  beliefsFa: string;
  engineeringEn: string;
  engineeringFa: string;
  declineEn: string;
  declineFa: string;
  legacyEn: string;
  legacyFa: string;
  contemporariesEn: string[];
  contemporariesFa: string[];
}

export interface IranDynastyRecord {
  id: string;
  nameEn: string;
  nameFa: string;
  periodDisplay: string;
  startYear: number; // positive = CE, negative = BCE
  endYear: number;
  capitals: string;
  founder: string;
  keyAchievementEn: string;
  keyAchievementFa: string;
  notableMonarch: string;
  territoryExtent: string;
  eventsCount: number;
}

export interface IranEventRecord {
  id: string;
  yearDisplay: string;
  yearNumeric: number;
  titleEn: string;
  titleFa: string;
  category: 'political' | 'cultural' | 'scientific' | 'monument';
  descriptionEn: string;
  descriptionFa: string;
}

export interface IranThematicFacet {
  id: string;
  titleEn: string;
  titleFa: string;
  icon: string;
  items: {
    nameEn: string;
    nameFa: string;
    detailEn: string;
    detailFa: string;
    originPeriod: string;
  }[];
}

export interface ScholarlySourceRecord {
  id: string;
  name: string;
  domain: 'Paleoclimatology' | 'Paleobiology' | 'Tectonics' | 'Archaeology' | 'Linguistics' | 'Geodesy';
  domainFa: string;
  leadInstitution: string;
  coverage: string;
  license: 'CC-BY-4.0' | 'CC-BY-3.0' | 'CC0' | 'Public Domain' | 'Academic Open Access' | 'ODbL';
  confidenceLevel: 'High' | 'Very High' | 'Moderate' | 'Scenario Model';
  notesEn: string;
  notesFa: string;
  doiOrUrl: string;
}

// -------------------------------------------------------------
// PALEOGEOGRAPHY & CLIMATE EPOCHS
// -------------------------------------------------------------
export const PALEOGEOGRAPHY_EPOCHS: PaleogeographyState[] = [
  {
    epochId: 'rodinia',
    yearDisplay: '1.1 Ga (1,100 Ma)',
    yearsAgo: 1100000000,
    periodNameEn: 'Mesoproterozoic — Supercontinent Rodinia',
    periodNameFa: 'مزپروتروزوئیک — ابرقاره رودینیا',
    co2Ppm: 2400,
    tempAnomalyC: 4.2,
    seaLevelM: -40,
    iceCoverPct: 8,
    supercontinent: 'Rodinia',
    descriptionEn: 'Rodinia centers on Laurentia and Amazonia. Barren landmasses with no land vegetation; eukaryotic red algae emerge in coastal shallows.',
    descriptionFa: 'رودینیا در مرکز خشکی‌های اولیه متمرکز بود. خشکی‌ها کاملاً بی‌گیاه بودند و جلبک‌های پرسلولی اولیه در کناره‌ها پدیدار شدند.',
    majorTectonicEventEn: 'Grenville Orogeny mountain building',
    majorTectonicEventFa: 'کوه‌زایی گرنویل و تجمیع پوسته‌ها',
    svgContinents: [
      { name: 'Proto-Laurentia', path: 'M 350,180 Q 420,150 480,200 Q 510,270 450,300 Q 380,310 340,260 Z', fill: '#4A9B82' },
      { name: 'Proto-Amazonia', path: 'M 460,260 Q 520,240 550,290 Q 530,350 480,340 Z', fill: '#D19E83' },
      { name: 'Proto-Baltica', path: 'M 310,190 Q 350,170 360,220 Q 320,250 290,220 Z', fill: '#E8C62E' },
      { name: 'Proto-Australia', path: 'M 240,260 Q 300,240 320,300 Q 280,360 220,320 Z', fill: '#D25C58' },
    ],
  },
  {
    epochId: 'cambrian',
    yearDisplay: '514 Ma',
    yearsAgo: 514000000,
    periodNameEn: 'Cambrian Period — Gondwana Formation',
    periodNameFa: 'دوران کامبرین — شکل‌گیری گوندوانا',
    co2Ppm: 4500,
    tempAnomalyC: 7.8,
    seaLevelM: 120,
    iceCoverPct: 1,
    supercontinent: 'Proto-Gondwana & Laurentia',
    descriptionEn: 'Warm greenhouse planet. Extensive epeiric shallow seas where trilobites, archaeocyathids, and anomalocarid predators radiate.',
    descriptionFa: 'سیاره‌ای بسیار گرم و گلخانه‌ای با دریاهای کم‌عمق پهناور که محل انفجار حیات تریلوبیت‌ها و جانداران سخت‌پوست بود.',
    majorTectonicEventEn: 'Opening of the Iapetus Ocean',
    majorTectonicEventFa: 'گشایش اقیانوس یاپتوس',
    svgContinents: [
      { name: 'Gondwana', path: 'M 320,260 Q 480,200 620,280 Q 640,380 480,410 Q 330,370 300,320 Z', fill: '#4A9B82' },
      { name: 'Laurentia', path: 'M 180,180 Q 250,150 270,220 Q 220,260 170,230 Z', fill: '#D19E83' },
      { name: 'Baltica', path: 'M 250,260 Q 290,240 310,290 Q 270,320 230,290 Z', fill: '#E8C62E' },
      { name: 'Siberia', path: 'M 380,120 Q 460,110 470,160 Q 420,190 370,160 Z', fill: '#D25C58' },
    ],
  },
  {
    epochId: 'permian',
    yearDisplay: '252 Ma',
    yearsAgo: 252000000,
    periodNameEn: 'Latest Permian — Pangaea Supercontinent',
    periodNameFa: 'پایان دوران پرمین — ابرقاره پانگه‌آ',
    co2Ppm: 3200,
    tempAnomalyC: 11.5,
    seaLevelM: 60,
    iceCoverPct: 3,
    supercontinent: 'Pangaea (Panthalassa Ocean)',
    descriptionEn: 'The giant single C-shaped landmass of Pangaea surrounded by the vast Panthalassa Ocean. Catastrophic Siberian Traps flood basalts trigger global anoxia.',
    descriptionFa: 'ابرقاره یکپارچه پانگه‌آ و اقیانوس پهناور پانتالاسا. فوران عظیم تله‌های بازالتی سیبری و اسیدی‌شدن دریاها.',
    majorTectonicEventEn: 'Siberian Traps Eruption & Pangaea Full Assembly',
    majorTectonicEventFa: 'فوران تله‌های بازالتی سیبری و اوج شکل‌گیری پانگه‌آ',
    svgContinents: [
      { name: 'Pangaea Core', path: 'M 380,90 Q 480,110 520,180 Q 490,260 560,320 Q 530,420 380,420 Q 300,360 340,240 Q 300,160 380,90 Z', fill: '#1D453B' },
      { name: 'Tethys Gulf Islands', path: 'M 540,240 Q 590,220 620,260 Q 580,290 540,270 Z', fill: '#E8C62E' },
      { name: 'Cathaysian Blocks', path: 'M 640,180 Q 700,160 720,220 Q 670,250 630,210 Z', fill: '#4A9B82' },
    ],
  },
  {
    epochId: 'cretaceous',
    yearDisplay: '90 Ma',
    yearsAgo: 90000000,
    periodNameEn: 'Late Cretaceous — Tethys Ocean & Continental Rifting',
    periodNameFa: 'اواخر کرتاسه — اقیانوس تتیس و شکافت قاره‌ها',
    co2Ppm: 1600,
    tempAnomalyC: 6.5,
    seaLevelM: 180,
    iceCoverPct: 0,
    supercontinent: 'Laurasia & Gondwana fragmented',
    descriptionEn: 'High sea levels flood continental interiors (Western Interior Seaway). India races north as an island continent across the Tethys.',
    descriptionFa: 'سطح آب دریاها به بالاترین حد تاریخی می‌رسد. شبه‌قاره هند با سرعت به سمت آسیا در حرکت است و دایناسورها در اوج شکوه زیستی هستند.',
    majorTectonicEventEn: 'Atlantic Seafloor Spreading & India Isolation',
    majorTectonicEventFa: 'گسترش بستر اقیانوس اطلس و حرکت پرشتاب هند',
    svgContinents: [
      { name: 'North America', path: 'M 160,110 Q 250,100 280,180 Q 230,260 170,220 Z', fill: '#4A9B82' },
      { name: 'South America', path: 'M 240,260 Q 310,240 330,340 Q 270,410 230,330 Z', fill: '#D19E83' },
      { name: 'Eurasia', path: 'M 420,100 Q 640,90 690,190 Q 580,230 460,200 Z', fill: '#1D453B' },
      { name: 'Africa', path: 'M 400,200 Q 500,200 520,320 Q 450,380 390,300 Z', fill: '#E8C62E' },
      { name: 'India Island', path: 'M 570,300 Q 610,290 620,340 Q 580,360 560,330 Z', fill: '#D25C58' },
    ],
  },
  {
    epochId: 'modern',
    yearDisplay: 'Present (0 CE)',
    yearsAgo: 0,
    periodNameEn: 'Anthropocene / Holocene — Modern Geography',
    periodNameFa: 'هولوسن / آنتروپوسن — جغرافیای دوران مدرن',
    co2Ppm: 424,
    tempAnomalyC: 1.3,
    seaLevelM: 0,
    iceCoverPct: 10,
    supercontinent: 'Seven Modern Continents',
    descriptionEn: 'Current geography shaped by the Alpine-Himalayan collision and East African rift. Rapidly altering atmosphere and biosphere by human civilization.',
    descriptionFa: 'چیدمان کنونی قاره‌ها، برخورد فلات ایران و هیمالیا و باز شدن دریای سرخ. تأثیر مستقیم فعالیت انسان بر اتمسفر و زیست‌کره.',
    majorTectonicEventEn: 'Himalayan & Zagros Uplift Ongoing',
    majorTectonicEventFa: 'برخورد و ارتفاع‌گیری رشته‌کوه‌های زاگرس و هیمالیا',
    svgContinents: [
      { name: 'Americas', path: 'M 140,90 Q 240,80 230,190 Q 210,240 260,270 Q 270,390 220,410 Q 180,320 180,220 Q 120,150 140,90 Z', fill: '#4A9B82' },
      { name: 'Africa & Europe', path: 'M 380,80 Q 520,80 500,160 Q 530,220 530,340 Q 450,400 400,300 Q 380,220 380,140 Z', fill: '#1D453B' },
      { name: 'Asia', path: 'M 510,80 Q 730,90 710,220 Q 640,290 540,240 Q 500,170 510,80 Z', fill: '#D19E83' },
      { name: 'Australia', path: 'M 640,320 Q 720,300 730,380 Q 660,420 630,370 Z', fill: '#E8C62E' },
    ],
  },
  {
    epochId: 'future250m',
    yearDisplay: '+250 Million Years',
    yearsAgo: -250000000,
    periodNameEn: 'Future Earth — Pangaea Ultima',
    periodNameFa: 'آیندهٔ زمین — ابرقارهٔ پانگه‌آ اولتیما',
    co2Ppm: 550,
    tempAnomalyC: 8.0,
    seaLevelM: -50,
    iceCoverPct: 2,
    supercontinent: 'Pangaea Ultima / Amasia',
    descriptionEn: 'The Atlantic Ocean closes as subduction zones consume oceanic crust. Africa slams into Europe, and the Americas collide with Africa-Eurasia.',
    descriptionFa: 'بسته شدن اقیانوس اطلس و برخورد مجدد قاره‌های آمریکا با آفریقا و اوراسیا و شکل‌گیری ابرقاره جدید با مرکز بیابانی گرم.',
    majorTectonicEventEn: 'Atlantic Basin Subduction & Supercontinent Fusion',
    majorTectonicEventFa: 'فرورانش حوضه اطلس و تجمیع نهایی ابرقاره جدید',
    svgContinents: [
      { name: 'Pangaea Ultima Core', path: 'M 340,110 Q 540,90 600,190 Q 640,300 560,410 Q 380,430 300,330 Q 280,210 340,110 Z', fill: '#D25C58' },
      { name: 'Interior Remnant Sea', path: 'M 440,220 Q 500,200 520,260 Q 460,280 440,220 Z', fill: '#132E27' },
      { name: 'Antarctic Outlier', path: 'M 400,430 Q 480,420 490,460 Q 420,470 390,450 Z', fill: '#4A9B82' },
    ],
  },
];

// -------------------------------------------------------------
// THE BIG FIVE MASS EXTINCTIONS
// -------------------------------------------------------------
export const MASS_EXTINCTIONS: MassExtinctionEvent[] = [
  {
    id: 'ordovician',
    nameEn: 'Ordovician-Silurian Extinction',
    nameFa: 'انقراض اردویسین – سیلورین',
    yearsAgo: 445000000,
    timeLabel: '445 Ma',
    killCurvePct: 85,
    victimsEn: 'Brachiopods, trilobites, conodonts, graptolites',
    victimsFa: 'براکیوپودها، تریلوبیت‌ها، قیف‌دندان‌ها و گرافیت‌ها',
    triggersEn: 'Rapid Gondwana glaciation followed by ocean anoxia during deglaciation',
    triggersFa: 'یخ‌بندان ناگهانی گوندوانا و بی‌اکسیژنی گسترده آب‌های عمیق',
    recoveryYearsEn: '~5 million years',
    recoveryYearsFa: 'حدود ۵ میلیون سال',
  },
  {
    id: 'devonian',
    nameEn: 'Late Devonian Extinction (Kellwasser)',
    nameFa: 'انقراض اواخر دوونین (رویداد کل‌واسر)',
    yearsAgo: 375000000,
    timeLabel: '375 Ma',
    killCurvePct: 75,
    victimsEn: 'Placoderm armored fish, stromatoporoids, rugose coral reefs',
    victimsFa: 'ماهیان زره‌دار (پلاکودرم‌ها)، مرجان‌های روگوز و اسفنج‌های آهکی',
    triggersEn: 'Massive land plant soil weathering pulling CO2 down, ocean eutrophication',
    triggersFa: 'هوازدگی سریع خاک توسط گیاهان خشکی، کاهش شدید CO2 و خفگی دریاها',
    recoveryYearsEn: '~15 million years',
    recoveryYearsFa: 'حدود ۱۵ میلیون سال',
  },
  {
    id: 'permian_ext',
    nameEn: 'Permian-Triassic (The Great Dying)',
    nameFa: 'انقراض پرمین – تریاس (مرگ بزرگ)',
    yearsAgo: 252000000,
    timeLabel: '252 Ma',
    killCurvePct: 96,
    victimsEn: 'Trilobites wiped out, 96% marine invertebrates, gorgonopsids',
    victimsFa: 'انقراض کامل تریلوبیت‌ها، ۹۶٪ جانداران دریایی و سیناپسیدهای کهن',
    triggersEn: 'Siberian Traps basalt flood volcanism, runaway methane, ocean acidification',
    triggersFa: 'فوران تله‌های بازالتی سیبری، تصعید گازهای متان و اسیدی شدن مرگبار اقیانوس‌ها',
    recoveryYearsEn: '~10 to 30 million years',
    recoveryYearsFa: '۱۰ تا ۳۰ میلیون سال',
  },
  {
    id: 'triassic_ext',
    nameEn: 'Triassic-Jurassic Extinction',
    nameFa: 'انقراض تریاس – ژوراسیک',
    yearsAgo: 201000000,
    timeLabel: '201 Ma',
    killCurvePct: 80,
    victimsEn: 'Conodonts, pseudosuchian archosaurs, large amphibians',
    victimsFa: 'قیف‌دندان‌ها، شاه‌سوسمارهای کهن و دوزیستان غول‌پیکر',
    triggersEn: 'Central Atlantic Magmatic Province (CAMP) rift eruptions',
    triggersFa: 'فوران‌های شکافتی استان ماگمایی اطلس مرکزی (CAMP)',
    recoveryYearsEn: '~4 million years (paved way for Dinosaurs)',
    recoveryYearsFa: 'حدود ۴ میلیون سال (آغاز عصر حاکمیت دایناسورها)',
  },
  {
    id: 'kpg_ext',
    nameEn: 'Cretaceous-Paleogene (Chicxulub Impact)',
    nameFa: 'انقراض کرتاسه – پالئوژن (برخورد چیکشلوب)',
    yearsAgo: 66000000,
    timeLabel: '66 Ma',
    killCurvePct: 76,
    victimsEn: 'Non-avian dinosaurs, pterosaurs, ammonites, mosasaurs',
    victimsFa: 'دایناسورهای غیرپرنده، پتروسورها (خزندگان بال‌دار)، آمونیت‌ها',
    triggersEn: '10km Asteroid impact at Yucatan + Deccan Traps volcanism in India',
    triggersFa: 'برخورد سیارک ۱۰ کیلومتری در شبه‌جزیره یوکاتان و فوران دکن هند',
    recoveryYearsEn: '~2 million years (paved way for Mammalian radiation)',
    recoveryYearsFa: 'حدود ۲ میلیون سال (شکوفایی و تنوع پستانداران)',
  },
];

// -------------------------------------------------------------
// 60 REPRESENTATIVE CLADES OF THE TREE OF LIFE
// -------------------------------------------------------------
export const CLADES_OF_LIFE: CladeLifeGroup[] = [
  {
    id: 'cyanobacteria',
    nameEn: 'Cyanobacteria (Blue-Green Algae)',
    nameFa: 'سیانوباکتری‌ها (باکتری‌های فتوسنتزکننده)',
    cladeCategory: 'microbe',
    appearedYearsAgo: 3500000000,
    appearedLabelEn: '3.5 Ga',
    appearedLabelFa: '۳٫۵ میلیارد سال پیش',
    iconType: 'Sparkles',
    descriptionEn: 'Invented oxygenic photosynthesis; transformed the planet during the Great Oxidation Event.',
    descriptionFa: 'ابداع‌کنندگان فتوسنتز اکسیژنی؛ سیاره را در رویداد بزرگ اکسیداسیون دگرگون کردند.',
  },
  {
    id: 'eukaryotes',
    nameEn: 'First Eukaryotes (Nucleated Cells)',
    nameFa: 'نخستین یوکاریوت‌ها (سلول‌های هسته‌دار)',
    cladeCategory: 'microbe',
    appearedYearsAgo: 2100000000,
    appearedLabelEn: '2.1 Ga',
    appearedLabelFa: '۲٫۱ میلیارد سال پیش',
    iconType: 'Dna',
    descriptionEn: 'Endosymbiotic engulfment of proteobacteria forming mitochondria.',
    descriptionFa: 'درون‌هم‌زیستی سرنوشت‌ساز و پیدایش میتوکندری در سلول‌های پیچیده.',
  },
  {
    id: 'trilobita',
    nameEn: 'Trilobites (Trilobita)',
    nameFa: 'تریلوبیت‌ها (بندپایان کهن)',
    cladeCategory: 'invertebrate',
    appearedYearsAgo: 521000000,
    extinctYearsAgo: 252000000,
    appearedLabelEn: '521 Ma (Early Cambrian)',
    appearedLabelFa: '۵۲۱ میلیون سال پیش (کامبرین)',
    extinctLabelEn: '252 Ma (Permian Extinction)',
    extinctLabelFa: '۲۵۲ میلیون سال پیش (انقراض پرمین)',
    iconType: 'Bug',
    isBigFiveVictim: true,
    descriptionEn: 'Over 20,000 described species dominant for 270 million years; calcite compound eyes.',
    descriptionFa: 'بیش از ۲۰ هزار گونه ثبت‌شده که ۲۷۰ میلیون سال بر دریاها حکمرانی کردند با چشمان کلسیتی مرکب.',
  },
  {
    id: 'placodermi',
    nameEn: 'Placoderms (Armored Jawed Fish)',
    nameFa: 'پلاکودرم‌ها (ماهیان زره‌دار آرواره‌دار)',
    cladeCategory: 'fish',
    appearedYearsAgo: 430000000,
    extinctYearsAgo: 359000000,
    appearedLabelEn: '430 Ma (Silurian)',
    appearedLabelFa: '۴۳۰ میلیون سال پیش (سیلورین)',
    extinctLabelEn: '359 Ma (End Devonian)',
    extinctLabelFa: '۳۵۹ میلیون سال پیش (پایان دوونین)',
    iconType: 'Fish',
    isBigFiveVictim: true,
    descriptionEn: 'First vertebrates to evolve true jaws; Dunkleosteus was an 8-meter apex predator.',
    descriptionFa: 'نخستین مهره‌دارانی که آرواره واقعی یافتند؛ دانکل‌استئوس شکارچی رأس زنجیره به طول ۸ متر بود.',
  },
  {
    id: 'cooksonia',
    nameEn: 'Early Vascular Land Plants (Cooksonia)',
    nameFa: 'نخستین گیاهان آوندی خشکی (کوکسونیا)',
    cladeCategory: 'plant',
    appearedYearsAgo: 433000000,
    appearedLabelEn: '433 Ma',
    appearedLabelFa: '۴۳۳ میلیون سال پیش',
    iconType: 'TreePine',
    descriptionEn: 'Colonized barren continents, developing xylem for fluid conduction.',
    descriptionFa: 'آغاز فتح خشکی‌ها توسط گیاهان دارای آوند برای انتقال مواد غذایی و آب.',
  },
  {
    id: 'tetrapods',
    nameEn: 'Stem Tetrapods (Tiktaalik & Acanthostega)',
    nameFa: 'تتراپودهای اولیه (تیکتالیک و پیشگامان چهارپا)',
    cladeCategory: 'amphibian' as any,
    appearedYearsAgo: 375000000,
    appearedLabelEn: '375 Ma',
    appearedLabelFa: '۳۷۵ میلیون سال پیش',
    iconType: 'Footprints',
    descriptionEn: 'Transitional fossils walking out of Devonian wetlands onto land.',
    descriptionFa: 'فسیل‌های بینابینی که انتقال از آب‌های کم‌عمق به خشکی با چهار دست و پا را رقم زدند.',
  },
  {
    id: 'synapsids',
    nameEn: 'Synapsida (Mammal-like Reptiles)',
    nameFa: 'سیناپسیدها (اجداد کهن پستانداران)',
    cladeCategory: 'mammal',
    appearedYearsAgo: 318000000,
    appearedLabelEn: '318 Ma (Carboniferous)',
    appearedLabelFa: '۳۱۸ میلیون سال پیش',
    iconType: 'PawPrint',
    descriptionEn: 'Single temporal fenestra behind eye; Dimetrodon and Gorgonopsids.',
    descriptionFa: 'دارای یک حفره گیجگاهی پشت چشم؛ دیمترودون با بادبان پشتی و گرگونوپس‌ها.',
  },
  {
    id: 'sauropoda',
    nameEn: 'Sauropod Dinosaurs (Long-Necks)',
    nameFa: 'سوروپودها (دایناسورهای غول‌پیکر گردن‌دراز)',
    cladeCategory: 'dinosaur',
    appearedYearsAgo: 228000000,
    extinctYearsAgo: 66000000,
    appearedLabelEn: '228 Ma',
    appearedLabelFa: '۲۲۸ میلیون سال پیش',
    extinctLabelEn: '66 Ma (K-Pg Impact)',
    extinctLabelFa: '۶۶ میلیون سال پیش (چیکشلوب)',
    iconType: 'Crown',
    isBigFiveVictim: true,
    descriptionEn: 'Largest terrestrial animals to ever walk Earth; Argentinosaurus reached 70+ tonnes.',
    descriptionFa: 'بزرگ‌ترین جانوران خشکی‌زی تاریخ زمین؛ آرژانتینوسوروس با وزنی فراتر از ۷۰ تن.',
  },
  {
    id: 'pterosauria',
    nameEn: 'Pterosaurs (Flying Reptiles)',
    nameFa: 'پتروسورها (خزندگان پرندهٔ آسمان کهن)',
    cladeCategory: 'reptile',
    appearedYearsAgo: 220000000,
    extinctYearsAgo: 66000000,
    appearedLabelEn: '220 Ma',
    appearedLabelFa: '۲۲۰ میلیون سال پیش',
    extinctLabelEn: '66 Ma',
    extinctLabelFa: '۶۶ میلیون سال پیش',
    iconType: 'Bird',
    isBigFiveVictim: true,
    descriptionEn: 'First vertebrates to achieve powered flight; Quetzalcoatlus had an 11-meter wingspan.',
    descriptionFa: 'نخستین مهره‌داران با توانایی پرواز فعال؛ کوئیزالکواتلوس با پهنای بال ۱۱ متر.',
  },
  {
    id: 'angiosperms',
    nameEn: 'Angiosperms (Flowering Plants)',
    nameFa: 'نهان‌دانگان (گیاهان گل‌دار)',
    cladeCategory: 'plant',
    appearedYearsAgo: 135000000,
    appearedLabelEn: '135 Ma (Early Cretaceous)',
    appearedLabelFa: '۱۳۵ میلیون سال پیش',
    iconType: 'Flower',
    descriptionEn: 'Co-evolved with pollinators, completely transforming terrestrial nutrition and landscapes.',
    descriptionFa: 'فرگشت هم‌گام با حشرات گرده‌افشان و تسلط مطلق بر پوشش گیاهی خشکی‌ها.',
  },
  {
    id: 'cetacea',
    nameEn: 'Cetaceans (Whales & Dolphins)',
    nameFa: 'آب‌بازسانان (نهنگ‌ها و دلفین‌ها)',
    cladeCategory: 'mammal',
    appearedYearsAgo: 50000000,
    appearedLabelEn: '50 Ma',
    appearedLabelFa: '۵۰ میلیون سال پیش',
    iconType: 'Waves',
    descriptionEn: 'Even-toed ungulates that returned to the oceans, becoming the largest animals in Earth history.',
    descriptionFa: 'پستانداران خشکی‌زی که به آب بازگشتند و بزرگ‌ترین موجود تاریخ زمین (نهنگ آبی) را پدید آوردند.',
  },
  {
    id: 'hominini',
    nameEn: 'Hominini (Bipedal Apes & Humans)',
    nameFa: 'هومینینی (انسان‌تباران دوپا)',
    cladeCategory: 'hominid',
    appearedYearsAgo: 7000000,
    appearedLabelEn: '7 Ma (Sahelanthropus)',
    appearedLabelFa: '۷ میلیون سال پیش',
    iconType: 'User',
    descriptionEn: 'Bipedal locomotion, encephalization, complex language, fire control, and technology.',
    descriptionFa: 'راه‌رفتن روی دو پا، رشد حجم مغز، ابزارسازی سنگی، مهار آتش و تکلم نمادین.',
  },
];

// -------------------------------------------------------------
// 78 GLOBAL CIVILIZATIONS SAMPLE (Highlighted Key Polities)
// -------------------------------------------------------------
export const CIVILIZATIONS_CATALOG: CivilizationRecord[] = [
  {
    id: 'elam',
    nameEn: 'Elamite Civilization',
    nameFa: 'تمدن کهن عیلام',
    region: 'Middle East',
    regionFa: 'خاورمیانه و غرب آسیا',
    startBce: 3200,
    endBce: 539,
    periodLabel: '3200 – 539 BCE',
    capitalEn: 'Susa & Anshan',
    capitalFa: 'شوش و انشان',
    governmentEn: 'Federated monarchy with sukkalmah (supreme regent) and regional vice-regents.',
    governmentFa: 'پادشاهی فدراتیو با سوکل‌ماخ (نایب‌السلطنه اعظم) و فرمانروایان محلی شوش و انشان.',
    economyEn: 'Highland-lowland pastoral transhumance, tin and lapis lazuli trade, irrigated wheat agriculture.',
    economyFa: 'پیوند کشاورزی جلگه‌ای خوزستان با اقتصاد شبانی زاگرس، تجارت قلع و لاجورد.',
    languageEn: 'Elamite (Linguistic isolate; Linear Elamite and Elamite Cuneiform scripts).',
    languageFa: 'زبان عیلامی (تک‌خانواده زبانی؛ با خط نیاعیلامی، عیلامی خطی و خط میخی عیلامی).',
    beliefsEn: 'Polytheism honoring Inshushinak (lord of Susa), Pinikir, and waters of life.',
    beliefsFa: 'نظام ایزدان با محوریت اینشوشیناک (ایزد شوش و داور مردگان)، پینیکیر و آب‌های مقدس.',
    engineeringEn: 'Chogha Zanbil UNESCO ziggurat, sophisticated clay baked drainage, monumental bronze casting.',
    engineeringFa: 'زیگورات چغازنبیل، شبکه آبرسانی پیشرفته با کانال‌های سفالی، ریخته‌گری مفرغی عظیم.',
    declineEn: 'Devastating sack of Susa by Neo-Assyrian Ashurbanipal (646 BCE), incorporated by Achaemenids.',
    declineFa: 'یورش و ویرانی شوش توسط آشوربانی‌پال در ۶۴۶ پیش از میلاد و سپس جذب در شاهنشاهی هخامنشی.',
    legacyEn: 'Royal dress, administrative protocols, and legal traditions passed directly to Persia.',
    legacyFa: 'سنت‌های دیوانی، پوشش شاهی و خط میخی عیلامی که تا کتیبه بیستون تداوم یافت.',
    contemporariesEn: ['Sumer', 'Akkad', 'Indus Valley', 'Old Kingdom Egypt'],
    contemporariesFa: ['سومر', 'آکد', 'تمدن دره سند', 'پادشاهی کهن مصر'],
  },
  {
    id: 'achaemenid',
    nameEn: 'Achaemenid Persian Empire',
    nameFa: 'شاهنشاهی هخامنشی',
    region: 'Middle East',
    regionFa: 'خاورمیانه و غرب آسیا',
    startBce: 550,
    endBce: 330,
    periodLabel: '550 – 330 BCE',
    capitalEn: 'Pasargadae, Persepolis, Susa, Ecbatana',
    capitalFa: 'پاسارگاد، تخت جمشید، شوش، هگمتانه',
    governmentEn: 'Satrapial administration under the King of Kings with institutional autonomy for subjects.',
    governmentFa: 'نظام شهربانی (ساتراپی) تحت فرمان شاهنشاه با احترام به خودمختاری محلی و ادیان ملل.',
    economyEn: 'Standardized bimetallic coinage (Gold Daric & Silver Siglos), Royal Road trade network.',
    economyFa: 'نظام استاندارد دوپولی (دریک طلا و سیگلو نقره)، امنیت بازرگانی شاهراه شاهی.',
    languageEn: 'Old Persian (monumental), Imperial Aramaic (lingua franca admin), Elamite, Babylonian.',
    languageFa: 'فارسی باستان (سنگ‌نبشته‌ها)، آرامی شاهی (زبان دیپلماسی و اسناد)، عیلامی و بابلی.',
    beliefsEn: 'Zoroastrian principles of Asha (truth and cosmic cosmic order) invoking Ahura Mazda.',
    beliefsFa: 'آیین مزدیسنا و بزرگداشت اهورامزدا در کنار ستایش راستی (اشه) و نکوهش دروغ (دروج).',
    engineeringEn: 'Persepolis monumental terrace and apadana column architecture, Qanat irrigation systems, Suez Canal precursor.',
    engineeringFa: 'صفه و ستون‌های تخت جمشید، حفر کانال داریوش در سوئز، شبکه مهندسی قنات.',
    declineEn: 'Campaigns of Alexander of Macedon culminating in Gaugamela and the burning of Persepolis (330 BCE).',
    declineFa: 'لشکرکشی اسکندر مقدونی، نبرد گوگمل و به آتش کشیده‌شدن تخت جمشید در ۳۳۰ پیش از میلاد.',
    legacyEn: 'Cyrus Cylinder human rights ethos, universal postal system, global imperial bureaucracy blueprint.',
    legacyFa: 'منشور کوروش بزرگ، الگوی اداری امپراتوری‌های جهان، سیستم چاپار و ارتباطات سریع.',
    contemporariesEn: ['Classical Athens', 'Carthage', 'Nanda Empire (India)', 'Zhou / Warring States (China)'],
    contemporariesFa: ['آتن کلاسیک', 'کارتاژ', 'سلسله ناندا هند', 'دوران دولت‌های جنگ‌طلب چین'],
  },
  {
    id: 'han',
    nameEn: 'Han Dynasty China',
    nameFa: 'امپراتوری هان چین',
    region: 'Asia',
    regionFa: 'شرق آسیا',
    startBce: 202,
    endBce: -220,
    periodLabel: '202 BCE – 220 CE',
    capitalEn: 'Chang\'an, Luoyang',
    capitalFa: 'چانگ‌آن، لویانگ',
    governmentEn: 'Centralized imperial bureaucracy guided by Confucian state examination scholarship.',
    governmentFa: 'دیوان‌سالاری مرکزی آزمون‌محور مبتنی بر فلسفه اخلاقی و سیاسی کنفوسیوس.',
    economyEn: 'State monopolies on salt and iron, silk export, Silk Road caravan trade with Parthia.',
    economyFa: 'انحصار دولتی نمک و آهن، تولید انبوه ابریشم و مبادلات جاده ابریشم با پارت‌ها.',
    languageEn: 'Classical Chinese with clerical and seal scripts.',
    languageFa: 'چینی باستان با خط نگارشی استاندارد درباری.',
    beliefsEn: 'Confucianism, Daoism, and introduction of Buddhism from Central Asia.',
    beliefsFa: 'کنفوسیوس‌گرایی به عنوان ایدئولوژی دولت، تائوئیسم و ورود آیین بودا.',
    engineeringEn: 'Invention of papermaking (Cai Lun), seismoscope, Great Wall extension, wheelbarrow.',
    engineeringFa: 'اختراع کاغذ توسط تسای لون، نخستین زلزله‌نگار، توسعه دیوار بزرگ چین و چرخ‌دستی.',
    declineEn: 'Yellow Turban peasant rebellions, warlord factionalism leading into Three Kingdoms period.',
    declineFa: 'شورش دستار زردها، نفوذ خواجه‌سرایان و تجزیه به دوران سه پادشاهی.',
    legacyEn: 'Ethno-cultural identity of Han Chinese, civil service testing standard for millennia.',
    legacyFa: 'شکل‌گیری هویت قوم هان و نظام شایسته‌سالاری آزمون‌های اداری چین.',
    contemporariesEn: ['Parthian Empire', 'Roman Republic / Empire', 'Kushan Empire'],
    contemporariesFa: ['شاهنشاهی اشکانی', 'جمهوری و امپراتوری روم', 'شاهنشاهی کوشان'],
  },
  {
    id: 'rome',
    nameEn: 'Roman Empire',
    nameFa: 'امپراتوری روم',
    region: 'Europe',
    regionFa: 'اروپا و مدیترانه',
    startBce: 27,
    endBce: -476,
    periodLabel: '27 BCE – 476 CE',
    capitalEn: 'Rome, Ravenna, Constantinople',
    capitalFa: 'رم، راونا، قسطنطنیه',
    governmentEn: 'Autocratic Principate and Dominate resting on Senate facade and legionary military power.',
    governmentFa: 'نظام پرینسیپاته و دومیناته مبتنی بر ارتش لژیونر و نهادهای قانونی سنا.',
    economyEn: 'Mediterranean maritime basin trade (Mare Nostrum), slave-labor latifundia, grain dole.',
    economyFa: 'شبکه بازرگانی دریای مدیترانه، مزارع بزرگ با نیروی کار برده و توزیع غلات دولتی.',
    languageEn: 'Latin in Western provinces; Koine Greek in Eastern provinces.',
    languageFa: 'لاتین در غرب؛ یونانی کوئینه در استان‌های شرقی.',
    beliefsEn: 'Greco-Roman Olympian polytheism; state Christianization under Constantine & Theodosius.',
    beliefsFa: 'چندخداپرستی پاگان رومی؛ سپس پذیرش و تحکیم مسیحیت به عنوان دین رسمی دولت.',
    engineeringEn: 'Hydraulic pozzolanic concrete, monumental aqueducts, arches, Colosseum, Pantheon.',
    engineeringFa: 'بتن هیدرولیکی پوزولانی، آب‌گذرهای معلق، گنبد پانتئون و شبکه ۲۵۰ هزار کیلومتری راه‌ها.',
    declineEn: 'Hyperinflation, Germanic migrations (Goths, Vandals), division into East and West (395 CE).',
    declineFa: 'بحران سده سوم، تورم شدید، هجوم قبایل ژرمن و تجزیه به روم غربی و روم شرقی.',
    legacyEn: 'Civil law foundation (Corpus Juris Civilis), Romance languages, republican terminology.',
    legacyFa: 'پایه‌گذاری حقوق مدنی اروپا، زبان‌های رومی، معماری گنبد و طاق و الفبای لاتین.',
    contemporariesEn: ['Parthian & Sasanian Empires', 'Han Dynasty', 'Aksumite Kingdom'],
    contemporariesFa: ['شاهنشاهی اشکانی و ساسانی', 'سلسله هان چین', 'پادشاهی آکسوم'],
  },
  {
    id: 'sasanian',
    nameEn: 'Sasanian Empire (Eranshahr)',
    nameFa: 'شاهنشاهی ساسانی (ایران‌شهر)',
    region: 'Middle East',
    regionFa: 'خاورمیانه و غرب آسیا',
    startBce: -224,
    endBce: -651,
    periodLabel: '224 – 651 CE',
    capitalEn: 'Ctesiphon (Tyspwn)',
    capitalFa: 'تیسفون',
    governmentEn: 'Eranshahr statehood: sacred Zoroastrian monarchy supported by four societal castes.',
    governmentFa: 'مفهوم دولت‌داری ایران‌شهر: همبستگی دین و پادشاهی با ساختار چهارگانه طبقات اجتماعی.',
    economyEn: 'Silk Road transit hubs, silver Drahm currency standard across Eurasia, state irrigation.',
    economyFa: 'کنترل گلوگاه‌های زمینی و دریایی جاده ابریشم، درهم نقره ساسانی به عنوان ارز بین‌المللی.',
    languageEn: 'Middle Persian (Pahlavi) written in Inscriptional and Book Pahlavi script.',
    languageFa: 'فارسی میانه (پهلوی ساسانی) با خط و کتیبه‌های پهلوی.',
    beliefsEn: 'Zoroastrianism as codified state church with Mobad-e Mobadan; Avesta compilation.',
    beliefsFa: 'تدوین رسمی کتاب اوستا و نهاد روحانی موبدموبدان؛ رویارویی با مانویت و مزدکیت.',
    engineeringEn: 'Taq Kasra (largest unreinforced single-span brick arch in the world), Shushtar hydraulic system.',
    engineeringFa: 'طاق کسری (بزرگ‌ترین طاق خشتی بدون قالب‌بندی جهان)، سازه‌های آبی شوشتر، دانشگاه گندی‌شاپور.',
    declineEn: 'Exhausting 26-year war with Byzantium, internal dynastic coups, Arab Muslim conquest (651 CE).',
    declineFa: 'جنگ فرسایشی ۲۶ ساله با روم شرقی، بحران جانشینی و در نهایت نبردهای قادسیه و نهاوند.',
    legacyEn: 'Gundeshapur medical school, chess dissemination, chivalric ethos, Islamic golden age administrative forms.',
    legacyFa: 'دانشگاه گندی‌شاپور، انتقال شطرنج، آیین‌های پهلوانی و پایه‌ریزی دیوان‌داری دوران اسلامی.',
    contemporariesEn: ['Byzantine Empire', 'Gupta Empire (India)', 'Kingdom of Aksum', 'Tang China'],
    contemporariesFa: ['امپراتوری بیزانس', 'امپراتوری گوپتا هند', 'پادشاهی آکسوم اتیوپی', 'دودمان تانگ چین'],
  },
  {
    id: 'maya',
    nameEn: 'Classic Maya Civilization',
    nameFa: 'تمدن کلاسیک مایا',
    region: 'Americas',
    regionFa: 'قاره آمریکا (مسوآمریکا)',
    startBce: -250,
    endBce: -900,
    periodLabel: '250 – 900 CE',
    capitalEn: 'Tikal, Calakmul, Palenque, Copán',
    capitalFa: 'تیکال، کالاکمول، پالنکه، کوپان',
    governmentEn: 'Competing city-states ruled by divine k\'uhul ajaw kings engaged in complex alliances.',
    governmentFa: 'دولت‌شهرهای رقیب با پادشاهان الهی (کوهول آخاو) و ائتلاف‌های پیچیده نظامی.',
    economyEn: 'Raised field agriculture, cacao bean currency, obsidian and jade exchange networks.',
    economyFa: 'کشاورزی در زمین‌های باتلاقی زهکشی‌شده، استفاده از دانه‌های کاکائو به عنوان پول، تجارت یشم.',
    languageEn: 'Mayan hieroglyphic logographic and syllabic script.',
    languageFa: 'هیروگلیف پیچیده مایا با نشانه‌های واژگانی و هجایی.',
    beliefsEn: 'Cosmology with 13 heavens and 9 underworlds (Xibalba); Long Count calendar cycles.',
    beliefsFa: 'کیهان‌شناسی با طبقات سیزده‌گانه آسمان و جهان زیرین (شیبالبا)؛ تقویم‌های بسیار دقیق نجومی.',
    engineeringEn: 'Stepped pyramid temples, precision zenith observation towers, mathematical discovery of zero.',
    engineeringFa: 'اهرام پله‌ای عظیم در جنگل بارانی، ابداع مستقل مفهوم ریاضی صفر، گاه‌شماری دقیق خورشیدی.',
    declineEn: 'Severe megadroughts combined with deforestation and intense inter-city warfare in 9th century.',
    declineFa: 'خشکسالی‌های شدید و پیاپی، جنگ‌های مخرب میان شهرها و رها شدن مراکز بزرگ در قرن نهم میلادی.',
    legacyEn: 'Indigenous linguistic survival of 30 Mayan languages, mathematical and calendrical marvels.',
    legacyFa: 'تداوم بیش از ۳۰ زبان زنده مایایی و دستاوردهای جاودان ریاضی و نجوم باستان.',
    contemporariesEn: ['Teotihuacan', 'Zapotec Empire', 'Moche Civilization (Peru)'],
    contemporariesFa: ['تئوئیتیواکان', 'تمدن زاپوتک', 'تمدن موچه پرو'],
  },
  {
    id: 'abbasid',
    nameEn: 'Abbasid Caliphate (Islamic Golden Age)',
    nameFa: 'خلافت عباسی و عصر طلایی دانش',
    region: 'Middle East',
    regionFa: 'خاورمیانه و شمال آفریقا',
    startBce: -750,
    endBce: -1258,
    periodLabel: '750 – 1258 CE',
    capitalEn: 'Baghdad (Round City), Samarra',
    capitalFa: 'بغداد (مدینة السلام)، سامرا',
    governmentEn: 'Universal caliphate heavily reliant on Iranian viziers (Barmakids) and administrative apparatus.',
    governmentFa: 'خلافت با تکیه بر دیوان‌سالاری و وزیران کاردان ایرانی (خاندان برمکی) و فرمانروایی‌های خودمختار.',
    economyEn: 'Monetary silver dirham/gold dinar basin, maritime trade from Persian Gulf to Guangzhou, paper mills.',
    economyFa: 'شبکه بازرگانی از خلیج فارس تا چین، کارخانه‌های کاغذسازی، بانکداری با برات و صکوک.',
    languageEn: 'Arabic (scholarly lingua franca) with Persian (literary New Persian renaissance).',
    languageFa: 'عربی (زبان علمی) در کنار رنسانس ادبی زبان فارسی دری در خراسان و ماوراءالنهر.',
    beliefsEn: 'Islam with rich intellectual schools (Mu\'tazila rationalism, Sufism, Ash\'arism).',
    beliefsFa: 'اندیشه اسلامی با بالندگی مکاتب کلامی (عقل‌گرایی معتزله)، فقهی، فلسفی و عرفان.',
    engineeringEn: 'House of Wisdom (Bayt al-Hikma), algebra foundation (al-Khwarizmi), astrolabes, optics.',
    engineeringFa: 'بیت‌الحکمه، پایه‌گذاری جبر توسط خوارزمی، نورشناسی ابن‌هیثم، پزشکی ابن‌سینا، اسطرلاب.',
    declineEn: 'Fragmentation into autonomous regional sultanates, culminated in Mongol sack of Baghdad (1258).',
    declineFa: 'تجزیه قدرت به حکومت‌های مستقل محلی و سرانجام سقوط بغداد توسط هلاکوخان مغول در ۱۲۵۸ م.',
    legacyEn: 'Preservation and critical advancement of world science, medical encyclopedias, algebra.',
    legacyFa: 'انتقال و بسط دانش یونان، هند و ایران، قانون ابن‌سینا و پایه‌ریزی علوم نوین جهانی.',
    contemporariesEn: ['Tang & Song China', 'Carolingian Empire (Europe)', 'Khmer Empire', 'Chola Empire (India)'],
    contemporariesFa: ['دودمان تانگ و سونگ چین', 'امپراتوری کارولنژی اروپا', 'امپراتوری خمر', 'امپراتوری چولا هند'],
  },
];

// -------------------------------------------------------------
// IRAN PILOT: 28 STATES & SPECIAL FACETS
// -------------------------------------------------------------
export const IRAN_DYNASTIES_DATA: IranDynastyRecord[] = [
  {
    id: 'elam_pilot',
    nameEn: 'Elamite Civilizations',
    nameFa: 'پادشاهی‌های عیلام',
    periodDisplay: '3200 – 539 BCE',
    startYear: -3200,
    endYear: -539,
    capitals: 'Awan, Shimashki, Susa, Anshan',
    founder: 'Peli of Awan / Untash-Napirisha',
    keyAchievementEn: 'Chogha Zanbil Ziggurat, Linear Elamite script decipherment, metallurgy.',
    keyAchievementFa: 'ساخت زیگورات چغازنبیل، خط و نگارش عیلامی، فلزکاری کهن مفرغ.',
    notableMonarch: 'Untash-Napirisha & Shutruk-Nakhkhunte',
    territoryExtent: 'Khuzestan, Fars, Zagros mountains, Persian Gulf coastline',
    eventsCount: 8,
  },
  {
    id: 'medes',
    nameEn: 'Median Kingdom',
    nameFa: 'پادشاهی ماد',
    periodDisplay: '678 – 550 BCE',
    startYear: -678,
    endYear: -550,
    capitals: 'Ecbatana (Hamadan)',
    founder: 'Deioces (Diyako)',
    keyAchievementEn: 'Unification of Iranian tribes, overthrow of the Neo-Assyrian Empire at Nineveh (612 BCE).',
    keyAchievementFa: 'اتحاد قبایل ایرانی، تاسیس هگمتانه، پایان دادن به سلطه آشور در نینوا (۶۱۲ پ.م).',
    notableMonarch: 'Cyaxares (Huvaxshatra)',
    territoryExtent: 'Anatolia (Halys river) to Central Iranian plateau',
    eventsCount: 5,
  },
  {
    id: 'achaemenid_pilot',
    nameEn: 'Achaemenid Empire',
    nameFa: 'شاهنشاهی هخامنشی',
    periodDisplay: '550 – 330 BCE',
    startYear: -550,
    endYear: -330,
    capitals: 'Pasargadae, Persepolis, Susa, Ecbatana, Babylon',
    founder: 'Cyrus the Great',
    keyAchievementEn: 'World\'s first universal human rights charter, 2,500km Royal Road, Persepolis architecture.',
    keyAchievementFa: 'منشور حقوق بشر کوروش بزرگ، احداث ۲۵۰۰ کیلومتر شاهراه شاهی، معماری آپادانا.',
    notableMonarch: 'Cyrus II, Darius I the Great, Xerxes I',
    territoryExtent: 'From Indus River and Central Asia to Egypt, Thrace, and Aegean Sea (~5.5M km²)',
    eventsCount: 16,
  },
  {
    id: 'parthian_pilot',
    nameEn: 'Parthian Empire (Arsacid)',
    nameFa: 'شاهنشاهی اشکانی',
    periodDisplay: '247 BCE – 224 CE',
    startYear: -247,
    endYear: 224,
    capitals: 'Nisa, Hecatompylos, Ctesiphon',
    founder: 'Arsaces I',
    keyAchievementEn: 'Defeat of Crassus at Carrhae (53 BCE), opening and securing Silk Road commerce.',
    keyAchievementFa: 'پیروزی سورنا در نبرد حران (کارهه)، امنیت جاده ابریشم میان چین و روم.',
    notableMonarch: 'Mithridates I, Mithridates II, Orodes II',
    territoryExtent: 'Euphrates River to Indus, Caspian Sea to Persian Gulf',
    eventsCount: 12,
  },
  {
    id: 'sasanian_pilot',
    nameEn: 'Sasanian Empire',
    nameFa: 'شاهنشاهی ساسانی',
    periodDisplay: '224 – 651 CE',
    startYear: 224,
    endYear: 651,
    capitals: 'Ctesiphon, Istakhr',
    founder: 'Ardashir I Papakan',
    keyAchievementEn: 'Gundeshapur Medical Academy, Taq Kasra vault, silver currency standard.',
    keyAchievementFa: 'دانشگاه گندی‌شاپور، طاق کسری تیسفون، تثبیت پول درهم در سراسر آسیا.',
    notableMonarch: 'Shapur I, Shapur II, Khosrow I Anushirvan',
    territoryExtent: 'Mesopotamia, Iranian Plateau, Caucasus, Central Asia, Indus margins',
    eventsCount: 14,
  },
  {
    id: 'tahirid_saffarid_samanid',
    nameEn: 'Samanid Renaissance',
    nameFa: 'سامانیان و رنسانس ایرانی',
    periodDisplay: '819 – 999 CE',
    startYear: 819,
    endYear: 999,
    capitals: 'Bukhara, Samarkand',
    founder: 'Ahmad ibn Asad / Ismail Samani',
    keyAchievementEn: 'Patronage of Ferdowsi, Rudaki, and Avicenna; resurrection of Persian literature.',
    keyAchievementFa: 'احیای زبان و ادب فارسی دری، حامیان رودکی، آغاز شاهنامه، رشد ابن‌سینا و بیرونی.',
    notableMonarch: 'Amir Ismail Samani, Nasr II',
    territoryExtent: 'Khorasan, Transoxiana, Sistan, Rayy',
    eventsCount: 9,
  },
  {
    id: 'seljuk',
    nameEn: 'Great Seljuk Empire',
    nameFa: 'امپراتوری سلجوقیان بزرگ',
    periodDisplay: '1037 – 1194 CE',
    startYear: 1037,
    endYear: 1194,
    capitals: 'Nishapur, Rayy, Isfahan, Merv',
    founder: 'Tughril Beg & Chaghri Beg',
    keyAchievementEn: 'Nizamiyyah academies established by Vizier Nizam al-Mulk; Jalali Solar Calendar (Omar Khayyam).',
    keyAchievementFa: 'مدارس نظامیه توسط خواجه نظام‌الملک طوسی، تقویم جلالی با سرپرستی خیام نیشابوری.',
    notableMonarch: 'Alp Arslan, Malik Shah I, Sultan Sanjar',
    territoryExtent: 'Hindu Kush to Anatolia, Persian Gulf to Aral Sea',
    eventsCount: 11,
  },
  {
    id: 'safavid_pilot',
    nameEn: 'Safavid Empire',
    nameFa: 'شاهنشاهی صفوی',
    periodDisplay: '1501 – 1736 CE',
    startYear: 1501,
    endYear: 1736,
    capitals: 'Tabriz, Qazvin, Isfahan',
    founder: 'Shah Ismail I',
    keyAchievementEn: 'Unification of Iran\'s sovereign borders, architectural apex of Naqsh-e Jahan, silk diplomacy.',
    keyAchievementFa: 'تجدید هویت و یکپارچگی ارضی ایران، شاهکار میدان نقش جهان اصفهان، هنر قالی و سرامیک.',
    notableMonarch: 'Shah Ismail I, Shah Abbas the Great',
    territoryExtent: 'Caucasus to Indus, Persian Gulf to Amu Darya',
    eventsCount: 15,
  },
  {
    id: 'qajar_pahlavi_modern',
    nameEn: 'Modern & Constitutional Era',
    nameFa: 'عصر مشروطه و دوران معاصر',
    periodDisplay: '1906 CE – Present',
    startYear: 1906,
    endYear: 2026,
    capitals: 'Tehran',
    founder: 'Constitutional Revolution Movement',
    keyAchievementEn: 'First constitutional parliament in Asia (1906), oil nationalization (1951), modern scientific institutes.',
    keyAchievementFa: 'انقلاب مشروطه و نخستین مجلس ملی آسیا (۱۹۰۶)، نهضت ملی شدن نفت، تاسیس دانشگاه تهران.',
    notableMonarch: 'Constitutional Assemblies & Modern State',
    territoryExtent: 'Modern recognized borders of the Islamic Republic of Iran (1,648,195 km²)',
    eventsCount: 18,
  },
];

// THEMATIC IRAN FACETS
export const IRAN_THEMATIC_PANELS: IranThematicFacet[] = [
  {
    id: 'inventions',
    titleEn: 'Engineering & Inventions',
    titleFa: 'ابداعات و نبوغ مهندسی',
    icon: 'Cpu',
    items: [
      {
        nameEn: 'Qanat Hydraulic Systems',
        nameFa: 'کاریز و فناوری حفر قنات',
        detailEn: 'Over 3,000 years of subterranean gravity aqueducts carrying snowmelt without evaporation loss across deserts.',
        detailFa: 'بیش از ۳۰۰۰ سال حفر قنات‌های زیرزمینی مهندسی‌شده برای انتقال آب شیرین از کوهپایه به دشت بدون تبخیر.',
        originPeriod: 'Early 1st Millennium BCE',
      },
      {
        nameEn: 'Windmills of Sistan (Asbads)',
        nameFa: 'آسبادهای کهن سیستان',
        detailEn: 'Vertical-axis windmills designed to harness the ferocious 120-day winds of Sistan to mill grain.',
        detailFa: 'نخستین آسیاب‌های بادی با محور عمودی جهان برای مهار بادهای معروف ۱۲۰ روزه سیستان و آرد کردن گندم.',
        originPeriod: '7th Century CE',
      },
      {
        nameEn: 'Yakhchal (Desert Ice Storage)',
        nameFa: 'یخچال‌های طبیعی کویری',
        detailEn: 'Domed adobe evaporative cooling structures that preserved winter ice and sorbets through blazing desert summers.',
        detailFa: 'سازه‌های خشتی مخروطی با سیستم سرمایش تبخیری شبانه برای نگهداری یخ زمستان در قلب تابستان کویر.',
        originPeriod: '400 BCE',
      },
      {
        nameEn: 'Chapar Khaneh (Royal Post)',
        nameFa: 'چاپارخانه (نخستین سیستم پست جهان)',
        detailEn: 'Staged relay stations with fresh horses every 25km enabling messages to travel 2,500km in under a week.',
        detailFa: 'ایستگاه‌های سوارکاری و اسب‌های تازه‌نفس هر ۲۵ کیلومتر که نامه را ظرف ۷ روز در سراسر شاهنشاهی می‌رساندند.',
        originPeriod: '550 BCE (Cyrus & Darius)',
      },
    ],
  },
  {
    id: 'language',
    titleEn: 'Linguistic Evolution',
    titleFa: 'سیر تطور زبان و خط در فلات',
    icon: 'BookOpen',
    items: [
      {
        nameEn: 'Old Persian & Cuneiform',
        nameFa: 'فارسی باستان و خط میخی',
        detailEn: 'Indo-Iranian tongue preserved on royal trilingual stone monuments at Bisotun, Persepolis, and Naqsh-e Rustam.',
        detailFa: 'زبان کتیبه‌های شاهی با الفبای میخی ابداعی ۳۶ نشانه‌ای داریوش در بیستون و تخت جمشید.',
        originPeriod: '6th – 4th Century BCE',
      },
      {
        nameEn: 'Avestan Sacred Language',
        nameFa: 'زبان اوستایی کهن',
        detailEn: 'Archaic Indo-European liturgical language in which the Gathas of Zarathustra and the Avesta were composed.',
        detailFa: 'زبان کهن دینی هم‌ریشه با سنسکریت وداها که سروده‌های گاهان زرتشت با آن سروده شده است.',
        originPeriod: '2nd Millennium BCE',
      },
      {
        nameEn: 'Middle Persian (Pahlavi)',
        nameFa: 'پارسی میانه (پهلوی ساسانی)',
        detailEn: 'The language of the Sasanian court, administration, and rich literature, using the Aramaic-derived Pahlavi script.',
        detailFa: 'زبان رسمی و اداری شاهنشاهی ساسانی با کتیبه‌ها و متون فلسفی، ادبی و دینی پندنامه‌ها.',
        originPeriod: '3rd Century BCE – 8th Century CE',
      },
      {
        nameEn: 'New Persian (Farsi-ye Dari)',
        nameFa: 'فارسی نو (دری) و شعر پارسی',
        detailEn: 'Perso-Arabic script literary renaissance producing the works of Ferdowsi, Hafez, Rumi, Saadi, and Khayyam.',
        detailFa: 'رنسانس ادبی خراسان و تولد شاهنامه فردوسی، غزلیات حافظ و سعدی و مثنوی مولانا که زبان شعر آسیا شد.',
        originPeriod: '9th Century CE – Present',
      },
    ],
  },
  {
    id: 'ecology',
    titleEn: 'Wildlife & Natural Flora',
    titleFa: 'اکولوژی، حیات وحش و گیاهان بومی',
    icon: 'Leaf',
    items: [
      {
        nameEn: 'Asiatic Cheetah (Yuzpalang)',
        nameFa: 'یوزپلنگ آسیایی (توران و دشت کویر)',
        detailEn: 'Critically endangered subspecies clinging to existence on the Iranian central plateau; fastest land animal in Asia.',
        detailFa: 'تنها بازماندگان یوزپلنگ در قاره آسیا که در پارک ملی توران و میاندشت زندگی می‌کنند.',
        originPeriod: 'Pleistocene to Present',
      },
      {
        nameEn: 'Persian Saffron & Pomegranate',
        nameFa: 'زعفران و انار اصیل ایرانی',
        detailEn: 'Crocus sativus domestic cultivation originating in the Zagros; Iran produces over 90% of global saffron supply.',
        detailFa: 'اهلی‌سازی و کشت چند هزار ساله طلای سرخ (زعفران) و انار که نماد برکت و زندگی در فرهنگ ایرانی است.',
        originPeriod: 'Neolithic to Present',
      },
      {
        nameEn: 'Hyrcanian Ancient Forests',
        nameFa: 'جنگل‌های باستانی هیرکانی (کاسپین)',
        detailEn: 'UNESCO World Heritage relic forests dating back 25 to 50 million years; survived the Ice Ages as a biological refuge.',
        detailFa: 'میراث طبیعی یونسکو و بازمانده عصر یخبندان به قدمت بیش از ۲۵ میلیون سال در کرانه جنوبی دریای کاسپین.',
        originPeriod: 'Tertiary Refugium',
      },
    ],
  },
];

// -------------------------------------------------------------
// 83 SCHOLARLY DATA SOURCES CATALOG (Sample Representative Data)
// -------------------------------------------------------------
export const SCHOLARLY_SOURCES_CATALOG: ScholarlySourceRecord[] = [
  {
    id: 'earthbyte',
    name: 'EarthByte Plate Tectonic Reconstructions (GPlates)',
    domain: 'Tectonics',
    domainFa: 'زمین‌ساخت و بازسازی قاره‌ها',
    leadInstitution: 'University of Sydney & Caltech',
    coverage: '1,000 Ma → Present day continental grids',
    license: 'CC-BY-4.0',
    confidenceLevel: 'Very High',
    notesEn: 'Continuous digital paleomaps integrating seafloor magnetic anomalies and paleomagnetism.',
    notesFa: 'مدل‌های پیوسته حرکت صفحات تکتونیکی مبتنی بر ناهنجاری‌های مغناطیسی بستر دریا و دیرینه‌مغناطیس.',
    doiOrUrl: 'https://www.earthbyte.org/',
  },
  {
    id: 'pbdb',
    name: 'Paleobiology Database (PBDB)',
    domain: 'Paleobiology',
    domainFa: 'دیرینه‌زیست‌شناسی و فسیل‌ها',
    leadInstitution: 'International Consortium (University of Wisconsin–Madison)',
    coverage: 'Phanerozoic fossil occurrence records (450,000+ collections)',
    license: 'CC-BY-4.0',
    confidenceLevel: 'Very High',
    notesEn: 'Global scientific occurrences of taxonomic clades with stratigraphic age constraints.',
    notesFa: 'کامل‌ترین پایگاه ثبت فسیل‌های کره زمین با تخمین سن چینه‌شناسی و بازسازی دوره‌های انقراض.',
    doiOrUrl: 'https://paleobiodb.org/',
  },
  {
    id: 'hyde',
    name: 'HYDE 3.2 (History Database of the Global Environment)',
    domain: 'Archaeology',
    domainFa: 'جمعیت‌شناسی تاریخی و کاربری اراضی',
    leadInstitution: 'PBL Netherlands Environmental Assessment Agency',
    coverage: '10,000 BCE → 2020 CE at 5 arc-minute resolution',
    license: 'CC-BY-4.0',
    confidenceLevel: 'High',
    notesEn: 'Spatially explicit historical human population counts and agricultural cropland expansion.',
    notesFa: 'برآورد تاریخی تراکم جمعیت بشر و گسترش زمین‌های کشاورزی از دوران نوسنگی تا امروز.',
    doiOrUrl: 'https://www.pbl.nl/hyde',
  },
  {
    id: 'pleiades',
    name: 'Pleiades Gazetteer of Ancient Places',
    domain: 'Archaeology',
    domainFa: 'جغرافیای تاریخی و شهرهای باستانی',
    leadInstitution: 'Institute for the Study of the Ancient World (NYU) & Stoa Consortium',
    coverage: '35,000+ ancient settlements and landmarks across Afro-Eurasia',
    license: 'CC-BY-3.0',
    confidenceLevel: 'Very High',
    notesEn: 'Definitive geospatial coordinate database for antiquity places, settlements, and borders.',
    notesFa: 'مختصات دقیق و نام‌های باستانی سکونتگاه‌های کهن خاورمیانه، مدیترانه و آسیای مرکزی.',
    doiOrUrl: 'https://pleiades.stoa.org/',
  },
  {
    id: 'macrostrat',
    name: 'Macrostrat Geologic Engine',
    domain: 'Paleoclimatology',
    domainFa: 'چینه‌شناسی و لایه‌های زمین',
    leadInstitution: 'University of Wisconsin Geological Survey',
    coverage: 'Global rock columns, lithology, and chronostratigraphy',
    license: 'CC-BY-4.0',
    confidenceLevel: 'High',
    notesEn: 'Maps geological formations and lithological facies across geologic eras.',
    notesFa: 'اطلس لایه‌های سنگی و رسوبی کره زمین و انطباق با تغییرات سطح آب دریاها.',
    doiOrUrl: 'https://macrostrat.org/',
  },
  {
    id: 'gvp',
    name: 'Global Volcanism Program (Holocene & Large Igneous Provinces)',
    domain: 'Tectonics',
    domainFa: 'آتشفشان‌شناسی و تله‌های بازالتی',
    leadInstitution: 'Smithsonian Institution',
    coverage: 'All documented volcanic eruptions, flood basalts, and VEI ratings',
    license: 'Public Domain',
    confidenceLevel: 'Very High',
    notesEn: 'Eruption catalogs tying volcanic SO2 and CO2 aerosol pulses to mass extinction horizons.',
    notesFa: 'کاتالوگ جامع فوران‌های آتشفشانی و انطباق پالس‌های گوگرد و دی‌اکسید کربن با انقراض‌ها.',
    doiOrUrl: 'https://volcano.si.edu/',
  },
  {
    id: 'unesco_heritage',
    name: 'UNESCO World Heritage Geospatial Inventory',
    domain: 'Archaeology',
    domainFa: 'میراث جهانی باستان‌شناسی',
    leadInstitution: 'UNESCO World Heritage Centre',
    coverage: '1,199 cultural and natural monuments with spatial boundaries',
    license: 'Academic Open Access',
    confidenceLevel: 'Very High',
    notesEn: 'Preservation status, architectural documentation, and legal boundaries of heritage sites.',
    notesFa: 'مستندات معماری، مرزهای حریم تاریخی و ارزیابی ارزش‌های جهانی آثار باستانی.',
    doiOrUrl: 'https://whc.unesco.org/',
  },
];
