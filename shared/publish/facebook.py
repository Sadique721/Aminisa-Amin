# -*- coding: utf-8 -*-
"""
Official Facebook Pages Graph API Publisher
Publishes video reels and feed posts directly to Facebook Page.
"""

import os
import time
from .base_publisher import BasePublisher, ENV

class FacebookPublisher(BasePublisher):
    def __init__(self):
        super().__init__("Facebook")
        self.page_id = os.getenv("FB_PAGE_ID", "61594814066987")
        self.page_token = os.getenv("FB_PAGE_TOKEN", "")
        self.graph_version = "v21.0"
        self.api_base = f"https://graph.facebook.com/{self.graph_version}"

    def publish_video_reel(self, video_url, caption, title="Aminsa AI Creator", dry_run=None):
        is_dry = self.dry_run if dry_run is None else dry_run

        if is_dry or not self.page_token or "your_" in self.page_token:
            print(f"[*] [Facebook DRY RUN] Simulating Page Reel publishing...")
            print(f"    Page ID  : {self.page_id}")
            print(f"    Video URL: {video_url}")
            print(f"    Title    : {title}")
            time.sleep(1.0)
            mock_id = f"mock_fb_reel_{int(time.time())}"
            return {
                "success": True,
                "platform": "Facebook",
                "mode": "DRY_RUN",
                "post_id": mock_id,
                "permalink": f"https://www.facebook.com/{self.page_id}/videos/{mock_id}/"
            }

        # Official Facebook Page Video Upload via URL
        url = f"{self.api_base}/{self.page_id}/videos"
        payload = {
            "file_url": video_url,
            "description": caption,
            "title": title,
            "access_token": self.page_token
        }
        res = self.make_request(url, data=payload, method="POST")
        if "id" in res:
            video_id = res["id"]
            return {
                "success": True,
                "platform": "Facebook",
                "mode": "LIVE",
                "post_id": video_id,
                "permalink": f"https://www.facebook.com/{self.page_id}/videos/{video_id}/"
            }
        return {"success": False, "error": res.get("error", "Facebook video upload failed")}

facebook_publisher = FacebookPublisher()
