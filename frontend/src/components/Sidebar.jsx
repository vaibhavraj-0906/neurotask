import React from 'react'

/**
 * Sidebar Component
 */
export const Sidebar = ({ stats, onNavigate }) => {
  return (
    <aside className="w-64 bg-gray-50 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4 hidden lg:block">
      <div className="space-y-6">
        {/* Quick Stats */}
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">📊 Stats</h3>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Total Tasks</span>
              <span className="font-bold dark:text-gray-200">{stats?.total || 0}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Active</span>
              <span className="font-bold text-blue-600 dark:text-blue-400">{stats?.active || 0}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Completed</span>
              <span className="font-bold text-green-600 dark:text-green-400">{stats?.completed || 0}</span>
            </div>
          </div>
        </div>

        {/* Priority Breakdown */}
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">🎯 By Priority</h3>
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 rounded-full bg-red-500"></div>
              <span className="text-gray-600 dark:text-gray-400">High</span>
              <span className="ml-auto font-bold dark:text-gray-200">{stats?.byPriority?.high || 0}</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 rounded-full bg-amber-500"></div>
              <span className="text-gray-600 dark:text-gray-400">Medium</span>
              <span className="ml-auto font-bold dark:text-gray-200">{stats?.byPriority?.medium || 0}</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 rounded-full bg-blue-500"></div>
              <span className="text-gray-600 dark:text-gray-400">Low</span>
              <span className="ml-auto font-bold dark:text-gray-200">{stats?.byPriority?.low || 0}</span>
            </div>
          </div>
        </div>

        {/* Quick Links */}
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">⚡ Quick Links</h3>
          <div className="space-y-2">
            <button 
              onClick={() => onNavigate('all')}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm dark:text-gray-300"
            >
              📋 All Tasks
            </button>
            <button 
              onClick={() => onNavigate('upcoming')}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm dark:text-gray-300"
            >
              📅 Upcoming
            </button>
            <button 
              onClick={() => onNavigate('completed')}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm dark:text-gray-300"
            >
              ✅ Completed
            </button>
          </div>
        </div>
      </div>
    </aside>
  )
}
