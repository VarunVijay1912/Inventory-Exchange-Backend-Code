import uvicorn
import os

if __name__ == "__main__":
    # Ensure upload directories exist
    os.makedirs("uploads/products", exist_ok=True)
    os.makedirs("uploads/documents", exist_ok=True)
    
    print("Starting Manufacturing Marketplace API Server...")
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("Redoc Documentation: http://127.0.0.1:8000/redoc")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["app"]
    )