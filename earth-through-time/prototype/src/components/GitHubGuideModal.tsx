import React, { useState } from 'react';
import { X, Github, ExternalLink, Copy, Check, Terminal, FolderGit2, Globe, ShieldCheck } from 'lucide-react';
import { LanguageKey } from '../types';
import { GITHUB_REPO_URL, LIVE_DEMO_URL, PORTFOLIO_REPO_URL } from '../data/projectData';

interface GitHubGuideModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentLang: LanguageKey;
}

export const GitHubGuideModal: React.FC<GitHubGuideModalProps> = ({
  isOpen,
  onClose,
  currentLang,
}) => {
  const [copiedCmd, setCopiedCmd] = useState(false);
  const isFa = currentLang === 'fa';

  if (!isOpen) return null;

  const gitCommands = `# ۱. اینیشیالایز گیت در پوشهٔ پروژه
git init
git add .
git commit -m "feat: Chrono Atlas showcase & multilingual portfolio cards"

# ۲. اتصال به مخزن گیت‌هاب شما
git branch -M main
git remote add origin https://github.com/MaryamJaberi/chrono-atlas.git

# ۳. پوش کردن به گیت‌هاب
git push -u origin main`;

  const handleCopyCommands = () => {
    navigator.clipboard.writeText(gitCommands);
    setCopiedCmd(true);
    setTimeout(() => setCopiedCmd(false), 2400);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-3xl max-h-[90vh] bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/80">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400">
              <FolderGit2 className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-bold text-white font-cinzel">
                {isFa ? 'لینک‌ها و راهنمای قرار دادن روی گیت‌هاب' : 'GitHub Links & Deployment Guide'}
              </h3>
              <p className="text-xs text-slate-400">
                GitHub Repositories & Pages Setup
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-300 text-xs sm:text-sm">
          {/* Quick Direct Links Cards */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-amber-400">
              {isFa ? '🔗 لینک‌های مستقیم پروژهٔ شما' : 'Direct Project URLs'}
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <a
                href={LIVE_DEMO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500/50 transition-all flex items-center justify-between group"
              >
                <div>
                  <span className="text-[11px] text-slate-400 block">{isFa ? 'سایت زنده (GitHub Pages)' : 'Live Demo'}</span>
                  <span className="text-xs font-mono font-semibold text-amber-300 group-hover:underline">
                    maryamjaberi.github.io/chrono-atlas
                  </span>
                </div>
                <Globe className="w-4 h-4 text-slate-400 group-hover:text-amber-400" />
              </a>

              <a
                href={GITHUB_REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500/50 transition-all flex items-center justify-between group"
              >
                <div>
                  <span className="text-[11px] text-slate-400 block">{isFa ? 'مخزن سورس‌کد پروژه' : 'Chrono Atlas Source Repo'}</span>
                  <span className="text-xs font-mono font-semibold text-white group-hover:underline">
                    github.com/MaryamJaberi/chrono-atlas
                  </span>
                </div>
                <Github className="w-4 h-4 text-slate-400 group-hover:text-white" />
              </a>
            </div>

            <a
              href={PORTFOLIO_REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 hover:border-slate-700 transition-all flex items-center justify-between block"
            >
              <div>
                <span className="text-[11px] text-slate-400 block">
                  {isFa ? 'مخزن سایت پورتفولیوی شخصی شما (برای الصاق کارت‌ها)' : 'Your Portfolio Website Repository (To paste cards)'}
                </span>
                <span className="text-xs font-mono text-slate-300">
                  github.com/MaryamJaberi/MaryamJaberi.github.io
                </span>
              </div>
              <ExternalLink className="w-4 h-4 text-slate-400" />
            </a>
          </div>

          {/* Export via Google AI Studio */}
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <h4 className="text-xs font-semibold text-white flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-amber-400" />
              <span>{isFa ? 'خروجی مستقیم به گیت‌هاب از محیط استودیو' : 'Export Directly to GitHub via Studio'}</span>
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed">
              {isFa
                ? 'در گوشهٔ بالا-راست محیط Google AI Studio، منوی سه‌نقطه یا دکمهٔ Export را بزنید و گزینهٔ "Export to GitHub" را انتخاب کنید تا مستقیماً مخزن شما با این طراحی جدید سینک شود.'
                : 'In Google AI Studio, open the top-right Settings/Export menu and click "Export to GitHub" or "Download ZIP" to commit this project straight to your repo.'}
            </p>
          </div>

          {/* Git Terminal Commands */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5 text-amber-400" />
                <span>{isFa ? 'دستورات ترمینال برای ارسال به گیت‌هاب' : 'Manual Terminal Git Commands'}</span>
              </h4>
              <button
                onClick={handleCopyCommands}
                className="inline-flex items-center gap-1 text-xs text-amber-400 hover:underline"
              >
                {copiedCmd ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copiedCmd ? (isFa ? 'کپی شد' : 'Copied') : (isFa ? 'کپی دستورات' : 'Copy')}</span>
              </button>
            </div>
            <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 font-code text-xs text-slate-300 overflow-x-auto whitespace-pre leading-relaxed">
              {gitCommands}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};
