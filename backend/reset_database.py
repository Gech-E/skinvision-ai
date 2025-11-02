"""
Reset Database Script
Deletes the existing database and recreates it with the current schema.

WARNING: This will delete all existing data!
Use this only in development when you don't need to preserve data.
"""
import os
from app.database import DATABASE_URL, Base, engine

def reset_database():
    """Delete and recreate the database."""
    print("⚠️  WARNING: This will delete all existing data!")
    print(f"Database location: {DATABASE_URL}")
    
    # Extract database file path
    if DATABASE_URL.startswith("sqlite:///"):
        db_path = DATABASE_URL.replace("sqlite:///", "").replace("./", "")
        
        if os.path.exists(db_path):
            print(f"\n🗑️  Deleting database file: {db_path}")
            os.remove(db_path)
            print("✅ Database file deleted")
        else:
            print(f"\nℹ️  Database file doesn't exist: {db_path}")
    
    # Create new database with current schema
    print("\n🔨 Creating new database with current schema...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database created successfully!")
    print("\n📊 Schema includes:")
    print("   - Users table with: id, email, hashed_password, role, phone_number, email_notifications, sms_notifications")
    print("   - Predictions table with: id, image_url, predicted_class, confidence, heatmap_url, timestamp, user_id, email_sent, sms_sent")

if __name__ == "__main__":
    try:
        reset_database()
    except Exception as e:
        print(f"\n❌ Reset failed: {e}")
        import traceback
        traceback.print_exc()
