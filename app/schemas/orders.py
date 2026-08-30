from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.Enum.orders import OrderStatus


class OrderItemResponse(BaseModel):
    id: int

    product_id: int
    product_name: str

    price: Decimal
    quantity: int


class OrderResponse(BaseModel):
    id: int

    status: str

    total_price: Decimal

    created_at: datetime

    items: list[OrderItemResponse]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus