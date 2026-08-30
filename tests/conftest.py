import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.pool import NullPool

from app.config import settings
from app.database.database import Base, get_db
from app.main import app

from app.database.models import User
from app.security.password import hash_password
from app.security.jwt import create_access_token


engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    poolclass=NullPool
)


TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_client(db_session: AsyncSession):
    admin = User(
        username="test_admin",
        email="admin@test.com",
        age=25,
        hashed_password=hash_password("password123"),
        role="admin"
    )

    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)

    token = create_access_token(admin.id)

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={
            "Authorization": f"Bearer {token}"
        }
    ) as client:
        yield client

    app.dependency_overrides.clear()