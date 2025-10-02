from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Numeric, Date, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum
from app.database import Base

class ProductCondition(str, enum.Enum):
    new = "new"
    like_new = "like_new"
    good = "good"
    fair = "fair"
    poor = "poor"

class ProductStatus(str, enum.Enum):
    active = "active"
    sold = "sold"
    reserved = "reserved"
    inactive = "inactive"

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    material_id = Column(UUID(as_uuid=True), ForeignKey("materials.id"))
    quantity = Column(Integer, nullable=False)
    unit = Column(String)  # kg, pieces, meters, etc.
    price = Column(Numeric(10, 2))
    price_negotiable = Column(Boolean, default=True)
    condition = Column(Enum(ProductCondition), default=ProductCondition.good)
    manufacturing_date = Column(Date)
    location_city = Column(String)
    location_state = Column(String)
    pincode = Column(String)
    specifications = Column(JSONB)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    status = Column(Enum(ProductStatus), default=ProductStatus.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    seller = relationship("User", back_populates="products")
    category = relationship("Category", back_populates="products")
    material = relationship("Material", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="product")

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    image_path = Column(String, nullable=False)
    image_name = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    file_size = Column(Integer)
    mime_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="images")