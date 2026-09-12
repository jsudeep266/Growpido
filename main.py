from database import init_db
from ingestion import run_ingestion
from llm.classifier import MentionClassifier
from services.human_gate import process_human_gate
from services.brief_generator import generate_weekly_brief

def main():
    # 1. Initialize SQLite Database Schema
    init_db()

    # 2. Run Data Ingestion (Local or External based on .env)
    run_ingestion()

    # 3. Classify Unprocessed Mentions via OpenAI
    classifier = MentionClassifier()
    classifier.process_unclassified_mentions()

    # 4. Process Human Gate for High Risk Alerts
    process_human_gate()

    # 5. Generate Weekly Executive Brief
    generate_weekly_brief()

if __name__ == "__main__":
    main()