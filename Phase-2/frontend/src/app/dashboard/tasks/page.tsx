'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import TaskCard from '@/components/TaskCard'
import { useTasks } from '@/hooks/useTasks'
import { TaskStatus } from '@/types/task'

export default function TasksPage() {
  const { tasks, getTasks, deleteTask, completeTask, isLoading, error, clearError } =
    useTasks()
  const [selectedStatus, setSelectedStatus] = useState<TaskStatus | 'all'>('all')
  const [currentPage, setCurrentPage] = useState(0)
  const itemsPerPage = 10

  // Fetch tasks on mount and when filters change
  useEffect(() => {
    const status = selectedStatus === 'all' ? undefined : selectedStatus
    getTasks(currentPage * itemsPerPage, itemsPerPage, status)
  }, [selectedStatus, currentPage, getTasks])

  const handleDelete = async (id: number) => {
    try {
      await deleteTask(id)
      // Refresh the task list
      const status = selectedStatus === 'all' ? undefined : selectedStatus
      getTasks(currentPage * itemsPerPage, itemsPerPage, status)
    } catch (err) {
      // Error is handled by useTasks hook
    }
  }

  const handleComplete = async (id: number) => {
    try {
      await completeTask(id)
      // Refresh the task list
      const status = selectedStatus === 'all' ? undefined : selectedStatus
      getTasks(currentPage * itemsPerPage, itemsPerPage, status)
    } catch (err) {
      // Error is handled by useTasks hook
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">My Tasks</h1>
          <p className="text-gray-600 mt-1">View and manage all your tasks</p>
        </div>
        <Link
          href="/dashboard/tasks/create"
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
        >
          ➕ New Task
        </Link>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="alert alert-error">
          <div className="flex justify-between items-start">
            <span>{error}</span>
            <button
              type="button"
              onClick={clearError}
              className="text-xl font-bold cursor-pointer"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Status Filter */}
      <div className="card">
        <h3 className="font-semibold mb-3">Filter by Status</h3>
        <div className="flex gap-2 flex-wrap">
          {(['all', 'pending', 'in_progress', 'completed'] as const).map((status) => (
            <button
              key={status}
              onClick={() => {
                setSelectedStatus(status)
                setCurrentPage(0)
              }}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedStatus === status
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {status === 'all'
                ? '📋 All Tasks'
                : status === 'pending'
                  ? '⏳ Pending'
                  : status === 'in_progress'
                    ? '⚡ In Progress'
                    : '✅ Completed'}
            </button>
          ))}
        </div>
      </div>

      {/* Tasks Grid */}
      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="text-center">
            <div className="spinner mb-4" style={{ height: '40px', width: '40px' }}></div>
            <p className="text-gray-600">Loading tasks...</p>
          </div>
        </div>
      ) : tasks.length === 0 ? (
        <div className="card bg-gray-50 text-center py-12">
          <div className="text-4xl mb-4">📭</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No tasks found</h3>
          <p className="text-gray-600 mb-6">
            {selectedStatus === 'all'
              ? "You don't have any tasks yet. Create one to get started!"
              : `No ${selectedStatus} tasks found.`}
          </p>
          <Link
            href="/dashboard/tasks/create"
            className="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
          >
            Create First Task
          </Link>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-4">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onDelete={handleDelete}
                onComplete={handleComplete}
                isLoading={isLoading}
              />
            ))}
          </div>

          {/* Pagination */}
          {Math.ceil(tasks.length / itemsPerPage) > 1 && (
            <div className="flex justify-center gap-2">
              <button
                onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
                disabled={currentPage === 0}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                ← Previous
              </button>
              <span className="px-4 py-2 text-gray-600">
                Page {currentPage + 1}
              </span>
              <button
                onClick={() => setCurrentPage(currentPage + 1)}
                disabled={tasks.length < itemsPerPage}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
