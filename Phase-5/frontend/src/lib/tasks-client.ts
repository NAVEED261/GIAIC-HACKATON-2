/**
 * Tasks API Client
 *
 * Handles all task-related CRUD operations
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface TaskCreate {
  title: string
  description?: string
}

export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
}

export interface Task {
  id: number
  user_id: number
  title: string
  description?: string
  completed: boolean
  priority: string
  due_date?: string
  is_recurring: boolean
  recurrence_pattern?: string
  recurrence_interval: number
  is_overdue: boolean
  created_at: string
  updated_at: string
}

class TasksClient {
  private getAuthHeader(): { Authorization: string } | {} {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
    if (!token) return {}
    return { Authorization: `Bearer ${token}` }
  }

  async getTasks(): Promise<Task[]> {
    const response = await fetch(`${API_URL}/api/tasks/`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json', ...this.getAuthHeader() }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch tasks')
    }

    return await response.json()
  }

  async createTask(data: TaskCreate): Promise<Task> {
    const response = await fetch(`${API_URL}/api/tasks/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...this.getAuthHeader() },
      body: JSON.stringify(data)
    })

    if (!response.ok) {
      let errorDetail = 'Failed to create task'
      try {
        const error = await response.json()
        errorDetail = error.detail || errorDetail
      } catch {}
      throw new Error(errorDetail)
    }

    return await response.json()
  }

  async updateTask(taskId: number, data: TaskUpdate): Promise<Task> {
    const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', ...this.getAuthHeader() },
      body: JSON.stringify(data)
    })

    if (!response.ok) {
      let errorDetail = 'Failed to update task'
      try {
        const error = await response.json()
        errorDetail = error.detail || errorDetail
      } catch {}
      throw new Error(errorDetail)
    }

    return await response.json()
  }

  async deleteTask(taskId: number): Promise<void> {
    const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json', ...this.getAuthHeader() }
    })

    if (!response.ok && response.status !== 204) {
      throw new Error('Failed to delete task')
    }
  }

  async completeTask(taskId: number): Promise<Task> {
    return this.updateTask(taskId, { completed: true })
  }
}

export const tasksClient = new TasksClient()
