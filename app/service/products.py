from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.products import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)

from app.repository import categories as categories_repository
from app.repository import products as products_repository


async def create_product(
    db: AsyncSession,
    payload: ProductCreate
) -> ProductResponse:

    existing_product = await products_repository.get_product_by_name(
        db=db,
        name=payload.name
    )

    if existing_product:
        raise HTTPException(
            status_code=409,
            detail=f"Product '{payload.name}' already exists"
        )

    category = await categories_repository.get_category_by_id(
        db=db,
        category_id=payload.category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {payload.category_id} not found"
        )

    product = await products_repository.create_product(
        db=db,
        payload=payload
    )

    return ProductResponse.model_validate(product)


async def get_products(
    db: AsyncSession,
    category_id: int | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    in_stock: bool | None = None,
    offset: int = 0,
    limit: int = 20,
    sort_by: str = "id",
    order: str = "asc"
) -> list[ProductResponse]:

    if category_id is not None:

        category = await categories_repository.get_category_by_id(
            db=db,
            category_id=category_id
        )

        if category is None:
            raise HTTPException(
                status_code=404,
                detail=f"Category with id {category_id} not found"
            )

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price"
        )

    products = await products_repository.get_products(
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

    return [
        ProductResponse.model_validate(product)
        for product in products
    ]


async def get_product_by_id(
    db: AsyncSession,
    product_id: int
) -> ProductResponse:

    product = await products_repository.get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )

    return ProductResponse.model_validate(product)


async def update_product(
    db: AsyncSession,
    product_id: int,
    payload: ProductUpdate
) -> ProductResponse:

    product = await products_repository.get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )

    if payload.name is not None:

        existing_product = await products_repository.get_product_by_name(
            db=db,
            name=payload.name
        )

        if (
            existing_product
            and existing_product.id != product_id
        ):
            raise HTTPException(
                status_code=409,
                detail=f"Product '{payload.name}' already exists"
            )

    if payload.category_id is not None:

        category = await categories_repository.get_category_by_id(
            db=db,
            category_id=payload.category_id
        )

        if category is None:
            raise HTTPException(
                status_code=404,
                detail=f"Category with id {payload.category_id} not found"
            )

    product = await products_repository.update_product(
        db=db,
        product_id=product_id,
        payload=payload
    )

    return ProductResponse.model_validate(product)


async def delete_product(
    db: AsyncSession,
    product_id: int
) -> ProductResponse:

    product = await products_repository.get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )

    deleted_product = await products_repository.delete_product(
        db=db,
        product=product
    )

    return ProductResponse.model_validate(deleted_product)