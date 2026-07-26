import { useNavigate } from 'react-router-dom'
import { createRole, type RoleFormValues } from '../../../api/roles'
import { RoleForm } from './RoleForm'

const initialValues: RoleFormValues = { name: '', description: '', permission_codes: [] }

export function RoleCreatePage() {
  const navigate = useNavigate()

  async function handleSubmit(values: RoleFormValues) {
    await createRole(values)
    navigate('/admin/user/role/list')
  }

  return (
    <section>
      <h1>Nowa rola</h1>
      <RoleForm initialValues={initialValues} submitLabel="Utwórz" onSubmit={handleSubmit} />
    </section>
  )
}
