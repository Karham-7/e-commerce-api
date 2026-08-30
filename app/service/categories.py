from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.categories import (
    CategoryCreate,
    CategoryResponse
)

from app.repository import categories as categories_repository


async def create_category(
    db: AsyncSession,
    payload: CategoryCreate
) -> CategoryResponse:

    existing_category = await categories_repository.get_category_by_name(
        db=db,
        category_name=payload.name
    )

    if existing_category:
        raise HTTPException(
            status_code=409,
            detail=f"Category '{payload.name}' already exists"
        )

    category = await categories_repository.create_category(
        db=db,
        payload=payload
    )

    return CategoryResponse.model_validate(category)


async def get_all_categories(
    db: AsyncSession
) -> list[CategoryResponse]:

    categories = await categories_repository.get_all_categories(
        db=db
    )

    return [
        CategoryResponse.model_validate(category)
        for category in categories
    ]


async def get_category_by_id(
    db: AsyncSession,
    category_id: int
) -> CategoryResponse:

    category = await categories_repository.get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {category_id} not found"
        )

    return CategoryResponse.model_validate(category)


async def update_category_name(
    db: AsyncSession,
    category_id: int,
    new_name: str
) -> CategoryResponse:

    category = await categories_repository.get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {category_id} not found"
        )

    new_name = new_name.capitalize()

    existing_category = await categories_repository.get_category_by_name(
        db=db,
        category_name=new_name
    )

    if existing_category and existing_category.id != category_id:
        raise HTTPException(
            status_code=409,
            detail=f"Category '{new_name}' already exists"
        )

    updated_category = await categories_repository.update_category_name(
        db=db,
        category_id=category_id,
        new_name=new_name
    )

    return CategoryResponse.model_validate(updated_category)


async def delete_category(
    db: AsyncSession,
    category_id: int
) -> CategoryResponse:

    category = await categories_repository.get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {category_id} not found"
        )

    has_products = await categories_repository.category_has_products(
        db=db,
        category_id=category_id
    )

    if has_products:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete category because it contains products"
        )

    deleted_category = await categories_repository.delete_category(
        db=db,
        category_id=category_id
    )

    return CategoryResponse.model_validate(deleted_category)