/**
 * ConversationsList Component
 *
 * Displays list of user's conversations
 * Allows selecting and deleting conversations
 *
 * @specs/phase-3-overview.md - Conversation Management
 */

'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { chatClient } from '@/lib/chat-client'

interface Conversation {
  id: number
  message_count: number
  created_at: string
  updated_at: string
  preview: string
}

interface ConversationsListProps {
  onSelectConversation?: (id: number) => void
  onDeleteConversation?: (id: number) => void
}

export default function ConversationsList({
  onSelectConversation,
  onDeleteConversation
}: ConversationsListProps) {
  const { user, token } = useAuth()
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (user && token) {
      loadConversations()
    }
  }, [user, token])

  const loadConversations = async () => {
    if (!user || !token) return

    setIsLoading(true)
    setError(null)

    try {
      const data = await chatClient.listConversations(user.id, token)
      setConversations(data.conversations || [])
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load conversations'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async (conversationId: number, e: React.MouseEvent) => {
    e.stopPropagation()

    if (!user || !token) return

    if (!window.confirm('Are you sure you want to delete this conversation?')) {
      return
    }

    try {
      await chatClient.deleteConversation(user.id, conversationId, token)
      setConversations(conversations.filter(c => c.id !== conversationId))
      onDeleteConversation?.(conversationId)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to delete conversation'
      setError(message)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    if (date.toDateString() === today.toDateString()) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday'
    } else {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' })
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-4">
        <div className="text-gray-500">Loading conversations...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-700 text-sm">{error}</p>
        <button
          onClick={loadConversations}
          className="mt-2 text-sm text-red-600 hover:text-red-700 font-medium"
        >
          Retry
        </button>
      </div>
    )
  }

  if (conversations.length === 0) {
    return (
      <div className="flex items-center justify-center p-4 text-center">
        <div className="text-gray-500">
          <p className="text-sm">No conversations yet</p>
          <p className="text-xs text-gray-400 mt-1">Start a new chat to create one</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {conversations.map(conversation => (
        <div
          key={conversation.id}
          onClick={() => onSelectConversation?.(conversation.id)}
          className="p-3 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition group"
        >
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                Conversation #{conversation.id}
              </p>
              <p className="text-xs text-gray-600 truncate mt-1">
                {conversation.preview}
              </p>
              <p className="text-xs text-gray-400 mt-1">
                {conversation.message_count} messages • {formatDate(conversation.updated_at)}
              </p>
            </div>

            <button
              onClick={(e) => handleDelete(conversation.id, e)}
              className="opacity-0 group-hover:opacity-100 px-2 py-1 text-xs font-medium text-red-600 hover:bg-red-50 rounded transition"
              title="Delete conversation"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
