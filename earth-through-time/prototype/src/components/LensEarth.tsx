import React from 'react';
import { Globe, Layers, Wind, Flame, Mountain } from 'lucide-react';
import { LanguageKey } from '../types';
import { InteractiveMapGlobe } from './InteractiveMapGlobe';

interface LensEarthProps {
  currentLang: LanguageKey;
  currentTime: number;
}

export const LensEarth: React.FC<LensEarthProps> = ({ currentLang, currentTime }) => {
  const isFa = currentLang === 'fa';

  return (
    <div className="space-y-6">
      {/* The Interactive Map & Globe Projection with Telemetry */}
      <InteractiveMapGlobe currentLang={currentLang} currentTime={currentTime} />

      {/* Geological Mechanism Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 shadow-lg">
          <div className="w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/25 flex items-center justify-center text-amber-400 mb-3">
            <Mountain className="w-4 h-4" />
          </div>
          <h4 className="text-sm sm:text-base font-bold text-white font-vazir mb-2">
            {isFa ? 'چرخه‌های تکتونیکی ویلسون' : 'Wilson Tectonic Cycles'}
          </h4>
          <p className="text-xs text-slate-400 leading-relaxed font-vazir">
            {isFa
              ? 'پوسته قاره‌ای زمین هر ۳۰۰ تا ۵۰۰ میلیون سال در قالب یک ابرقاره (مانند کلمبیا، رودینیا و پانگه‌آ) متمرکز شده و سپس بر اثر جریان‌های همرفتی گوشته دچار شکافت می‌شود.'
              : 'Every 300 to 500 million years, Earth\'s continental crust aggregates into a supercontinent before rifting apart driven by mantle convection.'}
          </p>
        </div>

        <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 shadow-lg">
          <div className="w-9 h-9 rounded-xl bg-rose-500/10 border border-rose-500/25 flex items-center justify-center text-rose-400 mb-3">
            <Flame className="w-4 h-4" />
          </div>
          <h4 className="text-sm sm:text-base font-bold text-white font-vazir mb-2">
            {isFa ? 'فوران‌های عظیم بازالتی (LIP)' : 'Large Igneous Provinces (LIP)'}
          </h4>
          <p className="text-xs text-slate-400 leading-relaxed font-vazir">
            {isFa
              ? 'خروج میلیون‌ها کیلومتر مکعب گدازه در سیبری و دکن، گازهای گلخانه‌ای عظیم به اتمسفر تزریق کرده و آغازگر انقراض‌های اقلیمی بزرگ بوده است.'
              : 'Effusion of millions of cubic kilometers of flood basalt injected colossal CO2 pulses, triggering severe biotic turnover.'}
          </p>
        </div>

        <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 shadow-lg">
          <div className="w-9 h-9 rounded-xl bg-cyan-500/10 border border-cyan-500/25 flex items-center justify-center text-cyan-400 mb-3">
            <Wind className="w-4 h-4" />
          </div>
          <h4 className="text-sm sm:text-base font-bold text-white font-vazir mb-2">
            {isFa ? 'دوره‌های گلخانه‌ای و یخبندان' : 'Greenhouse vs Icehouse States'}
          </h4>
          <p className="text-xs text-slate-400 leading-relaxed font-vazir">
            {isFa
              ? 'زمین در طول تاریخ بارها میان وضعیت فوق‌گرم گلخانه‌ای (با تراز دریایی بسیار بالاتر) و وضعیت‌های یخبندان با کلاهک‌های قطبی وسیع در نوسان بوده است.'
              : 'Earth continuously shifts between warm greenhouse worlds and cold icehouse periods with expansive glacial sheets.'}
          </p>
        </div>
      </div>
    </div>
  );
};
