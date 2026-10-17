$ErrorActionPreference = "Stop"
$adb = "C:\platform-tools\adb.exe"
$device = "WS9X6LLJXW7H7TFQ"
$localDir = "d:\current using file\1 social media automation handler file\mobile_termux_node"
$tmpDest = "/data/local/tmp/md_sadique_amin_deploy"
$termuxDest = "/data/data/com.termux/files/home/md_sadique_amin_mobile_ecosystem"
$sdcardDest = "/sdcard/DCIM/Md Sadique Amin/mobile_termux_node"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🚀 DEPLOYING MD_SADIQUE_AMIN STANDALONE ECOSYSTEM TO OPPO A78 5G" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Push to /data/local/tmp
Write-Host "[1/5] Pushing files to staging area (/data/local/tmp)..." -ForegroundColor Yellow
& $adb -s $device shell "rm -rf $tmpDest && mkdir -p $tmpDest"
& $adb -s $device push $localDir $tmpDest
& $adb -s $device shell "chmod -R 777 $tmpDest"

# 2. Push to /sdcard for backup
Write-Host "[2/5] Backing up to /sdcard/DCIM/Md Sadique Amin..." -ForegroundColor Yellow
& $adb -s $device shell "mkdir -p $sdcardDest"
& $adb -s $device push $localDir /sdcard/DCIM/Md Sadique Amin/

# 3. Install into Termux home via run-as
Write-Host "[3/5] Installing into Termux internal home directory..." -ForegroundColor Yellow
$shCmd = @"
mkdir -p $termuxDest
mkdir -p /data/data/com.termux/files/home/.termux/boot
cp -r $tmpDest/mobile_termux_node/* $termuxDest/
cp $termuxDest/md_sadique_amin_boot.sh /data/data/com.termux/files/home/.termux/boot/md_sadique_amin_boot.sh
chmod -R 755 $termuxDest
chmod 755 /data/data/com.termux/files/home/.termux/boot/md_sadique_amin_boot.sh
rm -rf $tmpDest
"@
& $adb -s $device shell "run-as com.termux sh -c '$shCmd'"

# 4. Configure .bashrc shortcuts
Write-Host "[4/5] Adding Termux shortcuts..." -ForegroundColor Yellow
$aliasCmd = @"
grep -q 'md_sadique_amin-start' /data/data/com.termux/files/home/.bashrc 2>/dev/null || (
    echo '' >> /data/data/com.termux/files/home/.bashrc
    echo '# --- Md Sadique Amin Standalone Ecosystem Shortcuts ---' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias md_sadique_amin-start=\"bash /data/data/com.termux/files/home/md_sadique_amin_mobile_ecosystem/start_daemon.sh\"' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias md_sadique_amin-stop=\"bash /data/data/com.termux/files/home/md_sadique_amin_mobile_ecosystem/stop_daemon.sh\"' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias md_sadique_amin-status=\"bash /data/data/com.termux/files/home/md_sadique_amin_mobile_ecosystem/status.sh\"' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias md_sadique_amin-test=\"python3 /data/data/com.termux/files/home/md_sadique_amin_mobile_ecosystem/test_suite.py\"' >> /data/data/com.termux/files/home/.bashrc
    echo 'alias md_sadique_amin-log=\"tail -f /sdcard/DCIM/Md Sadique Amin/md_sadique_amin_daemon.log\"' >> /data/data/com.termux/files/home/.bashrc
)
"@
& $adb -s $device shell "run-as com.termux sh -c '$aliasCmd'"

# 5. Ensure ADB TCPIP daemon is alive
Write-Host "[5/5] Re-arming ADB loopback daemon on port 5555..." -ForegroundColor Yellow
& $adb -s $device tcpip 5555

Write-Host "✅ DEPLOYMENT FINISHED SUCCESSFULLY!" -ForegroundColor Green
