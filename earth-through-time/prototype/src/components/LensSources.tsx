import React, { useState } from 'react';
import { Library, ShieldCheck, Search, ExternalLink, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { LanguageKey } from '../types';
import { SCHOLARLY_SOURCES_CATALOG, ScholarlySourceRecord } from '../data/atlasData';

interface LensSourcesProps {
  currentLang: LanguageKey;
}

export const LensSources: React.FC<LensSourcesProps> = ({ currentLang }) => {
  const isFa = currentLang === 'fa';
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const filteredSources = SCHOLARLY_SOURCES_CATALOG.filter((src) => {
    const matchesDomain = selectedDomain === 'all' || src.domain === selectedDomain;
    const matchesSearch =
      src.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      src.leadInstitution.toLowerCase().includes(searchQuery.toLowerCase()) ||
      src.notesEn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      src.notesFa.includes(searchQuery);
    return matchesDomain && matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Epistemic Principles Callout Box */}
      <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 sm:p-6 grid grid-cols-1 md:grid-cols-3 gap-5 shadow-xl font-vazir">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0 mt-0.5">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <div>
            <h5 className="text-sm font-bold text-white mb-1">
              {isFa ? 'سطح قطعیت علمی داده‌ها' : 'Stratified Confidence'}
            </h5>
            <p className="text-xs text-slate-300 leading-relaxed">
              {isFa
                ? 'هر ادعا در این اطلس دارای رتبهٔ اعتبار است؛ داده‌های فسیلی با داده‌های باستان‌شناسی تفکیک شده‌اند.'
                : 'Every record indicates whether data is directly measured, stratigraphically constrained, or modeled.'}
            </p>
          </div>
        </div>

        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shrink-0 mt-0.5">
            <CheckCircle2 className="w-4 h-4" />
          </div>
          <div>
            <h5 className="text-sm font-bold text-white mb-1">
              {isFa ? 'آینده به عنوان سناریو' : 'Scenarios, Not Forecasts'}
            </h5>
            <p className="text-xs text-slate-300 leading-relaxed">
              {isFa
                ? 'لایه‌های زمانی فراتر از زمان حال (+۱۰۰۰ سال) به صراحت سناریوهای اقلیمی هستند نه پیش‌بینی قطعی.'
                : 'Future horizons are formulated as climate and geosphere scenarios, not deterministic predictions.'}
            </p>
          </div>
        </div>

        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-lg bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400 shrink-0 mt-0.5">
            <AlertTriangle className="w-4 h-4" />
          </div>
          <div>
            <h5 className="text-sm font-bold text-white mb-1">
              {isFa ? 'نمایش شکاف پژوهشی' : 'Data Gap Transparency'}
            </h5>
            <p className="text-xs text-slate-300 leading-relaxed">
              {isFa
                ? 'مناطقی که بدون داده مانده‌اند نشان‌دهنده کمبود کاوش باستان‌شناسی است، نه نبودِ سکونت بشر.'
                : 'Empty map zones signify lack of archaeological surveys rather than absence of human civilization.'}
            </p>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 sm:p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-5">
          <div>
            <h4 className="text-lg sm:text-xl font-bold font-vazir text-white">
              {isFa ? 'کاتالوگ ۸۳ پایگاه دادهٔ علمی داوری‌شده' : 'Scholarly Repositories & Data Sources'}
            </h4>
            <p className="text-xs text-slate-400 font-vazir mt-0.5">
              {isFa ? 'مراجع با ذکر مجوز دسترسی باز و نهادهای علمی همکار' : 'Peer-reviewed databases with open licenses'}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2 font-vazir">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute right-3 sm:right-auto sm:left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder={isFa ? 'جستجو در مراجع و نهادها...' : 'Search sources...'}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pr-9 sm:pr-3 sm:pl-8 py-1.5 rounded-xl bg-slate-800/80 border border-white/10 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-amber-500 font-vazir"
              />
            </div>

            <select
              value={selectedDomain}
              onChange={(e) => setSelectedDomain(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-slate-800/80 border border-white/10 text-xs text-white focus:outline-none focus:border-amber-500 font-vazir"
            >
              <option value="all">{isFa ? 'تمام حوزه‌های علمی' : 'All Domains'}</option>
              <option value="Tectonics">{isFa ? 'زمین‌ساخت و پالئوژئوگرافی' : 'Tectonics'}</option>
              <option value="Paleobiology">{isFa ? 'دیرینه‌زیست‌شناسی' : 'Paleobiology'}</option>
              <option value="Archaeology">{isFa ? 'باستان‌شناسی و مکان‌های کهن' : 'Archaeology'}</option>
              <option value="Paleoclimatology">{isFa ? 'دیرینه‌اقلیم‌شناسی' : 'Paleoclimatology'}</option>
            </select>
          </div>
        </div>

        {/* Source Cards List */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredSources.map((src) => (
            <div
              key={src.id}
              className="bg-[#161F30] border border-white/10 rounded-xl p-4 sm:p-5 flex flex-col justify-between hover:border-amber-500/40 transition-all shadow-sm"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="text-[11px] font-vazir text-cyan-400">
                    {isFa ? src.domainFa : src.domain}
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded-md bg-slate-800 text-amber-400 border border-white/10 font-num">
                    {src.license}
                  </span>
                </div>

                <h5 className="font-bold font-vazir text-white text-sm sm:text-base mb-1">
                  {src.name}
                </h5>

                <div className="text-xs text-slate-400 font-vazir mb-3">
                  {src.leadInstitution} · <span className="font-num text-[11px] text-slate-400">{src.coverage}</span>
                </div>

                <p className="text-xs text-slate-300 font-vazir leading-relaxed">
                  {isFa ? src.notesFa : src.notesEn}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-white/10 flex items-center justify-between text-xs font-vazir">
                <div className="flex items-center gap-1 text-[11px] text-amber-400">
                  <span>{isFa ? 'سطح اطمینان:' : 'Confidence:'}</span>
                  <span className="font-bold">{src.confidenceLevel}</span>
                </div>

                <a
                  href={src.doiOrUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-cyan-400 hover:text-amber-400 text-xs flex items-center gap-1 transition-colors"
                >
                  <span>{isFa ? 'پایگاه مرجع' : 'Access Repo'}</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
