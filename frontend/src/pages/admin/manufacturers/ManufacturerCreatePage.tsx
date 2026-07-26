import { useNavigate } from 'react-router-dom'
import { createManufacturer, type ManufacturerFormValues } from '../../../api/manufacturers'
import { ManufacturerForm } from './ManufacturerForm'

const initialValues: ManufacturerFormValues = {
  name: '',
  description: '',
  is_description_ai_generated: false,
  image_url: '',
}

export function ManufacturerCreatePage() {
  const navigate = useNavigate()

  async function handleSubmit(values: ManufacturerFormValues) {
    await createManufacturer(values)
    navigate('/admin/manufacturer/list')
  }

  return (
    <section>
      <h1>Nowy producent</h1>
      <ManufacturerForm initialValues={initialValues} submitLabel="Utwórz" onSubmit={handleSubmit} />
    </section>
  )
}
