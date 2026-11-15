import React from 'react';
import { Github, Globe, Compass } from 'lucide-react';
import { LanguageKey } from '../types';
import { GITHUB_REPO_URL } from '../data/projectData';

interface FooterProps {
  currentLang: LanguageKey;
  onOpenDeployModal: () => void;
}

export const Footer: React.FC<FooterProps> = ({ currentLang, onOpenDeployModal }) => {
  const isFa = currentLang === 'fa';

  return (
    <footer className="border-t border-white/10 bg-[#0A0E17] py-8 mt-12 text-slate-400 font-vazir">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3 text-center md:text-left">
          <div className="w-8 h-8 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0">
            <Compass className="w-4 h-4" />
          </div>
          <div>
            <span className="text-sm sm:text-base font-bold text-white block">
              {isFa ? 'کرونو اطلس — اطلس تعاملی زمین و زمان' : 'Chrono Atlas — Earth Through Time'}
            </span>
            <p className="text-xs text-slate-400 mt-0.5">
              {isFa
                ? 'پژوهش و مصورسازی تاریخ زمین، زیست‌کره و تمدن‌های بشری'
                : 'Interactive paleogeography, macroevolution, and civilizational history'}
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-4 text-xs">
          <button
            onClick={onOpenDeployModal}
            className="hover:text-amber-400 transition-colors flex items-center gap-1.5 text-amber-400 font-semibold"
          >
            <Globe className="w-3.5 h-3.5" />
            <span>{isFa ? 'لینک مستقیم و اشتراک' : 'Share & Online Link'}</span>
          </button>

          <a
            href={GITHUB_REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-white transition-colors flex items-center gap-1.5 text-slate-400"
          >
            <Github className="w-3.5 h-3.5" />
            <span>GitHub</span>
          </a>
        </div>
      </div>
    </footer>
  );
};
