'use client'

import { useState, useCallback } from 'react'
import { apiClient } from '@/lib/api-client'
import {
  User,
  SignupRequest,
  LoginRequest,
  LoginResponse,
  CurrentUserResponse,
  AuthError,
} from '@/types/auth'

interface UseAuthReturn {
  user: User | null
  isLoading: boolean
  error: AuthError | null
  signup: (data: SignupRequest) => Promise<void>
  login: (data: LoginRequest) => Promise<void>
  logout: () => Promise<void>
  getCurrentUser: () => Promise<void>
  clearError: () => void
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<AuthError | null>(null)

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  const signup = useCallback(async (data: SignupRequest) => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await apiClient.getClient().post('/api/auth/signup', data)
      // After signup, user needs to login
      setIsLoading(false)
    } catch (err: any) {
      const errorData: AuthError = {
        detail: err.response?.data?.detail || 'Signup failed',
        status_code: err.response?.status || 500,
      }
      setError(errorData)
      setIsLoading(false)
      throw err
    }
  }, [])

  const login = useCallback(async (data: LoginRequest) => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await apiClient.getClient().post<LoginResponse>(
        '/api/auth/login',
        data
      )
      const { access_token, refresh_token, user: userData } = response.data

      // Store tokens
      apiClient.setAccessToken(access_token)
      apiClient.setRefreshToken(refresh_token)

      setUser(userData)
      setIsLoading(false)
    } catch (err: any) {
      const errorData: AuthError = {
        detail: err.response?.data?.detail || 'Login failed',
        status_code: err.response?.status || 500,
      }
      setError(errorData)
      setIsLoading(false)
      throw err
    }
  }, [])

  const logout = useCallback(async () => {
    setIsLoading(true)
    setError(null)

    try {
      // Call logout endpoint
      await apiClient.getClient().post('/api/auth/logout')

      // Clear local state and tokens
      apiClient.clearTokens()
      setUser(null)
      setIsLoading(false)
    } catch (err: any) {
      // Clear tokens even if logout endpoint fails
      apiClient.clearTokens()
      setUser(null)
      setIsLoading(false)
      throw err
    }
  }, [])

  const getCurrentUser = useCallback(async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await apiClient
        .getClient()
        .get<CurrentUserResponse>('/api/auth/me')
      setUser(response.data as User)
      setIsLoading(false)
    } catch (err: any) {
      const errorData: AuthError = {
        detail: err.response?.data?.detail || 'Failed to fetch user',
        status_code: err.response?.status || 500,
      }
      setError(errorData)
      setIsLoading(false)
      throw err
    }
  }, [])

  return {
    user,
    isLoading,
    error,
    signup,
    login,
    logout,
    getCurrentUser,
    clearError,
  }
}
