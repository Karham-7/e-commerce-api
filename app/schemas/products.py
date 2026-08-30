from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0)
    category_id: int
    description: str | None = Field(default=None, max_length=255)
    stock: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    category_id: int
    description: str | None
    stock: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    price: Decimal | None = Field(
        default=None,
        gt=0
    )
    category_id: int | None = Field(
        default=None,
        gt=0
    )
    description: str | None = Field(
        default=None,
        max_length=255
    )
    stock: int | None = Field(
        default=None,
        ge=0
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        name = name.strip()

        if not name:
            raise ValueError("Product name cannot be empty")

        return name





