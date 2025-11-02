"""
SMS Notification Service
Supports Twilio SMS API
"""

import os
from typing import Optional, Dict


class SMSService:
    """Professional SMS notification service using Twilio."""
    
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER", "")
        self.enabled = bool(self.account_sid and self.auth_token and self.from_number)
    
    def send_sms(self, to_phone: str, message: str) -> bool:
        """
        Send SMS notification using Twilio.
        
        Args:
            to_phone: Recipient phone number (E.164 format: +1234567890)
            message: SMS message text
        
        Returns:
            bool: True if sent successfully
        """
        if not self.enabled:
            print("SMS service not configured. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER")
            return False
        
        if not to_phone:
            return False
        
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            
            message = client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_phone
            )
            
            return message.sid is not None
        except ImportError:
            print("Twilio not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            print(f"SMS error: {e}")
            return False
    
    def send_diagnosis_notification(self, to_phone: str, prediction_data: Dict, user_name: Optional[str] = None) -> bool:
        """
        Send diagnosis completion SMS notification.
        
        Args:
            to_phone: Recipient phone number
            prediction_data: Dictionary with prediction details
            user_name: Optional user name for personalization
        """
        if not to_phone:
            return False
        
        disease = prediction_data.get('predicted_class', 'Unknown')
        confidence = prediction_data.get('confidence', 0.0)
        confidence_pct = int(confidence * 100)
        
        # Determine urgency
        if confidence >= 0.8:
            urgency = "High"
            advice = "Consult dermatologist within 3-7 days."
        elif confidence >= 0.5:
            urgency = "Medium"
            advice = "Book appointment within 2-4 weeks."
        else:
            urgency = "Low"
            advice = "Monitor and recheck in 8-12 weeks."
        
        greeting = f"Hi {user_name}," if user_name else "Hello,"
        
        message = f"""{greeting} Your SkinVision AI analysis is complete.

Result: {disease} ({confidence_pct}% confidence)
Urgency: {urgency}
{advice}

View full report: http://localhost:3000/result

⚠️ This is informational only. Consult a dermatologist for medical advice."""

        return self.send_sms(to_phone, message)


# Singleton instance
sms_service = SMSService()
