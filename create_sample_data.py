import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Category, Material  # Import from models package
from app.utils.security import get_password_hash

def create_sample_data():
    """Create sample data for testing"""
    db = SessionLocal()
    
    try:
        print("Creating sample data...")
        
        # Create sample categories
        categories_data = [
            {"name": "Textile Machinery Parts", "slug": "textile-machinery-parts", "description": "Parts and components for textile manufacturing machines"},
            {"name": "Automobile Parts", "slug": "automobile-parts", "description": "Automotive components and spare parts"},
            {"name": "Raw Materials", "slug": "raw-materials", "description": "Raw materials including rods, bars, sheets"},
            {"name": "Hydraulic Components", "slug": "hydraulic-components", "description": "Hydraulic pumps, cylinders, valves and components"},
        ]
        
        created_categories = 0
        for cat_data in categories_data:
            existing_cat = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
            if not existing_cat:
                category = Category(**cat_data)
                db.add(category)
                created_categories += 1
                print(f"✅ Created category: {cat_data['name']}")
        
        # Create sample materials
        materials_data = [
            {"name": "Steel", "slug": "steel", "description": "Various grades of steel"},
            {"name": "Aluminum", "slug": "aluminum", "description": "Aluminum alloys and components"},
            {"name": "Plastic", "slug": "plastic", "description": "Various plastic materials and components"},
            {"name": "Rubber", "slug": "rubber", "description": "Rubber components and materials"},
            {"name": "Copper", "slug": "copper", "description": "Copper and copper alloys"},
        ]
        
        created_materials = 0
        for mat_data in materials_data:
            existing_mat = db.query(Material).filter(Material.slug == mat_data["slug"]).first()
            if not existing_mat:
                material = Material(**mat_data)
                db.add(material)
                created_materials += 1
                print(f"✅ Created material: {mat_data['name']}")
        
        # Create sample user
        existing_user = db.query(User).filter(User.email == "demo@manufacturer.com").first()
        if not existing_user:
            sample_user = User(
                email="demo@manufacturer.com",
                phone="+919876543210",
                password_hash=get_password_hash("demo123"),
                company_name="Demo Manufacturing Ltd",
                contact_person="John Doe",
                gst_number="09ABCDE1234F1Z5",
                address="Demo Address, Industrial Area",
                city="Mumbai",
                state="Maharashtra",
                pincode="400001",
                is_verified=True,
                is_active=True
            )
            db.add(sample_user)
            print("✅ Created demo user: demo@manufacturer.com")
        else:
            print("ℹ️  Demo user already exists")
        
        # Create second sample user
        existing_user2 = db.query(User).filter(User.email == "buyer@company.com").first()
        if not existing_user2:
            sample_user2 = User(
                email="buyer@company.com",
                phone="+919876543211",
                password_hash=get_password_hash("buyer123"),
                company_name="Buyer Company Ltd",
                contact_person="Jane Smith",
                gst_number="09ABCDE1234F1Z6",
                address="Buyer Address, Commercial Area",
                city="Delhi",
                state="Delhi",
                pincode="110001",
                is_verified=True,
                is_active=True
            )
            db.add(sample_user2)
            print("✅ Created demo buyer: buyer@company.com")
        else:
            print("ℹ️  Demo buyer already exists")
        
        db.commit()
        print("\n🎉 Sample data created successfully!")
        
        # Print summary
        print(f"\n📊 Summary:")
        print(f"Categories created: {created_categories}")
        print(f"Materials created: {created_materials}")
        print(f"Total categories: {db.query(Category).count()}")
        print(f"Total materials: {db.query(Material).count()}")
        print(f"Total users: {db.query(User).count()}")
        
        # Print demo credentials
        print("\n📋 Demo Credentials:")
        print("Seller Account:")
        print("  Email: demo@manufacturer.com")
        print("  Password: demo123")
        print("  GST: 09ABCDE1234F1Z5")
        print("\nBuyer Account:")
        print("  Email: buyer@company.com")
        print("  Password: buyer123")
        print("  GST: 09ABCDE1234F1Z6")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    try:
        create_sample_data()
    except Exception as e:
        print(f"Failed to create sample data: {e}")
        sys.exit(1)