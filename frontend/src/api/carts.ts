import { apiClient } from './apiClient'
import type { OrderItem } from './orders'

export interface AdminCart {
  id: number
  user_id: number
  currency: string
  status: string
  created_at: string
  updated_at: string
  ai_summary: string | null
  items: OrderItem[]
}

export interface AdminCartListResponse {
  carts: AdminCart[]
  page: number
  size: number
  total: number
  pages: number
}

export function listCarts(page = 1, size = 10): Promise<AdminCartListResponse> {
  return apiClient.get(`/admin/carts/?page=${page}&size=${size}`)
}

export function deleteCart(id: number): Promise<void> {
  return apiClient.delete(`/admin/carts/${id}`)
}

export function generateCartSummary(id: number): Promise<{ summary: string | null }> {
  return apiClient.post(`/admin/carts/${id}/ai-summary`)
}
