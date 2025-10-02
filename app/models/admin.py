from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum
from app.database import Base

class AdminRole(str, enum.Enum):
    super_admin = "super_admin"
    moderator = "moderator"

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(AdminRole), default=AdminRole.moderator)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)