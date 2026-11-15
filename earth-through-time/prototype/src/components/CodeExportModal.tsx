import React, { useState } from 'react';
import { X, Copy, Check, Code2, Sparkles, ExternalLink, FileCode, CheckCircle2 } from 'lucide-react';
import { LanguageKey } from '../types';
import { RAW_PORTFOLIO_HTML, ENHANCED_CSS_SNIPPET, PROJECT_CONTENTS, PORTFOLIO_REPO_URL } from '../data/projectData';

interface CodeExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentLang: LanguageKey;
}

export const CodeExportModal: React.FC<CodeExportModalProps> = ({
  isOpen,
  onClose,
  currentLang,
}) => {
  const [activeTab, setActiveTab] = useState<'all' | 'fa' | 'en' | 'nl' | 'css'>('all');
  const [copied, setCopied] = useState(false);
  const isFa = currentLang === 'fa';

  if (!isOpen) return null;

  const getCodeSnippet = () => {
    switch (activeTab) {
      case 'all':
        return RAW_PORTFOLIO_HTML;
      case 'fa': {
        const d = PROJECT_CONTENTS.fa;
        return `<article class="project-card" data-lang="fa" dir="rtl" lang="fa">
  <h3 class="project-title">${d.title}</h3>
  <p class="project-tagline">${d.tagline}</p>

  <p class="project-summary">
    ${d.summary}
  </p>

  <ul class="project-highlights">
${d.highlights.map(h => `    <li>${h}</li>`).join('\n')}
  </ul>

  <p class="project-craft">
    <strong>تصمیم‌های محصولی و پژوهشی:</strong> ${d.craft.replace(/^.*?: /, '')}
  </p>

  <p class="project-meta">${d.meta}</p>

  <p class="project-links">
    <a class="btn" href="${d.liveDemoUrl}">نسخهٔ زنده</a>
    <a class="btn" href="${d.sourceCodeUrl}">کد منبع</a>
  </p>
</article>`;
      }
      case 'en': {
        const d = PROJECT_CONTENTS.en;
        return `<article class="project-card" data-lang="en">
  <h3 class="project-title">${d.title}</h3>
  <p class="project-tagline">${d.tagline}</p>

  <p class="project-summary">
    ${d.summary}
  </p>

  <ul class="project-highlights">
${d.highlights.map(h => `    <li>${h}</li>`).join('\n')}
  </ul>

  <p class="project-craft">
    <strong>Product and research choices:</strong> ${d.craft.replace(/^.*?: /, '')}
  </p>

  <p class="project-meta">${d.meta}</p>

  <p class="project-links">
    <a class="btn" href="${d.liveDemoUrl}">Live demo</a>
    <a class="btn" href="${d.sourceCodeUrl}">Source code</a>
  </p>
</article>`;
      }
      case 'nl': {
        const d = PROJECT_CONTENTS.nl;
        return `<article class="project-card" data-lang="nl" lang="nl">
  <h3 class="project-title">${d.title}</h3>
  <p class="project-tagline">${d.tagline}</p>

  <p class="project-summary">
    ${d.summary}
  </p>

  <ul class="project-highlights">
${d.highlights.map(h => `    <li>${h}</li>`).join('\n')}
  </ul>

  <p class="project-craft">
    <strong>Product- en onderzoekskeuzes:</strong> ${d.craft.replace(/^.*?: /, '')}
  </p>

  <p class="project-meta">${d.meta}</p>

  <p class="project-links">
    <a class="btn" href="${d.liveDemoUrl}">Live demo</a>
    <a class="btn" href="${d.sourceCodeUrl}">Broncode</a>
  </p>
</article>`;
      }
      case 'css':
        return ENHANCED_CSS_SNIPPET;
      default:
        return RAW_PORTFOLIO_HTML;
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(getCodeSnippet());
    setCopied(true);
    setTimeout(() => setCopied(false), 2400);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/80">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400">
              <Code2 className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-bold text-white font-cinzel">
                {isFa ? 'کد آمادهٔ قرارگیری در پورتفولیو گیت‌هاب' : 'Ready-to-Paste Portfolio Snippet'}
              </h3>
              <p className="text-xs text-slate-400">
                MaryamJaberi/MaryamJaberi.github.io
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Instructions banner */}
        <div className="px-6 py-3 bg-amber-500/10 border-b border-amber-500/20 text-xs text-amber-200/90 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-amber-400 shrink-0" />
            <span>
              {isFa
                ? '۱. مخزن MaryamJaberi.github.io را باز کنید ۲. کد را در لیست پروژه‌ها کنار دور و مافیا قرار دهید.'
                : '1. Open MaryamJaberi.github.io repo 2. Paste alongside Dor and Mafia Host OS.'}
            </span>
          </div>
          <a
            href={PORTFOLIO_REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="shrink-0 inline-flex items-center gap-1 font-semibold text-amber-300 hover:underline"
          >
            <span>{isFa ? 'باز کردن مخزن' : 'Open Repo'}</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>

        {/* Tab Controls */}
        <div className="flex items-center justify-between px-6 pt-4 pb-2 border-b border-slate-800 bg-slate-950/50 flex-wrap gap-2">
          <div className="flex items-center gap-1 p-1 rounded-lg bg-slate-900 border border-slate-800 text-xs">
            <button
              onClick={() => setActiveTab('all')}
              className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                activeTab === 'all'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {isFa ? 'هر ۳ زبان (EN + FA + NL)' : 'All 3 Languages'}
            </button>
            <button
              onClick={() => setActiveTab('fa')}
              className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                activeTab === 'fa'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              فارسی (RTL)
            </button>
            <button
              onClick={() => setActiveTab('en')}
              className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                activeTab === 'en'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              English
            </button>
            <button
              onClick={() => setActiveTab('nl')}
              className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                activeTab === 'nl'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Nederlands
            </button>
            <button
              onClick={() => setActiveTab('css')}
              className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                activeTab === 'css'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {isFa ? 'استایل مدرن (CSS)' : 'Modern Card CSS'}
            </button>
          </div>

          <button
            onClick={handleCopy}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-md shadow-amber-500/20 transition-all"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-slate-950" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? (isFa ? 'کپی شد!' : 'Copied!') : (isFa ? 'کپی در کلیپ‌بورد' : 'Copy Snippet')}</span>
          </button>
        </div>

        {/* Code Content */}
        <div className="flex-1 p-6 overflow-y-auto bg-slate-950 font-code text-xs text-slate-300">
          <pre className="whitespace-pre overflow-x-auto leading-relaxed selection:bg-amber-500/30 selection:text-amber-200">
            {getCodeSnippet()}
          </pre>
        </div>
      </div>
    </div>
  );
};
