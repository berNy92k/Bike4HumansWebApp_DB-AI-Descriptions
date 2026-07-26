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
      <h1>Krok 1: podsumowanie zamówienia</h1>
      <p>Masz {cart.items.length} produkt(ów) w koszyku.</p>

      <div className="cart-items">
        {cart.items.map((item) => {
          const bike = bikes[item.bike_id]
          return (
            <div key={item.id} className="cart-item">
              {bike?.image_url && <img src={bike.image_url} alt={bike.name} />}
              <div>
                <h4>{bike?.name ?? `Rower #${item.bike_id}`}</h4>
                <p>Ilość: {item.quantity}</p>
                {bike?.color && <p>Kolor: {bike.color}</p>}
              </div>
              <strong>{bike ? (bike.price * item.quantity).toFixed(2) : '—'} zł</strong>
            </div>
          )
        })}
      </div>

      {error && <p role="alert">{error}</p>}
      <button className="btn-primary" onClick={() => void handleNext()} disabled={isSubmitting}>
        {isSubmitting ? 'Przetwarzanie...' : 'Dalej'}
      </button>
    </main>
  )
}
