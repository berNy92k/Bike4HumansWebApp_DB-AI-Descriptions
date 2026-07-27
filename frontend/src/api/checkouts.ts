import { apiClient } from './apiClient'
import type { Address } from './address'
import type { OrderItem } from './orders'

export interface Checkout {
  id: number
  user_id: number
  currency: string
  status: string
  total_price: number
  payment_method_id: number
  created_at: string
  updated_at: string
  ai_summary: string | null
  address: Address | null
  items: OrderItem[]
}

export interface CheckoutListResponse {
  checkouts: Checkout[]
  page: number
  size: number
  total: number
  pages: number
}

export function listCheckouts(page = 1, size = 10): Promise<CheckoutListResponse> {
  return apiClient.get(`/admin/checkouts/?page=${page}&size=${size}`)
}

export function deleteCheckout(id: number): Promise<void> {
  return apiClient.delete(`/admin/checkouts/${id}`)
}

export function generateCheckoutSummary(id: number): Promise<{ summary: string | null }> {
  return apiClient.post(`/admin/checkouts/${id}/ai-summary`)
}
