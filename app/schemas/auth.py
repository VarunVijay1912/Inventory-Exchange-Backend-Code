from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str