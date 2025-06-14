#!/bin/bash
# Smart Shopping Platform - EC2 Deployment Script
# Spirit of the Immortals Ltd
# Run this script on your EC2 instance

echo "🚀 Starting Smart Shopping Platform Deployment..."
echo "=" * 50

# STEP 1: Update system and install dependencies
echo "📦 Updating system and installing dependencies..."
sudo dnf update -y
sudo dnf install python3 python3-pip git gcc python3-devel postgresql-devel -y

# STEP 2: Clone repository
echo "📁 Cloning Smart Shopping Platform repository..."
cd /home/ec2-user
git clone https://github.com/dkingDev/smart-shopping-platform.git
cd smart-shopping-platform

# STEP 3: Install Python requirements
echo "🐍 Installing Python dependencies..."
pip3 install -r requirements.txt --user

# Add pip local bin to PATH
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# STEP 4: Create environment file template
echo "⚙️  Creating environment configuration..."
cat > .env << 'EOF'
AWS_DB_HOST=supermarket-db.cbu8qc0uk2re.eu-north-1.rds.amazonaws.com
AWS_DB_NAME=postgres
AWS_DB_USER=postgres
AWS_DB_PASSWORD=REPLACE_WITH_YOUR_ACTUAL_PASSWORD
AWS_DB_PORT=5432
JWT_SECRET_KEY=spirits_immortals_shopping_platform_secure_key_2025_derek_king
EOF

echo "🔧 Environment file created. You need to edit .env and add your actual database password."
echo "Run: nano .env"
echo "Replace 'REPLACE_WITH_YOUR_ACTUAL_PASSWORD' with your real password"

# STEP 5: Set up systemd service for auto-start
echo "🔄 Creating systemd service..."
sudo tee /etc/systemd/system/smart-shopping.service > /dev/null << 'EOF'
[Unit]
Description=Smart Shopping Platform
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/smart-shopping-platform
Environment=PATH=/home/ec2-user/.local/bin
ExecStart=/usr/bin/python3 secure_aws_shopping.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
sudo systemctl daemon-reload
sudo systemctl enable smart-shopping.service

echo "✅ Deployment script completed!"
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Edit your password: nano .env"
echo "2. Start the service: sudo systemctl start smart-shopping"
echo "3. Check status: sudo systemctl status smart-shopping"
echo "4. View logs: sudo journalctl -u smart-shopping -f"
echo ""
echo "🌐 Your Smart Shopping Platform will be available at:"
echo "   http://51.21.152.177:8888"
echo ""
echo "🏢 Spirit of the Immortals Ltd - Smart Shopping Platform Ready!"
