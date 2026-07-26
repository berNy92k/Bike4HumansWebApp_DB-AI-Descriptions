import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getBike, type Bike } from '../../../api/bikes'
import { StatusBadge } from '../../../components/admin/StatusBadge'

export function BikeDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const [bike, setBike] = useState<Bike | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getBike(Number(id))
      .then(setBike)
      .catch(() => setError('Nie znaleziono roweru.'))
  }, [id])

  if (error) return <p role="alert">{error}</p>
  if (!bike) return <p>Ładowanie...</p>

  return (
    <section>
      <h1>{bike.name}</h1>
      <p>{bike.description ?? 'Brak opisu.'}</p>
      {bike.is_description_ai_generated && <span className="ai-badge">Opis wygenerowany przez AI</span>}
      <dl className="admin-details-grid">
        <dt>Cena</dt>
        <dd>{bike.price} PLN</dd>
        <dt>Stan magazynowy</dt>
        <dd>{bike.stock_quantity}</dd>
        <dt>Aktywny</dt>
        <dd>
          <StatusBadge active={bike.is_active} />
        </dd>
        <dt>Typ</dt>
        <dd>{bike.bike_type ?? '—'}</dd>
        <dt>Materiał ramy</dt>
        <dd>{bike.frame_material ?? '—'}</dd>
        <dt>Rozmiar ramy</dt>
        <dd>
          {bike.frame_size ?? '—'} {bike.frame_size_label ?? ''}
        </dd>
        <dt>Koła</dt>
        <dd>{bike.wheel_size ?? '—'}"</dd>
        <dt>Opony</dt>
        <dd>{bike.tire_width ?? '—'} mm</dd>
        <dt>Biegi</dt>
        <dd>{bike.gear_count ?? '—'}</dd>
        <dt>Hamulce</dt>
        <dd>{bike.brake_type ?? '—'}</dd>
        <dt>Amortyzacja</dt>
        <dd>{bike.suspension_type ?? '—'}</dd>
        <dt>Kolor</dt>
        <dd>{bike.color ?? '—'}</dd>
        <dt>Waga</dt>
        <dd>{bike.weight_kg ?? '—'} kg</dd>
        <dt>Zalecany wzrost</dt>
        <dd>
          {bike.recommended_height_min ?? '—'}–{bike.recommended_height_max ?? '—'} cm
        </dd>
        <dt>Przeznaczenie</dt>
        <dd>{bike.usage ?? '—'}</dd>
        <dt>Dla kogo</dt>
        <dd>{bike.target_user ?? '—'}</dd>
      </dl>
      <Link to={`/admin/bikes/${bike.id}/edit`}>Edytuj</Link>
      {' · '}
      <Link to="/admin/bikes/list">Wróć do listy</Link>
    </section>
  )
}
