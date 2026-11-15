// Thematic Map & Geo-Chronicle Data Engine
// Structured for Iran & World across deep civilizational time

export type ThemeType = 'civilization' | 'fauna' | 'religion' | 'literature' | 'art' | 'music';

export interface ThemeConfig {
  id: ThemeType;
  nameFa: string;
  nameEn: string;
  iconName: string;
  accentColor: string; // Hex for Tailwind & SVG
  bgTint: string;
  borderTint: string;
  badgeBg: string;
  badgeText: string;
  descriptionFa: string;
  descriptionEn: string;
}

export const THEME_CONFIGS: Record<ThemeType, ThemeConfig> = {
  civilization: {
    id: 'civilization',
    nameFa: 'تمدن‌ها و حکومت‌ها',
    nameEn: 'Civilizations & Empires',
    iconName: 'Landmark',
    accentColor: '#F59E0B', // Amber / Royal Gold
    bgTint: 'bg-amber-500/10',
    borderTint: 'border-amber-500/30',
    badgeBg: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
    badgeText: 'text-amber-400',
    descriptionFa: 'قلمروهای سرزمینی، پایتخت‌ها و مرزهای متغیر تمدن‌ها در گذر زمان',
    descriptionEn: 'Territorial boundaries, capitals, and changing empire frontiers',
  },
  fauna: {
    id: 'fauna',
    nameFa: 'حیات‌وحش و جانوران',
    nameEn: 'Historic Fauna & Wildlife',
    iconName: 'Cat',
    accentColor: '#10B981', // Emerald / Nature Green
    bgTint: 'bg-emerald-500/10',
    borderTint: 'border-emerald-500/30',
    badgeBg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
    badgeText: 'text-emerald-400',
    descriptionFa: 'زیستگاه و پراکندگی جانوران تاریخی و کهن در فلات ایران و جهان',
    descriptionEn: 'Habitats of prehistoric and historical wildlife across regions',
  },
  religion: {
    id: 'religion',
    nameFa: 'ادیان، باورها و آیین‌ها',
    nameEn: 'Religions & Philosophies',
    iconName: 'Flame',
    accentColor: '#8B5CF6', // Purple / Mystic Violet
    bgTint: 'bg-purple-500/10',
    borderTint: 'border-purple-500/30',
    badgeBg: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
    badgeText: 'text-purple-400',
    descriptionFa: 'مراکز پیدایش و گسترش آیین‌ها، ادیان و مکاتب فکری در فلات و جهان',
    descriptionEn: 'Spiritual origins, temples, and philosophical traditions',
  },
  literature: {
    id: 'literature',
    nameFa: 'شاعران و نویسندگان',
    nameEn: 'Poets & Literature',
    iconName: 'BookOpen',
    accentColor: '#06B6D4', // Cyan / Sky Blue
    bgTint: 'bg-cyan-500/10',
    borderTint: 'border-cyan-500/30',
    badgeBg: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
    badgeText: 'text-cyan-400',
    descriptionFa: 'شاعران، نویسندگان، حکما و ادیبان هم‌عصر در شهرهای ایران و جهان',
    descriptionEn: 'Contemporary poets, philosophers, and writers across historical cities',
  },
  art: {
    id: 'art',
    nameFa: 'هنر، نگارگری و معماری',
    nameEn: 'Art & Painting & Architecture',
    iconName: 'Palette',
    accentColor: '#F43F5E', // Coral / Rose Carmine
    bgTint: 'bg-rose-500/10',
    borderTint: 'border-rose-500/30',
    badgeBg: 'bg-rose-500/20 text-rose-300 border-rose-500/40',
    badgeText: 'text-rose-400',
    descriptionFa: 'مکاتب نگارگری، معماری بناها، مفرغ‌ها و شاهکارهای هنری هر دوره',
    descriptionEn: 'Art schools, miniature ateliers, and monumental architecture',
  },
  music: {
    id: 'music',
    nameFa: 'موسیقی، سازها و نواها',
    nameEn: 'Music, Modes & Instruments',
    iconName: 'Music',
    accentColor: '#EAB308', // Warm Golden Yellow
    bgTint: 'bg-yellow-500/10',
    borderTint: 'border-yellow-500/30',
    badgeBg: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40',
    badgeText: 'text-yellow-400',
    descriptionFa: 'موسیقی‌دانان بزرگ، پیدایش سازهای باستانی و پرده‌ها و دستگاه‌ها',
    descriptionEn: 'Ancient musical instruments, court masters, and melodic systems',
  },
};

// Projected Map Entities
export interface ThematicEntity {
  id: string;
  theme: ThemeType;
  nameFa: string;
  nameEn: string;
  titleOrSubtitleFa: string;
  titleOrSubtitleEn: string;
  startYear: number; // e.g. -550 for 550 BCE, +1200 for 1200 CE
  endYear: number;   // e.g. -330 for 330 BCE, +1290 for 1290 CE
  periodLabelFa: string;
  periodLabelEn: string;
  // Normalized Map Coordinates (0 to 1000 width, 0 to 600 height)
  // Centered on Iranian Plateau (approx x: 480-620, y: 220-360)
  mapCoord: { x: number; y: number; regionNameFa: string; regionNameEn: string };
  summaryFa: string;
  summaryEn: string;
  detailsFa: {
    description: string;
    keyAchievements: string[];
    contemporaryEventsFa: string;
    quoteOrTextFa?: string;
  };
  detailsEn: {
    description: string;
    keyAchievements: string[];
    contemporaryEventsEn: string;
    quoteOrTextEn?: string;
  };
  // Optional territorial border SVG path if this entity represents a kingdom/empire
  territoryPolygon?: string;
}

// Major Historical Epochs for Boundary Shifts
export interface BoundaryEpoch {
  id: string;
  nameFa: string;
  nameEn: string;
  startYear: number;
  endYear: number;
  descriptionFa: string;
  descriptionEn: string;
  empiresActive: string[];
  // SVG paths for territorial boundaries during this epoch
  territories: {
    empireId: string;
    empireNameFa: string;
    empireNameEn: string;
    fillColor: string;
    path: string;
  }[];
}

