/**
 * Utility functions
 */

export const formatDate = (dateString) => {
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

export const calculateStats = (tasks) => {
  if (!tasks || tasks.length === 0) {
    return {
      total: 0,
      active: 0,
      completed: 0,
      byPriority: { high: 0, medium: 0, low: 0 },
      byCategory: {}
    }
  }

  const stats = {
    total: tasks.length,
    active: tasks.filter(t => !t.completed).length,
    completed: tasks.filter(t => t.completed).length,
    byPriority: { high: 0, medium: 0, low: 0 },
    byCategory: {}
  }

  tasks.forEach(task => {
    // Count by priority
    const priority = task.priority || 'medium'
    if (stats.byPriority[priority] !== undefined) {
      stats.byPriority[priority]++
    }

    // Count by category
    if (task.category) {
      stats.byCategory[task.category] = (stats.byCategory[task.category] || 0) + 1
    }
  })

  return stats
}

export const groupTasksByDate = (tasks) => {
  const grouped = {
    today: [],
    tomorrow: [],
    upcoming: [],
    overdue: []
  }

  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)

  tasks.forEach(task => {
    if (!task.deadline) {
      grouped.upcoming.push(task)
      return
    }

    const deadline = new Date(task.deadline)
    const deadlineDate = new Date(deadline.getFullYear(), deadline.getMonth(), deadline.getDate())

    if (deadlineDate < today) {
      grouped.overdue.push(task)
    } else if (deadlineDate.getTime() === today.getTime()) {
      grouped.today.push(task)
    } else if (deadlineDate.getTime() === tomorrow.getTime()) {
      grouped.tomorrow.push(task)
    } else {
      grouped.upcoming.push(task)
    }
  })

  return grouped
}

export const getUniqueCategories = (tasks) => {
  const categories = new Set()
  tasks.forEach(task => {
    if (task.category) categories.add(task.category)
  })
  return Array.from(categories).sort()
}
