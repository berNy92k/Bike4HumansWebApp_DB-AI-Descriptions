import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../../api/auth'
import { ApiError } from '../../api/apiClient'

const initialForm = { username: '', email: '', name: '', surname: '', password: '' }

export function RegisterPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  function updateField(field: keyof typeof initialForm) {
    return (event: React.ChangeEvent<HTMLInputElement>) =>
      setForm((prev) => ({ ...prev, [field]: event.target.value }))
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
      await register(form)
      navigate('/auth/login', { replace: true })
    } catch (err) {
      setError(err instanceof ApiError ? 'Nie udało się utworzyć konta. Sprawdź dane.' : 'Wystąpił błąd. Spróbuj ponownie.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="auth-page">
      <h1>Zarejestruj się</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Login
          <input value={form.username} onChange={updateField('username')} required minLength={3} maxLength={30} autoFocus />
        </label>
        <label>
          E-mail
          <input type="email" value={form.email} onChange={updateField('email')} required minLength={3} maxLength={30} />
        </label>
        <label>
          Imię
          <input value={form.name} onChange={updateField('name')} required minLength={3} maxLength={30} />
        </label>
        <label>
          Nazwisko
          <input value={form.surname} onChange={updateField('surname')} required minLength={3} maxLength={30} />
        </label>
        <label>
          Hasło
          <input type="password" value={form.password} onChange={updateField('password')} required minLength={5} maxLength={30} />
        </label>
        {error && <p role="alert">{error}</p>}
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Tworzenie konta...' : 'Zarejestruj się'}
        </button>
      </form>
      <p>
        Masz już konto? <Link to="/auth/login">Zaloguj się</Link>
      </p>
    </main>
  )
}
