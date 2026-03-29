from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers.endpoints.admin import admin_bike_router, admin_cart_router, admin_checkout_router, admin_order_router
from app.routers.endpoints.admin import admin_user_router, admin_manufacturers_router
from app.routers.endpoints.auth import auth_router
from app.routers.endpoints.front import homepage_router, shopping_cart_router, checkout_router, order_router
from app.routers.render_pages.admin import admin_render_router, admin_render_user_router, admin_render_bike_router, \
    admin_render_manufacturers_router, admin_render_cart_router, admin_render_checkout_router, admin_render_order_router
from app.routers.render_pages.auth import auth_render_router
from app.routers.render_pages.front import homepage_render_routers, homepage_render_bike_router, \
    cart_steps_render_router, order_steps_render_router


def init_pre_requested_methods(app: FastAPI):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


def init_routers(app: FastAPI):
    ## ENDPOINTS
    # front
    app.include_router(homepage_router.router)
    app.include_router(shopping_cart_router.router)
    app.include_router(checkout_router.router)
    app.include_router(order_router.router)

    # auth
    app.include_router(auth_router.router)

    # admin
    app.include_router(admin_user_router.router)
    app.include_router(admin_bike_router.router)
    app.include_router(admin_manufacturers_router.router)
    app.include_router(admin_cart_router.router)
    app.include_router(admin_checkout_router.router)
    app.include_router(admin_order_router.router)


def init_pages(app: FastAPI):
    # front
    app.include_router(homepage_render_routers.router)
    app.include_router(homepage_render_bike_router.router)
    app.include_router(cart_steps_render_router.router)
    app.include_router(order_steps_render_router.router)

    # auth
    app.include_router(auth_render_router.router)

    # admin
    app.include_router(admin_render_router.router)
    app.include_router(admin_render_user_router.router)
    app.include_router(admin_render_bike_router.router)
    app.include_router(admin_render_manufacturers_router.router)
    app.include_router(admin_render_cart_router.router)
    app.include_router(admin_render_checkout_router.router)
    app.include_router(admin_render_order_router.router)
