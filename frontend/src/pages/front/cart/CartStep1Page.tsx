import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getMyCart, type Cart } from '../../../api/cart'
import { createCheckout } from '../../../api/checkout'
import { useBikeLookup } from '../../../hooks/useBikeLookup'

export function CartStep1Page() {
  const navigate = useNavigate()
  const [cart, setCart] = useState<Cart | null>(null)
  const [isEmpty, setIsEmpty] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const bikes = useBikeLookup(cart?.items.map((i) => i.bike_id) ?? [])

  useEffect(() => {
    getMyCart()
      .then(setCart)
      .catch(() => setIsEmpty(true))
  }, [])

  async function handleNext() {
    setIsSubmitting(true)
    setError(null)
    try {
      await createCheckout()
      navigate('/cart/step2')
    } catch {
      setError('Nie udało się utworzyć checkoutu.')
      setIsSubmitting(false)
    }
  }

  if (isEmpty) {
    return (
      <main>
        <h1>Twój koszyk jest pusty</h1>
        <Link to="/">Wróć do zakupów</Link>
      </main>
    )
  }

  if (!cart) return <p>Ładowanie...</p>

  return (
    <main>
      <span className="page-eyebrow">Koszyk</span>
      <h1>Krok 1: podsumowanie zamówienia</h1>
      <p className="section-subtitle">Sprawdź zawartość koszyka i przejdź do kolejnego etapu zakupu.</p>

      <div className="order-details-main">
        <div className="order-details-main-header">
          <div>
            <h3>Twoje produkty</h3>
            <p className="card-subtitle">Masz {cart.items.length} produkt(ów) w koszyku.</p>
          </div>
          <span className="inline-badge">Krok 1 z 3</span>
        </div>

        <div className="cart-items">
          {cart.items.map((item) => {
            const bike = bikes[item.bike_id]
            return (
              <div key={item.id} className="cart-item">
                {bike?.image_url && <img src={bike.image_url} alt={bike.name} />}
                <div>
                  <h4>{bike?.name ?? `Rower #${item.bike_id}`}</h4>
                  {bike && (
                    <p>
                      Cena: <strong>{bike.price} zł</strong>
                    </p>
                  )}
                  <p>
                    Ilość: <strong>{item.quantity}</strong>
                  </p>
                  {bike?.color && (
                    <p>
                      Kolor: <strong>{bike.color}</strong>
                    </p>
                  )}
                  {bike?.frame_size && (
                    <p>
                      Rama: <strong>{bike.frame_size}</strong>
                    </p>
                  )}
                </div>
                <div className="cart-item-value">
                  <span>Wartość</span>
                  <strong>{bike ? (bike.price * item.quantity).toFixed(2) : '—'} zł</strong>
                </div>
              </div>
            )
          })}
        </div>

        <div className="cart-step1-footer">
          <p>Po kliknięciu najpierw utworzymy checkout, a potem przejdziesz do kolejnego kroku.</p>
          {error && <p role="alert">{error}</p>}
          <button className="btn-primary" onClick={() => void handleNext()} disabled={isSubmitting}>
            {isSubmitting ? 'Przetwarzanie...' : 'Dalej'}
          </button>
        </div>
      </div>
    </main>
  )
}
