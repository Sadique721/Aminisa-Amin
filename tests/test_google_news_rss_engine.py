# -*- coding: utf-8 -*-
"""
Unit Tests for Phase 2: Google News RSS Discovery & Fact Verification Engine
"""

import os
import sys
import unittest
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engines.production_ledger_db import ProductionLedgerDB
from engines.google_news_rss_engine import GoogleNewsRSSEngine


SAMPLE_RSS_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Google News</title>
    <item>
      <title>ISRO scheduled to launch NVS-02 navigation satellite on January 29 - The Hindu</title>
      <link>https://news.google.com/rss/articles/CBMiWWh0dHBzOi8vd3d3LnRoZWhpbmR1LmNvbS9zY2llbmNlL3NwYWNlL2lzcm8tc2NoZWR1bGVkLXRvLWxhdW5jaC1udnMtMDIvYXJ0aWNsZTEyMzQ1Njc4LmVjZQ?oc=5</link>
      <guid isPermaLink="false">CBMiWWh0dHBzOi8vd3d3LnRoZWhpbmR1LmNvb</guid>
      <pubDate>Mon, 23 Nov 2026 04:30:00 GMT</pubDate>
    </item>
    <item>
      <title>Finance Ministry proposes new tax incentives for deeptech startups in India - Livemint</title>
      <link>https://news.google.com/rss/articles/CBMiWWh0dHBzOi8vd3d3LmxpdmVtaW50LmNvbS9idXNpbmVzcy9zdGFydHVwcy9maW5hbmNlLW1pbmlzdHJ5LXByb3Bvc2VzLXRheC1pbmNlbnRpdmVzMTIzNDU2?oc=5</link>
      <guid isPermaLink="false">CBMiWWh0dHBzOi8vd3d3LmxpdmVtaW50LmNvb</guid>
      <pubDate>Mon, 23 Nov 2026 05:15:00 GMT</pubDate>
    </item>
    <item>
      <title>Breaking: Massive global cyber outage disrupts international flights - Unverified Source</title>
      <link>https://news.google.com/rss/articles/CBMiWWh0dHBzOi8vdW52ZXJpZmllZC1ibG9nLmNvbS9jeWJlci1vdXRhZ2UxMjM0NTY?oc=5</link>
      <guid isPermaLink="false">CBMiWWh0dHBzOi8vdW52ZXJpZmllZC1ibG9nLmNvb</guid>
      <pubDate>Mon, 23 Nov 2026 05:30:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


class TestGoogleNewsRSSEngine(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_file.close()
        self.db = ProductionLedgerDB(db_path=self.temp_file.name)
        self.engine = GoogleNewsRSSEngine(db=self.db)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except Exception:
                pass

    def test_clean_title_and_publisher_separation(self):
        headline, pub = self.engine._extract_publisher_and_clean_title(
            "ISRO scheduled to launch NVS-02 satellite: Live Updates - The Hindu"
        )
        self.assertEqual(pub, "The Hindu")
        self.assertEqual(headline, "ISRO scheduled to launch NVS-02 satellite")

    def test_rss_xml_parsing(self):
        items = self.engine.parse_rss_items(SAMPLE_RSS_XML, pillar="ISRO / Space / Innovation", query="Test Query")
        self.assertEqual(len(items), 3)

        # Item 1
        self.assertEqual(items[0]["publisher"], "The Hindu")
        self.assertIn("ISRO scheduled to launch", items[0]["cleaned_title"])
        self.assertIsNotNone(items[0]["published_at_ist"])
        self.assertIn("IST", items[0]["published_at_ist"])

    def test_fact_verification_classification(self):
        items = self.engine.parse_rss_items(SAMPLE_RSS_XML, pillar="ISRO / Space / Innovation", query="Test Query")
        trusted = ["thehindu.com", "livemint.com"]

        # Item 0: Scheduled future event from trusted publisher
        verif0 = self.engine.verify_story_and_classify(items[0], trusted)
        self.assertEqual(verif0["verification_status"], "SCHEDULED")
        self.assertGreaterEqual(verif0["confidence_score"], 0.85)

        # Item 1: Proposal from trusted publisher
        verif1 = self.engine.verify_story_and_classify(items[1], trusted)
        self.assertEqual(verif1["verification_status"], "PROPOSAL")
        self.assertGreaterEqual(verif1["confidence_score"], 0.80)

        # Item 2: Breaking / unverified source
        verif2 = self.engine.verify_story_and_classify(items[2], trusted)
        self.assertEqual(verif2["verification_status"], "DEVELOPING")
        self.assertEqual(verif2["confidence_score"], 0.50)

    def test_evergreen_fallback_when_offline(self):
        # Force offline by calling with non-existent local server
        self.engine.feed_health = {}
        topic_package = self.engine.select_daily_topic_for_slot(slot_id=7, cycle_date="2026-11-23")
        self.assertIsNotNone(topic_package)
        self.assertEqual(topic_package["pillar"], "ISRO / Space / Innovation")
        # Should cleanly fall back to labelled EVERGREEN
        self.assertIn(topic_package["verification_status"], ["CONFIRMED", "EVERGREEN"])
        self.assertGreaterEqual(topic_package["confidence_score"], 0.65)


if __name__ == "__main__":
    unittest.main()
