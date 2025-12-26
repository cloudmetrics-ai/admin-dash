"""
Authentication API Endpoints
=============================

This module provides API endpoints for user authentication including:
- User registration
- User login
- Token refresh
- Password reset

All endpoints are thoroughly documented with examples and error handling.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, TokenWithRefresh, LoginRequest
from app.schemas.email_verification import ForgotPasswordRequest, ResetPasswordRequest
from app.api.deps import get_current_user
from app.services.permission_service import PermissionService
from app.services.email_service import EmailService


# ============================================================================
# ROUTER CONFIGURATION
# ============================================================================

# Create an API router for authentication endpoints
# All routes in this router will be prefixed with /auth
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


# ============================================================================
# USER REGISTRATION ENDPOINT
# ============================================================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password"
)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> dict:
    """
    Register a new user
    
    This endpoint creates a new user account. It:
    1. Validates the input data (email format, password strength)
    2. Checks if the email is already registered
    3. Hashes the password
    4. Creates the user in the database (email_verified=False)
    5. Sends verification email
    6. Returns success message
    
    Args:
        user_data: User registration data (email, password, etc.)
        db: Database session (injected)
        
    Returns:
        dict: Success message with instructions
        
    Raises:
        HTTPException 400: If email is already registered
        HTTPException 422: If validation fails
        
    Example Request:
        ```json
        POST /api/v1/auth/register
        {
            "email": "john@example.com",
            "username": "johndoe",
            "full_name": "John Doe",
            "password": "SecurePass123"
        }
        ```
        
    Example Response:
        ```json
        {
            "message": "Registration successful. Please check your email to verify your account."
        }
        ```
    """
    
    # Check if user with this email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username is taken (if provided)
    if user_data.username:
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Hash the password before storing
    hashed_password = hash_password(user_data.password)
    
    # Generate verification token
    verification_token = EmailService.generate_token()
    verification_expires = EmailService.generate_verification_token_expiry()
    
    # Create new user object
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False,
        email_verified=False,  # Require email verification
        verification_token=verification_token,
        verification_token_expires=verification_expires
    )
    
    # Add user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Send verification email
    await EmailService.send_verification_email(new_user.email, verification_token)
    
    # Return success message (do NOT auto-login)
    return {
        "message": "Registration successful. Please check your email to verify your account.",
        "email": new_user.email
    }


# ============================================================================
# USER LOGIN ENDPOINT
# ============================================================================

@router.post(
    "/login",
    response_model=None,  # We'll return Union type
    summary="Login user",
    description="Authenticate user and return access tokens or MFA challenge"
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user and return JWT tokens
    
    This endpoint authenticates a user and returns JWT tokens. It:
    1. Validates the email and password
    2. Checks if the user exists
    3. Verifies the password
    4. Checks if the user is active
    5. Generates access and refresh tokens
    6. Returns the tokens
    
    Args:
        login_data: Login credentials (email and password)
        db: Database session (injected)
        
    Returns:
        TokenWithRefresh: Access token and refresh token
        
    Raises:
        HTTPException 401: If credentials are invalid
        HTTPException 403: If user account is inactive
        
    Example Request:
        ```json
        POST /api/v1/auth/login
        {
            "email": "john@example.com",
            "password": "SecurePass123"
        }
        ```
        
    Example Response:
        ```json
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
        ```
        
    Usage:
        After receiving the tokens, include the access_token in the
        Authorization header for subsequent requests:
        
        ```
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        ```
    """
    
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Check if email is verified
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in. Check your inbox for the verification link."
        )
    
    # Check if MFA is enabled
    if user.mfa_enabled:
        # Return temp token for MFA verification
        temp_token_data = {
            "sub": user.email,
            "user_id": user.id,
            "mfa_pending": True
        }
        temp_token = create_access_token(temp_token_data, expires_delta=timedelta(minutes=5))
        
        # Import MFALoginResponse
        from app.schemas.mfa import MFALoginResponse
        
        # Return MFA required response
        return MFALoginResponse(
            mfa_required=True,
            temp_token=temp_token,
            message="MFA verification required"
        )
    
    # Get user's role and permissions using direct queries
    # This avoids SQLAlchemy relationship loading issues
    role_name = "user"  # Default role
    permissions = []
    
    if user.role_id:
        # Query role directly
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if role:
            role_name = role.name
            # Get permissions using PermissionService
            permissions = PermissionService.get_user_permissions(user, db)
    
    # Create token data with role and permissions
    token_data = {
        "sub": user.email,  # Subject (user identifier)
        "user_id": user.id,  # Additional user information
        "role": role_name,  # User's role
        "permissions": permissions,  # User's permissions
    }
    
    # Generate access token (short-lived, e.g., 30 minutes)
    access_token = create_access_token(token_data)
    
    # Generate refresh token (long-lived, e.g., 7 days)
    refresh_token = create_refresh_token(token_data)
    
    # Return both tokens
    return TokenWithRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


