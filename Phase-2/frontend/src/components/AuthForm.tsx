'use client'

import { FormEvent, useState } from 'react'

export interface AuthFormFields {
  email?: string
  password: string
  name?: string
}

interface AuthFormProps {
  onSubmit: (data: AuthFormFields) => Promise<void>
  isLoading: boolean
  error?: string | null
  submitLabel: string
  includeNameField?: boolean
  onErrorDismiss?: () => void
}

export default function AuthForm({
  onSubmit,
  isLoading,
  error,
  submitLabel,
  includeNameField = false,
  onErrorDismiss,
}: AuthFormProps) {
  const [formData, setFormData] = useState<AuthFormFields>({
    email: '',
    password: '',
    ...(includeNameField && { name: '' }),
  })

  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({})

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {}

    if (!formData.email) {
      errors.email = 'Email is required'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Please enter a valid email'
    }

    if (!formData.password) {
      errors.password = 'Password is required'
    } else if (formData.password.length < 6) {
      errors.password = 'Password must be at least 6 characters'
    }

    if (includeNameField && !formData.name) {
      errors.name = 'Name is required'
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
      await onSubmit(formData)
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

      {/* Name Field (Signup Only) */}
      {includeNameField && (
        <div>
          <label htmlFor="name" className="block text-sm font-medium mb-1">
            Full Name
          </label>
          <input
            id="name"
            type="text"
            placeholder="John Doe"
            value={formData.name || ''}
            onChange={(e) => {
              setFormData({ ...formData, name: e.target.value })
              if (validationErrors.name) {
                setValidationErrors({ ...validationErrors, name: '' })
              }
            }}
            className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
              validationErrors.name
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500'
            }`}
            disabled={isLoading}
          />
          {validationErrors.name && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.name}</p>
          )}
        </div>
      )}

      {/* Email Field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1">
          Email Address
        </label>
        <input
          id="email"
          type="email"
          placeholder="you@example.com"
          value={formData.email || ''}
          onChange={(e) => {
            setFormData({ ...formData, email: e.target.value })
            if (validationErrors.email) {
              setValidationErrors({ ...validationErrors, email: '' })
            }
          }}
          className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
            validationErrors.email
              ? 'border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:ring-blue-500'
          }`}
          disabled={isLoading}
        />
        {validationErrors.email && (
          <p className="text-red-500 text-sm mt-1">{validationErrors.email}</p>
        )}
      </div>

      {/* Password Field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          placeholder="••••••••"
          value={formData.password}
          onChange={(e) => {
            setFormData({ ...formData, password: e.target.value })
            if (validationErrors.password) {
              setValidationErrors({ ...validationErrors, password: '' })
            }
          }}
          className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
            validationErrors.password
              ? 'border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:ring-blue-500'
          }`}
          disabled={isLoading}
        />
        {validationErrors.password && (
          <p className="text-red-500 text-sm mt-1">{validationErrors.password}</p>
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
