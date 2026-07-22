from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class WishlistCreate(BaseModel):
    product_id: int


class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: Optional[str] = None
    product_price: Optional[float] = None
    product_image: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class WishlistResponse(BaseModel):
    items: List[WishlistItemResponse]

    class Config:
        from_attributes = True
