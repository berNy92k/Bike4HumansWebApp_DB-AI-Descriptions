import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { getMyPendingCheckout } from '../../../api/checkout'
import { createOrder } from '../../../api/order'

// Mirrors app/templates/front/cart/step3.html: reached via /cart/payment-result?payment_status=,
// re-reads the *pending* checkout (not completed) and fire-and-forgets a POST /order/ on load —
// carried forward as-is per the migration plan, since the real flow goes through
// PaymentProviderPage instead (this route looks unreachable/superseded in the original app).
// One deviation: the old page counted down and redirected to a bare "/order" URL that doesn't
// exist in the Jinja app either (only "/order/details" does) — that's a dead end with no
// upside to reproduce, so this redirects home instead.
export function PaymentResultPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const paymentStatus = searchParams.get('payment_status') ?? ''
  const [secondsLeft, setSecondsLeft] = useState(3)

  useEffect(() => {
    getMyPendingCheckout().catch(() => {})
    createOrder().catch(() => {})
  }, [])

  useEffect(() => {
    if (secondsLeft <= 0) {
      navigate('/')
      return
    }
    const timer = setTimeout(() => setSecondsLeft((s) => s - 1), 1000)
    return () => clearTimeout(timer)
  }, [secondsLeft, navigate])

  const failed = paymentStatus === 'cancel' || paymentStatus === 'failed'

  return (
    <main>
      <h1>Krok 3: finalizacja płatności</h1>
      <p>{failed ? 'Płatność nie powiodła się albo została anulowana.' : 'Finalizujemy zamówienie...'}</p>
      <p>
        Status płatności: <strong>{paymentStatus || '—'}</strong>
      </p>
      <p>Przekierowanie za {secondsLeft}s...</p>
    </main>
  )
}
