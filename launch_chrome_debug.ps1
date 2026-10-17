$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $chrome)) {
    $chrome = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
}
$debugDir = "C:\Users\MD SADIQUE AMIN\AppData\Local\Google\Chrome\DebugProfile"
if (-not (Test-Path $debugDir)) {
    New-Item -ItemType Directory -Path $debugDir -Force | Out-Null
}

Write-Host "[*] Launching Google Chrome in Developer Debugging Mode..." -ForegroundColor Cyan
Start-Process $chrome -ArgumentList "--remote-debugging-port=9222", "--remote-debugging-address=127.0.0.1", "--user-data-dir=`"$debugDir`"", "--no-first-run", "--no-default-browser-check"
Start-Sleep -Seconds 3

try {
    $client = New-Object System.Net.Sockets.TcpClient('127.0.0.1', 9222)
    Write-Host "[+] SUCCESS: Chrome Developer Debugging Mode is LIVE on Port 9222!" -ForegroundColor Green
    $client.Close()
} catch {
    Write-Host "[-] Note: $($_.Exception.Message)" -ForegroundColor Yellow
}
