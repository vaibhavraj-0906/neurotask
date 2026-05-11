import React, { useEffect, useState } from 'react'
import { useTasks } from './hooks/useTasks'
import { useNotifications } from './hooks/useNotifications'
import { useDarkMode } from './hooks/useDarkMode'
import { calculateStats, getUniqueCategories } from './utils'
import { TaskInput, TaskList, TaskFilters, Header, Sidebar } from './components'
import './styles/global.css'

/**
 * Main App Component
 */
function App() {
  // State management
  const { tasks, loading, error, fetchTasks, createTask, completeTask, deleteTask } = useTasks()
  const { getDueReminders } = useNotifications()
  const { isDark, toggleDarkMode } = useDarkMode()
  const [filters, setFilters] = useState({})
  const [currentView, setCurrentView] = useState('all')
  const [filteredTasks, setFilteredTasks] = useState([])
  const [stats, setStats] = useState({})

  // Calculate stats whenever tasks change
  useEffect(() => {
    setStats(calculateStats(tasks))
  }, [tasks])

  // Apply filters to tasks
  useEffect(() => {
    let result = tasks

    // Filter by completion status
    if (filters.completed !== undefined) {
      result = result.filter(t => t.completed === filters.completed)
    }

    // Filter by priority
    if (filters.priority) {
      result = result.filter(t => t.priority === filters.priority)
    }

    // Filter by category
    if (filters.category) {
      result = result.filter(t => t.category === filters.category)
    }

    // Sort by priority and deadline
    result = result.sort((a, b) => {
      const priorityOrder = { high: 0, medium: 1, low: 2 }
      const aPriority = priorityOrder[a.priority] ?? 3
      const bPriority = priorityOrder[b.priority] ?? 3

      if (aPriority !== bPriority) {
        return aPriority - bPriority
      }

      // If same priority, sort by deadline
      if (a.deadline && b.deadline) {
        return new Date(a.deadline) - new Date(b.deadline)
      }

      return 0
    })

    setFilteredTasks(result)
  }, [tasks, filters])

  // Initial load
  useEffect(() => {
    fetchTasks()
    getDueReminders()

    // Set up auto-refresh every 5 minutes
    const interval = setInterval(() => {
      fetchTasks()
      getDueReminders()
    }, 300000)

    return () => clearInterval(interval)
  }, [fetchTasks, getDueReminders])

  // Handle task creation
  const handleCreateTask = async (text) => {
    try {
      await createTask(text)
      // Optionally show success toast
    } catch (err) {
      console.error('Failed to create task:', err)
      // Show error toast
    }
  }

  // Handle task completion
  const handleCompleteTask = async (taskId) => {
    try {
      await completeTask(taskId)
    } catch (err) {
      console.error('Failed to complete task:', err)
    }
  }

  // Handle task deletion
  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(taskId)
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }
  }

  // Handle filter changes
  const handleFilterChange = (filterKey, value) => {
    if (filterKey === 'reset') {
      setFilters({})
      return
    }
    setFilters(prev => ({
      ...prev,
      [filterKey]: value
    }))
  }

  const categories = getUniqueCategories(tasks)

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      {/* Sidebar */}
      <Sidebar
        stats={stats}
        onNavigate={(view) => {
          setCurrentView(view)
          if (view === 'all') setFilters({})
          else if (view === 'completed') setFilters({ completed: true })
          else if (view === 'upcoming') setFilters({ completed: false })
        }}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header taskCount={tasks.length} completedCount={stats.completed || 0} isDark={isDark} onToggleDarkMode={toggleDarkMode} />

        {/* Content Area */}
        <div className="flex-1 overflow-auto p-6">
          <div className="max-w-4xl mx-auto">
            {/* Task Input */}
            <div className="mb-8">
              <TaskInput
                onSubmit={handleCreateTask}
                isLoading={loading}
                placeholder="Type a task naturally... e.g., 'Finish OS lab report tonight' or 'Gym every Mon, Wed, Fri at 6am'"
              />
            </div>

            {/* Error Display */}
            {error && (
              <div className="mb-4 p-4 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg text-red-700 dark:text-red-300">
                ⚠️ {error}
              </div>
            )}

            {/* Filters */}
            {tasks.length > 0 && (
              <TaskFilters
                filters={filters}
                onFilterChange={handleFilterChange}
                categories={categories}
              />
            )}

            {/* Task List */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md dark:shadow-lg p-6">
              <TaskList
                tasks={filteredTasks}
                onComplete={handleCompleteTask}
                onDelete={handleDeleteTask}
                onEdit={(taskId) => {
                  console.log('Edit task:', taskId)
                  // TODO: Implement edit modal
                }}
                emptyMessage={
                  tasks.length === 0
                    ? "📝 No tasks yet. Create your first task to get started!"
                    : "✨ No tasks match your filters. Try adjusting them!"
                }
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
