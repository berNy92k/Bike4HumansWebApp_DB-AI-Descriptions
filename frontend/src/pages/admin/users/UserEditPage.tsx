import { useEffect, useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getUser, updateUser, type UserUpdateValues } from '../../../api/users'
import { listRoles, type Role } from '../../../api/roles'

export function UserEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [values, setValues] = useState<UserUpdateValues | null>(null)
  const [roles, setRoles] = useState<Role[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([getUser(Number(id)), listRoles(1, 100)])
      .then(([user, roleList]) => {
        setValues({
          username: user.username,
          email: user.email,
          name: user.name,
          surname: user.surname,
          role_id: user.role_id,
          is_active: user.is_active,
          email_verified: user.email_verified,
        })
        setRoles(roleList.items)
      })
      .catch(() => setError('Nie znaleziono użytkownika.'))
  }, [id])

  function set<K extends keyof UserUpdateValues>(field: K, value: UserUpdateValues[K]) {
    setValues((prev) => (prev ? { ...prev, [field]: value } : prev))
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!values) return
    setIsSubmitting(true)
    setError(null)
    try {
      await updateUser(Number(id), values)
      navigate('/admin/user/list')
    } catch {
      setError('Nie udało się zapisać użytkownika (sprawdź uprawnienia do wybranej roli).')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (error && !values) return <p role="alert">{error}</p>
  if (!values) return <p>Ładowanie...</p>

  return (
    <section>
      <h1>Edytuj użytkownika</h1>
      <form onSubmit={handleSubmit} className="admin-form">
        <label>
          Login
          <input value={values.username} onChange={(e) => set('username', e.target.value)} required minLength={3} maxLength={30} />
        </label>
        <label>
          E-mail
          <input value={values.email} onChange={(e) => set('email', e.target.value)} required minLength={3} maxLength={30} />
        </label>
        <label>
          Imię
          <input value={values.name} onChange={(e) => set('name', e.target.value)} required minLength={3} maxLength={30} />
        </label>
        <label>
          Nazwisko
          <input value={values.surname} onChange={(e) => set('surname', e.target.value)} required minLength={3} maxLength={30} />
        </label>
        <label>
          Rola
          <select value={values.role_id} onChange={(e) => set('role_id', Number(e.target.value))} required>
            {roles.map((role) => (
              <option key={role.id} value={role.id}>
                {role.name}
              </option>
            ))}
          </select>
        </label>
        <label className="admin-form-checkbox">
          <input type="checkbox" checked={values.is_active} onChange={(e) => set('is_active', e.target.checked)} />
          Aktywny
        </label>
        <label className="admin-form-checkbox">
          <input type="checkbox" checked={values.email_verified} onChange={(e) => set('email_verified', e.target.checked)} />
          E-mail zweryfikowany
        </label>

        {error && <p role="alert">{error}</p>}
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Zapisywanie...' : 'Zapisz'}
        </button>
      </form>
    </section>
  )
}
