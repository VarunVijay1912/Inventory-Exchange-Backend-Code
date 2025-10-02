import os
import uuid
from PIL import Image
from typing import Optional, Tuple
from fastapi import UploadFile

THUMBNAIL_SIZE = (200, 200)
MEDIUM_SIZE = (800, 600)

def create_directory(path: str):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)

def process_product_image(file: UploadFile, product_id: str, upload_dir: str) -> dict:
    """Process and save product image with multiple sizes"""
    # Generate unique filename
    file_extension = file.filename.split('.')[-1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Create directories
    product_dir = os.path.join(upload_dir, "products", product_id)
    original_dir = os.path.join(product_dir, "original")
    medium_dir = os.path.join(product_dir, "medium")
    thumb_dir = os.path.join(product_dir, "thumbnail")
    
    create_directory(original_dir)
    create_directory(medium_dir)
    create_directory(thumb_dir)
    
    # Save original
    original_path = os.path.join(original_dir, unique_filename)
    with open(original_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    # Create resized versions
    with Image.open(original_path) as img:
        # Convert to RGB if necessary
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Create medium size
        img_medium = img.copy()
        img_medium.thumbnail(MEDIUM_SIZE, Image.Resampling.LANCZOS)
        medium_path = os.path.join(medium_dir, unique_filename)
        img_medium.save(medium_path, optimize=True, quality=85)
        
        # Create thumbnail
        img_thumb = img.copy()
        img_thumb.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        thumb_path = os.path.join(thumb_dir, unique_filename)
        img_thumb.save(thumb_path, optimize=True, quality=80)
    
    return {
        "filename": unique_filename,
        "original_path": original_path,
        "medium_path": medium_path,
        "thumbnail_path": thumb_path,
        "file_size": os.path.getsize(original_path)
    }