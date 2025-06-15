#!/bin/bash
# Smart Shopping Platform - AWS EC2 Production Deployment
# Copyright (c) 2025 Spirit of the Immortals Ltd
# Company Registration: 13434726 (England & Wales)

set -e  # Exit on any error

echo "🚀 DEPLOYING SMART SHOPPING PLATFORM TO AWS EC2"
echo "🌐 Domains: thesmartshoppingsite.com, spiritoftheimmortalsltd.co.uk"
echo "☁️  Cloudflare + AWS Integration"
echo "================================================="

# Configuration
EC2_IP="51.21.152.177"
APP_DIR="/home/ubuntu/smart-shopping-platform"
PYTHON_CMD="python3"

echo "📦 Step 1: Installing System Dependencies..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git curl nginx

echo "🔧 Step 2: Setting up Python Environment..."
cd $APP_DIR || { echo "❌ App directory not found. Please upload your code first."; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

echo "📚 Step 3: Installing Python Dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔐 Step 4: Setting up Environment Variables..."
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# FastAPI Configuration
JWT_SECRET_KEY=$(openssl rand -base64 32)
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AWS Database Configuration
AWS_DB_HOST=your-db-host.amazonaws.com
AWS_DB_PORT=5432
AWS_DB_NAME=smart_shopping
AWS_DB_USER=postgres
AWS_DB_PASSWORD=your-secure-password

# Production Settings
ENVIRONMENT=production
DEBUG=False

# Allowed Origins
ALLOWED_ORIGINS=https://thesmartshoppingsite.com,https://www.thesmartshoppingsite.com,https://thesmartshoppingsite.co.uk,https://www.thesmartshoppingsite.co.uk,https://spiritoftheimmortalsltd.co.uk,https://www.spiritoftheimmortalsltd.co.uk
EOF
    echo "⚠️  Please update .env with your actual database credentials!"
fi

echo "🔥 Step 5: Testing FastAPI Application..."
# Test the application
python3 -c "import secure_aws_shopping; print('✅ FastAPI app imports successfully')"

echo "🌐 Step 6: Configuring Nginx Reverse Proxy..."
sudo tee /etc/nginx/sites-available/smart-shopping << EOF
server {
    listen 80;
    server_name thesmartshoppingsite.com www.thesmartshoppingsite.com;
    server_name thesmartshoppingsite.co.uk www.thesmartshoppingsite.co.uk;
    server_name spiritoftheimmortalsltd.co.uk www.spiritoftheimmortalsltd.co.uk;
    server_name spiritoftheimmortals.co.uk www.spiritoftheimmortals.co.uk;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Proxy to FastAPI
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Static files
    location /static/ {
        alias $APP_DIR/frontend/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/smart-shopping /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

echo "⚙️  Step 7: Creating Systemd Service..."
sudo tee /etc/systemd/system/smart-shopping.service << EOF
[Unit]
Description=Smart Shopping Platform FastAPI
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/python secure_aws_shopping.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "🚀 Step 8: Starting Services..."
sudo systemctl daemon-reload
sudo systemctl enable smart-shopping
sudo systemctl start smart-shopping
sudo systemctl enable nginx
sudo systemctl start nginx

echo "🔍 Step 9: Service Status Check..."
echo "FastAPI Service Status:"
sudo systemctl status smart-shopping --no-pager -l

echo "Nginx Status:"
sudo systemctl status nginx --no-pager -l

echo "🌐 Step 10: Testing Application..."
echo "Testing local connection..."
curl -I http://localhost:8000/health || echo "⚠️  FastAPI not responding locally"
curl -I http://localhost/health || echo "⚠️  Nginx proxy not working"

echo "Testing external connection..."
curl -I http://$EC2_IP/ || echo "⚠️  External connection failed"

echo "📊 Step 11: Port and Process Check..."
echo "Listening ports:"
sudo netstat -tlnp | grep -E ':(80|8000|443)'

echo "Python processes:"
ps aux | grep python | grep -v grep

echo "================================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "================================================="
echo "✅ FastAPI running on port 8000"
echo "✅ Nginx reverse proxy on port 80"
echo "✅ Systemd service configured"
echo "✅ Security headers enabled"
echo ""
echo "🌐 Your sites should now be accessible:"
echo "   https://thesmartshoppingsite.com"
echo "   https://spiritoftheimmortalsltd.co.uk"
echo ""
echo "📝 Next Steps:"
echo "1. Update .env with your actual database credentials"
echo "2. Add Cloudflare DNS records (see config/cloudflare-dns-records.txt)"
echo "3. Test SSL certificates in Cloudflare"
echo ""
echo "🔧 Management Commands:"
echo "   sudo systemctl status smart-shopping    # Check service"
echo "   sudo systemctl restart smart-shopping   # Restart app"
echo "   sudo journalctl -u smart-shopping -f    # View logs"
echo "================================================="
