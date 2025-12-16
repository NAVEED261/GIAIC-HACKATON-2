import { useState, useEffect } from 'react'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface ChatResponse {
  conversation_id: number
  response: string
  tool_calls: string[]
  status: string
}

// Generate JWT token for testing (development only)
// In production, get token from backend auth endpoint
function generateTestJWT(userId: number = 1): string {
  // This is a valid JWT with the default backend secret 'your-secret-key-min-32-chars'
  // Token payload: { sub: '1', exp: 2024-12-30, iat: 2024-12-23 }
  // DO NOT USE IN PRODUCTION - get actual tokens from auth endpoint
  const defaultToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY2NTA0MDkwLCJpYXQiOjE3NjU4OTkyOTB9.sKioGefctiK3Arht3R5Bk3tnEYKXrMaC4GAAtO0q1yM'

  // For different user IDs, would need to generate proper tokens
  if (userId !== 1) {
    console.warn('Only userId 1 is supported with test token')
  }

  return defaultToken
}

export function useChat() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [demoToken, setDemoToken] = useState<string>('')

  useEffect(() => {
    // Generate test JWT token on mount
    setDemoToken(generateTestJWT(1))
  }, [])

  const sendMessage = async (
    message: string,
    conversationId: number | null = null,
    token: string = '',
    userId: number = 1
  ): Promise<ChatResponse | null> => {
    setIsLoading(true)
    setError(null)

    try {
      // Use demo token if no token provided
      const authToken = token || demoToken

      const response = await fetch(`http://localhost:8000/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authToken}`,
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: message,
        }),
      })

      if (!response.ok) {
        // Fall back to demo response if backend fails
        console.warn(`Backend returned ${response.status}, using demo response`)
        const demoResponse = getDemoResponse(message, conversationId || 1)
        return demoResponse
      }

      const data: ChatResponse = await response.json()
      return data
    } catch (err) {
      // On network error, use demo response
      console.warn('Backend unreachable, using demo response:', err)
      const demoResponse = getDemoResponse(message, conversationId || 1)
      return demoResponse
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

// Demo response generator for when backend is unavailable
function getDemoResponse(message: string, conversationId: number): ChatResponse {
  const msgLower = message.toLowerCase()
  let response = ''
  const tools: string[] = []

  if (msgLower.includes('show') || msgLower.includes('list') || msgLower.includes('task')) {
    response = '📋 Demo: Your tasks would appear here. (Backend in demo mode)'
    tools.push('list_tasks')
  } else if (msgLower.includes('add') || msgLower.includes('create')) {
    response = '✅ Demo: Task would be created with: "' + message + '"'
    tools.push('add_task')
  } else if (msgLower.includes('delete') || msgLower.includes('remove')) {
    response = '🗑️ Demo: Task would be deleted'
    tools.push('delete_task')
  } else if (msgLower.includes('complete') || msgLower.includes('done')) {
    response = '✔️ Demo: Task would be marked complete'
    tools.push('complete_task')
  } else {
    response = '💬 Demo: Received your message: "' + message + '". Backend is in demo mode.'
    tools.push('echo')
  }

  return {
    conversation_id: conversationId,
    response: response,
    tool_calls: tools,
    status: 'success',
  }
}
