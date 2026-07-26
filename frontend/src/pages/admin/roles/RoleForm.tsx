import { useState, type FormEvent } from 'react'
import { PERMISSION_CODES, type RoleFormValues } from '../../../api/roles'

interface RoleFormProps {
  initialValues: RoleFormValues
  submitLabel: string
  onSubmit: (values: RoleFormValues) => Promise<void>
}

export function RoleForm({ initialValues, submitLabel, onSubmit }: RoleFormProps) {
  const [values, setValues] = useState(initialValues)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  function togglePermission(code: string, checked: boolean) {
    setValues((prev) => ({
      ...prev,
      permission_codes: checked ? [...prev.permission_codes, code] : prev.permission_codes.filter((c) => c !== code),
    }))
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setIsSubmitting(true)
    setError(null)
    try {
      await onSubmit(values)
    } catch {
      setError('Nie udało się zapisać roli (może brakować uprawnień super admina).')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="admin-form">
      <label>
        Nazwa
        <input
          value={values.name}
          onChange={(e) => setValues((prev) => ({ ...prev, name: e.target.value }))}
          required
          minLength={3}
          maxLength={20}
        />
      </label>
      <label>
        Opis
        <input
          value={values.description}
          onChange={(e) => setValues((prev) => ({ ...prev, description: e.target.value }))}
          required
          minLength={5}
          maxLength={200}
        />
      </label>
      <fieldset>
        <legend>Uprawnienia</legend>
        {PERMISSION_CODES.map((code) => (
          <label key={code} className="admin-form-checkbox">
            <input
              type="checkbox"
              checked={values.permission_codes.includes(code)}
              onChange={(e) => togglePermission(code, e.target.checked)}
            />
            {code}
          </label>
        ))}
      </fieldset>

      {error && <p role="alert">{error}</p>}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Zapisywanie...' : submitLabel}
      </button>
    </form>
  )
}
