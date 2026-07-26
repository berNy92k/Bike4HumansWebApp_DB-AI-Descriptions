import { useCallback, useState } from 'react'
import { ORDER_STATUSES, deleteOrder, generateOrderSummary, listOrders, updateOrderStatus, type Order } from '../../../api/orders'
import { usePaginatedList } from '../../../hooks/usePaginatedList'
import { Pagination } from '../../../components/Pagination'
import { AdminListSection } from '../../../components/admin/AdminListSection'

function OrderRow({ order, onChanged }: { order: Order; onChanged: () => void }) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [summary, setSummary] = useState(order.ai_summary)
  const [error, setError] = useState<string | null>(null)

  async function handleGenerateSummary() {
    setIsGenerating(true)
    setError(null)
    try {
      const response = await generateOrderSummary(order.id)
      setSummary(response.summary)
    } catch {
      setError('Nie udało się wygenerować podsumowania.')
    } finally {
      setIsGenerating(false)
    }
  }

  async function handleStatusChange(status: string) {
    setError(null)
    try {
      await updateOrderStatus(order.id, status)
      onChanged()
    } catch {
      setError('Nie udało się zmienić statusu.')
    }
  }

  async function handleDelete() {
    if (!window.confirm(`Na pewno usunąć zamówienie ${order.order_id}?`)) return
    await deleteOrder(order.id)
    onChanged()
  }

  return (
    <tr>
      <td>{order.order_id}</td>
      <td>{order.user_id}</td>
      <td>{order.total_price} PLN</td>
      <td>
        <select value={order.status.toLowerCase()} onChange={(e) => void handleStatusChange(e.target.value)}>
          {ORDER_STATUSES.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </td>
      <td>
        {summary ?? <em>brak</em>}
        <div>
          <button onClick={() => void handleGenerateSummary()} disabled={isGenerating}>
            {isGenerating ? 'Generowanie...' : 'Wygeneruj podsumowanie AI'}
          </button>
        </div>
      </td>
      <td>
        <button className="btn-danger" onClick={() => void handleDelete()}>
          Usuń
        </button>
        {error && <p role="alert">{error}</p>}
      </td>
    </tr>
  )
}

export function OrderListPage() {
  const [page, setPage] = useState(1)
  const fetcher = useCallback((p: number) => listOrders(p), [])
  const { data, isLoading, error, reload } = usePaginatedList(fetcher, page)

  return (
    <section>
      <div className="admin-page-header">
        <h1>Zamówienia</h1>
      </div>

      {isLoading && <p>Ładowanie...</p>}
      {error && <p role="alert">{error}</p>}

      {data && (
        <AdminListSection title="Lista zamówień" total={data.total}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>Nr zamówienia</th>
                <th>Użytkownik</th>
                <th>Wartość</th>
                <th>Status</th>
                <th>Podsumowanie AI</th>
                <th>Akcje</th>
              </tr>
            </thead>
            <tbody>
              {data.orders.map((order) => (
                <OrderRow key={order.id} order={order} onChanged={reload} />
              ))}
            </tbody>
          </table>
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        </AdminListSection>
      )}
    </section>
  )
}
