'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import TaskForm from '@/components/TaskForm'
import { useTasks } from '@/hooks/useTasks'
import { UpdateTaskRequest, Task } from '@/types/task'

export default function EditTaskPage() {
  const router = useRouter()
  const params = useParams()
  const taskId = parseInt(params.id as string, 10)

  const { getTask, updateTask, isLoading: isSubmitting, error, clearError } = useTasks()
  const [task, setTask] = useState<Task | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [loadError, setLoadError] = useState<string | null>(null)

  // Fetch task on mount
  useEffect(() => {
    const fetchTask = async () => {
      try {
        const data = await getTask(taskId)
        setTask(data)
        setIsLoading(false)
      } catch (err: any) {
        setLoadError(err.response?.data?.detail || 'Failed to load task')
        setIsLoading(false)
      }
    }

    fetchTask()
  }, [taskId, getTask])

  const handleUpdateTask = async (data: UpdateTaskRequest) => {
    try {
      const updatedTask = await updateTask(taskId, data)
      // Redirect to task list on successful update
      router.push('/dashboard/tasks')
    } catch (err: any) {
      // Error is handled by useTasks hook
    }
  }

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <div className="text-center">
          <div className="spinner mb-4" style={{ height: '40px', width: '40px' }}></div>
          <p className="text-gray-600">Loading task...</p>
        </div>
      </div>
    )
  }

  if (loadError) {
    return (
      <div className="max-w-2xl">
        <div className="alert alert-error">
          <p>{loadError}</p>
        </div>
        <button
          onClick={() => router.back()}
          className="mt-4 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
        >
          Go Back
        </button>
      </div>
    )
  }

  if (!task) {
    return (
      <div className="max-w-2xl">
        <div className="alert alert-error">
          <p>Task not found</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Edit Task</h1>
        <p className="text-gray-600">Update task details</p>
      </div>

      <div className="card">
        <TaskForm
          onSubmit={handleUpdateTask}
          isLoading={isSubmitting}
          error={error}
          submitLabel="Update Task"
          onErrorDismiss={clearError}
          initialData={{
            title: task.title,
            description: task.description,
            priority: task.priority,
            due_date: task.due_date,
          }}
        />
      </div>

      {/* Task Status Info */}
      <div className="card bg-blue-50 border-l-4 border-blue-600 mt-6">
        <h3 className="font-semibold text-blue-900 mb-2">Current Status</h3>
        <div className="space-y-2 text-sm text-blue-800">
          <p>
            <span className="font-medium">Status:</span>{' '}
            {task.status === 'pending'
              ? '⏳ Pending'
              : task.status === 'in_progress'
                ? '⚡ In Progress'
                : '✅ Completed'}
          </p>
          <p>
            <span className="font-medium">Created:</span>{' '}
            {new Date(task.created_at).toLocaleString()}
          </p>
          {task.completed_at && (
            <p>
              <span className="font-medium">Completed:</span>{' '}
              {new Date(task.completed_at).toLocaleString()}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
