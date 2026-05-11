import React from 'react'

/**
 * Filter and Sort Component
 */
export const TaskFilters = ({ 
  filters, 
  onFilterChange, 
  categories, 
  priorities = ['high', 'medium', 'low'] 
}) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-4 mb-6 border border-gray-200 dark:border-gray-700">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Priority Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Priority</label>
          <select
            value={filters.priority || ''}
            onChange={(e) => onFilterChange('priority', e.target.value || null)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          >
            <option value="">All Priorities</option>
            {priorities.map(p => (
              <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
            ))}
          </select>
        </div>

        {/* Category Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Category</label>
          <select
            value={filters.category || ''}
            onChange={(e) => onFilterChange('category', e.target.value || null)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          >
            <option value="">All Categories</option>
            {categories.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
          <select
            value={filters.completed === undefined ? '' : filters.completed}
            onChange={(e) => {
              if (e.target.value === '') {
                onFilterChange('completed', undefined)
              } else {
                onFilterChange('completed', e.target.value === 'true')
              }
            }}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          >
            <option value="">All Tasks</option>
            <option value="false">Active</option>
            <option value="true">Completed</option>
          </select>
        </div>

        {/* Reset Filters */}
        <div className="flex items-end">
          <button
            onClick={() => onFilterChange('reset')}
            className="w-full px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
          >
            Reset Filters
          </button>
        </div>
      </div>
    </div>
  )
}
