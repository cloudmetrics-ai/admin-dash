# SMTP Configuration Guide

## Option 1: Gmail (Recommended for Development)

### Step 1: Enable 2-Factor Authentication
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification if not already enabled

### Step 2: Create App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Name it "Learn App" or similar
4. Click "Generate"
5. Copy the 16-character password (no spaces)

### Step 3: Add to .env
```env
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM=your-email@gmail.com
SMTP_FROM_NAME=Learn App
```

---

## Option 2: SendGrid (Recommended for Production)

### Step 1: Create Account
1. Go to https://sendgrid.com/
2. Sign up for free account (100 emails/day)

### Step 2: Create API Key
1. Go to Settings → API Keys
2. Create API Key with "Full Access"
3. Copy the API key

### Step 3: Add to .env
```env
# Email Configuration (SendGrid)
SENDGRID_API_KEY=your-api-key-here
SMTP_FROM=noreply@yourdomain.com
SMTP_FROM_NAME=Learn App
```

---

## Option 3: Other SMTP Providers

### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### Yahoo
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

---

## Testing

After configuration:
1. Restart your backend server
2. Register a new user
3. Check your email inbox
4. Click the verification link

---

## Troubleshooting

**"Authentication failed"**
- Double-check username/password
- For Gmail, ensure you're using App Password, not regular password
- Check 2FA is enabled

**"Connection refused"**
- Check SMTP_HOST and SMTP_PORT
- Ensure firewall allows outbound connections on port 587

**"Emails not arriving"**
- Check spam folder
- Verify SMTP_FROM email is valid
- Check email provider's sending limits
