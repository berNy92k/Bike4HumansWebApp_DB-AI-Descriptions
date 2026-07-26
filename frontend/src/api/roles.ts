import { apiClient } from './apiClient'

export interface Role {
  id: number
  name: string
  description: string | null
  permission_codes: string[]
  created_at: string
  updated_at: string
}

export interface RoleListResponse {
  items: Role[]
  page: number
  size: number
  total: number
  pages: number
}

export interface RoleFormValues {
  name: string
  description: string
  permission_codes: string[]
}

// The whole system only defines these two permission codes (app/models/permission.py) —
// there is no endpoint to list them, so they're mirrored here as a closed set.
export const PERMISSION_CODES = ['ADMIN_PANEL_ACCESS', 'SUPER_ADMIN'] as const

export function listRoles(page = 1, size = 10): Promise<RoleListResponse> {
  return apiClient.get(`/admin/user/roles?page=${page}&size=${size}`)
}

export function getRole(id: number): Promise<Role> {
  return apiClient.get(`/admin/user/roles/${id}`)
}

export function createRole(payload: RoleFormValues): Promise<void> {
  return apiClient.post('/admin/user/role', payload)
}

export function updateRole(id: number, payload: RoleFormValues): Promise<void> {
  return apiClient.patch(`/admin/user/role/${id}`, payload)
}

export function deleteRole(id: number): Promise<void> {
  return apiClient.delete(`/admin/user/role/${id}`)
}
