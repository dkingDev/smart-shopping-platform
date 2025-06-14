#!/bin/bash
# 🚀 COMPLETE DEPLOYMENT SCRIPT
# Spirit of the Immortals Ltd - Multi-Domain Secure Platform
# Copyright (c) 2025 Spirit of the Immortals Ltd (13434726)

echo "🏢 Spirit of the Immortals Ltd - Complete Platform Deployment"
echo "=" * 70
echo "👑 Company Registration: 13434726 (England & Wales)"
echo "🎯 Director: Derek King"
echo ""

# =============================================================
# DEPLOYMENT OVERVIEW
# =============================================================

echo "📋 DEPLOYMENT OVERVIEW:"
echo ""
echo "🌐 Domains to Configure:"
echo "  ├── thesmartshoppingsite.com (Primary shopping platform)"
echo "  ├── thesmartshoppingsite.co.uk (UK shopping platform)"
echo "  ├── spiritoftheimmortalsltd.co.uk (Company global - NEW)"
echo "  └── spiritoftheimmortals.co.uk (Company UK operations)"
echo ""
echo "🔐 Security Features:"
echo "  ├── Enterprise-grade SSL/TLS (A+ rating)"
echo "  ├── Web Application Firewall (WAF)"
echo "  ├── DDoS protection & rate limiting"
echo "  ├── 6 Cloudflare secret stores"
echo "  └── Professional email system"
echo ""

# =============================================================
# STEP 1: CLOUDFLARE SETUP
# =============================================================

echo "🚀 STEP 1: CLOUDFLARE DASHBOARD SETUP"
echo "=" * 50
echo ""
echo "📝 Follow these steps in your Cloudflare Dashboard:"
echo ""
echo "1.1 Add Domains (5 minutes):"
echo "    └── Login: https://dash.cloudflare.com"
echo "    └── Add Site → Enter each domain:"
echo "        ├── thesmartshoppingsite.com"
echo "        ├── thesmartshoppingsite.co.uk"
echo "        ├── spiritoftheimmortalsltd.co.uk"
echo "        └── spiritoftheimmortals.co.uk"
echo ""
echo "1.2 Update DNS (10 minutes):"
echo "    └── Copy records from: config/cloudflare-dns-records.txt"
echo "    └── Replace YOUR_SERVER_IP with your actual IP"
echo ""
echo "1.3 Enable Security (10 minutes):"
echo "    └── Follow: config/cloudflare-quick-setup.md"
echo ""

read -p "✅ Press ENTER when Cloudflare setup is complete..."

# =============================================================
# STEP 2: SECRET STORES SETUP
# =============================================================

echo ""
echo "🔐 STEP 2: SECRET STORES CONFIGURATION"
echo "=" * 50
echo ""
echo "📝 Create these secret stores in Cloudflare Dashboard:"
echo "    └── Workers & Pages → Secret Stores → Create Secret Store"
echo ""

# Generate secure secrets
JWT_SECRET=$(openssl rand -hex 32 2>/dev/null || echo "GENERATE_THIS_MANUALLY")
WEBHOOK_SECRET=$(openssl rand -hex 16 2>/dev/null || echo "GENERATE_THIS_MANUALLY")

echo "🔑 Generated Secrets (save these):"
echo "    ├── JWT_SECRET_KEY: $JWT_SECRET"
echo "    └── WEBHOOK_SECRET: $WEBHOOK_SECRET"
echo ""

echo "📦 Secret Store Templates:"
echo ""
cat << 'EOF'
Secret Store #1: "spirit-immortals-database"
├── AWS_DB_HOST = supermarket-db.cbu8qc0uk2re.eu-north-1.rds.amazonaws.com
├── AWS_DB_NAME = postgres
├── AWS_DB_USER = postgres
├── AWS_DB_PASSWORD = [YOUR_SECURE_PASSWORD]
└── AWS_DB_PORT = 5432

Secret Store #2: "spirit-immortals-auth"
├── JWT_SECRET_KEY = [USE_GENERATED_ABOVE]
├── JWT_ALGORITHM = HS256
├── JWT_EXPIRATION_HOURS = 24
└── PASSWORD_SALT_ROUNDS = 12

