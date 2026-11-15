import React, { useState } from 'react';
import { Globe, Volume2, VolumeX, RotateCcw, Share2, Compass } from 'lucide-react';
import { LanguageKey } from '../types';
import { ambientSound } from '../utils/audioSynth';

interface HeaderProps {
  currentLang: LanguageKey;
  onLanguageChange: (lang: LanguageKey) => void;
  activeLens: 'thematicMap' | 'earth' | 'life' | 'civilizations' | 'iran' | 'sources';
  onSelectLens: (lens: 'thematicMap' | 'earth' | 'life' | 'civilizations' | 'iran' | 'sources') => void;
  onOpenDeployModal: () => void;
  onResetTime: () => void;
  currentEpochName: string;
}

export const Header: React.FC<HeaderProps> = ({
  currentLang,
  onLanguageChange,
  activeLens,
  onSelectLens,
  onOpenDeployModal,
  onResetTime,
  currentEpochName,
}) => {
  const isFa = currentLang === 'fa';
  const [isAudioActive, setIsAudioActive] = useState(false);

  const toggleAudio = () => {
    const active = ambientSound.toggle();
    setIsAudioActive(active);
  };

  return (
    <header className="sticky top-0 z-40 bg-[#0A0E17]/95 backdrop-blur-md border-b border-white/10">
      <div className="max-w-7xl mx-auto px-3 sm:px-6 h-14 sm:h-16 flex items-center justify-between gap-3">
        {/* Logo & Current Focus */}
        <div className="flex items-center gap-2.5 sm:gap-3 cursor-pointer select-none" onClick={onResetTime}>
          <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-gradient-to-tr from-amber-500/20 to-emerald-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400 shrink-0 shadow-sm">
            <Compass className="w-4 h-4 sm:w-5 sm:h-5 animate-spin-slow" />
          </div>

          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className="text-base sm:text-lg font-bold text-white tracking-normal font-vazir leading-tight">
                {isFa ? 'کرونو اطلس' : 'Chrono Atlas'}
              </span>
              <span className="hidden md:inline text-[11px] px-2 py-0.5 rounded-md bg-white/5 text-slate-300 border border-white/10 font-num">
                {currentEpochName}
              </span>
            </div>
            <span className="text-[11px] text-slate-400 hidden sm:inline leading-none">
              {isFa ? 'اطلس زمین و حیات در گذر زمان' : 'Interactive Atlas of Deep Time'}
            </span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-1.5 sm:gap-2.5">
          {/* Ambient Sound Button */}
          <button
            onClick={toggleAudio}
            className={`p-2 rounded-xl text-xs border transition-all flex items-center gap-1.5 ${
              isAudioActive
                ? 'bg-amber-500/15 text-amber-400 border-amber-500/40 shadow-sm'
                : 'bg-white/5 text-slate-400 border-white/10 hover:text-white hover:bg-white/10'
            }`}
            title={isFa ? 'صدای محیطی زمان عمیق' : 'Deep Time Ambient Audio'}
          >
            {isAudioActive ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            <span className="hidden sm:inline text-xs font-vazir">
              {isAudioActive ? (isFa ? 'صدا روشن' : 'Audio On') : (isFa ? 'صدا' : 'Mute')}
            </span>
          </button>

          {/* Reset to Present Button */}
          <button
            onClick={onResetTime}
            className="p-2 rounded-xl text-xs bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white border border-white/10 transition-all flex items-center gap-1"
            title={isFa ? 'بازنشانی به زمان حال' : 'Reset to Present'}
          >
            <RotateCcw className="w-4 h-4" />
            <span className="hidden md:inline text-xs font-vazir">
              {isFa ? 'زمان حال' : 'Now'}
            </span>
          </button>

          {/* Share / Link Modal */}
          <button
            onClick={onOpenDeployModal}
            className="p-2 rounded-xl text-xs bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition-all flex items-center gap-1 shadow-sm"
            title={isFa ? 'اشتراک‌گذاری و لینک آنلاین' : 'Share & Online Link'}
          >
            <Share2 className="w-4 h-4" />
            <span className="text-xs font-vazir">
              {isFa ? 'اشتراک' : 'Share'}
            </span>
          </button>

          {/* Clean Language Selector */}
          <div className="flex items-center bg-white/5 border border-white/10 rounded-xl p-0.5 text-xs">
            <button
              onClick={() => onLanguageChange('fa')}
              className={`px-2 py-1 rounded-lg transition-all font-medium font-vazir ${
                currentLang === 'fa'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              فا
            </button>
            <button
              onClick={() => onLanguageChange('en')}
              className={`px-2 py-1 rounded-lg transition-all font-medium ${
                currentLang === 'en'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              EN
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
