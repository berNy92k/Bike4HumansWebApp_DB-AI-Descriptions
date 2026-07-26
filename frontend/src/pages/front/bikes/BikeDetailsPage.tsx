import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getPublicBike, getSimilarBikes, type BikeSimilarRecommendation } from '../../../api/frontCatalog'
import { addToCart } from '../../../api/cart'
import { useAuth } from '../../../context/AuthContext'
import { ApiError } from '../../../api/apiClient'
import type { Bike } from '../../../api/bikes'

export function BikeDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [bike, setBike] = useState<Bike | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isAddingToCart, setIsAddingToCart] = useState(false)
  const [similar, setSimilar] = useState<BikeSimilarRecommendation | null>(null)
  const [isLoadingSimilar, setIsLoadingSimilar] = useState(false)

  useEffect(() => {
    getPublicBike(Number(id))
      .then(setBike)
      .catch(() => setError('Nie znaleziono roweru.'))
  }, [id])

  async function handleAddToCart() {
    if (!user) {
      navigate('/auth/login')
      return
    }
    setIsAddingToCart(true)
    try {
      await addToCart(Number(id))
      navigate('/cart/step1')
    } catch (err) {
      if (err instanceof ApiError && (err.status === 401 || err.status === 403)) {
        navigate('/auth/login')
        return
      }
      setError('Nie udało się dodać roweru do koszyka.')
    } finally {
      setIsAddingToCart(false)
    }
  }

  async function handleShowSimilar() {
    setIsLoadingSimilar(true)
    try {
      setSimilar(await getSimilarBikes(Number(id)))
    } catch {
      setError('Nie udało się pobrać podobnych rowerów.')
    } finally {
      setIsLoadingSimilar(false)
    }
  }

  if (error && !bike) return <p role="alert">{error}</p>
  if (!bike) return <p>Ładowanie...</p>

  return (
    <main>
      <Link to="/bikes">← Rowery</Link>
      <h1>{bike.name}</h1>

      <div className="bike-detail-layout">
        <div>
          {bike.image_url && <img src={bike.image_url} alt={bike.name} className="bike-detail-image" />}
          <h3>Opis</h3>
          <p>{bike.description ?? 'Brak opisu'}</p>

          <h3>Podobne rowery</h3>
          <button onClick={() => void handleShowSimilar()} disabled={isLoadingSimilar}>
            {isLoadingSimilar ? 'Szukam...' : 'Pokaż z AI'}
          </button>
          {similar?.note && <p>{similar.note}</p>}
          <div className="similar-bikes-list">
            {similar?.bikes.map((b) => (
              <Link key={b.id} to={`/bikes/${b.id}`} className="mini-item">
                <span>{b.name}</span>
                <span>{b.price} zł</span>
              </Link>
            ))}
            {similar && similar.bikes.length === 0 && <p>Brak podobnych rowerów do pokazania.</p>}
          </div>
        </div>

        <aside>
          <dl className="admin-details-grid">
            <dt>Rama</dt>
            <dd>{bike.frame_size ?? '—'}</dd>
            <dt>Koła</dt>
            <dd>{bike.wheel_size ?? '—'}</dd>
            <dt>Cena</dt>
            <dd>{bike.price} zł</dd>
            <dt>Dostępność</dt>
            <dd>{bike.stock_quantity}</dd>
            <dt>Kolor</dt>
            <dd>{bike.color ?? '—'}</dd>
          </dl>
          {error && <p role="alert">{error}</p>}
          <button className="btn-primary" onClick={() => void handleAddToCart()} disabled={isAddingToCart}>
            {isAddingToCart ? 'Dodawanie...' : 'Dodaj do koszyka'}
          </button>
        </aside>
      </div>
    </main>
  )
}
