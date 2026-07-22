from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models.user import User
from ..models.product import Product
from ..models.order import Order, OrderItem
from ..schemas.order import OrderResponse, OrderItemResponse, OrderStatusUpdate
from ..auth.jwt import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    total_orders = db.query(Order).count()
    total_products = db.query(Product).count()
    total_users = db.query(User).count()
    total_revenue = db.query(func.coalesce(func.sum(Order.total_amount), 0)).scalar()
    pending_orders = db.query(Order).filter(Order.order_status == "pending").count()
    delivered_orders = db.query(Order).filter(Order.order_status == "delivered").count()
    cancelled_orders = db.query(Order).filter(Order.order_status == "cancelled").count()

    now = datetime.utcnow()
    months = []
    monthly_revenue = []
    monthly_orders = []
    for i in range(5, -1, -1):
        d = now - timedelta(days=30 * i)
        month_name = d.strftime("%b")
        months.append(month_name)
        rev = db.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(
            extract("year", Order.created_at) == d.year,
            extract("month", Order.created_at) == d.month,
        ).scalar()
        cnt = db.query(Order).filter(
            extract("year", Order.created_at) == d.year,
            extract("month", Order.created_at) == d.month,
        ).count()
        monthly_revenue.append(float(rev))
        monthly_orders.append(cnt)

    category_data = {}
    products = db.query(Product).all()
    for p in products:
        cat = p.category or "Other"
        category_data[cat] = category_data.get(cat, 0) + 1

    top_products = db.query(
        OrderItem.product_id,
        func.sum(OrderItem.quantity).label("total_sold"),
    ).group_by(OrderItem.product_id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()

    top_products_list = []
    for pid, sold in top_products:
        prod = db.query(Product).filter(Product.id == pid).first()
        top_products_list.append({
            "name": prod.name if prod else f"Product #{pid}",
            "sold": int(sold),
        })

    return {
        "totals": {
            "orders": total_orders,
            "products": total_products,
            "users": total_users,
            "revenue": float(total_revenue),
        },
        "order_status": {
            "pending": pending_orders,
            "delivered": delivered_orders,
            "cancelled": cancelled_orders,
            "confirmed": total_orders - pending_orders - delivered_orders - cancelled_orders,
        },
        "monthly_revenue": {"labels": months, "data": monthly_revenue},
        "monthly_orders": {"labels": months, "data": monthly_orders},
        "category_data": category_data,
        "top_products": top_products_list,
    }


@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    status: str = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    query = db.query(Order).order_by(Order.created_at.desc())
    if status:
        query = query.filter(Order.order_status == status)
    orders = query.all()

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


@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_statuses = ["pending", "confirmed", "cancelled", "delivered"]
    if data.order_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

    order.order_status = data.order_status
    if data.order_status == "delivered":
        order.payment_status = "paid"
    db.commit()
    return {"message": f"Order status updated to {data.order_status}"}


@router.get("/users", response_model=List[dict])
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "full_name": u.full_name,
            "phone": u.phone,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]
