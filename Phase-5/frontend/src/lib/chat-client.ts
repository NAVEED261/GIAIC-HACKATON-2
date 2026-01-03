/**
 * Chat API Client - Phase-5
 *
 * Handles communication with OpenAI-powered chat endpoint
 * Uses JWT auth header (not userId in URL)
 */

// Smart API URL: works for local, docker, and minikube
const getApiUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:8000'
  const host = window.location.hostname
  if (host === 'phase5.local') return 'http://phase5.local'
  return 'http://localhost:8000'
}
const API_URL = getApiUrl()

export interface ChatRequest {
  message: string
}

export interface ChatResponse {
  response: string
  tool_calls: string[]
  status: string
}

class ChatClient {
  private getAuthHeader(): { Authorization: string } | {} {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
    if (!token) return {}
    return { Authorization: `Bearer ${token}` }
  }

  /**
   * Send message to chat endpoint
   * @param message User message
   * @returns Chat response with AI reply and any tool calls executed
   */
  async sendMessage(message: string): Promise<ChatResponse> {
    const response = await fetch(`${API_URL}/api/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeader()
      },
      body: JSON.stringify({ message })
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || `Chat request failed: ${response.status}`)
    }

    return response.json()
  }

  /**
   * List all conversations for user
   * @param userId User ID (unused - JWT auth)
   * @param token Auth token
   */
  async listConversations(userId: number, token: string): Promise<any> {
    const response = await fetch(`${API_URL}/api/conversations/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      throw new Error(`Failed to load conversations: ${response.status}`)
    }

    return response.json()
  }

  /**
   * Delete a conversation
   * @param userId User ID (unused - JWT auth)
   * @param conversationId Conversation to delete
   * @param token Auth token
   */
  async deleteConversation(userId: number, conversationId: number, token: string): Promise<void> {
    const response = await fetch(`${API_URL}/api/conversations/${conversationId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      throw new Error(`Failed to delete conversation: ${response.status}`)
    }
  }
}

export const chatClient = new ChatClient()
