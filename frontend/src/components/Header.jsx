import React from 'react'

/**
 * Header Component
 */
export const Header = ({ taskCount, completedCount, isDark, onToggleDarkMode }) => {
  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-700 dark:from-blue-900 dark:to-blue-800 text-white px-6 py-4 shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">NeuroTask</h1>
          <p className="text-blue-100 text-sm mt-1">AI-powered task management for the modern mind</p>
        </div>
        <div className="flex items-center gap-6">
          <div className="text-right">
            <p className="text-3xl font-bold">{taskCount - completedCount}</p>
            <p className="text-blue-100 text-sm">Active Tasks</p>
          </div>
          <button
            onClick={onToggleDarkMode}
            className="p-2 rounded-lg bg-blue-500 hover:bg-blue-400 dark:bg-blue-700 dark:hover:bg-blue-600 transition-colors"
            title="Toggle dark mode"
          >
            {isDark ? '☀️' : '🌙'}
          </button>
        </div>
      </div>
    </div>
  )
}
