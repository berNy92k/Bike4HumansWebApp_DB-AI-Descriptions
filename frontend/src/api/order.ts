import { apiClient } from './apiClient'
import type { Address } from './address'
import type { CartItem } from './cart'

export interface Order {
  id: number
  order_id: string
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

// "/api/order/{id}" not "/order/{id}": the latter would collide with the SPA's own
// "/order/details" client route once Jinja is gone (order_id is a free-form string, so
// "details" is a syntactically valid id) — see app/routers/endpoints/front/order_router.py.
export function getMyOrder(orderId: string): Promise<Order> {
  return apiClient.get(`/api/order/${orderId}`)
}

export function createOrder(): Promise<void> {
  return apiClient.post('/order/')
}

export function updateOrderStatus(status: string, previousStatus: string): Promise<{ order_id: string }> {
  return apiClient.put(`/order/?status=${status}&previous_status=${previousStatus}`)
}
