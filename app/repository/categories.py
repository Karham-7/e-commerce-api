from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Category, Product
from app.schemas.categories import CategoryCreate


async def create_category(
    db: AsyncSession,
    payload: CategoryCreate
) -> Category:

    category = Category(name=payload.name)

    db.add(category)

    await db.commit()
    await db.refresh(category)

    return category


async def get_category_by_name(
    db: AsyncSession,
    category_name: str
) -> Category | None:

    return await db.scalar(
        select(Category)
        .where(Category.name == category_name)
    )


async def get_all_categories(
    db: AsyncSession
) -> list[Category]:

    result = await db.scalars(
        select(Category)
        .order_by(Category.id)
    )

    return list(result.all())


async def get_category_by_id(
    db: AsyncSession,
    category_id: int
) -> Category | None:

    return await db.scalar(
        select(Category)
        .where(Category.id == category_id)
    )


async def update_category_name(
    db: AsyncSession,
    category_id: int,
    new_name: str
) -> Category | None:

    category = await get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        return None

    category.name = new_name.capitalize()

    await db.commit()
    await db.refresh(category)

    return category


async def delete_category(
    db: AsyncSession,
    category_id: int
) -> Category | None:

    category = await get_category_by_id(
        db=db,
        category_id=category_id
    )

    if category is None:
        return None

    await db.delete(category)
    await db.commit()

    return category


async def category_has_products(
    db: AsyncSession,
    category_id: int
) -> bool:

    return (
        await db.scalar(
            select(Product.id)
            .where(Product.category_id == category_id)
            .limit(1)
        )
        is not None
    )