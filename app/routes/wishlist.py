from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.product import Product
from ..models.wishlist import Wishlist
from ..schemas.wishlist import WishlistCreate, WishlistItemResponse, WishlistResponse
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/api/wishlist", tags=["Wishlist"])


@router.get("/", response_model=WishlistResponse)
def get_wishlist(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()
    result = []
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        result.append(WishlistItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=product.name if product else None,
            product_price=product.price if product else None,
            product_image=product.image_url if product else None,
            created_at=item.created_at,
        ))
    return WishlistResponse(items=result)


@router.post("/add")
def add_to_wishlist(
    data: WishlistCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == data.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == data.product_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already in wishlist")

    item = Wishlist(user_id=current_user.id, product_id=data.product_id)
    db.add(item)
    db.commit()
    return {"message": "Added to wishlist"}


@router.delete("/remove/{product_id}")
def remove_from_wishlist(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == product_id,
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in wishlist")
    db.delete(item)
    db.commit()
    return {"message": "Removed from wishlist"}
