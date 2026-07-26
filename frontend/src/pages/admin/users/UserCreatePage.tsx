import { useEffect, useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { createUser, type UserCreateValues } from '../../../api/users'
import { listRoles, type Role } from '../../../api/roles'

const initialValues: UserCreateValues = {
  username: '',
  email: '',
  name: '',
  surname: '',
  password: '',
  is_active: true,
  email_verified: true,
  role_id: 0,
}

export function UserCreatePage() {
  const navigate = useNavigate()
  const [values, setValues] = useState(initialValues)
  const [roles, setRoles] = useState<Role[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    listRoles(1, 100)
      .then((response) => setRoles(response.items))
      .catch(() => setError('Nie udało się pobrać listy ról.'))
  }, [])

  function set<K extends keyof UserCreateValues>(field: K, value: UserCreateValues[K]) {
    setValues((prev) => ({ ...prev, [field]: value }))
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setIsSubmitting(true)
    setError(null)
    try {
      await createUser(values)
      navigate('/admin/user/list')
    } catch {
      setError('Nie udało się utworzyć użytkownika (sprawdź uprawnienia do wybranej roli).')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section>
      <h1>Nowy użytkownik</h1>
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
          Hasło
          <input
            type="password"
            value={values.password}
            onChange={(e) => set('password', e.target.value)}
            required
            minLength={5}
            maxLength={30}
          />
        </label>
        <label>
          Rola
          <select value={values.role_id || ''} onChange={(e) => set('role_id', Number(e.target.value))} required>
            <option value="">— wybierz —</option>
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
          {isSubmitting ? 'Zapisywanie...' : 'Utwórz'}
        </button>
      </form>
    </section>
  )
}
