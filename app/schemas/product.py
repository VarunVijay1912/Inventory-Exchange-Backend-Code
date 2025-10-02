from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID
from app.models.product import ProductCondition, ProductStatus

class ProductImageBase(BaseModel):
    image_name: str
    is_primary: bool = False

class ProductImage(ProductImageBase):
    id: UUID
    product_id: UUID
    image_path: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    category_id: UUID
    material_id: Optional[UUID] = None
    quantity: int = Field(..., gt=0)
    unit: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    price_negotiable: bool = True
    condition: ProductCondition = ProductCondition.good
    manufacturing_date: Optional[date] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    pincode: Optional[str] = Field(None, pattern=r'^\d{6}$')
    specifications: Optional[Dict[str, Any]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    category_id: Optional[UUID] = None
    material_id: Optional[UUID] = None
    quantity: Optional[int] = Field(None, gt=0)
    unit: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    price_negotiable: Optional[bool] = None
    condition: Optional[ProductCondition] = None
    manufacturing_date: Optional[date] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    pincode: Optional[str] = Field(None, pattern=r'^\d{6}$')
    specifications: Optional[Dict[str, Any]] = None
    status: Optional[ProductStatus] = None

class Product(ProductBase):
    id: UUID
    seller_id: UUID
    is_active: bool
    is_featured: bool
    views_count: int
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
    images: List[ProductImage] = []

    model_config = ConfigDict(from_attributes=True)

class ProductListItem(BaseModel):
    id: UUID
    title: str
    price: Optional[Decimal]
    price_negotiable: bool
    condition: ProductCondition
    location_city: Optional[str]
    location_state: Optional[str]
    views_count: int
    status: ProductStatus
    created_at: datetime
    primary_image: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)