// SVG Territories for Historical Epochs
export const HISTORICAL_BOUNDARY_EPOCHS: BoundaryEpoch[] = [
  {
    id: 'early_bronze',
    nameFa: 'عصر مفرغ و نخستین دولت‌شهرها (عیلام و جیرفت)',
    nameEn: 'Early Bronze Age (Elam, Jiroft & Sumer)',
    startYear: -3200,
    endYear: -1200,
    descriptionFa: 'پیدایش تمدن عیلام در شوش و انشان، تمدن کهن ارت/جیرفت در جنوب شرق، شهر سوخته و دولت‌شهرهای سومر و اکد.',
    descriptionEn: 'Emergence of Elamite civilization in Susa and Anshan, the Jiroft culture, and Sumerian city-states.',
    empiresActive: ['elam', 'jiroft', 'sumer', 'shahr_e_sukhteh'],
    territories: [
      {
        empireId: 'elam',
        empireNameFa: 'پادشاهی کهن عیلام',
        empireNameEn: 'Elamite Kingdom',
        fillColor: '#F59E0B',
        path: 'M 440,290 Q 480,270 520,310 Q 500,360 450,340 Z',
      },
      {
        empireId: 'jiroft',
        empireNameFa: 'تمدن هلیل‌رود (جیرفت)',
        empireNameEn: 'Jiroft Civilization',
        fillColor: '#10B981',
        path: 'M 540,330 Q 590,320 610,360 Q 570,390 530,360 Z',
      },
      {
        empireId: 'sumer',
        empireNameFa: 'دولت‌شهرهای سومر و اکد',
        empireNameEn: 'Sumer & Akkad',
        fillColor: '#8B5CF6',
        path: 'M 380,280 Q 420,270 430,310 Q 390,330 370,300 Z',
      },
    ],
  },
  {
    id: 'iron_medes',
    nameFa: 'عصر آهن و اتحاد مادها',
    nameEn: 'Iron Age & Median Confederation',
    startYear: -850,
    endYear: -550,
    descriptionFa: 'اتحاد قبایل ایرانی در زاگرس و تشکیل شاهنشاهی ماد با پایتختی هگمتانه، هم‌زمان با امپراتوری آشور و بابل نو.',
    descriptionEn: 'Unification of Iranic tribes under the Median Empire based in Ecbatana, alongside Neo-Assyria and Babylonia.',
    empiresActive: ['medes', 'assyria', 'babylon', 'mannaea'],
    territories: [
      {
        empireId: 'medes',
        empireNameFa: 'شاهنشاهی ماد (اکباتان)',
        empireNameEn: 'Median Empire',
        fillColor: '#F59E0B',
        path: 'M 400,220 Q 530,190 620,240 Q 580,330 460,320 Q 410,270 400,220 Z',
      },
      {
        empireId: 'babylon',
        empireNameFa: 'امپراتوری بابل نو',
        empireNameEn: 'Neo-Babylonian Empire',
        fillColor: '#06B6D4',
        path: 'M 320,260 Q 390,250 400,320 Q 340,350 310,300 Z',
      },
    ],
  },
  {
    id: 'achaemenid',
    nameFa: 'شاهنشاهی هخامنشی (بزرگ‌ترین قلمرو جهان باستان)',
    nameEn: 'Achaemenid Persian Empire',
    startYear: -550,
    endYear: -330,
    descriptionFa: 'گستره از دره سند تا دانوب و مصر با منشور کوروش، راه شاهی، چاپارخانه و پایتخت‌های پاسارگاد، شوش و پارسه.',
    descriptionEn: 'From Indus to Danube and Nile: Cyrus Cylinder, the Royal Road, Persepolis and universal tolerance.',
    empiresActive: ['achaemenid', 'greece', 'carthage'],
    territories: [
      {
        empireId: 'achaemenid',
        empireNameFa: 'شاهنشاهی هخامنشیان',
        empireNameEn: 'Achaemenid Empire',
        fillColor: '#F59E0B',
        path: 'M 260,200 Q 420,150 710,230 Q 730,340 590,390 Q 430,380 340,320 Q 280,310 250,260 Z',
      },
    ],
  },
  {
    id: 'parthian_sasanian',
    nameFa: 'اشکانیان و ساسانیان (دوران هماوردی با روم)',
    nameEn: 'Parthian & Sasanian Empires',
    startYear: -247,
    endYear: 651,
    descriptionFa: 'حاکمیت اشکانیان (پارتیان) و احیای سنن ایرانی با شاهنشاهی ساسانی، پایتختی تیسفون و ایوان کسری و رقابت با روم.',
    descriptionEn: 'Arsacid Parthians and Sasanian revival; Ctesiphon Arch, Gundeshapur academy, and dual superpower rivalry with Rome.',
    empiresActive: ['sasanian', 'rome_byzantium', 'kushan'],
    territories: [
      {
        empireId: 'sasanian',
        empireNameFa: 'شاهنشاهی ساسانی (ایران‌شهر)',
        empireNameEn: 'Sasanian Empire (Iranshahr)',
        fillColor: '#F59E0B',
        path: 'M 350,190 Q 520,170 690,240 Q 670,360 520,380 Q 410,360 350,260 Z',
      },
      {
        empireId: 'rome_byzantium',
        empireNameFa: 'امپراتوری روم و بیزانس',
        empireNameEn: 'Roman / Byzantine Empire',
        fillColor: '#F43F5E',
        path: 'M 140,160 Q 300,170 330,260 Q 240,310 160,260 Z',
      },
    ],
  },
  {
    id: 'islamic_renaissance',
    nameFa: 'عصر زرین دانش و دولت‌های محلی ایران',
    nameEn: 'Islamic Golden Age & Persian Intermezzo',
    startYear: 750,
    endYear: 1220,
    descriptionFa: 'شکوفایی علوم با سامانیان در بخارا، آل بویه در ری و شیراز، غزنویان و سلجوقیان با حضور ابن سینا، بیرونی، فردوسی و خیام.',
    descriptionEn: 'Samanids, Buyids, and Seljuks; flourishing of astronomy, philosophy, and classical Persian literature.',
    empiresActive: ['samanids', 'buyids', 'seljuks', 'song_dynasty'],
    territories: [
      {
        empireId: 'seljuks',
        empireNameFa: 'امپراتوری سلجوقی',
        empireNameEn: 'Great Seljuk Empire',
        fillColor: '#06B6D4',
        path: 'M 310,190 Q 520,160 680,220 Q 640,350 480,360 Q 360,330 300,260 Z',
      },
    ],
  },
  {
    id: 'safavid_era',
    nameFa: 'عصر صفوی و احیای دولت متمرکز',
    nameEn: 'Safavid Dynasty & Early Modern Era',
    startYear: 1501,
    endYear: 1736,
    descriptionFa: 'تشکیل دولت یکپارچه صفوی با پایتختی اصفهان نصف جهان، شکوفایی مکتب نگارگری، معماری نقش جهان، هم‌زمان با گورکانیان هند و عثمانی.',
    descriptionEn: 'Safavid reunification under Shah Abbas I, Isfahan as cultural capital, alongside Ottomans and Mughal India.',
    empiresActive: ['safavid', 'ottoman', 'mughal'],
    territories: [
      {
        empireId: 'safavid',
        empireNameFa: 'شاهنشاهی صفویه',
        empireNameEn: 'Safavid Empire',
        fillColor: '#F59E0B',
        path: 'M 400,210 Q 560,190 660,250 Q 640,360 510,380 Q 420,350 390,280 Z',
      },
      {
        empireId: 'ottoman',
        empireNameFa: 'امپراتوری عثمانی',
        empireNameEn: 'Ottoman Empire',
        fillColor: '#8B5CF6',
        path: 'M 220,180 Q 370,190 380,290 Q 280,340 210,260 Z',
      },
      {
        empireId: 'mughal',
        empireNameFa: 'گورکانیان هند (مغول کبیر)',
        empireNameEn: 'Mughal Empire',
        fillColor: '#10B981',
        path: 'M 670,260 Q 780,270 790,390 Q 710,410 660,350 Z',
      },
    ],
  },
];

