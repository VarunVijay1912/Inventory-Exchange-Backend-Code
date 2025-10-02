from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_active_user, get_current_verified_user
from app.schemas.product import Product, ProductCreate, ProductUpdate, ProductListItem
from app.models.product import Product as ProductModel  # SQLAlchemy model
from app.services.product_service import ProductService
from app.utils.image_processing import process_product_image
from app.config import settings
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_create: ProductCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    product = ProductService.create_product(db, product_create, current_user.id)
    return product

@router.get("/", response_model=List[ProductListItem])
async def list_products(
    query: Optional[str] = None,
    category_id: Optional[UUID] = None,
    material_id: Optional[UUID] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    condition: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    products = ProductService.search_products(
        db, query, category_id, material_id, city, state,
        min_price, max_price, condition, sort_by, sort_order, skip, limit
    )
    
    # Convert to list items with primary image
    result = []
    for product in products:
        primary_image = next((img for img in product.images if img.is_primary), None)
        if not primary_image and product.images:
            primary_image = product.images[0]
        
        item = ProductListItem(
            id=product.id,
            title=product.title,
            price=product.price,
            price_negotiable=product.price_negotiable,
            condition=product.condition,
            location_city=product.location_city,
            location_state=product.location_state,
            views_count=product.views_count,
            status=product.status,
            created_at=product.created_at,
            primary_image=primary_image.image_path if primary_image else None
        )
        result.append(item)
    
    return result

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = ProductService.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Increment views
    ProductService.increment_views(db, product_id)
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: UUID,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    product = ProductService.update_product(db, product_id, product_update, current_user.id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or not authorized"
        )
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    success = ProductService.delete_product(db, product_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or not authorized"
        )

@router.post("/{product_id}/images")
async def upload_product_images(
    product_id: UUID,
    files: List[UploadFile] = File(...),
    is_primary: Optional[bool] = Form(False),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    # Verify product ownership
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id,
        ProductModel.seller_id == current_user.id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or not authorized"
        )
    
    uploaded_images = []
    for i, file in enumerate(files):
        # Validate file
        if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            continue
        
        # Process image
        image_data = process_product_image(file, str(product_id), settings.upload_directory)
        image_data["is_primary"] = is_primary and i == 0  # Only first image can be primary
        image_data["mime_type"] = file.content_type
        
        # Save to database
        db_image = ProductService.add_product_image(db, product_id, image_data)
        uploaded_images.append(db_image)
    
    return {"uploaded_count": len(uploaded_images), "images": uploaded_images}

@router.get("/my-products/", response_model=List[ProductListItem])
async def get_my_products(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    products = db.query(ProductModel).filter(
        ProductModel.seller_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    # Convert to list items
    result = []
    for product in products:
        primary_image = next((img for img in product.images if img.is_primary), None)
        if not primary_image and product.images:
            primary_image = product.images[0]
        
        item = ProductListItem(
            id=product.id,
            title=product.title,
            price=product.price,
            price_negotiable=product.price_negotiable,
            condition=product.condition,
            location_city=product.location_city,
            location_state=product.location_state,
            views_count=product.views_count,
            status=product.status,
            created_at=product.created_at,
            primary_image=primary_image.image_path if primary_image else None
        )
        result.append(item)
    
    return result