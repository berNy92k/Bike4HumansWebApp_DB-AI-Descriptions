import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getRole, updateRole, type RoleFormValues } from '../../../api/roles'
import { RoleForm } from './RoleForm'

export function RoleEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [initialValues, setInitialValues] = useState<RoleFormValues | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getRole(Number(id))
      .then((role) =>
        setInitialValues({ name: role.name, description: role.description ?? '', permission_codes: role.permission_codes }),
      )
      .catch(() => setError('Nie znaleziono roli.'))
  }, [id])

  async function handleSubmit(values: RoleFormValues) {
    await updateRole(Number(id), values)
    navigate('/admin/user/role/list')
  }

  if (error) return <p role="alert">{error}</p>
  if (!initialValues) return <p>Ładowanie...</p>

  return (
    <section>
      <h1>Edytuj rolę</h1>
      <RoleForm initialValues={initialValues} submitLabel="Zapisz" onSubmit={handleSubmit} />
    </section>
  )
}
