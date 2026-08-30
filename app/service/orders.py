from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.Enum.orders import OrderStatus, ALLOWED_STATUS_TRANSITIONS
from app.database.models import Order, OrderItem, User
from app.schemas.orders import (
    OrderResponse,
    OrderItemResponse,
    OrderStatusUpdate
)

from app.repository import orders as orders_repository
from app.repository import carts as cart_repository


async def create_order(
    db: AsyncSession,
    user_id: int
) -> OrderResponse:

    cart = await cart_repository.get_cart_by_user_id(
        db=db,
        user_id=user_id
    )

    if cart is None or not cart.items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total = Decimal("0")

    order = Order(
        user_id=user_id,
        status="pending",
        total=total
    )

    for cart_item in cart.items:

        product = cart_item.product

        if cart_item.quantity > product.stock:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Not enough product in stock: "
                    f"{product.name}. "
                    f"Available: {product.stock}"
                )
            )

        order_item = OrderItem(
            product_id=product.id,
            quantity=cart_item.quantity,
            price=product.price
        )

        order.items.append(order_item)

        total += product.price * cart_item.quantity

        product.stock -= cart_item.quantity

    order.total = total

    try:
        await orders_repository.create_order(
            db=db,
            order=order
        )

        cart.items.clear()

        await db.commit()

    except Exception:
        await db.rollback()
        raise

    return OrderResponse(
        id=order.id,
        status=order.status,
        total_price=order.total,
        created_at=order.created_at,
        items=[
            OrderItemResponse(
                id=item.id,
                product_id=item.product.id,
                product_name=item.product.name,
                price=item.price,
                quantity=item.quantity
            )
            for item in order.items
        ]
    )


async def get_order(
    db: AsyncSession,
    order_id: int,
    current_user: User
) -> OrderResponse:

    if current_user.role == "admin":
        order = await orders_repository.get_order_by_id(
            db=db,
            order_id=order_id
        )
    else:
        order = await orders_repository.get_order_by_id_and_user(
            db=db,
            order_id=order_id,
            user_id=current_user.id
        )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order with id {order_id} not found"
        )

    items = [
        OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=item.product.name,
            price=item.price,
            quantity=item.quantity
        )
        for item in order.items
    ]

    total_price = sum(
        item.price * item.quantity
        for item in order.items
    )

    return OrderResponse(
        id=order.id,
        status=order.status,
        total_price=total_price,
        created_at=order.created_at,
        items=items
    )


async def get_orders(
    db: AsyncSession,
    current_user: User
) -> list[OrderResponse]:

    orders = await orders_repository.get_orders_by_user_id(
        db=db,
        user_id=current_user.id
    )

    return [
        OrderResponse(
            id=order.id,
            status=order.status,
            total_price=order.total,
            created_at=order.created_at,
            items=[
                OrderItemResponse(
                    id=item.id,
                    product_id=item.product_id,
                    product_name=item.product.name,
                    price=item.price,
                    quantity=item.quantity
                )
                for item in order.items
            ]
        )
        for order in orders
    ]


async def update_order_status(
    db: AsyncSession,
    order_id: int,
    payload: OrderStatusUpdate
) -> OrderResponse:

    order = await orders_repository.get_order_by_id(
        db=db,
        order_id=order_id
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order with id {order_id} not found"
        )

    current_status = OrderStatus(order.status)

    new_status = payload.status

    allowed_statuses = ALLOWED_STATUS_TRANSITIONS[current_status]

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Cannot change order status from "
                f"{current_status.value} to "
                f"{new_status.value}"
            )
        )

    order = await orders_repository.update_order_status(
        db=db,
        order=order,
        status=new_status.value
    )

    return OrderResponse(
        id=order.id,
        status=order.status,
        total_price=order.total,
        created_at=order.created_at,
        items=[
            OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product.name,
                price=item.price,
                quantity=item.quantity
            )
            for item in order.items
        ]
    )


async def cancel_order(
    db: AsyncSession,
    order_id: int,
    current_user: User
) -> OrderResponse:

    order = await orders_repository.get_order_by_id_and_user(
        db=db,
        order_id=order_id,
        user_id=current_user.id
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order with id {order_id} not found"
        )

    current_status = OrderStatus(order.status)
    new_status = OrderStatus.CANCELLED

    allowed_statuses = ALLOWED_STATUS_TRANSITIONS[current_status]

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Cannot cancel order with status "
                f"{current_status.value}"
            )
        )

    try:
        for item in order.items:
            item.product.stock += item.quantity

        order.status = new_status.value

        await db.commit()

    except Exception:
        await db.rollback()
        raise

    return OrderResponse(
        id=order.id,
        status=order.status,
        total_price=order.total,
        created_at=order.created_at,
        items=[
            OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product.name,
                price=item.price,
                quantity=item.quantity
            )
            for item in order.items
        ]
    )