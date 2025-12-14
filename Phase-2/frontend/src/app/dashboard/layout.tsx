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
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Navigation */}
      <nav className="bg-white shadow-md sticky top-0 z-40">
        <div className="max-w-full px-3 sm:px-6 py-3 sm:py-4">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <Link href="/dashboard" className="text-xl sm:text-2xl font-bold text-blue-600">
              Task Manager
            </Link>

            {user && (
              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4 w-full sm:w-auto">
                <span className="text-xs sm:text-sm text-gray-600 break-words">
                  Welcome, <span className="font-semibold">{user.name}</span>
                </span>
                <button
                  onClick={handleLogout}
                  disabled={isLoading}
                  className="w-full sm:w-auto px-3 sm:px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-red-400 font-medium text-sm"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-40 sm:w-48 bg-white shadow-md min-h-full overflow-y-auto hidden sm:block">
          <nav className="space-y-1 p-3 sm:p-4">
            <Link
              href="/dashboard"
              className="block px-3 sm:px-4 py-2 rounded-lg hover:bg-blue-50 text-blue-600 font-medium text-sm sm:text-base"
            >
              📊 Dashboard
            </Link>
            <Link
              href="/dashboard/tasks/create"
              className="block px-3 sm:px-4 py-2 rounded-lg hover:bg-blue-50 text-gray-700 hover:text-blue-600 text-sm sm:text-base"
            >
              ➕ Create Task
            </Link>
            <Link
              href="/dashboard/tasks"
              className="block px-3 sm:px-4 py-2 rounded-lg hover:bg-blue-50 text-gray-700 hover:text-blue-600 text-sm sm:text-base"
            >
              📝 My Tasks
            </Link>
          </nav>
        </aside>

        {/* Mobile Navigation */}
        <div className="sm:hidden w-full border-b border-gray-200 bg-white">
          <nav className="flex gap-1 p-2 overflow-x-auto">
            <Link
              href="/dashboard"
              className="px-3 py-2 rounded-lg hover:bg-blue-50 text-blue-600 font-medium text-xs whitespace-nowrap flex-shrink-0"
            >
              📊 Dashboard
            </Link>
            <Link
              href="/dashboard/tasks/create"
              className="px-3 py-2 rounded-lg hover:bg-blue-50 text-gray-700 hover:text-blue-600 text-xs whitespace-nowrap flex-shrink-0"
            >
              ➕ Create
            </Link>
            <Link
              href="/dashboard/tasks"
              className="px-3 py-2 rounded-lg hover:bg-blue-50 text-gray-700 hover:text-blue-600 text-xs whitespace-nowrap flex-shrink-0"
            >
              📝 Tasks
            </Link>
          </nav>
        </div>

        {/* Main Content */}
        <main className="flex-1 p-3 sm:p-6 md:p-8 overflow-y-auto">
          {children}
        </main>
      </div>

      {/* Footer */}
      <footer className="bg-dark text-white py-4 sm:py-6 md:py-8 mt-8 sm:mt-12">
        <div className="max-w-full px-4 sm:px-6 text-center">
          <p className="text-xs sm:text-sm">&copy; 2025 Hackathon-2 Task Manager. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
