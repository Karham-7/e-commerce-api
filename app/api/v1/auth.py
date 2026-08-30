from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.auth import LoginRequest
from app.schemas.users import UserCreate

from app.service import auth as auth_service

router = APIRouter(
    prefix="/auth",
    tags=["authorization"]
)


@router.post("/register")
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await auth_service.register_user(
        db=db,
        payload=payload
    )


@router.post("/login")
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    return await auth_service.login_user(
        db=db,
        payload=payload
    )