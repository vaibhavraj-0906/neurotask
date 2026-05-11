import React from 'react'

/**
 * Task List Component
 */
export const TaskList = ({ tasks, onComplete, onDelete, onEdit, emptyMessage = "No tasks yet. Create one to get started!" }) => {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 dark:text-gray-400 text-lg">{emptyMessage}</p>
        <p className="text-gray-400 dark:text-gray-500 text-sm mt-2">✨ Try typing something like: "Finish assignment tomorrow at 8pm"</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {tasks.map(task => (
        <TaskCard
          key={task.id}
          task={task}
          onComplete={onComplete}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  )
}

import { TaskCard } from './TaskCard'
