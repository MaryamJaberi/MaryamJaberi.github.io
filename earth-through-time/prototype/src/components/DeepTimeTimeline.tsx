import React, { useState } from 'react';
import { Clock, Orbit, Sparkles, Scale, Info, ArrowLeftRight } from 'lucide-react';
import { LanguageKey, TimelineEpoch } from '../types';
import { TIMELINE_EPOCHS } from '../data/projectData';

interface DeepTimeTimelineProps {
  currentLang: LanguageKey;
}

export const DeepTimeTimeline: React.FC<DeepTimeTimelineProps> = ({ currentLang }) => {
  const [activeScale, setActiveScale] = useState<'log' | 'linear'>('log');
  const [selectedEpochIndex, setSelectedEpochIndex] = useState<number>(0);
  const isFa = currentLang === 'fa';

  const filteredEpochs = TIMELINE_EPOCHS.filter(
    e => activeScale === 'log' ? e.scaleType === 'log' : e.scaleType === 'linear'
  );

  const currentEpoch = filteredEpochs[selectedEpochIndex] || filteredEpochs[0];

  return (
    <section className="py-12 border-t border-slate-800/80">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-8">
          <div>
            <span className="text-xs uppercase tracking-widest text-amber-400 font-semibold flex items-center gap-1.5 mb-1.5">
              <Scale className="w-3.5 h-3.5" />
              <span>{isFa ? 'نوآوری در ریاضیات مقیاس زمان' : 'The Dual Scale Innovation'}</span>
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-white font-cinzel">
              {isFa ? 'چرا دو مقیاس زمان؟ (لگاریتمی + خطی)' : 'Logarithmic Deep-Time vs. Linear History'}
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-xl mt-1">
              {isFa
                ? 'یک مقیاس خطی نمی‌تواند هم ۱۳٫۸ میلیارد سال کیهان و هم ۶ هزار سال تمدن را بدون ناپدید شدن تاریخ انسان نمایش دهد.'
                : 'A single linear scale compresses 6,000 years of recorded human civilization into an invisible sub-pixel width.'}
            </p>
          </div>

          {/* Scale Switcher Toggle */}
          <div className="p-1 bg-slate-900 border border-slate-800 rounded-xl flex items-center self-start sm:self-auto">
            <button
              onClick={() => {
                setActiveScale('log');
                setSelectedEpochIndex(0);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeScale === 'log'
                  ? 'bg-amber-500 text-slate-950 font-bold shadow'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {isFa ? 'زمان عمیق (لگاریتمی: ۱۳٫۸ میلیارد سال)' : 'Deep Time (Logarithmic: 13.8 Ga)'}
            </button>
            <button
              onClick={() => {
                setActiveScale('linear');
                setSelectedEpochIndex(0);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeScale === 'linear'
                  ? 'bg-amber-500 text-slate-950 font-bold shadow'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {isFa ? 'تاریخ ثبت‌شده (خطی: ۶۰۰۰ سال)' : 'Recorded History (Linear: 6,000 Years)'}
            </button>
          </div>
        </div>

        {/* Interactive Scale Strip */}
        <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl mb-6">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-4 font-mono">
            <span>{activeScale === 'log' ? '13.8 Billion Years Ago (Big Bang)' : '3200 BCE (First Writing & Cities)'}</span>
            <span className="text-amber-400 font-semibold">{activeScale === 'log' ? 'Exponential Decade Decimation' : 'High-Resolution Decade Stepping'}</span>
            <span>{activeScale === 'log' ? '300,000 Years Ago' : '+1,000 Years Ahead (Scenarios)'}</span>
          </div>

          {/* Ruler Representation */}
          <div className="relative h-12 bg-slate-950 rounded-xl border border-slate-800 flex items-center px-4 overflow-x-auto">
            <div className="absolute inset-x-4 h-[2px] bg-slate-800" />
            <div className="relative flex items-center justify-between w-full min-w-[500px]">
              {filteredEpochs.map((epoch, idx) => {
                const isSelected = selectedEpochIndex === idx;
                return (
                  <button
                    key={idx}
                    onClick={() => setSelectedEpochIndex(idx)}
                    className="relative group flex flex-col items-center focus:outline-none"
                  >
                    <div
                      className={`w-4 h-4 rounded-full border-2 transition-all ${
                        isSelected
                          ? 'bg-amber-400 border-amber-300 scale-125 shadow-lg shadow-amber-500/50 ring-4 ring-amber-500/20'
                          : 'bg-slate-900 border-slate-600 group-hover:border-amber-400'
                      }`}
                    />
                    <span
                      className={`mt-2 text-[10px] font-mono whitespace-nowrap transition-colors ${
                        isSelected ? 'text-amber-300 font-bold' : 'text-slate-400 group-hover:text-slate-200'
                      }`}
                    >
                      {epoch.timeDisplay}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Selected Epoch Details */}
        {currentEpoch && (
          <div className="p-5 sm:p-6 rounded-xl bg-slate-950/80 border border-slate-800/90 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="space-y-1.5">
              <div className="flex items-center gap-2">
                <span className="text-xs px-2 py-0.5 rounded bg-amber-500/15 text-amber-300 font-mono font-semibold">
                  {currentEpoch.timeDisplay}
                </span>
                <span className="text-xs text-slate-500 capitalize">
                  {currentEpoch.category}
                </span>
              </div>
              <h3 className="text-lg font-bold text-white font-cinzel">
                {isFa ? currentEpoch.labelFa : currentEpoch.labelEn}
              </h3>
              <p className="text-xs sm:text-sm text-slate-300">
                {isFa ? currentEpoch.descriptionFa : currentEpoch.descriptionEn}
              </p>
            </div>

            <div className="shrink-0 p-3 rounded-xl bg-slate-900 border border-slate-800 text-center min-w-[130px]">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">
                {isFa ? 'نوع مقیاس فعال' : 'Active Scale Engine'}
              </span>
              <span className="text-xs font-mono font-bold text-amber-400 mt-1 block">
                {activeScale === 'log' ? 'Logarithmic (Deep Time)' : 'Linear (Historical)'}
              </span>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};
