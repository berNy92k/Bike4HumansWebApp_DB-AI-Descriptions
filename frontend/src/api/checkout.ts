import { apiClient } from './apiClient'
import type { Address } from './address'
import type { CartItem } from './cart'

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
  items: CartItem[]
}

export function getMyPendingCheckout(): Promise<Checkout> {
  return apiClient.get('/checkout/')
}

export function getMyCompletedCheckout(): Promise<Checkout> {
  return apiClient.get('/checkout/completed')
}

export function createCheckout(): Promise<void> {
  return apiClient.post('/checkout/')
}
