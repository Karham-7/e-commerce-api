from fastapi import FastAPI

from app.api.v1.categories import router as categories_router
from app.api.v1.products import router as products_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.carts import router as carts_router
from app.api.v1.orders import router as orders_router


app = FastAPI(
    title="E-commerce API",
    description="Backend интернет магазина",
    version="1.0.0"
)


app.include_router(
    categories_router,
    prefix="/api/v1"
)

app.include_router(
    products_router,
    prefix="/api/v1"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    users_router,
    prefix="/api/v1"
)

app.include_router(
    carts_router,
    prefix="/api/v1"
)

app.include_router(
    orders_router,
    prefix="/api/v1"
)

