import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getPublicManufacturer, listBikesByManufacturer } from '../../../api/frontCatalog'
import type { Manufacturer } from '../../../api/manufacturers'
import type { Bike } from '../../../api/bikes'

export function ManufacturerDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const [manufacturer, setManufacturer] = useState<Manufacturer | null>(null)
  const [bikes, setBikes] = useState<Bike[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([getPublicManufacturer(Number(id)), listBikesByManufacturer(Number(id))])
      .then(([m, b]) => {
        setManufacturer(m)
        setBikes(b)
      })
      .catch(() => setError('Nie znaleziono producenta.'))
  }, [id])

  if (error) return <p role="alert">{error}</p>
  if (!manufacturer) return <p>Ładowanie...</p>

  return (
    <main>
      <Link to="/manufacturers">← Producenci</Link>
      <h1>{manufacturer.name}</h1>
      {manufacturer.image_url && <img src={manufacturer.image_url} alt={manufacturer.name} className="bike-detail-image" />}
      <p>{manufacturer.description ?? 'Brak opisu'}</p>

      <h3>Rowery tej marki ({bikes.length})</h3>
      <div className="similar-bikes-list">
        {bikes.map((bike) => (
          <Link key={bike.id} to={`/bikes/${bike.id}`} className="mini-item">
            <span>{bike.name}</span>
            <span>{bike.price} zł</span>
          </Link>
        ))}
        {bikes.length === 0 && <p>Brak rowerów tej marki.</p>}
      </div>
    </main>
  )
}
