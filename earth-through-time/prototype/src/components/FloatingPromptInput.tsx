import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Sparkles, 
  CornerDownLeft, 
  Paperclip, 
  X, 
  FileText
} from 'lucide-react';

interface FloatingPromptInputProps {
  onSend: (promptText: string) => void;
  isGenerating: boolean;
  disabled?: boolean;
}

export const FloatingPromptInput: React.FC<FloatingPromptInputProps> = ({
  onSend,
  isGenerating,
  disabled = false,
}) => {
  const [prompt, setPrompt] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea when text changes
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      // If focused or has content, allow up to 200px height
      if (isFocused || prompt.length > 0) {
        textareaRef.current.style.height = `${Math.min(Math.max(scrollHeight, 72), 220)}px`;
      } else {
        textareaRef.current.style.height = '44px';
      }
    }
  }, [prompt, isFocused]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!prompt.trim() || isGenerating || disabled) return;
    onSend(prompt.trim());
    setPrompt('');
    if (textareaRef.current) {
      textareaRef.current.style.height = '44px';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  // Rough estimation of tokens (~4 chars per token)
  const estimatedTokens = Math.ceil(prompt.length / 4);

  return (
    <footer
      id="prompt-footer"
      className="sticky bottom-0 z-20 w-full p-[0.75rem] sm:p-[1rem] bg-gradient-to-t from-gray-50 via-gray-50/95 to-transparent dark:from-[#1F2937] dark:via-[#1F2937]/95 select-none"
    >
      <div className="max-w-[50rem] mx-auto">
        <form
          onSubmit={handleSubmit}
          className={`relative rounded-[1rem] border transition-all duration-300 shadow-md ${
            isFocused
              ? 'bg-white dark:bg-[#111827] border-[#4F46E5] ring-2 ring-[#4F46E5]/20 shadow-lg'
              : 'bg-white/90 dark:bg-[#111827]/90 border-gray-300 dark:border-gray-700 hover:border-gray-400 dark:hover:border-gray-600'
          }`}
        >
          {/* Main Input Field Area */}
          <div className="p-[0.75rem] sm:p-[1rem]">
            <label htmlFor="main-prompt-input" className="sr-only">
              Prompt input for AI model
            </label>
            <textarea
              id="main-prompt-input"
              ref={textareaRef}
              rows={1}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              onKeyDown={handleKeyDown}
              disabled={disabled || isGenerating}
              placeholder="Ask anything, formulate a prompt, or request code..."
              className="w-full bg-transparent border-0 resize-none text-[1rem] leading-[1.5] text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-0 disabled:opacity-50 min-h-[44px]"
            />
          </div>

          {/* Footer Controls within the floating input card */}
          <div className="flex items-center justify-between px-[0.75rem] sm:px-[1rem] pb-[0.625rem] pt-[0.25rem] border-t border-gray-100 dark:border-gray-800/80 text-[0.75rem]">
            {/* Left helper actions */}
            <div className="flex items-center gap-[0.5rem] text-gray-400">
              <span className="hidden sm:inline font-mono">
                {prompt.length > 0 ? `${prompt.length} chars · ~${estimatedTokens} tokens` : 'Shift + Enter for new line'}
              </span>

              {prompt.length > 0 && (
                <button
                  type="button"
                  onClick={() => setPrompt('')}
                  aria-label="Clear current input"
                  className="touch-target text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
                >
                  <X className="w-[0.875rem] h-[0.875rem]" aria-hidden="true" />
                  <span className="text-[0.75rem] ml-[0.25rem]">Clear</span>
                </button>
              )}
            </div>

            {/* Right: Submit Button - Minimum 44x44px touch target */}
            <div className="flex items-center gap-[0.5rem]">
              <button
                type="submit"
                disabled={!prompt.trim() || isGenerating || disabled}
                aria-label={isGenerating ? 'Generation in progress' : 'Submit prompt to model'}
                className="touch-target px-[1rem] rounded-[0.5rem] bg-[#4F46E5] hover:bg-[#4338CA] disabled:opacity-40 disabled:hover:bg-[#4F46E5] text-white font-medium text-[0.875rem] transition-all shadow-xs gap-[0.375rem] focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none"
              >
                <span>Generate</span>
                <Send className="w-[0.9375rem] h-[0.9375rem]" aria-hidden="true" />
              </button>
            </div>
          </div>
        </form>
      </div>
    </footer>
  );
};
