import React, { useState } from 'react';
import { ExternalLink, Github, Copy, Check, Sparkles, BookOpen, Clock, Compass, ShieldCheck } from 'lucide-react';
import { LanguageKey, ProjectCardContent } from '../types';
import { PROJECT_CONTENTS, GITHUB_REPO_URL, LIVE_DEMO_URL } from '../data/projectData';

interface CardPreviewProps {
  activeLang: LanguageKey;
  onSelectLang: (lang: LanguageKey) => void;
  onExploreViews: () => void;
  onOpenTimeline: () => void;
}

export const CardPreview: React.FC<CardPreviewProps> = ({
  activeLang,
  onSelectLang,
  onExploreViews,
  onOpenTimeline,
}) => {
  const [copied, setCopied] = useState(false);
  const [showAllThree, setShowAllThree] = useState(false);

  const cardData = PROJECT_CONTENTS[activeLang];
  const isFa = activeLang === 'fa';

  const handleCopySingleHtml = (lang: LanguageKey) => {
    const data = PROJECT_CONTENTS[lang];
    const isRtl = data.dir === 'rtl';
    const html = `<article class="project-card" data-lang="${data.lang}" ${isRtl ? 'dir="rtl" lang="fa"' : `lang="${data.lang}"`}>
  <h3 class="project-title">${data.title}</h3>
  <p class="project-tagline">${data.tagline}</p>

  <p class="project-summary">
    ${data.summary}
  </p>

  <ul class="project-highlights">
${data.highlights.map(h => `    <li>${h}</li>`).join('\n')}
  </ul>

  <p class="project-craft">
    <strong>${lang === 'fa' ? 'تصمیم‌های محصولی و پژوهشی:' : lang === 'nl' ? 'Product- en onderzoekskeuzes:' : 'Product and research choices:'}</strong> ${data.craft.replace(/^.*?: /, '')}
  </p>

  <p class="project-meta">${data.meta}</p>

  <p class="project-links">
    <a class="btn" href="${data.liveDemoUrl}">${lang === 'fa' ? 'نسخهٔ زنده' : lang === 'nl' ? 'Live demo' : 'Live demo'}</a>
    <a class="btn" href="${data.sourceCodeUrl}">${lang === 'fa' ? 'کد منبع' : lang === 'nl' ? 'Broncode' : 'Source code'}</a>
  </p>
</article>`;

    navigator.clipboard.writeText(html);
    setCopied(true);
    setTimeout(() => setCopied(false), 2400);
  };

  const renderSingleCard = (data: ProjectCardContent) => {
    const isRtl = data.dir === 'rtl';
    const isPersian = data.lang === 'fa';

    return (
      <div
        key={data.lang}
        dir={data.dir}
        className={`relative group rounded-2xl bg-gradient-to-b from-slate-900/95 via-slate-900/90 to-slate-950/95 border border-slate-800/90 hover:border-amber-500/40 p-6 sm:p-9 shadow-2xl transition-all duration-300 ${
          isPersian ? 'font-vazir' : 'font-sans'
        }`}
      >
        {/* Ambient Top Glow Line */}
        <div className="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-amber-500/70 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

        {/* Card Header & Language Badge */}
        <div className="flex flex-wrap items-start justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-300 border border-amber-500/30">
                <Compass className="w-3 h-3" />
                {data.lang === 'fa' ? 'پروژه شاخص پورتفولیو' : data.lang === 'nl' ? 'Uitgelicht Project' : 'Featured Showcase'}
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-slate-400 border border-slate-700">
                {data.lang.toUpperCase()}
              </span>
            </div>
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-white mb-2 font-cinzel">
              {data.title}
            </h2>
          </div>

          <button
            onClick={() => handleCopySingleHtml(data.lang)}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-amber-300 border border-slate-700 transition-colors"
            title="Copy this card's ready-to-paste HTML"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? (isFa ? 'کپی شد!' : 'Copied!') : (isFa ? 'کپی کد HTML' : 'Copy HTML')}</span>
          </button>
        </div>

        {/* Tagline */}
        <p className="text-base sm:text-lg text-amber-400 font-medium leading-relaxed mb-5">
          {data.tagline}
        </p>

        {/* Summary */}
        <p className="text-sm sm:text-base text-slate-300 leading-relaxed mb-6 font-normal">
          {data.summary}
        </p>

        {/* Key Highlights Grid */}
        <div className="mb-6">
          <h4 className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-3 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>{isFa ? 'ویژگی‌های برجسته' : isPersian ? 'Belangrijkste Hoogtepunten' : 'Core Highlights'}</span>
          </h4>
          <ul className="space-y-2.5">
            {data.highlights.map((highlight, idx) => (
              <li
                key={idx}
                className="flex items-start gap-2.5 text-xs sm:text-sm text-slate-300/90 leading-relaxed"
              >
                <span className="text-amber-400 select-none mt-0.5 font-bold">✦</span>
                <span>{highlight}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Craft & Research Statement */}
        <div className={`p-4 rounded-xl bg-amber-500/5 border ${isRtl ? 'border-r-4 border-r-amber-500 border-amber-500/20' : 'border-l-4 border-l-amber-500 border-amber-500/20'} mb-6`}>
          <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
            {data.craft}
          </p>
        </div>

        {/* Meta & Tech Stack */}
        <div className="pt-4 border-t border-dashed border-slate-800 mb-6 text-xs text-slate-400 font-code flex flex-wrap items-center justify-between gap-2">
          <span>{data.meta}</span>
          <span className="px-2 py-0.5 rounded bg-slate-800/80 text-amber-400/90 border border-slate-700/60">
            Self-Contained · No Build Step
          </span>
        </div>

        {/* Links & CTA Bar */}
        <div className="flex flex-wrap items-center gap-3">
          <a
            href={data.liveDemoUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-xs sm:text-sm font-semibold bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-lg shadow-amber-500/20 transition-all hover:scale-[1.02]"
          >
            <span>{isFa ? 'مشاهده نسخه زنده' : data.lang === 'nl' ? 'Live demo bekijken' : 'Open Live Demo'}</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>

          <a
            href={data.sourceCodeUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-xs sm:text-sm font-semibold bg-slate-800 hover:bg-slate-700 text-white border border-slate-700 transition-all hover:scale-[1.02]"
          >
            <Github className="w-3.5 h-3.5" />
            <span>{isFa ? 'کد منبع در گیت‌هاب' : data.lang === 'nl' ? 'Broncode op GitHub' : 'Source on GitHub'}</span>
          </a>

          <button
            onClick={onExploreViews}
            className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-full text-xs sm:text-sm font-medium bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-amber-400 border border-slate-800 transition-colors"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>{isFa ? 'بررسی ۵ نمای اطلس' : 'Explore 5 Views'}</span>
          </button>
        </div>
      </div>
    );
  };

  return (
    <section className="py-8 sm:py-12">
      <div className="max-w-5xl mx-auto px-4 sm:px-6">
        {/* Controls bar */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-800">
          <div>
            <span className="text-xs uppercase tracking-wider text-amber-400 font-semibold">
              {isFa ? 'پیش‌نمایش زنده کارت پورتفولیو' : 'Interactive Portfolio Card Preview'}
            </span>
            <p className="text-xs text-slate-400 mt-0.5">
              {isFa
                ? 'طراحی زیبا، خوانا و آمادهٔ قرارگیری در وب‌سایت MaryamJaberi.github.io'
                : 'Formatted ready for your personal portfolio repository'}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowAllThree(!showAllThree)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                showAllThree
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'bg-slate-800 text-slate-300 hover:text-white border border-slate-700'
              }`}
            >
              {isFa ? 'مقایسه هم‌زمان هر ۳ زبان' : 'Compare All 3 Languages'}
            </button>
          </div>
        </div>

        {/* Cards Container */}
        {showAllThree ? (
          <div className="space-y-8">
            {renderSingleCard(PROJECT_CONTENTS.fa)}
            {renderSingleCard(PROJECT_CONTENTS.en)}
            {renderSingleCard(PROJECT_CONTENTS.nl)}
          </div>
        ) : (
          renderSingleCard(cardData)
        )}
      </div>
    </section>
  );
};
