from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, asc
from app.models.product import Product, ProductImage
from app.models.category import Category, Material
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate
from typing import Optional, List, Dict, Any
from uuid import UUID

class ProductService:
    @staticmethod
    def create_product(db: Session, product_create: ProductCreate, seller_id: UUID) -> Product:
        db_product = Product(
            seller_id=seller_id,
            **product_create.model_dump()
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def get_product(db: Session, product_id: UUID) -> Optional[Product]:
        return db.query(Product).options(
            joinedload(Product.images),
            joinedload(Product.seller),
            joinedload(Product.category),
            joinedload(Product.material)
        ).filter(Product.id == product_id).first()

    @staticmethod
    def update_product(db: Session, product_id: UUID, product_update: ProductUpdate, user_id: UUID) -> Optional[Product]:
        product = db.query(Product).filter(
            and_(Product.id == product_id, Product.seller_id == user_id)
        ).first()
        
        if not product:
            return None
        
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product_id: UUID, user_id: UUID) -> bool:
        product = db.query(Product).filter(
            and_(Product.id == product_id, Product.seller_id == user_id)
        ).first()
        
        if not product:
            return False
        
        db.delete(product)
        db.commit()
        return True

    @staticmethod
    def search_products(
        db: Session,
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
        limit: int = 20
    ) -> List[Product]:
        
        query_filter = db.query(Product).filter(Product.is_active == True)
        
        if query:
            query_filter = query_filter.filter(
                or_(
                    Product.title.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%")
                )
            )
        
        if category_id:
            query_filter = query_filter.filter(Product.category_id == category_id)
        
        if material_id:
            query_filter = query_filter.filter(Product.material_id == material_id)
        
        if city:
            query_filter = query_filter.filter(Product.location_city.ilike(f"%{city}%"))
        
        if state:
            query_filter = query_filter.filter(Product.location_state.ilike(f"%{state}%"))
        
        if min_price:
            query_filter = query_filter.filter(Product.price >= min_price)
        
        if max_price:
            query_filter = query_filter.filter(Product.price <= max_price)
        
        if condition:
            query_filter = query_filter.filter(Product.condition == condition)
        
        # Sorting
        if sort_order == "desc":
            order_by = desc(getattr(Product, sort_by))
        else:
            order_by = asc(getattr(Product, sort_by))
        
        return query_filter.options(
            joinedload(Product.images)
        ).order_by(order_by).offset(skip).limit(limit).all()

    @staticmethod
    def increment_views(db: Session, product_id: UUID):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.views_count += 1
            db.commit()

    @staticmethod
    def add_product_image(db: Session, product_id: UUID, image_data: dict) -> ProductImage:
        # Set all other images as non-primary if this is primary
        if image_data.get("is_primary", False):
            db.query(ProductImage).filter(ProductImage.product_id == product_id).update(
                {"is_primary": False}
            )
        
        db_image = ProductImage(
            product_id=product_id,
            image_path=image_data["original_path"],
            image_name=image_data["filename"],
            is_primary=image_data.get("is_primary", False),
            file_size=image_data["file_size"],
            mime_type=image_data.get("mime_type")
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image