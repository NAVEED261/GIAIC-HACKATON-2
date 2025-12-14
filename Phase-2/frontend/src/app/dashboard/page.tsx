'use client'

import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'

export default function DashboardPage() {
  const { user } = useAuth()

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="card bg-gradient-to-r from-blue-50 to-indigo-50">
        <h1 className="text-4xl font-bold mb-2">Welcome, {user?.name}! 👋</h1>
        <p className="text-gray-600">
          You're all set to manage your tasks. Let's get started!
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card">
          <div className="text-blue-600 text-3xl mb-2">📊</div>
          <h3 className="font-semibold text-gray-800">Total Tasks</h3>
          <p className="text-2xl font-bold text-blue-600 mt-2">0</p>
        </div>

        <div className="card">
          <div className="text-green-600 text-3xl mb-2">✅</div>
          <h3 className="font-semibold text-gray-800">Completed</h3>
          <p className="text-2xl font-bold text-green-600 mt-2">0</p>
        </div>

        <div className="card">
          <div className="text-orange-600 text-3xl mb-2">⏳</div>
          <h3 className="font-semibold text-gray-800">Pending</h3>
          <p className="text-2xl font-bold text-orange-600 mt-2">0</p>
        </div>
      </div>

      {/* Actions */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">Get Started</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            href="/dashboard/tasks/create"
            className="block p-4 border-2 border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
          >
            <div className="text-2xl mb-2">➕</div>
            <h3 className="font-semibold text-blue-600">Create New Task</h3>
            <p className="text-gray-600 text-sm">Start by creating your first task</p>
          </Link>

          <Link
            href="/dashboard/tasks"
            className="block p-4 border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div className="text-2xl mb-2">📝</div>
            <h3 className="font-semibold text-gray-700">View All Tasks</h3>
            <p className="text-gray-600 text-sm">See all your tasks in one place</p>
          </Link>
        </div>
      </div>

      {/* Info Box */}
      <div className="card bg-blue-50 border-l-4 border-blue-600">
        <h3 className="font-semibold text-blue-900 mb-2">💡 Tip</h3>
        <p className="text-blue-800 text-sm">
          Create tasks to organize your work. Mark them complete when done, and track your
          progress all in one dashboard. Start by clicking "Create New Task" above!
        </p>
      </div>
    </div>
  )
}
