/**
 * useChat Hook
 *
 * Custom React hook for chat functionality
 * Handles sending messages and managing API communication
 *
 * @specs/phase-3-overview.md - Chat Hook Specification
 */

'use client'

import { useCallback } from 'react'
import { useAuth } from './useAuth'
import { chatClient } from '@/lib/chat-client'

export interface ChatResponse {
  conversation_id: number
  response: string
  tool_calls: string[]
  status: string
}

export function useChat() {
  const { user, token } = useAuth()

  const sendMessage = useCallback(
    async (message: string, conversationId: number | null): Promise<ChatResponse | null> => {
      if (!user || !token) {
        throw new Error('User not authenticated')
      }

      try {
        const response = await chatClient.sendMessage(
          user.id,
          {
            conversation_id: conversationId,
            message
          },
          token
        )

        return response
      } catch (error) {
        console.error('Error sending message:', error)
        throw error
      }
    },
    [user, token]
  )

  return {
    sendMessage
  }
}
