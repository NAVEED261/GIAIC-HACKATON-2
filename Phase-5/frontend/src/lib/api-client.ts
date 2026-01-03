// Smart API URL: works for local, docker, and minikube
const getApiUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:8000'
  const host = window.location.hostname
  if (host === 'phase5.local') return 'http://phase5.local'
  return 'http://localhost:8000'
}
const API_BASE_URL = getApiUrl()

export async function chatWithAI(
  userId: number,
  message: string,
  token: string,
  conversationId?: number
) {
  const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      conversation_id: conversationId || null,
      message,
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to send message')
  }

  return response.json()
}

export async function getConversations(userId: number, token: string) {
  const response = await fetch(`${API_BASE_URL}/api/${userId}/conversations`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    throw new Error('Failed to fetch conversations')
  }

  return response.json()
}
