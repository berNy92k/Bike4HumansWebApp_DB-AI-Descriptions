import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getMyCompletedCheckout, type Checkout } from '../../../api/checkout'
import { getPaymentMethod, type PaymentMethod } from '../../../api/paymentMethods'
import { updateOrderStatus } from '../../../api/order'
import { useAuth } from '../../../context/AuthContext'

// Order status values PUT /order/ accepts are lowercase (see app/models/order.py:OrderStatus);
// this simulated payment provider only ever transitions out of "pending".
const STATUS_OPTIONS = [
  { status: 'delivery', label: 'Zapłacone', className: 'btn-primary' },
  { status: 'canceled', label: 'Anuluj', className: 'btn-secondary' },
  { status: 'failed', label: 'Błąd płatności', className: 'btn-danger' },
]

export function PaymentProviderPage() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [checkout, setCheckout] = useState<Checkout | null>(null)
  const [method, setMethod] = useState<PaymentMethod | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [pendingStatus, setPendingStatus] = useState<string | null>(null)

  useEffect(() => {
    getMyCompletedCheckout()
      .then(async (c) => {
        setCheckout(c)
        setMethod(await getPaymentMethod(c.payment_method_id))
      })
      .catch(() => setError('Nie znaleziono checkoutu.'))
  }, [])

  async function handleStatus(status: string) {
    setPendingStatus(status)
    setError(null)
    try {
      const result = await updateOrderStatus(status, 'pending')
      navigate(`/order/details?order_id=${encodeURIComponent(result.order_id)}`)
    } catch {
      setError('Nie udało się zaktualizować zamówienia.')
      setPendingStatus(null)
    }
  }

  if (error && !checkout) return <p role="alert">{error}</p>
  if (!checkout || !method) return <p>Ładowanie...</p>

  return (
    <main>
      <span className="page-eyebrow">Payment provider</span>
      <h1>Fake provider płatności</h1>
      <p className="section-subtitle">Wybierz, czy płatność została zakończona, anulowana albo zakończyła się błędem.</p>

      <div className="order-details-grid">
        <div className="order-details-main">
          <div className="order-details-main-header">
            <h3>Informacje o płatności</h3>
            <span className="inline-badge">Symulacja</span>
          </div>
          <div className="order-summary-list">
            <div className="order-summary-item">
              <span>Checkout ID</span>
              <strong>{checkout.id}</strong>
            </div>
            <div className="order-summary-item">
              <span>Użytkownik</span>
              <strong>{user?.username}</strong>
            </div>
            <div className="order-summary-item">
              <span>Metoda płatności</span>
              <strong>{method.name}</strong>
            </div>
            <div className="order-summary-item">
              <span>Opłata serwisowa</span>
              <strong>
                {method.price} {checkout.currency}
              </strong>
            </div>
            <div className="order-summary-item order-summary-item--total">
              <span>Razem</span>
              <strong>
                {checkout.total_price + method.price} {checkout.currency}
              </strong>
            </div>
          </div>
        </div>

        <aside className="order-details-side">
          <h3>Fake provider</h3>
          {error && <p role="alert">{error}</p>}
          <div className="payment-provider-actions">
            {STATUS_OPTIONS.map((option) => (
              <button
                key={option.status}
                className={option.className}
                onClick={() => void handleStatus(option.status)}
                disabled={pendingStatus !== null}
              >
                {pendingStatus === option.status ? 'Przetwarzanie...' : option.label}
              </button>
            ))}
          </div>
        </aside>
      </div>
    </main>
  )
}
