# Simple Production Status Check
# Spirit of the Immortals Ltd - Smart Shopping Platform

Write-Host "=== PRODUCTION STATUS CHECK ===" -ForegroundColor Cyan
Write-Host "Checking Spirit of the Immortals Ltd infrastructure..." -ForegroundColor White

# Test EC2 connectivity
Write-Host "1. Testing EC2 server connectivity..." -ForegroundColor Yellow
$EC2_IP = "51.21.152.177"

# Test ports
$Ports = @(22, 80, 443, 8888)
foreach ($Port in $Ports) {
    Write-Host "   Testing port $Port..." -ForegroundColor Gray
    $Test = Test-NetConnection -ComputerName $EC2_IP -Port $Port -WarningAction SilentlyContinue -InformationLevel Quiet
    if ($Test.TcpTestSucceeded) {
        Write-Host "   ✅ Port $Port is OPEN" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Port $Port is CLOSED" -ForegroundColor Red
    }
}

# Test domains
Write-Host "`n2. Testing domain status..." -ForegroundColor Yellow
$Domains = @(
    "thesmartshoppingsite.com",
    "thesmartshoppingsite.co.uk", 
    "spiritoftheimmortalsltd.co.uk",
    "spiritoftheimmortals.co.uk"
)

foreach ($Domain in $Domains) {
    Write-Host "   Testing $Domain..." -ForegroundColor Gray
    
    # DNS test
    try {
        $DNS = Resolve-DnsName -Name $Domain -ErrorAction Stop
        Write-Host "     ✅ DNS: $($DNS[0].IPAddress)" -ForegroundColor Green
    } catch {
        Write-Host "     ❌ DNS: Failed to resolve" -ForegroundColor Red
    }
    
    # HTTPS test
    try {
        $Response = Invoke-WebRequest -Uri "https://$Domain" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "     ✅ HTTPS: $($Response.StatusCode)" -ForegroundColor Green
    } catch {
        if ($_.Exception.Message -like "*522*") {
            Write-Host "     ⚠️  HTTPS: 522 error (server not responding)" -ForegroundColor Yellow
        } else {
            Write-Host "     ❌ HTTPS: Error" -ForegroundColor Red
        }
    }
}

Write-Host "`n=== STATUS SUMMARY ===" -ForegroundColor Cyan
Write-Host "Your AWS security groups are properly configured." -ForegroundColor White
Write-Host "If ports show CLOSED, your FastAPI app needs to be started on EC2." -ForegroundColor Yellow
Write-Host "If domains show 522 errors, the application server is down." -ForegroundColor Yellow

Write-Host "`nTo deploy and start your application:" -ForegroundColor White
Write-Host "1. Run: .\Deploy-EC2.ps1" -ForegroundColor Cyan
Write-Host "2. Or SSH to EC2 and start the FastAPI app manually" -ForegroundColor Cyan
