# 🚀 CLOUDFLARE DASHBOARD QUICK SETUP
**Spirit of the Immortals Ltd - Domain Security Setup**

## **⚡ 15-MINUTE SECURITY SETUP**

### **STEP 1: Add Domains (5 minutes)**
```
Dashboard → Add a Site
├── thesmartshoppingsite.com
├── thesmartshoppingsite.co.uk  
├── spiritoftheimmortalsltd.co.uk
└── spiritoftheimmortals.co.uk
```

### **STEP 2: Essential Security (5 minutes)**
For EACH domain:
```
SSL/TLS → Overview
├── Encryption Mode: Full (strict) ✅
└── Always Use HTTPS: ON ✅

SSL/TLS → Edge Certificates  
├── HSTS: ON (Max Age: 6 months) ✅
└── TLS 1.3: ON ✅

Security → Settings
├── Security Level: High ✅
└── Bot Fight Mode: ON ✅
```

### **STEP 3: Secret Stores (5 minutes)**
```
Workers & Pages → Secret Stores → Create

Store 1: "spirit-immortals-database"
├── AWS_DB_PASSWORD = [YOUR_SECURE_PASSWORD]
└── JWT_SECRET_KEY = [GENERATE: openssl rand -hex 32]

Store 2: "spirit-immortals-email"  
├── SMTP_PASSWORD = [GMAIL_APP_PASSWORD]
└── ADMIN_EMAIL = derek@spiritoftheimmortals.co.uk
```

---

## **🔒 COPY-PASTE CONFIGURATIONS**

### **Rate Limiting Rules**
```javascript
// Login Protection
Expression: (http.request.uri.path eq "/auth/login")  
Action: Block
Rate: 5 requests per minute

// API Protection
Expression: (http.request.uri.path contains "/api/")
Action: Rate limit  
Rate: 100 requests per minute

// Registration Protection
Expression: (http.request.uri.path eq "/auth/register")
Action: Block
Rate: 3 requests per hour
```

### **Security Headers**
```
Navigate to: Rules → Transform Rules → Modify Response Header

Add these headers for ALL domains:
├── Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
├── X-Content-Type-Options: nosniff
├── X-Frame-Options: DENY  
├── X-XSS-Protection: 1; mode=block
└── Referrer-Policy: strict-origin-when-cross-origin
```

---

## **📧 NOTIFICATION SETUP**

```
Account → Notifications

Create alerts for:
├── SSL Certificate Expiring (14 days)
├── DDoS Attack Detected (Immediate)
├── High Error Rate (>5% for 15 minutes)
└── Security Event (Immediate)

Email: derek@spiritoftheimmortals.co.uk
```

---

## **✅ VERIFICATION CHECKLIST**

Test these URLs after setup:
- [ ] https://thesmartshoppingsite.com (Green padlock)
- [ ] https://thesmartshoppingsite.co.uk (Green padlock)
- [ ] https://spiritoftheimmortalsltd.co.uk (Green padlock)  
- [ ] https://spiritoftheimmortals.co.uk (Green padlock)

Check security:
- [ ] SSL Labs Test: A+ rating
- [ ] Security Headers Test: A+ rating
- [ ] HTTP → HTTPS redirect working
- [ ] Rate limiting active (test login endpoint)

---

## **🎯 PRIORITY ORDER**

1. **🔥 CRITICAL (Do first):** SSL/TLS Full (strict) + HSTS
2. **🚨 HIGH:** Rate limiting on /auth/ endpoints  
3. **⚡ MEDIUM:** Security headers implementation
4. **📊 LOW:** Analytics and monitoring setup

**⏱️ Total setup time: 15-30 minutes for enterprise-grade security!**
