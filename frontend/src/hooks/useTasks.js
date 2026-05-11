import { useState, useCallback } from 'react'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

/**
 * Custom hook for managing tasks
 */
export const useTasks = () => {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Fetch all tasks
  const fetchTasks = useCallback(async (filters = {}) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks/`, { params: filters })
      setTasks(response.data)
    } catch (err) {
      setError(err.message)
      console.error('Error fetching tasks:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  // Create task from natural language
  const createTask = useCallback(async (text) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post(`${API_BASE_URL}/tasks/create`, { text })
      setTasks(prev => [response.data, ...prev])
      return response.data
    } catch (err) {
      setError(err.message)
      console.error('Error creating task:', err)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  // Parse task without creating
  const parseTask = useCallback(async (text) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/tasks/parse`, { text })
      return response.data
    } catch (err) {
      console.error('Error parsing task:', err)
      throw err
    }
  }, [])

  // Update task
  const updateTask = useCallback(async (taskId, data) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.put(`${API_BASE_URL}/tasks/${taskId}`, data)
      setTasks(prev => prev.map(t => t.id === taskId ? response.data : t))
      return response.data
    } catch (err) {
      setError(err.message)
      console.error('Error updating task:', err)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  // Complete task
  const completeTask = useCallback(async (taskId) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/tasks/${taskId}/complete`)
      setTasks(prev => prev.map(t => t.id === taskId ? response.data : t))
      return response.data
    } catch (err) {
      setError(err.message)
      console.error('Error completing task:', err)
      throw err
    }
  }, [])

  // Delete task
  const deleteTask = useCallback(async (taskId) => {
    try {
      await axios.delete(`${API_BASE_URL}/tasks/${taskId}`)
      setTasks(prev => prev.filter(t => t.id !== taskId))
    } catch (err) {
      setError(err.message)
      console.error('Error deleting task:', err)
      throw err
    }
  }, [])

  // Search tasks
  const searchTasks = useCallback(async (query) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks/search/query`, { 
        params: { q: query } 
      })
      setTasks(response.data)
    } catch (err) {
      setError(err.message)
      console.error('Error searching tasks:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  // Get upcoming tasks
  const getUpcomingTasks = useCallback(async (days = 7) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks/upcoming`, {
        params: { days }
      })
      setTasks(response.data)
    } catch (err) {
      setError(err.message)
      console.error('Error fetching upcoming tasks:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    parseTask,
    updateTask,
    completeTask,
    deleteTask,
    searchTasks,
    getUpcomingTasks
  }
}
