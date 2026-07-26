import { useEffect, useState, type FormEvent } from 'react'
import type { BikeFormValues } from '../../../api/bikes'
import { autoTagBike, generateBikeDescription } from '../../../api/bikes'
import { listManufacturers, type Manufacturer } from '../../../api/manufacturers'
import { StatusBadge } from '../../../components/admin/StatusBadge'
import {
  BIKE_COLORS,
  BIKE_TYPES,
  BIKE_USAGES,
  BRAKE_TYPES,
  FRAME_MATERIALS,
  FRAME_SIZE_LABELS,
  SUSPENSION_TYPES,
  TARGET_USERS,
} from '../../../api/bikeEnums'

interface BikeFormProps {
  initialValues: BikeFormValues
  submitLabel: string
  onSubmit: (values: BikeFormValues) => Promise<void>
}

function OptionalSelect({
  label,
  value,
  options,
  onChange,
}: {
  label: string
  value: string | null
  options: string[]
  onChange: (value: string) => void
}) {
  return (
    <label>
      {label}
      <select value={value ?? ''} onChange={(e) => onChange(e.target.value)}>
        <option value="">—</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  )
}

function numberOrNull(value: string): number | null {
  return value === '' ? null : Number(value)
}

export function BikeForm({ initialValues, submitLabel, onSubmit }: BikeFormProps) {
  const [values, setValues] = useState(initialValues)
  const [manufacturers, setManufacturers] = useState<Manufacturer[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isGeneratingDescription, setIsGeneratingDescription] = useState(false)
  const [isAutoTagging, setIsAutoTagging] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    listManufacturers(1, 100)
      .then((response) => setManufacturers(response.items))
      .catch(() => setError('Nie udało się pobrać listy producentów.'))
  }, [])

  function set<K extends keyof BikeFormValues>(field: K, value: BikeFormValues[K]) {
    setValues((prev) => ({ ...prev, [field]: value }))
  }

  async function handleGenerateDescription() {
    setIsGeneratingDescription(true)
    setError(null)
    try {
      const response = await generateBikeDescription(values)
      setValues((prev) => ({ ...prev, description: response.description ?? prev.description, is_description_ai_generated: true }))
    } catch {
      setError('Nie udało się wygenerować opisu.')
    } finally {
      setIsGeneratingDescription(false)
    }
  }

  async function handleAutoTag() {
    if (!values.description) {
      setError('Auto-tagowanie wymaga wypełnionego opisu.')
      return
    }
    setIsAutoTagging(true)
    setError(null)
    try {
      const tags = await autoTagBike(values.name, values.description)
      setValues((prev) => ({
        ...prev,
        bike_type: tags.bike_type ?? prev.bike_type,
        frame_material: tags.frame_material ?? prev.frame_material,
        frame_size_label: tags.frame_size_label ?? prev.frame_size_label,
        brake_type: tags.brake_type ?? prev.brake_type,
        suspension_type: tags.suspension_type ?? prev.suspension_type,
        color: tags.color ?? prev.color,
        usage: tags.usage ?? prev.usage,
        target_user: tags.target_user ?? prev.target_user,
      }))
    } catch {
      setError('Nie udało się wygenerować tagów.')
    } finally {
      setIsAutoTagging(false)
    }
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setIsSubmitting(true)
    setError(null)
    try {
      await onSubmit(values)
    } catch {
      setError('Nie udało się zapisać roweru.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="admin-form">
      <label>
        Nazwa
        <input value={values.name} onChange={(e) => set('name', e.target.value)} required maxLength={255} />
      </label>

      <label>
        Producent
        <select value={values.brand_id || ''} onChange={(e) => set('brand_id', Number(e.target.value))} required>
          <option value="">— wybierz —</option>
          {manufacturers.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name}
            </option>
          ))}
        </select>
      </label>

      <label>
        Opis
        <textarea
          value={values.description ?? ''}
          onChange={(e) => {
            set('description', e.target.value)
            set('is_description_ai_generated', false)
          }}
          maxLength={2000}
          rows={4}
        />
      </label>
      <div className="admin-form-actions-inline">
        <button type="button" onClick={() => void handleGenerateDescription()} disabled={isGeneratingDescription || !values.name}>
          {isGeneratingDescription ? 'Generowanie...' : 'Wygeneruj opis AI'}
        </button>
        <button type="button" onClick={() => void handleAutoTag()} disabled={isAutoTagging || !values.name || !values.description}>
          {isAutoTagging ? 'Tagowanie...' : 'Auto-tag AI'}
        </button>
        <StatusBadge active={values.is_description_ai_generated} trueLabel="Wygenerowany przez AI" falseLabel="Wpisany ręcznie" />
      </div>

      <OptionalSelect label="Typ roweru" value={values.bike_type} options={BIKE_TYPES} onChange={(v) => set('bike_type', v)} />
      <OptionalSelect
        label="Materiał ramy"
        value={values.frame_material}
        options={FRAME_MATERIALS}
        onChange={(v) => set('frame_material', v)}
      />
      <label>
        Rozmiar ramy (cm)
        <input
          type="number"
          value={values.frame_size ?? ''}
          onChange={(e) => set('frame_size', numberOrNull(e.target.value))}
          min={0}
        />
      </label>
      <OptionalSelect
        label="Etykieta rozmiaru"
        value={values.frame_size_label}
        options={FRAME_SIZE_LABELS}
        onChange={(v) => set('frame_size_label', v)}
      />
      <label>
        Rozmiar kół (cale)
        <input
          type="number"
          value={values.wheel_size ?? ''}
          onChange={(e) => set('wheel_size', numberOrNull(e.target.value))}
          min={0}
        />
      </label>
      <label>
        Szerokość opon (mm)
        <input
          type="number"
          value={values.tire_width ?? ''}
          onChange={(e) => set('tire_width', numberOrNull(e.target.value))}
          min={0}
        />
      </label>
      <label>
        Liczba biegów
        <input
          type="number"
          value={values.gear_count ?? ''}
          onChange={(e) => set('gear_count', numberOrNull(e.target.value))}
          min={0}
        />
      </label>
      <OptionalSelect label="Hamulce" value={values.brake_type} options={BRAKE_TYPES} onChange={(v) => set('brake_type', v)} />
      <OptionalSelect
        label="Amortyzacja"
        value={values.suspension_type}
        options={SUSPENSION_TYPES}
        onChange={(v) => set('suspension_type', v)}
      />
      <OptionalSelect label="Kolor" value={values.color} options={BIKE_COLORS} onChange={(v) => set('color', v)} />
      <label>
        Waga (kg)
        <input
          type="number"
          step="0.01"
          value={values.weight_kg ?? ''}
          onChange={(e) => set('weight_kg', numberOrNull(e.target.value))}
          min={0}
        />
      </label>
      <label>
        Zalecany wzrost min (cm)
        <input
          type="number"
          value={values.recommended_height_min ?? ''}
          onChange={(e) => set('recommended_height_min', numberOrNull(e.target.value))}
          min={0}
        />
      </label>
      <label>
        Zalecany wzrost max (cm)
        <input
          type="number"
          value={values.recommended_height_max ?? ''}
          onChange={(e) => set('recommended_height_max', numberOrNull(e.target.value))}
          min={0}
        />
      </label>
      <OptionalSelect label="Przeznaczenie" value={values.usage} options={BIKE_USAGES} onChange={(v) => set('usage', v)} />
      <OptionalSelect
        label="Dla kogo"
        value={values.target_user}
        options={TARGET_USERS}
        onChange={(v) => set('target_user', v)}
      />

      <label>
        Cena (PLN)
        <input
          type="number"
          step="0.01"
          value={values.price}
          onChange={(e) => set('price', Number(e.target.value))}
          required
          min={0.01}
        />
      </label>
      <label>
        Stan magazynowy
        <input
          type="number"
          value={values.stock_quantity}
          onChange={(e) => set('stock_quantity', Number(e.target.value))}
          required
          min={0}
        />
      </label>
      <label>
        URL zdjęcia
        <input value={values.image_url ?? ''} onChange={(e) => set('image_url', e.target.value)} maxLength={500} />
      </label>
      {values.image_url && (
        <div className="admin-form-image-preview">
          <img src={values.image_url} alt="Podgląd zdjęcia roweru" />
        </div>
      )}
      <label className="admin-form-checkbox">
        <input type="checkbox" checked={values.is_active} onChange={(e) => set('is_active', e.target.checked)} />
        Aktywny
      </label>

      {error && <p role="alert">{error}</p>}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Zapisywanie...' : submitLabel}
      </button>
    </form>
  )
}
