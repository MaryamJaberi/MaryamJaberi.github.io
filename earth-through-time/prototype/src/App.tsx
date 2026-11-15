import React, { useState, useEffect } from 'react';
import { 
  Compass, 
  Globe, 
  Dna, 
  Landmark, 
  Crown, 
  Library, 
  Map, 
  Eye, 
  Sparkles,
  Volume2,
  Share2,
  Calendar,
  Layers
} from 'lucide-react';
import { LanguageKey } from './types';
import { Header } from './components/Header';
import { MasterTimelineController } from './components/MasterTimelineController';
import { ThematicAtlasMap } from './components/ThematicAtlasMap';
import { LensEarth } from './components/LensEarth';
import { LensLife } from './components/LensLife';
import { LensCivilizations } from './components/LensCivilizations';
import { LensIran } from './components/LensIran';
import { LensSources } from './components/LensSources';
import { DeploymentLinkModal } from './components/DeploymentLinkModal';
import { Footer } from './components/Footer';

export default function App() {
  // Primary app state
  const [currentLang, setCurrentLang] = useState<LanguageKey>('fa');
  const [currentTime, setCurrentTime] = useState<number>(-2500); // 500 BCE (Achaemenid era)
  const [scaleMode, setScaleMode] = useState<'log' | 'linear'>('log');
  const [activeLens, setActiveLens] = useState<'thematicMap' | 'earth' | 'life' | 'civilizations' | 'iran' | 'sources'>('thematicMap');
  const [isDeployModalOpen, setIsDeployModalOpen] = useState(false);

  const isFa = currentLang === 'fa';

  // Update HTML document dir and lang attributes
  useEffect(() => {
    document.documentElement.lang = currentLang;
    document.documentElement.dir = currentLang === 'fa' ? 'rtl' : 'ltr';
  }, [currentLang]);

  // Format the epoch name for the header badge
  const getEpochName = (time: number): string => {
    if (time <= -1000000000) {
      const val = (Math.abs(time) / 1000000000).toFixed(1);
      return isFa ? `${val} میلیارد سال پیش` : `${val} Ga`;
    }
    if (time <= -1000000) {
      const val = Math.round(Math.abs(time) / 1000000);
      return isFa ? `${val} میلیون سال پیش` : `${val} Ma`;
    }
    if (time < 0) {
      const val = Math.abs(time).toLocaleString();
      return isFa ? `${val} پ.م (پیش از میلاد)` : `${val} BCE`;
    }
    if (time === 0) {
      return isFa ? 'عصر حاضر (۲۰۲۶)' : 'Present Day (2026)';
    }
    return isFa ? `+${time} سال آینده (سناریو)` : `+${time} Future Scenario`;
  };

  const lenses = [
    {
      id: 'thematicMap' as const,
      labelEn: 'Visual Thematic Atlas',
      labelFa: 'نقشه اطلس تصویری و موضوعی',
      icon: <Map className="w-4 h-4 text-amber-400" />,
      badge: isFa ? 'لایه تصویری ۶گانه' : '6 Visual Themes',
      descFa: 'نقشه تعاملی فلات ایران و جهان با لایه‌های تمدن، جانوران، ادیان، شاعران، هنر و موسیقی',
      descEn: 'Interactive map of Iran & the world with fauna, religions, literature, art, and music'
    },
    {
      id: 'earth' as const,
      labelEn: 'Earth & Geology',
      labelFa: 'زمین و رانش قاره‌ها',
      icon: <Globe className="w-4 h-4 text-sky-400" />,
      badge: isFa ? 'کره زمین و اقلیم' : 'Globe & Climate',
      descFa: 'حرکت صفحات تکتونیکی، شکافت ابرقاره‌ها، شاخص‌های CO2 و یخچالی',
      descEn: 'Continental drift, plate tectonics, atmospheric CO2, and ice age cycles'
    },
    {
      id: 'life' as const,
      labelEn: 'Tree of Life',
      labelFa: 'درخت حیات و انقراض‌ها',
      icon: <Dna className="w-4 h-4 text-emerald-400" />,
      badge: isFa ? '۶۰ گروه زیستی' : '60 Clades & Big 5',
      descFa: 'انفجار کامبرین، خزندگان کهن، هومونیدها و ۵ انقراض هولناک زمین',
      descEn: 'Phylogenetic clades, Cambrian explosion, mass extinctions'
    },
    {
      id: 'civilizations' as const,
      labelEn: '78 Civilizations',
      labelFa: '۷۸ تمدن جهان',
      icon: <Landmark className="w-4 h-4 text-purple-400" />,
      badge: isFa ? '۶ قاره' : '6 Continents',
      descFa: 'ساختار حکومت، خط و زبان، باورها، مهندسی و میراث تمدن‌های تاریخ بشر',
      descEn: 'Governance, languages, engineering, and cultural legacies across history'
    },
    {
      id: 'iran' as const,
      labelEn: 'Iran Deep-Dive',
      labelFa: 'ویژه فلات ایران',
      icon: <Crown className="w-4 h-4 text-yellow-400" />,
      badge: isFa ? '۲۸ سلسله · ۹۸ رویداد' : '28 Dynasties',
      descFa: 'از تمدن عیلام تا دوران معاصر، گاه‌شمار اختراعات (قنات، چاپار)، زبان‌ها و اقلیم',
      descEn: 'From Elam to modern Iran, inventions, languages, and ecosystems'
    },
    {
      id: 'sources' as const,
      labelEn: 'Scholarly Sources',
      labelFa: 'مراجع و پایگاه‌های علمی',
      icon: <Library className="w-4 h-4 text-rose-400" />,
      badge: isFa ? '۸۳ پایگاه داده' : '83 Databases',
      descFa: 'مستندات متدولوژی، منابع دیرینه‌شناسی، نقشه‌های تاریخی و مراجع باز',
      descEn: 'Peer-reviewed academic databases, open licenses, and paleomap references'
    },
  ];

  return (
    <div className="min-h-screen bg-[#0A0E17] text-[#F1F5F9] font-vazir bg-modern-grid flex flex-col selection:bg-amber-500/30 selection:text-amber-200">
      {/* Sticky Main Header */}
      <Header
        currentLang={currentLang}
        onLanguageChange={setCurrentLang}
        activeLens={activeLens}
        onSelectLens={setActiveLens}
        onOpenDeployModal={() => setIsDeployModalOpen(true)}
        onResetTime={() => setCurrentTime(0)}
        currentEpochName={getEpochName(currentTime)}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-3 sm:px-6 lg:px-8 py-5 sm:py-6 space-y-6">
        
        {/* Visual Learning Banner for Visual Learners */}
        <div className="bg-gradient-to-r from-amber-500/15 via-emerald-500/10 to-indigo-500/15 border border-amber-500/30 rounded-2xl p-4 sm:p-5 shadow-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400 shrink-0">
              <Eye className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider text-amber-400 font-vazir">
                  {isFa ? 'حالت یادگیری تصویری و شهودی' : 'Visual Learning Experience'}
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-num">
                  {isFa ? 'نقشه و تصویر محور' : 'Visual-First'}
                </span>
              </div>
              <p className="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed font-vazir">
                {isFa 
                  ? 'همه چیز با نقشه، نشانگرهای تصویری، رنگ‌های راهنما و المان‌های دیداری نمایش داده می‌شود تا بدون نیاز به خواندن متن‌های سنگین، تاریخ زمین و ایران را با تصویر تجربه کنید.'
                  : 'Everything is designed with maps, visual badges, and graphics so you can discover Earth and Iranian history visually.'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0 self-end sm:self-center">
            <button
              onClick={() => setActiveLens('thematicMap')}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 shadow-sm ${
                activeLens === 'thematicMap'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'bg-white/10 hover:bg-white/15 text-white border border-white/15'
              }`}
            >
              <Map className="w-4 h-4" />
              <span>{isFa ? 'مشاهده نقشه تصویری' : 'Open Thematic Map'}</span>
            </button>
          </div>
        </div>

        {/* Master Timeline Scrubber & Controller */}
        <section aria-label="Deep Time Controller" className="rounded-2xl shadow-xl overflow-hidden">
          <MasterTimelineController
            currentLang={currentLang}
            currentTime={currentTime}
            onTimeChange={setCurrentTime}
            scaleMode={scaleMode}
            onScaleModeChange={setScaleMode}
          />
        </section>

        {/* Visual Lenses Navigation Bar */}
        <nav aria-label="Atlas Perspectives" className="bg-[#111827]/80 backdrop-blur-md border border-white/10 rounded-2xl p-2 sm:p-2.5 shadow-lg">
          <div className="flex items-center justify-between gap-2 px-2 pb-2 mb-2 border-b border-white/5 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-amber-400" />
              <span className="font-semibold text-white">
                {isFa ? 'پنجره‌های کاوش در زمان و جغرافیا' : 'Exploration Windows'}
              </span>
            </div>
            <span className="text-[11px] font-num text-slate-400">
              {isFa ? 'نشانگر زمان به تمام پنجره‌ها متصل است' : 'Scrubber syncs across all views'}
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
            {lenses.map((lens) => {
              const isActive = activeLens === lens.id;
              return (
                <button
                  key={lens.id}
                  onClick={() => setActiveLens(lens.id)}
                  className={`p-3 rounded-xl text-right transition-all flex flex-col justify-between relative group ${
                    isActive
                      ? 'bg-gradient-to-br from-amber-500/20 to-amber-600/10 border border-amber-500/50 shadow-md shadow-amber-500/10'
                      : 'bg-[#1F2937]/50 hover:bg-[#1F2937] border border-white/5 hover:border-white/15'
                  }`}
                >
                  <div className="flex items-center justify-between gap-1 w-full mb-2">
                    <div className={`p-2 rounded-lg ${isActive ? 'bg-amber-500/20 text-amber-300' : 'bg-white/5 text-slate-400 group-hover:text-white'}`}>
                      {lens.icon}
                    </div>
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-white/5 text-slate-400 font-num">
                      {lens.badge}
                    </span>
                  </div>

                  <div>
                    <h3 className={`text-xs sm:text-sm font-bold font-vazir leading-tight ${isActive ? 'text-amber-400' : 'text-slate-200 group-hover:text-white'}`}>
                      {isFa ? lens.labelFa : lens.labelEn}
                    </h3>
                  </div>

                  {isActive && (
                    <div className="absolute bottom-0 left-3 right-3 h-0.5 bg-amber-400 rounded-full" />
                  )}
                </button>
              );
            })}
          </div>
        </nav>

        {/* Active Lens Dynamic View Container */}
        <section aria-label="Active Lens Content" className="transition-opacity duration-200">
          {activeLens === 'thematicMap' && (
            <ThematicAtlasMap
              currentLang={currentLang}
              currentTime={currentTime}
              onTimeChange={setCurrentTime}
            />
          )}

          {activeLens === 'earth' && (
            <LensEarth
              currentLang={currentLang}
              currentTime={currentTime}
            />
          )}

          {activeLens === 'life' && (
            <LensLife
              currentLang={currentLang}
              currentTime={currentTime}
            />
          )}

          {activeLens === 'civilizations' && (
            <LensCivilizations
              currentLang={currentLang}
              currentTime={currentTime}
            />
          )}

          {activeLens === 'iran' && (
            <LensIran
              currentLang={currentLang}
              currentTime={currentTime}
            />
          )}

          {activeLens === 'sources' && (
            <LensSources
              currentLang={currentLang}
            />
          )}
        </section>
      </main>

      {/* Footer */}
      <Footer
        currentLang={currentLang}
        onOpenDeployModal={() => setIsDeployModalOpen(true)}
      />

      {/* Deployment & Direct Link Modal */}
      <DeploymentLinkModal
        isOpen={isDeployModalOpen}
        onClose={() => setIsDeployModalOpen(false)}
        currentLang={currentLang}
      />
    </div>
  );
}
