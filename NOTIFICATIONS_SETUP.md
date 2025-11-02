# 🔔 Notification System Setup Guide

SkinVision AI now includes **Email and SMS notifications** that automatically notify users when their diagnosis is complete!

## 📧 Email Notifications

### Quick Setup with Gmail (Development)

1. **Enable App Password** (if 2FA enabled):
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Generate App Password for "Mail"

2. **Set Environment Variables**:

**Windows PowerShell:**
```powershell
$env:EMAIL_NOTIFICATIONS_ENABLED = "true"
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "your-email@gmail.com"
$env:SMTP_PASSWORD = "your-app-password"
$env:FROM_EMAIL = "your-email@gmail.com"
```

**Linux/Mac:**
```bash
export EMAIL_NOTIFICATIONS_ENABLED=true
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export FROM_EMAIL=your-email@gmail.com
```

### Email Features

✅ **Beautiful HTML email** with diagnosis results  
✅ **Confidence score visualization**  
✅ **Urgency-based recommendations**  
✅ **Link to view full results**  
✅ **Medical disclaimer included**

---

## 📱 SMS Notifications

### Quick Setup with Twilio

1. **Sign up**: https://www.twilio.com/try-twilio
2. **Get credentials** from dashboard:
   - Account SID
   - Auth Token
   - Phone Number

3. **Set Environment Variables**:

**Windows PowerShell:**
```powershell
$env:SMS_NOTIFICATIONS_ENABLED = "true"
$env:TWILIO_ACCOUNT_SID = "your-account-sid"
$env:TWILIO_AUTH_TOKEN = "your-auth-token"
$env:TWILIO_FROM_NUMBER = "+1234567890"
```

**Linux/Mac:**
```bash
export SMS_NOTIFICATIONS_ENABLED=true
export TWILIO_ACCOUNT_SID=your-account-sid
export TWILIO_AUTH_TOKEN=your-auth-token
export TWILIO_FROM_NUMBER=+1234567890
```

### Phone Number Format

Use **E.164 format**: `+[country code][number]`

Examples:
- US: `+15551234567`
- UK: `+447911123456`
- India: `+919876543210`

### SMS Features

✅ **Concise summary** of diagnosis  
✅ **Confidence score**  
✅ **Urgency level**  
✅ **Link to view results**

---

## 🧪 Testing Notifications

### Test Email

```bash
cd backend/app/services
python test_notifications.py
```

Select option `1` for email test.

### Test SMS

```bash
cd backend/app/services
python test_notifications.py
```

Select option `2` for SMS test.

---

## ⚙️ User Preferences

Users can manage notification preferences via API:

### Get Preferences
```bash
GET /notifications/preferences
Headers: Authorization: Bearer <token>
```

### Update Preferences
```bash
PUT /notifications/preferences
Headers: Authorization: Bearer <token>
Body: {
  "phone_number": "+1234567890",
  "email_notifications": "true",
  "sms_notifications": "true"
}
```

---

## 🔄 How It Works

1. **User uploads image** → Gets analyzed
2. **Diagnosis complete** → Prediction saved
3. **Notifications sent automatically** (in background):
   - ✅ Email (if enabled and user has email notifications on)
   - ✅ SMS (if enabled and user has phone + SMS enabled)

**Notifications are non-blocking** - they don't slow down the API response!

---

## 💰 Cost Considerations

**Email:**
- Gmail: Free (up to 500/day)
- SendGrid: Free tier (100/day)
- Other SMTP: Varies

**SMS (Twilio):**
- ~$0.0075 per SMS in US
- Free trial: $15.50 credit
- 💡 **Tip**: Enable SMS only for high-urgency cases

---

## 🚫 Disabling Notifications

Simply don't set the environment variables, or set:
```bash
export EMAIL_NOTIFICATIONS_ENABLED=false
export SMS_NOTIFICATIONS_ENABLED=false
```

---

## 📚 More Information

- **Detailed config**: [backend/app/services/notification_config.md](backend/app/services/notification_config.md)
- **API docs**: http://localhost:8000/docs
- **Router docs**: [backend/app/routers/README_NOTIFICATIONS.md](backend/app/routers/README_NOTIFICATIONS.md)
