import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getManufacturer, type Manufacturer } from '../../../api/manufacturers'

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
      <p>{manufacturer.description ?? 'Brak opisu.'}</p>
      {manufacturer.is_description_ai_generated && <span className="ai-badge">Opis wygenerowany przez AI</span>}
      <p>Zdjęcie: {manufacturer.image_url ?? '—'}</p>
      <Link to={`/admin/manufacturer/${manufacturer.id}/edit`}>Edytuj</Link>
      {' · '}
      <Link to="/admin/manufacturer/list">Wróć do listy</Link>
    </section>
  )
}
