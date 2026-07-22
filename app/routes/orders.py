from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.product import Product
from ..models.cart import Cart, CartItem
from ..models.order import Order, OrderItem
from ..schemas.order import OrderCreate, OrderResponse, OrderItemResponse
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderResponse])
def get_my_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    result = []
    for order in orders:
        items = []
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            items.append(OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=product.name if product else None,
                product_price=product.price if product else None,
                quantity=item.quantity,
                price=item.price,
            ))
        result.append(OrderResponse(
            id=order.id,
            user_id=order.user_id,
            total_amount=order.total_amount,
            payment_method=order.payment_method,
            payment_status=order.payment_status,
            order_status=order.order_status,
            full_name=order.full_name,
            phone=order.phone,
            city=order.city,
            province=order.province,
            postal_code=order.postal_code,
            shipping_address=order.shipping_address,
            notes=order.notes,
            created_at=order.created_at,
            items=items,
        ))
    return result


@router.post("/place", response_model=OrderResponse)
def place_order(
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Get cart items
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all() if cart else []

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order_items_data = []
    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product or product.stock < cart_item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        price = product.discount_price if product.discount_price else product.price
        total += price * cart_item.quantity
        order_items_data.append({
            "product_id": product.id,
            "quantity": cart_item.quantity,
            "price": price,
        })

    payment_status = "paid" if data.payment_method == "advance_payment" else "pending"
    order = Order(
        user_id=current_user.id,
        total_amount=total,
        payment_method=data.payment_method,
        payment_status=payment_status,
        order_status="pending",
        full_name=data.full_name,
        phone=data.phone,
        city=data.city,
        province=data.province,
        postal_code=data.postal_code,
        shipping_address=data.shipping_address,
        notes=data.notes,
    )
    db.add(order)
    db.flush()

    for item_data in order_items_data:
        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        product.stock -= item_data["quantity"]
        order_item = OrderItem(
            order_id=order.id,
            **item_data,
        )
        db.add(order_item)

    # Clear cart
    for cart_item in cart_items:
        db.delete(cart_item)

    db.commit()
    db.refresh(order)

    items_result = []
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        items_result.append(OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=product.name if product else None,
            product_price=product.price if product else None,
            quantity=item.quantity,
            price=item.price,
        ))

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        total_amount=order.total_amount,
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        order_status=order.order_status,
        full_name=order.full_name,
        phone=order.phone,
        city=order.city,
        province=order.province,
        postal_code=order.postal_code,
        shipping_address=order.shipping_address,
        notes=order.notes,
        created_at=order.created_at,
        items=items_result,
    )


@router.post("/place-direct", response_model=OrderResponse)
def place_direct_order(
    product_id: int,
    quantity: int = 1,
    payment_method: str = "cash_on_delivery",
    full_name: str = "",
    phone: str = "",
    city: str = "",
    province: str = "",
    postal_code: str = "",
    shipping_address: str = "",
    notes: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    price = product.discount_price if product.discount_price else product.price
    total = price * quantity
    payment_status = "paid" if payment_method == "advance_payment" else "pending"

    order = Order(
        user_id=current_user.id,
        total_amount=total,
        payment_method=payment_method,
        payment_status=payment_status,
        order_status="pending",
        full_name=full_name,
        phone=phone,
        city=city,
        province=province,
        postal_code=postal_code,
        shipping_address=shipping_address,
        notes=notes,
    )
    db.add(order)
    db.flush()

    product.stock -= quantity
    order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, price=price)
    db.add(order_item)
    db.commit()
    db.refresh(order)

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        total_amount=order.total_amount,
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        order_status=order.order_status,
        full_name=order.full_name,
        phone=order.phone,
        city=order.city,
        province=order.province,
        postal_code=order.postal_code,
        shipping_address=order.shipping_address,
        notes=order.notes,
        created_at=order.created_at,
        items=[OrderItemResponse(
            id=order_item.id,
            product_id=product.id,
            product_name=product.name,
            product_price=product.price,
            quantity=quantity,
            price=price,
        )],
    )
