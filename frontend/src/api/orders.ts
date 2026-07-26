import { apiClient } from './apiClient'

export interface OrderItem {
  id: number
  bike_id: number
  quantity: number
  created_at: string
  updated_at: string
}

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
  items: OrderItem[]
}

export interface OrderListResponse {
  orders: Order[]
  page: number
  size: number
  total: number
  pages: number
}

// Order.status is stored uppercase (e.g. "PENDING"), but PUT /admin/orders/{id} takes the
// OrderStatus *enum value*, which is lowercase (see app/models/order.py:OrderStatus).
export const ORDER_STATUSES = ['pending', 'delivery', 'canceled', 'failed', 'completed'] as const

export function listOrders(page = 1, size = 10): Promise<OrderListResponse> {
  return apiClient.get(`/admin/orders/?page=${page}&size=${size}`)
}

export function deleteOrder(id: number): Promise<void> {
  return apiClient.delete(`/admin/orders/${id}`)
}

export function updateOrderStatus(id: number, status: string): Promise<void> {
  return apiClient.put(`/admin/orders/${id}?status=${status}`)
}

export function generateOrderSummary(id: number): Promise<{ summary: string | null }> {
  return apiClient.post(`/admin/orders/${id}/ai-summary`)
}
