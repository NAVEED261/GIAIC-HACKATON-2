'use client'

import { FormEvent, useState } from 'react'
import { TaskPriority, CreateTaskRequest, UpdateTaskRequest } from '@/types/task'

interface TaskFormProps {
  onSubmit: (data: CreateTaskRequest | UpdateTaskRequest) => Promise<void>
  isLoading: boolean
  error?: string | null
  submitLabel: string
  onErrorDismiss?: () => void
  initialData?: {
    title: string
    description?: string | null
    priority: TaskPriority
    due_date?: string | null
  }
}

export default function TaskForm({
  onSubmit,
  isLoading,
  error,
  submitLabel,
  onErrorDismiss,
  initialData,
}: TaskFormProps) {
  const [formData, setFormData] = useState<CreateTaskRequest>({
    title: initialData?.title || '',
    description: initialData?.description || '',
    priority: initialData?.priority || 'medium',
    due_date: initialData?.due_date || '',
  })

  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({})

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {}

    if (!formData.title.trim()) {
      errors.title = 'Task title is required'
    } else if (formData.title.length > 200) {
      errors.title = 'Title must be less than 200 characters'
    }

    if (formData.description && formData.description.length > 1000) {
      errors.description = 'Description must be less than 1000 characters'
    }

    if (formData.due_date && new Date(formData.due_date) < new Date()) {
      errors.due_date = 'Due date cannot be in the past'
    }

    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    try {
      await onSubmit({
        title: formData.title,
        description: formData.description || undefined,
        priority: formData.priority,
        due_date: formData.due_date || undefined,
      })
    } catch (err) {
      // Error is handled by parent component
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Error Alert */}
      {error && (
        <div className="alert alert-error">
          <div className="flex justify-between items-start">
            <span>{error}</span>
            {onErrorDismiss && (
              <button
                type="button"
                onClick={onErrorDismiss}
                className="text-xl font-bold cursor-pointer"
              >
                ×
              </button>
            )}
          </div>
        </div>
      )}

      {/* Title Field */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium mb-1">
          Task Title *
        </label>
        <input
          id="title"
          type="text"
          placeholder="Enter task title..."
          maxLength={200}
          value={formData.title}
          onChange={(e) => {
            setFormData({ ...formData, title: e.target.value })
            if (validationErrors.title) {
              setValidationErrors({ ...validationErrors, title: '' })
            }
          }}
          className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
            validationErrors.title
              ? 'border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:ring-blue-500'
          }`}
          disabled={isLoading}
          required
        />
        <div className="flex justify-between items-center">
          {validationErrors.title && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.title}</p>
          )}
          <p className="text-gray-400 text-xs mt-1">{formData.title.length}/200</p>
        </div>
      </div>

      {/* Description Field */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium mb-1">
          Description
        </label>
        <textarea
          id="description"
          placeholder="Enter task description..."
          maxLength={1000}
          rows={4}
          value={formData.description || ''}
          onChange={(e) => {
            setFormData({ ...formData, description: e.target.value })
            if (validationErrors.description) {
              setValidationErrors({ ...validationErrors, description: '' })
            }
          }}
          className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
            validationErrors.description
              ? 'border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:ring-blue-500'
          }`}
          disabled={isLoading}
        />
        <div className="flex justify-between items-center">
          {validationErrors.description && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.description}</p>
          )}
          <p className="text-gray-400 text-xs mt-1">
            {(formData.description || '').length}/1000
          </p>
        </div>
      </div>

      {/* Priority Field */}
      <div>
        <label htmlFor="priority" className="block text-sm font-medium mb-1">
          Priority
        </label>
        <select
          id="priority"
          value={formData.priority}
          onChange={(e) =>
            setFormData({
              ...formData,
              priority: e.target.value as TaskPriority,
            })
          }
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isLoading}
        >
          <option value="low">🟢 Low Priority</option>
          <option value="medium">🟡 Medium Priority</option>
          <option value="high">🔴 High Priority</option>
        </select>
      </div>

      {/* Due Date Field */}
      <div>
        <label htmlFor="due_date" className="block text-sm font-medium mb-1">
          Due Date
        </label>
        <input
          id="due_date"
          type="datetime-local"
          value={formData.due_date || ''}
          onChange={(e) => {
            setFormData({ ...formData, due_date: e.target.value })
            if (validationErrors.due_date) {
              setValidationErrors({ ...validationErrors, due_date: '' })
            }
          }}
          className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
            validationErrors.due_date
              ? 'border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:ring-blue-500'
          }`}
          disabled={isLoading}
        />
        {validationErrors.due_date && (
          <p className="text-red-500 text-sm mt-1">{validationErrors.due_date}</p>
        )}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading}
        className={`w-full py-2 px-4 rounded-lg font-medium text-white transition-colors ${
          isLoading
            ? 'bg-blue-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'
        }`}
      >
        {isLoading ? (
          <span className="flex items-center justify-center">
            <span className="spinner mr-2"></span>
            Processing...
          </span>
        ) : (
          submitLabel
        )}
      </button>
    </form>
  )
}
