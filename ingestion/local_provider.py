import uuid
from datetime import datetime, timezone, timedelta
from typing import Any
from ingestion.base import BaseIngestionProvider

class LocalIngestionProvider(BaseIngestionProvider):

    def fetch_mentions(self, target_entity: str) -> list[dict[str, Any]]:
        now = datetime.now(timezone.utc)
        
        # Helper to generate dates in the past week
        def days_ago(n):
            return (now - timedelta(days=n)).isoformat()

        mock_data = {
            "Growpido": [
                {
                    "mention_id": str(uuid.uuid4()),
                    "target_entity": "Growpido",
                    "source_platform": "LinkedIn",
                    "author_name": "Compliance Officer A",
                    "author_profile_url": "https://linkedin.com/in/compliance-officer-a",
                    "content_body": "Reputation agencies are manufacturing statistics for fund managers. A 2025 study shows 71 percent of B2B buyers check profiles. This pressure causes agencies like Growpido to cut corners. Beware.",
                    "original_url": "https://linkedin.com/posts/activity-7001",
                    "published_timestamp": days_ago(1),
                    "ingested_timestamp": now.isoformat()
                },
                {
                    "mention_id": str(uuid.uuid4()),
                    "target_entity": "Growpido",
                    "source_platform": "News",
                    "author_name": "Dubai FinTech Weekly",
                    "author_profile_url": "https://dubaifintech.substack.com",
                    "content_body": "Growpido's Five Stage Reputation Architecture is standard practice now for building organic audiences in DIFC.",
                    "original_url": "https://dubaifintech.substack.com/p/edition-42",
                    "published_timestamp": days_ago(3),
                    "ingested_timestamp": now.isoformat()
                },
                {
                    "mention_id": str(uuid.uuid4()),
                    "target_entity": "Growpido",
                    "source_platform": "Open Web",
                    "author_name": "Tech Review Blog",
                    "author_profile_url": "https://techreview.com",
                    "content_body": "Checking out Growpido's latest advisory tools. They seem to be gaining traction in the Middle East market.",
                    "original_url": "https://techreview.com/growpido-review",
                    "published_timestamp": days_ago(5),
                    "ingested_timestamp": now.isoformat()
                }
            ],
            "Nidhi Hooda": [
                {
                    "mention_id": str(uuid.uuid4()),
                    "target_entity": "Nidhi Hooda",
                    "source_platform": "LinkedIn",
                    "author_name": "Anonymous Fund Manager",
                    "author_profile_url": "https://linkedin.com/in/anonymous-fm",
                    "content_body": "Nidhi Hooda just advised my firm to publish a completely fabricated AUM growth metric to drive engagement. This is a severe regulatory risk.",
                    "original_url": "https://linkedin.com/posts/activity-7002",
                    "published_timestamp": days_ago(0),
                    "ingested_timestamp": now.isoformat()
                },
                {
                    "mention_id": str(uuid.uuid4()),
                    "target_entity": "Nidhi Hooda",
                    "source_platform": "News",
                    "author_name": "Industry Insider",
                    "author_profile_url": "https://industryinsider.com",
                    "content_body": "Nidhi Hooda is scheduled to speak at the upcoming DIFC summit on digital reputation.",
                    "original_url": "https://industryinsider.com/summits",
                    "published_timestamp": days_ago(2),
                    "ingested_timestamp": now.isoformat()
                }
            ]
        }

        return mock_data.get(target_entity, [])
