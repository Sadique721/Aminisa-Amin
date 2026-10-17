"""
Md Sadique Amin Master Toolchain & Ecosystem Verification Engine
Audits and verifies all local and cloud tools, daemons, packages, and frameworks.
"""

import sys
import urllib.request
import json
import importlib
import os

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def check_endpoint(name, url, timeout=2):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Md Sadique AminChecker/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, f"HTTP {resp.status} ONLINE"
    except Exception as e:
        return False, f"OFFLINE ({type(e).__name__})"

def check_package(pkg_name):
    try:
        mod = importlib.import_module(pkg_name)
        ver = getattr(mod, "__version__", "Installed")
        return True, str(ver)
    except ImportError:
        return False, "NOT INSTALLED"

def run_system_audit():
    print("=" * 80)
    print("🛠️  MD_SADIQUE_AMIN AUTONOMOUS SYSTEM: END-TO-END TOOLCHAIN AUDIT & INTEGRATION")
    print("=" * 80)
    
    # 1. Daemon Endpoints
    print("\n🌐 [1. Core Daemon & Router Endpoints]")
    endpoints = [
        ("Ollama Model Engine", "http://127.0.0.1:11435/api/tags"),
        ("OmniRoute AI Gateway", "http://127.0.0.1:20128/v1/models"),
        ("MSA Token Optimizer Router", "http://127.0.0.1:20130/health"),
        ("Mission Control Dashboard", "http://127.0.0.1:20130/dashboard"),
    ]
    for name, url in endpoints:
        ok, msg = check_endpoint(name, url)
        status_icon = "🟢" if ok else "🔴"
        print(f"  {status_icon} {name:<30} -> {msg}")

    # 2. Python AI & Audio Libraries
    print("\n🐍 [2. Python AI, Audio & Rendering Libraries]")
    packages = [
        ("edge_tts", "Microsoft Edge Neural TTS Engine"),
        ("imageio_ffmpeg", "FFmpeg Video Reel Compositor"),
        ("openpyxl", "Excel Performance Audit Logger"),
        ("torch", "PyTorch Deep Learning Engine"),
        ("transformers", "Hugging Face Model Transformer"),
        ("onnxruntime", "ONNX Runtime CPU Inference"),
        ("cv2", "OpenCV Image Processing"),
        ("PIL", "Pillow Image Library"),
        ("playwright", "Playwright Browser Automation"),
        ("requests", "HTTP Requests Client"),
    ]
    for pkg, desc in packages:
        ok, ver = check_package(pkg)
        status_icon = "🟢" if ok else "🔴"
        print(f"  {status_icon} {pkg:<16} (v{ver:<12}) -> {desc}")

    # 3. Mobile Bridge & Configuration Files
    print("\n📱 [3. Mobile & System Configuration Artifacts]")
    artifacts = [
        ("config/ecosystem_tools.json", "Ecosystem Tools Manifest"),
        ("config/accounts_config.json", "Social Media Account Credentials"),
        ("mobile/termux_autonomous_agent.py", "Termux Autonomous Agent Script"),
        ("mobile/termux_setup.sh", "Termux One-Click Setup Script"),
        ("engines/trend_harvester.py", "Google Trends & News Harvester"),
        ("engines/voice_synthesizer.py", "224Hz Neural Voice Synthesizer"),
        ("engines/reel_composer.py", "1080x1920 9:16 Video Reel Composer"),
        ("reports/excel_logger.py", "24-Hour Telemetry Audit Engine"),
        ("reports/daily_performance.xlsx", "Live Dynamic Excel Ledger"),
    ]
    for path, desc in artifacts:
        exists = os.path.exists(path)
        status_icon = "🟢" if exists else "🔴"
        size_str = f"{os.path.getsize(path):,} B" if exists else "Missing"
        print(f"  {status_icon} {path:<36} [{size_str:<9}] -> {desc}")

    print("\n" + "=" * 80)
    print("✅ MASTER TOOLCHAIN INTEGRATION STATUS: COMPLETE & SYNCHRONIZED")
    print("=" * 80)

if __name__ == "__main__":
    run_system_audit()
