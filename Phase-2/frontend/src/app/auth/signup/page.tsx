'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import AuthForm, { AuthFormFields } from '@/components/AuthForm'
import { useAuth } from '@/hooks/useAuth'

export default function SignupPage() {
  const router = useRouter()
  const { signup, error, isLoading, clearError } = useAuth()
  const [successMessage, setSuccessMessage] = useState('')

  const handleSignup = async (data: AuthFormFields) => {
    try {
      await signup({
        email: data.email!,
        password: data.password,
        name: data.name!,
      })

      setSuccessMessage('Account created successfully! Redirecting to login...')

      // Redirect to login after 2 seconds
      setTimeout(() => {
        router.push('/auth/login')
      }, 2000)
    } catch (err: any) {
      // Error is handled by useAuth hook
    }
  }

  return (
    <div className="space-y-8">
      {/* Success Message */}
      {successMessage && (
        <div className="alert alert-success">
          <p>{successMessage}</p>
        </div>
      )}

      {/* Card */}
      <div className="card">
        <h1 className="text-3xl font-bold mb-2 text-center">Create Account</h1>
        <p className="text-gray-600 text-center mb-6">
          Join us to start managing your tasks effectively
        </p>

        <AuthForm
          onSubmit={handleSignup}
          isLoading={isLoading}
          error={error?.detail}
          submitLabel="Sign Up"
          includeNameField={true}
          onErrorDismiss={clearError}
        />

        {/* Login Link */}
        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Already have an account?{' '}
            <Link href="/auth/login" className="text-blue-600 hover:text-blue-700 font-medium">
              Login here
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
