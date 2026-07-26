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
          <a href="/#about">Dlaczego my</a>
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
      <footer className="site-footer">
        <div className="site-footer-inner">
          <div className="site-footer-brand">
            <h3>Bike4Humans</h3>
            <p>Nowoczesny sklep rowerowy z wyselekcjonowaną ofertą rowerów, ram i akcesoriów.</p>
          </div>
          <div>
            <h4>Szybkie linki</h4>
            <Link to="/">Strona główna</Link>
            <Link to="/bikes">Rowery</Link>
            <Link to="/manufacturers">Producenci</Link>
            <a href="/#about">O nas</a>
          </div>
          <div>
            <h4>Kontakt</h4>
            <p>Adres: Twoja lokalizacja</p>
            <p>Email: kontakt@example.com</p>
            <p>Telefon: +48 000 000 000</p>
          </div>
        </div>
        <div className="site-footer-bottom">
          <span>© 2026 Bike4Humans</span>
          <span>Zrobione z pasją do rowerów</span>
        </div>
      </footer>
    </div>
  )
}
