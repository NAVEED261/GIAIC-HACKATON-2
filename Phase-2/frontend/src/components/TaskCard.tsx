'use client'

import Link from 'next/link'
import { Task, TaskStatus, TaskPriority } from '@/types/task'

interface TaskCardProps {
  task: Task
  onDelete?: (id: number) => void
  onComplete?: (id: number) => void
  isLoading?: boolean
}

const statusColors: Record<TaskStatus, string> = {
  pending: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  in_progress: 'bg-blue-100 text-blue-800 border-blue-300',
  completed: 'bg-green-100 text-green-800 border-green-300',
}

const statusLabels: Record<TaskStatus, string> = {
  pending: '⏳ Pending',
  in_progress: '⚡ In Progress',
  completed: '✅ Completed',
}

const priorityIcons: Record<TaskPriority, string> = {
  low: '🟢',
  medium: '🟡',
  high: '🔴',
}

const priorityLabels: Record<TaskPriority, string> = {
  low: 'Low',
  medium: 'Medium',
  high: 'High',
}

export default function TaskCard({
  task,
  onDelete,
  onComplete,
  isLoading = false,
}: TaskCardProps) {
  const createdDate = new Date(task.created_at).toLocaleDateString()
  const dueDate = task.due_date ? new Date(task.due_date).toLocaleDateString() : null

  return (
    <div className="card card-hover border-l-4 border-blue-500">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-800">{task.title}</h3>
          <p className="text-sm text-gray-500 mt-1">Created: {createdDate}</p>
        </div>
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">{task.description}</p>
      )}

      {/* Status and Priority */}
      <div className="flex flex-wrap gap-2 mb-4">
        <span
          className={`inline-block px-3 py-1 rounded-full text-xs font-medium border ${
            statusColors[task.status]
          }`}
        >
          {statusLabels[task.status]}
        </span>
        <span className="inline-block px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium border border-gray-300">
          {priorityIcons[task.priority]} {priorityLabels[task.priority]}
        </span>

        {dueDate && (
          <span className="inline-block px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-xs font-medium border border-orange-300">
            📅 Due: {dueDate}
          </span>
        )}
      </div>

      {/* Actions */}
      <div className="flex gap-2">
        <Link
          href={`/dashboard/tasks/${task.id}/edit`}
          className="flex-1 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium text-center transition-colors"
        >
          Edit
        </Link>

        {task.status !== 'completed' && onComplete && (
          <button
            onClick={() => onComplete(task.id)}
            disabled={isLoading}
            className="flex-1 px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-green-400 text-sm font-medium transition-colors"
          >
            ✅ Complete
          </button>
        )}

        {onDelete && (
          <button
            onClick={() => {
              if (confirm('Are you sure you want to delete this task?')) {
                onDelete(task.id)
              }
            }}
            disabled={isLoading}
            className="flex-1 px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-red-400 text-sm font-medium transition-colors"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  )
}
