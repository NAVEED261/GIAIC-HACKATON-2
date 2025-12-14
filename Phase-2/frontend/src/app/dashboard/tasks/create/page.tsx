'use client'

import { useRouter } from 'next/navigation'
import TaskForm from '@/components/TaskForm'
import { useTasks } from '@/hooks/useTasks'
import { CreateTaskRequest } from '@/types/task'

export default function CreateTaskPage() {
  const router = useRouter()
  const { createTask, isLoading, error, clearError } = useTasks()

  const handleCreateTask = async (data: CreateTaskRequest) => {
    try {
      const newTask = await createTask(data)
      // Redirect to task list on successful creation
      router.push('/dashboard/tasks')
    } catch (err: any) {
      // Error is handled by useTasks hook
    }
  }

  return (
    <div className="max-w-2xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Create New Task</h1>
        <p className="text-gray-600">Add a new task to your task list</p>
      </div>

      <div className="card">
        <TaskForm
          onSubmit={handleCreateTask}
          isLoading={isLoading}
          error={error}
          submitLabel="Create Task"
          onErrorDismiss={clearError}
        />
      </div>

      {/* Info Box */}
      <div className="card bg-blue-50 border-l-4 border-blue-600 mt-6">
        <h3 className="font-semibold text-blue-900 mb-2">💡 Tips</h3>
        <ul className="text-blue-800 text-sm space-y-1">
          <li>• Be specific with your task title</li>
          <li>• Add a description for more details</li>
          <li>• Set appropriate priority level</li>
          <li>• Set a due date to stay on track</li>
        </ul>
      </div>
    </div>
  )
}
