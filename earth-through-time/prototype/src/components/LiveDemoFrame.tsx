import React, { useState } from 'react';
import { ExternalLink, Play, RotateCcw, Compass, Globe, Sparkles, Layers, Maximize2 } from 'lucide-react';
import { LanguageKey } from '../types';
import { LIVE_DEMO_URL, GITHUB_REPO_URL } from '../data/projectData';

interface LiveDemoFrameProps {
  currentLang: LanguageKey;
}

export const LiveDemoFrame: React.FC<LiveDemoFrameProps> = ({ currentLang }) => {
  const [timelineYear, setTimelineYear] = useState<number>(0); // 0 = present, -250000000 = Permian, etc.
  const [activeLayer, setActiveLayer] = useState<'earth' | 'life' | 'civ' | 'iran'>('civ');
  const [showIframe, setShowIframe] = useState<boolean>(false);
  const isFa = currentLang === 'fa';

  const yearsOptions = [
    { label: isFa ? '۱۳٫۸ میلیارد سال قبل (مهبانگ)' : '-13.8 Ga (Big Bang)', val: -13800000000, desc: 'Cosmic Microwave Background' },
    { label: isFa ? '۲۵۲ میلیون سال قبل (انقراض پرمین)' : '-252 Ma (Great Dying)', val: -252000000, desc: 'Pangaea Supercontinent' },
    { label: isFa ? '۵۵۰ پیش از میلاد (کوروش و هخامنشیان)' : '-550 BCE (Achaemenid)', val: -2575, desc: 'First Universal Empire' },
    { label: isFa ? 'عصر حاضر (اکنون)' : 'Present Day', val: 0, desc: 'Anthropocene & Digital Era' },
    { label: isFa ? '+۱۰۰۰ سال آینده (سناریوها)' : '+1,000y (Scenarios)', val: 1000, desc: 'Planetary Stewardship Models' },
  ];

  return (
    <section className="py-12 border-t border-slate-800/80 bg-slate-950/60">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        {/* Section Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-8">
          <div>
            <span className="text-xs uppercase tracking-widest text-amber-400 font-semibold flex items-center gap-1.5 mb-1.5">
              <Compass className="w-3.5 h-3.5" />
              <span>{isFa ? 'شبیه‌ساز تعاملی رابط کاربری اطلس' : 'Interactive Atlas HUD Simulator'}</span>
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-white font-cinzel">
              {isFa ? 'تجربهٔ زندهٔ کرونو اطلس' : 'Live Chrono Atlas Preview'}
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              {isFa
                ? 'مشاهدهٔ مستقیم عملکرد بدون نیاز به سرور؛ اجرا شده بر بستر GitHub Pages.'
                : 'Zero build step, single self-contained HTML engine, deployed at GitHub Pages.'}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowIframe(!showIframe)}
              className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors flex items-center gap-1.5"
            >
              <Maximize2 className="w-3.5 h-3.5 text-amber-400" />
              <span>{showIframe ? (isFa ? 'حالت شبیه‌ساز' : 'HUD Simulator') : (isFa ? 'بارگذاری وب‌سایت زنده (iFrame)' : 'Load Live Pages')}</span>
            </button>

            <a
              href={LIVE_DEMO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-amber-500 hover:bg-amber-400 text-slate-950 shadow transition-all flex items-center gap-1.5"
            >
              <span>{isFa ? 'باز کردن در تب جدید' : 'Open in New Tab'}</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>

        {/* Display Frame */}
        {showIframe ? (
          <div className="rounded-2xl border border-slate-800 overflow-hidden bg-slate-900 shadow-2xl h-[580px] relative">
            <iframe
              src={LIVE_DEMO_URL}
              title="Chrono Atlas Live"
              className="w-full h-full border-0"
              sandbox="allow-scripts allow-same-origin allow-popups"
            />
            <div className="absolute bottom-3 right-3 z-10">
              <a
                href={LIVE_DEMO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-1.5 rounded-md bg-slate-900/90 hover:bg-slate-800 text-slate-200 text-xs font-mono border border-slate-700 flex items-center gap-1.5 shadow"
              >
                <span>maryamjaberi.github.io/chrono-atlas</span>
                <ExternalLink className="w-3 h-3 text-amber-400" />
              </a>
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-slate-800 bg-gradient-to-b from-slate-900 to-slate-950 p-6 sm:p-8 shadow-2xl relative overflow-hidden">
            {/* Ambient Background Grid & Stars */}
            <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#f59e0b_1px,transparent_1px)] [background-size:24px_24px] pointer-events-none" />

            {/* Virtual HUD Top Bar */}
            <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-6 border-b border-slate-800 relative z-10">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-xs font-mono text-slate-300">
                  CHRONO-ATLAS-CORE // SINGLE-FILE STANDALONE
                </span>
              </div>

              {/* Layer switchers */}
              <div className="flex items-center gap-1 p-1 rounded-lg bg-slate-950 border border-slate-800 text-xs">
                <button
                  onClick={() => setActiveLayer('earth')}
                  className={`px-3 py-1 rounded transition-all ${activeLayer === 'earth' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'}`}
                >
                  {isFa ? 'زمین' : 'Earth'}
                </button>
                <button
                  onClick={() => setActiveLayer('life')}
                  className={`px-3 py-1 rounded transition-all ${activeLayer === 'life' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'}`}
                >
                  {isFa ? 'حیات' : 'Life'}
                </button>
                <button
                  onClick={() => setActiveLayer('civ')}
                  className={`px-3 py-1 rounded transition-all ${activeLayer === 'civ' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'}`}
                >
                  {isFa ? 'تمدن‌ها' : 'Civilizations'}
                </button>
                <button
                  onClick={() => setActiveLayer('iran')}
                  className={`px-3 py-1 rounded transition-all ${activeLayer === 'iran' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'}`}
                >
                  {isFa ? 'ایران' : 'Iran'}
                </button>
              </div>
            </div>

            {/* Virtual Map Canvas Mockup */}
            <div className="relative rounded-xl bg-slate-950 border border-slate-800/80 p-8 min-h-[300px] flex flex-col items-center justify-center text-center overflow-hidden">
              {/* Cosmic Ring SVG Graphic */}
              <svg className="absolute w-[450px] h-[450px] text-amber-500/10 pointer-events-none animate-spin-slow" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" stroke="currentColor" strokeWidth="0.5" fill="none" strokeDasharray="2, 4" />
                <circle cx="50" cy="50" r="32" stroke="currentColor" strokeWidth="0.5" fill="none" />
                <circle cx="50" cy="50" r="18" stroke="currentColor" strokeWidth="0.3" fill="none" strokeDasharray="4, 4" />
              </svg>

              <div className="relative z-10 max-w-lg space-y-3">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-700/80 text-amber-400 text-xs font-mono">
                  <span>ACTIVE ERA:</span>
                  <span className="font-bold text-white">
                    {yearsOptions.find(o => o.val === timelineYear)?.label}
                  </span>
                </div>

                <h3 className="text-xl sm:text-2xl font-bold text-slate-100 font-cinzel">
                  {yearsOptions.find(o => o.val === timelineYear)?.desc}
                </h3>

                <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
                  {isFa
                    ? 'با تغییر هر مقطع زمانی، اطلس جابه‌جایی قاره‌ها، وضعیت اقلیم، لایه‌های زیستی و حدود قلمروهای تمدنی را همگام‌سازی می‌کند.'
                    : 'Dragging the timeline synchronizes continental coordinates, temperature deviations, extinctions, and territorial boundaries.'}
                </p>

                <div className="pt-3">
                  <a
                    href={LIVE_DEMO_URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full text-xs sm:text-sm font-semibold bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-lg shadow-amber-500/25 transition-transform hover:scale-105"
                  >
                    <span>{isFa ? 'ورود به اطلس زنده در GitHub Pages' : 'Launch Full Interactive Atlas'}</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            </div>

            {/* Quick Timeline Selector Strip */}
            <div className="mt-6 pt-5 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2">
              <span className="text-xs font-medium text-slate-400">
                {isFa ? 'نقاط عطف آزمایشی:' : 'Epoch Presets:'}
              </span>
              <div className="flex flex-wrap gap-2">
                {yearsOptions.map((opt) => (
                  <button
                    key={opt.val}
                    onClick={() => setTimelineYear(opt.val)}
                    className={`px-3 py-1 rounded-lg text-xs font-mono transition-all ${
                      timelineYear === opt.val
                        ? 'bg-amber-500 text-slate-950 font-bold'
                        : 'bg-slate-950 hover:bg-slate-800 text-slate-300 border border-slate-800'
                    }`}
                  >
                    {opt.label.split(' ')[0]}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};
