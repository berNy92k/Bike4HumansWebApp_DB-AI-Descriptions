import { apiClient } from './apiClient'

export interface Address {
  id: number
  type: string
  company_name: string | null
  vat_number: string | null
  address_line_1: string
  address_line_2: string | null
  city: string
  postal_code: string
  country_code: string
  state_province: string
  created_at: string
  updated_at: string
}

export type AddressPayload = Omit<Address, 'id' | 'type' | 'created_at' | 'updated_at'>

export function getMyAddress(): Promise<Address> {
  return apiClient.get('/address/me')
}

export function saveMyAddress(payload: AddressPayload): Promise<Address> {
  return apiClient.put('/address/me', payload)
}
