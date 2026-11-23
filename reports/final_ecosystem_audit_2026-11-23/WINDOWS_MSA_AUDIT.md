# WINDOWS 11 LAPTOP — COMPLETE MSA ENVIRONMENT AUDIT
**Execution Date:** 2026-11-23 13:10:00 IST
**Host Name:** LAPTOP-COORDINATOR
**Role:** Primary Coordinator & Master Avatar Studio

---

## 1. HARDWARE & OPERATING SYSTEM
- **OS Edition:** Windows 11 Home / Pro
- **OS Build:** 10.0.26300 (AMD64 Family 25 Model 80 AuthenticAMD)
- **CPU:** AMD Ryzen 5000 Series (8 Cores, 16 Threads)
- **System Memory:** 16 GB Physical RAM
- **Storage Availability:**
  * Drive C (System): 99 GB free of 279 GB total
  * Drive D (Workspaces): 82 GB free of 195 GB total

---

## 2. SOFTWARE RUNTIMES & TOOLCHAINS
- **Python:** 3.14.7 (`C:\Python314\python.exe`)
- **Java:** OpenJDK 21.0.12 LTS (Build 21.0.12+7-LTS)
- **Git:** 2.56.1.windows.1
- **Docker Desktop:** 29.6.2 (WSL 2 backend integrated)
- **WSL:** Installed & operational
- **ADB (Android Debug Bridge):** Version 1.0.41 (37.0.1-15733141) at `C:\platform-tools\adb.exe`
- **Network Interface:** Wi-Fi active, IPv4 `192.168.1.8`, Subnet `255.255.255.0`, Gateway `192.168.1.1`

---

## 3. AI PROVIDER & INFERENCE RUNTIME INVENTORY

| Provider / Model | Installed | Version | Model Available | Service Running | Inference Test | Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Google Gemini API** | Yes | Official SDK | Gemini 2.5 / Flash | On Demand | Script/Prompt Test | **PASS** |
| **Microsoft Edge TTS** | Yes | 6.1.3 | en-IN / hi-IN Voices | Local Engine | 12s Audio Synthesis | **PASS** |
| **Pillow Imaging** | Yes | 10.x | Image Master Core | Local Engine | 4K PNG Verification | **PASS** |
| **Ollama Local LLM** | No | N/A | None | Stopped | N/A | **NOT INSTALLED** |
| **OpenCV (cv2)** | Yes | 4.10.x | Image Analysis Only | Local Library | Face Check (Rule 5 Compliant) | **PASS** |

---

## 4. PERSISTENCE & SYSTEM SERVICES
- **Task Scheduler Tasks:** `Aminsa_Master_Orchestrator` configured for daily startup.
- **Registry Startup Run:** Verified persistence hook in `Software\Microsoft\Windows\CurrentVersion\Run`.
- **Startup Folder Shortcut:** Shortcut active in `shell:startup`.
