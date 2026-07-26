import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getManufacturer, type Manufacturer } from '../../../api/manufacturers'
import { StatusBadge } from '../../../components/admin/StatusBadge'

export function ManufacturerDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const [manufacturer, setManufacturer] = useState<Manufacturer | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getManufacturer(Number(id))
      .then(setManufacturer)
      .catch(() => setError('Nie znaleziono producenta.'))
  }, [id])

  if (error) return <p role="alert">{error}</p>
  if (!manufacturer) return <p>Ładowanie...</p>

  return (
    <section>
      <h1>{manufacturer.name}</h1>
      {manufacturer.image_url && (
        <div className="admin-detail-image">
          <img src={manufacturer.image_url} alt={manufacturer.name} />
        </div>
      )}
      <p>{manufacturer.description ?? 'Brak opisu.'}</p>
      <dl className="admin-details-grid">
        <dt>Źródło opisu</dt>
        <dd>
          <StatusBadge
            active={manufacturer.is_description_ai_generated}
            trueLabel="Wygenerowany przez AI"
            falseLabel="Wpisany ręcznie"
          />
        </dd>
      </dl>
      <Link to={`/admin/manufacturer/${manufacturer.id}/edit`}>Edytuj</Link>
      {' · '}
      <Link to="/admin/manufacturer/list">Wróć do listy</Link>
    </section>
  )
}
