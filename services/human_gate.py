import uuid
from datetime import datetime, timezone
from database import get_db_connection
from llm.responder import DraftResponder
from config import Config

def process_human_gate() -> None:
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        SELECT cl.mention_id, rm.content_body, rm.target_entity 
        FROM classification_log cl
        JOIN raw_mentions rm ON cl.mention_id = rm.mention_id
        LEFT JOIN human_gate_actions hg ON cl.mention_id = hg.mention_id
        WHERE cl.risk_flag = 'Respond Now' AND hg.action_id IS NULL
    ''')
    pending_items = c.fetchall()

    if not pending_items:
        print("[Human Gate] No pending 'Respond Now' alerts requiring approval.")
        conn.close()
        return

    responder = DraftResponder()

    print("\n=======================================")
    print("       HUMAN APPROVAL GATE REQUIRED    ")
    print("=======================================")

    for item in pending_items:
        print(f"\nTarget Entity: {item['target_entity']}")
        print(f"Mention Text : {item['content_body']}")

        choice = input("\nAuthorize LLM to generate response draft? (y/n): ").strip().lower()

        if choice == "y":
            decision = "Authorize Draft"
            print("\nGenerating approved response draft...")
            draft = responder.generate_draft(item["content_body"])
            print(f"\n[APPROVED DRAFT OUTPUT]:\n{draft}\n")
        else:
            decision = "Block Response"
            draft = None
            print("\nResponse drafting blocked by human reviewer.\n")

        c.execute('''
            INSERT INTO human_gate_actions (
                action_id, mention_id, slack_reviewer_id, review_decision,
                generated_draft, action_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()), item["mention_id"], Config.SLACK_REVIEWER_ID,
            decision, draft, datetime.now(timezone.utc).isoformat()
        ))

    conn.commit()
    conn.close()