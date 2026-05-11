import { useEffect, useState } from 'react'

/**
 * Custom hook for managing dark mode
 * Persists to localStorage and applies to document
 */
export const useDarkMode = () => {
  const [isDark, setIsDark] = useState(() => {
    // Check localStorage first
    const stored = localStorage.getItem('darkMode')
    if (stored !== null) {
      return stored === 'true'
    }

    // Check system preference
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  })

  // Apply dark mode to document
  useEffect(() => {
    const htmlElement = document.documentElement
    if (isDark) {
      htmlElement.classList.add('dark')
    } else {
      htmlElement.classList.remove('dark')
    }

    // Save to localStorage
    localStorage.setItem('darkMode', isDark.toString())
  }, [isDark])

  const toggleDarkMode = () => {
    setIsDark(prev => !prev)
  }

  return { isDark, toggleDarkMode }
}
