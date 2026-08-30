from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.users import UserCreate, UserResponse
from app.repository import users as users_repository
from app.security.jwt import create_access_token
from app.security.password import hash_password, verify_password


async def register_user(
    db: AsyncSession,
    payload: UserCreate
) -> UserResponse:

    existing_email = await users_repository.get_user_by_email(
        db=db,
        email=payload.email
    )

    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    existing_username = await users_repository.get_user_by_username(
        db=db,
        username=payload.username
    )

    if existing_username:
        raise HTTPException(
            status_code=409,
            detail="Username already taken"
        )

    user = User(
        username=payload.username,
        email=payload.email,
        age=payload.age,
        hashed_password=hash_password(payload.password),
    )

    created_user = await users_repository.create_user(
        db=db,
        user=user
    )

    return UserResponse.model_validate(created_user)


async def login_user(
    db: AsyncSession,
    payload: LoginRequest
) -> TokenResponse:

    user = await users_repository.get_user_by_email(
        db=db,
        email=payload.login
    )

    if user is None:
        user = await users_repository.get_user_by_username(
            db=db,
            username=payload.login
        )

    if user is None or not verify_password(
        payload.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )