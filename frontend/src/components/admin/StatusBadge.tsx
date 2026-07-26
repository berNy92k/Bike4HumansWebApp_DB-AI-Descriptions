interface StatusBadgeProps {
  active: boolean
  trueLabel?: string
  falseLabel?: string
}

export function StatusBadge({ active, trueLabel = 'Tak', falseLabel = 'Nie' }: StatusBadgeProps) {
  return <span className={`status-badge ${active ? 'status-badge--success' : 'status-badge--danger'}`}>{active ? trueLabel : falseLabel}</span>
}

const STATUS_TONE: Record<string, 'success' | 'danger' | 'neutral' | 'info'> = {
  COMPLETED: 'success',
  DELIVERY: 'info',
  PENDING: 'neutral',
  CANCELED: 'danger',
  FAILED: 'danger',
}

export function TextStatusBadge({ status }: { status: string }) {
  const tone = STATUS_TONE[status.toUpperCase()] ?? 'neutral'
  return <span className={`status-badge status-badge--${tone}`}>{status}</span>
}
