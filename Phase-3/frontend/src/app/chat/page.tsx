/**
 * Chat Page
 *
 * Main chat interface page
 * Integrates Chat component with dashboard layout
 *
 * @specs/phase-3-overview.md - Chat UI Specification
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import Chat from '@/components/Chat'

export default function ChatPage() {
  const { user, isLoading } = useAuth()
  const router = useRouter()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (mounted && !isLoading && !user) {
      router.push('/auth/login')
    }
  }, [user, isLoading, mounted, router])

  if (!mounted || isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 shadow-sm p-4">
        <div className="mb-6">
          <h2 className="text-xl font-bold text-gray-900">Todo Assistant</h2>
          <p className="text-sm text-gray-500 mt-1">Chat-powered todo management</p>
        </div>

        <div className="space-y-3">
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm font-medium text-blue-900">Logged in as</p>
            <p className="text-sm text-blue-700 mt-1 truncate">{user.email}</p>
          </div>

          <button
            onClick={() => router.push('/dashboard')}
            className="w-full px-4 py-2 text-left text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition"
          >
            ← Back to Dashboard
          </button>
        </div>

        <div className="mt-6 p-3 bg-gray-50 rounded-lg">
          <p className="text-xs font-semibold text-gray-600 uppercase mb-3">Quick Commands</p>
          <ul className="text-xs space-y-2 text-gray-600">
            <li>• <span className="font-medium">Add task:</span> "Add task: Buy groceries"</li>
            <li>• <span className="font-medium">List tasks:</span> "Show my tasks"</li>
            <li>• <span className="font-medium">Complete:</span> "Mark task 1 complete"</li>
            <li>• <span className="font-medium">Delete:</span> "Delete task 1"</li>
            <li>• <span className="font-medium">Update:</span> "Update task 1 to ..."</li>
          </ul>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        <Chat />
      </div>
    </div>
  )
}
