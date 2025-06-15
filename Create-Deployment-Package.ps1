# Direct FastAPI Deployment - Manual Method
# Spirit of the Immortals Ltd

Write-Host "🚀 FASTAPI DEPLOYMENT - MANUAL METHOD" -ForegroundColor Cyan
Write-Host "Smart Shopping Platform Production Setup" -ForegroundColor White
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host "📦 Creating deployment package..." -ForegroundColor Yellow

# Create deployment directory
$DeployDir = ".\deployment-package"
if (Test-Path $DeployDir) {
    Remove-Item $DeployDir -Recurse -Force
}
New-Item -ItemType Directory -Path $DeployDir -Force | Out-Null

# Copy essential files
$FilesToDeploy = @(
    "secure_aws_shopping.py",
    "requirements.txt",
    ".env.production", 
    "deploy_to_ec2_production.sh",
    "frontend",
    "database",
    "config"
)

Write-Host "Copying files to deployment package..." -ForegroundColor Gray
foreach ($File in $FilesToDeploy) {
    if (Test-Path $File) {
        Write-Host "  ✅ $File" -ForegroundColor Green
        Copy-Item $File -Destination $DeployDir -Recurse -Force
    } else {
        Write-Host "  ⚠️ $File (not found)" -ForegroundColor Yellow
    }
}

# Create simple startup script
$StartupScript = @"
#!/bin/bash
# FastAPI Startup Script
echo "🚀 Starting Smart Shopping Platform FastAPI"
cd /home/ubuntu/smart-shopping-platform
source venv/bin/activate
python3 secure_aws_shopping.py
"@

$StartupScript | Out-File -FilePath "$DeployDir\start-fastapi.sh" -Encoding UTF8

# Create installation script  
$InstallScript = @"
#!/bin/bash
# Installation Script
echo "📦 Installing Smart Shopping Platform"
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv
cd /home/ubuntu/smart-shopping-platform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x *.sh
echo "✅ Installation complete!"
"@

$InstallScript | Out-File -FilePath "$DeployDir\install.sh" -Encoding UTF8

Write-Host ""
Write-Host "✅ DEPLOYMENT PACKAGE CREATED!" -ForegroundColor Green
Write-Host "📁 Location: $DeployDir" -ForegroundColor White
Write-Host ""
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Upload the 'deployment-package' folder to your EC2 instance" -ForegroundColor White
Write-Host "2. SSH into your EC2 instance" -ForegroundColor White  
Write-Host "3. Run: bash install.sh" -ForegroundColor White
Write-Host "4. Run: bash start-fastapi.sh" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Your domains will be live once FastAPI is running!" -ForegroundColor Cyan
Write-Host "• https://thesmartshoppingsite.com" -ForegroundColor White
Write-Host "• https://spiritoftheimmortalsltd.co.uk" -ForegroundColor White
