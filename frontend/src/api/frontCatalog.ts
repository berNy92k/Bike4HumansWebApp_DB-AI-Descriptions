import { apiClient } from './apiClient'
import type { Bike, BikeListResponse } from './bikes'
import type { Manufacturer, ManufacturerListResponse } from './manufacturers'

export interface BikeFilters {
  page?: number
  size?: number
  bike_type?: string
  usage?: string
  target_user?: string
  price_min?: number
  price_max?: number
}

// Public catalog endpoints live under /api/bikes and /api/manufacturers, not the bare
// /bikes and /manufacturers prefixes — those are still owned by the old Jinja pages until
// Faza 5 (see the comment in app/routers/endpoints/front/bike_router.py).
export function listPublicBikes(filters: BikeFilters = {}): Promise<BikeListResponse> {
  const query = new URLSearchParams()
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== '') query.set(key, String(value))
  })
  return apiClient.get(`/api/bikes/?${query.toString()}`)
}

export function getPublicBike(id: number): Promise<Bike> {
  return apiClient.get(`/api/bikes/${id}`)
}

export function listPublicManufacturers(page = 1, size = 9): Promise<ManufacturerListResponse> {
  return apiClient.get(`/api/manufacturers/?page=${page}&size=${size}`)
}

export function getPublicManufacturer(id: number): Promise<Manufacturer> {
  return apiClient.get(`/api/manufacturers/${id}`)
}

export function listBikesByManufacturer(manufacturerId: number): Promise<Bike[]> {
  return apiClient.get(`/api/manufacturers/${manufacturerId}/bikes`)
}

export interface BikeSearchFilters {
  bike_type: string | null
  usage: string | null
  target_user: string | null
  price_min: number | null
  price_max: number | null
}

export function searchBikesWithAi(query: string): Promise<BikeSearchFilters> {
  return apiClient.post('/bikes/ai-search', { query })
}

export interface SimilarBike {
  id: number
  name: string
  price: number
  image_url: string | null
}

export interface BikeSimilarRecommendation {
  note: string | null
  bikes: SimilarBike[]
}

export function getSimilarBikes(bikeId: number): Promise<BikeSimilarRecommendation> {
  return apiClient.post(`/bikes/${bikeId}/ai-similar-bikes`)
}
