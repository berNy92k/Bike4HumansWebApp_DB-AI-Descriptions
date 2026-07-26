import { apiClient } from './apiClient'

export interface Manufacturer {
  id: number
  name: string
  description: string | null
  is_description_ai_generated: boolean
  image_url: string | null
  created_at: string
  updated_at: string
}

export interface ManufacturerListResponse {
  items: Manufacturer[]
  page: number
  size: number
  total: number
  pages: number
}

export interface ManufacturerFormValues {
  name: string
  description: string | null
  is_description_ai_generated: boolean
  image_url: string | null
}

export function listManufacturers(page = 1, size = 10): Promise<ManufacturerListResponse> {
  return apiClient.get(`/admin/manufacturer/?page=${page}&size=${size}`)
}

export function getManufacturer(id: number): Promise<Manufacturer> {
  return apiClient.get(`/admin/manufacturer/${id}`)
}

export function createManufacturer(payload: ManufacturerFormValues): Promise<void> {
  return apiClient.post('/admin/manufacturer/', payload)
}

export function updateManufacturer(id: number, payload: ManufacturerFormValues): Promise<void> {
  return apiClient.put(`/admin/manufacturer/${id}`, payload)
}

export function deleteManufacturer(id: number): Promise<void> {
  return apiClient.delete(`/admin/manufacturer/${id}`)
}

export function generateManufacturerDescription(name: string, description: string | null): Promise<{ description: string | null }> {
  return apiClient.post('/admin/manufacturer/ai-generate-description', { name, description })
}
