from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database import get_db
from app.models.user import User as UserModel  # SQLAlchemy model
from app.models.product import Product as ProductModel  # SQLAlchemy model
from app.schemas.user import User  # Pydantic schema for response
from app.models.admin import AdminUser

router = APIRouter()

# For MVP, we'll keep admin endpoints simple
# In production, add proper admin authentication

@router.get("/dashboard")
async def admin_dashboard(db: Session = Depends(get_db)):
    total_users = db.query(UserModel).count()
    verified_users = db.query(UserModel).filter(UserModel.is_verified == True).count()
    total_products = db.query(ProductModel).count()
    active_products = db.query(ProductModel).filter(ProductModel.is_active == True).count()
    
    return {
        "total_users": total_users,
        "verified_users": verified_users,
        "total_products": total_products,
        "active_products": active_products,
        "verification_pending": total_users - verified_users
    }

@router.get("/users", response_model=List[User])
async def list_users_admin(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.put("/users/{user_id}/verify")
async def verify_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_verified = True
    db.commit()
    return {"message": "User verified successfully"}

@router.put("/users/{user_id}/deactivate")
async def deactivate_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    db.commit()
    return {"message": "User deactivated successfully"}