// Rich Curated Thematic Entities across all 6 Themes
export const THEMATIC_ENTITIES: ThematicEntity[] = [
  // ==================== 1. CIVILIZATIONS & EMPIRES ====================
  {
    id: 'civ_elam',
    theme: 'civilization',
    nameFa: 'تمدن عیلام (پادشاهی شوش و انشان)',
    nameEn: 'Elamite Civilization',
    titleOrSubtitleFa: 'کهن‌ترین تمدن ثبت‌شده فلات ایران',
    titleOrSubtitleEn: 'Earliest Recorded Plateau Civilization',
    startYear: -3200,
    endYear: -539,
    periodLabelFa: '۳۲۰۰ تا ۵۳۹ پیش از میلاد',
    periodLabelEn: '3200 - 539 BCE',
    mapCoord: { x: 460, y: 310, regionNameFa: 'شوش، خوزستان و ایلام', regionNameEn: 'Susa & Khuzestan' },
    summaryFa: 'بنیان‌گذار شهرنشینی، زیگورات چغازنبیل و خط عیلامی خطی در جنوب‌غرب فلات ایران.',
    summaryEn: 'Founders of urban civilization in SW Iran, builders of the Chogha Zanbil ziggurat.',
    detailsFa: {
      description: 'تمدن عیلام یکی از قدیمی‌ترین تمدن‌های بشری است که از دره شوش تا کوه‌های انشان (فارس امروزی) گسترده بود. اثر سترگ زیگورات چغازنبیل نماد اوج معماری مذهبی این پادشاهی در هزاره دوم پیش از میلاد است.',
      keyAchievements: ['ساخت زیگورات چغازنبیل با سیستم تصفیه آب کهن', 'اختراع خط پیشاعیلامی و عیلامی میخی', 'فلزکاری مفرغی و سفالینه‌های منقوش شوش'],
      contemporaryEventsFa: 'هم‌عصر با تمدن‌های سومر، بابل باستان و دودمان‌های کهن مصر.',
    },
    detailsEn: {
      description: 'Elam was one of the earliest high cultures of the Near East, forming the bedrock of Iranian civilization.',
      keyAchievements: ['Construction of Chogha Zanbil with early hydraulic filtration', 'Proto-Elamite and Linear Elamite writing systems', 'Mastery of metallurgy and glazed bricks'],
      contemporaryEventsEn: 'Contemporary with Sumer, Old Babylon, and Old Kingdom Egypt.',
    },
  },
  {
    id: 'civ_achaemenid',
    theme: 'civilization',
    nameFa: 'شاهنشاهی هخامنشی',
    nameEn: 'Achaemenid Persian Empire',
    titleOrSubtitleFa: 'پاسارگاد و تخت جمشید · کوروش و داریوش بزرگ',
    titleOrSubtitleEn: 'Persepolis & Cyrus the Great',
    startYear: -550,
    endYear: -330,
    periodLabelFa: '۵۵۰ تا ۳۳۰ پیش از میلاد',
    periodLabelEn: '550 - 330 BCE',
    mapCoord: { x: 530, y: 340, regionNameFa: 'پارسه (تخت جمشید) و پاسارگاد، فارس', regionNameEn: 'Persepolis, Fars' },
    summaryFa: 'نخستین ابرقدرت جهانی با منشور حقوق بشر کوروش، ساتراپی‌ها و راه شاهی از شوش تا سارد.',
    summaryEn: 'First global empire unifying the civilized world with institutional tolerance.',
    detailsFa: {
      description: 'بنیان‌گذاری شده توسط کوروش بزرگ با صدور منشور استوانه کوروش. اداره قلمرو پهناور از طریق نظام ساتراپی، ایجاد پست پیشرفته چاپارخانه، پول واحد دریک و معماری باشکوه آپادانا در تخت جمشید.',
      keyAchievements: ['استوانه حقوق بشر کوروش در بابل', 'ساخت تخت جمشید و سیستم کانال سوئز داریوش', 'تاسیس نخستین شبکه پست سراسری (چاپارخانه) و راه شاهی'],
      contemporaryEventsFa: 'هم‌عصر با عصر طلایی یونان باستان (آتن و اسپارت)، پادشاهی روم اولیه و عصر ماهاجاناپاداها در هند.',
    },
    detailsEn: {
      description: 'Founded by Cyrus the Great, establishing Pax Persica spanning three continents.',
      keyAchievements: ['Cyrus Cylinder legal proclamation', 'Persepolis ceremonial complex', 'Royal Road postal courier infrastructure'],
      contemporaryEventsEn: 'Contemporary with Classical Athens, early Roman Republic, and Buddha in India.',
    },
  },
  {
    id: 'civ_sasanian',
    theme: 'civilization',
    nameFa: 'شاهنشاهی ساسانی (ایران‌شهر)',
    nameEn: 'Sasanian Empire',
    titleOrSubtitleFa: 'تیسفون، ایوان کسری و دانشگاه گندی‌شاپور',
    titleOrSubtitleEn: 'Ctesiphon & Academy of Gundeshapur',
    startYear: 224,
    endYear: 651,
    periodLabelFa: '۲۲۴ تا ۶۵۱ میلادی',
    periodLabelEn: '224 - 651 CE',
    mapCoord: { x: 420, y: 290, regionNameFa: 'تیسفون و خوزستان (گندی‌شاپور)', regionNameEn: 'Ctesiphon & Khuzestan' },
    summaryFa: 'احیاگر هویت ملی ایران، قطب دانش جهان با دانشگاه گندی‌شاپور و هماورد اصلی امپراتوری روم و بیزانس.',
    summaryEn: 'Last pre-Islamic Iranian empire, home to Gundeshapur medical academy and rival to Rome.',
    detailsFa: {
      description: 'ساسانیان با اردشیر بابکان آغاز و با شاپور و خسرو انوشیروان به اوج رسید. دانشگاه گندی‌شاپور بزرگ‌ترین مرکز پزشکی و ترجمه متون علمی یونانی، هندی و پهلوی در عصر باستان بود.',
      keyAchievements: ['دانشگاه و بیمارستان آموزشی گندی‌شاپور', 'طاق کسری با دهانه‌ای ۲۵ متری بدون ستون', 'کتاب پهلوی خدای‌نامگ و ترجمه کلیله و دمنه'],
      contemporaryEventsFa: 'هم‌عصر با امپراتوری روم شرقی (بیزانس) و دودمان گوپتا در هند.',
    },
    detailsEn: {
      description: 'A cultural zenith codifying Avestan texts and housing international scholars.',
      keyAchievements: ['Gundeshapur medical university', 'Arch of Ctesiphon vault masonry', 'Translation of Indian and Greek scientific treatises'],
      contemporaryEventsEn: 'Contemporary with the Byzantine Empire and Gupta Empire in India.',
    },
  },
  {
    id: 'civ_safavid',
    theme: 'civilization',
    nameFa: 'شاهنشاهی صفویه',
    nameEn: 'Safavid Dynasty',
    titleOrSubtitleFa: 'اصفهان نصف جهان · شاه عباس بزرگ',
    titleOrSubtitleEn: 'Isfahan Cultural Capital & Shah Abbas',
    startYear: 1501,
    endYear: 1736,
    periodLabelFa: '۱۵۰۱ تا ۱۷۳۶ میلادی',
    periodLabelEn: '1501 - 1736 CE',
    mapCoord: { x: 510, y: 290, regionNameFa: 'اصفهان، فلات مرکزی', regionNameEn: 'Isfahan, Central Plateau' },
    summaryFa: 'یکپارچه‌سازی جغرافیایی ایران پس از قرن‌ها، شکوفایی شاهکارهای معماری میدان نقش جهان و مکتب هنری اصفهان.',
    summaryEn: 'Reunification of Iran, establishing modern sovereign borders and architectural wonders.',
    detailsFa: {
      description: 'با شاه اسماعیل اول در تبریز پایه‌گذاری شد و در زمان شاه عباس اول با پایتختی اصفهان به یکی از باشکوه‌ترین تمدن‌های دوران مدرن اولیه بدل گشت. احداث ۹۹۹ کاروانسرا در مسیرهای تجاری ابریشم.',
      keyAchievements: ['میدان نقش جهان، مسجد شیخ لطف‌الله و کاخ عالی‌قاپو', 'شبکه کاروانسراهای شاه‌عباسی', 'توسعه صنعت بافت فرش، کاشی‌کاری معرق و ابریشم'],
      contemporaryEventsFa: 'هم‌عصر با امپراتوری عثمانی در استانبول، گورکانیان (مغولان هند) و دوره رنسانس پسین در اروپا.',
    },
    detailsEn: {
      description: 'The renaissance of unified Iranian statehood and cosmopolitan diplomacy.',
      keyAchievements: ['Naqsh-e Jahan Square complex', 'Silk trade commercial revitalization', 'Golden age of Persian carpet and tile crafts'],
      contemporaryEventsEn: 'Contemporary with the Ottoman Empire, Mughal India, and Elizabethan England.',
    },
  },

  // ==================== 2. FAUNA & PREHISTORIC ANIMALS ====================
  {
    id: 'fauna_persian_lion',
    theme: 'fauna',
    nameFa: 'شیر ایرانی (Panthera leo persica)',
    nameEn: 'Asiatic / Persian Lion',
    titleOrSubtitleFa: 'نماد باستانی قدرت و شکوه فلات ایران',
    titleOrSubtitleEn: 'Historical King of the Plateau Woodlands',
    startYear: -5000,
    endYear: 1942,
    periodLabelFa: 'از باستان تا اوایل قرن بیستم میلادی',
    periodLabelEn: 'Ancient times to early 20th century',
    mapCoord: { x: 480, y: 330, regionNameFa: 'بیشه‌زارهای خوزستان، فارس و زاگرس جنوبی', regionNameEn: 'Khuzestan & Fars Woodlands' },
    summaryFa: 'زیستگاه تاریخی در دشت ارژن فارس و کرانه‌های کارون؛ نقش‌مایه برجسته در نقوش تخت جمشید.',
    summaryEn: 'Native to oak forests of Fars and reedbeds of Karun; immortalized on Persepolis reliefs.',
    detailsFa: {
      description: 'شیر ایرانی تا اواخر دوران قاجار و پهلوی اول در نیزارهای کارون و کرخه و جنگل‌های بلوط دشت ارژن فارس می‌زیست. این جانور در نمادهای سلطنتی، پرچم کهن و هنر هخامنشی نقشی بنیادین داشت.',
      keyAchievements: ['زیستگاه بومی در دشت ارژن و کامفیروز فارس', 'الهام‌بخش کتیبه‌های هخامنشی و نقوش شیر و خورشید', 'واپسین گزارش مستند در سال ۱۳۲۱ خورشیدی در دزفول'],
      contemporaryEventsFa: 'هم‌زیستی با تمدن‌های عیلام، هخامنشی تا دوران معاصر در زاگرس.',
    },
    detailsEn: {
      description: 'The historic predator of Iranian savannahs and oak scrublands.',
      keyAchievements: ['Key motif on Apadana palace friezes', 'Historic presence across Zagros piedmont', 'Extirpated in Iran around mid-20th century'],
      contemporaryEventsEn: 'Contemporary with all major dynasties from Elam to Qajar.',
    },
  },
  {
    id: 'fauna_caspian_tiger',
    theme: 'fauna',
    nameFa: 'ببر مازندران / هیرکانی (Panthera tigris virgata)',
    nameEn: 'Caspian Tiger (Mazandaran)',
    titleOrSubtitleFa: 'غول باشکوه جنگل‌های بارانی هیرکانی',
    titleOrSubtitleEn: 'Regal Predator of Hyrcanian Rainforests',
    startYear: -8000,
    endYear: 1958,
    periodLabelFa: 'از دوران نوسنگی تا دهه ۱۹۵۰ میلادی',
    periodLabelEn: 'Neolithic to 1950s CE',
    mapCoord: { x: 510, y: 210, regionNameFa: 'جنگل‌های هیرکانی، گلستان، مازندران و گیلان', regionNameEn: 'Hyrcanian Forests, North Iran' },
    summaryFa: 'یکی از بزرگ‌ترین گربه‌سانان تاریخ؛ زیستگاه در متراکم‌ترین جنگل‌های جنوب دریای کاسپین.',
    summaryEn: 'One of the largest felids, roaming ancient temperate rainforests of Caspian shore.',
    detailsFa: {
      description: 'ببر مازندران (ببر تورانی) با یال ضخیم‌تر و بدنی تنومند، ارباب جنگل‌های بارانی هیرکانی بود. در شاهنامه فردوسی بارها به نبرد رستم با ببر بیان و ببر مازندران اشاره شده است.',
      keyAchievements: ['سازگاری با پوشش گیاهی کهن هیرکانی (فسیل زنده دوران سوم زمین‌شناسی)', 'الهام‌بخش ادبیات حماسی و نقاشی‌های مینیاتور', 'ثبت واپسین مشاهده در پارک ملی گلستان در سال ۱۳۳۷'],
      contemporaryEventsFa: 'شاهد تحولات اقوام کاسپی، کادوسی، تپورها و علویان طبرستان.',
    },
    detailsEn: {
      description: 'Dense-coated apex predator endemic to the Caspian shoreline.',
      keyAchievements: ['Adapted to Pleistocene relict Hyrcanian temperate forests', 'Prominently featured in Ferdowsi\'s epic Shahnameh', 'Declared extinct in late 1950s'],
      contemporaryEventsEn: 'Roamed alongside ancient Caspian tribes and Tabaristan principalities.',
    },
  },
  {
    id: 'fauna_asiatic_cheetah',
    theme: 'fauna',
    nameFa: 'یوزپلنگ آسیایی (Acinonyx jubatus venaticus)',
    nameEn: 'Asiatic Cheetah (Iranian Cheetah)',
    titleOrSubtitleFa: 'سریع‌ترین دونده خشکی · آخرین پناهگاه: کویر مرکزی ایران',
    titleOrSubtitleEn: 'Fastest Terrestrial Animal · Sole Refuge in Iran',
    startYear: -10000,
    endYear: 2026,
    periodLabelFa: 'از کهن‌ترین دوران تا عصر حاضر (در معرض خطر)',
    periodLabelEn: 'Prehistoric to Present (Critically Endangered)',
    mapCoord: { x: 570, y: 270, regionNameFa: 'دشت کویر، توران سمنان و یزد', regionNameEn: 'Dasht-e Kavir & Touran Biosphere' },
    summaryFa: 'ایران آخرین زیستگاه بازمانده این گربه‌سان شگفت‌انگیز در تمام قاره آسیا است.',
    summaryEn: 'Iran remains the very last habitat on Earth preserving this Asiatic subspecies.',
    detailsFa: {
      description: 'یوزپلنگ آسیایی زمانی از هند تا خاورمیانه و شمال آفریقا می‌دوید. امروزه تنها چند ده فرد در پناهگاه حیات‌وحش میاندشت و ذخیره‌گاه زیست‌کره توران در ایران نفس می‌کشند.',
      keyAchievements: ['سرعت شتاب تا ۱۰۰ کیلومتر در ساعت در دشت‌های استپی', 'دوران تربیت در دربار شاهان باستان برای شکار غزال', 'تلاش‌های بین‌المللی برای تکثیر و احیا نظیر پروژه یوز ایرانی (پیروز)'],
      contemporaryEventsFa: 'شاهد تمدن‌های کویری سیلک، یزد، جندق و شهر سوخته.',
    },
    detailsEn: {
      description: 'The emblem of wildlife conservation in the Middle East.',
      keyAchievements: ['Sprint velocity exceeding 100 km/h on open plains', 'Trained as royal hunting companions in antiquity', 'Currently conserved in Touran and Miandasht reserves'],
      contemporaryEventsEn: 'Contemporary with human habitation from ancient Sialk to modern day.',
    },
  },
  {
    id: 'fauna_persian_onager',
    theme: 'fauna',
    nameFa: 'گورخر ایرانی (Equus hemionus onager)',
    nameEn: 'Persian Onager (Wild Ass)',
    titleOrSubtitleFa: 'دونده چالاک استپ‌های طلایی کویر',
    titleOrSubtitleEn: 'Swift Wild Equid of the Salt Steppes',
    startYear: -12000,
    endYear: 2026,
    periodLabelFa: 'از پیشاتاریخ تا کنون',
    periodLabelEn: 'Prehistoric to Present',
    mapCoord: { x: 550, y: 310, regionNameFa: 'بهرام گور، فارس و پارک ملی کویر', regionNameEn: 'Bahram Gur Sanctuary, Fars' },
    summaryFa: 'قهرمان داستان‌های شکار بهرام پنجم (بهرام گور ساسانی) و بومی استپ‌های نمکی ایران.',
    summaryEn: 'Celebrated in Persian lore regarding King Bahram V (Bahram Gur).',
    detailsFa: {
      description: 'گورخر ایرانی یکی از تیزپاترین و سرسخت‌ترین علف‌خواران بیابانی جهان است که توانایی تحمل شرایط فوق‌العاده خشک و آب‌های شور فلات را دارد.',
      keyAchievements: ['سازگاری فیزیولوژیک با شوری بالای آب کویر', 'موضوع داستان‌ها و منظومه‌های هفت‌پیکر نظامی', 'حفاظت‌شده در ذخیره‌گاه بهرام گور فارس'],
      contemporaryEventsFa: 'هم‌عصر با فرهنگ‌های پیشاتاریخی فلات و دوران ساسانی.',
    },
    detailsEn: {
      description: 'Hardy desert equid adapted to extreme aridity.',
      keyAchievements: ['Survives on hyper-saline desert forage', 'Immortalized in Nizami\'s Haft Paykar', 'Protected in Bahram Gur protected area'],
      contemporaryEventsEn: 'Contemporary with Sasanian and Islamic royal hunting preserves.',
    },
  },

  // ==================== 3. RELIGIONS & PHILOSOPHIES ====================
  {
    id: 'rel_zoroastrianism',
    theme: 'religion',
    nameFa: 'آیین زرتشتی و مزدیسنا',
    nameEn: 'Zoroastrianism (Mazdayasna)',
    titleOrSubtitleFa: 'اندیشه نیک، گفتار نیک، کردار نیک · آتشکده آذرگشنسپ',
    titleOrSubtitleEn: 'Good Thoughts, Good Words, Good Deeds',
    startYear: -1200,
    endYear: 2026,
    periodLabelFa: 'هزاره دوم پیش از میلاد تا کنون',
    periodLabelEn: '2nd Millennium BCE to Present',
    mapCoord: { x: 470, y: 220, regionNameFa: 'تخت سلیمان (آذربایجان) و بلخ کهن', regionNameEn: 'Takht-e Soleyman & Bactria' },
    summaryFa: 'یکی از کهن‌ترین ادیان توحیدی جهان با تاکید بر تقدس عناصر چهارگانه و اخلاق‌محوری.',
    summaryEn: 'One of the earliest monotheistic ethics traditions, revering primordial elements.',
    detailsFa: {
      description: 'با آموزه‌های اشوزرتشت در شرق فلات ایران (بلخ/خوارزم) آغاز شد و در دوران هخامنشی، اشکانی و ساسانی به دین رسمی یا مسلط فلات ایران بدل گشت. آتشکده آذرگشنسپ در تکاب آذربایجان کانون زیارت شهریاران بود.',
      keyAchievements: ['سرایش گاهان اوستا، کهن‌ترین متن ادبیات ایرانی', 'تاکید بی‌سابقه بر دادگری و نبرد نور علیه تاریکی', 'ثبت جهانی آتشکده و محوطه تخت سلیمان در یونسکو'],
      contemporaryEventsFa: 'هم‌عصر با ودائیان هند، معابد مصر و پیامبران عبرانی باستان.',
    },
    detailsEn: {
      description: 'Founded by prophet Zarathustra, influencing Abrahamic philosophies.',
      keyAchievements: ['The Gathas poetry of the Avesta', 'Tripartite ethical dictum of cosmic harmony', 'Imperial fire temple of Adur Gushnasp'],
      contemporaryEventsEn: 'Contemporary with Vedic India and the early Hebrew kingdom.',
    },
  },
  {
    id: 'rel_mithraism',
    theme: 'religion',
    nameFa: 'مهرپرستی (میترائیسم)',
    nameEn: 'Mithraism (Cult of Mithra)',
    titleOrSubtitleFa: 'ایزد پیمان، نور و راستی · نفوذ از ایران تا امپراتوری روم',
    titleOrSubtitleEn: 'Covenant & Solar Light from Iran to Rome',
    startYear: -1500,
    endYear: 400,
    periodLabelFa: 'هزاره دوم پیش از میلاد تا قرن چهارم میلادی',
    periodLabelEn: '1500 BCE - 400 CE',
    mapCoord: { x: 450, y: 260, regionNameFa: 'کرمانشاه، بیستون و زاگرس مرکزی', regionNameEn: 'Zagros Caves & Kermanshah' },
    summaryFa: 'آیین کهن مهر که از فلات ایران برخاست و سراسر قلمرو سربازان و لژیون‌های رومی را تسخیر کرد.',
    summaryEn: 'Ancient mystery tradition that spread from Iranian mountains across Roman legions.',
    detailsFa: {
      description: 'مهر، ایزد عهد، راستی و نور خورشید بود. آیین‌های سرّی مهر در غارهای تاریک برگزار می‌شد و با سربازان اشکانی و رومی تا قلب اروپا (لندن، رم و دانوب) راه یافت و معابد میترائوم متعددی از آن باقی است.',
      keyAchievements: ['پیمان‌محوری و اخلاق شوالیه‌گری باستان', 'تاسیس صدها معبد میترائوم در سرتاسر قلمرو روم', 'تاثیر بر جشن‌های شب چله (یلدا) و زایش مهر'],
      contemporaryEventsFa: 'هم‌عصر با امپراتوری اشکانی در ایران و امپراتوری روم باستان.',
    },
    detailsEn: {
      description: 'The worship of Mithra as guardian of truth and oaths.',
      keyAchievements: ['Influenced winter solstice celebration of Yalda', 'Spread across Roman garrisons up to Hadrian\'s Wall', 'Left underground cave sanctuaries (Mithraea) across Europe'],
      contemporaryEventsEn: 'Contemporary with Arsacid Parthia and imperial Rome.',
    },
  },
  {
    id: 'rel_sufism_ishraq',
    theme: 'religion',
    nameFa: 'مکتب اشراق و عرفان ایرانی-اسلامی',
    nameEn: 'Illuminationism (Hikmat al-Ishraq) & Sufism',
    titleOrSubtitleFa: 'سهروردی، ابن سینا و عارفان خراسان',
    titleOrSubtitleEn: 'Suhrawardi & Khorasan Mystical Philosophy',
    startYear: 900,
    endYear: 1600,
    periodLabelFa: 'قرن چهارم تا یازدهم هجری',
    periodLabelEn: '9th - 16th Century CE',
    mapCoord: { x: 480, y: 250, regionNameFa: 'سهرورد زنجان، نیشابور و همدان', regionNameEn: 'Zanjan, Hamadan & Nishapur' },
    summaryFa: 'پیوند فلسفه یونانی با نورالانوار ایران باستان و حکمت ذوقی توسط شهاب‌الدین سهروردی.',
    summaryEn: 'Synthesis of Platonic-Aristotelian thought with ancient Iranian philosophy of light.',
    detailsFa: {
      description: 'شیخ اشراق (سهروردی) با بهره‌گیری از حکمت خسروانی ایران باستان و آموزه‌های اسلامی، فلسفه نور را پایه‌گذاری کرد. هم‌زمان مکاتب عرفانی خراسان و شیراز با بایزید بسطامی، ابوسعید ابوالخیر و عطار شکوفا شدند.',
      keyAchievements: ['کتاب حکمة الاشراق سهروردی', 'مکتب فلسفی مشاء ابن سینا در کتاب شفا', 'بنیان‌گذاری فتوت و جوانمردی در فرهنگ عمومی'],
      contemporaryEventsFa: 'هم‌عصر با توماس آکویناس در اروپای قرون وسطی و فیلسوفان اندلس مانند ابن رشد.',
    },
    detailsEn: {
      description: 'Founded by the Master of Illumination (Suhrawardi) bridging Zoroastrian light and Islamic gnosis.',
      keyAchievements: ['Treatise Hikmat al-Ishraq on metaphysics of light', 'Ibn Sina\'s masterwork The Book of Healing', 'Growth of Persian mystical lodges and ethics'],
      contemporaryEventsEn: 'Contemporary with Thomas Aquinas and Averroes (Ibn Rushd).',
    },
  },

  // ==================== 4. POETS & LITERATURE ====================
  {
    id: 'lit_ferdowsi',
    theme: 'literature',
    nameFa: 'حکیم ابوالقاسم فردوسی',
    nameEn: 'Hakim Abul-Qasim Ferdowsi',
    titleOrSubtitleFa: 'حماسه‌سرای توس · زنده کننده زبان پارسی',
    titleOrSubtitleEn: 'Epic Bard of Tus · Resurrector of Persian',
    startYear: 940,
    endYear: 1020,
    periodLabelFa: '۹۴۰ تا ۱۰۲۰ میلادی (قرن چهارم هجری)',
    periodLabelEn: '940 - 1020 CE',
    mapCoord: { x: 630, y: 220, regionNameFa: 'توس، خراسان رضوی', regionNameEn: 'Tus, Khorasan' },
    summaryFa: 'آفرینش شاهنامه با شصت هزار بیت؛ حفظ هویت، تاریخ اسطوره‌ای و زبان فارسی در برابر زوال.',
    summaryEn: 'Author of the Shahnameh (Book of Kings), cementing the Persian literary renaissance.',
    detailsFa: {
      description: 'فردوسی طی سی سال رنج مداوم، تاریخ و اساطیر کهن ایران از کیومرث تا سقوط ساسانیان را در قالب شاهنامه به نظم کشید و زبان پارسی را برای هزاره‌ها بیمه کرد.',
      keyAchievements: ['سرایش شاهنامه در ۶۰٬۰۰۰ بیت بدون به‌کارگیری لغات غیرضروری بیگانه', 'احیای پهلوانی‌ها، خردورزی و دادخواهی با رستم و سیاوش', 'تندیس و آرامگاه ملی در طوس خراسان'],
      contemporaryEventsFa: 'هم‌عصر با رودکی، بوعلی سینا، ابوریحان بیرونی و حکومت سامانیان و غزنویان.',
      quoteOrTextFa: 'بسی رنج بردم در این سال سی / عجم زنده کردم بدین پارسی',
    },
    detailsEn: {
      description: 'Spent three decades composing the world\'s longest epic poem by a single author.',
      keyAchievements: ['60,000 rhyming couplets immortalizing Iranian heritage', 'Ethical foundations of justice and resisting tyranny', 'Preserved the New Persian language during Arabization'],
      contemporaryEventsEn: 'Contemporary with Ibn Sina (Avicenna), Biruni, and the Samanid revival.',
      quoteOrTextEn: 'Much have I suffered during these thirty years; I revived the Persians with this Persian language.',
    },
  },
  {
    id: 'lit_khayyam',
    theme: 'literature',
    nameFa: 'حکیم عمر خیام نیشابوری',
    nameEn: 'Omar Khayyam of Nishapur',
    titleOrSubtitleFa: 'ریاضی‌دان، ستاره‌شناس و فیلسوف رباعیات',
    titleOrSubtitleEn: 'Polymath, Astronomer & Poet of Rubaiyat',
    startYear: 1048,
    endYear: 1131,
    periodLabelFa: '۱۰۴۸ تا ۱۱۳۱ میلادی',
    periodLabelEn: '1048 - 1131 CE',
    mapCoord: { x: 610, y: 230, regionNameFa: 'نیشابور، خراسان', regionNameEn: 'Nishapur, Khorasan' },
    summaryFa: 'تدوین دقیق‌ترین تقویم خورشیدی جهان (گاهشماری جلالی)، جبر پیشرفته و رباعیات فلسفی غنیمت‌شماری دم.',
    summaryEn: 'Formulated the Jalali solar calendar (more accurate than Gregorian) and celebrated Rubaiyat.',
    detailsFa: {
      description: 'خیام دانشمندی جامع‌الاطراف بود که معادلات درجه سه هندسی را حل کرد، تقویم جلالی را طراحی نمود و در اوقات فراغت رباعیاتی ژرف درباره راز هستی، گذرا بودن زمان و ارزش لحظه حال سرود که با ترجمه ادوارد فیتزجرالد به نماد جهانی ادبیات شرق بدل شد.',
      keyAchievements: ['گاه‌شماری جلالی با خطای یک روز در ۵۰۰۰ سال', 'کتاب جبر و مقابله و حل معادلات درجه سه', 'رباعیات خیام ترجمه شده به صدها زبان جهان'],
      contemporaryEventsFa: 'هم‌عصر با خواجه نظام‌الملک طوسی، حسن صباح و سلسله سلجوقیان؛ در جهان هم‌عصر با جنگ‌های صلیبی اول در اروپا.',
      quoteOrTextFa: 'این قافله عمر عجب می‌گذرد / دریاب دمی که با طرب می‌گذرد',
    },
    detailsEn: {
      description: 'Astronomer royal who reformed the calendar and penned timeless quatrains on existence.',
      keyAchievements: ['Jalali Calendar calculation with error of one day in 5,000 years', 'Geometric solutions to cubic equations', 'FitzGerald\'s English translation made Rubaiyat a worldwide sensation'],
      contemporaryEventsEn: 'Contemporary with Nizam al-Mulk, the First Crusade, and the Norman Conquest.',
      quoteOrTextEn: 'The Moving Finger writes; and, having writ, moves on.',
    },
  },
  {
    id: 'lit_hafez',
    theme: 'literature',
    nameFa: 'شمس‌الدین محمد حافظ شیرازی',
    nameEn: 'Hafez of Shiraz (Lisan al-Ghayb)',
    titleOrSubtitleFa: 'لسان‌الغیب · خداوندگار غزل عاشقانه و عارفانه',
    titleOrSubtitleEn: 'Master of the Persian Ghazal & Lyric Mystery',
    startYear: 1315,
    endYear: 1390,
    periodLabelFa: '۱۳۱۵ تا ۱۳۹۰ میلادی (قرن هشتم هجری)',
    periodLabelEn: '1315 - 1390 CE',
    mapCoord: { x: 530, y: 340, regionNameFa: 'شیراز، فارس', regionNameEn: 'Shiraz, Fars' },
    summaryFa: 'اوج غزل فارسی با ایهام‌های بی‌پایان، نقد ریاکاری مذهبی و ستایش عشق و خرد.',
    summaryEn: 'The supreme lyricist of Persian literature, inspiring Goethe\'s West-östlicher Divan.',
    detailsFa: {
      description: 'حافظ شیرازی دیوان غزل‌های خود را با چنان هنر والایی درآمیخت که هر غزل آن لایه‌های چندگانه معنایی دارد. گوته، شاعر نامدار آلمان، پس از خواندن دیوان حافظ چنان شیفته او شد که دیوان غربی-شرقی را سرود و حافظ را همتای ابدی خود نامید.',
      keyAchievements: ['تثبیت غزل عرفانی و اجتماعی در تاریخ ادبیات', 'نقد بی‌امان تزویر و ریا در شعر پارسی', 'الهام‌بخش بزرگان ادبیات غرب نظیر گوته، نیچه و رالف والدو امرسون'],
      contemporaryEventsFa: 'هم‌عصر با حمله تیمور لنگ، حکومت آل مظفر در شیراز؛ در اروپا هم‌عصر با دانته آلیگیری و جفری چاسر.',
      quoteOrTextFa: 'غلام همت آنم که زیر چرخ کبود / ز هر چه رنگ تعلق پذیرد آزاد است',
    },
    detailsEn: {
      description: 'The master of polysemy and musicality, speaking truth to power against hypocrisy.',
      keyAchievements: ['Divan of Hafez revered across households for bibliomancy (Fal-e Hafez)', 'Pinnacle of ghazal craft and mystical ambiguity', 'Direct catalyst for Goethe\'s West-Eastern Divan'],
      contemporaryEventsEn: 'Contemporary with Timur (Tamerlane), Geoffrey Chaucer, and the early Italian Renaissance.',
      quoteOrTextEn: 'I am the servant of the aspiration of anyone under the azure sky who is free from all that bears the hue of attachment.',
    },
  },
  {
    id: 'lit_rumi',
    theme: 'literature',
    nameFa: 'مولانا جلال‌الدین محمد بلخی (رومی)',
    nameEn: 'Mawlana Jalal al-Din Rumi',
    titleOrSubtitleFa: 'سلطان عاشقان · سراینده مثنوی معنوی و دیوان شمس',
    titleOrSubtitleEn: 'Poet of Universal Ecstasy & The Masnavi',
    startYear: 1207,
    endYear: 1273,
    periodLabelFa: '۱۲۰۷ تا ۱۲۷۳ میلادی',
    periodLabelEn: '1207 - 1273 CE',
    mapCoord: { x: 660, y: 200, regionNameFa: 'بلخ کهن (زادگاه) و قونیه (مزار)', regionNameEn: 'Balkh & Konya' },
    summaryFa: 'مثنوی معنوی ملقب به قرآن پارسی، آموزگار عشق جهان‌شمول و سازنده پل گفت‌وگوی انسان‌ها.',
    summaryEn: 'One of the most widely read poets worldwide, author of the profound spiritual Masnavi.',
    detailsFa: {
      description: 'مولانا در بلخ خراسان زاده شد و در پی حمله مغولان به قونیه در آناتولی مهاجرت کرد. دیدار او با شمس تبریزی طوفانی از سرایش و وجد عرفانی آفرید که ثمره آن مثنوی معنوی و دیوان شمس تبریزی با بیش از ۴۰ هزار بیت است.',
      keyAchievements: ['سرایش مثنوی معنوی در ۶ دفتر تمثیلی و عرفانی', 'دیوان شمس با غزل‌های پرشور رقص سماع', 'پرخواننده‌ترین شاعر در ادبیات معاصر جهان'],
      contemporaryEventsFa: 'هم‌عصر با هجوم ویرانگر چنگیزخان و ایلخانان مغول، سعدی شیرازی و خواجه نصیرالدین طوسی.',
      quoteOrTextFa: 'بشنو این نی چون شکایت می‌کند / از جدایی‌ها حکایت می‌کند',
    },
    detailsEn: {
      description: 'Born in Balkh, wandering to Anatolia; ignited into cosmic poetic ecstasy by Shams Tabrizi.',
      keyAchievements: ['Composed the 26,000-verse Masnavi-ye Ma\'navi', 'Inspired the Mevlevi Whirling Dervishes tradition', 'Best-selling poet in modern translation worldwide'],
      contemporaryEventsEn: 'Contemporary with the Mongol invasions, Saadi of Shiraz, and Thomas Aquinas.',
      quoteOrTextEn: 'Listen to the reed how it tells a tale, complaining of separations.',
    },
  },

  // ==================== 5. ART & ARCHITECTURE ====================
  {
    id: 'art_sialk_pottery',
    theme: 'art',
    nameFa: 'سفال‌های منقوش تپه سیلک کاشان',
    nameEn: 'Painted Pottery of Tepe Sialk',
    titleOrSubtitleFa: 'سپیده‌دم هنر انتزاعی و طراحی حیوانی در فلات',
    titleOrSubtitleEn: 'Dawn of Geometric & Zoomorphic Art',
    startYear: -4500,
    endYear: -3000,
    periodLabelFa: 'هزاره پنجم تا چهارم پیش از میلاد',
    periodLabelEn: '5th - 4th Millennium BCE',
    mapCoord: { x: 500, y: 280, regionNameFa: 'تپه سیلک، کاشان', regionNameEn: 'Tepe Sialk, Kashan' },
    summaryFa: 'نقوش شگفت‌انگیز بز کوهی، خورشید و پرندگان شکاری روی ظروف نخودی با مهارت خارق‌العاده.',
    summaryEn: 'Masterpieces of stylized ibex horns and sun motifs on Neolithic clay.',
    detailsFa: {
      description: 'سفالگران سیلک با ساده‌سازی شکل شاخ‌های بز کوهی و ترکیب آن با خورشید و گیاهان، یکی از اولین سبک‌های انتزاعی هنری بشر را خلق کردند که بعدها در آثار مفرغی و هخامنشی تداوم یافت.',
      keyAchievements: ['ابداع چرخ سفالگری و کوره‌های پخت با حرارت کنترل‌شده', 'طراحی نمادین و هندسی شاخ بز کوهی نماد باروری و آب', 'نمایش نمونه‌ها در موزه لوور پاریس و موزه ملی ایران'],
      contemporaryEventsFa: 'هم‌عصر با دوره عبید در بین‌النهرین و تمدن‌های اولیه دره نیل.',
    },
    detailsEn: {
      description: 'Early plateau ceramicists abstracted nature into dynamic circular graphic motifs.',
      keyAchievements: ['Introduction of potter\'s wheel and oxidizing kilns', 'Abstract curved ibex horn as fertility and rain symbol', 'Treasures preserved in Louvre and National Museum of Iran'],
      contemporaryEventsEn: 'Contemporary with Ubaid period Mesopotamia and pre-dynastic Egypt.',
    },
  },
  {
    id: 'art_behzad_miniature',
    theme: 'art',
    nameFa: 'کمال‌الدین بهزاد و مکتب نگارگری هرات',
    nameEn: 'Kamal ud-Din Behzad (Herat School)',
    titleOrSubtitleFa: 'پدر مینیاتور و نقاشی اصیل ایرانی · عصر تیموری',
    titleOrSubtitleEn: 'Father of Persian Miniature Painting',
    startYear: 1450,
    endYear: 1535,
    periodLabelFa: '۱۴۵۰ تا ۱۵۳۵ میلادی',
    periodLabelEn: '1450 - 1535 CE',
    mapCoord: { x: 650, y: 260, regionNameFa: 'هرات و تبریز', regionNameEn: 'Herat & Tabriz Ateliers' },
    summaryFa: 'دمیدن روح واقع‌گرایی، انسان‌مداری و حرکات پویا در نقاشی مینیاتور و تذهیب کتاب‌های خطی.',
    summaryEn: 'Transformed stylized manuscripts into expressive human realism and composition.',
    detailsFa: {
      description: 'بهزاد با مهارت بی‌مانند در رنگ‌آمیزی لاجوردی، طلایی و شنگرفی و نمایش جزئیات چهره‌ها و زندگی کارگران و مردم عادی، مکتب هرات و سپس مکتب تبریز عصر صفوی را به اوج رساند.',
      keyAchievements: ['نگارگری ظفرنامه تیموری و خمسه نظامی', 'ترکیب‌بندی‌های معماری با پرسپکتیو چندگانه معنوی', 'تاسیس دارالانشای هنری دربار هرات و تبریز'],
      contemporaryEventsFa: 'هم‌عصر با لئوناردو داوینچی و میکل‌آنژ در رنسانس ایتالیا، دوره سلطان حسین بایقرا در هرات.',
    },
    detailsEn: {
      description: 'Celebrated court miniaturist who brought individual portraiture and kinetic energy to Persian art.',
      keyAchievements: ['Illustrated Zafarnama and Nizami\'s Khamsa', 'Mastery of lapis lazuli and gold leaf pigments', 'Headed royal ateliers in Herat and Safavid Tabriz'],
      contemporaryEventsEn: 'Contemporary with Leonardo da Vinci and Michelangelo in Renaissance Italy.',
    },
  },

  // ==================== 6. MUSIC & INSTRUMENTS ====================
  {
    id: 'mus_barbad',
    theme: 'music',
    nameFa: 'باربد مروزی و رامشگران ساسانی',
    nameEn: 'Barbad of Merv & Sasanian Court Music',
    titleOrSubtitleFa: 'نوازنده بربط · تدوین هفت خسروانی و سی لحن',
    titleOrSubtitleEn: 'Master of the Barbat (Oud) · Khosravani Modes',
    startYear: 585,
    endYear: 628,
    periodLabelFa: 'اواخر قرن ششم و اوایل قرن هفتم میلادی',
    periodLabelEn: '585 - 628 CE',
    mapCoord: { x: 640, y: 190, regionNameFa: 'مرو کهن و تیسفون (دربار خسرو پرویز)', regionNameEn: 'Merv & Ctesiphon Court' },
    summaryFa: 'سازنده نخستین نظام مدال و دستگاه‌های موسیقی باستان با ۳۰ لحن برای روزهای ماه و ۳۶۰ دستان.',
    summaryEn: 'Codified the imperial musical modal system of 7 Royal Modes and 30 Melodies.',
    detailsFa: {
      description: 'باربد همراه با نکیسا بزرگ‌ترین موسیقی‌دانان دربار ساسانی بودند. او با ساز بربط (نیای عود و لوت اروپایی) نغمه‌هایی برای هر یک از روزهای تقویم اوستایی خلق کرد که پایه دستگاه‌های موسیقی ایرانی شد.',
      keyAchievements: ['تنظیم ۳۰ لحن باربدی (مانند کین سیاوش، شبدیز، سبز در سبز)', 'تکامل ساز بربط زهی با کاسه چوبی و مضراب', 'الهام‌بخش نظام دوازده مقام موسیقی خاورمیانه'],
      contemporaryEventsFa: 'هم‌عصر با خسرو پرویز ساسانی، شاهنشاهی بیزانس و آغاز سده‌های میانه در غرب.',
    },
    detailsEn: {
      description: 'Legendary court minstrel inventing modal archetypes preserved throughout Persian Dastgah system.',
      keyAchievements: ['Composed the 30 Barbadic Modes corresponding to days of the Zoroastrian month', 'Master of the wood-bellied Barbat (precursor to European lute)', 'Immortalized in Nizami\'s Khosrow and Shirin romance'],
      contemporaryEventsEn: 'Contemporary with Sasanian King Khosrow II and the Byzantine Empire.',
    },
  },
  {
    id: 'mus_farabi',
    theme: 'music',
    nameFa: 'ابونصر فارابی (کتاب الموسیقی الکبیر)',
    nameEn: 'Abu Nasr Al-Farabi (Musicus Primus)',
    titleOrSubtitleFa: 'فیلسوف و بزرگ‌ترین نظریه‌پرداز موسیقی مشرق‌زمین',
    titleOrSubtitleEn: 'Master Theorist of Acoustics & Instruments',
    startYear: 872,
    endYear: 950,
    periodLabelFa: '۸۷۲ تا ۹۵۰ میلادی (قرن سوم و چهارم هجری)',
    periodLabelEn: '872 - 950 CE',
    mapCoord: { x: 620, y: 170, regionNameFa: 'فاراب (خراسان بزرگ) و بغداد', regionNameEn: 'Farab (Transoxiana) & Baghdad' },
    summaryFa: 'تالیف جامع‌ترین دانش‌نامه آکوستیک و فواصل صوتی موسیقی باستان و اختراع و تکامل ساز قانون.',
    summaryEn: 'Authored The Great Book of Music, calibrating microtonal intervals and the Qanun zither.',
    detailsFa: {
      description: 'فارابی ملقب به معلم ثانی، نه تنها فیلسوفی نامدار بلکه نوازنده‌ای چیره و مبدع ساز قانون بود. کتاب الموسیقی الکبیر او فواصل پرده‌ها، آکوستیک تارهای زهی و تاثیرات روان‌شناختی نغمات را به شیوه‌ای ریاضی و علمی تدوین کرد.',
      keyAchievements: ['تالیف کتاب الموسیقی الکبیر (شاهکار آکوستیک و فواصل موسیقی)', 'طراحی و تکمیل ساز قانون و عود چندسیمه', 'تشریح علمی پرده‌ها و گام‌های موسیقی سنتی'],
      contemporaryEventsFa: 'هم‌عصر با سامانیان و اوایل خلافت عباسی؛ در جهان هم‌عصر با سلسله تانگ پسین در چین.',
    },
    detailsEn: {
      description: 'The Second Teacher after Aristotle, founding mathematical musicology and organology.',
      keyAchievements: ['Authored Kitab al-Musiqa al-Kabir (The Great Book of Music)', 'Developed the modern form of the plucked box zither (Qanun)', 'Acoustic physics of strings and intervals'],
      contemporaryEventsEn: 'Contemporary with the Samanid renaissance and Late Tang Dynasty.',
    },
  },
];
