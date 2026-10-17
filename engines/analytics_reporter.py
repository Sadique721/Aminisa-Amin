#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Md Sadique Amin Analytics & 24h Reporting Engine
Generates detailed daily logs and 24-hour summaries of posts, trends, and upload statuses.
"""
import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DB_PATH = Path(__file__).resolve().parent.parent / "md_sadique_amin_automation_records.db"

def get_24h_summary():
    if not DB_PATH.exists():
        print("[-] No database found at:", DB_PATH)
        return "No database found."

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    since_time = (datetime.now() - timedelta(hours=24)).isoformat()
    
    # 1. Video logs
    cur.execute("CREATE TABLE IF NOT EXISTS content_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, topic TEXT UNIQUE, category TEXT, script TEXT, video_path TEXT, youtube_video_id TEXT, status TEXT, duration_sec REAL)")
    cur.execute("SELECT COUNT(*) FROM content_logs WHERE timestamp >= ?", (since_time,))
    total_videos = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM content_logs WHERE timestamp >= ? AND (status LIKE 'SUCCESS%' OR status = 'UPLOADED')", (since_time,))
    success_videos = cur.fetchone()[0]

    # 2. Image logs
    cur.execute("CREATE TABLE IF NOT EXISTS image_posts (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, topic TEXT UNIQUE, category TEXT, hook TEXT, caption TEXT, image_path TEXT, platform TEXT, status TEXT)")
    cur.execute("SELECT COUNT(*) FROM image_posts WHERE timestamp >= ?", (since_time,))
    total_images = cur.fetchone()[0]

    total_posts = total_videos + total_images
    
    cur.execute("SELECT topic, category, youtube_video_id, status, timestamp FROM content_logs WHERE timestamp >= ? ORDER BY timestamp DESC", (since_time,))
    recent_videos = cur.fetchall()

    conn.close()
    
    report = []
    report.append("="*75)
    report.append(f"?? MD SADIQUE AMIN AI 24-HOUR CONTENT AUTOMATION AUDIT ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    report.append("="*75)
    report.append(f"? Total Posts (24h)     : {total_posts} (Videos: {total_videos}, Infographics: {total_images})")
    report.append(f"? Successful Posts      : {success_videos + total_images}")
    report.append(f"? Video Pipeline Yield  : {success_videos} published / local-ready")
    report.append(f"? YouTube Quota Usage   : ~{total_videos * 100} / 10,000 units ({round((total_videos*100)/10000*100, 1)}%)")
    report.append("-" * 75)
    report.append("LATEST PIPELINE ACTIVITY:")
    if recent_videos:
        for r in recent_videos[:5]:
            report.append(f"  [{r[4][:19]}] [{r[1]}] {r[0][:40]}... -> Status: {r[3]} (Ref: {r[2]})")
    else:
        report.append("  No video activity recorded in the last 24 hours.")
    report.append("="*75)
    
    summary_text = "\n".join(report)
    print(summary_text)
    return summary_text

if __name__ == "__main__":
    get_24h_summary()
