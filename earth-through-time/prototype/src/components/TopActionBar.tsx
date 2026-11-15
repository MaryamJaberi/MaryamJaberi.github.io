import React, { useState, useRef, useEffect } from 'react';
import { 
  Play, 
  Trash2, 
  Save, 
  Download, 
  Sliders, 
  Moon, 
  Sun, 
  Menu, 
  Check, 
  FileText, 
  FileCode, 
  Sparkles,
  ChevronDown
} from 'lucide-react';
import { ThemeMode } from '../types/studio';

interface TopActionBarProps {
  onRun: () => void;
  onClear: () => void;
  onSave: () => void;
  onExport: (format: 'markdown' | 'json' | 'text') => void;
  onToggleSettings: () => void;
  isSettingsOpen: boolean;
  onToggleSidebar: () => void;
  isGenerating: boolean;
  themeMode: ThemeMode;
  onToggleTheme: () => void;
  activeSessionTitle: string;
}

export const TopActionBar: React.FC<TopActionBarProps> = ({
  onRun,
  onClear,
  onSave,
  onExport,
  onToggleSettings,
  isSettingsOpen,
  onToggleSidebar,
  isGenerating,
  themeMode,
  onToggleTheme,
  activeSessionTitle,
}) => {
  const [isExportOpen, setIsExportOpen] = useState(false);
  const [isSavedRecently, setIsSavedRecently] = useState(false);
  const exportRef = useRef<HTMLDivElement>(null);

  // Close export menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (exportRef.current && !exportRef.current.contains(event.target as Node)) {
        setIsExportOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSaveClick = () => {
    onSave();
    setIsSavedRecently(true);
    setTimeout(() => setIsSavedRecently(false), 2000);
  };

  return (
    <header 
      id="top-action-bar"
      className="sticky top-0 z-30 w-full h-[4rem] bg-white dark:bg-[#111827] border-b border-gray-200 dark:border-gray-800 px-[1rem] sm:px-[1.5rem] flex items-center justify-between shadow-xs select-none transition-colors"
    >
      {/* Left Zone: Sidebar trigger & Title Breadcrumb */}
      <div className="flex items-center gap-[0.75rem] min-w-0">
        {/* Mobile / Desktop Sidebar toggle button */}
        <button
          type="button"
          onClick={onToggleSidebar}
          aria-label="Toggle navigation and task history sidebar"
          className="touch-target rounded-[0.5rem] text-gray-600 dark:text-gray-300 hover:text-[#4F46E5] hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none"
        >
          <Menu className="w-[1.25rem] h-[1.25rem]" aria-hidden="true" />
        </button>

        {/* Brand & Active Task Title (Hierarchy Level 1 -> Level 2) */}
        <div className="flex items-center gap-[0.5rem] min-w-0">
          <div className="w-[2rem] h-[2rem] rounded-[0.5rem] bg-[#4F46E5] flex items-center justify-center text-white shrink-0 shadow-xs">
            <Sparkles className="w-[1.125rem] h-[1.125rem]" aria-hidden="true" />
          </div>
          <div className="flex flex-col min-w-0">
            <span className="text-[0.75rem] font-semibold text-[#4F46E5] dark:text-[#6366F1] uppercase tracking-wider hidden sm:inline">
              Google AI Studio
            </span>
            <h1 className="text-[0.9375rem] sm:text-[1rem] font-bold text-gray-900 dark:text-gray-100 truncate max-w-[200px] sm:max-w-[340px] md:max-w-[420px]">
              {activeSessionTitle}
            </h1>
          </div>
        </div>
      </div>

      {/* Right Zone: Task Management Controls */}
      <div className="flex items-center gap-[0.5rem]">
        {/* Run / Generate Button - Primary semantic #4F46E5 */}
        <button
          type="button"
          onClick={onRun}
          disabled={isGenerating}
          aria-label={isGenerating ? 'Generating response in progress' : 'Run prompt (⌘+Enter)'}
          title="Run Prompt (⌘+Enter)"
          className="touch-target px-[1rem] rounded-[0.5rem] bg-[#4F46E5] hover:bg-[#4338CA] active:bg-[#3730A3] text-white font-medium text-[0.875rem] transition-colors shadow-xs disabled:opacity-50 disabled:cursor-not-allowed focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none gap-[0.5rem]"
        >
          <Play className={`w-[1rem] h-[1rem] fill-current ${isGenerating ? 'animate-pulse' : ''}`} aria-hidden="true" />
          <span className="hidden sm:inline">{isGenerating ? 'Generating...' : 'Run'}</span>
          <span className="hidden md:inline text-[0.75rem] opacity-75 bg-white/20 px-[0.375rem] py-[0.125rem] rounded">
            ⌘↵
          </span>
        </button>

        {/* Clear Button */}
        <button
          type="button"
          onClick={onClear}
          aria-label="Clear active session prompts and results"
          title="Clear session"
          className="touch-target px-[0.75rem] rounded-[0.5rem] text-gray-600 dark:text-gray-300 hover:text-[#EF4444] hover:bg-red-50 dark:hover:bg-red-950/30 transition-colors focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none gap-[0.375rem] text-[0.875rem] font-medium"
        >
          <Trash2 className="w-[1.125rem] h-[1.125rem]" aria-hidden="true" />
          <span className="hidden lg:inline">Clear</span>
        </button>

        {/* Save Button */}
        <button
          type="button"
          onClick={handleSaveClick}
          aria-label="Save current session"
          title="Save session"
          className="touch-target px-[0.75rem] rounded-[0.5rem] text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none gap-[0.375rem] text-[0.875rem] font-medium"
        >
          {isSavedRecently ? (
            <>
              <Check className="w-[1.125rem] h-[1.125rem] text-[#10B981]" aria-hidden="true" />
              <span className="hidden lg:inline text-[#10B981]">Saved</span>
            </>
          ) : (
            <>
              <Save className="w-[1.125rem] h-[1.125rem]" aria-hidden="true" />
              <span className="hidden lg:inline">Save</span>
            </>
          )}
        </button>

        {/* Export Dropdown Menu */}
        <div className="relative" ref={exportRef}>
          <button
            type="button"
            onClick={() => setIsExportOpen(!isExportOpen)}
            aria-label="Export session options"
            aria-expanded={isExportOpen}
            aria-haspopup="true"
            className="touch-target px-[0.75rem] rounded-[0.5rem] text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none gap-[0.25rem] text-[0.875rem] font-medium"
          >
            <Download className="w-[1.125rem] h-[1.125rem]" aria-hidden="true" />
            <span className="hidden lg:inline">Export</span>
            <ChevronDown className="w-[0.875rem] h-[0.875rem] opacity-60" aria-hidden="true" />
          </button>

          {isExportOpen && (
            <div 
              role="menu"
              aria-orientation="vertical"
              className="absolute right-0 mt-[0.5rem] w-[12rem] bg-white dark:bg-[#1F2937] border border-gray-200 dark:border-gray-700 rounded-[0.5rem] shadow-lg py-[0.5rem] z-50 animate-fade-in"
            >
              <button
                role="menuitem"
                type="button"
                onClick={() => {
                  onExport('markdown');
                  setIsExportOpen(false);
                }}
                className="touch-target w-full px-[1rem] text-left text-[0.875rem] text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700/80 transition-colors gap-[0.75rem] justify-start"
              >
                <FileText className="w-[1rem] h-[1rem] text-[#4F46E5]" aria-hidden="true" />
                <span>Export Markdown (.md)</span>
              </button>

              <button
                role="menuitem"
                type="button"
                onClick={() => {
                  onExport('json');
                  setIsExportOpen(false);
                }}
                className="touch-target w-full px-[1rem] text-left text-[0.875rem] text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700/80 transition-colors gap-[0.75rem] justify-start"
              >
                <FileCode className="w-[1rem] h-[1rem] text-[#10B981]" aria-hidden="true" />
                <span>Export JSON (.json)</span>
              </button>

              <button
                role="menuitem"
                type="button"
                onClick={() => {
                  onExport('text');
                  setIsExportOpen(false);
                }}
                className="touch-target w-full px-[1rem] text-left text-[0.875rem] text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700/80 transition-colors gap-[0.75rem] justify-start"
              >
                <FileText className="w-[1rem] h-[1rem] text-gray-400" aria-hidden="true" />
                <span>Export Plain Text (.txt)</span>
              </button>
            </div>
          )}
        </div>

        {/* Separator */}
        <div className="h-[1.5rem] w-[1px] bg-gray-200 dark:bg-gray-800 mx-[0.25rem] hidden sm:block" />

        {/* Settings Toggle Button */}
        <button
          type="button"
          onClick={onToggleSettings}
          aria-label={isSettingsOpen ? 'Close contextual settings panel' : 'Open contextual settings panel'}
          aria-pressed={isSettingsOpen}
          className={`touch-target px-[0.75rem] rounded-[0.5rem] transition-colors focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none gap-[0.375rem] text-[0.875rem] font-medium ${
            isSettingsOpen
              ? 'bg-[#4F46E5]/10 text-[#4F46E5] dark:bg-[#6366F1]/20 dark:text-[#6366F1]'
              : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800'
          }`}
        >
          <Sliders className="w-[1.125rem] h-[1.125rem]" aria-hidden="true" />
          <span className="hidden md:inline">Settings</span>
        </button>

        {/* Light / Dark Mode Toggle */}
        <button
          type="button"
          onClick={onToggleTheme}
          aria-label={themeMode === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          className="touch-target rounded-[0.5rem] text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none"
        >
          {themeMode === 'dark' ? (
            <Sun className="w-[1.25rem] h-[1.25rem] text-amber-400" aria-hidden="true" />
          ) : (
            <Moon className="w-[1.25rem] h-[1.25rem]" aria-hidden="true" />
          )}
        </button>
      </div>
    </header>
  );
};
