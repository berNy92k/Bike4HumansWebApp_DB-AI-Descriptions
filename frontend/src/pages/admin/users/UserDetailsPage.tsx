import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getUser, type UserDetails } from '../../../api/users'
import { StatusBadge } from '../../../components/admin/StatusBadge'

export function UserDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const [user, setUser] = useState<UserDetails | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getUser(Number(id))
      .then(setUser)
      .catch(() => setError('Nie znaleziono użytkownika.'))
  }, [id])

  if (error) return <p role="alert">{error}</p>
  if (!user) return <p>Ładowanie...</p>

  return (
    <section>
      <h1>{user.username}</h1>
      <dl className="admin-details-grid">
        <dt>Imię i nazwisko</dt>
        <dd>
          {user.name} {user.surname}
        </dd>
        <dt>E-mail</dt>
        <dd>{user.email}</dd>
        <dt>Rola</dt>
        <dd>{user.role_name}</dd>
        <dt>Aktywny</dt>
        <dd>
          <StatusBadge active={user.is_active} />
        </dd>
        <dt>E-mail zweryfikowany</dt>
        <dd>
          <StatusBadge active={user.email_verified} />
        </dd>
        <dt>Ostatnie logowanie</dt>
        <dd>{user.last_login ?? '—'}</dd>
      </dl>
      <Link to={`/admin/user/${user.id}/edit`}>Edytuj</Link>
      {' · '}
      <Link to="/admin/user/list">Wróć do listy</Link>
    </section>
  )
}
