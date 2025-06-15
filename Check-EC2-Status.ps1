# EC2 Instance Status Check and Management Guide
# Spirit of the Immortals Ltd - Smart Shopping Platform

Write-Host "🔍 EC2 INSTANCE STATUS CHECK" -ForegroundColor Cyan
Write-Host "Smart Shopping Platform Infrastructure" -ForegroundColor White
Write-Host "=====================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "🚨 POSSIBLE ISSUE: EC2 Instance Stopped" -ForegroundColor Yellow
Write-Host ""
Write-Host "If SSH connection fails, your EC2 instance might be:" -ForegroundColor White
Write-Host "• ❌ Stopped (can be restarted)" -ForegroundColor Red
Write-Host "• ❌ Terminated (needs new instance)" -ForegroundColor Red
Write-Host "• ❌ In different region" -ForegroundColor Red
Write-Host "• ❌ Security group misconfigured" -ForegroundColor Red

Write-Host ""
Write-Host "🔧 HOW TO CHECK EC2 STATUS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Open AWS Console (https://console.aws.amazon.com)" -ForegroundColor White
Write-Host "2. Go to EC2 Dashboard" -ForegroundColor White
Write-Host "3. Click 'Instances' in left menu" -ForegroundColor White
Write-Host "4. Look for your instance with IP: 51.21.152.177" -ForegroundColor White
Write-Host ""
Write-Host "📊 INSTANCE STATES:" -ForegroundColor Yellow
Write-Host "• 🟢 Running - Instance is active (should accept SSH)" -ForegroundColor Green
Write-Host "• 🟡 Stopped - Instance is stopped (needs to be started)" -ForegroundColor Yellow
Write-Host "• 🔴 Terminated - Instance is destroyed (need new one)" -ForegroundColor Red
Write-Host "• 🟡 Pending - Instance is starting up" -ForegroundColor Yellow

Write-Host ""
Write-Host "🚀 HOW TO START A STOPPED INSTANCE:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Select your stopped instance" -ForegroundColor White
Write-Host "2. Click 'Instance State' button" -ForegroundColor White
Write-Host "3. Click 'Start Instance'" -ForegroundColor White
Write-Host "4. Wait 2-3 minutes for it to boot up" -ForegroundColor White
Write-Host "5. Note the new Public IP (might change!)" -ForegroundColor White

Write-Host ""
Write-Host "⚠️  IMPORTANT NOTES:" -ForegroundColor Yellow
Write-Host ""
Write-Host "• If instance was STOPPED:" -ForegroundColor White
Write-Host "  - Your data is preserved" -ForegroundColor Cyan
Write-Host "  - Public IP might change" -ForegroundColor Cyan
Write-Host "  - Need to update DNS records if IP changes" -ForegroundColor Cyan
Write-Host ""
Write-Host "• If instance was TERMINATED:" -ForegroundColor White
Write-Host "  - All data is lost" -ForegroundColor Red
Write-Host "  - Need to create new instance" -ForegroundColor Red
Write-Host "  - Need to redeploy everything" -ForegroundColor Red

Write-Host ""
Write-Host "🌐 AFTER STARTING INSTANCE:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Check the new Public IP address" -ForegroundColor White
Write-Host "2. Update Cloudflare DNS records if IP changed" -ForegroundColor White
Write-Host "3. Test SSH connection again" -ForegroundColor White
Write-Host "4. Deploy FastAPI application" -ForegroundColor White

Write-Host ""
Write-Host "💡 NEXT STEPS:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Check AWS Console for instance status" -ForegroundColor White
Write-Host "2. Start the instance if it's stopped" -ForegroundColor White
Write-Host "3. Get the current Public IP" -ForegroundColor White
Write-Host "4. Come back and we'll deploy FastAPI" -ForegroundColor White

Write-Host ""
Write-Host "🎯 CURRENT EXPECTED IP: 51.21.152.177" -ForegroundColor Cyan
Write-Host "📝 Check if this matches your EC2 instance in AWS Console" -ForegroundColor White
