interface PaginationProps {
  page: number
  pages: number
  total: number
  onPageChange: (page: number) => void
}

export function Pagination({ page, pages, total, onPageChange }: PaginationProps) {
  if (pages <= 1) return null

  return (
    <div className="pagination">
      <button disabled={page <= 1} onClick={() => onPageChange(page - 1)}>
        Poprzednia
      </button>
      <span>
        Strona {page} z {pages} ({total} wyników)
      </span>
      <button disabled={page >= pages} onClick={() => onPageChange(page + 1)}>
        Następna
      </button>
    </div>
  )
}
