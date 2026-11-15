import React, { useRef, useEffect } from 'react';
import { 
  Sparkles, 
  Bot, 
  User, 
  Clock, 
  Zap, 
  ArrowRight, 
  AlertCircle,
  CheckCircle2,
  BookOpen
} from 'lucide-react';
import { ChatMessage, ToastNotification } from '../types/studio';
import { CodeBlock } from './CodeBlock';
import { SkeletonLoader } from './SkeletonLoader';
import { STARTER_PROMPTS } from '../data/defaultSessions';

interface MainWorkspaceProps {
  messages: ChatMessage[];
  isGenerating: boolean;
  onSelectStarterPrompt: (promptText: string) => void;
  toast: ToastNotification | null;
  onDismissToast: () => void;
  modelName: string;
}

export const MainWorkspace: React.FC<MainWorkspaceProps> = ({
  messages,
  isGenerating,
  onSelectStarterPrompt,
  toast,
  onDismissToast,
  modelName,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto scroll to bottom when new messages arrive or while generating
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isGenerating]);

  return (
    <main
      id="main-workspace"
      role="main"
      className="flex-1 flex flex-col min-w-0 overflow-y-auto px-[1rem] sm:px-[1.5rem] lg:px-[2rem] py-[1rem] relative"
    >
      {/* Toast Notification Banner with WCAG AA contrast (icon + label) */}
      {toast && (
        <div
          role="alert"
          className={`sticky top-[0.5rem] z-40 mb-[1rem] p-[0.875rem] sm:p-[1rem] rounded-[0.75rem] border flex items-center justify-between shadow-md transition-all animate-fade-in ${
            toast.type === 'success'
              ? 'bg-emerald-50 dark:bg-emerald-950/80 border-[#10B981] text-[#065F46] dark:text-[#34D399]'
              : toast.type === 'error'
              ? 'bg-red-50 dark:bg-red-950/80 border-[#EF4444] text-[#991B1B] dark:text-[#F87171]'
              : 'bg-indigo-50 dark:bg-indigo-950/80 border-[#4F46E5] text-[#3730A3] dark:text-[#A5B4FC]'
          }`}
        >
          <div className="flex items-center gap-[0.625rem] text-[0.875rem] font-medium">
            {toast.type === 'success' && <CheckCircle2 className="w-[1.25rem] h-[1.25rem] text-[#10B981]" aria-hidden="true" />}
            {toast.type === 'error' && <AlertCircle className="w-[1.25rem] h-[1.25rem] text-[#EF4444]" aria-hidden="true" />}
            {toast.type === 'info' && <Sparkles className="w-[1.25rem] h-[1.25rem] text-[#4F46E5]" aria-hidden="true" />}
            <span>{toast.message}</span>
          </div>

          <button
            type="button"
            onClick={onDismissToast}
            aria-label="Dismiss message notification"
            className="touch-target text-current hover:opacity-70 font-semibold text-[0.875rem] ml-[1rem]"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Model Status Bar */}
      <div className="flex items-center justify-between pb-[0.75rem] mb-[1rem] border-b border-gray-200 dark:border-gray-800 text-[0.8125rem] text-gray-500 dark:text-gray-400">
        <div className="flex items-center gap-[0.5rem]">
          <span className="w-[0.5rem] h-[0.5rem] rounded-full bg-[#10B981] animate-pulse" aria-hidden="true" />
          <span className="font-medium text-gray-700 dark:text-gray-300">Ready</span>
          <span>·</span>
          <span>Engine: <strong className="text-gray-800 dark:text-gray-200">{modelName}</strong></span>
        </div>

        <div className="flex items-center gap-[0.375rem]">
          <Zap className="w-[0.875rem] h-[0.875rem] text-[#4F46E5] dark:text-[#6366F1]" aria-hidden="true" />
          <span className="hidden sm:inline">Streaming mode enabled</span>
        </div>
      </div>

      {/* Message List or Actionable Empty State */}
      <div className="flex-1 space-y-[1.5rem] pb-[2rem]">
        {messages.length === 0 ? (
          /* Actionable Empty State with Call-To-Action */
          <div className="flex flex-col items-center justify-center text-center py-[2.5rem] sm:py-[4rem] px-[1rem] max-w-[46rem] mx-auto animate-fade-in">
            <div className="w-[3.5rem] h-[3.5rem] rounded-[1rem] bg-[#4F46E5]/10 dark:bg-[#6366F1]/20 flex items-center justify-center text-[#4F46E5] dark:text-[#6366F1] mb-[1.25rem] shadow-xs">
              <Sparkles className="w-[1.75rem] h-[1.75rem]" aria-hidden="true" />
            </div>

            <h2 className="text-[clamp(1.25rem,3vw,1.75rem)] font-bold text-gray-900 dark:text-gray-100 tracking-tight mb-[0.5rem]">
              Google AI Studio Workspace
            </h2>

            <p className="text-[1rem] leading-[1.5] text-gray-600 dark:text-gray-400 max-w-[75ch] mb-[2rem] text-left sm:text-center">
              Start by entering a prompt in the floating field below, or select a pre-configured template to explore analytical synthesis, code generation, and research.
            </p>

            {/* Quick Action Starter Prompts */}
            <div className="w-full text-left">
              <div className="flex items-center gap-[0.375rem] text-[0.75rem] font-bold text-gray-500 uppercase tracking-wider mb-[0.75rem]">
                <BookOpen className="w-[0.875rem] h-[0.875rem] text-[#4F46E5]" aria-hidden="true" />
                <span>Suggested Prompt Starters</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-[0.75rem]">
                {STARTER_PROMPTS.map((starter, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => onSelectStarterPrompt(starter.prompt)}
                    className="group p-[1rem] rounded-[0.75rem] bg-white dark:bg-[#111827] border border-gray-200 dark:border-gray-800 hover:border-[#4F46E5] dark:hover:border-[#6366F1] transition-all text-left shadow-xs hover:shadow-sm focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none flex flex-col justify-between"
                  >
                    <div>
                      <span className="text-[0.6875rem] font-semibold uppercase text-[#4F46E5] dark:text-[#6366F1]">
                        {starter.category}
                      </span>
                      <h3 className="font-semibold text-[0.9375rem] text-gray-900 dark:text-gray-100 mt-[0.125rem] group-hover:text-[#4F46E5] dark:group-hover:text-[#6366F1] transition-colors">
                        {starter.title}
                      </h3>
                      <p className="text-[0.8125rem] leading-[1.4] text-gray-500 dark:text-gray-400 mt-[0.375rem] line-clamp-2">
                        {starter.prompt}
                      </p>
                    </div>

                    <div className="mt-[0.75rem] pt-[0.5rem] border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-[0.75rem] text-[#4F46E5] dark:text-[#6366F1] font-medium">
                      <span>Use this prompt</span>
                      <ArrowRight className="w-[0.875rem] h-[0.875rem] group-hover:translate-x-1 transition-transform" aria-hidden="true" />
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          /* Render Conversational Messages */
          messages.map((message) => {
            const isUser = message.role === 'user';

            return (
              <article
                key={message.id}
                aria-label={`${isUser ? 'User' : 'Assistant'} message`}
                className={`flex gap-[0.75rem] sm:gap-[1rem] max-w-[75ch] text-left ${
                  isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'
                }`}
              >
                {/* Avatar */}
                <div
                  className={`w-[2.25rem] h-[2.25rem] rounded-[0.5rem] flex items-center justify-center shrink-0 shadow-xs ${
                    isUser
                      ? 'bg-gray-800 text-white dark:bg-gray-700'
                      : 'bg-[#4F46E5] text-white dark:bg-[#6366F1]'
                  }`}
                >
                  {isUser ? (
                    <User className="w-[1.125rem] h-[1.125rem]" aria-hidden="true" />
                  ) : (
                    <Bot className="w-[1.125rem] h-[1.125rem]" aria-hidden="true" />
                  )}
                </div>

                {/* Message Bubble Card */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-[0.5rem] mb-[0.25rem] text-[0.75rem] text-gray-500 dark:text-gray-400">
                    <span className="font-semibold text-gray-900 dark:text-gray-200">
                      {isUser ? 'You' : modelName}
                    </span>
                    <span>·</span>
                    <span className="flex items-center gap-[0.25rem]">
                      <Clock className="w-[0.75rem] h-[0.75rem]" aria-hidden="true" />
                      <span>{message.timestamp}</span>
                    </span>
                  </div>

                  <div
                    className={`p-[1.125rem] rounded-[1rem] border text-[1rem] leading-[1.5] text-left transition-colors shadow-xs ${
                      isUser
                        ? 'bg-[#4F46E5]/5 dark:bg-[#6366F1]/15 border-[#4F46E5]/20 text-gray-900 dark:text-gray-100'
                        : 'bg-white dark:bg-[#111827] border-gray-200 dark:border-gray-800 text-gray-800 dark:text-gray-200'
                    }`}
                  >
                    {/* Render text content with paragraph breaks and bullet points */}
                    <div className="space-y-[0.75rem] whitespace-pre-line break-words text-left">
                      {message.content.split('\n\n').map((paragraph, pIdx) => {
                        // Check if paragraph contains bullet points
                        if (paragraph.includes('• ') || paragraph.startsWith('- ')) {
                          const lines = paragraph.split('\n');
                          return (
                            <ul key={pIdx} className="space-y-[0.375rem] my-[0.5rem] pl-[1.25rem] list-disc">
                              {lines.map((line, lIdx) => {
                                const cleanLine = line.replace(/^[•\-]\s*/, '');
                                return (
                                  <li key={lIdx} className="leading-[1.5]">
                                    {cleanLine}
                                  </li>
                                );
                              })}
                            </ul>
                          );
                        }
                        return (
                          <p key={pIdx} className="leading-[1.5]">
                            {paragraph}
                          </p>
                        );
                      })}
                    </div>

                    {/* Syntax-highlighted Code Blocks */}
                    {message.codeBlocks && message.codeBlocks.length > 0 && (
                      <div className="mt-[1rem]">
                        {message.codeBlocks.map((block) => (
                          <CodeBlock
                            key={block.id}
                            code={block.code}
                            language={block.language}
                            title={block.title}
                          />
                        ))}
                      </div>
                    )}

                    {/* Metadata Footer: Token Count & Latency */}
                    {message.tokenCount && (
                      <div className="mt-[0.875rem] pt-[0.625rem] border-t border-gray-100 dark:border-gray-800/80 flex items-center gap-[0.75rem] text-[0.75rem] text-gray-400 font-mono">
                        <span>Prompt: {message.tokenCount.prompt} tok</span>
                        <span>·</span>
                        <span>Completion: {message.tokenCount.completion} tok</span>
                      </div>
                    )}
                  </div>
                </div>
              </article>
            );
          })
        )}

        {/* Loading State: Animated Spinner and Skeleton Screen */}
        {isGenerating && (
          <div className="max-w-[75ch] text-left">
            <SkeletonLoader statusMessage="Synthesizing response with Gemini 2.5..." />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>
    </main>
  );
};
