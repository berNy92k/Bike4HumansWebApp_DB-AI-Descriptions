import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getBike, updateBike, type Bike, type BikeFormValues } from '../../../api/bikes'
import { BikeForm } from './BikeForm'

function toFormValues(bike: Bike): BikeFormValues {
  const { id: _id, created_at: _createdAt, updated_at: _updatedAt, ...form } = bike
  return form
}

export function BikeEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [initialValues, setInitialValues] = useState<BikeFormValues | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getBike(Number(id))
      .then((bike) => setInitialValues(toFormValues(bike)))
      .catch(() => setError('Nie znaleziono roweru.'))
  }, [id])

  async function handleSubmit(values: BikeFormValues) {
    await updateBike(Number(id), values)
    navigate('/admin/bikes/list')
  }

  if (error) return <p role="alert">{error}</p>
  if (!initialValues) return <p>Ładowanie...</p>

  return (
    <section>
      <h1>Edytuj rower</h1>
      <BikeForm initialValues={initialValues} submitLabel="Zapisz" onSubmit={handleSubmit} />
    </section>
  )
}
