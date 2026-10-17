# -*- coding: utf-8 -*-
"""
Md Sadique Amin Meta Graph API Engine (Instagram, Threads, Facebook Page)
========================================================================
Supports official automated publishing to:
1. Instagram Feed / Reels (Meta Graph API Container + Media Publish flow)
2. Facebook Page (Official Graph API direct photo/video multipart upload)
3. Threads (Official Threads Graph API container + publish flow)

Secrets loaded from:
- secrets/meta_credentials.json (or .env / environment variables)
"""

import os
import sys
import json
import time
import base64
import requests
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SECRETS_DIR = PROJECT_ROOT / "secrets"
CONFIG_FILE = SECRETS_DIR / "meta_credentials.json"

GRAPH_API_VERSION = "v21.0"
GRAPH_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
THREADS_URL = f"https://graph.threads.net/v1.0"


def load_meta_config() -> dict:
    """Loads credentials from secrets/meta_credentials.json or environment variables."""
    config = {
        "META_APP_ID": os.environ.get("META_APP_ID", ""),
        "META_APP_SECRET": os.environ.get("META_APP_SECRET", ""),
        "META_IG_USER_ID": os.environ.get("META_IG_USER_ID", ""),
        "META_THREADS_USER_ID": os.environ.get("META_THREADS_USER_ID", ""),
        "META_PAGE_ID": os.environ.get("META_PAGE_ID", ""),
        "INSTAGRAM_ACCESS_TOKEN": os.environ.get("INSTAGRAM_ACCESS_TOKEN", ""),
        "THREADS_ACCESS_TOKEN": os.environ.get("THREADS_ACCESS_TOKEN", ""),
        "FACEBOOK_PAGE_ACCESS_TOKEN": os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN", ""),
        "IMGBB_API_KEY": os.environ.get("IMGBB_API_KEY", ""),
    }
    if CONFIG_FILE.exists():
        try:
            file_data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            for k, v in file_data.items():
                if v and not config.get(k):
                    config[k] = v
        except Exception as e:
            print(f"[!] Warning reading meta_credentials.json: {e}")
    return config


