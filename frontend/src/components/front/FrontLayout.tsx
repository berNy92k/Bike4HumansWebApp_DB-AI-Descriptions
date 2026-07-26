import { Link, Outlet } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { useCartCheckoutStatus } from '../../hooks/useCartCheckoutStatus'
import { ThemeToggle } from '../ThemeToggle'

export function FrontLayout() {
  const { user, logout } = useAuth()
  const { hasCart, hasCheckout } = useCartCheckoutStatus()

  return (
    <div className="front-shell">
      <header className="site-header">
        <Link to="/" className="site-brand">
          🚴 Bike4Humans
        </Link>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/bikes">Rowery</Link>
          <Link to="/manufacturers">Producenci</Link>
        </nav>
        <div className="site-header-actions">
          <ThemeToggle />
          {user ? (
            <>
              {hasCheckout ? (
                <Link to="/cart/step2">Checkout</Link>
              ) : hasCart ? (
                <Link to="/cart/step1">Koszyk</Link>
              ) : null}
              <button onClick={() => void logout()}>Wyloguj się</button>
            </>
          ) : (
            <Link to="/auth/login">Zaloguj się</Link>
          )}
        </div>
      </header>
      <Outlet />
    </div>
  )
}
