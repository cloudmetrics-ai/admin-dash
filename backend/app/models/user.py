"""
User Database Model
===================

This module defines the User model for the database using SQLAlchemy ORM.
The User model represents users in the system and includes fields for
authentication, profile information, and timestamps.

The model is used for:
- User registration and authentication
- Storing user profile information
- Managing user permissions (is_active, is_superuser)
- Tracking user creation and updates
"""

from typing import Optional
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class User(Base):
    """
    User Model
    
    Represents a user in the system. Each user has authentication credentials,
    profile information, and permission flags.
    
    Attributes:
        id: Unique identifier for the user (UUID)
        email: User's email address (unique, used for login)
        username: User's username (unique, optional)
        hashed_password: Bcrypt hashed password
        full_name: User's full name (optional)
        is_active: Whether the user account is active
        is_superuser: Whether the user has admin privileges
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
        
    Relationships:
        chat_sessions: One-to-many relationship with ChatSession model
        
    Example Usage:
        ```python
        # Create a new user
        user = User(
            email="john@example.com",
            username="johndoe",
            hashed_password=hash_password("password123"),
            full_name="John Doe"
        )
        db.add(user)
        db.commit()
        
        # Query users
        user = db.query(User).filter(User.email == "john@example.com").first()
        ```
    """
    
    # ========================================================================
    # TABLE CONFIGURATION
    # ========================================================================
    
    __tablename__ = "users"
    
    # ========================================================================
    # PRIMARY KEY
    # ========================================================================
    
    # Use UUID as primary key for better security and scalability
    # UUIDs are globally unique and don't reveal information about the number of users
    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        comment="Unique identifier for the user (UUID)"
    )
    
    # ========================================================================
    # AUTHENTICATION FIELDS
    # ========================================================================
    
    # Email address - used as the primary login identifier
    # Must be unique across all users
    # Indexed for fast lookups during login
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="User's email address (unique, used for login)"
    )
    
    # Username - optional alternative identifier
    # Can be used for display purposes or as an alternative login method
    username = Column(
        String(100),
        unique=True,
        index=True,
        nullable=True,
        comment="User's username (unique, optional)"
    )
    
    # Hashed password - NEVER store plain text passwords!
    # This field stores the bcrypt hash of the user's password
    # The hash includes a salt for additional security
    hashed_password = Column(
        String(255),
        nullable=False,
        comment="Bcrypt hashed password (never store plain text!)"
    )
    
    # ========================================================================
    # PROFILE FIELDS
    # ========================================================================
    
    # Full name - optional field for user's display name
    full_name = Column(
        String(255),
        nullable=True,
        comment="User's full name (optional)"
    )
    
    # ========================================================================
    # PERMISSION FLAGS
    # ========================================================================
    
    # Is Active - controls whether the user can log in
    # Set to False to disable a user account without deleting it
    # Useful for temporarily suspending accounts
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether the user account is active (can log in)"
    )
    
    # Is Superuser - grants admin privileges
    # Superusers have access to all features and can manage other users
    # Be careful when granting this permission!
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether the user has admin privileges"
    )
    
    # ========================================================================
    # ROLE RELATIONSHIP (RBAC)
    # ========================================================================
    
    # Role ID - foreign key to roles table
    # Defines the user's role for permission-based access control
    role_id = Column(
        Integer,
        ForeignKey('roles.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        comment="User's role ID for RBAC"
    )
    
    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    
    # Created at - automatically set when the user is created
    # Useful for analytics and user management
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Timestamp when the user was created"
    )
    
    # Updated at - automatically updated when the user is modified
    # Useful for tracking when user information was last changed
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Timestamp when the user was last updated"
    )
    
    # ========================================================================
    # MULTI-FACTOR AUTHENTICATION (MFA)
    # ========================================================================
    
    # MFA Enabled - whether the user has MFA enabled
    # When enabled, user must provide TOTP code during login
    mfa_enabled = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether MFA is enabled for this user"
    )
    
    # MFA Secret - encrypted TOTP secret for generating codes
    # This is the shared secret between server and authenticator app
    # Stored encrypted for security
    mfa_secret = Column(
        String(255),
        nullable=True,
        comment="Encrypted TOTP secret for MFA"
    )
    
    # MFA Backup Codes - hashed backup codes for account recovery
    # JSON array of hashed codes, single-use only
    mfa_backup_codes = Column(
        String(1000),
        nullable=True,
        comment="JSON array of hashed backup codes"
    )
    
    # ========================================================================
    # EMAIL VERIFICATION
    # ========================================================================
    
    # Email Verified - whether the user has verified their email
    # Users cannot login until email is verified
    email_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether the user's email has been verified"
    )
    
    # Verification Token - token sent via email for verification
    # Expires after 24 hours
    verification_token = Column(
        String(255),
        nullable=True,
        comment="Token for email verification"
    )
    
    # Verification Token Expiry - when the verification token expires
    verification_token_expires = Column(
        DateTime,
        nullable=True,
        comment="Expiration time for verification token"
    )
    
    # ========================================================================
    # PASSWORD RESET
    # ========================================================================
    
    # Reset Token - token sent via email for password reset
    # Expires after 1 hour, single-use only
    reset_token = Column(
        String(255),
        nullable=True,
        comment="Token for password reset"
    )
    
    # Reset Token Expiry - when the reset token expires
    reset_token_expires = Column(
        DateTime,
        nullable=True,
        comment="Expiration time for reset token"
    )
    
    # ========================================================================
    # RELATIONSHIPS
    # ========================================================================
    
    # Many-to-one relationship with Role
    # A user belongs to one role
    role = relationship("Role", back_populates="users", lazy="joined")
    
    @property
    def role_display_name(self) -> Optional[str]:
        """Returns the display name of the assigned role"""
        if self.role:
            return self.role.display_name
        return "User" if not self.is_superuser else "Admin"
    
    # One-to-many relationship with chat sessions
    # A user can have multiple chat sessions
    # cascade="all, delete-orphan" means:
    #   - When a user is deleted, all their chat sessions are also deleted
    #   - When a chat session is removed from the user, it's deleted from the database
    # chat_sessions = relationship(
    #     "ChatSession",
    #     back_populates="user",
    #     cascade="all, delete-orphan"
    # )
    
    # ========================================================================
    # STRING REPRESENTATION
    # ========================================================================
    
    def __repr__(self) -> str:
        """
        String representation of the User model
        
        Returns a readable string representation of the user,
        useful for debugging and logging.
        
        Returns:
            str: String representation of the user
        """
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def to_dict(self) -> dict:
        """
        Convert user model to dictionary
        
        Useful for serialization and API responses.
        Note: This excludes the hashed_password for security.
        
        Returns:
            dict: Dictionary representation of the user
            
        Example:
            ```python
            user_dict = user.to_dict()
            # Returns: {
            #     "id": "123e4567-e89b-12d3-a456-426614174000",
            #     "email": "john@example.com",
            #     "username": "johndoe",
            #     "full_name": "John Doe",
            #     "is_active": True,
            #     "is_superuser": False,
            #     "created_at": "2024-01-01T00:00:00",
            #     "updated_at": "2024-01-01T00:00:00"
            # }
            ```
        """
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
