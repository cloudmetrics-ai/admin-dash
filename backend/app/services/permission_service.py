"""
Permission Service
==================

Service for managing and checking user permissions in the RBAC system.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role, Permission


class PermissionService:
    """Service for permission management and validation"""
    
    @staticmethod
    def get_user_permissions(user: User, db: Session) -> List[str]:
        """
        Get all permission names for a user
        
        Args:
            user: User object
            db: Database session
            
        Returns:
            List of permission names (e.g., ['users.create', 'users.read'])
        """
        if not user.role:
            return []
        
        # Refresh role to ensure permissions are loaded
        db.refresh(user.role)
        
        return [perm.name for perm in user.role.permissions]
    
    @staticmethod
    def user_has_permission(user: User, permission: str, db: Session) -> bool:
        """
        Check if user has a specific permission
        
        Supports:
        - Exact match: 'users.create'
        - Wildcard: 'system.*' grants all permissions
        - Category wildcard: 'users.*' grants all user permissions
        
        Args:
            user: User object
            permission: Permission to check (e.g., 'users.create')
            db: Database session
            
        Returns:
            True if user has permission, False otherwise
        """
        permissions = PermissionService.get_user_permissions(user, db)
        
        # Check for system-wide wildcard
        if "system.*" in permissions:
            return True
        
        # Check for exact permission
        if permission in permissions:
            return True
        
        # Check for category wildcard (e.g., "users.*")
        if '.' in permission:
            category = permission.split('.')[0]
            if f"{category}.*" in permissions:
                return True
        
        return False
    
    @staticmethod
    def get_role_by_name(name: str, db: Session) -> Optional[Role]:
        """Get role by name"""
        return db.query(Role).filter(Role.name == name).first()
    
    @staticmethod
    def get_all_roles(db: Session) -> List[Role]:
        """Get all roles"""
        return db.query(Role).all()
    
    @staticmethod
    def get_all_permissions(db: Session) -> List[Permission]:
        """Get all available permissions"""
        return db.query(Permission).order_by(Permission.category, Permission.action).all()
    
    @staticmethod
    def create_role(
        name: str,
        display_name: str,
        description: str,
        db: Session
    ) -> Role:
        """
        Create a new role
        
        Args:
            name: Role name (e.g., 'custom_role')
            display_name: Human-readable name
            description: Role description
            db: Database session
            
        Returns:
            Created Role object
        """
        role = Role(
            name=name,
            display_name=display_name,
            description=description,
            is_system_role=False
        )
        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    
    @staticmethod
    def assign_permissions_to_role(
        role_id: int,
        permission_ids: List[int],
        db: Session
    ):
        """
        Assign permissions to a role
        
        Args:
            role_id: ID of the role
            permission_ids: List of permission IDs to assign
            db: Database session
        """
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise ValueError(f"Role with ID {role_id} not found")
        
        permissions = db.query(Permission).filter(
            Permission.id.in_(permission_ids)
        ).all()
        
        role.permissions = permissions
        db.commit()
    
    @staticmethod
    def assign_role_to_user(user_id: str, role_id: int, db: Session):
        """
        Assign a role to a user
        
        Args:
            user_id: User ID
            role_id: Role ID
            db: Database session
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise ValueError(f"Role with ID {role_id} not found")
        
        user.role_id = role_id
        db.commit()
