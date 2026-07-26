import { apiClient } from './apiClient'

export interface User {
  id: number
  username: string
  email: string
  name: string
  surname: string
  role_id: number
  is_active: boolean
  email_verified: boolean
  last_login: string | null
  created_at: string
  updated_at: string
}

export interface UserDetails extends User {
  role_name: string
}

export interface UserListResponse {
  items: User[]
  page: number
  size: number
  total: number
  pages: number
}

export interface UserCreateValues {
  username: string
  email: string
  name: string
  surname: string
  password: string
  is_active: boolean
  email_verified: boolean
  role_id: number
}

export interface UserUpdateValues {
  username: string
  email: string
  name: string
  surname: string
  role_id: number
  is_active: boolean
  email_verified: boolean
}

export function listUsers(page = 1, size = 10): Promise<UserListResponse> {
  return apiClient.get(`/admin/user/?page=${page}&size=${size}`)
}

export function getUser(id: number): Promise<UserDetails> {
  return apiClient.get(`/admin/user/${id}`)
}

export function createUser(payload: UserCreateValues): Promise<void> {
  return apiClient.post('/admin/user/', payload)
}

export function updateUser(id: number, payload: UserUpdateValues): Promise<void> {
  return apiClient.put(`/admin/user/${id}`, payload)
}

export function deleteUser(id: number): Promise<void> {
  return apiClient.delete(`/admin/user/${id}`)
}
