import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listPublicBikes, listPublicManufacturers } from '../../api/frontCatalog'
import type { Bike } from '../../api/bikes'
import { IconBike, IconFactory } from '../../components/icons/Icons'

const BENEFITS = [
  {
    title: 'Selekcja produktów',
    body: 'Pokazujemy tylko oferty, które mają sens i dobrze wyglądają w katalogu.',
  },
  {
    title: 'Łatwa nawigacja',
    body: 'Strona prowadzi klienta szybko do tego, czego naprawdę szuka.',
  },
  {
    title: 'Gotowe pod rozwój',
    body: 'Układ jest prosty do rozbudowy o koszyk, filtry i szczegóły produktów.',
  },
]

export function HomePage() {
  const [bikeCount, setBikeCount] = useState<number | null>(null)
  const [manufacturerCount, setManufacturerCount] = useState<number | null>(null)
  const [featuredBikes, setFeaturedBikes] = useState<Bike[]>([])
  const [manufacturerNames, setManufacturerNames] = useState<Record<number, string>>({})

  useEffect(() => {
    listPublicBikes({ page: 1, size: 4 }).then((response) => {
      setBikeCount(response.total)
      setFeaturedBikes(response.items)
    })
    listPublicManufacturers(1, 100).then((response) => {
      setManufacturerCount(response.total)
      setManufacturerNames(Object.fromEntries(response.items.map((m) => [m.id, m.name])))
    })
  }, [])

  return (
    <main className="home-page">
      <section className="hero">
        <div className="hero-content">
          <span className="hero-badge">🚴 Sklep rowerowy premium</span>
          <h1>Rower i części, które naprawdę pasują do Twojej jazdy</h1>
          <p>
            Wybierz sprzęt, który łączy jakość, wygodę i dobry wygląd. Bez przypadkowych ofert. Bez bałaganu. Tylko
            sprawdzone produkty.
          </p>
          <div className="hero-actions">
            <Link to="/bikes" className="site-btn-primary">
              Zobacz produkty
            </Link>
            <a href="#about" className="site-btn-secondary">
              Dowiedz się więcej
            </a>
          </div>
          <div className="hero-stats">
            <div>
              <strong>{bikeCount ?? '—'}</strong>
              <span>rowerów</span>
            </div>
            <div>
              <strong>{manufacturerCount ?? '—'}</strong>
              <span>producentów</span>
            </div>
            <div>
              <strong>48h</strong>
              <span>realizacji</span>
            </div>
          </div>
        </div>
        <div className="hero-visual">
          <img src="/static/images/bikemainlogo.png" alt="Rowerzysta w lesie" />
        </div>
      </section>

      <section className="stats-grid">
        <div>
          <strong>{bikeCount ?? '—'}</strong>
          <span>rowerów w ofercie</span>
        </div>
        <div>
          <strong>{manufacturerCount ?? '—'}</strong>
          <span>sprawdzonych marek</span>
        </div>
        <div>
          <strong>48h</strong>
          <span>szybka realizacja</span>
        </div>
        <div>
          <strong>99%</strong>
          <span>satysfakcji klientów</span>
        </div>
      </section>

      <section id="categories">
        <span className="page-eyebrow">Kategorie</span>
        <h2>Wszystko, czego potrzebujesz do jazdy</h2>
        <p className="section-subtitle">Wybierz kategorię i przejdź od razu do sensownych produktów.</p>
        <div className="categories-grid">
          <Link to="/bikes" className="category-card">
            <span className="category-card-icon">
              <IconBike />
            </span>
            <h3>Rowery</h3>
            <p>Modele miejskie, trekkingowe i sportowe.</p>
          </Link>
          <Link to="/manufacturers" className="category-card">
            <span className="category-card-icon">
              <IconFactory />
            </span>
            <h3>Producenci</h3>
            <p>Sprawdzone marki i renomowani dostawcy.</p>
          </Link>
        </div>
      </section>

      <section id="about">
        <span className="page-eyebrow">Dlaczego my</span>
        <h2>Prosto, przejrzyście i bez zbędnego chaosu</h2>
        <div className="benefits-grid">
          {BENEFITS.map((benefit) => (
            <div key={benefit.title} className="benefit-card">
              <h3>{benefit.title}</h3>
              <p>{benefit.body}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="products">
        <span className="page-eyebrow">Polecane produkty</span>
        <h2>Przykładowe pozycje z oferty</h2>
        <div className="bike-grid">
          {featuredBikes.map((bike) => (
            <Link key={bike.id} to={`/bikes/${bike.id}`} className="bike-card">
              <div className="bike-card-image">{bike.image_url && <img src={bike.image_url} alt={bike.name} />}</div>
              {manufacturerNames[bike.brand_id] && (
                <span className="bike-card-badge">{manufacturerNames[bike.brand_id]}</span>
              )}
              <h3>{bike.name}</h3>
              <p>{bike.description ? bike.description.slice(0, 90) : ''}</p>
              <div className="bike-card-footer">
                <strong>{bike.price} zł</strong>
                <span className="bike-card-link">Szczegóły →</span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="cta-banner">
        <div>
          <span className="page-eyebrow">Gotowy?</span>
          <h2>Sprawdź ofertę i wybierz sprzęt dla siebie</h2>
          <p>To może być bardzo mocna strona główna, jeśli później podłączysz dynamiczne kategorie i filtry.</p>
        </div>
        <Link to="/bikes" className="site-btn-primary">
          Przejdź do produktów
        </Link>
      </section>
    </main>
  )
}
