import React from 'react'

/**
 * Sidebar Component
 */
export const Sidebar = ({ stats, onNavigate }) => {
  return (
    <aside className="w-64 bg-gray-50 border-r border-gray-200 p-4 hidden lg:block">
      <div className="space-y-6">
        {/* Quick Stats */}
        <div>
          <h3 className="font-semibold text-gray-900 mb-3">📊 Stats</h3>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Total Tasks</span>
              <span className="font-bold">{stats?.total || 0}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Active</span>
              <span className="font-bold text-blue-600">{stats?.active || 0}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Completed</span>
              <span className="font-bold text-green-600">{stats?.completed || 0}</span>
            </div>
          </div>
        </div>

        {/* Priority Breakdown */}
        <div>
          <h3 className="font-semibold text-gray-900 mb-3">🎯 By Priority</h3>
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 rounded-full bg-red-500"></div>
              <span className="text-gray-600">High</span>
              <span className="ml-auto font-bold">{stats?.byPriority?.high || 0}</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 rounded-full bg-amber-500"></div>
              <span className="text-gray-600">Medium</span>
              <span className="ml-auto font-bold">{stats?.byPriority?.medium || 0}</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 rounded-full bg-blue-500"></div>
              <span className="text-gray-600">Low</span>
              <span className="ml-auto font-bold">{stats?.byPriority?.low || 0}</span>
            </div>
          </div>
        </div>

        {/* Quick Links */}
        <div>
          <h3 className="font-semibold text-gray-900 mb-3">⚡ Quick Links</h3>
          <div className="space-y-2">
            <button 
              onClick={() => onNavigate('all')}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm"
            >
              📋 All Tasks
            </button>
            <button 
              onClick={() => onNavigate('upcoming')}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm"
            >
              📅 Upcoming
            </button>
            <button 
              onClick={() => onNavigate('completed')}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm"
            >
              ✅ Completed
            </button>
          </div>
        </div>
      </div>
    </aside>
  )
}
