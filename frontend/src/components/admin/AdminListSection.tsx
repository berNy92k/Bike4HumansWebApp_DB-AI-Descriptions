import type { ReactNode } from 'react'

interface AdminListSectionProps {
  title: string
  total: number
  children: ReactNode
}

export function AdminListSection({ title, total, children }: AdminListSectionProps) {
  return (
    <div className="admin-list-card">
      <div className="admin-list-card-header">
        <h3>{title}</h3>
        <span className="admin-count-badge">{total} rekordów</span>
      </div>
      {children}
    </div>
  )
}
