/**
 * Chat Page
 *
 * Main chat interface page with full-screen chat UI
 * Integrates Chat component for todo management via natural language
 *
 * @specs/phase-3-overview.md - Chat UI Specification
 */

'use client'

import Chat from '@/components/Chat'

export default function ChatPage() {
  return (
    <div className="h-screen flex flex-col">
      <Chat />
    </div>
  )
}

