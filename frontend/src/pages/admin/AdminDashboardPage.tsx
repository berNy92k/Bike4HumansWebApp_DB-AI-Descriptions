import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listBikes, type Bike } from '../../api/bikes'
import { listManufacturers } from '../../api/manufacturers'
import { listUsers } from '../../api/users'
import { listRoles } from '../../api/roles'
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

const CATALOG_HEALTH = [
  { label: 'Produkty kompletne', percent: 84 },
  { label: 'Zdjęcia dodane', percent: 71 },
  { label: 'Opisy uzupełnione', percent: 92 },
  { label: 'Producenci aktywni', percent: 95 },
]

const TIPS = [
  {
    title: 'Sprawdzaj kompletność danych',
    body: 'Zanim zapiszesz produkt, upewnij się, że ma nazwę, producenta, cenę i sensowny opis. Braki w tych polach najszybciej psują jakość katalogu.',
  },
  {
    title: 'Dbaj o zdjęcia i opisy',
    body: 'Produkty bez zdjęć albo z bardzo krótkim opisem warto uzupełniać w pierwszej kolejności. To właśnie one najbardziej wpływają na odbiór oferty.',
  },
  {
    title: 'Uważaj na poprawność przypisań',
    body: 'Sprawdź, czy rower jest przypisany do właściwego producenta i czy dane nie dublują się pod podobnymi nazwami. To później oszczędza dużo ręcznej poprawy.',
  },
  {
    title: 'Porządkuj katalog regularnie',
    body: 'Jeśli widzisz nieaktualne, niepełne albo przypadkowe rekordy, poprawiaj je na bieżąco. Panel najlepiej działa wtedy, gdy dane są czyste i spójne.',
  },
]

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
              <p className="admin-panel-subtitle">Krótki podgląd jakości danych.</p>
            </div>
          </div>
          <div className="admin-progress-list">
            {CATALOG_HEALTH.map((row) => (
              <div key={row.label} className="admin-progress-row">
                <div className="admin-progress-top">
                  <span>{row.label}</span>
                  <span>{row.percent}%</span>
                </div>
                <div className="admin-progress-bar">
                  <span style={{ width: `${row.percent}%` }} />
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
