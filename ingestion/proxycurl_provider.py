import uuid
import requests
from datetime import datetime, timezone
from typing import Any
from config import Config
from ingestion.base import BaseIngestionProvider

class ProxycurlIngestionProvider(BaseIngestionProvider):

    def fetch_mentions(self, target_entity: str) -> list[dict[str, Any]]:
        if not Config.PROXYCURL_API_KEY:
            print("[Proxycurl] Key missing. Skipping LinkedIn ingestion.")
            return []

        headers = {"Authorization": f"Bearer {Config.PROXYCURL_API_KEY}"}
        endpoint = "https://nubela.co/proxycurl/api/v2/linkedin/company/mention"
        params = {"keyword": target_entity}

        try:
            response = requests.get(endpoint, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            posts = response.json().get("posts", [])
            now = datetime.now(timezone.utc).isoformat()

            mentions = []
            for post in posts:
                mentions.append({
                    "mention_id": str(uuid.uuid4()),
                    "target_entity": target_entity,
                    "source_platform": "LinkedIn",
                    "author_name": post.get("author_name", "LinkedIn User"),
                    "author_profile_url": post.get("author_profile_url", ""),
                    "content_body": post.get("text", ""),
                    "original_url": post.get("post_url", ""),
                    "published_timestamp": post.get("timestamp", now),
                    "ingested_timestamp": now
                })
            return mentions
        except Exception as e:
            print(f"[Proxycurl] Ingestion failed for {target_entity}: {e}")
            return []