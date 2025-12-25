"""
Role and Permission Schemas
============================

Pydantic schemas for role and permission API requests/responses.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# ============================================================================
# PERMISSION SCHEMAS
# ============================================================================

class PermissionResponse(BaseModel):
    """Permission response schema"""
    id: int
    name: str
    category: str
    action: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class PermissionsByCategory(BaseModel):
    """Permissions grouped by category"""
    category: str
    permissions: List[PermissionResponse]


# ============================================================================
# ROLE SCHEMAS
# ============================================================================

class RoleBase(BaseModel):
    """Base role schema with common fields"""
    display_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class RoleCreate(RoleBase):
    """Schema for creating a new role"""
    name: str = Field(..., min_length=1, max_length=50, pattern="^[a-z0-9_]+$")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "content_editor",
                "display_name": "Content Editor",
                "description": "Can create and edit content but not publish"
            }
        }


class RoleUpdate(BaseModel):
    """Schema for updating a role"""
    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "display_name": "Senior Content Editor",
                "description": "Can create, edit, and publish content"
            }
        }


class RoleResponse(BaseModel):
    """Role response schema"""
    id: int
    name: str
    display_name: str
    description: Optional[str] = None
    is_system_role: bool
    created_at: datetime
    updated_at: datetime
    permissions: List[PermissionResponse] = []
    user_count: Optional[int] = 0  # Number of users with this role
    
    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """Simplified role response for list views"""
    id: int
    name: str
    display_name: str
    description: Optional[str] = None
    is_system_role: bool
    permission_count: int
    user_count: int
    
    class Config:
        from_attributes = True


class AssignPermissionsRequest(BaseModel):
    """Schema for assigning permissions to a role"""
    permission_ids: List[int] = Field(..., min_items=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "permission_ids": [1, 2, 3, 10, 11]
            }
        }


class AssignRoleRequest(BaseModel):
    """Schema for assigning a role to a user"""
    role_id: int = Field(..., gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "role_id": 3
            }
        }
