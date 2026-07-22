from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str
    gender: Optional[str] = "All"


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    gender: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
