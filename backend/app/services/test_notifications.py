"""
Test script for email and SMS notifications
Run this to verify your notification setup is working.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.email_service import email_service
from app.services.sms_service import sms_service


def test_email():
    """Test email notification."""
    print("=" * 50)
    print("Testing Email Notification")
    print("=" * 50)
    
    test_email = input("Enter test email address: ").strip()
    if not test_email:
        print("No email provided. Skipping email test.")
        return
    
    result = email_service.send_diagnosis_notification(
        to_email=test_email,
        patient_name="Test User",
        predicted_class="Melanoma",
        confidence=0.92,
        urgency_level="High",
        report_url="http://localhost:3000/result"
    )
    
    if result:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email. Check configuration.")


def test_sms():
    """Test SMS notification."""
    print("=" * 50)
    print("Testing SMS Notification")
    print("=" * 50)
    
    test_phone = input("Enter test phone number (E.164 format, e.g., +1234567890): ").strip()
    if not test_phone:
        print("No phone number provided. Skipping SMS test.")
        return
    
    result = sms_service.send_diagnosis_notification(
        to_phone=test_phone,
        predicted_class="Melanoma",
        confidence=0.92,
        urgency_level="High"
    )
    
    if result:
        print("✅ SMS sent successfully!")
    else:
        print("❌ Failed to send SMS. Check Twilio configuration.")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Notification Services Test")
    print("=" * 50)
    print()
    
    # Check if services are enabled
    print(f"Email notifications: {'✅ Enabled' if email_service.enabled else '❌ Disabled'}")
    print(f"SMS notifications: {'✅ Enabled' if sms_service.enabled else '❌ Disabled'}")
    print()
    
    choice = input("Test (1) Email, (2) SMS, or (3) Both [1/2/3]: ").strip()
    
    if choice == "1":
        test_email()
    elif choice == "2":
        test_sms()
    elif choice == "3":
        test_email()
        print()
        test_sms()
    else:
        print("Invalid choice.")
