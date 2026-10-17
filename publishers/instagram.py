# -*- coding: utf-8 -*-
"""
Official Instagram Graph API Reel Publisher
Publishes video reels via official Graph API container flow.
"""

import os
import time
from .base_publisher import BasePublisher, ENV

class InstagramPublisher(BasePublisher):
    def __init__(self):
        super().__init__("Instagram")
        self.ig_user_id = os.getenv("IG_USER_ID", "")
        self.access_token = os.getenv("FB_PAGE_TOKEN", "") or os.getenv("META_APP_SECRET", "")
        self.graph_version = "v21.0"
        self.api_base = f"https://graph.facebook.com/{self.graph_version}"

    def publish_reel(self, video_url, caption, share_to_feed=True, dry_run=None):
        is_dry = self.dry_run if dry_run is None else dry_run
        
        # Guard against unconfigured credentials
        if is_dry or not self.ig_user_id or "your_" in self.ig_user_id:
            print(f"[*] [Instagram DRY RUN] Simulating Reel publishing...")
            print(f"    Target IG ID: {self.ig_user_id or 'ig_aminsa_official'}")
            print(f"    Video URL   : {video_url}")
            print(f"    Caption     : {caption[:70]}...")
            time.sleep(1.2)
            mock_id = f"mock_ig_reel_{int(time.time())}"
            return {
                "success": True,
                "platform": "Instagram",
                "mode": "DRY_RUN",
                "media_id": mock_id,
                "permalink": f"https://www.instagram.com/reel/{mock_id}/"
            }

        # Step 1: Create media container
        url = f"{self.api_base}/{self.ig_user_id}/media"
        payload = {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": "true" if share_to_feed else "false",
            "access_token": self.access_token
        }
        res = self.make_request(url, data=payload, method="POST")
        if "id" not in res:
            return {"success": False, "error": res.get("error", "Failed to create media container")}

        container_id = res["id"]
        print(f"[+] Instagram Container Created: {container_id}. Waiting for processing...")

        # Step 2: Poll container status
        status_url = f"{self.api_base}/{container_id}?fields=status_code&access_token={self.access_token}"
        max_retries = 20
        for _ in range(max_retries):
            time.sleep(5)
            stat = self.make_request(status_url, method="GET")
            status_code = stat.get("status_code", "")
            if status_code == "FINISHED":
                break
            elif status_code in ("ERROR", "EXPIRED"):
                return {"success": False, "error": f"Container status failed: {status_code}"}

        # Step 3: Publish container
        pub_url = f"{self.api_base}/{self.ig_user_id}/media_publish"
        pub_payload = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        pub_res = self.make_request(pub_url, data=pub_payload, method="POST")
        if "id" in pub_res:
            media_id = pub_res["id"]
            return {
                "success": True,
                "platform": "Instagram",
                "mode": "LIVE",
                "media_id": media_id,
                "permalink": f"https://www.instagram.com/reel/{media_id}/"
            }
        return {"success": False, "error": pub_res.get("error", "Media publish failed")}

instagram_publisher = InstagramPublisher()