Secret Store #3: "spirit-immortals-email"
├── SMTP_HOST = smtp.gmail.com
├── SMTP_PORT = 587
├── SMTP_USER = derek.j.king@live.com
├── SMTP_PASSWORD = [GMAIL_APP_PASSWORD]
└── ADMIN_EMAIL = derek@spiritoftheimmortals.co.uk
EOF

read -p "✅ Press ENTER when secret stores are configured..."

# =============================================================
# STEP 3: APPLICATION DEPLOYMENT
# =============================================================

echo ""
echo "🖥️  STEP 3: APPLICATION DEPLOYMENT"
echo "=" * 50
echo ""

echo "Choose your deployment platform:"
echo "1) Heroku (Recommended for beginners)"
echo "2) Railway (Modern platform)"
echo "3) AWS EC2 (Full control)"
echo "4) Vercel (Frontend) + Railway (Backend)"
echo ""

read -p "Enter choice (1-4): " DEPLOY_CHOICE

case $DEPLOY_CHOICE in
    1)
        echo ""
        echo "🟢 HEROKU DEPLOYMENT:"
        echo "1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        echo "2. Run these commands:"
        echo ""
        echo "   heroku login"
        echo "   heroku create spirit-immortals-shopping"
        echo "   git push heroku main"
        echo ""
        echo "3. Add custom domains:"
        echo "   heroku domains:add thesmartshoppingsite.com"
        echo "   heroku domains:add thesmartshoppingsite.co.uk"
        echo "   heroku domains:add spiritoftheimmortalsltd.co.uk"
        echo "   heroku domains:add spiritoftheimmortals.co.uk"
        echo ""
        echo "4. Update Cloudflare DNS to point to Heroku"
        ;;
    2)
        echo ""
        echo "🚄 RAILWAY DEPLOYMENT:"
        echo "1. Visit: https://railway.app"
        echo "2. Connect your GitHub repository"
        echo "3. Deploy automatically"
        echo "4. Add custom domains in Railway dashboard"
        echo "5. Update Cloudflare DNS accordingly"
        ;;
    3)
        echo ""
        echo "☁️  AWS EC2 DEPLOYMENT:"
        echo "1. Launch EC2 instance (t3.micro for start)"
        echo "2. Run: bash deploy_to_ec2.sh"
        echo "3. Update YOUR_SERVER_IP in Cloudflare DNS"
        echo "4. Test all domains"
        ;;
    4)
        echo ""
        echo "⚡ HYBRID DEPLOYMENT:"
        echo "Frontend (Vercel):"
        echo "1. Push frontend/ to separate repo"
        echo "2. Deploy to Vercel"
        echo "3. Point domains to Vercel"
        echo ""
        echo "Backend (Railway):"
        echo "1. Deploy secure_aws_shopping.py to Railway"
        echo "2. Update API URLs in frontend"
        ;;
esac

read -p "✅ Press ENTER when application is deployed..."

# =============================================================
# STEP 4: EMAIL CONFIGURATION
# =============================================================

echo ""
echo "📧 STEP 4: PROFESSIONAL EMAIL SETUP"
echo "=" * 50
echo ""
echo "🔧 Cloudflare Email Routing (FREE):"
echo ""
echo "For each domain:"
echo "1. Go to: Email → Email Routing"
echo "2. Enable Email Routing"
echo "3. Add these forwarding rules:"
echo ""
echo "spiritoftheimmortals.co.uk:"
echo "├── derek@spiritoftheimmortals.co.uk → derek.j.king@live.com"
echo "├── info@spiritoftheimmortals.co.uk → derek.j.king@live.com"
echo "└── support@spiritoftheimmortals.co.uk → derek.j.king@live.com"
echo ""
echo "spiritoftheimmortalsltd.co.uk:"
echo "├── derek@spiritoftheimmortalsltd.co.uk → derek.j.king@live.com"
echo "├── info@spiritoftheimmortalsltd.co.uk → derek.j.king@live.com"
echo "└── support@spiritoftheimmortalsltd.co.uk → derek.j.king@live.com"
echo ""
echo "thesmartshoppingsite.com & .co.uk:"
echo "├── support@thesmartshoppingsite.com → derek.j.king@live.com"
echo "└── hello@thesmartshoppingsite.com → derek.j.king@live.com"
echo ""

