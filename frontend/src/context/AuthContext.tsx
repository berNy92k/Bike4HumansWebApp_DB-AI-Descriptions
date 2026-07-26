import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { getCookieValue } from '../api/apiClient'
import { login as loginRequest, logout as logoutRequest } from '../api/auth'

export interface AuthUser {
  userId: number
  roleId: number
  username: string
}

interface AuthContextValue {
  user: AuthUser | null
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

// The access_token cookie is httponly=False (see app/services/auth/auth_service.py), so its
// JWT payload can be decoded client-side to restore the logged-in user after a page refresh
// without an extra round-trip to the backend.
function decodeJwtPayload(token: string): Record<string, unknown> | null {
  try {
    const payload = token.split('.')[1]
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/')
    const json = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + c.charCodeAt(0).toString(16).padStart(2, '0'))
        .join(''),
    )
    return JSON.parse(json) as Record<string, unknown>
  } catch {
    return null
  }
}

function userFromToken(token: string): AuthUser | null {
  const payload = decodeJwtPayload(token)
  if (!payload) return null

  const userId = Number(payload.id)
  const roleId = Number(payload.role_id)
  const username = typeof payload.sub === 'string' ? payload.sub : ''

  if (!userId || !roleId || !username) return null

  return { userId, roleId, username }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = getCookieValue('access_token')
    setUser(token ? userFromToken(token) : null)
    setIsLoading(false)
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isLoading,
      login: async (username, password) => {
        const response = await loginRequest(username, password)
        setUser({ userId: response.user_id, roleId: response.role_id, username: response.username })
      },
      logout: async () => {
        await logoutRequest()
        setUser(null)
      },
    }),
    [user, isLoading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
