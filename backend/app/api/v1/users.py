"""
Users API Endpoints
===================

This module provides API endpoints for user management including:
- List users with pagination and search
- Get single user
- Update user
- Delete user
- Activate/deactivate user

All endpoints require admin authentication.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.role import AssignRoleRequest
from app.api.deps import get_current_user, get_current_superuser

# ============================================================================
# ROUTER CONFIGURATION
# ============================================================================

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# ============================================================================
# LIST USERS ENDPOINT
# ============================================================================

@router.get(
    "",
    response_model=List[UserResponse],
    summary="List all users",
    description="Get a list of all users with optional pagination and search"
)
def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search by email, username, or full name"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> List[UserResponse]:
    """
    List all users with pagination and optional search/filters.
    
    Only accessible by admin users.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        search: Optional search term (searches email, username, full_name)
        is_active: Optional filter by active status
        db: Database session (injected)
        current_user: Current authenticated admin user (injected)
        
    Returns:
        List[UserResponse]: List of users
        
    Example:
        GET /api/v1/users?skip=0&limit=10&search=john&is_active=true
    """
    # Start with base query
    query = db.query(User)
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                User.email.ilike(search_term),
                User.username.ilike(search_term),
                User.full_name.ilike(search_term)
            )
        )
    
    # Apply active status filter if provided
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    # Apply pagination
    users = query.offset(skip).limit(limit).all()
    
    return [UserResponse.from_orm(user) for user in users]


# ============================================================================
# GET SINGLE USER ENDPOINT
# ============================================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Get a single user by their ID"
)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> UserResponse:
    """
    Get a single user by ID.
    
    Only accessible by admin users.
    
    Args:
        user_id: ID of the user to retrieve
        db: Database session (injected)
        current_user: Current authenticated admin user (injected)
        
    Returns:
        UserResponse: User object
        
    Raises:
        HTTPException 404: If user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return UserResponse.from_orm(user)


# ============================================================================
# UPDATE USER ENDPOINT
# ============================================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update user information"
)
def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> UserResponse:
    """
    Update a user's information.
    
    Only accessible by admin users.
    
    Args:
        user_id: ID of the user to update
        user_update: User update data
        db: Database session (injected)
        current_user: Current authenticated admin user (injected)
        
    Returns:
        UserResponse: Updated user object
        
    Raises:
        HTTPException 404: If user not found
        HTTPException 400: If email/username already taken
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Check if email is being changed and if it's already taken
    if user_update.email and user_update.email != user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if username is being changed and if it's already taken
    if user_update.username and user_update.username != user.username:
        existing_user = db.query(User).filter(User.username == user_update.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return UserResponse.from_orm(user)


# ============================================================================
# DELETE USER ENDPOINT
# ============================================================================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user",
    description="Delete a user by ID"
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> dict:
    """
    Delete a user.
    
    Only accessible by admin users.
    Cannot delete yourself.
    
    Args:
        user_id: ID of the user to delete
        db: Database session (injected)
        current_user: Current authenticated admin user (injected)
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException 404: If user not found
        HTTPException 400: If trying to delete yourself
    """
    # Prevent deleting yourself
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Delete user
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user.email} deleted successfully"}


# ============================================================================
# ACTIVATE/DEACTIVATE USER ENDPOINT
# ============================================================================

@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse,
    summary="Activate/deactivate user",
    description="Toggle user active status"
)
def toggle_user_status(
    user_id: str,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> UserResponse:
    """
    Activate or deactivate a user.
    
    Only accessible by admin users.
    Cannot deactivate yourself.
    
    Args:
        user_id: ID of the user to update
        is_active: New active status
        db: Database session (injected)
        current_user: Current authenticated admin user (injected)
        
    Returns:
        UserResponse: Updated user object
        
    Raises:
        HTTPException 404: If user not found
        HTTPException 400: If trying to deactivate yourself
    """
    # Prevent deactivating yourself
    if user_id == current_user.id and not is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Update status
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    
    return UserResponse.from_orm(user)


# ============================================================================
# ASSIGN ROLE TO USER ENDPOINT
# ============================================================================

@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
    summary="Assign role to user",
    description="Assign a role to a user"
)
def assign_user_role(
    user_id: str,
    request: AssignRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> UserResponse:
    """
    Assign a role to a user.
    
    Only accessible by admin users.
    
    Args:
        user_id: ID of the user
        request: Role assignment request with role_id
        db: Database session (injected)
        current_user: Current authenticated admin user (injected)
        
    Returns:
        UserResponse: Updated user object
        
    Raises:
        HTTPException 404: If user or role not found
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Get role
    role = db.query(Role).filter(Role.id == request.role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {request.role_id} not found"
        )
    
    # Assign role
    user.role_id = request.role_id
    db.commit()
    db.refresh(user)
    
    return UserResponse.from_orm(user)
