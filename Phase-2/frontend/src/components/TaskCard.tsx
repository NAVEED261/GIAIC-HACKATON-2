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
      <div className="flex flex-col sm:flex-row justify-between items-start gap-2 mb-2 sm:mb-3">
        <div className="flex-1 min-w-0">
          <h3 className="text-base sm:text-lg font-semibold text-gray-800 break-words">{task.title}</h3>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">Created: {createdDate}</p>
        </div>
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-gray-600 text-xs sm:text-sm mb-2 sm:mb-3 line-clamp-2">{task.description}</p>
      )}

      {/* Status and Priority */}
      <div className="flex flex-wrap gap-1 sm:gap-2 mb-3 sm:mb-4">
        <span
          className={`inline-block px-2 sm:px-3 py-1 rounded-full text-xs font-medium border ${
            statusColors[task.status]
          }`}
        >
          {statusLabels[task.status]}
        </span>
        <span className="inline-block px-2 sm:px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium border border-gray-300">
          {priorityIcons[task.priority]} {priorityLabels[task.priority]}
        </span>

        {dueDate && (
          <span className="inline-block px-2 sm:px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-xs font-medium border border-orange-300 whitespace-nowrap">
            📅 {dueDate}
          </span>
        )}
      </div>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-2">
        <Link
          href={`/dashboard/tasks/${task.id}/edit`}
          className="flex-1 px-2 sm:px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-xs sm:text-sm font-medium text-center transition-colors"
        >
          Edit
        </Link>

        {task.status !== 'completed' && onComplete && (
          <button
            onClick={() => onComplete(task.id)}
            disabled={isLoading}
            className="flex-1 px-2 sm:px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-green-400 text-xs sm:text-sm font-medium transition-colors"
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
            className="flex-1 px-2 sm:px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-red-400 text-xs sm:text-sm font-medium transition-colors"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  )
}
