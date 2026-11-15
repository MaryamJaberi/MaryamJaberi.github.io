import React, { useState } from 'react';
import { Landmark, Scroll, Globe, ShieldAlert, Award, BookOpen, Coins, Users } from 'lucide-react';
import { LanguageKey } from '../types';
import { CIVILIZATIONS_CATALOG, CivilizationRecord } from '../data/atlasData';

interface LensCivilizationsProps {
  currentLang: LanguageKey;
  currentTime: number;
}

export const LensCivilizations: React.FC<LensCivilizationsProps> = ({
  currentLang,
  currentTime,
}) => {
  const isFa = currentLang === 'fa';
  const [selectedRegion, setSelectedRegion] = useState<string>('all');
  const [activeCiv, setActiveCiv] = useState<CivilizationRecord | null>(null);

  const isCivActive = (civ: CivilizationRecord): boolean => {
    if (currentTime < -10000 || currentTime > 1000) return false;
    const startYear = civ.startBce > 0 ? -civ.startBce : Math.abs(civ.startBce);
    const endYear = civ.endBce > 0 ? -civ.endBce : Math.abs(civ.endBce);
    const actualMin = Math.min(startYear, endYear);
    const actualMax = Math.max(startYear, endYear);
    return currentTime >= actualMin && currentTime <= actualMax;
  };

  const filteredCivs = CIVILIZATIONS_CATALOG.filter((civ) => {
    if (selectedRegion === 'all') return true;
    return civ.region === selectedRegion;
  });

  return (
    <div className="space-y-6">
      {/* Region Filter Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-[#111827] p-3.5 sm:p-4 rounded-2xl border border-white/10">
        <div className="flex items-center gap-2 text-xs text-slate-300 font-vazir">
          <Globe className="w-4 h-4 text-amber-400" />
          <span>{isFa ? 'فیلتر بر اساس حوزهٔ جغرافیایی:' : 'Filter Region:'}</span>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {[
            { id: 'all', labelEn: 'All (78)', labelFa: 'همه حوزه‌ها (۷۸)' },
            { id: 'Middle East', labelEn: 'Middle East & W. Asia', labelFa: 'خاورمیانه و غرب آسیا' },
            { id: 'Asia', labelEn: 'East & South Asia', labelFa: 'شرق و جنوب آسیا' },
            { id: 'Europe', labelEn: 'Europe & Med', labelFa: 'اروپا و مدیترانه' },
            { id: 'Americas', labelEn: 'Americas', labelFa: 'قاره آمریکا' },
          ].map((reg) => (
            <button
              key={reg.id}
              onClick={() => setSelectedRegion(reg.id)}
              className={`px-3 py-1.5 rounded-xl text-xs font-vazir transition-all ${
                selectedRegion === reg.id
                  ? 'bg-amber-500 text-slate-950 font-bold shadow-sm'
                  : 'bg-[#161F30] text-slate-300 hover:text-white border border-white/10'
              }`}
            >
              {isFa ? reg.labelFa : reg.labelEn}
            </button>
          ))}
        </div>
      </div>

      {/* Civilizations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCivs.map((civ) => {
          const activeNow = isCivActive(civ);
          return (
            <div
              key={civ.id}
              onClick={() => setActiveCiv(civ)}
              className={`rounded-2xl p-5 border transition-all cursor-pointer flex flex-col justify-between group shadow-lg ${
                activeNow
                  ? 'bg-amber-500/10 border-amber-500 ring-1 ring-amber-500/50'
                  : 'bg-[#111827] hover:bg-[#161F30] border-white/10 hover:border-amber-500/40'
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2.5">
                  <span className="text-[11px] font-vazir text-slate-400">
                    {isFa ? civ.regionFa : civ.region}
                  </span>
                  {activeNow ? (
                    <span className="text-[11px] px-2 py-0.5 rounded-full bg-amber-500 text-slate-950 font-bold font-vazir">
                      {isFa ? 'هم‌زمان با اسلایدر' : 'Active'}
                    </span>
                  ) : (
                    <span className="text-[11px] font-num text-slate-400">
                      {civ.periodLabel}
                    </span>
                  )}
                </div>

                <h4 className="text-base sm:text-lg font-bold font-vazir text-white group-hover:text-amber-400 transition-colors mb-1">
                  {isFa ? civ.nameFa : civ.nameEn}
                </h4>

                <div className="text-xs text-amber-400 font-medium font-vazir mb-2.5">
                  {isFa ? `پایتخت: ${civ.capitalFa}` : `Capital: ${civ.capitalEn}`}
                </div>

                <p className="text-xs text-slate-300 font-vazir line-clamp-3 leading-relaxed">
                  {isFa ? civ.engineeringFa : civ.engineeringEn}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-slate-400 font-vazir">
                <span className="flex items-center gap-1.5">
                  <Scroll className="w-3.5 h-3.5 text-amber-400" />
                  <span>{isFa ? 'شناسنامهٔ ۸ زاویه‌ای' : '8-Facet Dossier'}</span>
                </span>
                <span className="text-amber-400 font-bold group-hover:translate-x-1 transition-transform">
                  ←
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* 8-Facet Deep Inspector Modal */}
      {activeCiv && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md">
          <div className="bg-[#111827] border border-amber-500/50 rounded-3xl max-w-3xl w-full max-h-[90vh] overflow-y-auto p-5 sm:p-7 shadow-2xl relative">
            <button
              onClick={() => setActiveCiv(null)}
              className="absolute top-4 left-4 sm:left-auto sm:right-4 text-slate-400 hover:text-white text-lg font-bold bg-[#161F30] w-8 h-8 rounded-full flex items-center justify-center border border-white/10"
            >
              ✕
            </button>

            {/* Modal Header */}
            <div className="border-b border-white/10 pb-4 mb-5">
              <span className="text-xs font-vazir text-amber-400 font-medium block mb-1">
                {isFa ? activeCiv.regionFa : activeCiv.region} · {activeCiv.periodLabel}
              </span>
              <h3 className="text-2xl font-bold font-vazir text-white">
                {isFa ? activeCiv.nameFa : activeCiv.nameEn}
              </h3>
              <p className="text-xs sm:text-sm text-slate-300 mt-1 font-vazir">
                {isFa ? `پایتخت‌ها و مراکز اداری: ${activeCiv.capitalFa}` : `Capitals: ${activeCiv.capitalEn}`}
              </p>
            </div>

            {/* 8 Structured Facets Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 text-xs font-vazir">
              <div className="bg-[#161F30] p-4 rounded-xl border border-white/10">
                <div className="flex items-center gap-1.5 text-amber-400 font-bold mb-1.5">
                  <Landmark className="w-4 h-4" />
                  <span>{isFa ? '۱. ساختار سیاسی و حکومت' : '1. Governance'}</span>
                </div>
                <p className="text-slate-200 leading-relaxed">
                  {isFa ? activeCiv.governmentFa : activeCiv.governmentEn}
                </p>
              </div>

              <div className="bg-[#161F30] p-4 rounded-xl border border-white/10">
                <div className="flex items-center gap-1.5 text-amber-400 font-bold mb-1.5">
                  <Coins className="w-4 h-4" />
                  <span>{isFa ? '۲. اقتصاد و بازرگانی' : '2. Economy'}</span>
                </div>
                <p className="text-slate-200 leading-relaxed">
                  {isFa ? activeCiv.economyFa : activeCiv.economyEn}
                </p>
              </div>

              <div className="bg-[#161F30] p-4 rounded-xl border border-white/10">
                <div className="flex items-center gap-1.5 text-amber-400 font-bold mb-1.5">
                  <BookOpen className="w-4 h-4" />
                  <span>{isFa ? '۳. زبان و خط رسمی' : '3. Language'}</span>
                </div>
                <p className="text-slate-200 leading-relaxed">
                  {isFa ? activeCiv.languageFa : activeCiv.languageEn}
                </p>
              </div>

              <div className="bg-[#161F30] p-4 rounded-xl border border-white/10">
                <div className="flex items-center gap-1.5 text-amber-400 font-bold mb-1.5">
                  <Scroll className="w-4 h-4" />
                  <span>{isFa ? '۴. باورها و جهان‌بینی' : '4. Beliefs'}</span>
                </div>
                <p className="text-slate-200 leading-relaxed">
                  {isFa ? activeCiv.beliefsFa : activeCiv.beliefsEn}
                </p>
              </div>

              <div className="bg-[#161F30] p-4 rounded-xl border border-white/10">
                <div className="flex items-center gap-1.5 text-amber-400 font-bold mb-1.5">
                  <Award className="w-4 h-4" />
                  <span>{isFa ? '۵. دستاوردهای مهندسی' : '5. Engineering'}</span>
                </div>
                <p className="text-slate-200 leading-relaxed">
                  {isFa ? activeCiv.engineeringFa : activeCiv.engineeringEn}
                </p>
              </div>

              <div className="bg-[#161F30] p-4 rounded-xl border border-rose-500/30">
                <div className="flex items-center gap-1.5 text-rose-400 font-bold mb-1.5">
                  <ShieldAlert className="w-4 h-4" />
                  <span>{isFa ? '۶. دلایل افول و فروپاشی' : '6. Decline'}</span>
                </div>
                <p className="text-slate-200 leading-relaxed">
                  {isFa ? activeCiv.declineFa : activeCiv.declineEn}
                </p>
              </div>

              <div className="bg-[#161F30] p-4 rounded-xl border border-white/10">
                <div className="flex items-center gap-1.5 text-emerald-400 font-bold mb-1.5">
                  <Scroll className="w-4 h-4" />
                  <span>{isFa ? '۷. میراث ماندگار' : '7. Legacy'}</span>
                </div>
                <p className="text-slate-200 leading-relaxed">
                  {isFa ? activeCiv.legacyFa : activeCiv.legacyEn}
                </p>
              </div>

              <div className="bg-[#161F30] p-4 rounded-xl border border-white/10">
                <div className="flex items-center gap-1.5 text-cyan-400 font-bold mb-1.5">
                  <Users className="w-4 h-4" />
                  <span>{isFa ? '۸. هم‌عصران جهانی' : '8. Contemporaries'}</span>
                </div>
                <div className="flex flex-wrap gap-1 mt-1.5">
                  {(isFa ? activeCiv.contemporariesFa : activeCiv.contemporariesEn).map((c, i) => (
                    <span key={i} className="px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 border border-white/10 text-[11px]">
                      {c}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <button
              onClick={() => setActiveCiv(null)}
              className="w-full mt-5 py-2.5 rounded-xl bg-amber-500 text-slate-950 font-bold font-vazir text-xs hover:bg-amber-400 transition-colors"
            >
              {isFa ? 'بستن شناسنامه' : 'Close'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
