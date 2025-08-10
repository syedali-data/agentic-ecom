"""
Database configuration and connection handling for Agentic-Ecom.
Provides SQLAlchemy engine, session management, and database utilities.
"""

import os
import logging
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./agentic_ecom.db"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.
    Yields a database session and ensures it's closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database by creating all tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        raise

def check_db_connection() -> bool:
    """Check if database connection is working."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def get_db_stats() -> dict:
    """Get database statistics."""
    try:
        with engine.connect() as connection:
            # Get table counts
            tables = [
                'products', 'customers', 'orders', 'order_items',
                'support_tickets', 'ad_campaigns', 'inventory_items',
                'pricing_history', 'agent_sessions', 'audit_logs', 'event_logs'
            ]
            
            stats = {}
            for table in tables:
                try:
                    result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    stats[table] = count
                except:
                    stats[table] = 0
            
            return stats
    except Exception as e:
        logger.error(f"❌ Error getting database stats: {e}")
        return {}

def health_check() -> dict:
    """Perform database health check."""
    connection_ok = check_db_connection()
    stats = get_db_stats() if connection_ok else {}
    
    return {
        "status": "healthy" if connection_ok else "unhealthy",
        "connection": connection_ok,
        "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL,
        "stats": stats
    }

if __name__ == "__main__":
    # Test database connection
    print("🔍 Testing database connection...")
    health = health_check()
    print(f"Status: {health['status']}")
    print(f"Connection: {health['connection']}")
    print(f"Database: {health['database_url']}")
    if health['stats']:
        print("📊 Table counts:")
        for table, count in health['stats'].items():
            print(f"  {table}: {count}") 