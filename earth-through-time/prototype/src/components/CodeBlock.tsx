import React, { useState } from 'react';
import { Check, Copy, Terminal } from 'lucide-react';

interface CodeBlockProps {
  code: string;
  language?: string;
  title?: string;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language = 'plaintext',
  title,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      const textArea = document.createElement('textarea');
      textArea.value = code;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="my-[1rem] rounded-[0.75rem] border border-gray-200 dark:border-gray-700 overflow-hidden bg-gray-900 text-gray-100 shadow-sm">
      {/* Code Header Bar */}
      <div className="flex items-center justify-between px-[1rem] py-[0.5rem] bg-gray-800/90 border-b border-gray-700/60 text-[0.875rem]">
        <div className="flex items-center gap-[0.5rem] font-mono text-gray-300">
          <Terminal className="w-[1rem] h-[1rem] text-[#4F46E5] dark:text-[#6366F1]" aria-hidden="true" />
          <span className="font-semibold text-[0.8125rem] text-gray-200 uppercase tracking-wider">
            {language}
          </span>
          {title && (
            <span className="text-gray-400 text-[0.8125rem] font-normal border-l border-gray-600 pl-[0.5rem]">
              {title}
            </span>
          )}
        </div>

        {/* Action button with minimum 44x44px touch target */}
        <button
          type="button"
          onClick={handleCopy}
          aria-label={copied ? 'Code snippet copied to clipboard' : 'Copy code snippet to clipboard'}
          className="touch-target px-[0.75rem] rounded-[0.5rem] text-[0.8125rem] font-medium text-gray-300 hover:text-white hover:bg-gray-700/80 transition-colors focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none gap-[0.375rem]"
        >
          {copied ? (
            <>
              <Check className="w-[1.125rem] h-[1.125rem] text-[#10B981]" aria-hidden="true" />
              <span className="text-[#10B981] font-semibold">Copied</span>
            </>
          ) : (
            <>
              <Copy className="w-[1.125rem] h-[1.125rem]" aria-hidden="true" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>

      {/* Code Content with syntax highlighting styling and high contrast */}
      <div className="p-[1rem] overflow-x-auto text-[0.875rem] leading-[1.6] font-mono bg-[#0F172A] text-[#F8FAFC]">
        <pre className="m-0 select-text whitespace-pre">
          <code>{code}</code>
        </pre>
      </div>
    </div>
  );
};
