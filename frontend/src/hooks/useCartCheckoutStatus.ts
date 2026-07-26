import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { getMyCart } from '../api/cart'
import { getMyPendingCheckout } from '../api/checkout'

// Mirrors the old Jinja homepage router's best-effort has_cart/has_checkout resolution used
// to decide which header link to show. Re-checked on navigation so the header stays fresh
// after e.g. adding an item to the cart on another page.
export function useCartCheckoutStatus() {
  const { user } = useAuth()
  const location = useLocation()
  const [hasCart, setHasCart] = useState(false)
  const [hasCheckout, setHasCheckout] = useState(false)

  useEffect(() => {
    if (!user) {
      setHasCart(false)
      setHasCheckout(false)
      return
    }

    getMyCart()
      .then(() => setHasCart(true))
      .catch(() => setHasCart(false))
    getMyPendingCheckout()
      .then(() => setHasCheckout(true))
      .catch(() => setHasCheckout(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, location.pathname])

  return { hasCart, hasCheckout }
}
