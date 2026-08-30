from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.database.models import User
from app.dependencies.auth import get_current_user
from app.schemas.carts import (
    CartResponse,
    CartItemResponse,
    CartItemCreate,
    CartItemUpdate
)
from app.service import carts as cart_service


router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)


@router.get(
    "/",
    response_model=CartResponse
)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await cart_service.get_or_create_cart(
        db=db,
        user_id=current_user.id
    )


@router.post(
    "/items",
    response_model=CartItemResponse,
    status_code=201
)
async def add_cart_item(
    payload: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await cart_service.add_cart_item(
        db=db,
        user_id=current_user.id,
        payload=payload
    )


@router.patch(
    "/items/{item_id}",
    response_model=CartItemResponse
)
async def update_cart_item(
    item_id: int,
    payload: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await cart_service.update_cart_item(
        db=db,
        user_id=current_user.id,
        item_id=item_id,
        payload=payload
    )


@router.delete(
    "/items/{item_id}",
    response_model=CartItemResponse
)
async def delete_cart_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await cart_service.delete_cart_item(
        db=db,
        user_id=current_user.id,
        item_id=item_id
    )


@router.delete(
    "/",
    status_code=204
)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await cart_service.clear_cart(
        db=db,
        user_id=current_user.id
    )