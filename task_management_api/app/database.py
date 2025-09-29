"""
Database configuration and session management - MySQL Version
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os
import logging

from .models.task import Base
from .models.user import User  # Import User model to create table

logger = logging.getLogger(__name__)

# MySQL Database URL from environment or default
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:password@localhost:3306/task_management"
)

# Create engine with MySQL-specific settings
engine = create_engine(
    DATABASE_URL,
    # MySQL specific settings
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections every hour
    echo=False,          # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise


def get_db_session() -> Session:
    """Get database session"""
    return SessionLocal()


@contextmanager
def get_db_context():
    """Database session context manager"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency for FastAPI
def get_db():
    """FastAPI dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            logger.info("Database connection successful!")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
