# Notification System Documentation

## Overview

SkinVision AI now includes email and SMS notification capabilities to notify users when their diagnosis is complete.

## Features

- ✅ **Email Notifications** - HTML email with diagnosis results
- ✅ **SMS Notifications** - Text message with key results
- ✅ **User Preferences** - Users can enable/disable notifications
- ✅ **Background Processing** - Notifications don't block API response
- ✅ **Automatic Urgency Messages** - Different messages based on severity

## How It Works

### Automatic Notifications

When a user completes a diagnosis:

1. **Prediction is saved** to database
2. **Notifications are queued** (background task)
3. **Email sent** (if enabled and user has email notifications on)
4. **SMS sent** (if enabled and user has phone number + SMS enabled)

### Notification Content

**Email includes:**
- Diagnosis result (disease name)
- Confidence percentage with visual bar
- Urgency level with color coding
- Medical recommendations
- Link to view full results
- Download report link

**SMS includes:**
- Diagnosis result
- Confidence score
- Urgency level message
- Link to view results

## Setup Instructions

### Quick Start (Development)

**Email with Gmail:**
```bash
export EMAIL_NOTIFICATIONS_ENABLED=true
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
```

**SMS with Twilio:**
```bash
export SMS_NOTIFICATIONS_ENABLED=true
export TWILIO_ACCOUNT_SID=your-sid
export TWILIO_AUTH_TOKEN=your-token
export TWILIO_FROM_NUMBER=+1234567890
```

See [notification_config.md](../services/notification_config.md) for detailed setup.

## API Endpoints

### Get Notification Preferences
```
GET /notifications/preferences
Headers: Authorization: Bearer <token>

Response:
{
  "id": 1,
  "email": "user@example.com",
  "phone_number": "+1234567890",
  "email_notifications": "true",
  "sms_notifications": "false"
}
```

### Update Notification Preferences
```
PUT /notifications/preferences
Headers: Authorization: Bearer <token>
Body: {
  "phone_number": "+1234567890",
  "email_notifications": "true",
  "sms_notifications": "true"
}
```

## User Flow

1. **User signs up** → Email notifications enabled by default
2. **User uploads image** → Gets analyzed
3. **Diagnosis complete** → Notifications sent automatically
4. **User receives:**
   - Email with full details
   - SMS with summary (if enabled)

## Testing

Run the test script:
```bash
cd backend/app/services
python test_notifications.py
```

## Disabling Notifications

Notifications are **opt-in** by default. They only send if:
- Service is enabled (environment variables set)
- User has notifications enabled in preferences
- User has email/phone configured

To disable completely, don't set the environment variables.
