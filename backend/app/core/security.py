"""
Security and Authentication Utilities
======================================

This module provides security-related functionality including:
- Password hashing and verification
- JWT token creation and validation
- User authentication helpers

These utilities are used throughout the application for user authentication
and authorization.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt

from app.core.config import settings


# ============================================================================
# PASSWORD HASHING
# ============================================================================

# Use bcrypt directly instead of passlib due to Python 3.13 compatibility issues
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Hashed password
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash using bcrypt
    
    Args:
        plain_password: Plain text password from user input
        hashed_password: Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    # Convert to bytes
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Verify using bcrypt
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# ============================================================================
# JWT TOKEN MANAGEMENT
# ============================================================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token
    
    Generates a JSON Web Token (JWT) that can be used for authentication.
    The token contains user data and an expiration time.
    
    Args:
        data: Dictionary of data to encode in the token (usually user_id, email)
        expires_delta: Optional custom expiration time. If not provided,
                      uses ACCESS_TOKEN_EXPIRE_MINUTES from settings
                      
    Returns:
        str: Encoded JWT token
        
    Example:
        ```python
        # Create a token for a user
        token_data = {"sub": user.email, "user_id": user.id}
        token = create_access_token(token_data)
        
        # Create a token with custom expiration (1 hour)
        token = create_access_token(
            token_data,
            expires_delta=timedelta(hours=1)
        )
        ```
        
    Token Structure:
        The token contains:
        - sub: Subject (usually user email or ID)
        - exp: Expiration timestamp
        - iat: Issued at timestamp
        - Any additional data passed in the 'data' parameter
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()
    
    # Calculate expiration time
    if expires_delta:
        # Use custom expiration time if provided
        expire = datetime.utcnow() + expires_delta
    else:
        # Use default expiration time from settings
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Add expiration time to the token data
    to_encode.update({
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow()  # Issued at time
    })
    
    # Encode the token using the secret key and algorithm
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT refresh token
    
    Refresh tokens have a longer expiration time than access tokens.
    They are used to obtain new access tokens without requiring the user
    to log in again.
    
    Args:
        data: Dictionary of data to encode in the token
        
    Returns:
        str: Encoded JWT refresh token
        
    Example:
        ```python
        refresh_token = create_refresh_token({"sub": user.email})
        ```
    """
    # Create refresh token with longer expiration time
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_access_token(data, expires_delta)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT token
    
    Decodes a JWT token and validates its signature and expiration.
    Returns the token payload if valid, None if invalid.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Optional[Dict]: Token payload if valid, None if invalid
        
    Example:
        ```python
        payload = decode_token(token)
        if payload:
            user_email = payload.get("sub")
            user_id = payload.get("user_id")
        else:
            print("Invalid token!")
        ```
        
    Common Errors:
        - JWTError: Token is invalid or expired
        - ExpiredSignatureError: Token has expired
        - JWTClaimsError: Token claims are invalid
    """
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
        
    except JWTError as e:
        # Token is invalid (expired, wrong signature, etc.)
        print(f"Token decode error: {e}")
        return None


def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Get the expiration time of a JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Optional[datetime]: Expiration time if token is valid, None otherwise
        
    Example:
        ```python
        exp_time = get_token_expiration(token)
        if exp_time:
            print(f"Token expires at: {exp_time}")
        ```
    """
    payload = decode_token(token)
    if payload and "exp" in payload:
        # Convert Unix timestamp to datetime
        return datetime.fromtimestamp(payload["exp"])
    return None


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired
    
    Args:
        token: JWT token string
        
    Returns:
        bool: True if token is expired, False otherwise
        
    Example:
        ```python
        if is_token_expired(token):
            print("Token has expired, please login again")
        ```
    """
    exp_time = get_token_expiration(token)
    if exp_time:
        return datetime.utcnow() > exp_time
    return True  # If we can't get expiration, consider it expired


# ============================================================================
# TOKEN EXTRACTION HELPERS
# ============================================================================

def extract_token_from_header(authorization: str) -> Optional[str]:
    """
    Extract JWT token from Authorization header
    
    The Authorization header should be in the format:
    "Bearer <token>"
    
    Args:
        authorization: Authorization header value
        
    Returns:
        Optional[str]: Token if found, None otherwise
        
    Example:
        ```python
        auth_header = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        token = extract_token_from_header(auth_header)
        # Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        ```
    """
    if not authorization:
        return None
    
    # Split the header into scheme and token
    parts = authorization.split()
    
    # Check if the header is in the correct format
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    
    return parts[1]


# ============================================================================
# PASSWORD VALIDATION
# ============================================================================

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    
    Checks if a password meets minimum security requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    
    Args:
        password: Password to validate
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
        
    Example:
        ```python
        is_valid, message = validate_password_strength("weak")
        if not is_valid:
            print(f"Password error: {message}")
        ```
    """
    # Check minimum length
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Check for uppercase letter
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for lowercase letter
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for digit
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"


# ============================================================================
# SECURITY UTILITIES
# ============================================================================

def generate_password_reset_token(email: str) -> str:
    """
    Generate a password reset token
    
    Creates a short-lived token for password reset functionality.
    
    Args:
        email: User's email address
        
    Returns:
        str: Password reset token
        
    Example:
        ```python
        reset_token = generate_password_reset_token(user.email)
        # Send this token to user's email
        ```
    """
    # Create a token that expires in 30 minutes
    delta = timedelta(minutes=30)
    return create_access_token(
        data={"sub": email, "type": "password_reset"},
        expires_delta=delta
    )


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify a password reset token
    
    Args:
        token: Password reset token
        
    Returns:
        Optional[str]: User email if token is valid, None otherwise
        
    Example:
        ```python
        email = verify_password_reset_token(token)
        if email:
            # Allow user to reset password
            pass
        ```
    """
    payload = decode_token(token)
    if payload and payload.get("type") == "password_reset":
        return payload.get("sub")
    return None
