import React, { useMemo } from 'react';
import { Globe, Compass, Wind, Thermometer, Waves, Mountain } from 'lucide-react';
import { LanguageKey } from '../types';
import { PALEOGEOGRAPHY_EPOCHS, PaleogeographyState } from '../data/atlasData';

interface InteractiveMapGlobeProps {
  currentLang: LanguageKey;
  currentTime: number;
}

export const InteractiveMapGlobe: React.FC<InteractiveMapGlobeProps> = ({
  currentLang,
  currentTime,
}) => {
  const isFa = currentLang === 'fa';

  const activeEpoch: PaleogeographyState = useMemo(() => {
    if (currentTime <= -800000000) return PALEOGEOGRAPHY_EPOCHS[0]; // Rodinia
    if (currentTime <= -400000000) return PALEOGEOGRAPHY_EPOCHS[1]; // Cambrian
    if (currentTime <= -180000000) return PALEOGEOGRAPHY_EPOCHS[2]; // Permian / Pangaea
    if (currentTime <= -30000000) return PALEOGEOGRAPHY_EPOCHS[3]; // Cretaceous
    if (currentTime <= 1000) return PALEOGEOGRAPHY_EPOCHS[4]; // Modern
    return PALEOGEOGRAPHY_EPOCHS[5]; // Future Pangaea Ultima
  }, [currentTime]);

  return (
    <div className="w-full bg-[#111827] border border-white/10 rounded-2xl overflow-hidden shadow-2xl relative">
      {/* Top Status Bar */}
      <div className="bg-[#161F30] px-4 sm:px-6 py-3 border-b border-white/10 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <Globe className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs sm:text-sm font-bold text-white font-vazir">
                {isFa ? 'نقشهٔ پالئوژئوگرافی و وضعیت اقلیم' : 'Paleogeography & Planetary Geodesy'}
              </span>
              <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 font-num font-medium">
                {activeEpoch.supercontinent}
              </span>
            </div>
            <p className="text-xs text-slate-400 font-vazir mt-0.5">
              {isFa ? activeEpoch.periodNameFa : activeEpoch.periodNameEn}
            </p>
          </div>
        </div>

        {/* Tectonic event badge */}
        <div className="text-right hidden sm:block">
          <span className="text-[11px] text-slate-400 font-vazir block">
            {isFa ? 'رویداد زمین‌ساختی فعال' : 'Active Tectonic Event'}
          </span>
          <span className="text-xs font-semibold text-emerald-400 font-vazir">
            {isFa ? activeEpoch.majorTectonicEventFa : activeEpoch.majorTectonicEventEn}
          </span>
        </div>
      </div>

      {/* Main Interactive Paleomap SVG Projection */}
      <div className="relative w-full aspect-[2/1] min-h-[300px] sm:min-h-[400px] bg-[#0A0E17] flex items-center justify-center overflow-hidden">
        {/* Graticule lines (Parallels & Meridians) */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-20">
          <defs>
            <pattern id="graticule" width="80" height="40" patternUnits="userSpaceOnUse">
              <path d="M 80 0 L 0 0 0 40" fill="none" stroke="#38BDF8" strokeWidth="0.5" strokeDasharray="2 3" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#graticule)" />
          <line x1="0" y1="50%" x2="100%" y2="50%" stroke="#F59E0B" strokeWidth="0.75" strokeDasharray="6 4" />
          <line x1="0" y1="35%" x2="100%" y2="35%" stroke="#64748B" strokeWidth="0.5" strokeDasharray="3 3" />
          <line x1="0" y1="65%" x2="100%" y2="65%" stroke="#64748B" strokeWidth="0.5" strokeDasharray="3 3" />
        </svg>

        {/* Dynamic Continents SVG Projection */}
        <svg
          viewBox="0 0 850 480"
          className="w-full h-full max-h-[440px] object-contain transition-all duration-700 ease-in-out relative z-10"
        >
          {/* Subtle Outer Geodesic Horizon */}
          <circle cx="425" cy="240" r="225" fill="none" stroke="#1E293B" strokeWidth="1" />
          <circle cx="425" cy="240" r="235" fill="none" stroke="#F59E0B" strokeWidth="0.75" strokeOpacity="0.4" strokeDasharray="4 6" />

          {/* Continents for active epoch */}
          <g className="transition-all duration-700 ease-in-out">
            {activeEpoch.svgContinents.map((continent, idx) => (
              <g key={idx}>
                <path
                  d={continent.path}
                  fill={continent.fill}
                  fillOpacity="0.9"
                  stroke="#F59E0B"
                  strokeWidth="1.25"
                  className="transition-all duration-700 hover:fill-opacity-100 hover:stroke-width-2 cursor-pointer drop-shadow-md"
                />
                <title>{continent.name}</title>
              </g>
            ))}
          </g>

          {/* Minimalist Compass Rose */}
          <g transform="translate(70, 70) scale(0.6)" opacity="0.6">
            <circle cx="0" cy="0" r="35" fill="none" stroke="#94A3B8" strokeWidth="1" strokeDasharray="2 3" />
            <line x1="0" y1="-40" x2="0" y2="40" stroke="#94A3B8" strokeWidth="1.5" />
            <line x1="-40" y1="0" x2="40" y2="0" stroke="#94A3B8" strokeWidth="1.5" />
            <polygon points="0,-40 4,-16 0,-22 -4,-16" fill="#F59E0B" />
            <polygon points="0,40 4,16 0,22 -4,16" fill="#64748B" />
            <text x="0" y="-45" textAnchor="middle" fill="#F59E0B" fontSize="12" fontWeight="bold" fontFamily="sans-serif">N</text>
          </g>
        </svg>

        {/* Informative Epoch Overlay Description */}
        <div className="absolute bottom-3 left-3 right-3 sm:bottom-4 sm:left-4 sm:right-4 z-20 pointer-events-none">
          <div className="bg-[#111827]/95 backdrop-blur-md border border-white/10 rounded-xl p-3 sm:p-4 max-w-2xl shadow-xl pointer-events-auto">
            <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-vazir">
              {isFa ? activeEpoch.descriptionFa : activeEpoch.descriptionEn}
            </p>
          </div>
        </div>
      </div>

      {/* Planetary Telemetry Indicators (CO2, Temp, Sea Level, Ice) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-white/10 border-t border-white/10">
        {/* CO2 Indicator */}
        <div className="bg-[#111827] p-3.5 sm:p-4 flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/25 flex items-center justify-center text-amber-400 shrink-0">
            <Wind className="w-4 h-4" />
          </div>
          <div>
            <span className="text-[11px] text-slate-400 font-vazir block">
              {isFa ? 'دی‌اکسید کربن (CO₂)' : 'Atmospheric CO₂'}
            </span>
            <div className="flex items-baseline gap-1 mt-0.5">
              <span className="text-base sm:text-lg font-bold font-num text-white">
                {activeEpoch.co2Ppm.toLocaleString()}
              </span>
              <span className="text-[11px] text-amber-400 font-num">ppm</span>
            </div>
          </div>
        </div>

        {/* Global Temperature Anomaly */}
        <div className="bg-[#111827] p-3.5 sm:p-4 flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-rose-500/10 border border-rose-500/25 flex items-center justify-center text-rose-400 shrink-0">
            <Thermometer className="w-4 h-4" />
          </div>
          <div>
            <span className="text-[11px] text-slate-400 font-vazir block">
              {isFa ? 'انحراف دما از امروز' : 'Temp Anomaly'}
            </span>
            <div className="flex items-baseline gap-1 mt-0.5">
              <span className="text-base sm:text-lg font-bold font-num text-white">
                {activeEpoch.tempAnomalyC > 0 ? `+${activeEpoch.tempAnomalyC}` : activeEpoch.tempAnomalyC}°
              </span>
              <span className="text-[11px] text-rose-400 font-num">°C</span>
            </div>
          </div>
        </div>

        {/* Sea Level */}
        <div className="bg-[#111827] p-3.5 sm:p-4 flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-cyan-500/10 border border-cyan-500/25 flex items-center justify-center text-cyan-400 shrink-0">
            <Waves className="w-4 h-4" />
          </div>
          <div>
            <span className="text-[11px] text-slate-400 font-vazir block">
              {isFa ? 'تراز آب دریاها' : 'Sea Level'}
            </span>
            <div className="flex items-baseline gap-1 mt-0.5">
              <span className="text-base sm:text-lg font-bold font-num text-white">
                {activeEpoch.seaLevelM > 0 ? `+${activeEpoch.seaLevelM}` : activeEpoch.seaLevelM}
              </span>
              <span className="text-[11px] text-cyan-400 font-num">{isFa ? 'متر' : 'm'}</span>
            </div>
          </div>
        </div>

        {/* Glacial Coverage */}
        <div className="bg-[#111827] p-3.5 sm:p-4 flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-emerald-500/10 border border-emerald-500/25 flex items-center justify-center text-emerald-400 shrink-0">
            <Mountain className="w-4 h-4" />
          </div>
          <div>
            <span className="text-[11px] text-slate-400 font-vazir block">
              {isFa ? 'پوشش یخچالی خشکی' : 'Ice Cover'}
            </span>
            <div className="flex items-baseline gap-1 mt-0.5">
              <span className="text-base sm:text-lg font-bold font-num text-white">
                {activeEpoch.iceCoverPct}%
              </span>
              <span className="text-[11px] text-emerald-400 font-num">{isFa ? 'خشکی‌ها' : 'of land'}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
