import { useCallback, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import {
  ORDER_STATUSES,
  deleteOrder,
  generateOrderSummary,
  listOrders,
  updateOrderStatus,
  type Order,
  type OrderListResponse,
} from '../../../api/orders'
import { usePaginatedList } from '../../../hooks/usePaginatedList'
import { Pagination } from '../../../components/Pagination'
import { AdminListSection } from '../../../components/admin/AdminListSection'

const PAGE_SIZES = ['5', '10', '20', '50', '100']

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

  async function handleMarkDelivered() {
    if (!window.confirm('Na pewno zmienić status na COMPLETED?')) return
    await handleStatusChange('completed')
  }

  async function handleDelete() {
    if (!window.confirm(`Na pewno usunąć zamówienie ${order.order_id}?`)) return
    await deleteOrder(order.id)
    onChanged()
  }

  return (
    <tr>
      <td>{order.id}</td>
      <td>{order.order_id}</td>
      <td>{order.user_id}</td>
      <td>{order.total_price}</td>
      <td>{order.currency}</td>
      <td>{order.payment_method_id}</td>
      <td>
        <select value={order.status.toLowerCase()} onChange={(e) => void handleStatusChange(e.target.value)}>
          {ORDER_STATUSES.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </td>
      <td>{order.created_at}</td>
      <td>{order.updated_at}</td>
      <td title={order.address ? `${order.address.address_line_1}, ${order.address.postal_code} ${order.address.city}` : undefined}>
        {order.address?.city ?? '—'}
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
        <div className="admin-table-actions">
          <button className="btn-danger" onClick={() => void handleDelete()}>
            Usuń
          </button>
          <button className="btn-info" onClick={() => void handleMarkDelivered()}>
            Dostarczono
          </button>
        </div>
        {error && <p role="alert">{error}</p>}
      </td>
    </tr>
  )
}

export function OrderListPage() {
  const [searchParams, setSearchParams] = useSearchParams()

  const page = Number(searchParams.get('page') ?? '1')
  const size = searchParams.get('size') ?? '10'
  const orderId = searchParams.get('order_id') ?? ''
  const userId = searchParams.get('user_id') ?? ''
  const status = searchParams.get('status') ?? ''
  const sortBy = searchParams.get('sort_by') ?? 'created_at'
  const sortDirection = searchParams.get('sort_direction') ?? 'desc'
  const totalPriceMin = searchParams.get('total_price_min') ?? ''
  const totalPriceMax = searchParams.get('total_price_max') ?? ''
  const createdAtMin = searchParams.get('created_at_min') ?? ''
  const createdAtMax = searchParams.get('created_at_max') ?? ''

  const [orderIdInput, setOrderIdInput] = useState(orderId)
  const [userIdInput, setUserIdInput] = useState(userId)
  const [statusInput, setStatusInput] = useState(status)
  const [sortByInput, setSortByInput] = useState(sortBy)
  const [sortDirectionInput, setSortDirectionInput] = useState(sortDirection)
  const [totalPriceMinInput, setTotalPriceMinInput] = useState(totalPriceMin)
  const [totalPriceMaxInput, setTotalPriceMaxInput] = useState(totalPriceMax)
  const [createdAtMinInput, setCreatedAtMinInput] = useState(createdAtMin)
  const [createdAtMaxInput, setCreatedAtMaxInput] = useState(createdAtMax)

  const fetcher = useCallback(
    (p: number): Promise<OrderListResponse> =>
      listOrders({
        page: p,
        size: Number(size),
        order_id: orderId || undefined,
        user_id: userId ? Number(userId) : undefined,
        status: status || undefined,
        sort_by: sortBy as 'created_at' | 'status',
        sort_direction: sortDirection as 'asc' | 'desc',
        total_price_min: totalPriceMin ? Number(totalPriceMin) : undefined,
        total_price_max: totalPriceMax ? Number(totalPriceMax) : undefined,
        created_at_min: createdAtMin || undefined,
        created_at_max: createdAtMax || undefined,
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [size, orderId, userId, status, sortBy, sortDirection, totalPriceMin, totalPriceMax, createdAtMin, createdAtMax],
  )
  const { data, isLoading, error, reload } = usePaginatedList(fetcher, page)

  function changePage(newPage: number) {
    const next = new URLSearchParams(searchParams)
    next.set('page', String(newPage))
    setSearchParams(next)
  }

  function applyFilters() {
    const next = new URLSearchParams()
    next.set('page', '1')
    next.set('size', size)
    if (orderIdInput) next.set('order_id', orderIdInput)
    if (userIdInput) next.set('user_id', userIdInput)
    if (statusInput) next.set('status', statusInput)
    next.set('sort_by', sortByInput)
    next.set('sort_direction', sortDirectionInput)
    if (totalPriceMinInput) next.set('total_price_min', totalPriceMinInput)
    if (totalPriceMaxInput) next.set('total_price_max', totalPriceMaxInput)
    if (createdAtMinInput) next.set('created_at_min', createdAtMinInput)
    if (createdAtMaxInput) next.set('created_at_max', createdAtMaxInput)
    setSearchParams(next)
  }

  function resetFilters() {
    setOrderIdInput('')
    setUserIdInput('')
    setStatusInput('')
    setSortByInput('created_at')
    setSortDirectionInput('desc')
    setTotalPriceMinInput('')
    setTotalPriceMaxInput('')
    setCreatedAtMinInput('')
    setCreatedAtMaxInput('')
    setSearchParams({ page: '1', size: '5' })
  }

  function changeSize(newSize: string) {
    const next = new URLSearchParams(searchParams)
    next.set('page', '1')
    next.set('size', newSize)
    setSearchParams(next)
  }

  return (
    <section>
      <div className="admin-page-header">
        <div>
          <h1>Zamówienia</h1>
          <p className="admin-subtitle">Przegląd wszystkich zamówień w panelu administracyjnym.</p>
        </div>
        <button className="btn-secondary" onClick={reload}>
          Odśwież
        </button>
      </div>

      {data && (
        <div className="admin-metric-cards">
          <div>
            <span>Łącznie zamówień</span>
            <strong>{data.total}</strong>
          </div>
          <div>
            <span>Strona</span>
            <strong>{data.page}</strong>
          </div>
          <div>
            <span>Na stronie</span>
            <strong>{data.size}</strong>
          </div>
          <div>
            <span>Wszystkie strony</span>
            <strong>{data.pages}</strong>
          </div>
        </div>
      )}

      <div className="admin-filters-card">
        <div className="admin-filters-card-header">
          <h3>Filtry i sortowanie</h3>
          <span className="admin-badge admin-badge--blue">Wyszukiwanie zamówień</span>
        </div>
        <div className="admin-filters-grid">
          <label>
            Order ID
            <input value={orderIdInput} onChange={(e) => setOrderIdInput(e.target.value)} placeholder="np. ORD-123" />
          </label>
          <label>
            User ID
            <input
              type="number"
              min={1}
              value={userIdInput}
              onChange={(e) => setUserIdInput(e.target.value)}
              placeholder="np. 1"
            />
          </label>
          <label>
            Status
            <select value={statusInput} onChange={(e) => setStatusInput(e.target.value)}>
              <option value="">Wszystkie</option>
              {ORDER_STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </label>
          <label>
            Sortuj po
            <select value={sortByInput} onChange={(e) => setSortByInput(e.target.value)}>
              <option value="created_at">Data stworzenia</option>
              <option value="status">Status</option>
            </select>
          </label>
          <label>
            Kierunek sortowania
            <select value={sortDirectionInput} onChange={(e) => setSortDirectionInput(e.target.value)}>
              <option value="desc">Malejąco</option>
              <option value="asc">Rosnąco</option>
            </select>
          </label>
          <label>
            Total price min
            <input
              type="number"
              step="0.01"
              min={0}
              value={totalPriceMinInput}
              onChange={(e) => setTotalPriceMinInput(e.target.value)}
              placeholder="np. 100"
            />
          </label>
          <label>
            Total price max
            <input
              type="number"
              step="0.01"
              min={0}
              value={totalPriceMaxInput}
              onChange={(e) => setTotalPriceMaxInput(e.target.value)}
              placeholder="np. 500"
            />
          </label>
          <label>
            Data stworzenia od
            <input type="datetime-local" value={createdAtMinInput} onChange={(e) => setCreatedAtMinInput(e.target.value)} />
          </label>
          <label>
            Data stworzenia do
            <input type="datetime-local" value={createdAtMaxInput} onChange={(e) => setCreatedAtMaxInput(e.target.value)} />
          </label>
        </div>
        <div className="admin-filters-actions">
          <button className="btn-primary" onClick={applyFilters}>
            Filtruj
          </button>
          <button className="btn-secondary" onClick={resetFilters}>
            Wyczyść filtry
          </button>
        </div>
      </div>

      {isLoading && <p>Ładowanie...</p>}
      {error && <p role="alert">{error}</p>}

      {data && (
        <AdminListSection title="Lista zamówień" total={data.total}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Order ID</th>
                <th>User ID</th>
                <th>Total Price</th>
                <th>Waluta</th>
                <th>Payment Method ID</th>
                <th>Status</th>
                <th>Data stworzenia</th>
                <th>Data zaktualizowania</th>
                <th>Adres</th>
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
          <div className="admin-pagination-footer">
            <span>
              Pokazano {data.orders.length} z {data.total} rekordów
            </span>
            <label className="admin-page-size">
              Na stronie:
              <select value={size} onChange={(e) => changeSize(e.target.value)}>
                {PAGE_SIZES.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </label>
            <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={changePage} />
          </div>
        </AdminListSection>
      )}
    </section>
  )
}
