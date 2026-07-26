import { useEffect, useState } from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { apiClient } from '../api/apiClient'

type Status = 'checking' | 'allowed' | 'denied'

// Admin-panel access is granted per role via a DB-configurable permission
// (PermissionCode.ADMIN_PANEL_ACCESS, see app/services/auth/auth_service.py:get_current_admin_user),
// not a fixed set of role ids, so this cannot be decided from the JWT alone. It's confirmed here
// with a cheap probe request against an existing admin-only endpoint; the backend remains the
// actual security boundary regardless of what this component decides.
export function RequireAdmin() {
  const [status, setStatus] = useState<Status>('checking')

  useEffect(() => {
    let cancelled = false

    apiClient
      .get('/admin/user/roles?page=1&size=1')
      .then(() => {
        if (!cancelled) setStatus('allowed')
      })
      .catch(() => {
        if (!cancelled) setStatus('denied')
      })

    return () => {
      cancelled = true
    }
  }, [])

  if (status === 'checking') return null
  if (status === 'denied') return <Navigate to="/" replace />

  return <Outlet />
}
