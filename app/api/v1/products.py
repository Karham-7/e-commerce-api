from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.database.models import User
from app.dependencies.auth import require_admin
from app.schemas.products import (
    ProductResponse,
    ProductCreate,
    ProductUpdate
)

from app.service import products as product_service


router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201
)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return await product_service.create_product(
        db=db,
        payload=payload
    )


@router.get(
    "/",
    response_model=list[ProductResponse]
)
async def get_products(
    category_id: int | None = Query(
        default=None,
        gt=0
    ),
    min_price: Decimal | None = Query(
        default=None,
        gt=0
    ),
    max_price: Decimal | None = Query(
        default=None,
        gt=0
    ),
    in_stock: bool | None = None,
    offset: int = Query(
        default=0,
        ge=0
    ),
    limit: int = Query(
        default=20,
        gt=0,
        le=100
    ),
    sort_by: str = Query(
        default="id"
    ),
    order: str = Query(
        default="asc"
    ),
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_products(
        db=db,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        order=order
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
async def get_product_by_id(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_product_by_id(
        db=db,
        product_id=product_id
    )


@router.patch(
    "/{product_id}",
    response_model=ProductResponse
)
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return await product_service.update_product(
        db=db,
        product_id=product_id,
        payload=payload
    )


@router.delete(
    "/{product_id}",
    response_model=ProductResponse
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return await product_service.delete_product(
        db=db,
        product_id=product_id
    )