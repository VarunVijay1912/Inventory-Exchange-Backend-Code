from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash, verify_password
from app.utils.validators import verify_gst_number
from typing import Optional

class AuthService:
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            phone=user_create.phone,
            password_hash=hashed_password,
            company_name=user_create.company_name,
            contact_person=user_create.contact_person,
            gst_number=user_create.gst_number,
            business_license=user_create.business_license,
            address=user_create.address,
            city=user_create.city,
            state=user_create.state,
            pincode=user_create.pincode,
            user_type=user_create.user_type
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_gst(db: Session, gst_number: str) -> Optional[User]:
        return db.query(User).filter(User.gst_number == gst_number).first()

    @staticmethod
    def get_user_by_phone(db: Session, phone: str) -> Optional[User]:
        return db.query(User).filter(User.phone == phone).first()

    @staticmethod
    async def verify_user_gst(db: Session, user_id: str) -> dict:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"success": False, "message": "User not found"}
        
        verification_result = await verify_gst_number(user.gst_number)
        if verification_result["valid"]:
            user.is_verified = True
            db.commit()
            return {"success": True, "message": "GST verified successfully"}
        
        return {"success": False, "message": "GST verification failed"}