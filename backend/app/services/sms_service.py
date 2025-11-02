"""
SMS Notification Service
Handles sending SMS notifications for diagnosis completion.
Supports Twilio and other SMS providers.
"""

import os
from typing import Optional


class SMSService:
    """Service for sending SMS notifications."""
    
    def __init__(self):
        # Twilio Configuration
        self.twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
        self.twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
        self.twilio_from_number = os.environ.get("TWILIO_FROM_NUMBER", "")
        self.enabled = os.environ.get("SMS_NOTIFICATIONS_ENABLED", "false").lower() == "true"
        
        # Initialize Twilio client if credentials are available
        self.twilio_client = None
        if self.enabled and self.twilio_account_sid and self.twilio_auth_token:
            try:
                from twilio.rest import Client
                self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
                print("SMS service initialized with Twilio")
            except ImportError:
                print("Twilio not installed. Install with: pip install twilio")
                self.enabled = False
            except Exception as e:
                print(f"Failed to initialize Twilio: {e}")
                self.enabled = False
    
    def send_diagnosis_notification(
        self,
        to_phone: str,
        predicted_class: str = "Unknown",
        confidence: float = 0.0,
        urgency_level: str = "Low"
    ) -> bool:
        """
        Send diagnosis completion notification SMS.
        
        Args:
            to_phone: Recipient phone number (E.164 format: +1234567890)
            predicted_class: Predicted disease class
            confidence: Confidence score (0-1)
            urgency_level: Urgency level (High/Medium/Low)
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            print("SMS notifications are disabled")
            return False
        
        if not to_phone:
            print("No phone number provided")
            return False
        
        # Format phone number (ensure + prefix)
        if not to_phone.startswith('+'):
            to_phone = '+' + to_phone.lstrip('+')
        
        try:
            # Create SMS message
            confidence_pct = round(confidence * 100, 1)
            
            # Determine urgency message
            if urgency_level == "High":
                urgency_msg = "⚠️ HIGH URGENCY - Consult dermatologist within 3-7 days."
            elif urgency_level == "Medium":
                urgency_msg = "📋 MEDIUM - Book appointment within 2-4 weeks."
            else:
                urgency_msg = "✅ LOW - Monitor and recheck in 8-12 weeks."
            
            message_body = f"""SkinVision AI - Diagnosis Complete

Result: {predicted_class}
Confidence: {confidence_pct}%

{urgency_msg}

View full results: http://localhost:3000/result

⚠️ For informational purposes only. Not a substitute for medical advice."""

            # Send via Twilio
            if self.twilio_client:
                message = self.twilio_client.messages.create(
                    body=message_body,
                    from_=self.twilio_from_number,
                    to=to_phone
                )
                print(f"SMS notification sent to {to_phone}. SID: {message.sid}")
                return True
            else:
                print("SMS service not configured")
                return False
                
        except Exception as e:
            print(f"Failed to send SMS notification: {e}")
            return False


# Global instance
sms_service = SMSService()
