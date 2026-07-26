import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listPublicManufacturers } from '../../../api/frontCatalog'
import type { ManufacturerListResponse } from '../../../api/manufacturers'
import { Pagination } from '../../../components/Pagination'

export function ManufacturerListPage() {
  const [page, setPage] = useState(1)
  const [data, setData] = useState<ManufacturerListResponse | null>(null)

  useEffect(() => {
    listPublicManufacturers(page, 9).then(setData)
  }, [page])

  return (
    <main>
      <span className="page-eyebrow">Marki</span>
      <h1>Producenci</h1>

      {data && (
        <>
          <div className="bike-grid">
            {data.items.map((manufacturer) => (
              <Link key={manufacturer.id} to={`/manufacturers/${manufacturer.id}`} className="bike-card">
                <div className="bike-card-image">
                  {manufacturer.image_url && <img src={manufacturer.image_url} alt={manufacturer.name} />}
                </div>
                <h3>{manufacturer.name}</h3>
                <p>{manufacturer.description ? manufacturer.description.slice(0, 140) : 'Brak opisu'}</p>
              </Link>
            ))}
          </div>
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        </>
      )}
    </main>
  )
}
