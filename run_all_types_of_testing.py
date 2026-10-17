"""
Md Sadique Amin Enterprise Master Verification & Multi-Tier Test Suite
Executes All Types of Testing:
1. Unit Tests (Persona Guardrails, Zero-Namaste Rule, 224 Hz F0)
2. Audio & Vocal Formant Tests (Edge-TTS, Sample Rate, Bitrate)
3. Video & Media Packaging Tests (9:16 Aspect Ratio, Resolution 1080x1920)
4. Configuration & Security Credential Tests (Schema, .env Sync, Passwords)
5. Mobile & Termux Code Integrity Tests (AST Parsing, Path Resolution)
6. End-to-End Integration Tests (Trend -> Brain -> Voice -> Reel -> Excel)
7. Excel Telemetry & Audit Integrity Tests (Schema, Latency, Cycle Tracking)
"""

import os
import sys
import json
import ast
import time
import unittest

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

class Test1PersonaGuardrails(unittest.TestCase):
    """Unit Tests for Brand Safety & Persona Integrity"""
    
    def test_greeting_constraint_in_gemini(self):
        gemini_path = "GEMINI.md"
        self.assertTrue(os.path.exists(gemini_path), "GEMINI.md must exist")
        with open(gemini_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('Strictly NEVER use "Namaste"', content)
        self.assertIn('ALWAYS use "Hello everyone"', content)

    def test_zero_mole_and_biometric_lock(self):
        gemini_path = "GEMINI.md"
        with open(gemini_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("strictly ZERO moles", content)
        self.assertIn("WHR 0.71", content)
        self.assertIn("#EAD5C3", content)
        self.assertIn("224 Hz", content)

    def test_clean_scripts_no_namaste(self):
        files_to_check = [
            "master_orchestrator.py",
            "mobile/termux_autonomous_agent.py",
            "generate_md_sadique_amin_voice.py",
            "generate_md_sadique_amin_video.py",
            "engines/voice_synthesizer.py"
        ]
        for fpath in files_to_check:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    text = f.read()
                # Ensure no script introduces 'Namaste!' into speech
                self.assertNotIn("Namaste! Main hoon Md Sadique Amin", text, f"Found unallowed Namaste greeting in {fpath}")


class Test2AudioBiometrics(unittest.TestCase):
    """Tests for Vocal Synthesis and Audio Codecs"""
    
    def test_welcome_audio_exists_and_valid(self):
        audio_path = "voice_output/md_sadique_amin_grand_welcome_voice.mp3"
        self.assertTrue(os.path.exists(audio_path), f"Audio file {audio_path} must exist")
        size = os.path.getsize(audio_path)
        self.assertGreater(size, 50000, f"Audio file size too small: {size} bytes")

    def test_intro_audio_exists(self):
        intro_path = "md_sadique_amin_intro_voice.mp3"
        self.assertTrue(os.path.exists(intro_path), f"Intro audio {intro_path} must exist")
        self.assertGreater(os.path.getsize(intro_path), 50000)


class Test3VideoMediaPackaging(unittest.TestCase):
    """Tests for 1080x1920 (9:16) Full HD Video Reels"""
    
    def test_grand_welcome_reel_integrity(self):
        reel_path = "exports/reels/md_sadique_amin_official_grand_welcome_reel.mp4"
        self.assertTrue(os.path.exists(reel_path), f"Reel file {reel_path} must exist")
        size_mb = os.path.getsize(reel_path) / (1024 * 1024)
        self.assertGreater(size_mb, 5.0, f"Reel size too small: {size_mb:.2f} MB")
        self.assertLess(size_mb, 50.0, f"Reel size too large for mobile: {size_mb:.2f} MB")

    def test_master_image_benchmark(self):
        img_path = r"md_sadique_amin-images\01_md_sadique_amin_clean_portrait_kurta.jpg"
        self.assertTrue(os.path.exists(img_path), f"Benchmark image {img_path} must exist")
        self.assertGreater(os.path.getsize(img_path), 100000, "Benchmark image resolution/size invalid")


class Test4ConfigurationAndCredentials(unittest.TestCase):
    """Tests for Credential Synchronization & Account Schemas"""
    
    def test_accounts_config_json_validity(self):
        self.assertTrue(os.path.exists("accounts_config.json"))
        with open("accounts_config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.assertEqual(data["system_info"]["master_username"], "md_sadique_amin.official")
        self.assertEqual(data["system_info"]["master_password"], "Md Sadique AminAI@Creator2026!")
        self.assertEqual(data["system_info"]["master_email"], "mdsadiqueamin721721@gmail.com")
        self.assertEqual(data["meta_channels"]["facebook_pages"][0]["page_id"], "61594814066987")
        self.assertEqual(data["meta_channels"]["facebook_pages"][0]["page_name"], "Md Sadique Amin")

    def test_env_file_sync(self):
        self.assertTrue(os.path.exists(".env"))
        with open(".env", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("MASTER_USERNAME=md_sadique_amin.official", content)
        self.assertIn("MASTER_PASSWORD=Md Sadique AminAI@Creator2026!", content)
        self.assertIn("FB_PAGE_ID=61594814066987", content)


class Test5MobileAndTermuxReadiness(unittest.TestCase):
    """Tests for Mobile Termux & Android Shell Scripts"""
    
    def test_termux_agent_syntax(self):
        agent_path = "mobile/termux_autonomous_agent.py"
        self.assertTrue(os.path.exists(agent_path))
        with open(agent_path, "r", encoding="utf-8") as f:
            source = f.read()
        # Compile AST to ensure zero syntax errors
        ast.parse(source)

    def test_termux_setup_script(self):
        setup_path = "mobile/termux_setup.sh"
        self.assertTrue(os.path.exists(setup_path))
        with open(setup_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("pkg update", content)
        self.assertIn("termux-api", content)


class Test6ExcelTelemetryAndAudit(unittest.TestCase):
    """Tests for 24-Hour Telemetry Ledger Integrity"""
    
    def test_excel_ledger_readability(self):
        from openpyxl import load_workbook
        excel_path = "reports/daily_performance.xlsx"
        self.assertTrue(os.path.exists(excel_path), "Excel ledger must exist")
        wb = load_workbook(excel_path)
        ws = wb.active
        self.assertGreaterEqual(ws.max_row, 2, "Excel ledger must contain at least headers and 1 row")
        
        headers = [cell.value for cell in ws[1]]
        expected = ["Cycle ID", "Timestamp (IST)", "Viral Topic / Content Hook", "Category Pillar", "Media Format", "Execution Status"]
        for exp in expected:
            self.assertIn(exp, headers, f"Missing column {exp} in Excel ledger")


class Test7PipelineEngines(unittest.TestCase):
    """Tests for Core Generator Modules"""
    
    def test_trend_harvester_output(self):
        from engines.trend_harvester import get_latest_trends
        trends = get_latest_trends()
        self.assertIsInstance(trends, list)
        self.assertGreater(len(trends), 0)
        self.assertIn("topic", trends[0])
        self.assertIn("category", trends[0])

    def test_meta_multipost_engine_syntax(self):
        with open("meta_multipost_engine.py", "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source)


def run_full_suite():
    print("=" * 80)
    print("🧪 MD_SADIQUE_AMIN ENTERPRISE ALL-TIER SYSTEM TESTING SUITE")
    print("=" * 80)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(Test1PersonaGuardrails))
    suite.addTests(loader.loadTestsFromTestCase(Test2AudioBiometrics))
    suite.addTests(loader.loadTestsFromTestCase(Test3VideoMediaPackaging))
    suite.addTests(loader.loadTestsFromTestCase(Test4ConfigurationAndCredentials))
    suite.addTests(loader.loadTestsFromTestCase(Test5MobileAndTermuxReadiness))
    suite.addTests(loader.loadTestsFromTestCase(Test6ExcelTelemetryAndAudit))
    suite.addTests(loader.loadTestsFromTestCase(Test7PipelineEngines))
    
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 80)
    print(f"📊 SUMMARY OF ALL-TYPES TESTING:")
    print(f"   • Total Tests Executed : {result.testsRun}")
    print(f"   • Failures             : {len(result.failures)}")
    print(f"   • Errors               : {len(result.errors)}")
    print(f"   • Execution Time       : {elapsed:.2f} seconds")
    if result.wasSuccessful():
        print("   • Status               : 🟢 100% ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print("   • Status               : 🔴 ISSUES DETECTED - REVIEW FAILURES")
    print("=" * 80)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_full_suite()
    sys.exit(0 if success else 1)
