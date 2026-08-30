from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import Order, OrderItem


async def create_order(
    db: AsyncSession,
    order: Order
) -> Order:

    db.add(order)
    await db.flush()

    return order


async def get_order_by_id(
    db: AsyncSession,
    order_id: int
) -> Order | None:

    return await db.scalar(
        select(Order)
        .options(
            selectinload(Order.items)
            .selectinload(OrderItem.product)
        )
        .where(Order.id == order_id)
    )


async def get_order_by_id_and_user(
    db: AsyncSession,
    order_id: int,
    user_id: int
) -> Order | None:

    return await db.scalar(
        select(Order)
        .options(
            selectinload(Order.items)
            .selectinload(OrderItem.product)
        )
        .where(
            Order.id == order_id,
            Order.user_id == user_id
        )
    )


async def get_orders_by_user_id(
    db: AsyncSession,
    user_id: int
) -> list[Order]:

    result = await db.scalars(
        select(Order)
        .options(
            selectinload(Order.items)
            .selectinload(OrderItem.product)
        )
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )

    return list(result.all())


async def get_all_orders(
    db: AsyncSession
) -> list[Order]:

    result = await db.scalars(
        select(Order)
        .options(
            selectinload(Order.items)
            .selectinload(OrderItem.product)
        )
        .order_by(Order.created_at.desc())
    )

    return list(result.all())


async def update_order_status(
    db: AsyncSession,
    order: Order,
    status: str
) -> Order:

    order.status = status

    await db.commit()
    await db.refresh(order)

    return order