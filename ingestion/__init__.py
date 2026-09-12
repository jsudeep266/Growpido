from database import get_db_connection
from config import Config
from ingestion.local_provider import LocalIngestionProvider
from ingestion.serpapi_provider import SerpApiIngestionProvider
from ingestion.proxycurl_provider import ProxycurlIngestionProvider
from typing import List, Optional

def run_ingestion(entities: Optional[List[str]] = None, platforms: Optional[List[str]] = None) -> int:
    conn = get_db_connection()
    c = conn.cursor()

    target_entities = entities if entities else Config.TARGET_ENTITIES
    
    # Mapping platforms to providers
    active_providers = []
    
    if Config.DATA_SOURCE == "external":
        print("[Ingestion] Data source: EXTERNAL APIs")
        
        # Match user-facing names to technical providers
        include_linkedin = not platforms or "LinkedIn" in platforms
        include_web = not platforms or ("Open Web" in platforms or "News" in platforms or "Web Search" in platforms)

        if include_linkedin:
            active_providers.append(ProxycurlIngestionProvider())
        if include_web:
            active_providers.append(SerpApiIngestionProvider())
    else:
        print("[Ingestion] Data source: LOCAL MOCK DATA")
        active_providers.append(LocalIngestionProvider())

    total_added = 0
    for entity in target_entities:
        for provider in active_providers:
            mentions = provider.fetch_mentions(entity)
            for m in mentions:
                c.execute(
                    "SELECT COUNT(*) FROM raw_mentions WHERE content_body = ? AND target_entity = ?",
                    (m["content_body"], m["target_entity"])
                )
                if c.fetchone()[0] == 0:
                    c.execute('''
                        INSERT INTO raw_mentions (
                            mention_id, target_entity, source_platform, author_name,
                            author_profile_url, content_body, original_url,
                            published_timestamp, ingested_timestamp
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        m["mention_id"], m["target_entity"], m["source_platform"],
                        m["author_name"], m["author_profile_url"], m["content_body"],
                        m["original_url"], m["published_timestamp"], m["ingested_timestamp"]
                    ))
                    total_added += 1

    conn.commit()
    conn.close()
    print(f"[Ingestion] Saved {total_added} new unique mentions to the database.")
    return total_added
