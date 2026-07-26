import { useCallback, useState } from 'react'
import { Link } from 'react-router-dom'
import { deleteBike, listBikes } from '../../../api/bikes'
import { usePaginatedList } from '../../../hooks/usePaginatedList'
import { Pagination } from '../../../components/Pagination'
import { AdminListSection } from '../../../components/admin/AdminListSection'
import { StatusBadge } from '../../../components/admin/StatusBadge'

export function BikeListPage() {
  const [page, setPage] = useState(1)
  const fetcher = useCallback((p: number) => listBikes(p), [])
  const { data, isLoading, error, reload } = usePaginatedList(fetcher, page)

  async function handleDelete(id: number, name: string) {
    if (!window.confirm(`Na pewno usunąć rower "${name}"?`)) return
    await deleteBike(id)
    reload()
  }

  return (
    <section>
      <div className="admin-page-header">
        <h1>Rowery</h1>
        <Link to="/admin/bikes/create" className="btn-primary">
          Nowy rower
        </Link>
      </div>

      {isLoading && <p>Ładowanie...</p>}
      {error && <p role="alert">{error}</p>}

      {data && (
        <AdminListSection title="Lista rowerów" total={data.total}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nazwa</th>
                <th>Cena</th>
                <th>Stan</th>
                <th>Aktywny</th>
                <th>Akcje</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((bike) => (
                <tr key={bike.id}>
                  <td>{bike.id}</td>
                  <td>{bike.name}</td>
                  <td>{bike.price} PLN</td>
                  <td>{bike.stock_quantity}</td>
                  <td>
                    <StatusBadge active={bike.is_active} />
                  </td>
                  <td>
                    <div className="admin-table-actions">
                      <Link to={`/admin/bikes/${bike.id}/details`} className="btn-info">
                        Szczegóły
                      </Link>
                      <Link to={`/admin/bikes/${bike.id}/edit`} className="btn-warning">
                        Edytuj
                      </Link>
                      <button className="btn-danger" onClick={() => void handleDelete(bike.id, bike.name)}>
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
