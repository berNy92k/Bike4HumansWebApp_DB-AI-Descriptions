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

export interface OrderFilters {
  page?: number
  size?: number
  order_id?: string
  user_id?: number
  status?: string
  total_price_min?: number
  total_price_max?: number
  created_at_min?: string
  created_at_max?: string
  sort_by?: 'created_at' | 'status'
  sort_direction?: 'asc' | 'desc'
}

export function listOrders(filters: OrderFilters = {}): Promise<OrderListResponse> {
  const query = new URLSearchParams()
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && String(value) !== '') query.set(key, String(value))
  })
  return apiClient.get(`/admin/orders/?${query.toString()}`)
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
