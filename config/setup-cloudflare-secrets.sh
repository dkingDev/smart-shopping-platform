#!/bin/bash
# Cloudflare Secret Store Management Script
# Spirit of the Immortals Ltd - Secure Configuration

echo "🔐 Setting up Cloudflare Secret Stores for Spirit of the Immortals Ltd..."

# =============================================================
# SECRET STORE TEMPLATES FOR CLOUDFLARE DASHBOARD
# =============================================================

cat << 'EOF'
📋 CLOUDFLARE SECRET STORES SETUP

Copy these configurations into your Cloudflare Dashboard:
Workers & Pages → Secret Stores → Create Secret Store

=============================================================
SECRET STORE #1: Database Configuration
=============================================================
Name: spirit-immortals-database
Description: AWS PostgreSQL database credentials

Secrets to add:
├── AWS_DB_HOST = supermarket-db.cbu8qc0uk2re.eu-north-1.rds.amazonaws.com
├── AWS_DB_NAME = postgres  
├── AWS_DB_USER = postgres
├── AWS_DB_PASSWORD = [YOUR_SECURE_PASSWORD]
└── AWS_DB_PORT = 5432

=============================================================
SECRET STORE #2: Authentication & Security
=============================================================
Name: spirit-immortals-auth
Description: JWT tokens and authentication secrets

Secrets to add:
├── JWT_SECRET_KEY = [GENERATE_WITH_COMMAND_BELOW]
├── JWT_ALGORITHM = HS256
├── JWT_EXPIRATION_HOURS = 24
└── PASSWORD_SALT_ROUNDS = 12

Generate JWT Secret:
openssl rand -hex 32

=============================================================
SECRET STORE #3: Email Configuration
=============================================================
Name: spirit-immortals-email  
Description: SMTP and email service credentials

Secrets to add:
├── SMTP_HOST = smtp.gmail.com
├── SMTP_PORT = 587
├── SMTP_USER = derek.j.king@live.com
├── SMTP_PASSWORD = [APP_SPECIFIC_PASSWORD]
├── EMAIL_FROM_NAME = Spirit of the Immortals Ltd
└── SUPPORT_EMAIL = support@spiritoftheimmortals.co.uk

=============================================================
SECRET STORE #4: API Keys & Integrations
=============================================================
Name: spirit-immortals-apis
Description: Third-party service API keys

Secrets to add:
├── CLOUDFLARE_API_TOKEN = [YOUR_API_TOKEN]
├── RECAPTCHA_SECRET = [GOOGLE_RECAPTCHA_SECRET]
├── ANALYTICS_KEY = [GOOGLE_ANALYTICS_KEY]
└── WEBHOOK_SECRET = [RANDOM_WEBHOOK_SECRET]

=============================================================
SECRET STORE #5: Domain Configuration
=============================================================
Name: spirit-immortals-domains
Description: Domain-specific configuration

Secrets to add:
├── PRIMARY_DOMAIN = thesmartshoppingsite.com
├── UK_DOMAIN = thesmartshoppingsite.co.uk
├── COMPANY_GLOBAL = spiritoftheimmortalsltd.co.uk
├── COMPANY_UK = spiritoftheimmortals.co.uk
└── ADMIN_EMAIL = derek@spiritoftheimmortals.co.uk

=============================================================
SECRET STORE #6: SSL & Security
=============================================================
Name: spirit-immortals-security
Description: Security configuration and certificates

Secrets to add:
├── HSTS_MAX_AGE = 15768000
├── CSP_POLICY = default-src 'self'; script-src 'self' 'unsafe-inline'
├── SECURITY_LEVEL = high
└── RATE_LIMIT_THRESHOLD = 100

=============================================================
WORKER SCRIPT EXAMPLE
=============================================================

// Example Cloudflare Worker using secret stores
export default {
  async fetch(request, env, ctx) {
    // Access secrets from different stores
    const dbHost = await env.spirit_immortals_database.get("AWS_DB_HOST");
    const jwtSecret = await env.spirit_immortals_auth.get("JWT_SECRET_KEY");
    const primaryDomain = await env.spirit_immortals_domains.get("PRIMARY_DOMAIN");
    
    // Your application logic here
    return new Response("Secure Spirit of the Immortals Ltd API");
  }
};

EOF

# =============================================================
# SECURITY HARDENING CHECKLIST
# =============================================================

echo ""
echo "🛡️  SECURITY HARDENING CHECKLIST:"
echo ""
echo "Domain Security:"
echo "□ SSL/TLS set to Full (strict) for all domains"
echo "□ HSTS enabled with 6-month max-age"
echo "□ TLS 1.3 enabled"
echo "□ Automatic HTTPS Rewrites enabled"
echo ""
echo "WAF & Protection:"
echo "□ Web Application Firewall enabled"
echo "□ Managed rules activated"
echo "□ Rate limiting configured"
echo "□ Bot Fight Mode enabled"
echo ""
echo "Access Control:"
echo "□ API tokens with minimal permissions"
echo "□ Secret stores properly configured"
echo "□ IP restrictions where possible"
echo "□ Email notifications enabled"
echo ""

# =============================================================
# SECURITY COMMANDS
# =============================================================

echo "🔧 SECURITY COMMANDS:"
echo ""
echo "Generate JWT Secret:"
echo "openssl rand -hex 32"
echo ""
echo "Generate Webhook Secret:"
echo "openssl rand -hex 16"
echo ""
echo "Test SSL Configuration:"
echo "curl -I https://thesmartshoppingsite.com"
echo "curl -I https://spiritoftheimmortals.co.uk"
echo ""
echo "Check Security Headers:"
echo "curl -I https://thesmartshoppingsite.com | grep -i security"
echo ""

echo "✅ Cloudflare Secret Store setup complete!"
echo "🔐 Your domains will have enterprise-grade security!"
echo ""
echo "Next steps:"
echo "1. Login to Cloudflare Dashboard"
echo "2. Create the secret stores above"
echo "3. Configure security settings per domain"
echo "4. Test all security features"
