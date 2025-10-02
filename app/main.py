from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import auth, users, products, categories, conversations, admin
from app.config import settings
import os

# Create tables
Base.metadata.create_all(bind=engine)

# Create upload directories
upload_dirs = [
    settings.upload_directory,
    os.path.join(settings.upload_directory, "products"),
    os.path.join(settings.upload_directory, "documents")
]

for directory in upload_dirs:
    os.makedirs(directory, exist_ok=True)

app = FastAPI(
    title="Manufacturing Marketplace API",
    description="API for B2B Manufacturing Marketplace",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory=settings.upload_directory), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["Conversations"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Manufacturing Marketplace API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)