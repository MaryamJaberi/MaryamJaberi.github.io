import React, { useState } from 'react';
import { 
  Plus, 
  Search, 
  Pin, 
  Trash2, 
  Clock, 
  X, 
  MessageSquare, 
  Layers, 
  Sparkles,
  FolderOpen
} from 'lucide-react';
import { TaskSession } from '../types/studio';

interface SidebarProps {
  sessions: TaskSession[];
  activeSessionId: string;
  onSelectSession: (sessionId: string) => void;
  onNewSession: () => void;
  onDeleteSession: (sessionId: string) => void;
  onTogglePinSession: (sessionId: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  activeSessionId,
  onSelectSession,
  onNewSession,
  onDeleteSession,
  onTogglePinSession,
  isOpen,
  onClose,
}) => {
  const [searchQuery, setSearchQuery] = useState('');

  // Filter sessions based on search
  const filteredSessions = sessions.filter((s) =>
    s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const pinnedSessions = filteredSessions.filter((s) => s.pinned);
  const recentSessions = filteredSessions.filter((s) => !s.pinned);

  return (
    <>
      {/* Mobile Backdrop Overlay (<768px) */}
      {isOpen && (
        <div 
          onClick={onClose}
          aria-hidden="true"
          className="fixed inset-0 bg-black/50 z-40 md:hidden backdrop-blur-xs transition-opacity"
        />
      )}

      {/* Semantic Aside & Nav Element */}
      <aside
        id="sidebar"
        aria-label="Task history and navigation"
        className={`fixed md:static inset-y-0 left-0 z-50 w-[18rem] bg-white dark:bg-[#111827] border-r border-gray-200 dark:border-gray-800 flex flex-col h-full transform transition-transform duration-300 ease-in-out select-none ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        {/* Level 1: Sidebar Header with New Task Button & Close (Mobile) */}
        <div className="p-[1rem] border-b border-gray-200 dark:border-gray-800 flex flex-col gap-[0.75rem]">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-[0.5rem] font-semibold text-[0.875rem] text-gray-900 dark:text-gray-100">
              <Layers className="w-[1.125rem] h-[1.125rem] text-[#4F46E5] dark:text-[#6366F1]" aria-hidden="true" />
              <span>Task Navigator</span>
            </div>

            {/* Mobile close button */}
            <button
              type="button"
              onClick={onClose}
              aria-label="Close task history sidebar"
              className="touch-target md:hidden rounded-[0.5rem] text-gray-500 hover:text-gray-900 dark:hover:text-white"
            >
              <X className="w-[1.25rem] h-[1.25rem]" aria-hidden="true" />
            </button>
          </div>

          {/* New Prompt / Task Button - Primary Action */}
          <button
            type="button"
            onClick={() => {
              onNewSession();
              if (window.innerWidth < 768) onClose();
            }}
            aria-label="Start new prompt session"
            className="touch-target w-full rounded-[0.5rem] bg-[#4F46E5] hover:bg-[#4338CA] text-white text-[0.875rem] font-medium transition-colors gap-[0.5rem] shadow-xs focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none"
          >
            <Plus className="w-[1.125rem] h-[1.125rem]" aria-hidden="true" />
            <span>New Prompt Session</span>
          </button>

          {/* Search Box */}
          <div className="relative">
            <Search className="absolute left-[0.75rem] top-1/2 -translate-y-1/2 w-[1rem] h-[1rem] text-gray-400" aria-hidden="true" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search prompts..."
              aria-label="Filter task history by title or category"
              className="w-full pl-[2.25rem] pr-[0.75rem] py-[0.5rem] text-[0.875rem] bg-gray-50 dark:bg-gray-800/80 border border-gray-200 dark:border-gray-700 rounded-[0.5rem] text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:bg-white dark:focus:bg-gray-800 focus-visible:ring-2 focus-visible:ring-[#4F46E5] focus-visible:outline-none transition-colors"
            />
          </div>
        </div>

        {/* Level 2 & 3: Navigation Lists */}
        <nav aria-label="Session list" className="flex-1 overflow-y-auto p-[0.75rem] space-y-[1.25rem]">
          {/* Section: Pinned Tasks (Level 2) */}
          {pinnedSessions.length > 0 && (
            <div>
              <div className="flex items-center gap-[0.375rem] px-[0.5rem] mb-[0.375rem] text-[0.75rem] font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                <Pin className="w-[0.75rem] h-[0.75rem] rotate-45 text-[#4F46E5] dark:text-[#6366F1]" aria-hidden="true" />
                <span>Pinned Tasks ({pinnedSessions.length})</span>
              </div>
              <ul className="space-y-[0.25rem] m-0 p-0 list-none">
                {pinnedSessions.map((session) => {
                  const isActive = session.id === activeSessionId;
                  return (
                    <li key={session.id}>
                      <div
                        className={`group relative flex items-center justify-between rounded-[0.5rem] px-[0.75rem] py-[0.625rem] text-[0.875rem] cursor-pointer transition-colors border ${
                          isActive
                            ? 'bg-[#4F46E5]/10 dark:bg-[#6366F1]/20 border-[#4F46E5]/40 text-[#4F46E5] dark:text-[#F9FAFB] font-medium'
                            : 'border-transparent text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800/70'
                        }`}
                        onClick={() => {
                          onSelectSession(session.id);
                          if (window.innerWidth < 768) onClose();
                        }}
                      >
                        <div className="flex items-center gap-[0.5rem] min-w-0 pr-[1rem]">
                          <MessageSquare className={`w-[1rem] h-[1rem] shrink-0 ${isActive ? 'text-[#4F46E5] dark:text-[#6366F1]' : 'text-gray-400'}`} aria-hidden="true" />
                          <span className="truncate">{session.title}</span>
                        </div>

                        {/* Actions (Level 3) */}
                        <div className="flex items-center gap-[0.25rem] shrink-0">
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              onTogglePinSession(session.id);
                            }}
                            aria-label="Unpin task"
                            className="p-[0.375rem] rounded-[0.25rem] text-gray-400 hover:text-[#4F46E5] dark:hover:text-[#6366F1]"
                          >
                            <Pin className="w-[0.875rem] h-[0.875rem] fill-current" aria-hidden="true" />
                          </button>
                        </div>
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
          )}

          {/* Section: Recent Tasks (Level 2) */}
          <div>
            <div className="flex items-center gap-[0.375rem] px-[0.5rem] mb-[0.375rem] text-[0.75rem] font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              <Clock className="w-[0.75rem] h-[0.75rem] text-gray-400" aria-hidden="true" />
              <span>Recent Sessions ({recentSessions.length})</span>
            </div>

            {recentSessions.length === 0 ? (
              <div className="px-[0.75rem] py-[1rem] text-[0.8125rem] text-gray-400 text-center">
                No recent sessions found.
              </div>
            ) : (
              <ul className="space-y-[0.25rem] m-0 p-0 list-none">
                {recentSessions.map((session) => {
                  const isActive = session.id === activeSessionId;
                  return (
                    <li key={session.id}>
                      <div
                        className={`group relative flex items-center justify-between rounded-[0.5rem] px-[0.75rem] py-[0.625rem] text-[0.875rem] cursor-pointer transition-colors border ${
                          isActive
                            ? 'bg-[#4F46E5]/10 dark:bg-[#6366F1]/20 border-[#4F46E5]/40 text-[#4F46E5] dark:text-[#F9FAFB] font-medium'
                            : 'border-transparent text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800/70'
                        }`}
                        onClick={() => {
                          onSelectSession(session.id);
                          if (window.innerWidth < 768) onClose();
                        }}
                      >
                        <div className="flex items-center gap-[0.5rem] min-w-0 pr-[0.75rem]">
                          <MessageSquare className={`w-[1rem] h-[1rem] shrink-0 ${isActive ? 'text-[#4F46E5] dark:text-[#6366F1]' : 'text-gray-400'}`} aria-hidden="true" />
                          <div className="flex flex-col min-w-0">
                            <span className="truncate">{session.title}</span>
                            <span className="text-[0.75rem] text-gray-400 dark:text-gray-500">
                              {session.category} · {session.messages.length} msgs
                            </span>
                          </div>
                        </div>

                        {/* Actions (Level 3) */}
                        <div className="flex items-center gap-[0.125rem] opacity-0 group-hover:opacity-100 focus-within:opacity-100 transition-opacity">
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              onTogglePinSession(session.id);
                            }}
                            aria-label="Pin task"
                            className="p-[0.375rem] rounded-[0.25rem] text-gray-400 hover:text-[#4F46E5] dark:hover:text-[#6366F1]"
                          >
                            <Pin className="w-[0.875rem] h-[0.875rem]" aria-hidden="true" />
                          </button>
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              onDeleteSession(session.id);
                            }}
                            aria-label={`Delete task ${session.title}`}
                            className="p-[0.375rem] rounded-[0.25rem] text-gray-400 hover:text-[#EF4444]"
                          >
                            <Trash2 className="w-[0.875rem] h-[0.875rem]" aria-hidden="true" />
                          </button>
                        </div>
                      </div>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        </nav>

        {/* Sidebar Footer Metadata */}
        <div className="p-[0.75rem] border-t border-gray-200 dark:border-gray-800 bg-gray-50/70 dark:bg-gray-900/40 text-[0.75rem] text-gray-500 dark:text-gray-400 flex items-center justify-between">
          <div className="flex items-center gap-[0.375rem]">
            <FolderOpen className="w-[0.875rem] h-[0.875rem] text-[#4F46E5]" aria-hidden="true" />
            <span>Workspace: Production</span>
          </div>
          <span className="font-mono text-[0.6875rem] bg-gray-200 dark:bg-gray-800 px-[0.375rem] py-[0.125rem] rounded">
            v2.5
          </span>
        </div>
      </aside>
    </>
  );
};
