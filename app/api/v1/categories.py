from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.database.models import User
from app.dependencies.auth import require_admin
from app.schemas.categories import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate
)
from app.service import categories as category_service


router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=201
)
async def create_category(
    payload: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return await category_service.create_category(
        db=db,
        payload=payload
    )


@router.get(
    "/",
    response_model=list[CategoryResponse]
)
async def get_all_categories(
    db: AsyncSession = Depends(get_db)
):
    return await category_service.get_all_categories(
        db=db
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
async def get_category_by_id(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await category_service.get_category_by_id(
        db=db,
        category_id=category_id
    )


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse
)
async def update_category_name(
    category_id: int,
    payload: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return await category_service.update_category_name(
        db=db,
        category_id=category_id,
        new_name=payload.name
    )


@router.delete(
    "/{category_id}",
    response_model=CategoryResponse
)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return await category_service.delete_category(
        db=db,
        category_id=category_id
    )