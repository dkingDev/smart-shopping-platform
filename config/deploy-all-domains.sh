#!/bin/bash
# Smart Shopping Platform - Multi-Domain Deployment Setup
# Copyright (c) 2025 Spirit of the Immortals Ltd
# Company Registration: 13434726 (England & Wales)

echo "🚀 Setting up multi-domain deployment for Smart Shopping Platform..."
echo "=" * 70

# =============================================================
# STEP 1: CLOUDFLARE DOMAIN SETUP
# =============================================================

echo "🌐 STEP 1: CLOUDFLARE DOMAIN SETUP"
echo ""
echo "1. Login to Cloudflare Dashboard: https://dash.cloudflare.com"
echo "2. Add each domain separately:"
echo "   - thesmartshoppingsite.com"
echo "   - thesmartshoppingsite.co.uk"
echo "   - spiritoftheimmortalsltd.co.uk"
echo "   - spiritoftheimmortals.co.uk"
echo ""
echo "3. Copy DNS records from: config/cloudflare-dns-records.txt"
echo "4. Replace YOUR_SERVER_IP with your actual server IP"
echo ""

# =============================================================
# STEP 2: SSL CERTIFICATE SETUP
# =============================================================

echo "🔒 STEP 2: SSL CERTIFICATE SETUP"
echo ""
echo "Cloudflare SSL (Recommended):"
echo "1. Set SSL/TLS mode to 'Full (strict)' for each domain"
echo "2. Enable 'Always Use HTTPS'"
echo "3. Enable 'HSTS'"
echo "4. Enable 'Automatic HTTPS Rewrites'"
echo ""
echo "Let's Encrypt Alternative:"
echo "1. Install certbot with cloudflare plugin"
echo "2. Run commands from: config/ssl-certificates.conf"
echo ""

# =============================================================
# STEP 3: EMAIL SETUP
# =============================================================

echo "📧 STEP 3: PROFESSIONAL EMAIL SETUP"
echo ""
echo "Cloudflare Email Routing (Free):"
echo "1. In each domain's dashboard: Email → Email Routing"
echo "2. Enable Email Routing"
echo "3. Add forwarding rules:"
echo "   derek@spiritoftheimmortals.co.uk → derek.j.king@live.com"
echo "   info@spiritoftheimmortals.co.uk → derek.j.king@live.com"
echo "   support@thesmartshoppingsite.com → derek.j.king@live.com"
echo ""
echo "4. Verify destination email address"
echo ""

# =============================================================
# STEP 4: SERVER DEPLOYMENT
# =============================================================

echo "🖥️  STEP 4: SERVER DEPLOYMENT OPTIONS"
echo ""
echo "Option A: AWS EC2"
echo "1. Launch EC2 instance"
echo "2. Update YOUR_SERVER_IP in DNS records"
echo "3. Run: bash deploy_to_ec2.sh"
echo ""
echo "Option B: Heroku"
echo "1. Create Heroku app"
echo "2. Set custom domains:"
echo "   heroku domains:add thesmartshoppingsite.com"
echo "   heroku domains:add thesmartshoppingsite.co.uk"
echo "   heroku domains:add spiritoftheimmortalsltd.co.uk"
echo "   heroku domains:add spiritoftheimmortals.co.uk"
echo "3. Update DNS CNAME records to point to Heroku"
echo ""
echo "Option C: Railway"
echo "1. Deploy to Railway"
echo "2. Add custom domains in Railway dashboard"
echo "3. Update DNS records"
echo ""

# =============================================================
# STEP 5: UPDATE APPLICATION CONFIGURATION
# =============================================================

echo "⚙️  STEP 5: APPLICATION CONFIGURATION"
echo ""
echo "Backend (secure_aws_shopping.py):"
echo "1. Update CORS origins to include all domains"
echo "2. Add domain-specific routing if needed"
echo ""
echo "Frontend (app.js & app.production.js):"
echo "✅ Already updated with domain-specific API URLs"
echo ""

# =============================================================
# STEP 6: COMPANY WEBSITE DEPLOYMENT
# =============================================================

echo "🏢 STEP 6: COMPANY WEBSITE DEPLOYMENT"
echo ""
echo "Deploy company website from: company-website/index.html"
echo ""
echo "Options:"
echo "1. GitHub Pages (separate repository)"
echo "2. Netlify"
echo "3. Same server as main application"
echo "4. Cloudflare Pages"
echo ""

# =============================================================
# STEP 7: TESTING
# =============================================================

echo "🧪 STEP 7: TESTING CHECKLIST"
echo ""
echo "Test each domain:"
echo "□ https://thesmartshoppingsite.com"
echo "□ https://thesmartshoppingsite.co.uk"  
echo "□ https://spiritoftheimmortalsltd.co.uk"
echo "□ https://spiritoftheimmortals.co.uk"
echo ""
echo "Test redirects:"
echo "□ www redirects work"
echo "□ HTTP to HTTPS redirects work"
echo "□ Email forwarding works"
echo ""
echo "Test SSL:"
echo "□ SSL certificates valid"
echo "□ SSL Labs grade A+"
echo "□ HSTS working"
echo ""

# =============================================================
# STEP 8: MONITORING & MAINTENANCE
# =============================================================

echo "📊 STEP 8: MONITORING & MAINTENANCE"
echo ""
echo "Set up monitoring for:"
echo "1. Domain expiration dates"
echo "2. SSL certificate expiration"
echo "3. Server uptime"
echo "4. Email delivery"
echo ""
echo "Regular tasks:"
echo "1. Monitor domain renewal (annual)"
echo "2. Update DNS records if server IP changes"
echo "3. Review security settings quarterly"
echo ""

# =============================================================
# SUMMARY
# =============================================================

echo "✅ DEPLOYMENT SUMMARY"
echo ""
echo "Domains configured:"
echo "🛒 thesmartshoppingsite.com (Primary platform)"
echo "🇬🇧 thesmartshoppingsite.co.uk (UK platform)"
echo "🏢 spiritoftheimmortalsltd.co.uk (Company global)"
echo "🇬🇧 spiritoftheimmortals.co.uk (Company UK)"
echo ""
echo "Professional emails:"
echo "📧 derek@spiritoftheimmortals.co.uk"
echo "📧 info@spiritoftheimmortals.co.uk"
echo "📧 support@thesmartshoppingsite.com"
echo ""
echo "Next steps:"
echo "1. Complete Cloudflare setup"
echo "2. Deploy to your chosen hosting platform"
echo "3. Test all domains and functionality"
echo "4. Update business cards and marketing materials"
echo ""
echo "🎉 Spirit of the Immortals Ltd is ready for business!"
