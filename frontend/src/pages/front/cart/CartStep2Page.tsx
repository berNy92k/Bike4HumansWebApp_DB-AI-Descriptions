import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getMyPendingCheckout, type Checkout } from '../../../api/checkout'
import { createOrder } from '../../../api/order'
import { listPaymentMethods, type PaymentMethod } from '../../../api/paymentMethods'

export function CartStep2Page() {
  const navigate = useNavigate()
  const [checkout, setCheckout] = useState<Checkout | null>(null)
  const [methods, setMethods] = useState<PaymentMethod[]>([])
  const [selectedMethodId, setSelectedMethodId] = useState<number | null>(null)
  const [tax, setTax] = useState('0')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([getMyPendingCheckout(), listPaymentMethods()])
      .then(([c, m]) => {
        setCheckout(c)
        setMethods(m)
        setSelectedMethodId(c.payment_method_id || m[0]?.id || null)
      })
      .catch(() => setError('Nie znaleziono checkoutu.'))
  }, [])

  async function handleSubmit() {
    setIsSubmitting(true)
    setError(null)
    try {
      await createOrder()
      navigate('/cart/payment-provider')
    } catch {
      setError('Nie udało się złożyć zamówienia.')
      setIsSubmitting(false)
    }
  }

  if (error && !checkout) return <p role="alert">{error}</p>
  if (!checkout) return <p>Ładowanie...</p>

  const selectedMethod = methods.find((m) => m.id === selectedMethodId)
  const total = checkout.total_price + (selectedMethod?.price ?? 0)

  return (
    <main>
      <span className="page-eyebrow">Koszyk</span>
      <h1>Krok 2: kwota całkowita, podatki, rabat i płatność</h1>
      <p className="section-subtitle">
        Sprawdź podsumowanie zamówienia, wybierz metodę płatności i opcjonalnie dodaj kod zniżkowy oraz tax.
      </p>

      <div className="order-details-grid">
        <div className="order-details-main-col">
          <div className="order-details-main">
            <div className="order-details-main-header">
              <h3>Podsumowanie checkouta</h3>
              <span className="inline-badge">Wyliczone wcześniej</span>
            </div>
            <div className="order-summary-list">
              <div className="order-summary-item">
                <span>Suma</span>
                <strong>
                  {checkout.total_price} {checkout.currency}
                </strong>
              </div>
              <div className="order-summary-item">
                <span>Dostawa</span>
                <strong>Darmowa</strong>
              </div>
              <div className="order-summary-item">
                <span>Opłata serwisowa</span>
                <strong>{selectedMethod ? selectedMethod.price.toFixed(2) : '0.00'} zł</strong>
              </div>
              <div className="order-summary-item">
                <span>Rabat</span>
                <strong>-0.00 zł</strong>
              </div>
              <div className="order-summary-item order-summary-item--total">
                <span>Razem</span>
                <strong>
                  {total} {checkout.currency}
                </strong>
              </div>
            </div>
          </div>

          <div className="order-details-main">
            <div className="order-details-main-header">
              <h3>Metody płatności</h3>
              <span className="inline-badge">Dostępne opcje</span>
            </div>
            <div className="payment-methods-list">
              {methods.map((method) => (
                <label key={method.id} className="payment-tile">
                  <input
                    type="radio"
                    name="payment_method"
                    checked={selectedMethodId === method.id}
                    onChange={() => setSelectedMethodId(method.id)}
                  />
                  <strong>{method.name}</strong>
                  <span>{method.price.toFixed(2)} zł</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        <aside className="order-details-side">
          <h3>Kod zniżkowy i tax</h3>
          <label>
            Kod zniżkowy
            <input type="text" placeholder="Wpisz kod" disabled title="Dla tego zamówienia nie da się wpisać zniżki" />
          </label>
          <label>
            Tax
            <select value={tax} onChange={(e) => setTax(e.target.value)}>
              <option value="0">0% — brak taxu</option>
              <option value="5">5% — przykładowo kraj A</option>
              <option value="8">8% — przykładowo kraj B</option>
              <option value="23">23% — przykładowo kraj C</option>
            </select>
          </label>
          {error && <p role="alert">{error}</p>}
          <button className="btn-primary" onClick={() => void handleSubmit()} disabled={isSubmitting}>
            {isSubmitting ? 'Przetwarzanie...' : 'Opłać i złóż zamówienie'}
          </button>
        </aside>
      </div>
    </main>
  )
}
