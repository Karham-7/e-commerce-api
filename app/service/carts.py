from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import carts as cart_repository
from app.repository import products as product_repository
from app.schemas.carts import (
    CartItemResponse,
    CartItemCreate,
    CartResponse,
    CartItemUpdate
)


async def get_or_create_cart(
    db: AsyncSession,
    user_id: int
) -> CartResponse:

    cart = await cart_repository.get_cart_by_user_id(
        db=db,
        user_id=user_id
    )

    if cart is None:
        cart = await cart_repository.create_cart(
            db=db,
            user_id=user_id
        )

    items = [
        CartItemResponse(
            id=item.id,
            product_id=item.product.id,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )
        for item in cart.items
    ]

    total = sum(
        item.price * item.quantity
        for item in items
    )

    return CartResponse(
        id=cart.id,
        items=items,
        total=total
    )


async def add_cart_item(
    db: AsyncSession,
    user_id: int,
    payload: CartItemCreate
) -> CartItemResponse:

    cart = await cart_repository.get_cart_by_user_id(
        db=db,
        user_id=user_id
    )

    if cart is None:
        cart = await cart_repository.create_cart(
            db=db,
            user_id=user_id
        )

    product = await product_repository.get_product_by_id(
        db=db,
        product_id=payload.product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {payload.product_id} not found"
        )

    cart_item = await cart_repository.get_cart_item(
        db=db,
        cart_id=cart.id,
        product_id=payload.product_id
    )

    if cart_item is None:
        new_quantity = payload.quantity
    else:
        new_quantity = cart_item.quantity + payload.quantity

    if new_quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Not enough product in stock. "
                f"Only {product.stock} available"
            )
        )

    if cart_item is None:

        cart_item = await cart_repository.create_cart_item(
            db=db,
            cart_id=cart.id,
            product_id=product.id,
            quantity=new_quantity
        )

    else:

        cart_item = await cart_repository.update_cart_item_quantity(
            db=db,
            cart_item=cart_item,
            quantity=new_quantity
        )

    return CartItemResponse(
        id=cart_item.id,
        product_id=product.id,
        product_name=product.name,
        price=product.price,
        quantity=cart_item.quantity
    )


async def update_cart_item(
    db: AsyncSession,
    user_id: int,
    item_id: int,
    payload: CartItemUpdate
) -> CartItemResponse:

    cart_item = await cart_repository.get_cart_item_by_id(
        db=db,
        item_id=item_id
    )

    if cart_item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Cart item with id {item_id} not found"
        )

    if cart_item.cart.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot modify this cart item"
        )

    product = await product_repository.get_product_by_id(
        db=db,
        product_id=cart_item.product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {cart_item.product_id} not found"
        )

    if payload.quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Not enough product in stock. "
                f"Only {product.stock} available"
            )
        )

    cart_item = await cart_repository.update_cart_item_quantity(
        db=db,
        cart_item=cart_item,
        quantity=payload.quantity
    )

    return CartItemResponse(
        id=cart_item.id,
        product_id=product.id,
        product_name=product.name,
        price=product.price,
        quantity=cart_item.quantity
    )


async def delete_cart_item(
    db: AsyncSession,
    user_id: int,
    item_id: int
) -> CartItemResponse:

    cart_item = await cart_repository.get_cart_item_by_id(
        db=db,
        item_id=item_id
    )

    if cart_item is None:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    if cart_item.cart.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this cart item"
        )

    response = CartItemResponse(
        id=cart_item.id,
        product_id=cart_item.product.id,
        product_name=cart_item.product.name,
        price=cart_item.product.price,
        quantity=cart_item.quantity
    )

    await cart_repository.delete_cart_item(
        db=db,
        cart_item=cart_item
    )

    return response


async def clear_cart(
    db: AsyncSession,
    user_id: int
) -> None:

    cart = await cart_repository.get_cart_by_user_id(
        db=db,
        user_id=user_id
    )

    if cart is None:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    await cart_repository.delete_cart_items(
        db=db,
        cart=cart
    )