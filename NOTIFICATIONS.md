# Email & SMS Notifications + OTP Authentication

This document explains the notification and OTP authentication features in SkinVision AI.

## Features

### 1. Email Notifications
When a user completes a diagnosis, they automatically receive an email notification with:
- Predicted disease and confidence level
- Urgency assessment (High/Medium/Low)
- Medical recommendations
- Link to view full report

### 2. SMS Notifications
Optional SMS notifications can be sent via Twilio for users who prefer text messages.

### 3. OTP Authentication for History Access
For enhanced security when accessing prediction history, users can enable OTP verification:
- Request OTP via email or SMS
- 6-digit code valid for 10 minutes
- One-time use only
- Session token valid for 30 minutes after verification

## Configuration

### Email Configuration

**Option 1: SMTP (Gmail, Outlook, etc.)**
```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export FROM_EMAIL=your-email@gmail.com
export FROM_NAME="SkinVision AI"
```

**Option 2: SendGrid API**
```bash
export SENDGRID_API_KEY=your-sendgrid-api-key
export FROM_EMAIL=noreply@yourdomain.com
export FROM_NAME="SkinVision AI"
```

### SMS Configuration (Twilio)

```bash
export TWILIO_ACCOUNT_SID=your-account-sid
export TWILIO_AUTH_TOKEN=your-auth-token
export TWILIO_PHONE_NUMBER=+1234567890  # Your Twilio phone number
```

### OTP Configuration

```bash
export OTP_EXPIRY_MINUTES=10  # Default: 10 minutes
export OTP_LENGTH=6  # Default: 6 digits
```

## API Endpoints

### Notification Settings

**GET `/notifications/settings`**
Get user notification preferences.

**PUT `/notifications/settings`**
Update notification preferences:
```json
{
  "phone_number": "+1234567890",
  "email_notifications": true,
  "sms_notifications": false,
  "name": "John Doe"
}
```

### OTP Authentication

**POST `/otp/request`**
Request OTP for history access:
```json
{
  "email": "user@example.com",  // Optional if configured in account
  "phone": "+1234567890"  // Optional if configured in account
}
```

**POST `/otp/verify`**
Verify OTP and get session token:
```json
{
  "email": "user@example.com",  // Or phone
  "otp": "123456"
}
```

Returns:
```json
{
  "session_token": "eyJ...",
  "expires_in": 1800
}
```

### History with OTP

**GET `/history/?require_otp=true`**
Access history with OTP verification required. Must use OTP session token from `/otp/verify`.

## User Flow

1. User completes diagnosis → Email/SMS notification sent automatically
2. User wants to access history → Click "Secure Reload" or access requires OTP
3. User requests OTP → Code sent via email/SMS
4. User enters OTP → Receives session token (valid 30 minutes)
5. User accesses history with session token

## Frontend Integration

The Admin dashboard includes:
- OTP modal component (`OTPModal.jsx`)
- "Secure Reload" button to enable OTP verification
- Automatic OTP prompt if required

## Security Notes

- OTPs expire after 10 minutes (configurable)
- OTPs can only be used once
- Maximum 5 verification attempts per OTP
- OTP session tokens expire after 30 minutes
- Failed OTP attempts are logged

## Development/Testing

For local development without email/SMS setup:
- Email service will log to console if not configured
- SMS service will log to console if not configured
- OTP codes are still generated and can be found in server logs (not recommended for production)

## Production Recommendations

1. Use SendGrid or AWS SES for email delivery
2. Use Twilio for SMS delivery
3. Consider Redis for OTP storage (instead of in-memory)
4. Implement rate limiting on OTP requests
5. Monitor failed OTP attempts for security
6. Use HTTPS for all API calls

