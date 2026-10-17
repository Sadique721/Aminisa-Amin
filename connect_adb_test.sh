#!/data/data/com.termux/files/usr/bin/sh
export HOME=/data/data/com.termux/files/home
export PREFIX=/data/data/com.termux/files/usr
export PATH=/data/data/com.termux/files/usr/bin:$PATH
export LD_PRELOAD=/data/data/com.termux/files/usr/lib/libtermux-exec.so
export TMPDIR=/data/data/com.termux/files/usr/tmp

echo "=== AMINSA LOCAL ADB TEST WITH TMPDIR ==="
mkdir -p $TMPDIR
adb kill-server
adb connect 127.0.0.1:5555
sleep 2
adb devices
adb -s 127.0.0.1:5555 shell getprop ro.product.model
