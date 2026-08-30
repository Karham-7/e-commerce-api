from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import Cart, CartItem


async def get_cart_by_user_id(
    db: AsyncSession,
    user_id: int
) -> Cart | None:

    return await db.scalar(
        select(Cart)
        .options(
            selectinload(Cart.items)
            .selectinload(CartItem.product)
        )
        .where(Cart.user_id == user_id)
    )


async def create_cart(
    db: AsyncSession,
    user_id: int
) -> Cart:

    cart = Cart(
        user_id=user_id
    )

    db.add(cart)

    await db.commit()
    await db.refresh(cart)

    return cart


async def get_cart_item(
    db: AsyncSession,
    cart_id: int,
    product_id: int
) -> CartItem | None:

    return await db.scalar(
        select(CartItem)
        .where(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id
        )
    )


async def create_cart_item(
    db: AsyncSession,
    cart_id: int,
    product_id: int,
    quantity: int
) -> CartItem:

    cart_item = CartItem(
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(cart_item)

    await db.commit()
    await db.refresh(cart_item)

    return cart_item


async def get_cart_item_by_id(
    db: AsyncSession,
    item_id: int
) -> CartItem | None:

    return await db.scalar(
        select(CartItem)
        .options(
            selectinload(CartItem.cart),
            selectinload(CartItem.product)
        )
        .where(CartItem.id == item_id)
    )


async def update_cart_item_quantity(
    db: AsyncSession,
    cart_item: CartItem,
    quantity: int
) -> CartItem:

    cart_item.quantity = quantity

    await db.commit()
    await db.refresh(cart_item)

    return cart_item


async def delete_cart_item(
    db: AsyncSession,
    cart_item: CartItem
) -> CartItem:

    await db.delete(cart_item)

    await db.commit()

    return cart_item


async def delete_cart_items(
    db: AsyncSession,
    cart: Cart
) -> None:

    cart.items.clear()

    await db.commit()