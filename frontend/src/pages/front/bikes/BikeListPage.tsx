import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { listPublicBikes, searchBikesWithAi } from '../../../api/frontCatalog'
import type { BikeListResponse } from '../../../api/bikes'
import { Pagination } from '../../../components/Pagination'
import { BIKE_TYPES, BIKE_USAGES, TARGET_USERS } from '../../../api/bikeEnums'

export function BikeListPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [data, setData] = useState<BikeListResponse | null>(null)
  const [aiQuery, setAiQuery] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const page = Number(searchParams.get('page') ?? '1')
  const bikeType = searchParams.get('bike_type') ?? ''
  const usage = searchParams.get('usage') ?? ''
  const targetUser = searchParams.get('target_user') ?? ''
  const priceMin = searchParams.get('price_min') ?? ''
  const priceMax = searchParams.get('price_max') ?? ''

  useEffect(() => {
    listPublicBikes({
      page,
      size: 16,
      bike_type: bikeType || undefined,
      usage: usage || undefined,
      target_user: targetUser || undefined,
      price_min: priceMin ? Number(priceMin) : undefined,
      price_max: priceMax ? Number(priceMax) : undefined,
    }).then(setData)
  }, [page, bikeType, usage, targetUser, priceMin, priceMax])

  function updateFilter(key: string, value: string) {
    const next = new URLSearchParams(searchParams)
    if (value) next.set(key, value)
    else next.delete(key)
    next.set('page', '1')
    setSearchParams(next)
  }

  function changePage(newPage: number) {
    const next = new URLSearchParams(searchParams)
    next.set('page', String(newPage))
    setSearchParams(next)
  }

  async function handleAiSearch() {
    if (!aiQuery.trim()) {
      setError('Opisz najpierw, czego szukasz.')
      return
    }
    setIsSearching(true)
    setError(null)
    try {
      const filters = await searchBikesWithAi(aiQuery)
      const next = new URLSearchParams()
      next.set('page', '1')
      if (filters.bike_type) next.set('bike_type', filters.bike_type)
      if (filters.usage) next.set('usage', filters.usage)
      if (filters.target_user) next.set('target_user', filters.target_user)
      if (filters.price_min != null) next.set('price_min', String(filters.price_min))
      if (filters.price_max != null) next.set('price_max', String(filters.price_max))
      setSearchParams(next)
    } catch {
      setError('Nie udało się przetworzyć zapytania.')
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <main>
      <span className="page-eyebrow">Katalog</span>
      <h1>Rowery</h1>

      <div className="ai-search-box">
        <label htmlFor="ai-search-input">Opisz czego szukasz</label>
        <div className="ai-search-row">
          <input
            id="ai-search-input"
            value={aiQuery}
            onChange={(e) => setAiQuery(e.target.value)}
            placeholder="Np. szukam czegoś do miasta do 3000 zł"
          />
          <button onClick={() => void handleAiSearch()} disabled={isSearching}>
            {isSearching ? 'Szukam...' : 'Szukaj z AI'}
          </button>
          {(bikeType || usage || targetUser || priceMin || priceMax) && (
            <button onClick={() => setSearchParams({ page: '1' })}>Wyczyść filtry</button>
          )}
        </div>
        {error && <p role="alert">{error}</p>}
      </div>

      <div className="filter-bar">
        <label>
          Typ
          <select value={bikeType} onChange={(e) => updateFilter('bike_type', e.target.value)}>
            <option value="">Wszystkie</option>
            {BIKE_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </label>
        <label>
          Przeznaczenie
          <select value={usage} onChange={(e) => updateFilter('usage', e.target.value)}>
            <option value="">Wszystkie</option>
            {BIKE_USAGES.map((u) => (
              <option key={u} value={u}>
                {u}
              </option>
            ))}
          </select>
        </label>
        <label>
          Dla kogo
          <select value={targetUser} onChange={(e) => updateFilter('target_user', e.target.value)}>
            <option value="">Wszyscy</option>
            {TARGET_USERS.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </label>
      </div>

      {data && data.items.length === 0 && (
        <p>
          Brak rowerów spełniających wybrane kryteria. <Link to="/bikes">Wyczyść filtry</Link>.
        </p>
      )}

      {data && data.items.length > 0 && (
        <>
          <div className="bike-grid">
            {data.items.map((bike) => (
              <Link key={bike.id} to={`/bikes/${bike.id}`} className="bike-card">
                <div className="bike-card-image">{bike.image_url && <img src={bike.image_url} alt={bike.name} />}</div>
                <h3>{bike.name}</h3>
                <p>{bike.description ? bike.description.slice(0, 90) : ''}</p>
                <div className="bike-card-footer">
                  <strong>{bike.price} zł</strong>
                  <span>{bike.bike_type ?? '—'}</span>
                </div>
              </Link>
            ))}
          </div>
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={changePage} />
        </>
      )}
    </main>
  )
}
