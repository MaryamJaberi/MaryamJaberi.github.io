import React from 'react';
import { 
  X, 
  Cpu, 
  SlidersHorizontal, 
  Info, 
  ShieldCheck, 
  Activity, 
  HelpCircle,
  Hash
} from 'lucide-react';
import { ModelConfig } from '../types/studio';

interface ContextualPanelProps {
  modelConfig: ModelConfig;
  onChangeModelConfig: (newConfig: ModelConfig) => void;
  isOpen: boolean;
  onClose: () => void;
  totalTokens: { prompt: number; completion: number };
}

export const ContextualPanel: React.FC<ContextualPanelProps> = ({
  modelConfig,
  onChangeModelConfig,
  isOpen,
  onClose,
  totalTokens,
}) => {
  if (!isOpen) return null;

  return (
    <>
      {/* Mobile Backdrop Overlay (<768px) */}
      <div 
        onClick={onClose}
        aria-hidden="true"
        className="fixed inset-0 bg-black/40 z-40 lg:hidden backdrop-blur-xs transition-opacity"
      />

      <aside
        id="contextual-panel"
        aria-label="Model configurations and session metadata"
        className="fixed lg:static inset-y-0 right-0 z-50 w-[19rem] sm:w-[21rem] bg-white dark:bg-[#111827] border-l border-gray-200 dark:border-gray-800 flex flex-col h-full overflow-y-auto select-none shadow-xl lg:shadow-none transition-all duration-300 animate-fade-in"
      >
        {/* Header */}
        <div className="p-[1rem] border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">
          <div className="flex items-center gap-[0.5rem] font-semibold text-[0.875rem] text-gray-900 dark:text-gray-100">
            <SlidersHorizontal className="w-[1.125rem] h-[1.125rem] text-[#4F46E5] dark:text-[#6366F1]" aria-hidden="true" />
            <span>Parameters & Metadata</span>
          </div>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close parameters panel"
            className="touch-target rounded-[0.5rem] text-gray-500 hover:text-gray-900 dark:hover:text-white"
          >
            <X className="w-[1.25rem] h-[1.25rem]" aria-hidden="true" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-[1.25rem] space-y-[1.5rem] flex-1 text-[0.875rem]">
          {/* Section: Model Selector */}
          <div className="space-y-[0.5rem]">
            <label 
              htmlFor="model-select"
              className="block font-semibold text-[0.8125rem] text-gray-700 dark:text-gray-300 flex items-center gap-[0.375rem]"
            >
              <Cpu className="w-[0.875rem] h-[0.875rem] text-[#4F46E5] dark:text-[#6366F1]" aria-hidden="true" />
              <span>Foundation Model</span>
            </label>
            <select
              id="model-select"
              value={modelConfig.modelId}
              onChange={(e) => {
                const modelId = e.target.value;
                const modelName = modelId === 'gemini-2.5-pro' ? 'Gemini 2.5 Pro' : 'Gemini 2.5 Flash';
                onChangeModelConfig({ ...modelConfig, modelId, modelName });
              }}
              className="w-full h-[2.75rem] px-[0.75rem] bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-[0.5rem] text-gray-900 dark:text-gray-100 text-[0.875rem] focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none transition-colors"
            >
              <option value="gemini-2.5-flash">Gemini 2.5 Flash (Fast & Multimodal)</option>
              <option value="gemini-2.5-pro">Gemini 2.5 Pro (Complex Reasoning)</option>
            </select>
            <p className="text-[0.75rem] text-gray-500 dark:text-gray-400">
              Low-latency default optimized for high throughput interactive tasks.
            </p>
          </div>

          {/* Section: System Instructions */}
          <div className="space-y-[0.5rem]">
            <div className="flex items-center justify-between">
              <label 
                htmlFor="system-instructions"
                className="block font-semibold text-[0.8125rem] text-gray-700 dark:text-gray-300"
              >
                System Instructions
              </label>
              <span className="text-[0.6875rem] text-gray-400 font-mono">
                {modelConfig.systemInstruction.length} chars
              </span>
            </div>
            <textarea
              id="system-instructions"
              rows={4}
              value={modelConfig.systemInstruction}
              onChange={(e) => onChangeModelConfig({ ...modelConfig, systemInstruction: e.target.value })}
              placeholder="Provide persona, guidelines, or formatting rules..."
              className="w-full p-[0.75rem] text-[0.8125rem] leading-[1.5] bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-[0.5rem] text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:bg-white dark:focus:bg-gray-800 focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none transition-colors resize-y"
            />
          </div>

          {/* Section: Temperature Slider */}
          <div className="space-y-[0.375rem]">
            <div className="flex items-center justify-between text-[0.8125rem]">
              <label htmlFor="temperature-slider" className="font-semibold text-gray-700 dark:text-gray-300">
                Temperature
              </label>
              <span className="font-mono text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-[0.375rem] py-[0.125rem] rounded">
                {modelConfig.temperature.toFixed(1)}
              </span>
            </div>
            <input
              id="temperature-slider"
              type="range"
              min="0.0"
              max="2.0"
              step="0.1"
              value={modelConfig.temperature}
              onChange={(e) => onChangeModelConfig({ ...modelConfig, temperature: parseFloat(e.target.value) })}
              className="w-full accent-[#4F46E5] h-[0.5rem] bg-gray-200 dark:bg-gray-700 rounded-lg cursor-pointer"
            />
            <div className="flex justify-between text-[0.6875rem] text-gray-400">
              <span>Precise (0.0)</span>
              <span>Balanced (0.7)</span>
              <span>Creative (2.0)</span>
            </div>
          </div>

          {/* Section: Top-P Slider */}
          <div className="space-y-[0.375rem]">
            <div className="flex items-center justify-between text-[0.8125rem]">
              <label htmlFor="topp-slider" className="font-semibold text-gray-700 dark:text-gray-300">
                Top P (Nucleus Sampling)
              </label>
              <span className="font-mono text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-[0.375rem] py-[0.125rem] rounded">
                {modelConfig.topP.toFixed(2)}
              </span>
            </div>
            <input
              id="topp-slider"
              type="range"
              min="0.0"
              max="1.0"
              step="0.05"
              value={modelConfig.topP}
              onChange={(e) => onChangeModelConfig({ ...modelConfig, topP: parseFloat(e.target.value) })}
              className="w-full accent-[#4F46E5] h-[0.5rem] bg-gray-200 dark:bg-gray-700 rounded-lg cursor-pointer"
            />
          </div>

          {/* Section: Max Output Tokens */}
          <div className="space-y-[0.375rem]">
            <div className="flex items-center justify-between text-[0.8125rem]">
              <label htmlFor="tokens-slider" className="font-semibold text-gray-700 dark:text-gray-300">
                Max Output Tokens
              </label>
              <span className="font-mono text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-[0.375rem] py-[0.125rem] rounded">
                {modelConfig.maxOutputTokens}
              </span>
            </div>
            <input
              id="tokens-slider"
              type="range"
              min="256"
              max="8192"
              step="256"
              value={modelConfig.maxOutputTokens}
              onChange={(e) => onChangeModelConfig({ ...modelConfig, maxOutputTokens: parseInt(e.target.value) })}
              className="w-full accent-[#4F46E5] h-[0.5rem] bg-gray-200 dark:bg-gray-700 rounded-lg cursor-pointer"
            />
          </div>

          {/* Divider */}
          <div className="border-t border-gray-200 dark:border-gray-800 pt-[1.25rem] space-y-[0.75rem]">
            <span className="font-semibold text-[0.75rem] text-gray-400 dark:text-gray-500 uppercase tracking-wider block">
              Session Metadata & Telemetry
            </span>

            {/* Token Counter Card */}
            <div className="p-[0.75rem] rounded-[0.5rem] bg-gray-50 dark:bg-gray-800/60 border border-gray-200 dark:border-gray-700/60 space-y-[0.375rem]">
              <div className="flex items-center justify-between text-[0.75rem]">
                <span className="text-gray-500 dark:text-gray-400 flex items-center gap-[0.25rem]">
                  <Hash className="w-[0.75rem] h-[0.75rem]" aria-hidden="true" />
                  Prompt Tokens:
                </span>
                <span className="font-mono font-semibold text-gray-800 dark:text-gray-200">
                  {totalTokens.prompt.toLocaleString()}
                </span>
              </div>
              <div className="flex items-center justify-between text-[0.75rem]">
                <span className="text-gray-500 dark:text-gray-400 flex items-center gap-[0.25rem]">
                  <Activity className="w-[0.75rem] h-[0.75rem]" aria-hidden="true" />
                  Completion Tokens:
                </span>
                <span className="font-mono font-semibold text-gray-800 dark:text-gray-200">
                  {totalTokens.completion.toLocaleString()}
                </span>
              </div>
              <div className="flex items-center justify-between text-[0.75rem] border-t border-gray-200 dark:border-gray-700 pt-[0.375rem] mt-[0.375rem]">
                <span className="font-semibold text-gray-700 dark:text-gray-300">Total Tokens:</span>
                <span className="font-mono font-bold text-[#4F46E5] dark:text-[#6366F1]">
                  {(totalTokens.prompt + totalTokens.completion).toLocaleString()}
                </span>
              </div>
            </div>

            {/* Safety badge */}
            <div className="flex items-center gap-[0.5rem] p-[0.75rem] rounded-[0.5rem] bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/40 text-[#10B981] text-[0.75rem]">
              <ShieldCheck className="w-[1.125rem] h-[1.125rem] shrink-0" aria-hidden="true" />
              <span>Safety filters active · Standard content moderation</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};
