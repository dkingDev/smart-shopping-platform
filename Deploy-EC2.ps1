# Smart Shopping Platform - Windows PowerShell Deployment Script
# Copyright (c) 2025 Spirit of the Immortals Ltd

param(
    [string]$KeyPath = "",
    [string]$EC2Host = "ubuntu@51.21.152.177"
)

Write-Host "🚀 DEPLOYING SMART SHOPPING PLATFORM TO AWS EC2" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan

# Check if we have the necessary tools
if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
    Write-Host "❌ SSH not found. Please install OpenSSH or use WSL." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command scp -ErrorAction SilentlyContinue)) {
    Write-Host "❌ SCP not found. Please install OpenSSH or use WSL." -ForegroundColor Red
    exit 1
}

# Prompt for SSH key if not provided
if ([string]::IsNullOrEmpty($KeyPath)) {
    $KeyPath = Read-Host "Enter path to your EC2 SSH key file (e.g., C:\Users\derek\.ssh\my-key.pem)"
}

# Validate key file exists
if (-not (Test-Path $KeyPath)) {
    Write-Host "❌ SSH key file not found: $KeyPath" -ForegroundColor Red
    exit 1
}

Write-Host "📦 Step 1: Creating deployment package..." -ForegroundColor Yellow

# Create temporary directory for deployment
$TempDir = "$env:TEMP\smart-shopping-deploy"
if (Test-Path $TempDir) {
    Remove-Item $TempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

# Copy essential files
$FilesToCopy = @(
    "secure_aws_shopping.py",
    "requirements.txt",
    ".env.production",
    "deploy_to_ec2_production.sh",
    "frontend",
    "database",
    "config"
)

foreach ($File in $FilesToCopy) {
    if (Test-Path $File) {
        Write-Host "  Copying $File..." -ForegroundColor Gray
        Copy-Item $File -Destination $TempDir -Recurse -Force
    }
}

Write-Host "📤 Step 2: Uploading to EC2..." -ForegroundColor Yellow

# Create remote directory
Write-Host "  Creating remote directory..." -ForegroundColor Gray
ssh -i $KeyPath $EC2Host "mkdir -p /home/ubuntu/smart-shopping-platform"

# Upload files
Write-Host "  Uploading application files..." -ForegroundColor Gray
scp -i $KeyPath -r "$TempDir/*" "${EC2Host}:/home/ubuntu/smart-shopping-platform/"

# Set permissions
Write-Host "  Setting permissions..." -ForegroundColor Gray
ssh -i $KeyPath $EC2Host "chmod +x /home/ubuntu/smart-shopping-platform/*.sh"

Write-Host "🚀 Step 3: Running deployment on EC2..." -ForegroundColor Yellow

# Run deployment script
ssh -i $KeyPath $EC2Host "cd /home/ubuntu/smart-shopping-platform && bash deploy_to_ec2_production.sh"

Write-Host "🔍 Step 4: Testing deployment..." -ForegroundColor Yellow

# Test the deployment
$TestResult = ssh -i $KeyPath $EC2Host "curl -s -o /dev/null -w '%{http_code}' http://localhost/health"

if ($TestResult -eq "200") {
    Write-Host "✅ Deployment successful! Server is responding." -ForegroundColor Green
} else {
    Write-Host "⚠️  Server deployed but may need configuration. HTTP code: $TestResult" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "Your Smart Shopping Platform is now running on EC2!" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Next steps:" -ForegroundColor Yellow
Write-Host "1. Add DNS records in Cloudflare (see config/cloudflare-dns-records.txt)"
Write-Host "2. Update .env with real database credentials"
Write-Host "3. Test your domains:"
Write-Host "   • https://thesmartshoppingsite.com"
Write-Host "   • https://spiritoftheimmortalsltd.co.uk"
Write-Host ""
Write-Host "🔧 Management commands:" -ForegroundColor Yellow
Write-Host "ssh -i $KeyPath $EC2Host"
Write-Host "sudo systemctl status smart-shopping"
Write-Host "sudo journalctl -u smart-shopping -f"

# Cleanup
Remove-Item $TempDir -Recurse -Force

Write-Host ""
Write-Host "✨ Happy selling! Your e-commerce platform is live! ✨" -ForegroundColor Magenta
