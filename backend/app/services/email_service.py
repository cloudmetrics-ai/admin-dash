"""
Email Service
=============

Service for sending emails (verification, password reset, etc.)
Supports SMTP email sending when configured, falls back to console logging.
"""

import secrets
import os
from datetime import datetime, timedelta
from typing import Optional
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class EmailService:
    """
    Email service for sending verification and password reset emails.
    
    Configuration (add to .env):
    - SMTP_HOST: SMTP server host (e.g., smtp.gmail.com)
    - SMTP_PORT: SMTP server port (e.g., 587)
    - SMTP_USER: SMTP username/email
    - SMTP_PASSWORD: SMTP password/app password
    - SMTP_FROM: From email address
    - SMTP_FROM_NAME: From name (optional)
    """
    
    @staticmethod
    def generate_token() -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_verification_token_expiry() -> datetime:
        """Generate expiry time for verification token (24 hours)"""
        return datetime.utcnow() + timedelta(hours=24)
    
    @staticmethod
    def generate_reset_token_expiry() -> datetime:
        """Generate expiry time for reset token (1 hour)"""
        return datetime.utcnow() + timedelta(hours=1)
    
    @staticmethod
    def is_token_valid(token_expires: Optional[datetime]) -> bool:
        """Check if token is still valid (not expired)"""
        if not token_expires:
            return False
        return datetime.utcnow() < token_expires
    
    @staticmethod
    def _is_smtp_configured() -> bool:
        """Check if SMTP is configured"""
        return all([
            os.getenv('SMTP_HOST'),
            os.getenv('SMTP_PORT'),
            os.getenv('SMTP_USER'),
            os.getenv('SMTP_PASSWORD'),
        ])
    
    @staticmethod
    async def _send_email_smtp(to_email: str, subject: str, html_body: str) -> None:
        """Send email via SMTP"""
        try:
            import aiosmtplib
            
            smtp_host = os.getenv('SMTP_HOST')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_user = os.getenv('SMTP_USER')
            smtp_password = os.getenv('SMTP_PASSWORD')
            smtp_from = os.getenv('SMTP_FROM', smtp_user)
            smtp_from_name = os.getenv('SMTP_FROM_NAME', 'Learn App')
            
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{smtp_from_name} <{smtp_from}>"
            message['To'] = to_email
            
            # Add HTML body
            html_part = MIMEText(html_body, 'html')
            message.attach(html_part)
            
            # Send email
            await aiosmtplib.send(
                message,
                hostname=smtp_host,
                port=smtp_port,
                username=smtp_user,
                password=smtp_password,
                use_tls=True,
            )
            
            logger.info(f"Email sent successfully to {to_email}")
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise
    
    @staticmethod
    async def send_verification_email(email: str, token: str) -> None:
        """
        Send email verification email.
        
        Args:
            email: User's email address
            token: Verification token
        """
        verification_link = f"http://localhost:3000/verify-email?token={token}"
        
        subject = "Verify Your Email Address"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #0071e3;">Verify Your Email Address</h2>
                    <p>Thank you for registering! Please click the button below to verify your email address:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_link}" 
                           style="background-color: #0071e3; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Verify Email
                        </a>
                    </div>
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="background-color: #f5f5f7; padding: 10px; border-radius: 5px; word-break: break-all;">
                        {verification_link}
                    </p>
                    <p style="color: #666; font-size: 14px;">This link expires in 24 hours.</p>
                    <p style="color: #666; font-size: 14px;">
                        If you didn't create an account, please ignore this email.
                    </p>
                </div>
            </body>
        </html>
        """
        
        if EmailService._is_smtp_configured():
            await EmailService._send_email_smtp(email, subject, html_body)
        else:
            # Fallback to console logging
            logger.info(f"""
            ========================================
            📧 VERIFICATION EMAIL
            ========================================
            To: {email}
            Subject: {subject}
            
            Click the link below to verify your email:
            {verification_link}
            
            This link expires in 24 hours.
            ========================================
            """)
            print(f"\n🔗 Verification link for {email}:")
            print(f"   {verification_link}\n")
    
    @staticmethod
    async def send_password_reset_email(email: str, token: str) -> None:
        """
        Send password reset email.
        
        Args:
            email: User's email address
            token: Reset token
        """
        reset_link = f"http://localhost:3000/reset-password?token={token}"
        
        subject = "Reset Your Password"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #0071e3;">Reset Your Password</h2>
                    <p>You requested to reset your password. Click the button below to set a new password:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" 
                           style="background-color: #0071e3; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Reset Password
                        </a>
                    </div>
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="background-color: #f5f5f7; padding: 10px; border-radius: 5px; word-break: break-all;">
                        {reset_link}
                    </p>
                    <p style="color: #666; font-size: 14px;">This link expires in 1 hour.</p>
                    <p style="color: #666; font-size: 14px;">
                        If you didn't request this, please ignore this email. Your password will not be changed.
                    </p>
                </div>
            </body>
        </html>
        """
        
        if EmailService._is_smtp_configured():
            await EmailService._send_email_smtp(email, subject, html_body)
        else:
            # Fallback to console logging
            logger.info(f"""
            ========================================
            📧 PASSWORD RESET EMAIL
            ========================================
            To: {email}
            Subject: {subject}
            
            Click the link below to reset your password:
            {reset_link}
            
            This link expires in 1 hour.
            ========================================
            """)
            print(f"\n🔗 Password reset link for {email}:")
            print(f"   {reset_link}\n")
