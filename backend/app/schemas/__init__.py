"""
Schemas Package Initialization
===============================

This file makes the schemas directory a Python package and provides
convenient imports for all Pydantic schemas.
"""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
    UserInDB
)

from app.schemas.token import (
    Token,
    TokenWithRefresh,
    TokenPayload,
    LoginRequest,
    PasswordResetRequest,
    PasswordResetConfirm
)

# Export all schemas for easy importing
__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserListResponse",
    "UserInDB",
    # Token schemas
    "Token",
    "TokenWithRefresh",
    "TokenPayload",
    "LoginRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
]
