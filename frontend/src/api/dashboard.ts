import { apiClient } from './apiClient'

export interface StatusCount {
  status: string
  count: number
}

export interface MonthlyRevenue {
  month: string
  revenue: number
}

export interface TopBike {
  bike_id: number
  name: string
  quantity_sold: number
  revenue: number
}

export interface CatalogHealth {
  bikes_with_image_pct: number
  bikes_with_description_pct: number
  bikes_complete_pct: number
  manufacturers_with_bikes_pct: number
}

export interface DashboardStats {
  bikes_count: number
  manufacturers_count: number
  users_count: number
  roles_count: number
  orders_count: number
  orders_total_revenue: number
  average_order_value: number
  orders_by_status: StatusCount[]
  revenue_by_month: MonthlyRevenue[]
  top_bikes: TopBike[]
  catalog_health: CatalogHealth
}

export function getDashboardStats(): Promise<DashboardStats> {
  return apiClient.get('/admin/dashboard/stats')
}
