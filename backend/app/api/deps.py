"""
API Dependencies
=================

This module provides dependency injection functions for FastAPI routes.
Dependencies are used to:
- Get database sessions
- Authenticate users
- Check permissions
- Validate tokens

These dependencies can be injected into route handlers using FastAPI's
Depends() function.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.schemas.token import TokenPayload


# ============================================================================
# SECURITY SCHEME
# ============================================================================

# HTTP Bearer token security scheme
# This tells FastAPI to expect an Authorization header with a Bearer token
# Format: Authorization: Bearer <token>
security = HTTPBearer()


# ============================================================================
# GET CURRENT USER DEPENDENCY
# ============================================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from the JWT token
    
    This dependency:
    1. Extracts the JWT token from the Authorization header
    2. Decodes and validates the token
    3. Retrieves the user from the database
    4. Returns the user object
    
    Args:
        credentials: HTTP Bearer credentials (contains the token)
        db: Database session
        
    Returns:
        User: The authenticated user object
        
    Raises:
        HTTPException: If token is invalid or user not found
        
    Usage in routes:
        ```python
        @router.get("/me")
        def get_me(current_user: User = Depends(get_current_user)):
            return current_user
        ```
    """
    
    # Extract the token from credentials
    token = credentials.credentials
    
    # Decode the token to get the payload
    payload = decode_token(token)
    
    # Check if token is valid
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user email from token payload
    # The 'sub' (subject) field contains the user's email
    user_email: str = payload.get("sub")
    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Query the database for the user
    user = db.query(User).filter(User.email == user_email).first()
    
    # Check if user exists
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


# ============================================================================
# GET CURRENT ACTIVE USER DEPENDENCY
# ============================================================================

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current active user
    
    This dependency ensures the user is both authenticated and active.
    It's a wrapper around get_current_user that adds an additional check.
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        User: The active user object
        
    Raises:
        HTTPException: If user is inactive
        
    Usage:
        ```python
        @router.get("/protected")
        def protected_route(user: User = Depends(get_current_active_user)):
            return {"message": f"Hello {user.email}"}
        ```
    """
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return current_user


# ============================================================================
# GET CURRENT SUPERUSER DEPENDENCY
# ============================================================================

async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current superuser
    
    This dependency ensures the user is authenticated and has superuser privileges.
    Use this for admin-only endpoints.
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        User: The superuser object
        
    Raises:
        HTTPException: If user is not a superuser
        
    Usage:
        ```python
        @router.delete("/users/{user_id}")
        def delete_user(
            user_id: str,
            admin: User = Depends(get_current_superuser)
        ):
            # Only superusers can access this endpoint
            pass
        ```
    """
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Superuser access required."
        )
    
    return current_user


# ============================================================================
# OPTIONAL AUTHENTICATION DEPENDENCY
# ============================================================================

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise return None
    
    This dependency allows endpoints to be accessed both with and without authentication.
    Useful for endpoints that provide different data based on authentication status.
    
    Args:
        credentials: Optional HTTP Bearer credentials
        db: Database session
        
    Returns:
        Optional[User]: User object if authenticated, None otherwise
        
    Usage:
        ```python
        @router.get("/posts")
        def get_posts(user: Optional[User] = Depends(get_current_user_optional)):
            if user:
                # Return user-specific posts
                pass
            else:
                # Return public posts
                pass
        ```
    """
    
    # If no credentials provided, return None
    if credentials is None:
        return None
    
    # Try to get the user
    try:
        token = credentials.credentials
        payload = decode_token(token)
        
        if payload is None:
            return None
        
        user_email = payload.get("sub")
        if user_email is None:
            return None
        
        user = db.query(User).filter(User.email == user_email).first()
        return user
        
    except Exception:
        # If any error occurs, return None instead of raising an exception
        return None


# ============================================================================
# PAGINATION DEPENDENCY
# ============================================================================

class PaginationParams:
    """
    Pagination parameters dependency
    
    Provides common pagination parameters for list endpoints.
    
    Attributes:
        skip: Number of records to skip (for offset pagination)
        limit: Maximum number of records to return
        
    Usage:
        ```python
        @router.get("/users")
        def get_users(
            pagination: PaginationParams = Depends(),
            db: Session = Depends(get_db)
        ):
            users = db.query(User).offset(pagination.skip).limit(pagination.limit).all()
            return users
        ```
    """
    
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100
    ):
        """
        Initialize pagination parameters
        
        Args:
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100, max: 1000)
        """
        self.skip = max(0, skip)  # Ensure skip is not negative
        self.limit = min(limit, 1000)  # Cap limit at 1000 to prevent abuse


# ============================================================================
# RATE LIMITING DEPENDENCY (Placeholder)
# ============================================================================

async def check_rate_limit(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Check rate limiting for the current user
    
    This is a placeholder for rate limiting functionality.
    In production, you would implement actual rate limiting logic here
    using Redis or a similar solution.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: The user object if rate limit not exceeded
        
    Raises:
        HTTPException: If rate limit is exceeded
        
    TODO: Implement actual rate limiting logic
    """
    
    # Placeholder - implement actual rate limiting
    # Example: Check Redis for request count
    # If exceeded, raise HTTPException with status 429 (Too Many Requests)
    
    return current_user
