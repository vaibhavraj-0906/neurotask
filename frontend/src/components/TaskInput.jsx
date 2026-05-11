import React, { useState } from 'react'

/**
 * Task Input Component
 * Main natural language input field
 */
export const TaskInput = ({ onSubmit, isLoading, placeholder = "Type a task naturally..." }) => {
  const [input, setInput] = useState('')
  const [preview, setPreview] = useState(null)
  const [showPreview, setShowPreview] = useState(false)

  const handleChange = (e) => {
    const text = e.target.value
    setInput(text)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && input.trim()) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleSubmit = async () => {
    if (!input.trim()) return

    try {
      // Call parent submit handler
      await onSubmit(input)
      setInput('')
      setPreview(null)
      setShowPreview(false)
    } catch (error) {
      console.error('Error submitting task:', error)
    }
  }

  return (
    <div className="w-full">
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <textarea
            value={input}
            onChange={handleChange}
            onKeyPress={handleKeyPress}
            placeholder={placeholder}
            rows="2"
            disabled={isLoading}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          />
        </div>
        <button
          onClick={handleSubmit}
          disabled={isLoading || !input.trim()}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors font-medium"
        >
          {isLoading ? 'Creating...' : 'Add Task'}
        </button>
      </div>
      
      {showPreview && preview && (
        <div className="mt-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-2">📋 Task Preview</h4>
          <div className="text-sm space-y-1">
            <p><span className="font-medium">Task:</span> {preview.task_title}</p>
            {preview.deadline && <p><span className="font-medium">Due:</span> {preview.deadline}</p>}
            {preview.priority && <p><span className="font-medium">Priority:</span> {preview.priority}</p>}
            {preview.category && <p><span className="font-medium">Category:</span> {preview.category}</p>}
            {preview.recurrence && <p><span className="font-medium">Recurrence:</span> {preview.recurrence}</p>}
            <p><span className="font-medium">Confidence:</span> {preview.confidence_score}%</p>
          </div>
        </div>
      )}
    </div>
  )
}