def upload_image_to_public_host(image_path: str, api_key: str = "") -> str:
    """Uploads local image to ImgBB or free public HTTPS endpoint for Meta container URL requirement."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # 1. If ImgBB API key is provided
    if api_key:
        try:
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            r = requests.post(
                "https://api.imgbb.com/1/upload",
                data={"key": api_key, "image": b64},
                timeout=30
            )
            if r.status_code == 200:
                return r.json()["data"]["url"]
        except Exception as e:
            print(f"[!] ImgBB upload error: {e}")

    # 2. Fallback: Free temporary public image bridge (catbox/uguu for direct HTTPS raw image URL)
    try:
        with open(path, "rb") as f:
            files = {"fileToUpload": (path.name, f, "image/png")}
            data = {"reqtype": "fileupload"}
            r = requests.post("https://catbox.moe/user/api.php", files=files, data=data, timeout=30)
            if r.status_code == 200 and r.text.startswith("http"):
                return r.text.strip()
    except Exception as e:
        print(f"[!] Public bridge fallback error: {e}")

    raise RuntimeError("Could not obtain a publicly accessible HTTPS image URL for Meta Container API. Set IMGBB_API_KEY in secrets/meta_credentials.json.")


def post_to_instagram(image_path: str, caption: str) -> dict:
    """
    Official Instagram Content Publishing API flow:
    1. Upload image to public HTTPS URL
    2. POST /{ig-user-id}/media -> returns creation_id
    3. Wait/poll container status
    4. POST /{ig-user-id}/media_publish -> publishes post
    5. GET /{media-id} -> retrieves verified live permalink
    """
    cfg = load_meta_config()
    ig_user_id = cfg.get("META_IG_USER_ID")
    access_token = cfg.get("INSTAGRAM_ACCESS_TOKEN")

    if not ig_user_id or not access_token:
        return {
            "status": "NOT_CONFIGURED",
            "platform": "instagram",
            "message": "Missing META_IG_USER_ID or INSTAGRAM_ACCESS_TOKEN in secrets/meta_credentials.json"
        }

    print(f"[*] Posting to Instagram (@{ig_user_id})...")
    try:
        public_url = upload_image_to_public_host(image_path, cfg.get("IMGBB_API_KEY"))
        print(f"[*] Public media URL prepared: {public_url}")

        # Step 1: Create Container
        container_url = f"{GRAPH_URL}/{ig_user_id}/media"
        payload = {
            "image_url": public_url,
            "caption": caption,
            "access_token": access_token
        }
        r = requests.post(container_url, data=payload, timeout=30)
        c_res = r.json()
        if "id" not in c_res:
            return {"status": "FAILED", "platform": "instagram", "error": c_res}

        creation_id = c_res["id"]
        print(f"[+] Instagram container created: {creation_id}")

        # Wait for container processing
        time.sleep(3)

        # Step 2: Publish Container
        publish_url = f"{GRAPH_URL}/{ig_user_id}/media_publish"
        r_pub = requests.post(publish_url, data={"creation_id": creation_id, "access_token": access_token}, timeout=30)
        pub_res = r_pub.json()
        if "id" not in pub_res:
            return {"status": "FAILED", "platform": "instagram", "error": pub_res}

        media_id = pub_res["id"]

        # Step 3: Fetch verified permalink
        info_url = f"{GRAPH_URL}/{media_id}?fields=permalink,timestamp&access_token={access_token}"
        info_res = requests.get(info_url, timeout=15).json()
        permalink = info_res.get("permalink", f"https://www.instagram.com/p/{media_id}")

        return {
            "status": "SUCCESS",
            "platform": "instagram",
            "media_id": media_id,
            "permalink": permalink
        }
    except Exception as e:
        return {"status": "ERROR", "platform": "instagram", "error": str(e)}


def post_to_facebook_page(page_id: str, image_path: str, caption: str) -> dict:
    """
    Official Facebook Page Photos Publishing API:
    Supports DIRECT MULTIPART binary file upload (no public URL required)!
    POST /{page-id}/photos with multipart file
    """
    cfg = load_meta_config()
    target_page_id = page_id or cfg.get("META_PAGE_ID")
    access_token = cfg.get("FACEBOOK_PAGE_ACCESS_TOKEN")

    if not target_page_id or not access_token:
        return {
            "status": "NOT_CONFIGURED",
            "platform": "facebook_page",
            "message": "Missing META_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN in secrets/meta_credentials.json"
        }

    print(f"[*] Posting photo to Facebook Page ({target_page_id})...")
    path = Path(image_path)
    if not path.exists():
        return {"status": "ERROR", "platform": "facebook_page", "error": f"Image file not found: {image_path}"}

    try:
        url = f"{GRAPH_URL}/{target_page_id}/photos"
        with open(path, "rb") as f:
            files = {"source": (path.name, f, "image/png")}
            data = {"caption": caption, "access_token": access_token}
            r = requests.post(url, files=files, data=data, timeout=45)

        res = r.json()
        if "id" not in res:
            return {"status": "FAILED", "platform": "facebook_page", "error": res}

        photo_id = res["id"]
        post_id = res.get("post_id", photo_id)

        # Retrieve permalink
        p_url = f"{GRAPH_URL}/{post_id}?fields=permalink_url&access_token={access_token}"
        p_res = requests.get(p_url, timeout=15).json()
        permalink = p_res.get("permalink_url", f"https://www.facebook.com/{post_id}")

        return {
            "status": "SUCCESS",
            "platform": "facebook_page",
            "photo_id": photo_id,
            "post_id": post_id,
            "permalink": permalink
        }
    except Exception as e:
        return {"status": "ERROR", "platform": "facebook_page", "error": str(e)}


def post_to_threads(text: str, media_url: str = None) -> dict:
    """
    Official Threads Publishing API:
    1. POST /{threads-user-id}/threads (create container)
    2. POST /{threads-user-id}/threads_publish (publish container)
    3. Retrieve verified permalink
    """
    cfg = load_meta_config()
    threads_user_id = cfg.get("META_THREADS_USER_ID")
    access_token = cfg.get("THREADS_ACCESS_TOKEN")

    if not threads_user_id or not access_token:
        return {
            "status": "NOT_CONFIGURED",
            "platform": "threads",
            "message": "Missing META_THREADS_USER_ID or THREADS_ACCESS_TOKEN in secrets/meta_credentials.json"
        }

    print(f"[*] Publishing post to Threads ({threads_user_id})...")
    try:
        container_url = f"{THREADS_URL}/{threads_user_id}/threads"
        data = {
            "media_type": "IMAGE" if media_url else "TEXT",
            "text": text,
            "access_token": access_token
        }
        if media_url:
            data["image_url"] = media_url

        r = requests.post(container_url, data=data, timeout=30)
        c_res = r.json()
        if "id" not in c_res:
            return {"status": "FAILED", "platform": "threads", "error": c_res}

        creation_id = c_res["id"]
        time.sleep(3)

        publish_url = f"{THREADS_URL}/{threads_user_id}/threads_publish"
        r_pub = requests.post(publish_url, data={"creation_id": creation_id, "access_token": access_token}, timeout=30)
        pub_res = r_pub.json()
        if "id" not in pub_res:
            return {"status": "FAILED", "platform": "threads", "error": pub_res}

        threads_post_id = pub_res["id"]

        info_url = f"{THREADS_URL}/{threads_post_id}?fields=permalink&access_token={access_token}"
        info_res = requests.get(info_url, timeout=15).json()
        permalink = info_res.get("permalink", f"https://www.threads.net/post/{threads_post_id}")

        return {
            "status": "SUCCESS",
            "platform": "threads",
            "post_id": threads_post_id,
            "permalink": permalink
        }
    except Exception as e:
        return {"status": "ERROR", "platform": "threads", "error": str(e)}


def verify_meta_setup() -> dict:
    """Diagnostics for Meta developer accounts, permissions, and tokens."""
    cfg = load_meta_config()
    status = {}

    # Instagram
    if cfg.get("INSTAGRAM_ACCESS_TOKEN") and cfg.get("META_IG_USER_ID"):
        try:
            r = requests.get(f"{GRAPH_URL}/{cfg['META_IG_USER_ID']}?fields=username&access_token={cfg['INSTAGRAM_ACCESS_TOKEN']}", timeout=10)
            status["instagram"] = r.json() if r.status_code == 200 else {"error": r.json()}
        except Exception as e:
            status["instagram"] = {"exception": str(e)}
    else:
        status["instagram"] = {"status": "PENDING_CREDENTIALS"}

    # Facebook Page
    if cfg.get("FACEBOOK_PAGE_ACCESS_TOKEN") and cfg.get("META_PAGE_ID"):
        try:
            r = requests.get(f"{GRAPH_URL}/{cfg['META_PAGE_ID']}?fields=name,category&access_token={cfg['FACEBOOK_PAGE_ACCESS_TOKEN']}", timeout=10)
            status["facebook_page"] = r.json() if r.status_code == 200 else {"error": r.json()}
        except Exception as e:
            status["facebook_page"] = {"exception": str(e)}
    else:
        status["facebook_page"] = {"status": "PENDING_CREDENTIALS"}

    # Threads
    if cfg.get("THREADS_ACCESS_TOKEN") and cfg.get("META_THREADS_USER_ID"):
        try:
            r = requests.get(f"{THREADS_URL}/{cfg['META_THREADS_USER_ID']}?fields=username&access_token={cfg['THREADS_ACCESS_TOKEN']}", timeout=10)
            status["threads"] = r.json() if r.status_code == 200 else {"error": r.json()}
        except Exception as e:
            status["threads"] = {"exception": str(e)}
    else:
        status["threads"] = {"status": "PENDING_CREDENTIALS"}

    return status


if __name__ == "__main__":
    print("==================================================")
    print("Md Sadique Amin Meta Graph API Diagnostics")
    print("==================================================")
    diag = verify_meta_setup()
    print(json.dumps(diag, indent=2))
