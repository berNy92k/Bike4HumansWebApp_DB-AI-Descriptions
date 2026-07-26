import { useCallback, useState } from 'react'
import { deleteCart, generateCartSummary, listCarts, type AdminCart } from '../../../api/carts'
import { usePaginatedList } from '../../../hooks/usePaginatedList'
import { Pagination } from '../../../components/Pagination'
import { AdminListSection } from '../../../components/admin/AdminListSection'
import { TextStatusBadge } from '../../../components/admin/StatusBadge'

function CartRow({ cart, onChanged }: { cart: AdminCart; onChanged: () => void }) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [summary, setSummary] = useState(cart.ai_summary)
  const [error, setError] = useState<string | null>(null)

  async function handleGenerateSummary() {
    setIsGenerating(true)
    setError(null)
    try {
      const response = await generateCartSummary(cart.id)
      setSummary(response.summary)
    } catch {
      setError('Nie udało się wygenerować podsumowania.')
    } finally {
      setIsGenerating(false)
    }
  }

  async function handleDelete() {
    if (!window.confirm(`Na pewno usunąć koszyk #${cart.id}?`)) return
    await deleteCart(cart.id)
    onChanged()
  }

  return (
    <tr>
      <td>{cart.id}</td>
      <td>{cart.user_id}</td>
      <td>
        <TextStatusBadge status={cart.status} />
      </td>
      <td>{cart.items.length}</td>
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

export function CartListPage() {
  const [page, setPage] = useState(1)
  const fetcher = useCallback((p: number) => listCarts(p), [])
  const { data, isLoading, error, reload } = usePaginatedList(fetcher, page)

  return (
    <section>
      <div className="admin-page-header">
        <h1>Koszyki</h1>
      </div>

      {isLoading && <p>Ładowanie...</p>}
      {error && <p role="alert">{error}</p>}

      {data && (
        <AdminListSection title="Lista koszyków" total={data.total}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Użytkownik</th>
                <th>Status</th>
                <th>Pozycje</th>
                <th>Podsumowanie AI</th>
                <th>Akcje</th>
              </tr>
            </thead>
            <tbody>
              {data.carts.map((cart) => (
                <CartRow key={cart.id} cart={cart} onChanged={reload} />
              ))}
            </tbody>
          </table>
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        </AdminListSection>
      )}
    </section>
  )
}
