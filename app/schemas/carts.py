from decimal import Decimal

from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: Decimal
    quantity: int

    model_config = {
        "from_attributes": True
    }


class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]
    total: Decimal

    model_config = {
        "from_attributes": True
    }





