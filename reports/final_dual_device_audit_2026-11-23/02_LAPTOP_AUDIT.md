# REPORT 2 — WINDOWS 11 LAPTOP COORDINATOR AUDIT
**Timestamp:** 2026-11-23 14:05:00 IST
**Host:** Laptop Coordinator (Windows 11)

---

## 1. SYSTEM SPECIFICATIONS
- **OS Edition:** Windows 11 Build 10.0.26300 (AMD64 Family 25 Model 80 AuthenticAMD)
- **CPU:** AMD Ryzen 5000 Series (8 Cores, 16 Threads)
- **RAM:** 16 GB Physical Memory
- **Free Disk Space:** Drive C (99 GB free), Drive D (82 GB free)
- **Python:** 3.14.7 (`C:\Python314\python.exe`)
- **Java:** OpenJDK 21.0.12 LTS
- **Docker:** 29.6.2 (WSL 2 backend integrated)
- **Git:** 2.56.1.windows.1 (Head: `80df711` on `origin/main`)
- **ADB:** Version 1.0.41 at `C:\platform-tools\adb.exe`

---

## 2. RUNTIME ENGINES & PERSISTENCE
- **Scheduler:** `engines/ist_daily_scheduler.py` (08:00 AM cycle start, 2.4h intervals, Asia/Kolkata).
- **Ledger DB:** `data/aminsa_production_ledger.db` (20 tables active, WAL mode).
- **Task Scheduler:** `Aminsa_Master_Orchestrator` daily task registered.
- **Port Forwarding:** `adb forward tcp:8765 tcp:8765` connects laptop browser to mobile Termux daemon.
