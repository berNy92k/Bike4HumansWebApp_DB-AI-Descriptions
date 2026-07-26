import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getManufacturer, updateManufacturer, type ManufacturerFormValues } from '../../../api/manufacturers'
import { ManufacturerForm } from './ManufacturerForm'

export function ManufacturerEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [initialValues, setInitialValues] = useState<ManufacturerFormValues | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getManufacturer(Number(id))
      .then((manufacturer) =>
        setInitialValues({
          name: manufacturer.name,
          description: manufacturer.description,
          is_description_ai_generated: manufacturer.is_description_ai_generated,
          image_url: manufacturer.image_url,
        }),
      )
      .catch(() => setError('Nie znaleziono producenta.'))
  }, [id])

  async function handleSubmit(values: ManufacturerFormValues) {
    await updateManufacturer(Number(id), values)
    navigate('/admin/manufacturer/list')
  }

  if (error) return <p role="alert">{error}</p>
  if (!initialValues) return <p>Ładowanie...</p>

  return (
    <section>
      <h1>Edytuj producenta</h1>
      <ManufacturerForm initialValues={initialValues} submitLabel="Zapisz" onSubmit={handleSubmit} />
    </section>
  )
}
