"""
Role and Permission Models
===========================

Database models for role-based access control (RBAC).
"""

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


# ============================================================================
# ASSOCIATION TABLES
# ============================================================================

# Many-to-many relationship between roles and permissions
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False),
    Column('granted_at', DateTime, default=datetime.utcnow),
    Column('granted_by', String, ForeignKey('users.id'), nullable=True)  # String to match User.id (UUID)
)


# ============================================================================
# ROLE MODEL
# ============================================================================

class Role(Base):
    """
    Role Model
    
    Represents a user role with associated permissions.
    
    Attributes:
        id: Primary key
        name: Unique role name (e.g., 'admin', 'manager')
        display_name: Human-readable name
        description: Role description
        is_system_role: If True, role cannot be deleted
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_system_role = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )
    users = relationship("User", back_populates="role")
    
    def __repr__(self):
        return f"<Role {self.name}>"


# ============================================================================
# PERMISSION MODEL
# ============================================================================

class Permission(Base):
    """
    Permission Model
    
    Represents a specific permission that can be granted to roles.
    
    Attributes:
        id: Primary key
        name: Unique permission name (e.g., 'users.create')
        category: Permission category (e.g., 'users', 'products')
        action: Action type (e.g., 'create', 'read', 'update', 'delete')
        description: Permission description
        created_at: Creation timestamp
    """
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    action = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )
    
    def __repr__(self):
        return f"<Permission {self.name}>"
