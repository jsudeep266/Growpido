import uuid
import requests
from datetime import datetime, timezone
from typing import Any
from config import Config
from ingestion.base import BaseIngestionProvider

class SerpApiIngestionProvider(BaseIngestionProvider):

    def fetch_mentions(self, target_entity: str) -> list[dict[str, Any]]:
        if not Config.SERPAPI_API_KEY:
            print("[SerpAPI] Key missing. Skipping web ingestion.")
            return []

        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": f'"{target_entity}"',
            "api_key": Config.SERPAPI_API_KEY,
            "tbs": "qdr:w"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json().get("organic_results", [])
            now = datetime.now(timezone.utc).isoformat()

            mentions = []
            for item in results:
                mentions.append({
                    "mention_id": str(uuid.uuid4()),
                    "target_entity": target_entity,
                    "source_platform": "Open Web / News",
                    "author_name": item.get("source", "Web Publisher"),
                    "author_profile_url": item.get("link", ""),
                    "content_body": item.get("snippet", ""),
                    "original_url": item.get("link", ""),
                    "published_timestamp": now,
                    "ingested_timestamp": now
                })
            return mentions
        except Exception as e:
            print(f"[SerpAPI] Ingestion failed for {target_entity}: {e}")
            return []