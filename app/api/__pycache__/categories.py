from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.category import Category, Material
from app.models.category import Category as CategoryModel, Material as MaterialModel

router = APIRouter()

@router.get("/", response_model=List[Category])
async def list_categories(db: Session = Depends(get_db)):
    categories = db.query(CategoryModel).filter(CategoryModel.is_active == True).all()
    return categories

@router.get("/materials", response_model=List[Material])
async def list_materials(db: Session = Depends(get_db)):
    materials = db.query(MaterialModel).filter(MaterialModel.is_active == True).all()
    return materials