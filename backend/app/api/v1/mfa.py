"""
MFA API Endpoints
=================

API endpoints for Multi-Factor Authentication management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, decode_token
from app.models.user import User
from app.schemas.mfa import (
    MFASetupResponse,
    MFAEnableRequest,
    MFADisableRequest,
    MFAVerifyRequest,
    MFAStatusResponse,
    MFALoginResponse,
    BackupCodesResponse
)
from app.schemas.token import TokenWithRefresh
from app.api.deps import get_current_user
from app.services.mfa_service import MFAService


# ============================================================================
# ROUTER CONFIGURATION
# ============================================================================

router = APIRouter(
    prefix="/auth/mfa",
    tags=["mfa"],
    responses={404: {"description": "Not found"}},
)


# ============================================================================
# MFA SETUP ENDPOINT
# ============================================================================

@router.post(
    "/setup",
    response_model=MFASetupResponse,
    summary="Setup MFA",
    description="Generate MFA secret, QR code, and backup codes"
)
def setup_mfa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> MFASetupResponse:
    """
    Setup MFA for the current user.
    
    Generates:
    - TOTP secret
    - QR code for authenticator app
    - Backup codes for recovery
    
    Note: This does NOT enable MFA yet. User must verify a code first.
    """
    # Check if MFA is already enabled
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled"
        )
    
    # Generate secret, QR code, and backup codes
    secret, qr_code, backup_codes = MFAService.setup_mfa(current_user.email)
    
    # Store secret temporarily in session (we'll save it when user verifies)
    # For now, we'll return it and expect the frontend to send it back
    return MFASetupResponse(
        secret=secret,
        qr_code=qr_code,
        backup_codes=backup_codes
    )


# ============================================================================
# MFA ENABLE ENDPOINT
# ============================================================================

@router.post(
    "/enable",
    status_code=status.HTTP_200_OK,
    summary="Enable MFA",
    description="Verify TOTP code and enable MFA"
)
def enable_mfa(
    secret: str,
    code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Enable MFA after verifying TOTP code.
    
    The user must have called /setup first to get the secret.
    This endpoint verifies the code and enables MFA.
    """
    # Check if MFA is already enabled
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled"
        )
    
    # Verify the TOTP code with the provided secret
    if not MFAService.verify_totp(secret, code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid verification code"
        )
    
    # Generate backup codes
    backup_codes = MFAService.generate_backup_codes()
    
    # Enable MFA
    MFAService.enable_mfa(db, current_user, secret, backup_codes)
    
    return {"message": "MFA enabled successfully"}


# ============================================================================
# MFA DISABLE ENDPOINT
# ============================================================================

@router.post(
    "/disable",
    status_code=status.HTTP_200_OK,
    summary="Disable MFA",
    description="Disable MFA for the current user"
)
def disable_mfa(
    request: MFADisableRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Disable MFA for the current user.
    
    Requires password confirmation for security.
    """
    # Check if MFA is enabled
    if not current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled"
        )
    
    # Verify password
    if not verify_password(request.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # Disable MFA
    MFAService.disable_mfa(db, current_user)
    
    return {"message": "MFA disabled successfully"}


# ============================================================================
# MFA STATUS ENDPOINT
# ============================================================================

@router.get(
    "/status",
    response_model=MFAStatusResponse,
    summary="Get MFA status",
    description="Check if MFA is enabled for the current user"
)
def get_mfa_status(
    current_user: User = Depends(get_current_user)
) -> MFAStatusResponse:
    """
    Get MFA status for the current user.
    """
    return MFAStatusResponse(mfa_enabled=current_user.mfa_enabled)


# ============================================================================
# MFA VERIFY ENDPOINT (for login)
# ============================================================================

@router.post(
    "/verify",
    response_model=TokenWithRefresh,
    summary="Verify MFA code",
    description="Verify MFA code during login"
)
def verify_mfa(
    request: MFAVerifyRequest,
    db: Session = Depends(get_db)
) -> TokenWithRefresh:
    """
    Verify MFA code and return access token.
    
    This is called after the initial login when MFA is required.
    """
    # Decode temp token
    payload = decode_token(request.temp_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Get user
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Verify TOTP code or backup code
    is_valid = False
    
    # Try TOTP first
    if MFAService.verify_user_totp(user, request.code):
        is_valid = True
    # Try backup code
    elif MFAService.verify_user_backup_code(db, user, request.code):
        is_valid = True
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid MFA code"
        )
    
    # Create full access token
    from app.core.security import create_refresh_token
    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "mfa_verified": True
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenWithRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


# ============================================================================
# BACKUP CODES REGENERATE ENDPOINT
# ============================================================================

@router.post(
    "/backup-codes/regenerate",
    response_model=BackupCodesResponse,
    summary="Regenerate backup codes",
    description="Generate new backup codes (invalidates old ones)"
)
def regenerate_backup_codes(
    request: MFADisableRequest,  # Reuse for password confirmation
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> BackupCodesResponse:
    """
    Regenerate backup codes.
    
    Requires password confirmation.
    Invalidates all previous backup codes.
    """
    # Check if MFA is enabled
    if not current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled"
        )
    
    # Verify password
    if not verify_password(request.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # Generate new backup codes
    backup_codes = MFAService.generate_backup_codes()
    
    # Hash and store
    import json
    hashed_codes = [MFAService.hash_backup_code(code) for code in backup_codes]
    current_user.mfa_backup_codes = json.dumps(hashed_codes)
    db.commit()
    
    return BackupCodesResponse(
        backup_codes=backup_codes,
        message="Backup codes regenerated successfully"
    )
