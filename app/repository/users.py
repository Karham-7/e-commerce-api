from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User


async def get_user_by_id(
    db: AsyncSession,
    user_id: int
) -> User | None:

    return await db.scalar(
        select(User)
        .where(User.id == user_id)
    )


async def get_user_by_email(
    db: AsyncSession,
    email: str
) -> User | None:

    return await db.scalar(
        select(User)
        .where(User.email == email)
    )


async def get_user_by_username(
    db: AsyncSession,
    username: str
) -> User | None:

    return await db.scalar(
        select(User)
        .where(User.username == username)
    )


async def create_user(
    db: AsyncSession,
    user: User
) -> User:

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user