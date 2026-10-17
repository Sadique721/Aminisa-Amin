from engines.trend_harvester import get_latest_trends

trends = get_latest_trends()
print(f"Total trends fetched: {len(trends)}")
for i, t in enumerate(trends[:3]):
    print(f"\n--- TREND #{i+1} ---")
    print(f"Topic: {t['topic']}")
    print(f"Category: {t['category']}")
    print(f"Source: {t.get('source', '')}")
