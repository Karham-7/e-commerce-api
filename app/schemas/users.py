from datetime import datetime

from pydantic import BaseModel, Field, field_validator, EmailStr


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)
    age: int = Field(ge=1, le=99)

    @field_validator("username")
    @classmethod
    def normalize_username(cls, username: str) -> str:
        username = username.strip()

        if not username:
            raise ValueError("Username cannot be empty")

        return username

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, email: str) -> str:
        return str(email).strip().lower()


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    age: int
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}