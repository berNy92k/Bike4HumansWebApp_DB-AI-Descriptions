import { apiClient } from './apiClient'

export interface Bike {
  id: number
  name: string
  description: string | null
  is_description_ai_generated: boolean
  bike_type: string | null
  frame_material: string | null
  frame_size: number | null
  frame_size_label: string | null
  wheel_size: number | null
  tire_width: number | null
  gear_count: number | null
  brake_type: string | null
  suspension_type: string | null
  color: string | null
  weight_kg: number | null
  recommended_height_min: number | null
  recommended_height_max: number | null
  usage: string | null
  target_user: string | null
  price: number
  stock_quantity: number
  image_url: string | null
  is_active: boolean
  created_at: string
  updated_at: string
  brand_id: number
}

export interface BikeListResponse {
  items: Bike[]
  page: number
  size: number
  total: number
  pages: number
}

export interface BikeFormValues {
  name: string
  description: string | null
  is_description_ai_generated: boolean
  bike_type: string | null
  frame_material: string | null
  frame_size: number | null
  frame_size_label: string | null
  wheel_size: number | null
  tire_width: number | null
  gear_count: number | null
  brake_type: string | null
  suspension_type: string | null
  color: string | null
  weight_kg: number | null
  recommended_height_min: number | null
  recommended_height_max: number | null
  usage: string | null
  target_user: string | null
  price: number
  stock_quantity: number
  image_url: string | null
  is_active: boolean
  brand_id: number
}

export const emptyBikeForm: BikeFormValues = {
  name: '',
  description: '',
  is_description_ai_generated: false,
  bike_type: '',
  frame_material: '',
  frame_size: null,
  frame_size_label: '',
  wheel_size: null,
  tire_width: null,
  gear_count: null,
  brake_type: '',
  suspension_type: '',
  color: '',
  weight_kg: null,
  recommended_height_min: null,
  recommended_height_max: null,
  usage: '',
  target_user: '',
  price: 0,
  stock_quantity: 0,
  image_url: '',
  is_active: true,
  brand_id: 0,
}

export function listBikes(page = 1, size = 10): Promise<BikeListResponse> {
  return apiClient.get(`/admin/bikes/?page=${page}&size=${size}`)
}

export function getBike(id: number): Promise<Bike> {
  return apiClient.get(`/admin/bikes/${id}`)
}

// Backend BikeCreateDto/BikeUpdateDto reject empty strings for optional enum-like fields
// only via length, not value — but sending "" instead of null makes filters/selects downstream
// treat "no selection" consistently as null, so blank optional fields are normalized here.
function normalize(payload: BikeFormValues) {
  const blankToNull = (v: string | null) => (v === '' ? null : v)
  return {
    ...payload,
    description: blankToNull(payload.description),
    bike_type: blankToNull(payload.bike_type),
    frame_material: blankToNull(payload.frame_material),
    frame_size_label: blankToNull(payload.frame_size_label),
    brake_type: blankToNull(payload.brake_type),
    suspension_type: blankToNull(payload.suspension_type),
    color: blankToNull(payload.color),
    usage: blankToNull(payload.usage),
    target_user: blankToNull(payload.target_user),
    image_url: blankToNull(payload.image_url),
  }
}

export function createBike(payload: BikeFormValues): Promise<void> {
  return apiClient.post('/admin/bikes/', normalize(payload))
}

export function updateBike(id: number, payload: BikeFormValues): Promise<void> {
  return apiClient.put(`/admin/bikes/${id}`, normalize(payload))
}

export function deleteBike(id: number): Promise<void> {
  return apiClient.delete(`/admin/bikes/${id}`)
}

export function generateBikeDescription(payload: BikeFormValues): Promise<{ description: string | null }> {
  const { price: _price, stock_quantity: _stock, image_url: _image, is_active: _active, ...rest } = normalize(payload)
  return apiClient.post('/admin/bikes/ai-generate-description', rest)
}

export interface BikeAutoTagResponse {
  bike_type: string | null
  frame_material: string | null
  frame_size_label: string | null
  brake_type: string | null
  suspension_type: string | null
  color: string | null
  usage: string | null
  target_user: string | null
}

export function autoTagBike(name: string, description: string): Promise<BikeAutoTagResponse> {
  return apiClient.post('/admin/bikes/ai-auto-tag', { name, description })
}
