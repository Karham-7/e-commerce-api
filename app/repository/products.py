from decimal import Decimal

from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Product
from app.schemas.products import ProductCreate, ProductUpdate


async def create_product(
    db: AsyncSession,
    payload: ProductCreate
) -> Product:

    product = Product(
        name=payload.name,
        price=payload.price,
        category_id=payload.category_id,
        description=payload.description,
        stock=payload.stock
    )

    db.add(product)

    await db.commit()
    await db.refresh(product)

    return product


async def get_product_by_name(
    db: AsyncSession,
    name: str
) -> Product | None:

    return await db.scalar(
        select(Product)
        .where(Product.name == name)
    )


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
) -> list[Product]:

    query = select(Product)

    if category_id is not None:
        query = query.where(
            Product.category_id == category_id
        )

    if min_price is not None:
        query = query.where(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.where(
            Product.price <= max_price
        )

    if in_stock is not None:
        if in_stock:
            query = query.where(Product.stock > 0)
        else:
            query = query.where(Product.stock == 0)

    if sort_by == "price":
        sort_column = Product.price
    else:
        sort_column = Product.id

    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    query = query.offset(offset).limit(limit)

    result = await db.scalars(query)

    return list(result.all())


async def get_product_by_id(
    db: AsyncSession,
    product_id: int
) -> Product | None:

    return await db.scalar(
        select(Product)
        .where(Product.id == product_id)
    )


async def update_product(
    db: AsyncSession,
    product_id: int,
    payload: ProductUpdate
) -> Product | None:

    product = await get_product_by_id(
        db=db,
        product_id=product_id
    )

    if product is None:
        return None

    update_data = payload.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product


async def delete_product(
    db: AsyncSession,
    product: Product
) -> Product:

    await db.delete(product)
    await db.commit()

    return product