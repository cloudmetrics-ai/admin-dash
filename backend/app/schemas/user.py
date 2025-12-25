"""
User Pydantic Schemas
======================

This module defines Pydantic models for user data validation and serialization.
These schemas are used for:
- Request validation (ensuring incoming data is correct)
- Response serialization (formatting data sent to clients)
- Data transformation between API and database layers

Pydantic automatically validates data types, required fields, and custom validators.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


# ============================================================================
# BASE USER SCHEMA
# ============================================================================

class UserBase(BaseModel):
    """
    Base User Schema
    
    Contains fields common to all user-related schemas.
    Other schemas inherit from this to avoid code duplication.
    
    Attributes:
        email: User's email address (validated as proper email format)
        username: User's username (optional)
        full_name: User's full name (optional)
    """
    
    # Email field with automatic validation
    # EmailStr ensures the value is a valid email address
    email: EmailStr = Field(
        ...,  # Required field
        description="User's email address",
        example="john.doe@example.com"
    )
    
    # Optional username field
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="User's username (3-50 characters)",
        example="johndoe"
    )
    
    # Optional full name field
    full_name: Optional[str] = Field(
        None,
        max_length=255,
        description="User's full name",
        example="John Doe"
    )


# ============================================================================
# USER CREATION SCHEMA
# ============================================================================

class UserCreate(UserBase):
    """
    User Creation Schema
    
    Used when creating a new user (registration).
    Extends UserBase and adds the password field.
    
    Attributes:
        email: User's email (from UserBase)
        username: User's username (from UserBase)
        full_name: User's full name (from UserBase)
        password: Plain text password (will be hashed before storing)
        
    Example:
        ```python
        user_data = UserCreate(
            email="john@example.com",
            username="johndoe",
            full_name="John Doe",
            password="SecurePass123"
        )
        ```
    """
    
    # Password field - only used during creation
    # The password is validated for strength and then hashed before storage
    password: str = Field(
        ...,  # Required
        min_length=8,
        max_length=100,
        description="User's password (min 8 characters)",
        example="SecurePassword123"
    )
    
    @validator('password')
    def validate_password_strength(cls, v):
        """
        Validate password strength
        
        Ensures the password meets minimum security requirements:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        
        Args:
            v: Password value to validate
            
        Returns:
            str: Validated password
            
        Raises:
            ValueError: If password doesn't meet requirements
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        
        return v
    
    @validator('username')
    def validate_username(cls, v):
        """
        Validate username format
        
        Ensures username only contains alphanumeric characters and underscores.
        
        Args:
            v: Username value to validate
            
        Returns:
            str: Validated username
            
        Raises:
            ValueError: If username contains invalid characters
        """
        if v is not None and not v.replace('_', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v


# ============================================================================
# USER UPDATE SCHEMA
# ============================================================================

class UserUpdate(BaseModel):
    """
    User Update Schema
    
    Used when updating an existing user's information.
    All fields are optional - only provided fields will be updated.
    
    Attributes:
        email: New email address (optional)
        username: New username (optional)
        full_name: New full name (optional)
        password: New password (optional, will be hashed)
        is_active: New active status (optional)
        
    Example:
        ```python
        # Update only the full name
        update_data = UserUpdate(full_name="John Smith")
        
        # Update multiple fields
        update_data = UserUpdate(
            email="newemail@example.com",
            full_name="John Smith"
        )
        ```
    """
    
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    is_active: Optional[bool] = None
    role_id: Optional[int] = None


# ============================================================================
# USER RESPONSE SCHEMA
# ============================================================================

class UserResponse(UserBase):
    """
    User Response Schema
    
    Used when returning user data in API responses.
    Includes all user fields except the password.
    
    Attributes:
        id: User's unique identifier
        email: User's email
        username: User's username
        full_name: User's full name
        is_active: Whether the user is active
        is_superuser: Whether the user is a superuser
        created_at: When the user was created
        updated_at: When the user was last updated
        
    Example:
        ```python
        user_response = UserResponse.from_orm(user)
        # Automatically converts SQLAlchemy model to Pydantic model
        ```
    """
    
    # User ID (UUID)
    id: str = Field(
        ...,
        description="User's unique identifier (UUID)",
        example="123e4567-e89b-12d3-a456-426614174000"
    )
    
    # Permission flags
    is_active: bool = Field(
        ...,
        description="Whether the user account is active"
    )
    
    is_superuser: bool = Field(
        ...,
        description="Whether the user has admin privileges"
    )
    
    # Timestamps
    created_at: datetime = Field(
        ...,
        description="When the user was created"
    )
    
    updated_at: datetime = Field(
        ...,
        description="When the user was last updated"
    )
    
    # Role information
    role_id: Optional[int] = Field(
        None,
        description="ID of the assigned role"
    )
    
    role_display_name: Optional[str] = Field(
        None,
        description="Display name of the assigned role"
    )
    
    class Config:
        """
        Pydantic configuration
        
        - from_attributes: Allow creating Pydantic models from ORM models
        - json_encoders: Custom JSON encoders for specific types
        """
        from_attributes = True  # Allows: UserResponse.from_orm(user)
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Convert datetime to ISO format
        }


# ============================================================================
# USER LIST RESPONSE SCHEMA
# ============================================================================

class UserListResponse(BaseModel):
    """
    User List Response Schema
    
    Used when returning a list of users with pagination information.
    
    Attributes:
        users: List of user objects
        total: Total number of users
        page: Current page number
        page_size: Number of users per page
        
    Example:
        ```python
        response = UserListResponse(
            users=[user1, user2, user3],
            total=100,
            page=1,
            page_size=10
        )
        ```
    """
    
    users: list[UserResponse] = Field(
        ...,
        description="List of users"
    )
    
    total: int = Field(
        ...,
        description="Total number of users",
        example=100
    )
    
    page: int = Field(
        ...,
        description="Current page number",
        example=1
    )
    
    page_size: int = Field(
        ...,
        description="Number of users per page",
        example=10
    )


# ============================================================================
# USER IN DATABASE SCHEMA
# ============================================================================

class UserInDB(UserResponse):
    """
    User In Database Schema
    
    Internal schema that includes the hashed password.
    This should NEVER be returned in API responses!
    Only used internally for authentication.
    
    Attributes:
        All fields from UserResponse
        hashed_password: Bcrypt hashed password
    """
    
    hashed_password: str = Field(
        ...,
        description="Bcrypt hashed password (internal use only)"
    )
