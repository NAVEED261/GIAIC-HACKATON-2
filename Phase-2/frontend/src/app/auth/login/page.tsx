'use client'

import { useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import AuthForm, { AuthFormFields } from '@/components/AuthForm'
import { useAuth } from '@/hooks/useAuth'

export default function LoginPage() {
  const router = useRouter()
  const { login, user, error, isLoading, clearError } = useAuth()

  // Redirect to dashboard if already logged in
  useEffect(() => {
    if (user) {
      router.push('/dashboard')
    }
  }, [user, router])

  const handleLogin = async (data: AuthFormFields) => {
    try {
      await login({
        email: data.email!,
        password: data.password,
      })

      // Redirect to dashboard on successful login
      router.push('/dashboard')
    } catch (err: any) {
      // Error is handled by useAuth hook
    }
  }

  return (
    <div className="space-y-8">
      {/* Card */}
      <div className="card">
        <h1 className="text-3xl font-bold mb-2 text-center">Welcome Back</h1>
        <p className="text-gray-600 text-center mb-6">Sign in to your account</p>

        <AuthForm
          onSubmit={handleLogin}
          isLoading={isLoading}
          error={error?.detail}
          submitLabel="Sign In"
          includeNameField={false}
          onErrorDismiss={clearError}
        />

        {/* Signup Link */}
        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Don't have an account?{' '}
            <Link href="/auth/signup" className="text-blue-600 hover:text-blue-700 font-medium">
              Sign up here
            </Link>
          </p>
        </div>
      </div>

      {/* Info Box */}
      <div className="card bg-blue-50 border border-blue-200">
        <h3 className="font-semibold text-blue-900 mb-2">Demo Credentials</h3>
        <p className="text-sm text-blue-800">
          Use your registered email and password to login. Create a new account if you don't have one yet.
        </p>
      </div>
    </div>
  )
}