# ============================================================================
# TOKEN REFRESH ENDPOINT
# ============================================================================

@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
    description="Get a new access token using a refresh token"
)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> Token:
    """
    Refresh access token
    
    This endpoint allows users to get a new access token using their
    refresh token, without requiring them to log in again.
    
    Args:
        refresh_token: The refresh token received during login
        db: Database session (injected)
        
    Returns:
        Token: New access token
        
    Raises:
        HTTPException 401: If refresh token is invalid or expired
        
    Example Request:
        ```json
        POST /api/v1/auth/refresh
        {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
        ```
        
    Example Response:
        ```json
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
        ```
    """
    
    # Decode the refresh token
    payload = decode_token(refresh_token)
    
    # Check if token is valid
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user email from token
    user_email = payload.get("sub")
    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Find user in database
    user = db.query(User).filter(User.email == user_email).first()
    
    # Check if user exists and is active
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new access token
    token_data = {
        "sub": user.email,
        "user_id": user.id,
    }
    access_token = create_access_token(token_data)
    
    return Token(
        access_token=access_token,
        token_type="bearer"
    )


# ============================================================================
# GET CURRENT USER ENDPOINT
# ============================================================================

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the currently authenticated user's information"
)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Get current user information
    
    This endpoint returns the profile information of the currently
    authenticated user, including their role and permissions.
    
    Args:
        current_user: Current authenticated user (injected from token)
        db: Database session (injected)
        
    Returns:
        UserResponse: Current user's information with role and permissions
        
    Example Request:
        ```
        GET /api/v1/auth/me
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        ```
        
    Example Response:
        ```json
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "john@example.com",
            "username": "johndoe",
            "full_name": "John Doe",
            "is_active": true,
            "is_superuser": false,
            "role_id": 2,
            "role_name": "admin",
            "role_display_name": "Administrator",
            "permissions": ["users.read", "users.create", "products.read"],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        ```
    """
    
    # Create base response from ORM model
    user_response = UserResponse.from_orm(current_user)
    
    # Add role name if user has a role
    if current_user.role:
        user_response.role_name = current_user.role.name
    
    # Get user permissions
    permissions = PermissionService.get_user_permissions(current_user, db)
    user_response.permissions = permissions
    
    return user_response


# ============================================================================
# LOGOUT ENDPOINT (Optional - for token blacklisting)
# ============================================================================

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Logout the current user (client should discard tokens)"
)
def logout(
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Logout user
    
    Since JWTs are stateless, logout is typically handled on the client side
    by discarding the tokens. This endpoint is provided for consistency and
    can be extended to implement token blacklisting if needed.
    
    Args:
        current_user: Current authenticated user (injected)
        
    Returns:
        dict: Success message
        
    Example Request:
        ```
        POST /api/v1/auth/logout
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        ```
        
    Example Response:
        ```json
        {
            "message": "Successfully logged out"
        }
        ```
        
    Note:
        To implement proper logout with JWT:
        1. Client should delete the stored tokens
        2. Optionally, implement token blacklisting using Redis
        3. Set short expiration times for access tokens
    """
    
    # TODO: Implement token blacklisting if needed
    # Example: Add token to Redis blacklist with expiration
    return {"message": "Successfully logged out"}


