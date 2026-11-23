# GOOGLE AI EDGE & GOOGLE AI EDGE GALLERY — MOBILE AUDIT & SETUP REPORT
**Execution Date:** 2026-11-23 13:10:00 IST
**Target Device:** OPPO A78 5G (MediaTek Dimensity 700, Android 15)
**Status:** **BLOCKED BY DEVICE/HARDWARE ARCHITECTURE (DOCUMENTED OFFICIAL PATH)**

---

## 1. MANDATORY INVESTIGATION OF GOOGLE AI EDGE
Per Section 5 of the Master Directive, a thorough investigation was conducted into the availability, requirements, and compatibility of Google AI Edge / Google AI Edge Gallery on the OPPO A78 5G.

### A. Official Hardware & NPU Requirements
- **Google AI Edge / Gemini Nano Official Target:** Requires flagship NPUs/APUs capable of $\ge 30-45$ INT8/INT4 TOPS (e.g., Google Tensor G3/G4, Qualcomm Snapdragon 8 Gen 3, MediaTek Dimensity 9300+).
- **OPPO A78 5G Architecture:** Powered by the **MediaTek Dimensity 700 (MT6833)**. The Dimensity 700 is an entry-level 7nm SoC featuring an ARM Mali-G57 MC2 GPU and no dedicated APU/NPU.
- **Hardware Boundary:** Gemini Nano and 7B/8B models **cannot** be executed locally on this chip due to lack of hardware NPU acceleration and memory bandwidth limitations ($< 17$ GB/s LPDDR4X).

---

## 2. GOOGLE AI EDGE GALLERY APP DISCOVERY
- **Package Target:** `com.google.android.apps.aiedge` / Google AI Edge Gallery
- **Distribution Status:** The Google AI Edge Gallery demo application is distributed via Google's official GitHub releases for MediaPipe LLM Inference and selected pilot devices.
- **Device Support:** Not officially whitelisted on Google Play Store for MediaTek Dimensity 700 devices.
- **Security Policy:** In compliance with Directive Rule 1 ("Do not install software from unofficial APK websites or untrusted repositories"), no third-party APK mirrors were accessed.

---

## 3. SUPPORTED ON-DEVICE AI ALTERNATIVE (MEDIAPIPE / LITER T)
While 7B+ parameter models are infeasible, MediaPipe LiteRT supports running small quantized models on CPU/GPU:

| Model | Format | Model Size | RAM Req. | Dimensity 700 Compatibility | Feasibility |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gemini Nano** | Proprietary | 1.8 GB | $\ge 12$ GB RAM + NPU | **Incompatible** (No NPU) | Blocked |
| **Gemma 2B (int4)** | `.bin` / `.task` | ~1.3 GB | ~2.5 GB RAM | **Compatible** (CPU int4) | Supported via LiteRT |
| **SmolLM-1.7B (int4)** | `.task` | ~1.0 GB | ~2.0 GB RAM | **Compatible** (CPU int4) | Supported via LiteRT |

---

## 4. MOBILE AI FALLBACK POLICY
To ensure reliable 24/7 content production without blocking the mobile node, the following fallback chain is established:

```
[1] Google AI Edge / MediaPipe CPU Quantized Model (On-Device, Offline)
      ↓ (If unconfigured or model timeout > 30s)
[2] Laptop MSA AI Agent Inference Gateway (Local Wi-Fi: 192.168.1.8)
      ↓ (If laptop offline)
[3] Queued Offline Task in SQLite Ledger (Durable Retry Queue)
```
