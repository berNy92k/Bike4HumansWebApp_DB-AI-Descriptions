import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { getMyOrder, type Order } from '../../../api/order'
import { getPaymentMethod, type PaymentMethod } from '../../../api/paymentMethods'
import { useBikeLookup } from '../../../hooks/useBikeLookup'

export function OrderDetailsPage() {
  const [searchParams] = useSearchParams()
  const orderId = searchParams.get('order_id') ?? ''
  const [order, setOrder] = useState<Order | null>(null)
  const [method, setMethod] = useState<PaymentMethod | null>(null)
  const [error, setError] = useState<string | null>(null)
  const bikes = useBikeLookup(order?.items.map((i) => i.bike_id) ?? [])

  useEffect(() => {
    if (!orderId) {
      setError('Brak numeru zamówienia.')
      return
    }
    getMyOrder(orderId)
      .then(async (o) => {
        setOrder(o)
        setMethod(await getPaymentMethod(o.payment_method_id))
      })
      .catch(() => setError('Nie znaleziono zamówienia.'))
  }, [orderId])

  if (error) return <p role="alert">{error}</p>
  if (!order) return <p>Ładowanie...</p>

  const failed = ['CANCELED', 'FAILED'].includes(order.status.toUpperCase())
  const tax = 0

  return (
    <main>
      <span className="page-eyebrow">Zamówienie</span>
      <h1>{failed ? 'Nie udało się sfinalizować płatności' : 'Zamówienie zostało utworzone'}</h1>
      <p className="section-subtitle">
        {failed
          ? 'To zamówienie nie zostało opłacone lub zostało anulowane. Możesz wrócić i spróbować ponownie.'
          : 'Poniżej znajdziesz podsumowanie Twojego zamówienia i jego bieżący status.'}
      </p>

      <div className="order-details-grid">
        <div className="order-details-main">
          <div className="order-details-main-header">
            <h3>{failed ? 'Status zamówienia' : 'Podsumowanie zamówienia'}</h3>
            <span className={`inline-badge ${failed ? 'inline-badge--error' : 'inline-badge--success'}`}>
              {order.status}
            </span>
          </div>
          {failed ? (
            <p className="detail-text">Płatność została anulowana lub zakończona błędem.</p>
          ) : (
            <div className="checkout-summary">
              <div>
                <span>Order ID</span>
                <strong>#{order.order_id}</strong>
              </div>
              <div>
                <span>Metoda płatności</span>
                <strong>{method?.name}</strong>
              </div>
              <div>
                <span>Waluta</span>
                <strong>{order.currency}</strong>
              </div>
              <div>
                <span>Tax</span>
                <strong>{tax}%</strong>
              </div>
              <div>
                <span>Suma produktów</span>
                <strong>
                  {order.total_price} {order.currency}
                </strong>
              </div>
              <div className="checkout-summary-total">
                <span>Łącznie</span>
                <strong>
                  {order.total_price} {order.currency}
                </strong>
              </div>
            </div>
          )}
        </div>

        <aside className="order-details-side">
          {failed ? (
            <>
              <h3>Co dalej?</h3>
              <p className="detail-text">Możesz wrócić do koszyka i ponowić próbę płatności.</p>
              <Link to="/cart/step2" className="site-btn-primary">
                Wróć do płatności
              </Link>
            </>
          ) : (
            <>
              <h3>Informacje dodatkowe</h3>
              <div className="order-details-side-row">
                <span>Status</span>
                <strong>{order.status}</strong>
              </div>
              <div className="order-details-side-row">
                <span>Payment</span>
                <strong>{method?.name}</strong>
              </div>
              <Link to="/" className="site-btn-primary">
                Wróć na stronę główną
              </Link>
            </>
          )}
        </aside>
      </div>

      {!failed && (
        <div className="order-details-main" style={{ marginTop: 24 }}>
          <div className="order-details-main-header">
            <h3>Pozycje w zamówieniu</h3>
            <span className="inline-badge">Szczegóły</span>
          </div>
          <div className="order-items-list">
            {order.items.map((item) => {
              const bike = bikes[item.bike_id]
              return (
                <div key={item.id} className="order-item-row">
                  <span>
                    {bike?.name ?? `Rower #${item.bike_id}`} × {item.quantity}
                  </span>
                  <strong>{bike ? (bike.price * item.quantity).toFixed(2) : '—'} PLN</strong>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </main>
  )
}
