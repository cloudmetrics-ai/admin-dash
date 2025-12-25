"""
MFA Schemas
===========

Pydantic schemas for Multi-Factor Authentication endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class MFASetupResponse(BaseModel):
    """Response for MFA setup initiation"""
    secret: str = Field(..., description="Base32 encoded secret for manual entry")
    qr_code: str = Field(..., description="Data URL for QR code image")
    backup_codes: List[str] = Field(..., description="List of backup codes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "secret": "JBSWY3DPEHPK3PXP",
                "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANS...",
                "backup_codes": ["12345678", "87654321", "11223344"]
            }
        }


class MFAEnableRequest(BaseModel):
    """Request to enable MFA"""
    code: str = Field(..., min_length=6, max_length=6, description="6-digit TOTP code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "123456"
            }
        }


class MFADisableRequest(BaseModel):
    """Request to disable MFA"""
    password: str = Field(..., description="User's password for confirmation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "password": "user_password"
            }
        }


class MFAVerifyRequest(BaseModel):
    """Request to verify MFA code during login"""
    temp_token: str = Field(..., description="Temporary token from initial login")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit TOTP code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "temp_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "code": "123456"
            }
        }


class MFAStatusResponse(BaseModel):
    """Response for MFA status check"""
    mfa_enabled: bool = Field(..., description="Whether MFA is enabled")
    
    class Config:
        json_schema_extra = {
            "example": {
                "mfa_enabled": True
            }
        }


class MFALoginResponse(BaseModel):
    """Response when MFA is required during login"""
    mfa_required: bool = Field(True, description="Indicates MFA is required")
    temp_token: str = Field(..., description="Temporary token for MFA verification")
    message: str = Field(default="MFA verification required", description="User message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "mfa_required": True,
                "temp_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "message": "MFA verification required"
            }
        }


class BackupCodesResponse(BaseModel):
    """Response for backup codes regeneration"""
    backup_codes: List[str] = Field(..., description="List of new backup codes")
    message: str = Field(default="Backup codes regenerated successfully")
    
    class Config:
        json_schema_extra = {
            "example": {
                "backup_codes": ["12345678", "87654321", "11223344"],
                "message": "Backup codes regenerated successfully"
            }
        }
