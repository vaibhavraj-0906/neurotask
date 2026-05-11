import React from 'react'

/**
 * Header Component
 */
export const Header = ({ taskCount, completedCount }) => {
  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-4 shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">NeuroTask</h1>
          <p className="text-blue-100 text-sm mt-1">AI-powered task management for the modern mind</p>
        </div>
        <div className="text-right">
          <p className="text-3xl font-bold">{taskCount - completedCount}</p>
          <p className="text-blue-100 text-sm">Active Tasks</p>
        </div>
      </div>
    </div>
  )
}
