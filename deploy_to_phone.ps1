$ErrorActionPreference = "Continue"
$adb = "C:\platform-tools\adb.exe"
$localDir = "d:\current using file\Mine\1 social media automation handler file\mobile_termux_node"
$tmpDest = "/data/local/tmp/aminsa_deploy"
$termuxDest = "/data/data/com.termux/files/home/aminsa_mobile_ecosystem"
$sdcardDest = "/sdcard/DCIM/Aminsa/mobile_termux_node"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🚀 DEPLOYING AMINSA AMIN STANDALONE ECOSYSTEM TO PHONE (TERMUX)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 0. Check Connected Devices
Write-Host "[0/5] Detecting ADB device..." -ForegroundColor Yellow
$devList = & $adb devices
Write-Host ($devList -join "`n")

$hasDevice = ($devList | Where-Object { $_ -match "\bdevice\b" -and $_ -notmatch "List of" })
if (-not $hasDevice) {
    Write-Host "[!] No active ADB device found!" -ForegroundColor Red
    Write-Host "    Please connect phone via USB with USB Debugging ON, or connect via Wi-Fi: adb connect <PHONE_IP>:5555" -ForegroundColor Yellow
    exit 1
}

# 1. Push to /data/local/tmp
Write-Host "[1/5] Pushing files to staging area (/data/local/tmp)..." -ForegroundColor Yellow
& $adb shell "rm -rf $tmpDest && mkdir -p $tmpDest"
& $adb push "$localDir" $tmpDest
& $adb shell "chmod -R 777 $tmpDest"

# 2. Push to /sdcard for backup
Write-Host "[2/5] Backing up to /sdcard/DCIM/Aminsa..." -ForegroundColor Yellow
& $adb shell "mkdir -p '$sdcardDest'"
& $adb push "$localDir" "/sdcard/DCIM/Aminsa/"

# 3. Install into Termux home via run-as
Write-Host "[3/5] Installing into Termux internal home directory..." -ForegroundColor Yellow
$shCmd = @"
mkdir -p $termuxDest
mkdir -p /data/data/com.termux/files/home/.termux/boot
cp -r $tmpDest/mobile_termux_node/* $termuxDest/
cp $termuxDest/aminsa_boot.sh /data/data/com.termux/files/home/.termux/boot/aminsa_boot.sh 2>/dev/null || true
chmod -R 755 $termuxDest
chmod 755 /data/data/com.termux/files/home/.termux/boot/aminsa_boot.sh 2>/dev/null || true
rm -rf $tmpDest
"@
& $adb shell "run-as com.termux sh -c '$shCmd'"

# 4. Configure .bashrc shortcuts
Write-Host "[4/5] Adding Termux shortcuts (aminsa-start, aminsa-status)..." -ForegroundColor Yellow
$aliasCmd = @"
grep -q 'aminsa-start' /data/data/com.termux/files/home/.bashrc 2>/dev/null || (
    echo '' >> /data/data/com.termux/files/home/.bashrc
    echo '# --- Aminsa Amin Standalone Ecosystem Shortcuts ---' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias aminsa-start=\"bash /data/data/com.termux/files/home/aminsa_mobile_ecosystem/start_daemon.sh\"' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias aminsa-stop=\"bash /data/data/com.termux/files/home/aminsa_mobile_ecosystem/stop_daemon.sh\"' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias aminsa-status=\"bash /data/data/com.termux/files/home/aminsa_mobile_ecosystem/status.sh\"' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias aminsa-test=\"python3 /data/data/com.termux/files/home/aminsa_mobile_ecosystem/test_suite.py\"' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias aminsa-log=\"tail -f /sdcard/DCIM/Aminsa/aminsa_daemon.log\"' >> /data/data/com.termux/files/home/.bashrc
)
"@
& $adb shell "run-as com.termux sh -c '$aliasCmd'"

# 5. Ensure ADB TCPIP daemon is alive
Write-Host "[5/5] Re-arming ADB loopback daemon on port 5555..." -ForegroundColor Yellow
& $adb tcpip 5555

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "✅ AMINSA AMIN MOBILE ECOSYSTEM DEPLOYED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
