import { useCallback, useState } from 'react'
import { Link } from 'react-router-dom'
import { deleteUser, listUsers } from '../../../api/users'
import { usePaginatedList } from '../../../hooks/usePaginatedList'
import { Pagination } from '../../../components/Pagination'
import { AdminListSection } from '../../../components/admin/AdminListSection'
import { StatusBadge } from '../../../components/admin/StatusBadge'

export function UserListPage() {
  const [page, setPage] = useState(1)
  const fetcher = useCallback((p: number) => listUsers(p), [])
  const { data, isLoading, error, reload } = usePaginatedList(fetcher, page)

  async function handleDelete(id: number, username: string) {
    if (!window.confirm(`Na pewno usunąć użytkownika "${username}"?`)) return
    await deleteUser(id)
    reload()
  }

  return (
    <section>
      <div className="admin-page-header">
        <h1>Użytkownicy</h1>
        <Link to="/admin/user/create" className="btn-primary">
          Nowy użytkownik
        </Link>
      </div>

      {isLoading && <p>Ładowanie...</p>}
      {error && <p role="alert">{error}</p>}

      {data && (
        <AdminListSection title="Lista użytkowników" total={data.total}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Login</th>
                <th>E-mail</th>
                <th>Aktywny</th>
                <th>Akcje</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>
                    <StatusBadge active={user.is_active} />
                  </td>
                  <td>
                    <div className="admin-table-actions">
                      <Link to={`/admin/user/${user.id}/details`} className="btn-info">
                        Szczegóły
                      </Link>
                      <Link to={`/admin/user/${user.id}/edit`} className="btn-warning">
                        Edytuj
                      </Link>
                      <button className="btn-danger" onClick={() => void handleDelete(user.id, user.username)}>
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
