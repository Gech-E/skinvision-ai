"""
Database Migration Script
Adds missing columns to existing database tables.

Run this script once to update your database schema.
"""
import os
import sys
import io
from sqlalchemy import create_engine, text, inspect
from app.database import DATABASE_URL, Base, engine
from app.models import User, Prediction

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def column_exists(table_name, column_name, inspector):
    """Check if a column exists in a table."""
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def migrate_database():
    """Add missing columns to database if they don't exist."""
    print("Starting database migration...")
    print(f"Database: {DATABASE_URL}")
    
    inspector = inspect(engine)
    
    # Check if users table exists
    if 'users' not in inspector.get_table_names():
        print("WARNING: Users table doesn't exist. Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("SUCCESS: Database created with new schema!")
        return
    
    # Check and add columns to users table
    users_updates = []
    
    if not column_exists('users', 'phone_number', inspector):
        users_updates.append("ADD COLUMN phone_number VARCHAR")
        print("  + Adding phone_number column to users table...")
    
    if not column_exists('users', 'email_notifications', inspector):
        users_updates.append("ADD COLUMN email_notifications VARCHAR DEFAULT 'true'")
        print("  + Adding email_notifications column to users table...")
    
    if not column_exists('users', 'sms_notifications', inspector):
        users_updates.append("ADD COLUMN sms_notifications VARCHAR DEFAULT 'false'")
        print("  + Adding sms_notifications column to users table...")
    
    # Check and add columns to predictions table
    predictions_updates = []
    
    if not column_exists('predictions', 'email_sent', inspector):
        predictions_updates.append("ADD COLUMN email_sent VARCHAR DEFAULT 'false'")
        print("  + Adding email_sent column to predictions table...")
    
    if not column_exists('predictions', 'sms_sent', inspector):
        predictions_updates.append("ADD COLUMN sms_sent VARCHAR DEFAULT 'false'")
        print("  + Adding sms_sent column to predictions table...")
    
    # Apply migrations
    if users_updates or predictions_updates:
        with engine.connect() as conn:
            if users_updates:
                for update in users_updates:
                    try:
                        conn.execute(text(f"ALTER TABLE users {update}"))
                        conn.commit()
                        print(f"  SUCCESS: {update}")
                    except Exception as e:
                        print(f"  WARNING: Error applying {update}: {e}")
                        conn.rollback()
            
            if predictions_updates:
                for update in predictions_updates:
                    try:
                        conn.execute(text(f"ALTER TABLE predictions {update}"))
                        conn.commit()
                        print(f"  SUCCESS: {update}")
                    except Exception as e:
                        print(f"  WARNING: Error applying {update}: {e}")
                        conn.rollback()
        
        print("\nSUCCESS: Migration completed successfully!")
    else:
        print("SUCCESS: Database is up to date. No migrations needed.")
    
    # Verify schema
    print("\nCurrent schema:")
    inspector = inspect(engine)
    users_columns = [col['name'] for col in inspector.get_columns('users')]
    predictions_columns = [col['name'] for col in inspector.get_columns('predictions')]
    
    print(f"Users table columns: {', '.join(users_columns)}")
    print(f"Predictions table columns: {', '.join(predictions_columns)}")

if __name__ == "__main__":
    try:
        migrate_database()
    except Exception as e:
        print(f"\nERROR: Migration failed: {e}")
        print("\nTIP: If this persists, you can:")
        print("   1. Delete the database file (skinvision.db) and restart the server")
        print("   2. Or run: python reset_database.py (WARNING: deletes all data)")
        print("   3. Or check the error message above")
        sys.exit(1)
