import { useNavigate } from 'react-router-dom'
import { createBike, emptyBikeForm, type BikeFormValues } from '../../../api/bikes'
import { BikeForm } from './BikeForm'

export function BikeCreatePage() {
  const navigate = useNavigate()

  async function handleSubmit(values: BikeFormValues) {
    await createBike(values)
    navigate('/admin/bikes/list')
  }

  return (
    <section>
      <h1>Nowy rower</h1>
      <BikeForm initialValues={emptyBikeForm} submitLabel="Utwórz" onSubmit={handleSubmit} />
    </section>
  )
}
