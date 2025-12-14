export type TaskStatus = 'pending' | 'in_progress' | 'completed'
export type TaskPriority = 'low' | 'medium' | 'high'

export interface Task {
  id: number
  user_id: string
  title: string
  description?: string | null
  status: TaskStatus
  priority: TaskPriority
  due_date?: string | null
  created_at: string
  updated_at: string
  completed_at?: string | null
}

export interface CreateTaskRequest {
  title: string
  description?: string
  priority: TaskPriority
  due_date?: string
}

export interface UpdateTaskRequest {
  title?: string
  description?: string
  priority?: TaskPriority
  due_date?: string
  status?: TaskStatus
}

export interface TaskListResponse {
  items: Task[]
  total: number
  skip: number
  limit: number
}

export interface TaskResponse {
  id: number
  user_id: string
  title: string
  description?: string | null
  status: TaskStatus
  priority: TaskPriority
  due_date?: string | null
  created_at: string
  updated_at: string
  completed_at?: string | null
}

export interface CompleteTaskResponse {
  id: number
  status: 'completed'
  completed_at: string
  message: string
}
