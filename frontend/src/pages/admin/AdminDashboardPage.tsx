import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listBikes, type Bike } from '../../api/bikes'
import { listManufacturers } from '../../api/manufacturers'
import { listUsers } from '../../api/users'
import { listRoles } from '../../api/roles'
import { useAuth } from '../../context/AuthContext'
import { IconBike, IconFactory, IconShield, IconUser } from '../../components/icons/Icons'

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
  bikes: 'rowery',
  manufacturers: 'producenci',
  users: 'użytkownicy',
  roles: 'role',
}

export function AdminDashboardPage() {
  const { user } = useAuth()
  const [counts, setCounts] = useState<Counts | null>(null)
  const [recentBikes, setRecentBikes] = useState<Bike[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([listBikes(1, 10), listManufacturers(1, 1), listUsers(1, 1), listRoles(1, 1)])
      .then(([bikes, manufacturers, users, roles]) => {
        setRecentBikes(bikes.items)
        setCounts({ bikes: bikes.total, manufacturers: manufacturers.total, users: users.total, roles: roles.total })
      })
      .catch(() => setError('Nie udało się pobrać danych panelu.'))
  }, [])

  return (
    <section>
      <h1>Witaj w panelu admina 👋</h1>
      <p className="admin-subtitle">{user?.username}, masz pełną kontrolę nad produktami, producentami i zawartością sklepu.</p>
      {error && <p role="alert">{error}</p>}

      {counts && (
        <div className="admin-stats">
          {(Object.keys(counts) as (keyof Counts)[]).map((key) => {
            const StatIcon = STAT_ICONS[key]
            return (
              <div key={key}>
                <span className="admin-stat-icon">
                  <StatIcon />
                </span>
                <strong>{counts[key]}</strong>
                <span>{STAT_LABELS[key]}</span>
              </div>
            )
          })}
        </div>
      )}

      <h2>Szybkie akcje</h2>
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

      <h2>Ostatnio dodane rowery</h2>
      <ul className="admin-recent-list">
        {recentBikes.map((bike) => (
          <li key={bike.id}>
            <span className="admin-nav-icon">
              <IconBike />
            </span>
            <Link to={`/admin/bikes/${bike.id}/details`}>{bike.name}</Link>
            <span className="admin-recent-price">{bike.price} PLN</span>
          </li>
        ))}
      </ul>
    </section>
  )
}
