# 🔐 CLOUDFLARE SECURITY SETUP GUIDE
# Spirit of the Immortals Ltd - Multi-Domain Security Configuration

## **📋 OVERVIEW**
This guide will secure all 4 domains with enterprise-grade security:
- thesmartshoppingsite.com
- thesmartshoppingsite.co.uk  
- spiritoftheimmortalsltd.co.uk
- spiritoftheimmortals.co.uk

---

## **🚀 STEP 1: DOMAIN SECURITY BASELINE**

### **A. SSL/TLS Configuration (Critical)**
For each domain in Cloudflare Dashboard:

```
SSL/TLS → Overview
├── Encryption Mode: Full (strict) ✅
├── Always Use HTTPS: ON ✅
└── Minimum TLS Version: 1.2 ✅

SSL/TLS → Edge Certificates
├── HSTS: ON (Max Age: 6 months) ✅
├── TLS 1.3: ON ✅
├── Automatic HTTPS Rewrites: ON ✅
└── Certificate Transparency Monitoring: ON ✅
```

### **B. Security Headers**
```
Security → Settings
├── Security Level: High ✅
├── Challenge Passage: 30 minutes ✅
├── Browser Integrity Check: ON ✅
└── Privacy Pass: ON ✅
```

---

## **🔒 STEP 2: CLOUDFLARE SECRET STORES STRATEGY**

### **Secret Store #1: Database Credentials**
```json
{
  "name": "spirit-immortals-database",
  "secrets": {
    "AWS_DB_HOST": "supermarket-db.cbu8qc0uk2re.eu-north-1.rds.amazonaws.com",
    "AWS_DB_NAME": "postgres",
    "AWS_DB_USER": "postgres",
    "AWS_DB_PASSWORD": "[YOUR_SECURE_PASSWORD]",
    "AWS_DB_PORT": "5432"
  }
}
```

### **Secret Store #2: JWT & Authentication**
```json
{
  "name": "spirit-immortals-auth",
  "secrets": {
    "JWT_SECRET_KEY": "[GENERATE_256_BIT_KEY]",
    "JWT_ALGORITHM": "HS256",
    "JWT_EXPIRATION_HOURS": "24",
    "PASSWORD_SALT_ROUNDS": "12"
  }
}
```

### **Secret Store #3: Email Configuration**
```json
{
  "name": "spirit-immortals-email",
  "secrets": {
    "SMTP_HOST": "smtp.gmail.com",
    "SMTP_PORT": "587",
    "SMTP_USER": "derek.j.king@live.com",
    "SMTP_PASSWORD": "[APP_SPECIFIC_PASSWORD]",
    "EMAIL_FROM_NAME": "Spirit of the Immortals Ltd"
  }
}
```

### **Secret Store #4: API Keys & Integrations**
```json
{
  "name": "spirit-immortals-apis",
  "secrets": {
    "CLOUDFLARE_API_TOKEN": "[YOUR_API_TOKEN]",
    "STRIPE_SECRET_KEY": "[WHEN_READY_FOR_PAYMENTS]",
    "ANALYTICS_KEY": "[GOOGLE_ANALYTICS_KEY]",
    "RECAPTCHA_SECRET": "[RECAPTCHA_SECRET]"
  }
}
```

---

## **🛡️ STEP 3: ADVANCED SECURITY FEATURES**

### **A. Web Application Firewall (WAF)**
```
Security → WAF
├── Managed Rules: ON ✅
│   ├── Cloudflare Managed Ruleset: ON
│   ├── Cloudflare OWASP Core Ruleset: ON
│   └── Cloudflare Exposed Credentials Check: ON
├── Rate Limiting: Configure per domain ✅
└── Custom Rules: Set up below ✅
```

### **B. Rate Limiting Rules**
```javascript
// Rule 1: Login Protection
Expression: (http.request.uri.path eq "/auth/login")
Action: Rate limit
Rate: 5 requests per minute per IP

// Rule 2: API Protection  
Expression: (http.request.uri.path contains "/api/")
Action: Rate limit
Rate: 100 requests per minute per IP

// Rule 3: Registration Protection
Expression: (http.request.uri.path eq "/auth/register")
Action: Rate limit
Rate: 3 requests per hour per IP
```

