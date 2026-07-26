import { apiClient } from './apiClient'

export interface CartItem {
  id: number
  bike_id: number
  quantity: number
  created_at: string
  updated_at: string
}

export interface Cart {
  id: number
  user_id: number
  currency: string
  status: string
  created_at: string
  updated_at: string
  ai_summary: string | null
  items: CartItem[]
}

export function getMyCart(): Promise<Cart> {
  return apiClient.get('/cart/')
}

export function addToCart(bikeId: number): Promise<void> {
  return apiClient.post('/cart/item', { bike_id: bikeId })
}
