"""
Md Sadique Amin Trend Harvester Engine
Harvests real-time viral trends from Google Trends India RSS and Google News (Tech/Entertainment).
Zero-cost, open-source, no API keys required.
"""

import sys
import urllib.request
import xml.etree.ElementTree as ET

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def get_latest_trends():
    trends = []
    
    # 1. Google News Technology
    tech_url = "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-IN&gl=IN&ceid=IN:en"
    req = urllib.request.Request(tech_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            root = ET.fromstring(resp.read())
            for item in root.findall(".//item")[:3]:
                title = item.find("title").text
                link = item.find("link").text if item.find("link") is not None else ""
                trends.append({
                    "topic": title,
                    "category": "Tech & Future Lifestyle",
                    "source": "Google News Tech",
                    "url": link
                })
    except Exception as e:
        print(f"[-] Tech trends fetch note: {e}")

    # 2. Google News Entertainment / Culture
    ent_url = "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=en-IN&gl=IN&ceid=IN:en"
    req = urllib.request.Request(ent_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            root = ET.fromstring(resp.read())
            for item in root.findall(".//item")[:2]:
                title = item.find("title").text
                link = item.find("link").text if item.find("link") is not None else ""
                trends.append({
                    "topic": title,
                    "category": "Culture & Entertainment",
                    "source": "Google News Entertainment",
                    "url": link
                })
    except Exception as e:
        print(f"[-] Entertainment trends fetch note: {e}")

    return trends

if __name__ == "__main__":
    results = get_latest_trends()
    print(f"[+] Harvested {len(results)} live trends:")
    for idx, t in enumerate(results, 1):
        print(f"    {idx}. [{t['category']}] {t['topic']}")
