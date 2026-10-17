# -*- coding: utf-8 -*-
"""
Phase 3 Dry-Run Validation Suite
Runs one test post per platform (Instagram, Facebook, Threads) in dry-run mode.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from publishers.instagram import instagram_publisher
from publishers.facebook import facebook_publisher
from publishers.threads import threads_publisher

def run_dry_run_tests():
    sample_video_url = "https://media.aminsa.live/reels/aminsa_demo_sample.mp4"
    sample_caption = (
        "Hello everyone! Exploring AI virtual creator tech in 2026. "
        "#AIGenerated #VirtualCreator #Aminsa #TechTrends"
    )

    print("=" * 70)
    print("PHASE 3 OFFICIAL POSTING — DRY-RUN VALIDATION SUITE")
    print("=" * 70)

    # 1. Instagram Test
    ig_res = instagram_publisher.publish_reel(sample_video_url, sample_caption, dry_run=True)
    print(f"[TEST 1/3] Instagram : {'PASS' if ig_res.get('success') else 'FAIL'}")
    print(f"           Result    : {ig_res}")

    # 2. Facebook Test
    fb_res = facebook_publisher.publish_video_reel(sample_video_url, sample_caption, title="AI Innovation 2026", dry_run=True)
    print(f"[TEST 2/3] Facebook  : {'PASS' if fb_res.get('success') else 'FAIL'}")
    print(f"           Result    : {fb_res}")

    # 3. Threads Test
    th_res = threads_publisher.publish_video(sample_video_url, sample_caption, dry_run=True)
    print(f"[TEST 3/3] Threads   : {'PASS' if th_res.get('success') else 'FAIL'}")
    print(f"           Result    : {th_res}")

    print("=" * 70)
    all_pass = all([ig_res.get("success"), fb_res.get("success"), th_res.get("success")])
    if all_pass:
        print("[SUCCESS] All 3 Official API Publishers PASSED dry-run validation!")
    else:
        print("[-] One or more publishers failed.")
    return all_pass

if __name__ == "__main__":
    run_dry_run_tests()
