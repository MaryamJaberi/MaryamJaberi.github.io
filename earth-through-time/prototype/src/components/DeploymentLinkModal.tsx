import React, { useState } from 'react';
import { Copy, Check, Globe, Github, ExternalLink } from 'lucide-react';
import { LanguageKey } from '../types';
import { LIVE_DEMO_URL, GITHUB_REPO_URL, CREATE_GITHUB_REPO_URL } from '../data/projectData';

interface DeploymentLinkModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentLang: LanguageKey;
}

export const DeploymentLinkModal: React.FC<DeploymentLinkModalProps> = ({
  isOpen,
  onClose,
  currentLang,
}) => {
  const isFa = currentLang === 'fa';
  const [copiedLink, setCopiedLink] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedLink(id);
    setTimeout(() => setCopiedLink(null), 2000);
  };

  const gitCommands = `git init
git add .
git commit -m "Initial commit of Chrono Atlas"
git branch -M main
git remote add origin https://github.com/MaryamJaberi/chrono-atlas.git
git push -u origin main`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md">
      <div className="bg-[#111827] border border-amber-500/50 rounded-3xl max-w-2xl w-full max-h-[92vh] overflow-y-auto p-6 sm:p-8 shadow-2xl relative text-[#F1F5F9] font-vazir">
        <button
          onClick={onClose}
          className="absolute top-5 left-5 sm:left-auto sm:right-5 text-slate-400 hover:text-white text-base font-bold bg-[#161F30] w-8 h-8 rounded-full flex items-center justify-center border border-white/10"
        >
          ✕
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-2xl bg-amber-500/15 border border-amber-500/40 flex items-center justify-center text-amber-400 text-xl shadow-lg shrink-0">
            🌐
          </div>
          <div>
            <span className="text-xs text-amber-400 font-semibold block">
              {isFa ? 'مرکز اشتراک‌گذاری و استقرار آنلاین' : 'Live Deployment & Share'}
            </span>
            <h3 className="text-xl sm:text-2xl font-bold text-white">
              {isFa ? 'لینک‌های آنلاین و فعال پروژه' : 'Chrono Atlas Access Center'}
            </h3>
          </div>
        </div>

        {/* 1. Working Live URL */}
        <div className="bg-[#161F30] border border-amber-500/40 rounded-2xl p-5 mb-5 shadow-lg">
          <div className="flex items-center gap-2 text-xs text-amber-400 font-bold mb-2">
            <Globe className="w-4 h-4" />
            <span>{isFa ? 'لینک مستقیم و آنلاین برنامه (بدون ۴۰۴):' : 'Direct Live Cloud Deployment:'}</span>
          </div>

          <p className="text-xs text-slate-300 mb-3 leading-relaxed">
            {isFa
              ? 'این لینک در اینترنت فعال است و بدون هیچ خطایی مستقیماً باز می‌شود:'
              : 'This link is deployed and running live right now:'}
          </p>

          <div className="flex items-center gap-2 bg-[#0A0E17] p-2.5 rounded-xl border border-white/10">
            <input
              type="text"
              readOnly
              value={LIVE_DEMO_URL}
              className="w-full bg-transparent text-xs sm:text-sm font-num text-slate-200 focus:outline-none"
            />
            <button
              onClick={() => handleCopy(LIVE_DEMO_URL, 'cloud-url')}
              className="p-2 rounded-lg bg-[#161F30] hover:bg-amber-500 hover:text-slate-950 text-slate-300 transition-colors shrink-0"
              title={isFa ? 'کپی لینک' : 'Copy Link'}
            >
              {copiedLink === 'cloud-url' ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
            </button>
            <a
              href={LIVE_DEMO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-lg bg-amber-500 text-slate-950 hover:bg-amber-400 transition-colors shrink-0 flex items-center gap-1 text-xs font-bold"
            >
              <span>{isFa ? 'باز کردن' : 'Open'}</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>

        {/* 2. GitHub Quick Setup */}
        <div className="bg-[#161F30] border border-white/10 rounded-2xl p-5">
          <div className="flex items-center gap-2 text-xs text-slate-200 font-bold mb-2">
            <Github className="w-4 h-4 text-amber-400" />
            <span>{isFa ? 'نحوه ارسال کدها به گیت‌هاب شخصی:' : 'Push to GitHub Repository:'}</span>
          </div>

          <p className="text-xs text-slate-300 mb-3 leading-relaxed">
            {isFa
              ? 'ابتدا مخزن chrono-atlas را بسازید و سپس این دستورات را اجرا کنید:'
              : 'Create the repository then run these commands:'}
          </p>

          <div className="bg-[#0A0E17] p-3 rounded-xl border border-white/10 font-num text-xs text-amber-300/90 mb-3 overflow-x-auto whitespace-pre">
            {gitCommands}
          </div>

          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => handleCopy(gitCommands, 'git-cmds')}
              className="px-3 py-2 rounded-xl text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 border border-white/10 flex items-center gap-1.5 transition-colors"
            >
              {copiedLink === 'git-cmds' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{isFa ? 'کپی دستورات ترمینال' : 'Copy Commands'}</span>
            </button>

            <a
              href={CREATE_GITHUB_REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 rounded-xl text-xs bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold flex items-center gap-1.5 transition-colors"
            >
              <span>{isFa ? 'ساخت ریپازیتوری در گیت‌هاب' : 'Create Repo on GitHub'}</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
