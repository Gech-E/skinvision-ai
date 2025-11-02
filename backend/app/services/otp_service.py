"""
OTP (One-Time Password) Service for History Access Authentication
Generates and validates time-based OTPs sent via email or SMS
"""

import os
import secrets
import time
from typing import Dict, Optional
from datetime import datetime, timedelta
from .email_service import email_service
from .sms_service import sms_service


class OTPService:
    """OTP generation and validation service with expiration."""
    
    def __init__(self):
        self.otp_expiry_minutes = int(os.getenv("OTP_EXPIRY_MINUTES", "10"))
        self.otp_length = int(os.getenv("OTP_LENGTH", "6"))
        # In-memory storage for OTPs (in production, use Redis or database)
        self.otp_store: Dict[str, Dict] = {}
        # Cleanup expired OTPs periodically
        self._cleanup_interval = 300  # 5 minutes
        self._last_cleanup = time.time()
    
    def generate_otp(self) -> str:
        """Generate a random numeric OTP."""
        return ''.join([str(secrets.randbelow(10)) for _ in range(self.otp_length)])
    
    def send_otp_email(self, email: str, user_name: Optional[str] = None) -> tuple[str, bool]:
        """
        Generate and send OTP via email.
        
        Returns:
            tuple: (otp_code, success)
        """
        otp = self.generate_otp()
        expires_at = datetime.now() + timedelta(minutes=self.otp_expiry_minutes)
        
        # Store OTP
        self.otp_store[email] = {
            'otp': otp,
            'expires_at': expires_at,
            'attempts': 0,
            'max_attempts': 5
        }
        
        # Send email
        subject = "Your OTP for History Access - SkinVision AI"
        html_content = self._generate_otp_email_template(otp, user_name)
        text_content = f"Your OTP code is: {otp}\n\nThis code will expire in {self.otp_expiry_minutes} minutes.\n\nIf you didn't request this code, please ignore this email."
        
        success = email_service.send_email_smtp(email, subject, html_content, text_content) or \
                  email_service.send_email_sendgrid(email, subject, html_content, text_content)
        
        return otp, success
    
    def send_otp_sms(self, phone: str, user_name: Optional[str] = None) -> tuple[str, bool]:
        """
        Generate and send OTP via SMS.
        
        Returns:
            tuple: (otp_code, success)
        """
        otp = self.generate_otp()
        expires_at = datetime.now() + timedelta(minutes=self.otp_expiry_minutes)
        
        # Store OTP
        self.otp_store[phone] = {
            'otp': otp,
            'expires_at': expires_at,
            'attempts': 0,
            'max_attempts': 5
        }
        
        # Send SMS
        message = f"Your SkinVision AI OTP: {otp}\nExpires in {self.otp_expiry_minutes} minutes."
        success = sms_service.send_sms(phone, message)
        
        return otp, success
    
    def verify_otp(self, identifier: str, provided_otp: str) -> bool:
        """
        Verify OTP code.
        
        Args:
            identifier: Email or phone number
            provided_otp: OTP code provided by user
        
        Returns:
            bool: True if valid, False otherwise
        """
        self._cleanup_expired()
        
        if identifier not in self.otp_store:
            return False
        
        otp_data = self.otp_store[identifier]
        
        # Check expiration
        if datetime.now() > otp_data['expires_at']:
            del self.otp_store[identifier]
            return False
        
        # Check attempts
        if otp_data['attempts'] >= otp_data['max_attempts']:
            del self.otp_store[identifier]
            return False
        
        # Verify OTP
        if otp_data['otp'] == provided_otp:
            # Valid OTP - delete it (one-time use)
            del self.otp_store[identifier]
            return True
        
        # Invalid OTP - increment attempts
        otp_data['attempts'] += 1
        return False
    
    def _cleanup_expired(self):
        """Remove expired OTPs from storage."""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        now = datetime.now()
        expired_keys = [
            key for key, data in self.otp_store.items()
            if now > data['expires_at']
        ]
        
        for key in expired_keys:
            del self.otp_store[key]
        
        self._last_cleanup = current_time
    
    def _generate_otp_email_template(self, otp: str, user_name: Optional[str] = None) -> str:
        """Generate HTML email template for OTP."""
        greeting = f"Hello {user_name}," if user_name else "Hello,"
        expiry = self.otp_expiry_minutes
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #17252A; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2B7A78, #3AAFA9); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 30px; border: 1px solid #DEF2F1; }}
                .otp-box {{ background: #DEF2F1; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0; }}
                .otp-code {{ font-size: 48px; font-weight: bold; color: #2B7A78; letter-spacing: 10px; margin: 20px 0; }}
                .footer {{ background: #17252A; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 SkinVision AI</h1>
                    <p>One-Time Password</p>
                </div>
                <div class="content">
                    <p>{greeting}</p>
                    <p>You requested to access your prediction history. Use the OTP code below to authenticate:</p>
                    
                    <div class="otp-box">
                        <div style="margin-bottom: 10px; color: #17252A;">Your OTP Code:</div>
                        <div class="otp-code">{otp}</div>
                        <div style="margin-top: 10px; color: #17252A; font-size: 14px;">
                            Valid for {expiry} minutes
                        </div>
                    </div>
                    
                    <p style="font-size: 14px; color: #666;">
                        <strong>Security Notice:</strong> Never share this code with anyone. 
                        SkinVision AI will never ask for your password or OTP via phone or email.
                    </p>
                    
                    <p style="font-size: 14px; color: #666;">
                        If you didn't request this OTP, please ignore this email or contact support.
                    </p>
                </div>
                <div class="footer">
                    <p><strong>SkinVision AI</strong> - Secure Access</p>
                    <p>This is an automated notification. Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html


# Singleton instance
otp_service = OTPService()

