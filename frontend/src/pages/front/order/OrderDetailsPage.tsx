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

  return (
    <main>
      <h1>{failed ? 'Nie udało się sfinalizować płatności' : 'Zamówienie zostało utworzone'}</h1>

      <div className="checkout-summary">
        <div>
          <span>Status</span>
          <strong>{order.status}</strong>
        </div>
        {!failed && (
          <>
            <div>
              <span>Numer zamówienia</span>
              <strong>#{order.order_id}</strong>
            </div>
            <div>
              <span>Metoda płatności</span>
              <strong>{method?.name}</strong>
            </div>
            <div>
              <span>Suma produktów</span>
              <strong>
                {order.total_price} {order.currency}
              </strong>
            </div>
          </>
        )}
      </div>

      {failed ? (
        <Link to="/cart/step2">Wróć do płatności</Link>
      ) : (
        <>
          <h3>Pozycje w zamówieniu</h3>
          <div className="cart-items">
            {order.items.map((item) => {
              const bike = bikes[item.bike_id]
              return (
                <div key={item.id} className="cart-item">
                  <div>
                    <h4>
                      {bike?.name ?? `Rower #${item.bike_id}`} × {item.quantity}
                    </h4>
                  </div>
                  <strong>{bike ? (bike.price * item.quantity).toFixed(2) : '—'} zł</strong>
                </div>
              )
            })}
          </div>
          <Link to="/">Wróć na stronę główną</Link>
        </>
      )}
    </main>
  )
}
