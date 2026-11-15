import React from 'react';
import { Loader2, Sparkles } from 'lucide-react';

interface SkeletonLoaderProps {
  statusMessage?: string;
}

export const SkeletonLoader: React.FC<SkeletonLoaderProps> = ({
  statusMessage = 'Generating model response...',
}) => {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-busy="true"
      className="p-[1.25rem] rounded-[1rem] bg-white dark:bg-[#111827] border border-gray-200 dark:border-gray-700/80 shadow-sm space-y-[1rem] max-w-[75ch] animate-fade-in"
    >
      {/* Top indicator with Spinner and Status label */}
      <div className="flex items-center gap-[0.75rem] text-[0.875rem] font-medium text-[#4F46E5] dark:text-[#6366F1]">
        <div className="w-[2rem] h-[2rem] rounded-[0.5rem] bg-[#4F46E5]/10 dark:bg-[#6366F1]/20 flex items-center justify-center">
          <Loader2 className="w-[1.125rem] h-[1.125rem] animate-spin text-[#4F46E5] dark:text-[#6366F1]" aria-hidden="true" />
        </div>
        <div className="flex items-center gap-[0.375rem]">
          <Sparkles className="w-[1rem] h-[1rem]" aria-hidden="true" />
          <span>{statusMessage}</span>
        </div>
      </div>

      {/* Skeleton Text Lines */}
      <div className="space-y-[0.75rem] pt-[0.25rem]">
        <div className="h-[1rem] bg-gray-200 dark:bg-gray-700/70 rounded-[0.25rem] w-11/12 animate-pulse" />
        <div className="h-[1rem] bg-gray-200 dark:bg-gray-700/70 rounded-[0.25rem] w-full animate-pulse delay-75" />
        <div className="h-[1rem] bg-gray-200 dark:bg-gray-700/70 rounded-[0.25rem] w-4/5 animate-pulse delay-150" />
      </div>

      {/* Skeleton Code/List Block */}
      <div className="p-[1rem] rounded-[0.75rem] bg-gray-100 dark:bg-gray-800/60 border border-gray-200/80 dark:border-gray-700/60 space-y-[0.625rem]">
        <div className="h-[0.875rem] bg-gray-300 dark:bg-gray-700 rounded-[0.25rem] w-1/3 animate-pulse" />
        <div className="h-[0.875rem] bg-gray-300 dark:bg-gray-700 rounded-[0.25rem] w-2/3 animate-pulse" />
        <div className="h-[0.875rem] bg-gray-300 dark:bg-gray-700 rounded-[0.25rem] w-1/2 animate-pulse" />
      </div>

      {/* Final short skeleton line */}
      <div className="h-[1rem] bg-gray-200 dark:bg-gray-700/70 rounded-[0.25rem] w-3/4 animate-pulse" />
    </div>
  );
};
