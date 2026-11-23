# REPORT 3 — OPPO A78 5G & TERMUX AUDIT
**Timestamp:** 2026-11-23 14:05:00 IST
**Target Device:** OPPO A78 5G (`CPH2495` / `OP52F3L1`)

---

## 1. HARDWARE SPECIFICATIONS
- **SoC:** MediaTek Dimensity 700 (`mt6833`, 7nm)
- **CPU:** Octa-core (2x Cortex-A76 @ 2.2 GHz + 6x Cortex-A55 @ 2.0 GHz)
- **GPU:** ARM Mali-G57 MC2 (No dedicated NPU/APU)
- **RAM:** 7,823,300 kB (~7.8 GB total, ~2.2 GB free)
- **Storage:** 107 GB total on `/data`, 39 GB available (64% used)
- **Battery:** 70-71% (Status: Charging)

---

## 2. ANDROID 15 & TERMUX ENVIRONMENT
- **OS:** Android 15 (SDK 35, ColorOS 15)
- **Packages:** `com.termux`, `com.termux.boot`, `com.termux.api` (All INSTALLED).
- **Python Version in Termux:** `Python 3.14.6` at `/data/data/com.termux/files/usr/bin/python`.
- **Termux Daemon:** `PID 17331` (`python aminsa_web_daemon.py`), running since 11:18 AM IST.
- **Battery Whitelist:** Verified in `dumpsys deviceidle` (Termux whitelisted).
- **Wake-Lock:** `PARTIAL_WAKE_LOCK 'termux:service-wakelock'` active for > 1h33m.
