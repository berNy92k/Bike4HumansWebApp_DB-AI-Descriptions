import { defineConfig, type ProxyOptions } from 'vite'
import react from '@vitejs/plugin-react'
import type { IncomingMessage } from 'node:http'

// Backend runs separately (uvicorn) during development; production builds are
// served by FastAPI itself from the same origin (see Faza 4 of the migration plan).
const BACKEND_URL = 'http://127.0.0.1:8000'

// Several backend path prefixes (/admin, /auth, /bikes, /manufacturers, /cart, /checkout,
// /order) are shared between real JSON API calls AND client-side React Router pages that
// happen to live at the same URL (by design — see the migration plan's route mapping). A
// plain prefix-based proxy would also intercept full-page navigations/hard-refreshes for
// those React routes and forward them to FastAPI, which still serves the old Jinja page at
// the same path until it's deleted in Faza 5 — so the SPA would never actually be reachable
// there. `fetch()` calls made by src/api/apiClient.ts always send `Accept: application/json`;
// real browser page navigations send `Accept: text/html,...`. Use that to tell them apart:
// only forward to the backend when the client is not asking for an HTML document.
function apiOnly(): ProxyOptions {
  return {
    target: BACKEND_URL,
    bypass(req: IncomingMessage) {
      if (req.headers.accept?.includes('text/html')) {
        // Not an API call — let Vite serve index.html / the SPA route instead.
        return req.url
      }
    },
  }
}

// Pure API/asset prefixes with no overlapping SPA page route can be proxied unconditionally.
function alwaysProxy(): ProxyOptions {
  return { target: BACKEND_URL }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/admin': apiOnly(),
      '/auth': apiOnly(),
      '/bikes': apiOnly(),
      '/manufacturers': apiOnly(),
      '/cart': apiOnly(),
      '/checkout': apiOnly(),
      '/order': apiOnly(),
      '/api': alwaysProxy(),
      '/payment-methods': alwaysProxy(),
      '/static': alwaysProxy(),
      '/address': alwaysProxy(),
    },
  },
})
