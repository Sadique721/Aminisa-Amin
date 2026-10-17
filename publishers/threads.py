# -*- coding: utf-8 -*-
"""
Official Threads API Publisher
Publishes video posts to Threads via official 2-step media container flow.
"""

import os
import time
from .base_publisher import BasePublisher, ENV

class ThreadsPublisher(BasePublisher):
    def __init__(self):
        super().__init__("Threads")
        self.user_id = os.getenv("THREADS_USER_ID", "")
        self.token = os.getenv("THREADS_TOKEN", "")
        self.api_base = "https://graph.threads.net/v1.0"

    def publish_video(self, video_url, text, dry_run=None):
        is_dry = self.dry_run if dry_run is None else dry_run

        if is_dry or not self.token or "your_" in self.token:
            print(f"[*] [Threads DRY RUN] Simulating Threads video post...")
            print(f"    Threads ID: {self.user_id or 'aminsa.official'}")
            print(f"    Video URL : {video_url}")
            print(f"    Text      : {text[:70]}...")
            time.sleep(1.1)
            mock_id = f"mock_threads_{int(time.time())}"
            return {
                "success": True,
                "platform": "Threads",
                "mode": "DRY_RUN",
                "post_id": mock_id,
                "permalink": f"https://www.threads.net/@aminsa.official/post/{mock_id}"
            }

        # Step 1: Create Threads video container
        url = f"{self.api_base}/{self.user_id}/threads"
        payload = {
            "media_type": "VIDEO",
            "video_url": video_url,
            "text": text,
            "access_token": self.token
        }
        res = self.make_request(url, data=payload, method="POST")
        if "id" not in res:
            return {"success": False, "error": res.get("error", "Threads container creation failed")}

        container_id = res["id"]
        print(f"[+] Threads Container Created: {container_id}. Polling status...")

        # Step 2: Poll status
        status_url = f"{self.api_base}/{container_id}?fields=status&access_token={self.token}"
        for _ in range(15):
            time.sleep(4)
            stat = self.make_request(status_url, method="GET")
            status = stat.get("status", "")
            if status == "FINISHED":
                break
            elif status == "ERROR":
                return {"success": False, "error": "Threads media processing error"}

        # Step 3: Publish container
        pub_url = f"{self.api_base}/{self.user_id}/threads_publish"
        pub_payload = {
            "creation_id": container_id,
            "access_token": self.token
        }
        pub_res = self.make_request(pub_url, data=pub_payload, method="POST")
        if "id" in pub_res:
            post_id = pub_res["id"]
            return {
                "success": True,
                "platform": "Threads",
                "mode": "LIVE",
                "post_id": post_id,
                "permalink": f"https://www.threads.net/@aminsa.official/post/{post_id}"
            }
        return {"success": False, "error": pub_res.get("error", "Threads publish failed")}

threads_publisher = ThreadsPublisher()
