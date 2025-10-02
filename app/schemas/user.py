from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import UserType

class UserBase(BaseModel):
    email: EmailStr
    phone: str = Field(..., pattern=r'^\+?1?\d{9,15}$')
    company_name: str
    contact_person: str
    gst_number: str = Field(..., pattern=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')
    business_license: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = Field(None, pattern=r'^\d{6}$')
    user_type: UserType = UserType.both

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = Field(None, pattern=r'^\d{6}$')
    user_type: Optional[UserType] = None

class User(UserBase):
    id: UUID
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserProfile(User):
    pass