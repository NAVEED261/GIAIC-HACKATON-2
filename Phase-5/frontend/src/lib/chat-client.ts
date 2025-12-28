/**
 * Chat API Client - Phase-5
 *
 * Handles communication with OpenAI-powered chat endpoint
 * Uses JWT auth header (not userId in URL)
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

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
}

export const chatClient = new ChatClient()
