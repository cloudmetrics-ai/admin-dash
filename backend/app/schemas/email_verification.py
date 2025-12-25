"""
Email Verification & Password Reset Schemas
============================================

Pydantic schemas for email verification and password reset requests/responses.
"""

from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# EMAIL VERIFICATION SCHEMAS
# ============================================================================

class ResendVerificationRequest(BaseModel):
    """Request to resend verification email"""
    email: EmailStr


class VerifyEmailResponse(BaseModel):
    """Response after email verification"""
    message: str


# ============================================================================
# PASSWORD RESET SCHEMAS
# ============================================================================

class ForgotPasswordRequest(BaseModel):
    """Request to initiate password reset"""
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    """Response after requesting password reset"""
    message: str


class ResetPasswordRequest(BaseModel):
    """Request to reset password with token"""
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")


class ResetPasswordResponse(BaseModel):
    """Response after password reset"""
    message: str
