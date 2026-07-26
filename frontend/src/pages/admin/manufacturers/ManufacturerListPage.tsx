import { useCallback, useState } from 'react'
import { Link } from 'react-router-dom'
import { deleteManufacturer, listManufacturers } from '../../../api/manufacturers'
import { usePaginatedList } from '../../../hooks/usePaginatedList'
import { Pagination } from '../../../components/Pagination'
import { AdminListSection } from '../../../components/admin/AdminListSection'
import { StatusBadge } from '../../../components/admin/StatusBadge'

export function ManufacturerListPage() {
  const [page, setPage] = useState(1)
  const fetcher = useCallback((p: number) => listManufacturers(p), [])
  const { data, isLoading, error, reload } = usePaginatedList(fetcher, page)

  async function handleDelete(id: number, name: string) {
    if (!window.confirm(`Na pewno usunąć producenta "${name}"?`)) return
    await deleteManufacturer(id)
    reload()
  }

  return (
    <section>
      <div className="admin-page-header">
        <h1>Producenci</h1>
        <Link to="/admin/manufacturer/create" className="btn-primary">
          Nowy producent
        </Link>
      </div>

      {isLoading && <p>Ładowanie...</p>}
      {error && <p role="alert">{error}</p>}

      {data && (
        <AdminListSection title="Lista producentów" total={data.total}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nazwa</th>
                <th>Opis AI?</th>
                <th>Akcje</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((manufacturer) => (
                <tr key={manufacturer.id}>
                  <td>{manufacturer.id}</td>
                  <td>{manufacturer.name}</td>
                  <td>
                    <StatusBadge active={manufacturer.is_description_ai_generated} />
                  </td>
                  <td>
                    <div className="admin-table-actions">
                      <Link to={`/admin/manufacturer/${manufacturer.id}/details`} className="btn-info">
                        Szczegóły
                      </Link>
                      <Link to={`/admin/manufacturer/${manufacturer.id}/edit`} className="btn-warning">
                        Edytuj
                      </Link>
                      <button
                        className="btn-danger"
                        onClick={() => void handleDelete(manufacturer.id, manufacturer.name)}
                      >
                        Usuń
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        </AdminListSection>
      )}
    </section>
  )
}
