import { apiClient } from './apiClient'

export interface TokenResponse {
  access_token: string
  token_type: string
  user_id: number
  role_id: number
  username: string
}

// POST /auth/token expects OAuth2 form-urlencoded data, not JSON, so it bypasses apiClient.
export async function login(username: string, password: string): Promise<TokenResponse> {
  const body = new URLSearchParams()
  body.set('username', username)
  body.set('password', password)

  const response = await fetch('/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  })

  if (!response.ok) {
    throw new Error('Nieprawidłowy login lub hasło.')
  }

  return response.json() as Promise<TokenResponse>
}

export interface RegisterPayload {
  username: string
  email: string
  name: string
  surname: string
  password: string
}

export async function register(payload: RegisterPayload): Promise<void> {
  await apiClient.post('/auth/user', payload)
}

export async function logout(): Promise<void> {
  await fetch('/auth/logout')
}
