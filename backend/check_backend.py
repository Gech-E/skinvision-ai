"""Quick script to check backend setup"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.database import engine, Base
    from app import models
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created")
    
    # Test imports
    from app.routers import auth, predict, history
    print("[OK] All routers imported successfully")
    
    from app.main import app
    print("[OK] FastAPI app imported successfully")
    
    print("\n[OK] Backend is ready!")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
