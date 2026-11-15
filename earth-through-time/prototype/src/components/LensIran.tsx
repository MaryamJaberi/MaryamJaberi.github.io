import React, { useState } from 'react';
import { Crown, Cpu, BookOpen, Leaf, MapPin } from 'lucide-react';
import { LanguageKey } from '../types';
import { IRAN_DYNASTIES_DATA, IRAN_THEMATIC_PANELS, IranDynastyRecord } from '../data/atlasData';

interface LensIranProps {
  currentLang: LanguageKey;
  currentTime: number;
}

export const LensIran: React.FC<LensIranProps> = ({ currentLang, currentTime }) => {
  const isFa = currentLang === 'fa';
  const [selectedDynasty, setSelectedDynasty] = useState<IranDynastyRecord>(IRAN_DYNASTIES_DATA[2]); // Achaemenid default
  const [activeThematicTab, setActiveThematicTab] = useState<'inventions' | 'language' | 'ecology'>('inventions');

  return (
    <div className="space-y-6">
      {/* Dynasty Selector & Overview */}
      <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 sm:p-6 shadow-xl">
        <div className="flex items-center justify-between gap-4 mb-4 pb-3 border-b border-white/10">
          <div>
            <span className="text-xs font-semibold text-amber-400 font-vazir block">
              {isFa ? 'پایلوت فلات ایران (۲۸ دوره و ۹۸ رویداد مستند)' : 'Iranian Plateau Pilot (28 States & 98 Events)'}
            </span>
            <h3 className="text-lg sm:text-xl font-bold font-vazir text-white mt-0.5">
              {isFa ? 'سلسله‌ها و دوران‌های تاریخی فلات ایران' : 'Dynasties & Political Horizons'}
            </h3>
          </div>
          <span className="text-xs text-amber-400 font-num font-semibold">
            {selectedDynasty.periodDisplay}
          </span>
        </div>

        {/* Dynasty Horizontal Picker */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-3 mb-5 scrollbar-none">
          {IRAN_DYNASTIES_DATA.map((dyn) => {
            const isSelected = selectedDynasty.id === dyn.id;
            return (
              <button
                key={dyn.id}
                onClick={() => setSelectedDynasty(dyn)}
                className={`px-3.5 py-1.5 rounded-xl text-xs whitespace-nowrap transition-all font-vazir border shrink-0 ${
                  isSelected
                    ? 'bg-amber-500 text-slate-950 font-bold border-amber-500 shadow-sm'
                    : 'bg-[#161F30] text-slate-300 hover:text-white border-white/10'
                }`}
              >
                {isFa ? dyn.nameFa : dyn.nameEn}
              </button>
            );
          })}
        </div>

        {/* Selected Dynasty Deep Card */}
        <div className="bg-[#161F30] border border-white/10 rounded-2xl p-5 sm:p-6 grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="space-y-3 font-vazir">
            <div>
              <span className="text-[11px] text-slate-400 block mb-0.5">
                {isFa ? 'نام دوره و گستره زمانی' : 'Polity & Span'}
              </span>
              <h4 className="text-lg sm:text-xl font-bold text-white">
                {isFa ? selectedDynasty.nameFa : selectedDynasty.nameEn}
              </h4>
              <span className="text-xs font-num text-amber-400 font-semibold">
                {selectedDynasty.periodDisplay}
              </span>
            </div>

            <div className="pt-2 border-t border-white/10">
              <span className="text-[11px] text-slate-400 block mb-0.5">
                {isFa ? 'پایتخت‌ها و مراکز سیاسی' : 'Capitals'}
              </span>
              <p className="text-xs sm:text-sm text-slate-200 font-medium flex items-center gap-1.5">
                <MapPin className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                <span>{selectedDynasty.capitals}</span>
              </p>
            </div>
          </div>

          <div className="space-y-3 font-vazir">
            <div>
              <span className="text-[11px] text-slate-400 block mb-0.5">
                {isFa ? 'بنیان‌گذار و شهریاران شاخص' : 'Founder & Monarchs'}
              </span>
              <p className="text-xs sm:text-sm text-slate-200 font-medium">
                {selectedDynasty.founder} ({selectedDynasty.notableMonarch})
              </p>
            </div>

            <div className="pt-2 border-t border-white/10">
              <span className="text-[11px] text-slate-400 block mb-0.5">
                {isFa ? 'گستره جغرافیایی تقریبی' : 'Territory'}
              </span>
              <p className="text-xs text-slate-300 leading-relaxed">
                {selectedDynasty.territoryExtent}
              </p>
            </div>
          </div>

          <div className="bg-[#111827] p-4 rounded-xl border border-white/10 flex flex-col justify-between font-vazir">
            <div>
              <span className="text-[11px] text-amber-400 font-semibold block mb-1">
                {isFa ? 'شاهکار مهندسی و تمدنی' : 'Civilizational Feat'}
              </span>
              <p className="text-xs text-slate-200 leading-relaxed">
                {isFa ? selectedDynasty.keyAchievementFa : selectedDynasty.keyAchievementEn}
              </p>
            </div>

            <div className="mt-3 pt-2 border-t border-white/10 flex items-center justify-between text-xs text-slate-400">
              <span>{isFa ? 'رویدادهای ثبت‌شده:' : 'Cataloged Events:'}</span>
              <span className="font-num font-bold text-amber-400">{selectedDynasty.eventsCount} {isFa ? 'مورد' : 'events'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Thematic Panels: Inventions, Language, Ecology */}
      <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 sm:p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5 pb-3 border-b border-white/10">
          <div>
            <h4 className="text-base sm:text-lg font-bold font-vazir text-white">
              {isFa ? 'پرونده‌های تخصصی فلات ایران' : 'Thematic Plateau Dossiers'}
            </h4>
            <p className="text-xs text-slate-400 font-vazir mt-0.5">
              {isFa ? 'مهندسی بومی، سیر زبان و اکولوژی در گذر هزاره‌ها' : 'Engineering feats, linguistics, and endemic ecology'}
            </p>
          </div>

          {/* Tab Selector */}
          <div className="flex items-center gap-1 p-1 bg-[#161F30] rounded-xl border border-white/10 text-xs font-vazir">
            <button
              onClick={() => setActiveThematicTab('inventions')}
              className={`px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 ${
                activeThematicTab === 'inventions'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" />
              <span>{isFa ? 'ابداعات و مهندسی' : 'Inventions'}</span>
            </button>

            <button
              onClick={() => setActiveThematicTab('language')}
              className={`px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 ${
                activeThematicTab === 'language'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>{isFa ? 'زبان و خط' : 'Linguistics'}</span>
            </button>

            <button
              onClick={() => setActiveThematicTab('ecology')}
              className={`px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 ${
                activeThematicTab === 'ecology'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              <Leaf className="w-3.5 h-3.5" />
              <span>{isFa ? 'اکولوژی و حیات وحش' : 'Ecology'}</span>
            </button>
          </div>
        </div>

        {/* Thematic Cards */}
        {(() => {
          const currentPanel = IRAN_THEMATIC_PANELS.find((p) => p.id === activeThematicTab);
          if (!currentPanel) return null;
          return (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {currentPanel.items.map((item, idx) => (
                <div
                  key={idx}
                  className="bg-[#161F30] border border-white/10 rounded-xl p-4 sm:p-5 flex flex-col justify-between shadow-sm"
                >
                  <div>
                    <span className="text-[11px] font-num text-amber-400 block mb-1">
                      {item.originPeriod}
                    </span>
                    <h5 className="text-sm sm:text-base font-bold font-vazir text-white mb-1.5">
                      {isFa ? item.nameFa : item.nameEn}
                    </h5>
                    <p className="text-xs text-slate-300 font-vazir leading-relaxed">
                      {isFa ? item.detailFa : item.detailEn}
                    </p>
                  </div>

                  <div className="mt-3 pt-2.5 border-t border-white/10 flex items-center justify-between text-[11px] font-vazir text-slate-400">
                    <span>{isFa ? 'میراث ثبت‌شده' : 'Documented Heritage'}</span>
                    <span className="text-amber-400">✦</span>
                  </div>
                </div>
              ))}
            </div>
          );
        })()}
      </div>
    </div>
  );
};
