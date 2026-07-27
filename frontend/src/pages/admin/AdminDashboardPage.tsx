import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listBikes, type Bike } from '../../api/bikes'
import { getDashboardStats, type DashboardStats } from '../../api/dashboard'
import { useAuth } from '../../context/AuthContext'
import { IconBike, IconFactory, IconSearch, IconShield, IconUser } from '../../components/icons/Icons'

interface Counts {
  bikes: number
  manufacturers: number
  users: number
  roles: number
}

const STAT_ICONS: Record<keyof Counts, typeof IconBike> = {
  bikes: IconBike,
  manufacturers: IconFactory,
  users: IconUser,
  roles: IconShield,
}

const STAT_LABELS: Record<keyof Counts, string> = {
  bikes: 'Rowery',
  manufacturers: 'Producenci',
  users: 'Użytkownicy',
  roles: 'Role',
}

const STAT_NOTES: Record<keyof Counts, string> = {
  bikes: 'Liczba wszystkich rowerów w bazie',
  manufacturers: 'Ilość producentów w systemie',
  users: 'Ilość użytkowników w systemie',
  roles: 'Ilość roli w systemie',
}

const CATALOG_HEALTH_LABELS: { key: keyof DashboardStats['catalog_health']; label: string }[] = [
  { key: 'bikes_complete_pct', label: 'Produkty kompletne' },
  { key: 'bikes_with_image_pct', label: 'Zdjęcia dodane' },
  { key: 'bikes_with_description_pct', label: 'Opisy uzupełnione' },
  { key: 'manufacturers_with_bikes_pct', label: 'Producenci z ofertą' },
]

const STATUS_LABELS_PL: Record<string, string> = {
  PENDING: 'Oczekujące',
  DELIVERY: 'W dostawie',
  COMPLETED: 'Zrealizowane',
  CANCELED: 'Anulowane',
  FAILED: 'Nieudane',
}

const MONTH_LABELS_PL = [
  'sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip', 'sie', 'wrz', 'paź', 'lis', 'gru',
]

function formatMonth(month: string): string {
  const [, monthNum] = month.split('-')
  const index = Number(monthNum) - 1
  return MONTH_LABELS_PL[index] ?? month
}

function formatPln(value: number): string {
  return `${value.toLocaleString('pl-PL', { maximumFractionDigits: 0 })} zł`
}

const TIPS = [
  {
    title: 'Sprawdzaj kompletność danych',
    body: 'Zanim zapiszesz produkt, upewnij się, że ma nazwę, producenta, cenę i sensowny opis. Braki w tych polach najszybciej psują jakość katalogu.',
  },
  {
    title: 'Dbaj o zdjęcia i opisy',
    body: 'Produkty bez zdjęć albo z bardzo krótkim opisem warto uzupełniać w pierwszej kolejności. To właśnie one najbardziej wpływają na odbiór oferty.',
  },
]

