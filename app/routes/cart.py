from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.product import Product
from ..models.cart import Cart, CartItem
from ..schemas.cart import CartItemCreate, CartResponse, CartItemResponse
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/api/cart", tags=["Cart"])


def get_or_create_cart(user_id: int, db: Session):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/", response_model=CartResponse)
def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_or_create_cart(current_user.id, db)
    items = []
    total = 0
    for item in db.query(CartItem).filter(CartItem.cart_id == cart.id).all():
        product = db.query(Product).filter(Product.id == item.product_id).first()
        effective_price = product.discount_price if product and product.discount_price else (product.price if product else 0)
        items.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=product.name if product else None,
            product_price=effective_price,
            product_image=product.image_url if product else None,
            created_at=item.created_at,
        ))
        if product:
            total += effective_price * item.quantity
    return CartResponse(id=cart.id, user_id=cart.user_id, items=items, total=total, created_at=cart.created_at)


@router.post("/add")
def add_to_cart(
    data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == data.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart = get_or_create_cart(current_user.id, db)
    existing = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id,
    ).first()

    if existing:
        existing.quantity += data.quantity
    else:
        item = CartItem(cart_id=cart.id, user_id=current_user.id, product_id=data.product_id, quantity=data.quantity)
        db.add(item)
    db.commit()
    return {"message": "Item added to cart"}


@router.put("/update/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if quantity <= 0:
        db.delete(item)
    else:
        item.quantity = quantity
    db.commit()
    return {"message": "Cart updated"}


@router.delete("/remove/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}
