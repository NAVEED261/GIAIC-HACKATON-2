'use client'

import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'

export default function DashboardPage() {
  const { user } = useAuth()

  return (
    <div className="space-y-4 sm:space-y-6 md:space-y-8">
      {/* Welcome Section */}
      <div className="card bg-gradient-to-r from-blue-50 to-indigo-50">
        <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-2">Welcome, {user?.name}! 👋</h1>
        <p className="text-sm sm:text-base text-gray-600">
          You're all set to manage your tasks. Let's get started!
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
        <div className="card">
          <div className="text-blue-600 text-2xl sm:text-3xl mb-2">📊</div>
          <h3 className="font-semibold text-gray-800 text-sm sm:text-base">Total Tasks</h3>
          <p className="text-xl sm:text-2xl font-bold text-blue-600 mt-2">0</p>
        </div>

        <div className="card">
          <div className="text-green-600 text-2xl sm:text-3xl mb-2">✅</div>
          <h3 className="font-semibold text-gray-800 text-sm sm:text-base">Completed</h3>
          <p className="text-xl sm:text-2xl font-bold text-green-600 mt-2">0</p>
        </div>

        <div className="card">
          <div className="text-orange-600 text-2xl sm:text-3xl mb-2">⏳</div>
          <h3 className="font-semibold text-gray-800 text-sm sm:text-base">Pending</h3>
          <p className="text-xl sm:text-2xl font-bold text-orange-600 mt-2">0</p>
        </div>
      </div>

      {/* Actions */}
      <div className="card">
        <h2 className="text-xl sm:text-2xl font-bold mb-3 sm:mb-4">Get Started</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
          <Link
            href="/dashboard/tasks/create"
            className="block p-3 sm:p-4 border-2 border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
          >
            <div className="text-xl sm:text-2xl mb-2">➕</div>
            <h3 className="font-semibold text-blue-600 text-sm sm:text-base">Create New Task</h3>
            <p className="text-gray-600 text-xs sm:text-sm">Start by creating your first task</p>
          </Link>

          <Link
            href="/dashboard/tasks"
            className="block p-3 sm:p-4 border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div className="text-xl sm:text-2xl mb-2">📝</div>
            <h3 className="font-semibold text-gray-700 text-sm sm:text-base">View All Tasks</h3>
            <p className="text-gray-600 text-xs sm:text-sm">See all your tasks in one place</p>
          </Link>
        </div>
      </div>

      {/* Info Box */}
      <div className="card bg-blue-50 border-l-4 border-blue-600">
        <h3 className="font-semibold text-blue-900 mb-2 text-sm sm:text-base">💡 Tip</h3>
        <p className="text-blue-800 text-xs sm:text-sm">
          Create tasks to organize your work. Mark them complete when done, and track your
          progress all in one dashboard. Start by clicking "Create New Task" above!
        </p>
      </div>
    </div>
  )
}
