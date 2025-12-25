"""
MFA Service
===========

Service layer for Multi-Factor Authentication operations.
Handles TOTP generation, verification, QR code creation, and backup codes.
"""

import pyotp
import qrcode
import io
import base64
import secrets
import hashlib
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.config import settings


class MFAService:
    """Service for handling MFA operations"""
    
    @staticmethod
    def generate_secret() -> str:
        """
        Generate a random TOTP secret.
        
        Returns:
            str: Base32 encoded secret
        """
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(user_email: str, secret: str) -> str:
        """
        Generate QR code for TOTP setup.
        
        Args:
            user_email: User's email address
            secret: TOTP secret
            
        Returns:
            str: Data URL of QR code image
        """
        # Create TOTP URI
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user_email,
            issuer_name=settings.PROJECT_NAME
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 data URL
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    @staticmethod
    def verify_totp(secret: str, code: str, window: int = 1) -> bool:
        """
        Verify TOTP code.
        
        Args:
            secret: TOTP secret
            code: 6-digit code to verify
            window: Time window tolerance (default 1 = ±30 seconds)
            
        Returns:
            bool: True if code is valid
        """
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(code, valid_window=window)
        except Exception:
            return False
    
    @staticmethod
    def generate_backup_codes(count: int = 10) -> List[str]:
        """
        Generate backup codes for account recovery.
        
        Args:
            count: Number of codes to generate
            
        Returns:
            List[str]: List of backup codes
        """
        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(8))
            codes.append(code)
        return codes
    
    @staticmethod
    def hash_backup_code(code: str) -> str:
        """
        Hash a backup code for secure storage.
        
        Args:
            code: Backup code to hash
            
        Returns:
            str: Hashed code
        """
        return hashlib.sha256(code.encode()).hexdigest()
    
    @staticmethod
    def verify_backup_code(code: str, hashed_codes: List[str]) -> Tuple[bool, Optional[str]]:
        """
        Verify a backup code and return the hash if valid.
        
        Args:
            code: Backup code to verify
            hashed_codes: List of hashed backup codes
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, matched_hash)
        """
        code_hash = MFAService.hash_backup_code(code)
        if code_hash in hashed_codes:
            return True, code_hash
        return False, None
    
    @staticmethod
    def encrypt_secret(secret: str) -> str:
        """
        Encrypt MFA secret for storage.
        
        For now, we'll use base64 encoding.
        In production, use proper encryption (e.g., Fernet from cryptography library).
        
        Args:
            secret: Plain text secret
            
        Returns:
            str: Encrypted secret
        """
        # TODO: Implement proper encryption in production
        return base64.b64encode(secret.encode()).decode()
    
    @staticmethod
    def decrypt_secret(encrypted_secret: str) -> str:
        """
        Decrypt MFA secret.
        
        Args:
            encrypted_secret: Encrypted secret
            
        Returns:
            str: Plain text secret
        """
        # TODO: Implement proper decryption in production
        return base64.b64decode(encrypted_secret.encode()).decode()
    
    @staticmethod
    def setup_mfa(user_email: str) -> Tuple[str, str, List[str]]:
        """
        Setup MFA for a user (generate secret, QR code, and backup codes).
        
        Args:
            user_email: User's email address
            
        Returns:
            Tuple[str, str, List[str]]: (secret, qr_code, backup_codes)
        """
        secret = MFAService.generate_secret()
        qr_code = MFAService.generate_qr_code(user_email, secret)
        backup_codes = MFAService.generate_backup_codes()
        
        return secret, qr_code, backup_codes
    
    @staticmethod
    def enable_mfa(db: Session, user: User, secret: str, backup_codes: List[str]) -> None:
        """
        Enable MFA for a user.
        
        Args:
            db: Database session
            user: User object
            secret: TOTP secret
            backup_codes: List of backup codes
        """
        # Encrypt and store secret
        user.mfa_secret = MFAService.encrypt_secret(secret)
        user.mfa_enabled = True
        
        # Hash and store backup codes
        hashed_codes = [MFAService.hash_backup_code(code) for code in backup_codes]
        import json
        user.mfa_backup_codes = json.dumps(hashed_codes)
        
        db.commit()
    
    @staticmethod
    def disable_mfa(db: Session, user: User) -> None:
        """
        Disable MFA for a user.
        
        Args:
            db: Database session
            user: User object
        """
        user.mfa_enabled = False
        user.mfa_secret = None
        user.mfa_backup_codes = None
        db.commit()
    
    @staticmethod
    def verify_user_totp(user: User, code: str) -> bool:
        """
        Verify TOTP code for a user.
        
        Args:
            user: User object
            code: 6-digit code to verify
            
        Returns:
            bool: True if code is valid
        """
        if not user.mfa_enabled or not user.mfa_secret:
            return False
        
        secret = MFAService.decrypt_secret(user.mfa_secret)
        return MFAService.verify_totp(secret, code)
    
    @staticmethod
    def verify_user_backup_code(db: Session, user: User, code: str) -> bool:
        """
        Verify and consume a backup code for a user.
        
        Args:
            db: Database session
            user: User object
            code: Backup code to verify
            
        Returns:
            bool: True if code is valid
        """
        if not user.mfa_enabled or not user.mfa_backup_codes:
            return False
        
        import json
        hashed_codes = json.loads(user.mfa_backup_codes)
        is_valid, matched_hash = MFAService.verify_backup_code(code, hashed_codes)
        
        if is_valid:
            # Remove used backup code
            hashed_codes.remove(matched_hash)
            user.mfa_backup_codes = json.dumps(hashed_codes)
            db.commit()
            return True
        
        return False
