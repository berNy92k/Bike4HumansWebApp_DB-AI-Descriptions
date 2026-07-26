import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listPublicBikes, listPublicManufacturers } from '../../api/frontCatalog'
import type { Bike } from '../../api/bikes'

export function HomePage() {
  const [bikeCount, setBikeCount] = useState<number | null>(null)
  const [manufacturerCount, setManufacturerCount] = useState<number | null>(null)
  const [featuredBikes, setFeaturedBikes] = useState<Bike[]>([])

  useEffect(() => {
    listPublicBikes({ page: 1, size: 4 }).then((response) => {
      setBikeCount(response.total)
      setFeaturedBikes(response.items)
    })
    listPublicManufacturers(1, 1).then((response) => setManufacturerCount(response.total))
  }, [])

  return (
    <main className="home-page">
      <section className="hero">
        <h1>Rower i części, które naprawdę pasują do Twojej jazdy</h1>
        <p>Wybierz sprzęt, który łączy jakość, wygodę i dobry wygląd — bez przypadkowych ofert.</p>
        <div className="hero-actions">
          <Link to="/bikes" className="site-btn-primary">
            Zobacz rowery
          </Link>
          <Link to="/manufacturers" className="site-btn-secondary">
            Producenci
          </Link>
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
      </section>

      <section>
        <span className="page-eyebrow">Wybrane dla Ciebie</span>
        <h2>Polecane rowery</h2>
        <div className="bike-grid">
          {featuredBikes.map((bike) => (
            <Link key={bike.id} to={`/bikes/${bike.id}`} className="bike-card">
              <div className="bike-card-image">{bike.image_url && <img src={bike.image_url} alt={bike.name} />}</div>
              <h3>{bike.name}</h3>
              <p>{bike.description ? bike.description.slice(0, 90) : ''}</p>
              <strong>{bike.price} zł</strong>
            </Link>
          ))}
        </div>
      </section>
    </main>
  )
}
