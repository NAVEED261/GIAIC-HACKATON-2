'use client'

import { useState, useCallback } from 'react'
import { apiClient } from '@/lib/api-client'
import {
  Task,
  TaskListResponse,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskStatus,
} from '@/types/task'

interface UseTasksReturn {
  tasks: Task[]
  isLoading: boolean
  error: string | null
  total: number
  getTasks: (skip?: number, limit?: number, status?: TaskStatus) => Promise<void>
  getTask: (id: number) => Promise<Task>
  createTask: (data: CreateTaskRequest) => Promise<Task>
  updateTask: (id: number, data: UpdateTaskRequest) => Promise<Task>
  deleteTask: (id: number) => Promise<void>
  completeTask: (id: number) => Promise<Task>
  clearError: () => void
}

export function useTasks(): UseTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  const getTasks = useCallback(
    async (skip: number = 0, limit: number = 10, status?: TaskStatus) => {
      setIsLoading(true)
      setError(null)

      try {
        const params = new URLSearchParams()
        params.append('skip', skip.toString())
        params.append('limit', limit.toString())
        if (status) {
          params.append('status', status)
        }

        const response = await apiClient
          .getClient()
          .get<TaskListResponse>(`/api/tasks?${params.toString()}`)

        setTasks(response.data.items)
        setTotal(response.data.total)
        setIsLoading(false)
      } catch (err: any) {
        const errorMsg =
          err.response?.data?.detail || 'Failed to fetch tasks'
        setError(errorMsg)
        setIsLoading(false)
        throw err
      }
    },
    []
  )

  const getTask = useCallback(async (id: number): Promise<Task> => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await apiClient
        .getClient()
        .get<Task>(`/api/tasks/${id}`)
      setIsLoading(false)
      return response.data
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to fetch task'
      setError(errorMsg)
      setIsLoading(false)
      throw err
    }
  }, [])

  const createTask = useCallback(async (data: CreateTaskRequest): Promise<Task> => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await apiClient
        .getClient()
        .post<Task>('/api/tasks', data)
      setIsLoading(false)
      return response.data
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to create task'
      setError(errorMsg)
      setIsLoading(false)
      throw err
    }
  }, [])

  const updateTask = useCallback(
    async (id: number, data: UpdateTaskRequest): Promise<Task> => {
      setIsLoading(true)
      setError(null)

      try {
        const response = await apiClient
          .getClient()
          .put<Task>(`/api/tasks/${id}`, data)
        setIsLoading(false)
        return response.data
      } catch (err: any) {
        const errorMsg = err.response?.data?.detail || 'Failed to update task'
        setError(errorMsg)
        setIsLoading(false)
        throw err
      }
    },
    []
  )

  const deleteTask = useCallback(async (id: number) => {
    setIsLoading(true)
    setError(null)

    try {
      await apiClient.getClient().delete(`/api/tasks/${id}`)
      setIsLoading(false)
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to delete task'
      setError(errorMsg)
      setIsLoading(false)
      throw err
    }
  }, [])

  const completeTask = useCallback(async (id: number): Promise<Task> => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await apiClient
        .getClient()
        .patch<Task>(`/api/tasks/${id}/complete`)
      setIsLoading(false)
      return response.data
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to complete task'
      setError(errorMsg)
      setIsLoading(false)
      throw err
    }
  }, [])

  return {
    tasks,
    isLoading,
    error,
    total,
    getTasks,
    getTask,
    createTask,
    updateTask,
    deleteTask,
    completeTask,
    clearError,
  }
}
