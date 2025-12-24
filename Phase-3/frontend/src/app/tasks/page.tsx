'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface Task {
  id: number
  description: string
  status: 'pending' | 'in-progress' | 'completed'
  createdDate: string
}

export default function TasksPage() {
  const [searchMode, setSearchMode] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Load tasks from backend on mount
  useEffect(() => {
    const loadTasks = async () => {
      try {
        setLoading(true)
        setError(null)

        const userId = 1 // Default user ID for demo
        const response = await fetch(`http://localhost:8000/api/${userId}/tasks`, {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY2NTA0MDkwLCJpYXQiOjE3NjU4OTkyOTB9.sKioGefctiK3Arht3R5Bk3tnEYKXrMaC4GAAtO0q1yM',
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok && response.status !== 404) {
          throw new Error(`API error: ${response.status}`)
        }

        const data = await response.json()

        // Transform API response to match Task interface
        const transformedTasks = (data.tasks || []).map((task: any) => ({
          id: task.id,
          description: task.title || task.description,
          status: task.status || 'pending',
          createdDate: task.created_at ? new Date(task.created_at).toLocaleDateString('en-GB') : new Date().toLocaleDateString('en-GB')
        }))

        setTasks(transformedTasks)
      } catch (err) {
        // If API fails, use demo data
        console.log('Using demo data (API unavailable)')
        setTasks([
          {
            id: 1,
            description: 'Another Task',
            status: 'pending',
            createdDate: '30/08/2022'
          },
          {
            id: 2,
            description: 'Another Other Task',
            status: 'pending',
            createdDate: '30/08/2022'
          },
          {
            id: 3,
            description: 'Complete Project Report',
            status: 'in-progress',
            createdDate: '29/08/2022'
          },
          {
            id: 4,
            description: 'Review Code Changes',
            status: 'completed',
            createdDate: '28/08/2022'
          }
        ])
      } finally {
        setLoading(false)
      }
    }

    loadTasks()
  }, [])

  const filteredTasks = tasks.filter(task =>
    task.description.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const handleDelete = async (id: number) => {
    try {
      // Optimistically remove from UI
      setTasks(tasks.filter(task => task.id !== id))

      // Call backend API
      const userId = 1
      await fetch(`http://localhost:8000/api/${userId}/tasks/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY2NTA0MDkwLCJpYXQiOjE3NjU4OTkyOTB9.sKioGefctiK3Arht3R5Bk3tnEYKXrMaC4GAAtO0q1yM'
        }
      })
    } catch (err) {
      console.log('Task deleted locally (backend unavailable)')
    }
  }

  const handleComplete = async (id: number) => {
    try {
      // Optimistically update UI
      setTasks(tasks.map(task =>
        task.id === id ? { ...task, status: 'completed' as const } : task
      ))

      // Call backend API
      const userId = 1
      await fetch(`http://localhost:8000/api/${userId}/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY2NTA0MDkwLCJpYXQiOjE3NjU4OTkyOTB9.sKioGefctiK3Arht3R5Bk3tnEYKXrMaC4GAAtO0q1yM',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: 'completed' })
      })
    } catch (err) {
      console.log('Task completed locally (backend unavailable)')
    }
  }

  const getStatusBgColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100'
      case 'in-progress':
        return 'bg-yellow-100'
      default:
        return 'bg-purple-100'
    }
  }

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-200 text-green-800'
      case 'in-progress':
        return 'bg-yellow-200 text-yellow-800'
      default:
        return 'bg-purple-200 text-purple-800'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 pt-24">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">TO DO LIST</h1>
          <Link href="/" className="text-purple-600 hover:text-purple-700 font-semibold">
            ← Back to Chat
          </Link>
        </div>

        {/* Search Mode Activated Banner */}
        {searchMode && (
          <div className="mb-6 bg-purple-200 border-l-4 border-purple-600 p-4 rounded">
            <div className="flex justify-between items-center gap-4">
              <div className="flex-1">
                <h3 className="font-semibold text-purple-900 mb-3">Search Mode Activated</h3>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Another"
                  className="w-full px-4 py-2 border-2 border-purple-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setSearchMode(false)}
                  className="px-4 py-2 bg-slate-600 text-white rounded font-semibold hover:bg-slate-700 transition"
                >
                  Save
                </button>
                <button
                  onClick={() => {
                    setSearchQuery('')
                    setSearchMode(false)
                  }}
                  className="px-4 py-2 bg-purple-600 text-white rounded font-semibold hover:bg-purple-700 transition"
                >
                  SearchOFF
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Table Container */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden border-2 border-slate-300">
          {/* Table Header */}
          <div className="bg-gradient-to-r from-lime-500 via-purple-600 to-purple-600">
            <div className="grid grid-cols-4 gap-4 p-4 text-white font-bold text-sm">
              <div className="flex items-center gap-2">
                <span>Task Description</span>
                <span className="text-lg">↕️</span>
              </div>
              <div className="flex items-center gap-2">
                <span>Status</span>
                <span className="text-lg">↕️</span>
              </div>
              <div className="flex items-center gap-2">
                <span>Created Date</span>
                <span className="text-lg">↕️</span>
              </div>
              <div className="text-center">Actions</div>
            </div>
          </div>

          {/* Table Body */}
          <div>
            {loading ? (
              <div className="p-8 text-center">
                <div className="flex justify-center mb-4">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
                </div>
                <p className="text-slate-500 text-lg">Loading tasks...</p>
              </div>
            ) : filteredTasks.length === 0 ? (
              <div className="p-8 text-center">
                <p className="text-slate-500 text-lg">No tasks found</p>
              </div>
            ) : (
              filteredTasks.map((task, index) => (
                <div
                  key={task.id}
                  className={`${
                    index % 2 === 0 ? 'bg-purple-100' : 'bg-purple-50'
                  } border-b border-purple-200 hover:bg-purple-150 transition`}
                >
                  <div className="grid grid-cols-4 gap-4 p-4 items-center text-sm">
                    {/* Task Description */}
                    <div className="flex items-center gap-2">
                      <span className="text-slate-700">{task.description}</span>
                      <button className="text-blue-500 hover:text-blue-700 font-bold text-lg">
                        ✏️
                      </button>
                    </div>

                    {/* Status */}
                    <div>
                      <span className={`px-3 py-1 rounded font-semibold text-xs ${getStatusBadgeColor(task.status)}`}>
                        {task.status}
                      </span>
                    </div>

                    {/* Created Date */}
                    <div className="text-slate-700">{task.createdDate}</div>

                    {/* Actions */}
                    <div className="flex justify-center gap-4 text-lg">
                      <button
                        onClick={() => handleComplete(task.id)}
                        className="text-orange-500 hover:text-orange-700 text-xl transition"
                        title="Mark as in-progress"
                      >
                        ⏱️
                      </button>
                      <button
                        onClick={() => handleComplete(task.id)}
                        className="text-green-500 hover:text-green-700 text-xl transition"
                        title="Complete task"
                      >
                        ✅
                      </button>
                      <button
                        onClick={() => handleDelete(task.id)}
                        className="text-red-500 hover:text-red-700 text-xl transition"
                        title="Delete task"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-8 grid grid-cols-3 gap-4">
          <div className="bg-white p-6 rounded-lg shadow border-l-4 border-purple-600">
            <p className="text-slate-600 text-sm font-semibold mb-1">Total Tasks</p>
            <p className="text-3xl font-bold text-slate-900">{tasks.length}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow border-l-4 border-yellow-500">
            <p className="text-slate-600 text-sm font-semibold mb-1">In Progress</p>
            <p className="text-3xl font-bold text-yellow-600">
              {tasks.filter(t => t.status === 'in-progress').length}
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
            <p className="text-slate-600 text-sm font-semibold mb-1">Completed</p>
            <p className="text-3xl font-bold text-green-600">
              {tasks.filter(t => t.status === 'completed').length}
            </p>
          </div>
        </div>

        {/* Add Task Button */}
        <div className="mt-8 text-center pb-8">
          <Link
            href="/chat"
            className="px-8 py-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition transform hover:scale-105"
          >
            Add Task via Chat
          </Link>
        </div>
      </div>
    </div>
  )
}
