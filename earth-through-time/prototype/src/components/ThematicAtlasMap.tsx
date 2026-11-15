import React, { useState, useMemo } from 'react';
import { 
  Landmark, Cat, Flame, BookOpen, Palette, Music, 
  MapPin, Clock, Info, Globe, Sparkles, ChevronRight, Compass
} from 'lucide-react';
import { LanguageKey } from '../types';
import { 
  ThemeType, 
  THEME_CONFIGS, 
  HISTORICAL_BOUNDARY_EPOCHS, 
  THEMATIC_ENTITIES, 
  ThematicEntity,
  BoundaryEpoch 
} from '../data/thematicMapData';

interface ThematicAtlasMapProps {
  currentLang: LanguageKey;
  currentTime: number;
  onTimeChange: (time: number) => void;
}

export const ThematicAtlasMap: React.FC<ThematicAtlasMapProps> = ({
  currentLang,
  currentTime,
  onTimeChange,
}) => {
  const isFa = currentLang === 'fa';
  const [selectedTheme, setSelectedTheme] = useState<ThemeType>('civilization');
  const [selectedEntity, setSelectedEntity] = useState<ThematicEntity | null>(null);
  const [hoveredEntity, setHoveredEntity] = useState<ThematicEntity | null>(null);

  const themeConfig = THEME_CONFIGS[selectedTheme];

  // Helper to map icon names to Lucide icons
  const getThemeIcon = (type: ThemeType, className = "w-4 h-4") => {
    switch (type) {
      case 'civilization': return <Landmark className={className} />;
      case 'fauna': return <Cat className={className} />;
      case 'religion': return <Flame className={className} />;
      case 'literature': return <BookOpen className={className} />;
      case 'art': return <Palette className={className} />;
      case 'music': return <Music className={className} />;
    }
  };

  // Find the active boundary epoch for the current time
  const activeBoundaryEpoch: BoundaryEpoch = useMemo(() => {
    // If before early bronze age, return first
    if (currentTime <= -1200) return HISTORICAL_BOUNDARY_EPOCHS[0];
    if (currentTime <= -550) return HISTORICAL_BOUNDARY_EPOCHS[1];
    if (currentTime <= -330) return HISTORICAL_BOUNDARY_EPOCHS[2];
    if (currentTime <= 750) return HISTORICAL_BOUNDARY_EPOCHS[3];
    if (currentTime <= 1400) return HISTORICAL_BOUNDARY_EPOCHS[4];
    return HISTORICAL_BOUNDARY_EPOCHS[5];
  }, [currentTime]);

  // Filter entities matching the selected theme AND the current time range
  const activeEntities = useMemo(() => {
    return THEMATIC_ENTITIES.filter((entity) => {
      if (entity.theme !== selectedTheme) return false;
      // An entity is active if currentTime falls within its lifespan or buffer
      // If currentTime is far in deep time, check if it's within startYear & endYear
      const start = entity.startYear;
      const end = entity.endYear;
      const buffer = Math.max(80, Math.abs(end - start) * 0.4);
      return currentTime >= (start - buffer) && currentTime <= (end + buffer);
    });
  }, [selectedTheme, currentTime]);

  // All entities of this theme regardless of time (for the directory list)
  const allThemeEntities = useMemo(() => {
    return THEMATIC_ENTITIES.filter((e) => e.theme === selectedTheme);
  }, [selectedTheme]);

  return (
    <div className="space-y-5">
      {/* 1. Theme Switcher Bar with Dynamic Color Palette */}
      <div className="bg-[#111827] border border-white/10 rounded-2xl p-3 sm:p-4 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
          <div className="flex items-center gap-2">
            <div 
              className="w-8 h-8 rounded-xl flex items-center justify-center transition-colors duration-300"
              style={{ 
                backgroundColor: `${themeConfig.accentColor}20`,
                borderColor: `${themeConfig.accentColor}50`,
                borderWidth: '1px',
                color: themeConfig.accentColor
              }}
            >
              {getThemeIcon(selectedTheme, "w-4 h-4")}
            </div>
            <div>
              <span className="text-xs font-semibold block font-vazir text-slate-400">
                {isFa ? 'دسته‌بندی موضوعی لایه‌های نقشه:' : 'Active Thematic Layer:'}
              </span>
              <h3 className="text-base sm:text-lg font-bold font-vazir text-white">
                {isFa ? themeConfig.nameFa : themeConfig.nameEn}
              </h3>
            </div>
          </div>

          <span className="text-xs text-slate-400 font-vazir hidden md:inline">
            {isFa ? themeConfig.descriptionFa : themeConfig.descriptionEn}
          </span>
        </div>

        {/* The 6 Thematic Buttons */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
          {(Object.keys(THEME_CONFIGS) as ThemeType[]).map((tKey) => {
            const cfg = THEME_CONFIGS[tKey];
            const isSelected = selectedTheme === tKey;
            return (
              <button
                key={tKey}
                onClick={() => {
                  setSelectedTheme(tKey);
                  setSelectedEntity(null);
                }}
                className={`py-2.5 px-3 rounded-xl border text-xs font-bold font-vazir transition-all flex items-center gap-2 justify-center text-center ${
                  isSelected
                    ? 'shadow-md scale-[1.02]'
                    : 'bg-[#161F30] text-slate-300 hover:text-white hover:bg-slate-800 border-white/10'
                }`}
                style={isSelected ? {
                  backgroundColor: `${cfg.accentColor}25`,
                  borderColor: cfg.accentColor,
                  color: cfg.accentColor,
                } : {}}
              >
                {getThemeIcon(tKey, "w-3.5 h-3.5 shrink-0")}
                <span className="truncate">{isFa ? cfg.nameFa : cfg.nameEn}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 2. Interactive Historical Map Stage */}
      <div 
        className="w-full bg-[#111827] border rounded-3xl overflow-hidden shadow-2xl relative transition-colors duration-500"
        style={{ borderColor: `${themeConfig.accentColor}40` }}
      >
        {/* Map Top Status Bar */}
        <div className="bg-[#161F30] px-4 sm:px-6 py-3 border-b border-white/10 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div 
              className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{ 
                backgroundColor: `${themeConfig.accentColor}15`,
                color: themeConfig.accentColor 
              }}
            >
              <Compass className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs sm:text-sm font-bold text-white font-vazir">
                  {isFa ? 'نقشهٔ جغرافیایی و مرزهای فلات ایران و جهان' : 'Iranian Plateau & World Historical Geography'}
                </span>
                <span 
                  className="text-[11px] px-2.5 py-0.5 rounded-full font-vazir font-semibold"
                  style={{ 
                    backgroundColor: `${themeConfig.accentColor}20`,
                    color: themeConfig.accentColor,
                    borderColor: `${themeConfig.accentColor}40`,
                    borderWidth: '1px'
                  }}
                >
                  {isFa ? activeBoundaryEpoch.nameFa : activeBoundaryEpoch.nameEn}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-vazir mt-0.5">
                {isFa 
                  ? `${activeEntities.length} مورد فعال در این دوره زمانی بر روی نقشه`
                  : `${activeEntities.length} items active during this epoch`}
              </p>
            </div>
          </div>

          {/* Quick Epoch Selector Bar */}
          <div className="flex items-center gap-1 overflow-x-auto max-w-full pb-1 sm:pb-0">
            {HISTORICAL_BOUNDARY_EPOCHS.map((bEpoch) => {
              const isActive = activeBoundaryEpoch.id === bEpoch.id;
              return (
                <button
                  key={bEpoch.id}
                  onClick={() => onTimeChange((bEpoch.startYear + bEpoch.endYear) / 2)}
                  className={`px-2.5 py-1 rounded-lg text-[11px] whitespace-nowrap font-vazir transition-all border ${
                    isActive
                      ? 'font-bold shadow-sm'
                      : 'bg-slate-800 text-slate-400 hover:text-white border-white/5'
                  }`}
                  style={isActive ? {
                    backgroundColor: themeConfig.accentColor,
                    color: '#0B0F17',
                    borderColor: themeConfig.accentColor
                  } : {}}
                >
                  {isFa ? bEpoch.nameFa.split('(')[0] : bEpoch.nameEn.split('(')[0]}
                </button>
              );
            })}
          </div>
        </div>

        {/* SVG Geographic Map Canvas */}
        <div className="relative w-full aspect-[16/9] min-h-[380px] sm:min-h-[500px] bg-[#0A0E17] flex items-center justify-center overflow-hidden">
          {/* Subtle Cartographic Coordinate Grid */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-15">
            <defs>
              <pattern id="plateau-grid" width="60" height="60" patternUnits="userSpaceOnUse">
                <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#38BDF8" strokeWidth="0.5" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#plateau-grid)" />
          </svg>

          {/* Interactive Geographic Map SVG */}
          <svg
            viewBox="0 0 1000 580"
            className="w-full h-full max-h-[560px] object-contain select-none"
          >
            <defs>
              {/* Sea Water Gradient */}
              <radialGradient id="seaGrad" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#0B1B2B" />
                <stop offset="100%" stopColor="#07121F" />
              </radialGradient>

              {/* Landmass Shading */}
              <linearGradient id="landGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#1E293B" />
                <stop offset="50%" stopColor="#172233" />
                <stop offset="100%" stopColor="#111B28" />
              </linearGradient>

              {/* Mountain Relief Pattern */}
              <pattern id="mountainHatch" width="10" height="10" patternUnits="userSpaceOnUse">
                <path d="M-1,1 l2,-2 M0,10 l10,-10 M9,11 l2,-2" stroke="#334155" strokeWidth="0.75" opacity="0.4" />
              </pattern>
            </defs>

            {/* Continental Coastlines & Baseline Landmass (Centered on Near East, Iran, Central Asia) */}
            <g id="landmass-base">
              {/* Main Eurasian & Plateau Landmass */}
              <path
                d="M 120,80 Q 250,70 380,100 Q 520,70 700,90 Q 880,110 940,180 Q 920,320 840,400 Q 720,440 600,430 Q 480,450 360,420 Q 200,390 120,330 Z"
                fill="url(#landGrad)"
                stroke="#334155"
                strokeWidth="1.2"
              />

              {/* Caspian Sea (دریای مازندران) */}
              <path
                d="M 480,130 Q 515,110 525,160 Q 535,210 495,225 Q 465,190 480,130 Z"
                fill="#0F243A"
                stroke="#38BDF8"
                strokeWidth="1.5"
                strokeOpacity="0.8"
              />

              {/* Persian Gulf & Gulf of Oman (خلیج فارس و دریای عمان) */}
              <path
                d="M 420,330 Q 490,320 540,360 Q 580,380 620,370 Q 570,410 480,380 Q 430,360 420,330 Z"
                fill="#0F243A"
                stroke="#38BDF8"
                strokeWidth="1.5"
                strokeOpacity="0.8"
              />

              {/* Black Sea (دریای سیاه) */}
              <path
                d="M 280,130 Q 360,120 380,160 Q 330,185 270,170 Z"
                fill="#0F243A"
                stroke="#38BDF8"
                strokeWidth="1"
                strokeOpacity="0.6"
              />

              {/* Mediterranean Sea Eastern Basin */}
              <path
                d="M 160,200 Q 280,190 320,240 Q 260,280 180,260 Z"
                fill="#0F243A"
                stroke="#38BDF8"
                strokeWidth="1"
                strokeOpacity="0.6"
              />

              {/* Red Sea */}
              <path
                d="M 290,290 Q 330,340 370,410 Q 350,430 310,360 Z"
                fill="#0F243A"
                stroke="#38BDF8"
                strokeWidth="1"
                strokeOpacity="0.6"
              />

              {/* Zagros Mountain Arc (رشته‌کوه زاگرس) */}
              <path
                d="M 410,210 Q 460,270 520,330"
                fill="none"
                stroke="#64748B"
                strokeWidth="12"
                strokeLinecap="round"
                strokeDasharray="3 4"
                opacity="0.35"
              />

              {/* Alborz Mountain Range (رشته‌کوه البرز) */}
              <path
                d="M 460,215 Q 520,225 580,215"
                fill="none"
                stroke="#64748B"
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray="2 3"
                opacity="0.35"
              />

              {/* Great Kavir & Lut Basins (کویر مرکزی و لوت) */}
              <ellipse cx="560" cy="270" rx="35" ry="20" fill="#92400E" fillOpacity="0.12" stroke="#D97706" strokeWidth="0.5" strokeDasharray="3 3" />
            </g>

            {/* Geographic Landmark Text Labels */}
            <g id="geographic-labels" className="pointer-events-none select-none text-[10px] font-vazir" opacity="0.65">
              <text x="500" y="175" fill="#38BDF8" fontSize="10" fontWeight="bold" textAnchor="middle">
                {isFa ? 'دریای کاسپین' : 'Caspian Sea'}
              </text>
              <text x="510" y="365" fill="#38BDF8" fontSize="11" fontWeight="bold" textAnchor="middle">
                {isFa ? 'خلیج فارس' : 'Persian Gulf'}
              </text>
              <text x="360" y="270" fill="#64748B" fontSize="10" textAnchor="middle">
                {isFa ? 'بین‌النهرین' : 'Mesopotamia'}
              </text>
              <text x="545" y="255" fill="#CBD5E1" fontSize="13" fontWeight="bold" textAnchor="middle" opacity="0.8">
                {isFa ? 'فـلات ایـران' : 'IRANIAN PLATEAU'}
              </text>
              <text x="440" y="260" fill="#64748B" fontSize="9" textAnchor="middle" transform="rotate(-30 440,260)">
                {isFa ? 'رشته‌کوه زاگرس' : 'Zagros Range'}
              </text>
              <text x="645" y="220" fill="#64748B" fontSize="9" textAnchor="middle">
                {isFa ? 'خراسان بزرگ' : 'Greater Khorasan'}
              </text>
              <text x="730" y="320" fill="#64748B" fontSize="9" textAnchor="middle">
                {isFa ? 'دره سند' : 'Indus Valley'}
              </text>
            </g>

            {/* Dynamic Historical Boundary Shifts & Territories */}
            <g id="historical-territories">
              {activeBoundaryEpoch.territories.map((terr, idx) => (
                <g key={idx} className="transition-all duration-700">
                  <path
                    d={terr.path}
                    fill={terr.fillColor}
                    fillOpacity="0.16"
                    stroke={terr.fillColor}
                    strokeWidth="2"
                    strokeDasharray="6 4"
                    className="hover:fill-opacity-30 transition-all cursor-pointer"
                  />
                  {/* Territory Label in SVG */}
                  <text
                    x={terr.path.includes('440') ? '470' : '520'}
                    y={terr.path.includes('290') ? '310' : '260'}
                    fill={terr.fillColor}
                    fontSize="11"
                    fontWeight="bold"
                    textAnchor="middle"
                    className="pointer-events-none font-vazir drop-shadow-md"
                  >
                    {isFa ? terr.empireNameFa : terr.empireNameEn}
                  </text>
                </g>
              ))}
            </g>

            {/* Dynamic Thematic Location Markers & Entities */}
            <g id="thematic-markers">
              {activeEntities.map((entity) => {
                const isSelected = selectedEntity?.id === entity.id;
                const isHovered = hoveredEntity?.id === entity.id;
                const { x, y } = entity.mapCoord;

                return (
                  <g
                    key={entity.id}
                    transform={`translate(${x}, ${y})`}
                    onClick={() => setSelectedEntity(entity)}
                    onMouseEnter={() => setHoveredEntity(entity)}
                    onMouseLeave={() => setHoveredEntity(null)}
                    className="cursor-pointer group"
                  >
                    {/* Glowing Pulse Ring for active pin */}
                    <circle
                      cx="0"
                      cy="0"
                      r={isSelected || isHovered ? "22" : "14"}
                      fill={themeConfig.accentColor}
                      fillOpacity={isSelected ? "0.35" : "0.15"}
                      className="transition-all duration-300 animate-pulse"
                    />

                    {/* Central Marker Circle */}
                    <circle
                      cx="0"
                      cy="0"
                      r={isSelected ? "11" : "8"}
                      fill={themeConfig.accentColor}
                      stroke="#FFFFFF"
                      strokeWidth={isSelected ? "2.5" : "1.5"}
                      className="transition-all duration-300 shadow-xl group-hover:scale-125"
                    />

                    {/* Marker Title Label on Map */}
                    <text
                      x="0"
                      y={y > 340 ? -16 : 22}
                      textAnchor="middle"
                      fill="#FFFFFF"
                      fontSize={isSelected ? "12" : "10"}
                      fontWeight="bold"
                      fontFamily="Vazirmatn, sans-serif"
                      className="pointer-events-none drop-shadow-lg transition-all"
                      style={{
                        paintOrder: 'stroke',
                        stroke: '#0B0F17',
                        strokeWidth: '3px',
                        strokeLinejoin: 'round',
                      }}
                    >
                      {isFa ? entity.nameFa : entity.nameEn}
                    </text>
                  </g>
                );
              })}
            </g>
          </svg>

          {/* Active Hover / Floating Info Chip in Map Corner */}
          {(hoveredEntity || activeEntities[0]) && (
            <div className="absolute top-3 left-3 sm:top-4 sm:left-4 z-20 pointer-events-none max-w-xs">
              <div 
                className="bg-[#111827]/95 backdrop-blur-md border rounded-xl p-3 shadow-2xl transition-all"
                style={{ borderColor: `${themeConfig.accentColor}50` }}
              >
                <div className="flex items-center gap-1.5 mb-1">
                  <span 
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: themeConfig.accentColor }}
                  />
                  <span className="text-[11px] font-vazir font-semibold" style={{ color: themeConfig.accentColor }}>
                    {isFa ? themeConfig.nameFa : themeConfig.nameEn}
                  </span>
                  <span className="text-[10px] text-slate-400 font-num">
                    {(hoveredEntity || activeEntities[0]).periodLabelFa}
                  </span>
                </div>
                <h4 className="text-xs sm:text-sm font-bold text-white font-vazir">
                  {isFa ? (hoveredEntity || activeEntities[0]).nameFa : (hoveredEntity || activeEntities[0]).nameEn}
                </h4>
                <p className="text-[11px] text-slate-300 font-vazir mt-0.5 line-clamp-2">
                  {isFa ? (hoveredEntity || activeEntities[0]).summaryFa : (hoveredEntity || activeEntities[0]).summaryEn}
                </p>
                <span className="text-[10px] text-amber-400/80 font-vazir mt-1 block">
                  {isFa ? 'برای جزئیات بیشتر کلیک کنید ←' : 'Click marker for full dossier →'}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Dynamic Boundary Era Banner */}
        <div className="bg-[#161F30] p-4 border-t border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="space-y-0.5">
            <span className="text-[11px] font-semibold text-slate-400 font-vazir flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-amber-400" />
              <span>{isFa ? 'دورهٔ فعال خط مرزی در نقشه:' : 'Current Boundary Horizon:'}</span>
              <span className="text-white font-bold">{isFa ? activeBoundaryEpoch.nameFa : activeBoundaryEpoch.nameEn}</span>
            </span>
            <p className="text-xs text-slate-300 font-vazir">
              {isFa ? activeBoundaryEpoch.descriptionFa : activeBoundaryEpoch.descriptionEn}
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <span className="text-xs text-slate-400 font-vazir">{isFa ? 'تغییر زمان:' : 'Shift Era:'}</span>
            <button
              onClick={() => onTimeChange(Math.max(-4000, currentTime - 500))}
              className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-white/10 font-vazir"
            >
              ← {isFa ? '۵۰۰ سال قبل' : '-500y'}
            </button>
            <button
              onClick={() => onTimeChange(Math.min(1800, currentTime + 500))}
              className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-white/10 font-vazir"
            >
              {isFa ? '۵۰۰ سال بعد' : '+500y'} →
            </button>
          </div>
        </div>
      </div>

      {/* 3. Thematic Directory & Contemporaries Grid */}
      <div className="bg-[#111827] border border-white/10 rounded-2xl p-5 sm:p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 pb-3 border-b border-white/10">
          <div>
            <span 
              className="text-xs font-semibold font-vazir flex items-center gap-1.5"
              style={{ color: themeConfig.accentColor }}
            >
              {getThemeIcon(selectedTheme, "w-4 h-4")}
              <span>{isFa ? `فهرست ثبت‌شده: ${themeConfig.nameFa}` : `Documented Catalog: ${themeConfig.nameEn}`}</span>
            </span>
            <h3 className="text-lg sm:text-xl font-bold font-vazir text-white mt-1">
              {isFa ? 'شناسنامه‌ها و چهره‌های شاخص این دسته‌بندی' : 'Key Figures & Records in this Dimension'}
            </h3>
          </div>
          <span className="text-xs text-slate-400 font-vazir">
            {isFa ? 'برای باز کردن شناسنامه کامل روی هر کارت کلیک کنید' : 'Click to inspect complete dossier'}
          </span>
        </div>

        {/* Grid of All Entities for this Theme */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {allThemeEntities.map((entity) => {
            const isCurrentlyActive = activeEntities.some((ae) => ae.id === entity.id);
            const isSelected = selectedEntity?.id === entity.id;

            return (
              <div
                key={entity.id}
                onClick={() => {
                  setSelectedEntity(entity);
                  // Align timeline to the center of this entity's life
                  onTimeChange((entity.startYear + entity.endYear) / 2);
                }}
                className={`rounded-2xl p-4 sm:p-5 border transition-all cursor-pointer flex flex-col justify-between group shadow-lg ${
                  isSelected
                    ? 'ring-2 scale-[1.01]'
                    : isCurrentlyActive
                    ? 'bg-[#161F30] border-white/20 hover:border-white/40'
                    : 'bg-[#111827] border-white/5 opacity-80 hover:opacity-100 hover:bg-[#161F30]'
                }`}
                style={isSelected ? {
                  backgroundColor: `${themeConfig.accentColor}15`,
                  borderColor: themeConfig.accentColor,
                  outlineColor: themeConfig.accentColor,
                } : {}}
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-[11px] font-vazir text-slate-400">
                      {isFa ? entity.mapCoord.regionNameFa : entity.mapCoord.regionNameEn}
                    </span>
                    {isCurrentlyActive ? (
                      <span 
                        className="text-[11px] px-2 py-0.5 rounded-full font-bold font-vazir"
                        style={{
                          backgroundColor: `${themeConfig.accentColor}25`,
                          color: themeConfig.accentColor,
                          border: `1px solid ${themeConfig.accentColor}50`
                        }}
                      >
                        {isFa ? 'هم‌زمان با اسلایدر' : 'Active on Map'}
                      </span>
                    ) : (
                      <span className="text-[11px] font-num text-slate-400">
                        {isFa ? entity.periodLabelFa : entity.periodLabelEn}
                      </span>
                    )}
                  </div>

                  <h4 className="text-base sm:text-lg font-bold font-vazir text-white group-hover:text-white transition-colors mb-1">
                    {isFa ? entity.nameFa : entity.nameEn}
                  </h4>

                  <div 
                    className="text-xs font-semibold font-vazir mb-2"
                    style={{ color: themeConfig.accentColor }}
                  >
                    {isFa ? entity.titleOrSubtitleFa : entity.titleOrSubtitleEn}
                  </div>

                  <p className="text-xs text-slate-300 font-vazir line-clamp-3 leading-relaxed">
                    {isFa ? entity.summaryFa : entity.summaryEn}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-slate-400 font-vazir">
                  <span className="flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5" style={{ color: themeConfig.accentColor }} />
                    <span>{isFa ? 'پرش به زمان و مکان' : 'Jump to Era'}</span>
                  </span>
                  <span className="font-bold group-hover:translate-x-1 transition-transform" style={{ color: themeConfig.accentColor }}>
                    ←
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 4. Complete Detailed Dossier Modal */}
      {selectedEntity && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md">
          <div 
            className="bg-[#111827] border rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 shadow-2xl relative text-[#F1F5F9] font-vazir"
            style={{ borderColor: `${themeConfig.accentColor}60` }}
          >
            <button
              onClick={() => setSelectedEntity(null)}
              className="absolute top-5 left-5 sm:left-auto sm:right-5 text-slate-400 hover:text-white text-base font-bold bg-[#161F30] w-8 h-8 rounded-full flex items-center justify-center border border-white/10"
            >
              ✕
            </button>

            {/* Dossier Header */}
            <div className="flex items-center gap-3 mb-5 border-b border-white/10 pb-4">
              <div 
                className="w-12 h-12 rounded-2xl flex items-center justify-center text-xl shadow-lg shrink-0"
                style={{ 
                  backgroundColor: `${themeConfig.accentColor}20`,
                  border: `1px solid ${themeConfig.accentColor}50`,
                  color: themeConfig.accentColor
                }}
              >
                {getThemeIcon(selectedEntity.theme, "w-6 h-6")}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span 
                    className="text-xs font-semibold uppercase font-vazir"
                    style={{ color: themeConfig.accentColor }}
                  >
                    {isFa ? themeConfig.nameFa : themeConfig.nameEn}
                  </span>
                  <span className="text-[11px] font-num text-slate-400">
                    · {isFa ? selectedEntity.periodLabelFa : selectedEntity.periodLabelEn}
                  </span>
                </div>
                <h3 className="text-xl sm:text-2xl font-bold text-white mt-0.5">
                  {isFa ? selectedEntity.nameFa : selectedEntity.nameEn}
                </h3>
                <p className="text-xs text-slate-300 mt-0.5 font-vazir">
                  {isFa ? selectedEntity.titleOrSubtitleFa : selectedEntity.titleOrSubtitleEn}
                </p>
              </div>
            </div>

            {/* Main Detailed Description */}
            <div className="space-y-4 text-xs sm:text-sm font-vazir leading-relaxed text-slate-200 mb-6">
              <p className="bg-[#161F30] p-4 rounded-xl border border-white/10">
                {isFa ? selectedEntity.detailsFa.description : selectedEntity.detailsEn.description}
              </p>

              {/* Famous Quote or Poetry if available */}
              {(selectedEntity.detailsFa.quoteOrTextFa || selectedEntity.detailsEn.quoteOrTextEn) && (
                <div 
                  className="p-4 rounded-xl border italic text-center font-semibold"
                  style={{
                    backgroundColor: `${themeConfig.accentColor}10`,
                    borderColor: `${themeConfig.accentColor}35`,
                    color: themeConfig.accentColor
                  }}
                >
                  « {isFa ? selectedEntity.detailsFa.quoteOrTextFa : selectedEntity.detailsEn.quoteOrTextEn} »
                </div>
              )}

              {/* Key Achievements or Characteristics */}
              <div className="bg-[#161F30] p-4 rounded-xl border border-white/10 space-y-2">
                <span className="text-xs font-bold text-amber-400 block mb-1">
                  {isFa ? 'ویژگی‌ها و دستاوردهای شاخص:' : 'Key Feats & Characteristics:'}
                </span>
                <ul className="space-y-1.5 text-xs text-slate-300">
                  {(isFa ? selectedEntity.detailsFa.keyAchievements : selectedEntity.detailsEn.keyAchievements).map((ach, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-amber-400 font-bold">•</span>
                      <span>{ach}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Contemporaries */}
              <div className="bg-[#161F30] p-4 rounded-xl border border-white/10">
                <span className="text-xs font-bold text-cyan-400 block mb-1">
                  {isFa ? 'هم‌عصران و رویدادهای تاریخی هم‌زمان در جهان:' : 'Global Contemporaries & Events:'}
                </span>
                <p className="text-xs text-slate-300">
                  {isFa ? selectedEntity.detailsFa.contemporaryEventsFa : selectedEntity.detailsEn.contemporaryEventsEn}
                </p>
              </div>
            </div>

            {/* Bottom Actions */}
            <div className="flex gap-2">
              <button
                onClick={() => {
                  onTimeChange((selectedEntity.startYear + selectedEntity.endYear) / 2);
                  setSelectedEntity(null);
                }}
                className="flex-1 py-2.5 rounded-xl font-bold font-vazir text-xs transition-colors shadow-sm"
                style={{
                  backgroundColor: themeConfig.accentColor,
                  color: '#0A0E17'
                }}
              >
                {isFa ? 'پرش نوار زمان به این دوره' : 'Jump Timeline to this Epoch'}
              </button>
              <button
                onClick={() => setSelectedEntity(null)}
                className="px-5 py-2.5 rounded-xl bg-slate-800 text-slate-300 hover:text-white font-bold font-vazir text-xs transition-colors"
              >
                {isFa ? 'بستن' : 'Close'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
