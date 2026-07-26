import { useCallback, useEffect, useState } from 'react'

export function usePaginatedList<T>(fetcher: (page: number) => Promise<T>, page: number) {
  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [reloadToken, setReloadToken] = useState(0)

  const reload = useCallback(() => setReloadToken((t) => t + 1), [])

  useEffect(() => {
    let cancelled = false
    setIsLoading(true)
    setError(null)

    fetcher(page)
      .then((result) => {
        if (!cancelled) setData(result)
      })
      .catch(() => {
        if (!cancelled) setError('Nie udało się pobrać danych.')
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false)
      })

    return () => {
      cancelled = true
    }
    // fetcher is expected to be stable per call site (defined inline as a small wrapper);
    // re-running only on page/reloadToken change avoids infinite loops from new fn identities.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, reloadToken])

  return { data, isLoading, error, reload }
}
