export type LanguageKey = 'en' | 'fa' | 'nl';

export interface ProjectCardContent {
  lang: LanguageKey;
  dir: 'ltr' | 'rtl';
  title: string;
  tagline: string;
  summary: string;
  highlights: string[];
  craft: string;
  meta: string;
  liveDemoUrl: string;
  sourceCodeUrl: string;
  portfolioRepoUrl: string;
}

export interface AtlasView {
  id: 'thematicMap' | 'earth' | 'life' | 'civilizations' | 'iran' | 'sources';
  nameEn: string;
  nameFa: string;
  nameNl: string;
  icon: string;
  headlineEn: string;
  headlineFa: string;
  metrics: string;
  descriptionEn: string;
  descriptionFa: string;
  tags: string[];
}

export interface TimelineEpoch {
  labelEn: string;
  labelFa: string;
  timeDisplay: string;
  yearsAgo: number;
  scaleType: 'log' | 'linear';
  category: 'cosmos' | 'geology' | 'biology' | 'civilization' | 'future';
  descriptionEn: string;
  descriptionFa: string;
}

export interface IranStateHighlight {
  nameEn: string;
  nameFa: string;
  period: string;
  capital: string;
  notableAchievement: string;
}
