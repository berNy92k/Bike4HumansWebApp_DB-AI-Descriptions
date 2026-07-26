import { useCallback, useState } from 'react'
import { Link } from 'react-router-dom'
import { deleteRole, listRoles } from '../../../api/roles'
import { usePaginatedList } from '../../../hooks/usePaginatedList'
import { Pagination } from '../../../components/Pagination'
import { AdminListSection } from '../../../components/admin/AdminListSection'

export function RoleListPage() {
  const [page, setPage] = useState(1)
  const fetcher = useCallback((p: number) => listRoles(p), [])
  const { data, isLoading, error, reload } = usePaginatedList(fetcher, page)
  const [actionError, setActionError] = useState<string | null>(null)

  async function handleDelete(id: number, name: string) {
    if (!window.confirm(`Na pewno usunąć rolę "${name}"?`)) return
    setActionError(null)
    try {
      await deleteRole(id)
      reload()
    } catch {
      setActionError('Nie udało się usunąć roli (może brakować uprawnień super admina).')
    }
  }

  return (
    <section>
      <div className="admin-page-header">
        <h1>Role</h1>
        <Link to="/admin/user/role/create" className="btn-primary">
          Nowa rola
        </Link>
      </div>

      {isLoading && <p>Ładowanie...</p>}
      {error && <p role="alert">{error}</p>}
      {actionError && <p role="alert">{actionError}</p>}

      {data && (
        <AdminListSection title="Lista ról" total={data.total}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nazwa</th>
                <th>Uprawnienia</th>
                <th>Akcje</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((role) => (
                <tr key={role.id}>
                  <td>{role.id}</td>
                  <td>{role.name}</td>
                  <td>{role.permission_codes.join(', ') || '—'}</td>
                  <td>
                    <div className="admin-table-actions">
                      <Link to={`/admin/user/role/${role.id}`} className="btn-info">
                        Szczegóły
                      </Link>
                      <Link to={`/admin/user/role/${role.id}/edit`} className="btn-warning">
                        Edytuj
                      </Link>
                      <button className="btn-danger" onClick={() => void handleDelete(role.id, role.name)}>
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
