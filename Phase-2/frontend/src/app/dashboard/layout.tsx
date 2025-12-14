'use client'

import { useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { user, getCurrentUser, logout, isLoading } = useAuth()

  // Fetch current user on mount
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null
    if (!token) {
      router.push('/auth/login')
      return
    }

    // Fetch user info if not already loaded
    if (!user && typeof window !== 'undefined') {
      getCurrentUser().catch(() => {
        router.push('/auth/login')
      })
    }
  }, [user, router, getCurrentUser])

  const handleLogout = async () => {
    try {
      await logout()
      router.push('/')
    } catch (err) {
      // User is logged out even if endpoint fails
      router.push('/')
    }
  }

  if (!user && !isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">Redirecting to login...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-md">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold text-blue-600">
            Task Manager
          </Link>

          <div className="flex items-center space-x-4">
            {user && (
              <>
                <span className="text-sm text-gray-600">
                  Welcome, <span className="font-semibold">{user.name}</span>
                </span>
                <button
                  onClick={handleLogout}
                  disabled={isLoading}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-red-400 font-medium"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Sidebar */}
      <div className="flex">
        <aside className="w-48 bg-white shadow-md min-h-screen p-4">
          <nav className="space-y-2">
            <Link
              href="/dashboard"
              className="block px-4 py-2 rounded-lg hover:bg-blue-50 text-blue-600 font-medium"
            >
              📊 Dashboard
            </Link>
            <Link
              href="/dashboard/tasks/create"
              className="block px-4 py-2 rounded-lg hover:bg-blue-50 text-gray-700 hover:text-blue-600"
            >
              ➕ Create Task
            </Link>
            <Link
              href="/dashboard/tasks"
              className="block px-4 py-2 rounded-lg hover:bg-blue-50 text-gray-700 hover:text-blue-600"
            >
              📝 My Tasks
            </Link>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          {children}
        </main>
      </div>

      {/* Footer */}
      <footer className="bg-dark text-white py-8 mt-12">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p>&copy; 2025 Hackathon-2 Task Manager. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
