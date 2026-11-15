import React from 'react';
import { Sparkles, Github, ExternalLink, Globe, Layers, BookOpen, Clock, ShieldCheck, Download, Code } from 'lucide-react';
import { LanguageKey } from '../types';
import { GITHUB_REPO_URL, LIVE_DEMO_URL, PORTFOLIO_REPO_URL } from '../data/projectData';

interface HeroProps {
  currentLang: LanguageKey;
  onOpenExportModal: () => void;
  onOpenGithubGuide: () => void;
  onScrollToCard: () => void;
}

export const Hero: React.FC<HeroProps> = ({
  currentLang,
  onOpenExportModal,
  onOpenGithubGuide,
  onScrollToCard,
}) => {
  const isFa = currentLang === 'fa';

  const stats = [
    {
      value: '13.8B → +1k',
      labelEn: 'Years Spanned',
      labelFa: 'گسترهٔ زمانی (سال)',
      subEn: 'Cosmic to Scenarios',
      subFa: 'از مهبانگ تا آینده',
    },
    {
      value: '78',
      labelEn: 'Civilizations',
      labelFa: 'تمدن جهانی',
      subEn: 'All Continents',
      subFa: '۸ زاویه برای هر تمدن',
    },
    {
      value: '28 / 98',
      labelEn: 'Iran Pilot',
      labelFa: 'حکومت‌ها و رویدادهای ایران',
      subEn: 'Elam to Modernity',
      subFa: 'از عیلام تا دوران معاصر',
    },
    {
      value: '83',
      labelEn: 'Scholarly Sources',
      labelFa: 'پایگاه داده علمی',
      subEn: 'Academic & Open',
      subFa: 'با مجوزهای شفاف',
    },
    {
      value: '0',
      labelEn: 'Build Step / Deps',
      labelFa: 'وابستگی بیرونی و بیلد',
      subEn: 'Single HTML File',
      subFa: 'تک‌فایل و مستقل',
    },
  ];

  return (
    <section className="relative overflow-hidden pt-8 pb-12 sm:pt-14 sm:pb-16">
      {/* Subtle radial cosmic glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 relative z-10 text-center">
        {/* Top Tag */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-semibold mb-6 shadow-sm">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          <span>
            {isFa
              ? 'کارت ویژهٔ پورتفولیو · سورس‌کد و دمو روی گیت‌هاب'
              : 'Interactive Portfolio Showcase · GitHub Pages Ready'}
          </span>
        </div>

        {/* Main Title */}
        <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white mb-4 font-cinzel leading-tight">
          {isFa ? 'کرونو اطلس' : 'Chrono Atlas'}
          <span className="block text-xl sm:text-3xl lg:text-3xl font-medium text-amber-400 mt-2 font-sans">
            {isFa
              ? 'اطلس تعاملی زمین در گذر زمان، از مهبانگ تا هزار سال آینده'
              : 'Earth Through Time: From the Big Bang to 1,000 Years Ahead'}
          </span>
        </h1>

        {/* Subtitle Description */}
        <p className="max-w-2xl mx-auto text-sm sm:text-base text-slate-300 leading-relaxed mb-8">
          {isFa
            ? 'ساخته شده در یک فایل HTML مستقل، سبک و بدون نیاز به بیلد و اتصال داده. قاره‌ها جابه‌جا می‌شوند، حیات تکامل می‌یابد و تمدن‌ها اوج و افول را تجربه می‌کنند.'
            : 'A self-contained, zero-dependency interactive atlas designed to run instantly and work offline with 5 synchronized planetary lenses.'}
        </p>

        {/* Primary Action Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-4 mb-12">
          {/* Live Demo */}
          <a
            href={LIVE_DEMO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full text-xs sm:text-sm font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-xl shadow-amber-500/25 transition-all hover:scale-105"
          >
            <Globe className="w-4 h-4" />
            <span>{isFa ? 'مشاهده نسخه زنده در GitHub Pages' : 'Open Live on GitHub Pages'}</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>

          {/* Source Code */}
          <a
            href={GITHUB_REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full text-xs sm:text-sm font-semibold bg-slate-800 hover:bg-slate-700 text-white border border-slate-700 shadow-lg transition-all hover:scale-105"
          >
            <Github className="w-4 h-4" />
            <span>{isFa ? 'مخزن گیت‌هاب (Source Code)' : 'View GitHub Repo'}</span>
          </a>

          {/* Copy HTML Snippet */}
          <button
            onClick={onOpenExportModal}
            className="inline-flex items-center gap-2 px-5 py-3 rounded-full text-xs sm:text-sm font-semibold bg-slate-900 hover:bg-slate-800 text-amber-300 border border-amber-500/30 hover:border-amber-500/60 transition-all"
          >
            <Code className="w-4 h-4 text-amber-400" />
            <span>{isFa ? 'دریافت کد آماده برای پورتفولیو' : 'Copy Portfolio Snippet'}</span>
          </button>
        </div>

        {/* Quick Stats Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 sm:gap-4">
          {stats.map((st, idx) => (
            <div
              key={idx}
              className="p-3.5 sm:p-4 rounded-xl bg-slate-900/80 border border-slate-800/80 backdrop-blur text-center transition-all hover:border-amber-500/30"
            >
              <div className="text-xl sm:text-2xl font-extrabold text-white font-mono text-amber-400">
                {st.value}
              </div>
              <div className="text-xs font-semibold text-slate-200 mt-1">
                {isFa ? st.labelFa : st.labelEn}
              </div>
              <div className="text-[10px] text-slate-500 mt-0.5">
                {isFa ? st.subFa : st.subEn}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
