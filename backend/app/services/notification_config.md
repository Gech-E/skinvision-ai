# Notification Configuration Guide

## Email Notifications Setup

### Option 1: Gmail SMTP (Recommended for Development)

1. **Enable App Passwords** (if 2FA is enabled):
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Generate App Password for "Mail"

2. **Set Environment Variables:**
```bash
# Windows PowerShell
$env:EMAIL_NOTIFICATIONS_ENABLED = "true"
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "your-email@gmail.com"
$env:SMTP_PASSWORD = "your-app-password"
$env:FROM_EMAIL = "your-email@gmail.com"
```

```bash
# Linux/Mac
export EMAIL_NOTIFICATIONS_ENABLED=true
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export FROM_EMAIL=your-email@gmail.com
```

### Option 2: SendGrid (Production Recommended)

1. **Sign up for SendGrid**: https://sendgrid.com
2. **Create API Key**
3. **Set Environment Variables:**
```bash
export EMAIL_NOTIFICATIONS_ENABLED=true
export SMTP_HOST=smtp.sendgrid.net
export SMTP_PORT=587
export SMTP_USER=apikey
export SMTP_PASSWORD=your-sendgrid-api-key
export FROM_EMAIL=noreply@yourdomain.com
```

### Option 3: Other SMTP Providers

**Outlook/Hotmail:**
```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

**Yahoo:**
```bash
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Custom SMTP:**
```bash
SMTP_HOST=your-smtp-server.com
SMTP_PORT=587  # or 465 for SSL
```

## SMS Notifications Setup (Twilio)

### Step 1: Create Twilio Account

1. Sign up at: https://www.twilio.com/try-twilio
2. Get a phone number from Twilio
3. Get your Account SID and Auth Token from dashboard

### Step 2: Install Twilio

```bash
pip install twilio
```

### Step 3: Set Environment Variables

```bash
# Windows PowerShell
$env:SMS_NOTIFICATIONS_ENABLED = "true"
$env:TWILIO_ACCOUNT_SID = "your-account-sid"
$env:TWILIO_AUTH_TOKEN = "your-auth-token"
$env:TWILIO_FROM_NUMBER = "+1234567890"  # Your Twilio number

# Linux/Mac
export SMS_NOTIFICATIONS_ENABLED=true
export TWILIO_ACCOUNT_SID=your-account-sid
export TWILIO_AUTH_TOKEN=your-auth-token
export TWILIO_FROM_NUMBER=+1234567890
```

### Phone Number Format

Phone numbers must be in **E.164 format**: `+[country code][number]`

Examples:
- US: `+15551234567`
- UK: `+447911123456`
- India: `+919876543210`

## Testing Notifications

### Test Email

```bash
# Using Python
python -c "
from app.services.email_service import email_service
email_service.send_diagnosis_notification(
    to_email='test@example.com',
    predicted_class='Melanoma',
    confidence=0.92,
    urgency_level='High'
)
"
```

### Test SMS

```bash
# Using Python
python -c "
from app.services.sms_service import sms_service
sms_service.send_diagnosis_notification(
    to_phone='+1234567890',
    predicted_class='Melanoma',
    confidence=0.92,
    urgency_level='High'
)
"
```

## User Notification Preferences

Users can manage their notification preferences via API:

**Get Preferences:**
```
GET /notifications/preferences
Headers: Authorization: Bearer <token>
```

**Update Preferences:**
```
PUT /notifications/preferences
Headers: Authorization: Bearer <token>
Body: {
  "phone_number": "+1234567890",
  "email_notifications": "true",
  "sms_notifications": "true"
}
```

## Disable Notifications

To disable notifications completely:

```bash
export EMAIL_NOTIFICATIONS_ENABLED=false
export SMS_NOTIFICATIONS_ENABLED=false
```

Or simply don't set the credentials - notifications will be skipped gracefully.

## Cost Considerations

**Email (SMTP):**
- Gmail: Free (up to 500 emails/day)
- SendGrid: Free tier (100 emails/day)
- Custom SMTP: Varies by provider

**SMS (Twilio):**
- ~$0.0075 per SMS in US
- Free trial: $15.50 credit
- Recommended: Enable only for high-urgency cases

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** or secrets management
3. **Use App Passwords** instead of main passwords (Gmail)
4. **Rotate credentials** periodically
5. **Use dedicated email** for notifications (not personal)
