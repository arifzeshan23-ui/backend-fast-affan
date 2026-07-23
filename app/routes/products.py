import os
import uuid
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..auth.jwt import get_current_admin

router = APIRouter(prefix="/api/products", tags=["Products"])

# Resolves to project root: app/routes/products.py -> app/routes -> app -> /app/uploads
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=List[ProductResponse])
def get_products(
    category: str = None,
    gender: str = None,
    search: str = None,
    sort: str = None,
    featured: bool = None,
    new_arrival: bool = None,
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.is_active == True)
    if category:
        query = query.filter(Product.category == category)
    if gender:
        query = query.filter(Product.gender == gender)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if featured is not None:
        query = query.filter(Product.is_featured == featured)
    if new_arrival is not None:
        query = query.filter(Product.is_new_arrival == new_arrival)
    if sort == "price_asc":
        query = query.order_by(Product.discount_price.asc().nullslast(), Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.discount_price.desc().nullslast(), Product.price.desc())
    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.created_at.desc())
    return query.all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.post("/upload", response_model=dict)
def upload_image(
    file: UploadFile = File(...),
    admin=Depends(get_current_admin),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        raise HTTPException(status_code=400, detail="Only image files (jpg, png, gif, webp) are allowed")
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    return {"url": f"/uploads/{filename}", "filename": filename}


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}