import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from sqlalchemy import create_engine
from app.database import Base
from app.config import settings
from app.models import *

def init_database():
    """Initialize database tables"""
    try:
        print("Connecting to database...")
        engine = create_engine(settings.database_url)
        
        print("Creating database tables...")
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Print created tables
        print("\n📋 Created tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
        
        return True
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n🎉 Database initialization completed!")
    else:
        print("\n❌ Database initialization failed!")
        sys.exit(1)