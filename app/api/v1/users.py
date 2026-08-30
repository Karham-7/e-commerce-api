from fastapi import APIRouter, Depends

from app.database.models import User
from app.dependencies.auth import get_current_user, require_admin
from app.schemas.users import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/admin")
def admin_test(
    current_user: User = Depends(require_admin)
):
    return {
        "message": f"Hello, admin {current_user.username}"
    }