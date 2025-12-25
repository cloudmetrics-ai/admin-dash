"""
Database Configuration and Session Management
==============================================

This module sets up the database connection, session management, and base model
for SQLAlchemy ORM.

Key Components:
- Database engine configuration
- Session factory for database operations
- Base class for all database models
- Dependency injection for FastAPI routes
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings


# ============================================================================
# DATABASE ENGINE CONFIGURATION
# ============================================================================

# Create SQLAlchemy engine
# - The engine is the starting point for any SQLAlchemy application
# - It manages connections to the database
# - pool_pre_ping=True ensures connections are valid before using them
# - echo=True logs all SQL statements (useful for debugging, disable in production)

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using them
    pool_size=settings.DB_POOL_SIZE,  # Number of connections to keep open
    max_overflow=settings.DB_MAX_OVERFLOW,  # Max connections beyond pool_size
    echo=False,  # Set to True to log SQL statements (for debugging)
)


# ============================================================================
# SESSION FACTORY
# ============================================================================

# Create a SessionLocal class
# - Each instance of SessionLocal will be a database session
# - autocommit=False: Don't automatically commit transactions
# - autoflush=False: Don't automatically flush changes to the database
# - bind=engine: Bind this session factory to our database engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================================
# BASE MODEL CLASS
# ============================================================================

# Create a Base class for all database models
# - All SQLAlchemy models will inherit from this Base class
# - This allows Alembic to auto-detect models for migrations
# - Provides common functionality to all models

Base = declarative_base()


# ============================================================================
# DATABASE DEPENDENCY FOR FASTAPI
# ============================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI routes
    
    This function is used as a dependency in FastAPI routes to provide
    a database session. It ensures proper session management:
    
    1. Creates a new session for each request
    2. Yields the session to the route handler
    3. Automatically closes the session after the request completes
    4. Handles exceptions and rollbacks if needed
    
    Usage in FastAPI routes:
        @router.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        ```python
        from fastapi import Depends
        from app.core.database import get_db
        
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
        ```
    """
    # Create a new database session
    db = SessionLocal()
    
    try:
        # Yield the session to the route handler
        # The route handler can now use this session for database operations
        yield db
        
    finally:
        # Always close the session after the request completes
        # This ensures connections are returned to the pool
        # and prevents connection leaks
        db.close()


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db() -> None:
    """
    Initialize the database
    
    This function creates all database tables defined in the models.
    It should be called when the application starts.
    
    Note: In production, use Alembic migrations instead of this function.
    This is mainly useful for development and testing.
    
    Usage:
        from app.core.database import init_db
        init_db()  # Creates all tables
    """
    # Import all models here to ensure they are registered with Base
    # This is necessary for Base.metadata.create_all() to work
    from app.models import user  # noqa: F401
    from app.models import role  # noqa: F401
    # TODO: Uncomment when chat and message models are created
    # from app.models import chat, message  # noqa: F401
    
    # Create all tables in the database
    # This will only create tables that don't already exist
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """
    Drop all database tables
    
    WARNING: This will delete all data in the database!
    Only use this in development/testing environments.
    
    Usage:
        from app.core.database import drop_db
        drop_db()  # Drops all tables
    """
    # Drop all tables from the database
    # WARNING: This is destructive and will delete all data!
    Base.metadata.drop_all(bind=engine)


# ============================================================================
# DATABASE HEALTH CHECK
# ============================================================================

def check_db_connection() -> bool:
    """
    Check if the database connection is working
    
    This function attempts to execute a simple query to verify
    the database connection is active and working.
    
    Returns:
        bool: True if connection is successful, False otherwise
        
    Example:
        ```python
        if check_db_connection():
            print("Database is connected!")
        else:
            print("Database connection failed!")
        ```
    """
    try:
        # Create a temporary session
        db = SessionLocal()
        
        # Execute a simple query to test the connection
        # This will raise an exception if the connection fails
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        
        # Close the session
        db.close()
        
        return True
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Database connection failed: {e}")
        return False


# ============================================================================
# TRANSACTION CONTEXT MANAGER
# ============================================================================

class DatabaseTransaction:
    """
    Context manager for database transactions
    
    This class provides a convenient way to handle database transactions
    with automatic commit/rollback.
    
    Usage:
        ```python
        with DatabaseTransaction() as db:
            user = User(email="test@example.com")
            db.add(user)
            # Transaction is automatically committed when exiting the context
            # If an exception occurs, the transaction is rolled back
        ```
    """
    
    def __init__(self):
        """Initialize the transaction context manager"""
        self.db: Session = SessionLocal()
    
    def __enter__(self) -> Session:
        """
        Enter the context manager
        
        Returns:
            Session: Database session for the transaction
        """
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager
        
        If an exception occurred, rollback the transaction.
        Otherwise, commit the transaction.
        Always close the session.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        if exc_type is not None:
            # An exception occurred, rollback the transaction
            self.db.rollback()
        else:
            # No exception, commit the transaction
            self.db.commit()
        
        # Always close the session
        self.db.close()
