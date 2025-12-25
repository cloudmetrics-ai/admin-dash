"""
Token Pydantic Schemas
=======================

This module defines Pydantic models for authentication tokens.
These schemas are used for JWT token validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ============================================================================
# TOKEN SCHEMA
# ============================================================================

class Token(BaseModel):
    """
    Token Schema
    
    Represents an access token response after successful login.
    
    Attributes:
        access_token: JWT access token string
        token_type: Type of token (always "bearer" for JWT)
        
    Example:
        ```python
        token = Token(
            access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            token_type="bearer"
        )
        ```
    """
    
    access_token: str = Field(
        ...,
        description="JWT access token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    
    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer' for JWT)",
        example="bearer"
    )


# ============================================================================
# TOKEN WITH REFRESH SCHEMA
# ============================================================================

class TokenWithRefresh(Token):
    """
    Token With Refresh Schema
    
    Extends Token schema to include a refresh token.
    Used when implementing token refresh functionality.
    
    Attributes:
        access_token: JWT access token (from Token)
        token_type: Token type (from Token)
        refresh_token: JWT refresh token for obtaining new access tokens
        
    Example:
        ```python
        tokens = TokenWithRefresh(
            access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            token_type="bearer"
        )
        ```
    """
    
    refresh_token: str = Field(
        ...,
        description="JWT refresh token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )


# ============================================================================
# TOKEN PAYLOAD SCHEMA
# ============================================================================

class TokenPayload(BaseModel):
    """
    Token Payload Schema
    
    Represents the decoded payload of a JWT token.
    Used internally for token validation.
    
    Attributes:
        sub: Subject (usually user email or ID)
        exp: Expiration timestamp
        user_id: User's unique identifier (optional)
        
    Example:
        ```python
        payload = TokenPayload(
            sub="john@example.com",
            exp=1234567890,
            user_id="123e4567-e89b-12d3-a456-426614174000"
        )
        ```
    """
    
    sub: str = Field(
        ...,
        description="Subject (user email or ID)",
        example="john@example.com"
    )
    
    exp: Optional[int] = Field(
        None,
        description="Expiration timestamp",
        example=1234567890
    )
    
    user_id: Optional[str] = Field(
        None,
        description="User's unique identifier",
        example="123e4567-e89b-12d3-a456-426614174000"
    )


# ============================================================================
# LOGIN REQUEST SCHEMA
# ============================================================================

class LoginRequest(BaseModel):
    """
    Login Request Schema
    
    Used for user login requests.
    Validates email and password format.
    
    Attributes:
        email: User's email address
        password: User's password (plain text, will be verified against hash)
        
    Example:
        ```python
        login_data = LoginRequest(
            email="john@example.com",
            password="SecurePassword123"
        )
        ```
    """
    
    email: str = Field(
        ...,
        description="User's email address",
        example="john@example.com"
    )
    
    password: str = Field(
        ...,
        description="User's password",
        example="SecurePassword123"
    )


# ============================================================================
# PASSWORD RESET REQUEST SCHEMA
# ============================================================================

class PasswordResetRequest(BaseModel):
    """
    Password Reset Request Schema
    
    Used when a user requests a password reset.
    
    Attributes:
        email: User's email address
        
    Example:
        ```python
        reset_request = PasswordResetRequest(
            email="john@example.com"
        )
        ```
    """
    
    email: str = Field(
        ...,
        description="User's email address",
        example="john@example.com"
    )


# ============================================================================
# PASSWORD RESET CONFIRM SCHEMA
# ============================================================================

class PasswordResetConfirm(BaseModel):
    """
    Password Reset Confirm Schema
    
    Used when a user confirms a password reset with a token.
    
    Attributes:
        token: Password reset token (from email)
        new_password: New password to set
        
    Example:
        ```python
        reset_confirm = PasswordResetConfirm(
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            new_password="NewSecurePassword123"
        )
        ```
    """
    
    token: str = Field(
        ...,
        description="Password reset token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    
    new_password: str = Field(
        ...,
        min_length=8,
        description="New password (min 8 characters)",
        example="NewSecurePassword123"
    )