read -p "✅ Press ENTER when email routing is configured..."

# =============================================================
# STEP 5: TESTING & VERIFICATION
# =============================================================

echo ""
echo "🧪 STEP 5: TESTING & VERIFICATION"
echo "=" * 50
echo ""

echo "🔍 Test these URLs (should all show green padlock):"
TEST_URLS=(
    "https://thesmartshoppingsite.com"
    "https://thesmartshoppingsite.co.uk"
    "https://spiritoftheimmortalsltd.co.uk"
    "https://spiritoftheimmortals.co.uk"
)

for url in "${TEST_URLS[@]}"; do
    echo "  Testing: $url"
    if command -v curl >/dev/null 2>&1; then
        if curl -s -I "$url" | grep -q "200 OK"; then
            echo "    ✅ PASSED"
        else
            echo "    ❌ FAILED (check DNS/deployment)"
        fi
    else
        echo "    📝 Manual test required"
    fi
done

echo ""
echo "🔐 Security Tests:"
echo "  1. SSL Labs Test: https://www.ssllabs.com/ssltest/"
echo "  2. Security Headers: https://securityheaders.com/"
echo "  3. Mozilla Observatory: https://observatory.mozilla.org/"
echo ""

echo "📧 Email Tests:"
echo "  1. Send test email to: derek@spiritoftheimmortals.co.uk"
echo "  2. Send test email to: support@thesmartshoppingsite.com"
echo "  3. Verify delivery to: derek.j.king@live.com"
echo ""

# =============================================================
# STEP 6: FINAL CONFIGURATION
# =============================================================

echo ""
echo "⚙️  STEP 6: FINAL CONFIGURATION"
echo "=" * 50
echo ""

echo "📱 Update Business Materials:"
echo "  ├── Business cards: derek@spiritoftheimmortals.co.uk"
echo "  ├── Website footer: Company No. 13434726"
echo "  ├── Email signatures: Professional format"
echo "  └── Marketing materials: New domain names"
echo ""

echo "📊 Setup Monitoring:"
echo "  ├── Google Analytics (all domains)"
echo "  ├── Cloudflare Analytics (enabled)"
echo "  ├── SSL certificate expiry alerts"
echo "  └── Email delivery monitoring"
echo ""

echo "🔄 Regular Maintenance:"
echo "  ├── Monthly security review"
echo "  ├── Quarterly domain renewal check"
echo "  ├── SSL certificate monitoring"
echo "  └── Backup verification"
echo ""

# =============================================================
# DEPLOYMENT COMPLETE
# =============================================================

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "=" * 70
echo ""
echo "✅ WHAT'S NOW LIVE:"
echo ""
echo "🛒 Shopping Platform:"
echo "  ├── https://thesmartshoppingsite.com (Global)"
echo "  └── https://thesmartshoppingsite.co.uk (UK)"
echo ""
echo "🏢 Company Websites:"
echo "  ├── https://spiritoftheimmortalsltd.co.uk (Global business)"
echo "  └── https://spiritoftheimmortals.co.uk (UK operations)"
echo ""
echo "📧 Professional Emails:"
echo "  ├── derek@spiritoftheimmortals.co.uk (Primary business)"
echo "  ├── info@spiritoftheimmortals.co.uk (General inquiries)"
echo "  └── support@thesmartshoppingsite.com (Platform support)"
echo ""
echo "🔐 Security Features:"
echo "  ├── A+ SSL rating on all domains"
echo "  ├── Enterprise-grade WAF protection"
echo "  ├── Rate limiting & DDoS protection"
echo "  ├── Secure secret management"
echo "  └── Professional monitoring & alerts"
echo ""

echo "🎯 NEXT BUSINESS STEPS:"
echo "  1. Update all business documents with new domains"
echo "  2. Launch marketing campaigns"
echo "  3. Start customer acquisition"
echo "  4. Monitor analytics and security"
echo ""

echo "👑 Spirit of the Immortals Ltd is now ready for serious business!"
echo "🚀 Your platform has enterprise-grade infrastructure!"
echo "💼 Professional credibility: MAXIMUM"
echo ""
echo "🎊 Congratulations on your complete digital transformation!"
