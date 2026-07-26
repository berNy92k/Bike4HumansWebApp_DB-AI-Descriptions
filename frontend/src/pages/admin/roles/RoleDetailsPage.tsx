import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getRole, type Role } from '../../../api/roles'

export function RoleDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const [role, setRole] = useState<Role | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getRole(Number(id))
      .then(setRole)
      .catch(() => setError('Nie znaleziono roli.'))
  }, [id])

  if (error) return <p role="alert">{error}</p>
  if (!role) return <p>Ładowanie...</p>

  return (
    <section>
      <h1>{role.name}</h1>
      <p>{role.description ?? 'Brak opisu.'}</p>
      <p>Uprawnienia: {role.permission_codes.length > 0 ? role.permission_codes.join(', ') : '—'}</p>
      <Link to={`/admin/user/role/${role.id}/edit`}>Edytuj</Link>
      {' · '}
      <Link to="/admin/user/role/list">Wróć do listy</Link>
    </section>
  )
}
