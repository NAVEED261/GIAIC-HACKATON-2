import { useState } from 'react'
import { useAuth } from './useAuth'

interface ChatResponse {
  conversation_id: number
  response: string
  tool_calls: string[]
  status: string
}

export function useChat() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { token, isAuthenticated } = useAuth()

  const sendMessage = async (
    message: string,
    conversationId: number | null = null
  ): Promise<ChatResponse | null> => {
    setIsLoading(true)
    setError(null)

    // Validate auth
    if (!token || !isAuthenticated) {
      setError('Not authenticated. Please sign in first.')
      setIsLoading(false)
      return null
    }

    try {
      // Smart API URL: works for local, docker, and minikube
      const getApiUrl = () => {
        if (typeof window === 'undefined') return 'http://localhost:8000'
        const host = window.location.hostname
        if (host === 'phase5.local') return 'http://phase5.local'
        return 'http://localhost:8000'
      }
      const apiUrl = getApiUrl()

      const response = await fetch(`${apiUrl}/api/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: message,
          conversation_id: conversationId,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        const errorMessage = errorData.detail || `Server error: ${response.status}`
        setError(errorMessage)
        return null
      }

      const data: ChatResponse = await response.json()
      return data
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Network error'
      setError(`Failed to send message: ${errorMsg}`)
      return null
    } finally {
      setIsLoading(false)
    }
  }

  return {
    sendMessage,
    isLoading,
    error,
  }
}
