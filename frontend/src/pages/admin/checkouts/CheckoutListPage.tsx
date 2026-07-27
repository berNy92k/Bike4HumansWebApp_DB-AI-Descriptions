import { useCallback, useState } from 'react'
import { deleteCheckout, generateCheckoutSummary, listCheckouts, type Checkout } from '../../../api/checkouts'
import { usePaginatedList } from '../../../hooks/usePaginatedList'
import { Pagination } from '../../../components/Pagination'
import { AdminListSection } from '../../../components/admin/AdminListSection'
import { TextStatusBadge } from '../../../components/admin/StatusBadge'

function CheckoutRow({ checkout, onChanged }: { checkout: Checkout; onChanged: () => void }) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [summary, setSummary] = useState(checkout.ai_summary)
  const [error, setError] = useState<string | null>(null)

  async function handleGenerateSummary() {
    setIsGenerating(true)
    setError(null)
    try {
      const response = await generateCheckoutSummary(checkout.id)
      setSummary(response.summary)
    } catch {
      setError('Nie udało się wygenerować podsumowania.')
    } finally {
      setIsGenerating(false)
    }
  }

  async function handleDelete() {
    if (!window.confirm(`Na pewno usunąć checkout #${checkout.id}?`)) return
    await deleteCheckout(checkout.id)
    onChanged()
  }

  return (
    <tr>
      <td>{checkout.id}</td>
      <td>{checkout.user_id}</td>
      <td>{checkout.total_price} PLN</td>
      <td>
        <TextStatusBadge status={checkout.status} />
      </td>
      <td title={checkout.address ? `${checkout.address.address_line_1}, ${checkout.address.postal_code} ${checkout.address.city}` : undefined}>
        {checkout.address?.city ?? '—'}
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

export function CheckoutListPage() {
  const [page, setPage] = useState(1)
  const fetcher = useCallback((p: number) => listCheckouts(p), [])
  const { data, isLoading, error, reload } = usePaginatedList(fetcher, page)

  return (
    <section>
      <div className="admin-page-header">
        <h1>Checkouty</h1>
      </div>

      {isLoading && <p>Ładowanie...</p>}
      {error && <p role="alert">{error}</p>}

      {data && (
        <AdminListSection title="Lista checkoutów" total={data.total}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Użytkownik</th>
                <th>Wartość</th>
                <th>Status</th>
                <th>Adres</th>
                <th>Podsumowanie AI</th>
                <th>Akcje</th>
              </tr>
            </thead>
            <tbody>
              {data.checkouts.map((checkout) => (
                <CheckoutRow key={checkout.id} checkout={checkout} onChanged={reload} />
              ))}
            </tbody>
          </table>
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        </AdminListSection>
      )}
    </section>
  )
}
