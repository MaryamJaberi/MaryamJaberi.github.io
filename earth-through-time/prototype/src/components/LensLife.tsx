import React, { useState } from 'react';
import { Dna, Flame, Search, Filter } from 'lucide-react';
import { LanguageKey } from '../types';
import { CLADES_OF_LIFE, MASS_EXTINCTIONS, CladeLifeGroup, MassExtinctionEvent } from '../data/atlasData';

interface LensLifeProps {
  currentLang: LanguageKey;
  currentTime: number;
}

export const LensLife: React.FC<LensLifeProps> = ({ currentLang, currentTime }) => {
  const isFa = currentLang === 'fa';
  const [selectedExtinction, setSelectedExtinction] = useState<MassExtinctionEvent | null>(MASS_EXTINCTIONS[2]); // Permian
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeCladeModal, setActiveCladeModal] = useState<CladeLifeGroup | null>(null);

  const getCladeStatus = (clade: CladeLifeGroup): { status: 'unborn' | 'alive' | 'extinct'; labelEn: string; labelFa: string; color: string } => {
    const curYearsAgo = Math.abs(Math.min(0, currentTime));

    if (curYearsAgo > clade.appearedYearsAgo) {
      return {
        status: 'unborn',
        labelEn: 'Yet to Evolve',
        labelFa: 'هنوز فرگشت نیافته',
        color: 'text-slate-400 bg-slate-800/60 border-slate-700',
      };
    }
    if (clade.extinctYearsAgo && curYearsAgo < clade.extinctYearsAgo) {
      return {
        status: 'extinct',
        labelEn: 'Extinct',
        labelFa: 'منقرض‌شده',
        color: 'text-rose-400 bg-rose-500/10 border-rose-500/30',
      };
    }
    return {
      status: 'alive',
      labelEn: 'Flourishing',
      labelFa: 'پویا و شکوفا',
      color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
    };
  };

  const filteredClades = CLADES_OF_LIFE.filter((clade) => {
    const matchesCat = categoryFilter === 'all' || clade.cladeCategory === categoryFilter;
    const matchesSearch =
      clade.nameEn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      clade.nameFa.includes(searchQuery);
    return matchesCat && matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* The Big 5 Mass Extinctions Matrix */}
      <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 sm:p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mb-4 pb-3 border-b border-white/10">
          <div>
            <span className="text-xs font-semibold text-rose-400 font-vazir flex items-center gap-1.5">
              <Flame className="w-4 h-4" />
              <span>{isFa ? 'پنج انقراض بزرگ تاریخ زمین (The Big Five)' : 'The Big Five Mass Extinctions'}</span>
            </span>
            <h3 className="text-lg sm:text-xl font-bold font-vazir text-white mt-1">
              {isFa ? 'گلوگاه‌های تکامل و فروپاشی زیست‌کره' : 'Evolutionary Bottlenecks & Radiations'}
            </h3>
          </div>
          <span className="text-xs text-slate-400 font-vazir">
            {isFa ? 'برای مشاهده مشخصات هر رویداد کلیک کنید' : 'Click to inspect trigger mechanics'}
          </span>
        </div>

        {/* 5 Extinction Buttons */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5 mb-5">
          {MASS_EXTINCTIONS.map((ext) => {
            const isSelected = selectedExtinction?.id === ext.id;
            return (
              <button
                key={ext.id}
                onClick={() => setSelectedExtinction(ext)}
                className={`text-right sm:text-left p-3.5 rounded-xl border transition-all flex flex-col justify-between ${
                  isSelected
                    ? 'bg-rose-500/15 border-rose-500 shadow-md ring-1 ring-rose-500/50'
                    : 'bg-[#161F30] hover:bg-slate-800 border-white/10'
                }`}
              >
                <div>
                  <span className="font-num text-[11px] text-slate-400 block mb-1">{ext.timeLabel}</span>
                  <div className="font-bold font-vazir text-white text-xs sm:text-sm leading-snug">
                    {isFa ? ext.nameFa : ext.nameEn}
                  </div>
                </div>

                <div className="mt-3 pt-2 border-t border-white/10 flex items-center justify-between">
                  <span className="text-[11px] text-slate-400 font-vazir">{isFa ? 'نابودی گونه‌ها:' : 'Loss:'}</span>
                  <span className="font-num font-bold text-rose-400 text-xs sm:text-sm">~{ext.killCurvePct}%</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Selected Extinction Detailed Dossier */}
        {selectedExtinction && (
          <div className="bg-[#161F30] border border-rose-500/30 rounded-xl p-4 sm:p-5 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <span className="text-[11px] text-rose-400 font-vazir block mb-1 font-semibold">
                {isFa ? 'گونه‌ها و راسته‌های نابودشده' : 'Key Extinct Clades'}
              </span>
              <p className="text-xs sm:text-sm font-medium font-vazir text-slate-200 leading-relaxed">
                {isFa ? selectedExtinction.victimsFa : selectedExtinction.victimsEn}
              </p>
            </div>

            <div>
              <span className="text-[11px] text-amber-400 font-vazir block mb-1 font-semibold">
                {isFa ? 'محرک‌ها و علل زمین‌شناختی' : 'Geological Triggers'}
              </span>
              <p className="text-xs sm:text-sm font-vazir text-slate-300 leading-relaxed">
                {isFa ? selectedExtinction.triggersFa : selectedExtinction.triggersEn}
              </p>
            </div>

            <div>
              <span className="text-[11px] text-cyan-400 font-vazir block mb-1 font-semibold">
                {isFa ? 'زمان بازسازی زیست‌کره' : 'Biosphere Recovery Lag'}
              </span>
              <p className="text-xs sm:text-sm font-vazir text-slate-300 leading-relaxed">
                {isFa ? selectedExtinction.recoveryYearsFa : selectedExtinction.recoveryYearsEn}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Clades Explorer & Search */}
      <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 sm:p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-5">
          <div>
            <h4 className="text-lg sm:text-xl font-bold font-vazir text-white">
              {isFa ? 'راسته‌ها و شاخه‌های درخت حیات (۶۰ گروه)' : 'Tree of Life Clades & Radiations'}
            </h4>
            <p className="text-xs text-slate-400 font-vazir mt-0.5">
              {isFa
                ? 'وضعیت هر راسته به صورت زنده منطبق با اسلایدر زمان محاسبه می‌شود.'
                : 'Real-time evolutionary status matched to the continuum scrubber above.'}
            </p>
          </div>

          {/* Search & Category Filter */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute right-3 sm:right-auto sm:left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder={isFa ? 'جستجوی نام راسته یا جاندار...' : 'Search clade...'}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pr-9 sm:pr-3 sm:pl-8 py-1.5 rounded-xl bg-slate-800/80 border border-white/10 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-amber-500 font-vazir"
              />
            </div>

            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-slate-800/80 border border-white/10 text-xs text-white focus:outline-none focus:border-amber-500 font-vazir"
            >
              <option value="all">{isFa ? 'تمام دسته‌ها' : 'All Taxa'}</option>
              <option value="microbe">{isFa ? 'میکروب‌ها و سلول‌های کهن' : 'Microbes'}</option>
              <option value="invertebrate">{isFa ? 'بی‌مهرگان و بندپایان' : 'Invertebrates'}</option>
              <option value="plant">{isFa ? 'گیاهان' : 'Plants'}</option>
              <option value="fish">{isFa ? 'ماهیان' : 'Fishes'}</option>
              <option value="dinosaur">{isFa ? 'دایناسورها' : 'Dinosaurs'}</option>
              <option value="mammal">{isFa ? 'پستانداران' : 'Mammals'}</option>
              <option value="hominid">{isFa ? 'انسان‌تباران' : 'Hominids'}</option>
            </select>
          </div>
        </div>

        {/* Clade Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {filteredClades.map((clade) => {
            const statusInfo = getCladeStatus(clade);
            return (
              <div
                key={clade.id}
                onClick={() => setActiveCladeModal(clade)}
                className="bg-[#161F30] hover:bg-slate-800 border border-white/10 hover:border-amber-500/50 rounded-xl p-4 transition-all cursor-pointer flex flex-col justify-between group shadow-sm"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-[11px] font-num text-slate-400 uppercase">
                      {clade.cladeCategory}
                    </span>
                    <span className={`text-[11px] font-vazir font-semibold px-2 py-0.5 rounded-full border ${statusInfo.color}`}>
                      {isFa ? statusInfo.labelFa : statusInfo.labelEn}
                    </span>
                  </div>

                  <h5 className="font-bold font-vazir text-white text-sm group-hover:text-amber-400 transition-colors mb-1.5">
                    {isFa ? clade.nameFa : clade.nameEn}
                  </h5>

                  <p className="text-xs text-slate-300 font-vazir line-clamp-2 leading-relaxed">
                    {isFa ? clade.descriptionFa : clade.descriptionEn}
                  </p>
                </div>

                <div className="mt-3 pt-2.5 border-t border-white/10 flex items-center justify-between text-[11px] font-num text-slate-400">
                  <span>{isFa ? clade.appearedLabelFa : clade.appearedLabelEn}</span>
                  {clade.extinctLabelEn && (
                    <span className="text-rose-400">
                      † {isFa ? clade.extinctLabelFa : clade.extinctLabelEn}
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Clade Detail Modal */}
      {activeCladeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
          <div className="bg-[#111827] border border-amber-500/50 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative">
            <button
              onClick={() => setActiveCladeModal(null)}
              className="absolute top-4 left-4 sm:left-auto sm:right-4 text-slate-400 hover:text-white text-lg font-bold"
            >
              ✕
            </button>

            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-num uppercase text-amber-400 font-bold">
                {activeCladeModal.cladeCategory}
              </span>
              {activeCladeModal.isBigFiveVictim && (
                <span className="text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 border border-rose-500/40 font-vazir font-semibold">
                  {isFa ? 'قربانی انقراض‌های پنج‌گانه' : 'Mass Extinction Victim'}
                </span>
              )}
            </div>

            <h3 className="text-xl font-bold font-vazir text-white mb-3">
              {isFa ? activeCladeModal.nameFa : activeCladeModal.nameEn}
            </h3>

            <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-vazir mb-5">
              {isFa ? activeCladeModal.descriptionFa : activeCladeModal.descriptionEn}
            </p>

            <div className="bg-[#161F30] p-4 rounded-xl border border-white/10 space-y-2 text-xs font-vazir">
              <div className="flex justify-between">
                <span className="text-slate-400">{isFa ? 'پیدایش نخستین سنگواره:' : 'First Fossil Appearance:'}</span>
                <span className="text-amber-400 font-semibold">
                  {isFa ? activeCladeModal.appearedLabelFa : activeCladeModal.appearedLabelEn}
                </span>
              </div>
              {activeCladeModal.extinctLabelEn && (
                <div className="flex justify-between">
                  <span className="text-slate-400">{isFa ? 'انقراض نهایی:' : 'Extinction Horizon:'}</span>
                  <span className="text-rose-400 font-semibold">
                    {isFa ? activeCladeModal.extinctLabelFa : activeCladeModal.extinctLabelEn}
                  </span>
                </div>
              )}
            </div>

            <button
              onClick={() => setActiveCladeModal(null)}
              className="w-full mt-5 py-2.5 rounded-xl bg-amber-500 text-slate-950 font-bold font-vazir text-xs hover:bg-amber-400 transition-colors"
            >
              {isFa ? 'بستن' : 'Close'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
