import { useEffect, useState } from 'react'
import { getPublicBike } from '../api/frontCatalog'
import type { Bike } from '../api/bikes'

// CartItemReadDto/CheckoutItemReadDto/OrderItemReadDto only carry bike_id + quantity (the
// Jinja templates read bike.name/price/image_url off the ORM relationship directly, bypassing
// the DTO) — so line-item bike details are fetched client-side here instead of extending
// those DTOs, since these lists are always small (a handful of items per cart/checkout/order).
export function useBikeLookup(bikeIds: number[]) {
  const [bikes, setBikes] = useState<Record<number, Bike>>({})

  useEffect(() => {
    const uniqueIds = Array.from(new Set(bikeIds))
    const missing = uniqueIds.filter((id) => !(id in bikes))
    if (missing.length === 0) return

    let cancelled = false
    Promise.all(missing.map((id) => getPublicBike(id).then((bike) => [id, bike] as const))).then((entries) => {
      if (cancelled) return
      setBikes((prev) => {
        const next = { ...prev }
        for (const [id, bike] of entries) next[id] = bike
        return next
      })
    })

    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bikeIds.join(',')])

  return bikes
}
