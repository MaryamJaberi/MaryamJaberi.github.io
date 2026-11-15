import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, FastForward, Clock } from 'lucide-react';
import { LanguageKey } from '../types';
import { ambientSound } from '../utils/audioSynth';

interface MasterTimelineControllerProps {
  currentLang: LanguageKey;
  currentTime: number;
  onTimeChange: (newTime: number) => void;
  scaleMode: 'log' | 'linear';
  onScaleModeChange: (mode: 'log' | 'linear') => void;
}

export const MasterTimelineController: React.FC<MasterTimelineControllerProps> = ({
  currentLang,
  currentTime,
  onTimeChange,
  scaleMode,
  onScaleModeChange,
}) => {
  const isFa = currentLang === 'fa';
  const [isPlaying, setIsPlaying] = useState(false);
  const [playSpeed, setPlaySpeed] = useState<number>(1);

  // Key historical & deep-time bookmarks
  const keyEpochs = [
    { labelEn: 'Big Bang', labelFa: 'مهبانگ', time: -13800000000, category: 'cosmos' },
    { labelEn: 'Earth Born', labelFa: 'پیدایش زمین', time: -4540000000, category: 'geology' },
    { labelEn: 'First Life', labelFa: 'آغاز حیات', time: -3800000000, category: 'biology' },
    { labelEn: 'Cambrian', labelFa: 'انفجار کامبرین', time: -541000000, category: 'biology' },
    { labelEn: 'Permian Die-off', labelFa: 'انقراض پرمین', time: -252000000, category: 'extinction' },
    { labelEn: 'K-Pg Asteroid', labelFa: 'انقراض کرتاسه', time: -66000000, category: 'extinction' },
    { labelEn: 'First Cities (Elam)', labelFa: 'تمدن عیلام', time: -5200, category: 'civilization' },
    { labelEn: 'Achaemenid Era', labelFa: 'هخامنشیان', time: -2570, category: 'civilization' },
    { labelEn: 'Islamic Golden Age', labelFa: 'دوران زرین دانش', time: -1100, category: 'civilization' },
    { labelEn: 'Present Day', labelFa: 'عصر حاضر', time: 0, category: 'modern' },
    { labelEn: '+1,000y Future', labelFa: '+۱۰۰۰ سال سناریو', time: 1000, category: 'future' },
  ];

  // Helper to format any time number into human-readable text
  const formatTimeDisplay = (time: number): { en: string; fa: string; subEn: string; subFa: string } => {
    if (time <= -1000000000) {
      const billions = (Math.abs(time) / 1000000000).toFixed(1);
      return {
        en: `${billions} Billion Years Ago`,
        fa: `${billions} میلیارد سال پیش`,
        subEn: 'Cosmic & Geological Deep Time',
        subFa: 'زمان عمیق کیهانی و زمین‌شناسی',
      };
    }
    if (time <= -1000000) {
      const millions = Math.round(Math.abs(time) / 1000000);
      return {
        en: `${millions} Million Years Ago (Ma)`,
        fa: `${millions} میلیون سال پیش`,
        subEn: 'Phanerozoic Biological Radiation',
        subFa: 'دوران زیستی فانروزوئیک',
      };
    }
    if (time <= -10000) {
      const thousands = Math.round(Math.abs(time) / 1000);
      return {
        en: `${thousands},000 Years Ago (ka)`,
        fa: `${thousands} هزار سال پیش`,
        subEn: 'Late Pleistocene / Ice Age',
        subFa: 'عصر یخبندان و پراکندگی انسان',
      };
    }
    if (time < 0) {
      const bce = Math.abs(time);
      return {
        en: `${bce} BCE`,
        fa: `${bce} پیش از میلاد`,
        subEn: 'Human Historical Horizons',
        subFa: 'تاریخ تمدن و دولت‌داری بشر',
      };
    }
    if (time === 0) {
      return {
        en: 'Present Day (2026 CE)',
        fa: 'عصر حاضر (۲۰۲۶ میلادی)',
        subEn: 'Anthropocene & Global Era',
        subFa: 'عصر آنتروپوسن و تمدن امروز',
      };
    }
    return {
      en: `+${time} Years into Future`,
      fa: `+${time} سال در آینده`,
      subEn: 'Climate & Geosphere Scenarios',
      subFa: 'سناریوهای مدل‌سازی اقلیم و زمین',
    };
  };

  const sliderToTime = (val: number): number => {
    if (val === 900) return 0;
    if (val > 900) {
      const fraction = (val - 900) / 100;
      return Math.round(fraction * 1000);
    }
    if (val >= 700 && val < 900) {
      const fraction = (val - 700) / 200;
      return Math.round(-10000 * (1 - fraction));
    }
    const fraction = val / 700;
    const minLog = Math.log10(10000);
    const maxLog = Math.log10(13800000000);
    const logVal = maxLog - fraction * (maxLog - minLog);
    return -Math.round(Math.pow(10, logVal));
  };

  const timeToSlider = (time: number): number => {
    if (time > 0) {
      const frac = Math.min(1, time / 1000);
      return 900 + frac * 100;
    }
    if (time === 0) return 900;
    if (time >= -10000) {
      const frac = (time + 10000) / 10000;
      return 700 + frac * 200;
    }
    const minLog = Math.log10(10000);
    const maxLog = Math.log10(13800000000);
    const logVal = Math.log10(Math.abs(time));
    const clampedLog = Math.min(maxLog, Math.max(minLog, logVal));
    const frac = (maxLog - clampedLog) / (maxLog - minLog);
    return frac * 700;
  };

  useEffect(() => {
    let interval: any = null;
    if (isPlaying) {
      interval = setInterval(() => {
        const currentSlider = timeToSlider(currentTime);
        if (currentSlider >= 1000) {
          setIsPlaying(false);
          return;
        }
        const nextSlider = Math.min(1000, currentSlider + playSpeed * 1.5);
        const nextTime = sliderToTime(nextSlider);

        if (Math.abs(currentSlider - 250) < 5 || Math.abs(currentSlider - 550) < 5) {
          ambientSound.playEpochTick(true);
        }
        onTimeChange(nextTime);
      }, 50);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPlaying, playSpeed, currentTime]);

  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseFloat(e.target.value);
    const computedTime = sliderToTime(val);
    onTimeChange(computedTime);
    ambientSound.playEpochTick(Math.abs(computedTime + 252000000) < 20000000);
  };

  const display = formatTimeDisplay(currentTime);

  return (
    <div className="w-full bg-[#111827] border border-white/10 rounded-2xl p-4 sm:p-6 shadow-xl text-[#F1F5F9]">
      {/* Top Controller Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-white/10">
        {/* Active Time Horizon readout */}
        <div>
          <span className="text-[11px] font-medium text-amber-400 font-vazir block mb-0.5">
            {isFa ? 'موقعیت زمانی فعال در اطلس:' : 'Active Continuum Coordinate:'}
          </span>
          <div className="flex items-baseline gap-2">
            <h2 className="text-xl sm:text-2xl font-bold font-vazir text-white">
              {isFa ? display.fa : display.en}
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-vazir mt-0.5">
            {isFa ? display.subFa : display.subEn}
          </p>
        </div>

        {/* Playback & Velocity Controls */}
        <div className="flex items-center gap-2 self-start sm:self-auto">
          <button
            onClick={() => {
              setIsPlaying(!isPlaying);
              if (!isPlaying) ambientSound.start();
            }}
            className={`px-4 py-2 rounded-xl text-xs font-bold font-vazir transition-all flex items-center gap-1.5 shadow-sm ${
              isPlaying
                ? 'bg-rose-600 hover:bg-rose-500 text-white'
                : 'bg-amber-500 hover:bg-amber-400 text-slate-950'
            }`}
          >
            {isPlaying ? (
              <>
                <Pause className="w-3.5 h-3.5" />
                <span>{isFa ? 'توقف مرور' : 'Pause'}</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>{isFa ? 'مرور خودکار' : 'Play'}</span>
              </>
            )}
          </button>

          <button
            onClick={() => setPlaySpeed(playSpeed === 1 ? 5 : playSpeed === 5 ? 15 : 1)}
            className="px-2.5 py-2 rounded-xl text-xs font-num font-bold bg-white/5 hover:bg-white/10 text-amber-400 border border-white/10 flex items-center gap-1"
            title="Cycle play speed"
          >
            <FastForward className="w-3.5 h-3.5" />
            <span>{playSpeed}x</span>
          </button>

          <button
            onClick={() => {
              onTimeChange(0);
              ambientSound.playEpochTick(false);
            }}
            className="px-3 py-2 rounded-xl text-xs font-medium font-vazir bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 flex items-center gap-1.5 transition-colors"
            title={isFa ? 'پرش به زمان معاصر' : 'Reset to Present'}
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>{isFa ? 'اکنون' : 'Now'}</span>
          </button>
        </div>
      </div>

      {/* Main Interactive Slider */}
      <div className="relative my-5 px-1">
        {/* Scale Range Markers */}
        <div className="flex justify-between text-[11px] font-num text-slate-400 mb-2 px-1">
          <span className="text-rose-400 font-semibold">-13.8 Ga</span>
          <span className="hidden sm:inline text-amber-400">-252 Ma (Pangaea)</span>
          <span className="hidden sm:inline text-cyan-400">-5200 BCE (Elam)</span>
          <span className="text-white font-bold">0 CE (Present)</span>
          <span className="text-emerald-400">+1,000y</span>
        </div>

        {/* Range Slider Track */}
        <div className="relative flex items-center">
          <input
            id="master-time-scrubber"
            type="range"
            min="0"
            max="1000"
            step="1"
            value={timeToSlider(currentTime)}
            onChange={handleSliderChange}
            className="w-full h-2.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500/40 border border-white/10"
          />
        </div>

        {/* Subtle direction guides */}
        <div className="flex justify-between items-center text-[11px] text-slate-400 mt-2 px-1 font-vazir">
          <span>{isFa ? '← زمان عمیق (مهبانگ و پیدایش سیاره)' : '← Deep Time'}</span>
          <span>{isFa ? 'تاریخ تمدن و سناریوهای آینده →' : 'Civilizations & Future →'}</span>
        </div>
      </div>

      {/* Quick Jump Epoch Pills */}
      <div className="mt-3 pt-3 border-t border-white/10">
        <div className="text-xs font-medium text-slate-300 mb-2 flex items-center gap-1.5 font-vazir">
          <Clock className="w-3.5 h-3.5 text-amber-400" />
          <span>{isFa ? 'ایستگاه‌های عطف تاریخی:' : 'Pivotal Bookmarks:'}</span>
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
          {keyEpochs.map((ep, idx) => {
            const isActive = Math.abs(currentTime - ep.time) < Math.max(50, Math.abs(ep.time) * 0.15);
            return (
              <button
                key={idx}
                onClick={() => {
                  onTimeChange(ep.time);
                  ambientSound.playEpochTick(ep.category === 'extinction');
                }}
                className={`px-3 py-1.5 rounded-lg text-xs whitespace-nowrap transition-all font-vazir border shrink-0 ${
                  isActive
                    ? 'bg-amber-500 text-slate-950 font-bold border-amber-500 shadow-sm'
                    : ep.category === 'extinction'
                    ? 'bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border-rose-500/30'
                    : 'bg-white/5 hover:bg-white/10 text-slate-300 border-white/10'
                }`}
              >
                {isFa ? ep.labelFa : ep.labelEn}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
