import React from 'react'

/**
 * Task Card Component
 * Displays individual task with actions
 */
export const TaskCard = ({ task, onComplete, onDelete, onEdit }) => {
  const getPriorityColor = (priority) => {
    const colors = {
      high: '#ef4444',
      medium: '#f59e0b',
      low: '#3b82f6'
    }
    return colors[priority] || '#9ca3af'
  }

  const getPriorityCategoryColor = (priority) => {
    const colors = {
      high: 'bg-red-50 dark:bg-red-900/20',
      medium: 'bg-amber-50 dark:bg-amber-900/20',
      low: 'bg-blue-50 dark:bg-blue-900/20'
    }
    return colors[priority] || 'bg-gray-50 dark:bg-gray-800'
  }

  const formatDate = (dateString) => {
    if (!dateString) return null
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return dateString
    }
  }

  return (
    <div className={`${getPriorityCategoryColor(task.priority)} rounded-lg border-l-4 p-4 mb-3 transition-all hover:shadow-md`} style={{borderLeftColor: getPriorityColor(task.priority)}}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onComplete(task.id)}
              className="w-5 h-5 rounded"
            />
            <div className="flex-1">
              <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-400 dark:text-gray-600' : 'text-gray-800 dark:text-gray-100'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{task.description}</p>
              )}
            </div>
          </div>
          
          <div className="flex flex-wrap gap-4 mt-3 ml-8 text-xs">
            {task.deadline && (
              <div className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                <span className="font-medium">📅</span>
                {formatDate(task.deadline)}
              </div>
            )}
            {task.category && (
              <div className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                <span className="font-medium">🏷️</span>
                {task.category}
              </div>
            )}
            {task.recurrence && (
              <div className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                <span className="font-medium">🔄</span>
                {task.recurrence}
              </div>
            )}
          </div>
        </div>
        
        <div className="flex gap-2 ml-4">
          <button
            onClick={() => onEdit(task.id)}
            className="p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors"
            title="Edit task"
          >
            ✏️
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="p-2 hover:bg-red-100 dark:hover:bg-red-900/40 rounded-lg transition-colors"
            title="Delete task"
          >
            🗑️
          </button>
        </div>
      </div>
    </div>
  )
}
