#!/bin/bash
# Smart Shopping Platform - Professional Email Setup
# Copyright (c) 2025 Spirit of the Immortals Ltd
# Company Registration: 13434726 (England & Wales)

echo "📧 Setting up professional email for all domains..."

# =============================================================
# CLOUDFLARE EMAIL ROUTING SETUP (FREE)
# =============================================================

echo "🔧 Cloudflare Email Routing Configuration:"
echo ""

# Domain 1: spiritoftheimmortals.co.uk (Primary Company Email)
echo "Domain: spiritoftheimmortals.co.uk"
echo "  derek@spiritoftheimmortals.co.uk → derek.j.king@live.com"
echo "  info@spiritoftheimmortals.co.uk → derek.j.king@live.com"
echo "  support@spiritoftheimmortals.co.uk → derek.j.king@live.com"
echo "  admin@spiritoftheimmortals.co.uk → derek.j.king@live.com"
echo ""

# Domain 2: spiritoftheimmortalsltd.co.uk
echo "Domain: spiritoftheimmortalsltd.co.uk"
echo "  derek@spiritoftheimmortalsltd.co.uk → derek.j.king@live.com"
echo "  info@spiritoftheimmortalsltd.co.uk → derek.j.king@live.com"
echo "  support@spiritoftheimmortalsltd.co.uk → derek.j.king@live.com"
echo ""

# Domain 3: thesmartshoppingsite.com
echo "Domain: thesmartshoppingsite.com"
echo "  support@thesmartshoppingsite.com → derek.j.king@live.com"
echo "  hello@thesmartshoppingsite.com → derek.j.king@live.com"
echo "  team@thesmartshoppingsite.com → derek.j.king@live.com"
echo ""

# Domain 4: thesmartshoppingsite.co.uk
echo "Domain: thesmartshoppingsite.co.uk"
echo "  support@thesmartshoppingsite.co.uk → derek.j.king@live.com"
echo "  hello@thesmartshoppingsite.co.uk → derek.j.king@live.com"
echo ""

# =============================================================
# CLOUDFLARE SETUP INSTRUCTIONS
# =============================================================

echo "🚀 SETUP INSTRUCTIONS:"
echo ""
echo "1. Login to Cloudflare Dashboard"
echo "2. For each domain, go to Email → Email Routing"
echo "3. Enable Email Routing"
echo "4. Add the routing rules above"
echo "5. Verify your destination email: derek.j.king@live.com"
echo ""

# =============================================================
# DNS RECORDS NEEDED (Auto-added by Cloudflare)
# =============================================================

echo "📝 DNS Records (Cloudflare adds these automatically):"
echo ""
echo "MX Records:"
echo "  spiritoftheimmortals.co.uk     MX  10  isaac.mx.cloudflare.net"
echo "  spiritoftheimmortals.co.uk     MX  20  linda.mx.cloudflare.net"
echo "  spiritoftheimmortals.co.uk     MX  30  amir.mx.cloudflare.net"
echo ""
echo "TXT Records:"
echo "  spiritoftheimmortals.co.uk     TXT 'v=spf1 include:_spf.mx.cloudflare.net ~all'"
echo ""

# =============================================================
# GOOGLE WORKSPACE ALTERNATIVE (PAID)
# =============================================================

echo "💼 GOOGLE WORKSPACE ALTERNATIVE:"
echo ""
echo "For professional email with full features:"
echo "1. Sign up for Google Workspace (£4.14/user/month)"
echo "2. Verify domain ownership"
echo "3. Add MX records:"
echo "   Priority 1:  ASPMX.L.GOOGLE.COM"
echo "   Priority 5:  ALT1.ASPMX.L.GOOGLE.COM"
echo "   Priority 5:  ALT2.ASPMX.L.GOOGLE.COM"
echo "   Priority 10: ALT3.ASPMX.L.GOOGLE.COM"
echo "   Priority 10: ALT4.ASPMX.L.GOOGLE.COM"
echo ""

# =============================================================
# EMAIL SIGNATURES
# =============================================================

cat > /tmp/email_signature_derek.html << 'EOF'
<div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
<strong>Derek King</strong><br>
<em>Director</em><br>
<strong>Spirit of the Immortals Ltd</strong><br>
Company Registration: 13434726 (England & Wales)<br>
<br>
📧 derek@spiritoftheimmortals.co.uk<br>
🌐 <a href="https://spiritoftheimmortals.co.uk">spiritoftheimmortals.co.uk</a><br>
🛒 <a href="https://thesmartshoppingsite.com">Smart Shopping Platform</a><br>
<br>
<small style="color: #666;">
This email contains confidential and proprietary information.<br>
If you received this in error, please delete and notify the sender.
</small>
</div>
EOF

echo "📬 Professional email signature created: /tmp/email_signature_derek.html"
echo ""

# =============================================================
# BUSINESS EMAIL BEST PRACTICES
# =============================================================

echo "✅ BUSINESS EMAIL BEST PRACTICES:"
echo ""
echo "1. Use derek@spiritoftheimmortals.co.uk for official business"
echo "2. Use info@spiritoftheimmortals.co.uk for general inquiries"
echo "3. Use support@thesmartshoppingsite.com for platform support"
echo "4. Set up email forwarding to your main account"
echo "5. Create professional email signatures"
echo "6. Enable SPF, DKIM, and DMARC for security"
echo ""

echo "🎯 NEXT STEPS:"
echo "1. Set up Cloudflare Email Routing for all domains"
echo "2. Test each email address"
echo "3. Update your business cards and website"
echo "4. Configure email client with new signatures"
echo ""

echo "✅ Professional email setup complete!"
echo "📧 Primary business email: derek@spiritoftheimmortals.co.uk"
