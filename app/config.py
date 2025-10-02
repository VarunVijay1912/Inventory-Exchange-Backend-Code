import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    upload_directory: str = "./uploads"
    max_file_size: int = 10485760  # 10MB
    allowed_image_types_str: str = "jpg,jpeg,png,webp"
    gst_verification_api_key: str

    class Config:
        env_file = ".env"
        
    @property
    def allowed_image_types(self) -> List[str]:
        return [ext.strip() for ext in self.allowed_image_types_str.split(",")]

settings = Settings()