# ============================================================================
# EMAIL VERIFICATION ENDPOINTS
# ============================================================================

@router.get(
    "/verify-email",
    status_code=status.HTTP_200_OK,
    summary="Verify email address",
    description="Verify user email using token from email"
)
def verify_email(
    token: str,
    db: Session = Depends(get_db)
) -> dict:
    """
    Verify user email address.
    
    Validates the verification token and marks email as verified.
    """
    # Find user by verification token
    user = db.query(User).filter(User.verification_token == token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Check if already verified
    if user.email_verified:
        return {"message": "Email already verified"}
    
    # Check if token is expired
    if not EmailService.is_token_valid(user.verification_token_expires):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired. Please request a new one"
        )
    
    # Mark email as verified
    user.email_verified = True
    user.verification_token = None
    user.verification_token_expires = None
    
    db.commit()
    
    return {"message": "Email verified successfully. You can now login"}


@router.post(
    "/resend-verification",
    status_code=status.HTTP_200_OK,
    summary="Resend verification email",
    description="Resend verification email to user"
)
async def resend_verification(
    request_data: "ResendVerificationRequest",
    db: Session = Depends(get_db)
) -> dict:
    """
    Resend verification email.
    
    Generates a new verification token and sends email.
    """
    from app.schemas.email_verification import ResendVerificationRequest as ResendSchema
    
    # Find user by email
    user = db.query(User).filter(User.email == request_data.email).first()
    
    if not user:
        # Don't reveal if email exists
        return {"message": "If that email exists, a verification link has been sent"}
    
    # Check if already verified
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Generate new verification token
    verification_token = EmailService.generate_token()
    user.verification_token = verification_token
    user.verification_token_expires = EmailService.generate_verification_token_expiry()
    
    db.commit()
    
    # Send verification email
    await EmailService.send_verification_email(user.email, verification_token)
    
    return {"message": "If that email exists, a verification link has been sent"}


# ============================================================================
# PASSWORD RESET ENDPOINTS
# ============================================================================

@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    summary="Request password reset",
    description="Send password reset email to user"
)
async def forgot_password(
    request_data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
) -> dict:
    """
    Request password reset email.
    
    Sends an email with a reset token to the user's email address.
    Token expires in 1 hour.
    """
    # Find user by email
    user = db.query(User).filter(User.email == request_data.email).first()
    
    # Always return success to prevent email enumeration
    if not user:
        return {"message": "If that email exists, a reset link has been sent"}
    
    # Check if email is verified
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify your email first"
        )
    
    # Generate reset token
    reset_token = EmailService.generate_token()
    user.reset_token = reset_token
    user.reset_token_expires = EmailService.generate_reset_token_expiry()
    
    db.commit()
    
    # Send reset email
    await EmailService.send_password_reset_email(user.email, reset_token)
    
    return {"message": "If that email exists, a reset link has been sent"}


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    summary="Reset password",
    description="Reset password using token from email"
)
def reset_password(
    request_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
) -> dict:
    """
    Reset password using token.
    
    Validates the token and sets a new password.
    """
    # Find user by reset token
    user = db.query(User).filter(User.reset_token == request_data.token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Check if token is expired
    if not EmailService.is_token_valid(user.reset_token_expires):
        # Clear expired token
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired. Please request a new one"
        )
    
    # Update password
    user.hashed_password = hash_password(request_data.new_password)
    
    # Clear reset token (one-time use)
    user.reset_token = None
    user.reset_token_expires = None
    
    db.commit()
    
    return {"message": "Password reset successful"}
