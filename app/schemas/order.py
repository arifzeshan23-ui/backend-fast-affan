from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    payment_method: str  # cash_on_delivery, advance_payment
    full_name: str
    phone: str
    city: str
    province: str
    postal_code: Optional[str] = ""
    shipping_address: str
    notes: Optional[str] = ""


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: Optional[str] = None
    product_price: Optional[float] = None
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    payment_method: str
    payment_status: str
    order_status: str
    full_name: Optional[str] = None
    phone: str
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    shipping_address: str
    notes: Optional[str] = None
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    order_status: str  # confirmed, cancelled, delivered
