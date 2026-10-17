# PowerShell Script: Enable Chrome Remote Debugging Mode (Port 9222)
Write-Host "[*] Closing existing Chrome processes safely..." -ForegroundColor Yellow
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host "[*] Launching Chrome in Developer Debugging Mode (Port 9222)..." -ForegroundColor Cyan
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $chromePath)) {
    $chromePath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
}

Start-Process $chromePath -ArgumentList "--remote-debugging-port=9222", "--restore-last-session"
Start-Sleep -Seconds 3

Write-Host "[+] Chrome launched successfully on port 9222 with session restored!" -ForegroundColor Green
Write-Host "[*] Now running AI Live Controller..." -ForegroundColor Cyan
python "d:\current using file\1 social media automation handler file\chrome_cdp_controller.py"
