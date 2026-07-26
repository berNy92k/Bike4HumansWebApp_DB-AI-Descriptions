import { Link, NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { ThemeToggle } from '../ThemeToggle'
import {
  IconBike,
  IconCart,
  IconCreditCard,
  IconFactory,
  IconHome,
  IconPackage,
  IconShield,
  IconUser,
} from '../icons/Icons'

const navItems = [
  { to: '/admin', label: 'Dashboard', end: true, Icon: IconHome },
  { to: '/admin/bikes/list', label: 'Rowery', Icon: IconBike },
  { to: '/admin/manufacturer/list', label: 'Producenci', Icon: IconFactory },
  { to: '/admin/user/list', label: 'Użytkownicy', Icon: IconUser },
  { to: '/admin/user/role/list', label: 'Role', Icon: IconShield },
  { to: '/admin/orders/list', label: 'Zamówienia', Icon: IconPackage },
  { to: '/admin/checkouts/list', label: 'Checkouty', Icon: IconCreditCard },
  { to: '/admin/carts/list', label: 'Koszyki', Icon: IconCart },
]

export function AdminLayout() {
  const { user, logout } = useAuth()

  return (
    <div className="admin-shell">
      <aside className="admin-sidebar">
        <Link to="/admin" className="admin-sidebar-brand">
          <span className="admin-sidebar-logo">
            <IconBike />
          </span>
          <span>
            <strong>Bike4Humans</strong>
            <small>Panel administracyjny</small>
          </span>
        </Link>

        <span className="admin-nav-label">Nawigacja</span>
        <nav>
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.end}>
              <span className="admin-nav-icon">
                <item.Icon />
              </span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="admin-sidebar-footer">
          <span>Status: aktywny</span>
          <span>Zalogowano jako {user?.username}</span>
        </div>
      </aside>
      <div className="admin-main">
        <header className="admin-topbar">
          <ThemeToggle />
          <span>{user?.username}</span>
          <button onClick={() => void logout()}>Wyloguj</button>
        </header>
        <main className="admin-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
