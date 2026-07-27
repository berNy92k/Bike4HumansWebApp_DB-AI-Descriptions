from pathlib import Path

from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from app.routers.endpoints.admin import admin_bike_router, admin_cart_router, admin_checkout_router, admin_order_router
from app.routers.endpoints.admin import admin_user_router, admin_manufacturer_router, admin_dashboard_router
from app.routers.endpoints.auth import auth_router
from app.routers.endpoints.front import homepage_router, cart_router, checkout_router, order_router, bike_router, \
    manufacturer_router, payment_method_router


def init_pre_requested_methods(app: FastAPI):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


def init_routers(app: FastAPI):
    ## ENDPOINTS
    # front
    app.include_router(homepage_router.router)
    app.include_router(bike_router.router)
    app.include_router(bike_router.public_router)
    app.include_router(manufacturer_router.router)
    app.include_router(payment_method_router.router)
    app.include_router(cart_router.router)
    app.include_router(checkout_router.router)
    app.include_router(order_router.router)
    app.include_router(order_router.public_router)

    # auth
    app.include_router(auth_router.router)

    # admin
    app.include_router(admin_user_router.router)
    app.include_router(admin_bike_router.router)
    app.include_router(admin_manufacturer_router.router)
    app.include_router(admin_cart_router.router)
    app.include_router(admin_checkout_router.router)
    app.include_router(admin_order_router.router)
    app.include_router(admin_dashboard_router.router)


SPA_DIR = Path("app/static/spa")


def init_spa(app: FastAPI):
    """Serve the built React app (frontend/, see Dockerfile) once it exists.

    Must be called *after* init_routers(): the catch-all route below only handles GET requests
    that no earlier JSON API route matched, so it can serve every React client-side route (see
    frontend/src/App.tsx) without any per-route wiring here. In local dev (no Docker build),
    SPA_DIR won't exist and this is a no-op, matching the Vite-dev-server workflow.
    """
    if not SPA_DIR.exists():
        return

    app.mount("/assets", StaticFiles(directory=str(SPA_DIR / "assets")), name="spa-assets")

    index_path = SPA_DIR / "index.html"

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        return FileResponse(index_path)
