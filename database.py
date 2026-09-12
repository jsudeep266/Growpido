import sqlite3
from typing import Generator
from config import Config

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS raw_mentions (
            mention_id TEXT PRIMARY KEY,
            target_entity TEXT NOT NULL,
            source_platform TEXT NOT NULL,
            author_name TEXT NOT NULL,
            author_profile_url TEXT,
            content_body TEXT NOT NULL,
            original_url TEXT,
            published_timestamp TEXT NOT NULL,
            ingested_timestamp TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS classification_log (
            classification_id TEXT PRIMARY KEY,
            mention_id TEXT NOT NULL,
            sentiment_flag TEXT NOT NULL,
            risk_flag TEXT NOT NULL,
            llm_raw_output TEXT NOT NULL,
            classified_timestamp TEXT NOT NULL,
            FOREIGN KEY(mention_id) REFERENCES raw_mentions(mention_id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS human_gate_actions (
            action_id TEXT PRIMARY KEY,
            mention_id TEXT NOT NULL,
            slack_reviewer_id TEXT NOT NULL,
            review_decision TEXT NOT NULL,
            generated_draft TEXT,
            action_timestamp TEXT NOT NULL,
            FOREIGN KEY(mention_id) REFERENCES raw_mentions(mention_id)
        )
    ''')

    conn.commit()
    conn.close()