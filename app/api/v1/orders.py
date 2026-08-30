from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.database.models import User
from app.schemas.orders import OrderResponse, OrderStatusUpdate
from app.service import orders as order_service
from app.dependencies.auth import get_current_user, require_admin

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=201
)
async def create_order(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await order_service.create_order(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await order_service.get_order(
        db=db,
        order_id=order_id,
        current_user=current_user
    )


@router.get(
    "/",
    response_model=list[OrderResponse]
)
async def get_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await order_service.get_orders(
        db=db,
        current_user=current_user
    )


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse
)
async def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return await order_service.update_order_status(
        db=db,
        order_id=order_id,
        payload=payload
    )


@router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse
)
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await order_service.cancel_order(
        db=db,
        order_id=order_id,
        current_user=current_user
    )