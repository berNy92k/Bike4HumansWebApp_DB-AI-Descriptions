import { useState, type FormEvent } from 'react'
import type { ManufacturerFormValues } from '../../../api/manufacturers'
import { generateManufacturerDescription } from '../../../api/manufacturers'

interface ManufacturerFormProps {
  initialValues: ManufacturerFormValues
  submitLabel: string
  onSubmit: (values: ManufacturerFormValues) => Promise<void>
}

export function ManufacturerForm({ initialValues, submitLabel, onSubmit }: ManufacturerFormProps) {
  const [values, setValues] = useState(initialValues)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isGeneratingDescription, setIsGeneratingDescription] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleGenerateDescription() {
    setIsGeneratingDescription(true)
    setError(null)
    try {
      const response = await generateManufacturerDescription(values.name, values.description)
      setValues((prev) => ({ ...prev, description: response.description ?? prev.description, is_description_ai_generated: true }))
    } catch {
      setError('Nie udało się wygenerować opisu.')
    } finally {
      setIsGeneratingDescription(false)
    }
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setIsSubmitting(true)
    setError(null)
    try {
      await onSubmit(values)
    } catch {
      setError('Nie udało się zapisać producenta.')
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
          maxLength={255}
        />
      </label>
      <label>
        Opis
        <textarea
          value={values.description ?? ''}
          onChange={(e) =>
            setValues((prev) => ({ ...prev, description: e.target.value, is_description_ai_generated: false }))
          }
          maxLength={2000}
          rows={4}
        />
      </label>
      <button type="button" onClick={() => void handleGenerateDescription()} disabled={isGeneratingDescription || !values.name}>
        {isGeneratingDescription ? 'Generowanie...' : 'Wygeneruj opis AI'}
      </button>
      {values.is_description_ai_generated && <span className="ai-badge">Opis wygenerowany przez AI</span>}

      <label>
        URL zdjęcia
        <input
          value={values.image_url ?? ''}
          onChange={(e) => setValues((prev) => ({ ...prev, image_url: e.target.value }))}
          maxLength={500}
        />
      </label>

      {error && <p role="alert">{error}</p>}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Zapisywanie...' : submitLabel}
      </button>
    </form>
  )
}
