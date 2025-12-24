import { useState, useEffect } from 'react'

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [token, setToken] = useState<string | null>(null)
  const [userId, setUserId] = useState<number | null>(null)

  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    const storedUserId = localStorage.getItem('userId')

    if (storedToken && storedUserId) {
      setToken(storedToken)
      setUserId(parseInt(storedUserId))
      setIsAuthenticated(true)
    } else {
      const testToken = 'test-token-for-demo'
      const testUserId = 1

      localStorage.setItem('token', testToken)
      localStorage.setItem('userId', testUserId.toString())

      setToken(testToken)
      setUserId(testUserId)
      setIsAuthenticated(true)
    }
  }, [])

  return {
    isAuthenticated,
    token,
    userId,
  }
}
