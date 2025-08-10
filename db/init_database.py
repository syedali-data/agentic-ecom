#!/usr/bin/env python3
"""
Database initialization and management script for Agentic-Ecom.
Provides commands for creating tables, seeding data, and database maintenance.
"""

import argparse
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from db.database import init_db, health_check, get_db_stats
from db.seeds.sample_data import seed_sample_data
from db.models import Base
from sqlalchemy.orm import Session
from db.database import SessionLocal

def init_database():
    """Initialize database tables."""
    print("🗄️ Initializing database...")
    try:
        init_db()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def seed_database():
    """Seed database with sample data."""
    print("🌱 Seeding database with sample data...")
    try:
        db = SessionLocal()
        stats = seed_sample_data(db)
        db.close()
        
        print("✅ Sample data seeded successfully!")
        print("📊 Seeded data summary:")
        for table, count in stats.items():
            print(f"  {table}: {count}")
        return True
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        return False

def show_database_info():
    """Show database information and statistics."""
    print("🔍 Database Information:")
    
    # Health check
    health = health_check()
    print(f"Status: {health['status']}")
    print(f"Connection: {'✅ Connected' if health['connection'] else '❌ Failed'}")
    print(f"Database: {health['database_url']}")
    
    # Statistics
    if health['stats']:
        print("\n📊 Table Statistics:")
        for table, count in health['stats'].items():
            print(f"  {table}: {count} records")
    else:
        print("\n📊 No data available")

def reset_database():
    """Reset database by dropping and recreating all tables."""
    print("🔄 Resetting database...")
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=SessionLocal().bind)
        print("✅ All tables dropped")
        
        # Recreate tables
        init_db()
        print("✅ Tables recreated")
        
        # Seed with sample data
        seed_database()
        
        print("✅ Database reset completed!")
        return True
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        return False

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Agentic-Ecom Database Management")
    parser.add_argument(
        "--action", 
        choices=["init", "seed", "info", "reset", "full-setup"],
        default="info",
        help="Action to perform"
    )
    
    args = parser.parse_args()
    
    print("🚀 Agentic-Ecom Database Manager")
    print("=" * 40)
    
    if args.action == "init":
        success = init_database()
        sys.exit(0 if success else 1)
    
    elif args.action == "seed":
        success = seed_database()
        sys.exit(0 if success else 1)
    
    elif args.action == "info":
        show_database_info()
        sys.exit(0)
    
    elif args.action == "reset":
        confirm = input("⚠️ This will delete ALL data. Are you sure? (yes/no): ")
        if confirm.lower() == "yes":
            success = reset_database()
            sys.exit(0 if success else 1)
        else:
            print("❌ Reset cancelled")
            sys.exit(0)
    
    elif args.action == "full-setup":
        print("🔧 Full database setup...")
        success = init_database() and seed_database()
        if success:
            print("\n🎉 Full setup completed successfully!")
            show_database_info()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 