export function AdminDashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [recentBikes, setRecentBikes] = useState<Bike[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([getDashboardStats(), listBikes(1, 10)])
      .then(([dashboardStats, bikes]) => {
        setStats(dashboardStats)
        setRecentBikes(bikes.items)
      })
      .catch(() => setError('Nie udało się pobrać danych panelu.'))
  }, [])

  const counts: Counts | null = stats && {
    bikes: stats.bikes_count,
    manufacturers: stats.manufacturers_count,
    users: stats.users_count,
    roles: stats.roles_count,
  }

  const maxMonthlyRevenue = stats ? Math.max(1, ...stats.revenue_by_month.map((row) => row.revenue)) : 1
  const maxStatusCount = stats ? Math.max(1, ...stats.orders_by_status.map((row) => row.count)) : 1

  return (
    <section className="admin-dashboard">
      <div className="admin-dashboard-topbar">
        <div>
          <h1>Witaj w panelu admina 👋</h1>
          <p className="admin-subtitle">
            {user?.username}, masz pełną kontrolę nad produktami, producentami i zawartością sklepu.
          </p>
        </div>
        <label className="admin-search">
          <IconSearch />
          <input type="text" placeholder="Szukaj produktu, marki, modelu..." />
        </label>
      </div>

      {error && <p role="alert">{error}</p>}

      {counts && (
        <div className="admin-stats">
          {(Object.keys(counts) as (keyof Counts)[]).map((key) => {
            const StatIcon = STAT_ICONS[key]
            return (
              <div key={key}>
                <div className="admin-stat-top">
                  <span>{STAT_LABELS[key]}</span>
                  <span className="admin-stat-icon">
                    <StatIcon />
                  </span>
                </div>
                <strong>{counts[key]}</strong>
                <span className="admin-stat-note">{STAT_NOTES[key]}</span>
              </div>
            )
          })}
        </div>
      )}

      {stats && (
        <div className="admin-panel admin-revenue-panel">
          <div className="admin-panel-header">
            <div>
              <h2>Przychód</h2>
              <p className="admin-panel-subtitle">Na podstawie zrealizowanych zamówień (dostarczone i zakończone).</p>
            </div>
            <span className="admin-badge admin-badge--blue">{stats.orders_count} zamówień łącznie</span>
          </div>
          <div className="admin-revenue-summary">
            <div>
              <span className="admin-stat-note">Łączny przychód</span>
              <strong>{formatPln(stats.orders_total_revenue)}</strong>
            </div>
            <div>
              <span className="admin-stat-note">Średnia wartość zamówienia</span>
              <strong>{formatPln(stats.average_order_value)}</strong>
            </div>
          </div>
          {stats.revenue_by_month.length > 0 && (
            <div className="admin-bar-chart">
              {stats.revenue_by_month.map((row) => (
                <div key={row.month} className="admin-bar-chart-col">
                  <span className="admin-bar-chart-value">{formatPln(row.revenue)}</span>
                  <div className="admin-bar-chart-track">
                    <span style={{ height: `${(row.revenue / maxMonthlyRevenue) * 100}%` }} />
                  </div>
                  <span className="admin-bar-chart-label">{formatMonth(row.month)}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="admin-dashboard-grid">
        <div className="admin-panel">
          <div className="admin-panel-header">
            <div>
              <h2>Szybkie akcje</h2>
              <p className="admin-panel-subtitle">Najczęściej używane operacje w jednym miejscu.</p>
            </div>
            <span className="admin-badge admin-badge--blue">Admin tools</span>
          </div>
          <div className="admin-quick-actions">
            <Link to="/admin/bikes/create" className="admin-quick-action">
              <span className="admin-quick-action-icon admin-quick-action-icon--blue">
                <IconBike />
              </span>
              <span>
                <strong>Dodaj rower</strong>
                <small>Utwórz nowy produkt i przypisz go do producenta.</small>
              </span>
            </Link>
            <Link to="/admin/manufacturer/create" className="admin-quick-action">
              <span className="admin-quick-action-icon admin-quick-action-icon--orange">
                <IconFactory />
              </span>
              <span>
                <strong>Dodaj producenta</strong>
                <small>Rozszerz bazę marek i dostawców.</small>
              </span>
            </Link>
          </div>
        </div>

        <div className="admin-panel">
          <div className="admin-panel-header">
            <div>
              <h2>Stan katalogu</h2>
              <p className="admin-panel-subtitle">Realny podgląd jakości danych, liczony z bazy.</p>
            </div>
          </div>
          <div className="admin-progress-list">
            {stats && CATALOG_HEALTH_LABELS.map((row) => (
              <div key={row.key} className="admin-progress-row">
                <div className="admin-progress-top">
                  <span>{row.label}</span>
                  <span>{stats.catalog_health[row.key]}%</span>
                </div>
                <div className="admin-progress-bar">
                  <span style={{ width: `${stats.catalog_health[row.key]}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="admin-panel">
          <div className="admin-panel-header">
            <h2>Ostatnio dodane rowery</h2>
            <Link to="/admin/bikes/list" className="admin-badge admin-badge--green">
              Zobacz wszystkie
            </Link>
          </div>
          <ul className="admin-recent-list">
            {recentBikes.map((bike) => (
              <li key={bike.id}>
                <span className="admin-nav-icon">
                  <IconBike />
                </span>
                <span className="admin-recent-list-text">
                  <Link to={`/admin/bikes/${bike.id}/details`}>{bike.name}</Link>
                  <small>
                    ID: {bike.id} • {bike.created_at}
                  </small>
                </span>
                <span className="admin-recent-price">{bike.price} PLN</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="admin-panel">
          <div className="admin-panel-header">
            <div>
              <h2>Zamówienia wg statusu</h2>
              <p className="admin-panel-subtitle">Wszystkie zamówienia, niezależnie od realizacji.</p>
            </div>
            <Link to="/admin/orders/list" className="admin-badge admin-badge--green">
              Zobacz wszystkie
            </Link>
          </div>
          <div className="admin-progress-list">
            {stats && stats.orders_by_status.map((row) => (
              <div key={row.status} className="admin-progress-row">
                <div className="admin-progress-top">
                  <span>{STATUS_LABELS_PL[row.status] ?? row.status}</span>
                  <span>{row.count}</span>
                </div>
                <div className="admin-progress-bar">
                  <span style={{ width: `${(row.count / maxStatusCount) * 100}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="admin-panel">
          <div className="admin-panel-header">
            <h2>Najlepiej sprzedające się rowery</h2>
          </div>
          <ul className="admin-recent-list">
            {stats && stats.top_bikes.length === 0 && <li><span className="admin-stat-note">Brak zrealizowanych zamówień.</span></li>}
            {stats && stats.top_bikes.map((bike) => (
              <li key={bike.bike_id}>
                <span className="admin-nav-icon">
                  <IconBike />
                </span>
                <span className="admin-recent-list-text">
                  <Link to={`/admin/bikes/${bike.bike_id}/details`}>{bike.name}</Link>
                  <small>{bike.quantity_sold} szt. sprzedanych</small>
                </span>
                <span className="admin-recent-price">{formatPln(bike.revenue)}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="admin-panel">
          <div className="admin-panel-header">
            <div>
              <h2>Szybka uwaga</h2>
              <p className="admin-panel-subtitle">Co warto sprawdzić podczas pracy w panelu.</p>
            </div>
          </div>
          <div className="admin-hint-list">
            {TIPS.map((tip) => (
              <div key={tip.title} className="admin-hint-box">
                <h3>{tip.title}</h3>
                <p>{tip.body}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <p className="admin-footer-note">Bike4Humans admin dashboard • zbudowany jako lekka, czytelna baza.</p>
    </section>
  )
}
