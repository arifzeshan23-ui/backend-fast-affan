from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    stock: int = 0
    category: Optional[str] = None
    gender: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: Optional[bool] = False
    is_new_arrival: Optional[bool] = False


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    gender: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_new_arrival: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    stock: int
    category: Optional[str] = None
    gender: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    is_featured: bool
    is_new_arrival: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
