import { apiClient } from './apiClient'

export interface PaymentMethod {
  id: number
  name: string
  price: number
  created_at: string
  updated_at: string
}

export function listPaymentMethods(): Promise<PaymentMethod[]> {
  return apiClient.get('/payment-methods/')
}

export function getPaymentMethod(id: number): Promise<PaymentMethod> {
  return apiClient.get(`/payment-methods/${id}`)
}
