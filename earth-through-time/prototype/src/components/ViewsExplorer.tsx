import React, { useState } from 'react';
import { Globe2, Dna, Landmark, Crown, Library, ExternalLink, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { LanguageKey, AtlasView } from '../types';
import { ATLAS_VIEWS, IRAN_STATES_SAMPLE } from '../data/projectData';

interface ViewsExplorerProps {
  currentLang: LanguageKey;
}

export const ViewsExplorer: React.FC<ViewsExplorerProps> = ({ currentLang }) => {
  const [selectedViewId, setSelectedViewId] = useState<AtlasView['id']>('earth');
  const isFa = currentLang === 'fa';

  const selectedView = ATLAS_VIEWS.find(v => v.id === selectedViewId) || ATLAS_VIEWS[0];

  const getIconComponent = (iconName: string) => {
    switch (iconName) {
      case 'Globe2':
        return <Globe2 className="w-5 h-5 text-sky-400" />;
      case 'Dna':
        return <Dna className="w-5 h-5 text-emerald-400" />;
      case 'Landmark':
        return <Landmark className="w-5 h-5 text-amber-400" />;
      case 'Crown':
        return <Crown className="w-5 h-5 text-yellow-400" />;
      case 'Library':
        return <Library className="w-5 h-5 text-purple-400" />;
      default:
        return <Globe2 className="w-5 h-5 text-sky-400" />;
    }
  };

  return (
    <section id="views-section" className="py-12 border-t border-slate-800/80 bg-slate-900/40">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-10">
          <span className="inline-block text-xs uppercase tracking-widest text-amber-400 font-semibold mb-2">
            {isFa ? 'کاوش در پنج پنجرهٔ زمانی و فضایی' : 'Architecture & 5 Perspectives'}
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight font-cinzel">
            {isFa ? 'پنج نمای تعاملی کرونو اطلس' : 'Five Modular Perspectives'}
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-2">
            {isFa
              ? 'هر نما با اتصال به یک نوار زمانی مشترک، زاویه‌ای نو از دگرگونی‌های سیاره و انسان را نمایان می‌سازد.'
              : 'Each view synchronizes seamlessly with the central deep-time scrubber to reveal systemic shifts.'}
          </p>
        </div>

        {/* View Tabs */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 sm:gap-3 mb-8">
          {ATLAS_VIEWS.map((view) => {
            const isSelected = selectedView.id === view.id;
            const viewName = isFa ? view.nameFa : currentLang === 'nl' ? view.nameNl : view.nameEn;

            return (
              <button
                key={view.id}
                onClick={() => setSelectedViewId(view.id)}
                className={`p-3 sm:p-4 rounded-xl text-left sm:text-center transition-all border flex flex-col sm:items-center gap-2 ${
                  isSelected
                    ? 'bg-amber-500/10 border-amber-500/50 shadow-lg shadow-amber-500/10 text-white'
                    : 'bg-slate-900/70 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <div className="p-2 rounded-lg bg-slate-950 border border-slate-800/80">
                  {getIconComponent(view.icon)}
                </div>
                <div className="text-xs sm:text-sm font-semibold truncate w-full">
                  {viewName}
                </div>
                <span className="text-[10px] text-amber-400/80 font-mono hidden sm:block">
                  {view.metrics}
                </span>
              </button>
            );
          })}
        </div>

        {/* Selected View Spotlight Card */}
        <div className="rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900/90 to-slate-950 border border-slate-800 p-6 sm:p-8 shadow-xl">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* View Info */}
            <div className="lg:col-span-7 space-y-4">
              <div className="flex items-center gap-2">
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-mono">
                  {selectedView.metrics}
                </span>
                <span className="text-xs text-slate-400">
                  {isFa ? 'مدول یکپارچه' : 'Integrated Module'}
                </span>
              </div>

              <h3 className="text-xl sm:text-2xl font-bold text-white font-cinzel">
                {isFa ? selectedView.nameFa : selectedView.nameEn}
              </h3>

              <p className="text-sm sm:text-base text-amber-300/90 font-medium">
                {isFa ? selectedView.headlineFa : selectedView.headlineEn}
              </p>

              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                {isFa ? selectedView.descriptionFa : selectedView.descriptionEn}
              </p>

              {/* Tags */}
              <div className="flex flex-wrap gap-1.5 pt-2">
                {selectedView.tags.map(t => (
                  <span
                    key={t}
                    className="text-[11px] px-2.5 py-1 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700/60"
                  >
                    #{t}
                  </span>
                ))}
              </div>
            </div>

            {/* View Context Specific Panel */}
            <div className="lg:col-span-5 bg-slate-950/80 border border-slate-800 rounded-xl p-5">
              {selectedView.id === 'earth' && (
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-sky-400 flex items-center gap-1.5">
                    <Globe2 className="w-3.5 h-3.5" />
                    <span>{isFa ? 'فرآیندهای ژئوفیزیکی کلیدی' : 'Geophysical Simulation'}</span>
                  </h4>
                  <ul className="text-xs space-y-2 text-slate-300">
                    <li className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-sky-400 shrink-0" />
                      <span>{isFa ? 'رودینیا → پانگه‌آ → تجزیه به گوندوانا و لوراسیا' : 'Rodinia → Pangaea → Gondwana / Laurasia breakup'}</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-sky-400 shrink-0" />
                      <span>{isFa ? 'زمین‌ساخت صفحه‌ای پیوسته با نرخ جابه‌جایی سانتی‌متری' : 'Continuous plate vector kinematics across epochs'}</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-sky-400 shrink-0" />
                      <span>{isFa ? 'سطح تراز دریاها و دوره‌های کرهٔ زمین برفی' : 'Global sea level oscillations & Snowball Earth events'}</span>
                    </li>
                  </ul>
                  <div className="mt-3 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
                    {isFa ? 'داده‌ها بر مبنای مدل‌های بازسازی دانشگاه سیدنی و EarthByte' : 'Based on EarthByte & GPlates paleogeographic reconstructions.'}
                  </div>
                </div>
              )}

              {selectedView.id === 'life' && (
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
                    <Dna className="w-3.5 h-3.5" />
                    <span>{isFa ? 'پنج انقراض بزرگ ثبت‌شده' : 'The "Big Five" Die-Offs'}</span>
                  </h4>
                  <div className="space-y-1.5 text-xs text-slate-300 font-mono">
                    <div className="p-1.5 rounded bg-slate-900 border border-slate-800 flex justify-between">
                      <span>Ordovician-Silurian</span>
                      <span className="text-amber-400">445 Ma (~85% loss)</span>
                    </div>
                    <div className="p-1.5 rounded bg-slate-900 border border-slate-800 flex justify-between">
                      <span>Late Devonian</span>
                      <span className="text-amber-400">375 Ma (~75% loss)</span>
                    </div>
                    <div className="p-1.5 rounded bg-slate-900 border border-slate-800 flex justify-between">
                      <span>Permian-Triassic ("The Great Dying")</span>
                      <span className="text-red-400 font-bold">252 Ma (96% loss)</span>
                    </div>
                    <div className="p-1.5 rounded bg-slate-900 border border-slate-800 flex justify-between">
                      <span>Triassic-Jurassic</span>
                      <span className="text-amber-400">201 Ma (~80% loss)</span>
                    </div>
                    <div className="p-1.5 rounded bg-slate-900 border border-slate-800 flex justify-between">
                      <span>Cretaceous-Paleogene (K-Pg)</span>
                      <span className="text-yellow-400">66 Ma (Dinosaurs)</span>
                    </div>
                  </div>
                </div>
              )}

              {selectedView.id === 'civilizations' && (
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
                    <Landmark className="w-3.5 h-3.5" />
                    <span>{isFa ? 'ساختار ۸ گانه داده‌های هر تمدن' : '8 Structural Facets per Polity'}</span>
                  </h4>
                  <div className="grid grid-cols-2 gap-2 text-xs text-slate-300">
                    <div className="p-2 rounded bg-slate-900 border border-slate-800">
                      🏛️ {isFa ? 'نوع حکومت' : 'Government'}
                    </div>
                    <div className="p-2 rounded bg-slate-900 border border-slate-800">
                      🪙 {isFa ? 'نظام اقتصادی' : 'Economy'}
                    </div>
                    <div className="p-2 rounded bg-slate-900 border border-slate-800">
                      📜 {isFa ? 'زبان و خط' : 'Language'}
                    </div>
                    <div className="p-2 rounded bg-slate-900 border border-slate-800">
                      🕯️ {isFa ? 'نظام باورها' : 'Beliefs'}
                    </div>
                    <div className="p-2 rounded bg-slate-900 border border-slate-800">
                      ⚙️ {isFa ? 'دستاوردها' : 'Inventions'}
                    </div>
                    <div className="p-2 rounded bg-slate-900 border border-slate-800">
                      🌪️ {isFa ? 'علت افول' : 'Decline'}
                    </div>
                    <div className="p-2 rounded bg-slate-900 border border-slate-800">
                      🏺 {isFa ? 'میراث ماندگار' : 'Legacy'}
                    </div>
                    <div className="p-2 rounded bg-slate-900 border border-slate-800">
                      🌐 {isFa ? 'هم‌عصرها' : 'Contemporaries'}
                    </div>
                  </div>
                </div>
              )}

              {selectedView.id === 'iran' && (
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-yellow-400 flex items-center gap-1.5">
                    <Crown className="w-3.5 h-3.5" />
                    <span>{isFa ? 'نمونه‌هایی از ۲۸ حکومت فلات ایران' : 'Dynasties Sample (28 Total)'}</span>
                  </h4>
                  <div className="space-y-2 text-xs">
                    {IRAN_STATES_SAMPLE.slice(0, 3).map((state, idx) => (
                      <div key={idx} className="p-2 rounded bg-slate-900 border border-slate-800">
                        <div className="flex justify-between font-semibold text-slate-200">
                          <span>{isFa ? state.nameFa : state.nameEn}</span>
                          <span className="text-amber-400 text-[10px] font-mono">{state.period}</span>
                        </div>
                        <p className="text-[11px] text-slate-400 mt-1">{state.notableAchievement}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {selectedView.id === 'sources' && (
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-purple-400 flex items-center gap-1.5">
                    <Library className="w-3.5 h-3.5" />
                    <span>{isFa ? 'ارزیابی اعتبار و قطعیت داده‌ها' : 'Scholarly Integrity & Open Licences'}</span>
                  </h4>
                  <ul className="text-xs space-y-1.5 text-slate-300">
                    <li className="flex items-center gap-2">
                      <ShieldCheck className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                      <span>{isFa ? 'هر ادعا دارای درجهٔ اطمینان علمی است' : 'Explicit scientific confidence rating on each record'}</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <ShieldCheck className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                      <span>{isFa ? 'آینده به عنوان «سناریو» مشخص شده نه پیش‌گویی قطعی' : 'Future layers presented as scenarios, not predictions'}</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <ShieldCheck className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                      <span>{isFa ? 'نقاط خالی نشانهٔ کمبود پژوهش است، نه نبود تاریخ' : 'Data voids rendered as research gaps, avoiding false absences'}</span>
                    </li>
                  </ul>
                  <div className="mt-3 p-2 bg-purple-950/30 rounded border border-purple-800/40 text-[11px] text-purple-200">
                    {isFa ? '۸۳ پایگاه داده باز و دانشگاهی شامل PBDB, Pleiades, HYDE و EarthByte' : '83 academic databases cited with explicit DOI and licensing.'}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
