"""
Roles API Endpoints
===================

API endpoints for role and permission management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.user import User
from app.models.role import Role, Permission
from app.schemas.role import (
    RoleResponse,
    RoleListResponse,
    RoleCreate,
    RoleUpdate,
    PermissionResponse,
    PermissionsByCategory,
    AssignPermissionsRequest
)
from app.api.deps import get_current_superuser
from app.services.permission_service import PermissionService


# ============================================================================
# ROUTER CONFIGURATION
# ============================================================================

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)


# ============================================================================
# ROLES ENDPOINTS
# ============================================================================

@router.get(
    "",
    response_model=List[RoleListResponse],
    summary="List all roles",
    description="Get a list of all roles with permission and user counts"
)
def list_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> List[RoleListResponse]:
    """
    List all roles with counts.
    
    Requires: Super Admin access
    """
    roles = db.query(Role).all()
    
    result = []
    for role in roles:
        # Count users with this role
        user_count = db.query(User).filter(User.role_id == role.id).count()
        
        result.append(RoleListResponse(
            id=role.id,
            name=role.name,
            display_name=role.display_name,
            description=role.description,
            is_system_role=role.is_system_role,
            permission_count=len(role.permissions),
            user_count=user_count
        ))
    
    return result


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Get role by ID",
    description="Get detailed information about a specific role"
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> RoleResponse:
    """
    Get a single role with full details.
    
    Requires: Super Admin access
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Count users
    user_count = db.query(User).filter(User.role_id == role.id).count()
    
    # Build response
    response = RoleResponse.from_orm(role)
    response.user_count = user_count
    
    return response


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new role",
    description="Create a new custom role"
)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> RoleResponse:
    """
    Create a new custom role.
    
    Requires: Super Admin access
    """
    # Check if role name already exists
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with name '{role_data.name}' already exists"
        )
    
    # Create role
    role = Role(
        name=role_data.name,
        display_name=role_data.display_name,
        description=role_data.description,
        is_system_role=False  # Custom roles are never system roles
    )
    
    db.add(role)
    db.commit()
    db.refresh(role)
    
    response = RoleResponse.from_orm(role)
    response.user_count = 0
    
    return response


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Update role",
    description="Update role details (cannot update system roles)"
)
def update_role(
    role_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> RoleResponse:
    """
    Update a role's details.
    
    Cannot update system roles.
    Requires: Super Admin access
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Prevent updating system roles
    if role.is_system_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update system roles"
        )
    
    # Update fields
    update_data = role_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(role, field, value)
    
    db.commit()
    db.refresh(role)
    
    user_count = db.query(User).filter(User.role_id == role.id).count()
    response = RoleResponse.from_orm(role)
    response.user_count = user_count
    
    return response


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete role",
    description="Delete a custom role (cannot delete system roles or roles with users)"
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> dict:
    """
    Delete a custom role.
    
    Cannot delete:
    - System roles
    - Roles that have users assigned
    
    Requires: Super Admin access
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Prevent deleting system roles
    if role.is_system_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete system roles"
        )
    
    # Check if any users have this role
    user_count = db.query(User).filter(User.role_id == role.id).count()
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete role with {user_count} assigned user(s). Reassign users first."
        )
    
    db.delete(role)
    db.commit()
    
    return {"message": f"Role '{role.display_name}' deleted successfully"}


@router.post(
    "/{role_id}/permissions",
    response_model=RoleResponse,
    summary="Assign permissions to role",
    description="Assign a list of permissions to a role"
)
def assign_permissions(
    role_id: int,
    request: AssignPermissionsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> RoleResponse:
    """
    Assign permissions to a role.
    
    Replaces all existing permissions with the new list.
    Requires: Super Admin access
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Get permissions
    permissions = db.query(Permission).filter(
        Permission.id.in_(request.permission_ids)
    ).all()
    
    if len(permissions) != len(request.permission_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more permission IDs are invalid"
        )
    
    # Assign permissions (replaces existing)
    role.permissions = permissions
    db.commit()
    db.refresh(role)
    
    user_count = db.query(User).filter(User.role_id == role.id).count()
    response = RoleResponse.from_orm(role)
    response.user_count = user_count
    
    return response


# ============================================================================
# PERMISSIONS ENDPOINTS
# ============================================================================

@router.get(
    "/permissions/all",
    response_model=List[PermissionsByCategory],
    summary="List all permissions",
    description="Get all permissions grouped by category"
)
def list_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> List[PermissionsByCategory]:
    """
    List all permissions grouped by category.
    
    Requires: Super Admin access
    """
    permissions = db.query(Permission).order_by(Permission.category, Permission.action).all()
    
    # Group by category
    categories = {}
    for perm in permissions:
        if perm.category not in categories:
            categories[perm.category] = []
        categories[perm.category].append(PermissionResponse.from_orm(perm))
    
    # Convert to list of PermissionsByCategory
    result = [
        PermissionsByCategory(category=cat, permissions=perms)
        for cat, perms in categories.items()
    ]
    
    return result