### **C. Custom Security Rules**
```javascript
// Block suspicious countries (adjust as needed)
Expression: (ip.geoip.country in {"CN" "RU" "KP"})
Action: Block

// Allow only HTTPS
Expression: (ssl != true)
Action: Redirect to HTTPS

// Block common attack patterns
Expression: (http.request.uri.query contains "union select" or 
           http.request.uri.query contains "../" or
           http.request.uri.query contains "<script")
Action: Block
```

---

## **🌍 STEP 4: DOMAIN-SPECIFIC SECURITY**

### **Shopping Platform Domains Security**
```
thesmartshoppingsite.com & thesmartshoppingsite.co.uk:
├── Bot Fight Mode: ON ✅
├── DDoS Protection: Automatic ✅  
├── Browser Integrity Check: ON ✅
└── Email Obfuscation: ON ✅
```

### **Company Domain Security**
```
spiritoftheimmortalsltd.co.uk & spiritoftheimmortals.co.uk:
├── Under Attack Mode: Available if needed ✅
├── Challenge Passage: 30 minutes ✅
├── Security Level: High ✅
└── Hotlink Protection: ON ✅
```

---

## **🔐 STEP 5: ACCESS CONTROL & AUTHENTICATION**

### **A. Cloudflare Access (Optional - Premium Feature)**
```
Zero Trust → Access → Applications
├── Create Application: "Spirit Immortals Admin"
├── Domain: admin.spiritoftheimmortals.co.uk  
├── Authentication: Email OTP
└── Policies: derek@spiritoftheimmortals.co.uk only
```

### **B. API Token Security**
```
My Profile → API Tokens
├── Create Token: "Spirit Immortals Production"
├── Permissions: Zone:Read, DNS:Edit, SSL:Edit
├── Zone Resources: Include all your domains
└── IP Address Filtering: Your server IP only
```

---

## **📊 STEP 6: MONITORING & ANALYTICS**

### **A. Security Analytics**
```
Analytics → Security
├── Monitor failed login attempts ✅
├── Track blocked requests ✅  
├── Review threat intel ✅
└── Set up email alerts ✅
```

### **B. Performance Monitoring**
```
Speed → Optimization
├── Auto Minify: CSS, JS, HTML ✅
├── Brotli Compression: ON ✅
├── Early Hints: ON ✅
└── Rocket Loader: ON (test first) ✅
```

---

## **🚨 STEP 7: INCIDENT RESPONSE PLAN**

### **Emergency Actions Available**
```
If under attack:
1. Enable "Under Attack Mode" ✅
2. Increase Security Level to "I'm Under Attack" ✅  
3. Add temporary blocking rules ✅
4. Contact Cloudflare Support if needed ✅
```

### **Monitoring Alerts**
```
Set up notifications for:
├── SSL certificate expiration (14 days) ✅
├── High error rates (>5% 5xx errors) ✅
├── DDoS attacks detected ✅
└── Failed login spikes (>10/minute) ✅
```

---

## **✅ SECURITY CHECKLIST**

### **Domain Setup:**
- [ ] All 4 domains added to Cloudflare
- [ ] DNS records properly configured  
- [ ] SSL certificates active (Full strict)
- [ ] HSTS enabled with 6-month max-age

### **Security Features:**
- [ ] WAF enabled with managed rules
- [ ] Rate limiting configured
- [ ] Custom security rules active
- [ ] Bot protection enabled

### **Secret Management:**
- [ ] Database secrets in Cloudflare store
- [ ] JWT secrets properly generated
- [ ] Email credentials secured
- [ ] API tokens with minimal permissions

### **Monitoring:**
- [ ] Security analytics enabled
- [ ] Performance monitoring active
- [ ] Alert notifications configured
- [ ] Incident response plan documented

---

## **🎯 SECURITY SCORE TARGET**

**Goal: A+ Rating on all security tests**
- SSL Labs: A+ ✅
- Security Headers: A+ ✅  
- Mozilla Observatory: A+ ✅
- Cloudflare Security Insights: Excellent ✅

**🏆 Your Spirit of the Immortals Ltd domains will have enterprise-grade security!**
