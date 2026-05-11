import { useState, useCallback, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

/**
 * Custom hook for managing notifications
 */
export const useNotifications = () => {
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Fetch due reminders
  const getDueReminders = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_BASE_URL}/notifications/due`)
      setNotifications(response.data)
      return response.data
    } catch (err) {
      setError(err.message)
      console.error('Error fetching notifications:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  // Get upcoming reminders
  const getUpcomingReminders = useCallback(async (hours = 24) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_BASE_URL}/notifications/upcoming`, {
        params: { hours }
      })
      setNotifications(response.data)
      return response.data
    } catch (err) {
      setError(err.message)
      console.error('Error fetching upcoming reminders:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  // Check notifications manually
  const checkNotifications = useCallback(async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/notifications/check`)
      return response.data
    } catch (err) {
      console.error('Error checking notifications:', err)
    }
  }, [])

  // Set up periodic polling
  useEffect(() => {
    const interval = setInterval(() => {
      getDueReminders()
    }, 60000) // Check every minute

    return () => clearInterval(interval)
  }, [getDueReminders])

  return {
    notifications,
    loading,
    error,
    getDueReminders,
    getUpcomingReminders,
    checkNotifications
  }
}
