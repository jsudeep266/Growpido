import json
import uuid
from datetime import datetime, timezone
from openai import OpenAI
from groq import Groq
from config import Config
from database import get_db_connection

class MentionClassifier:

    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        if self.provider == "openai":
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        elif self.provider == "groq":
            self.client = Groq(api_key=Config.GROQ_API_KEY)

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            return response.choices[0].message.content
        elif self.provider == "groq":
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            return response.choices[0].message.content
        else:
            raise ValueError(f"Unknown LLM Provider: {self.provider}")

    def process_unclassified_mentions(self) -> int:
        conn = get_db_connection()
        c = conn.cursor()

        # Only fetch mentions that have actual content to classify
        c.execute('''
                SELECT rm.mention_id, rm.content_body, rm.target_entity 
                FROM raw_mentions rm
                LEFT JOIN classification_log cl ON rm.mention_id = cl.mention_id
                WHERE cl.classification_id IS NULL 
                AND rm.content_body IS NOT NULL 
                AND rm.content_body != ''
            ''')
        unclassified = c.fetchall()

        if not unclassified:
            print("[Classifier] No unclassified mentions found.")
            conn.close()
            return 0

        print(f"[Classifier] Classifying {len(unclassified)} mentions via {self.provider.upper()}...")
        success_count = 0

        system_prompt = """
            You are a reputation classification engine for Growpido, an advisory firm in Dubai.
            Analyze the provided mention text.
            Identify the Sentiment: Positive, Neutral, Negative, or Ambiguous.
            Identify the Risk: Ignore, Watch, or Respond Now.
            
            Classification Rules:
            - If the target firm or industry practice is criticized but the client is not explicitly named, Risk is 'Watch' and Sentiment is 'Ambiguous'.
            - If there is an explicit accusation of fabricated metrics, regulatory non-compliance, or direct professional misconduct, Risk is 'Respond Now'.
            - If it is routine praise, news syndication, or standard industry mention, Risk is 'Ignore'.
            
            Output MUST be strict JSON with exactly two keys: "sentiment" and "risk".
            """

        for row in unclassified:
            try:
                content = self._call_llm(system_prompt, f"Target Entity: {row['target_entity']}\nContent: {row['content_body']}")
                res = json.loads(content)
                sentiment = res.get("sentiment", "Ambiguous")
                risk = res.get("risk", "Watch")

                c.execute('''
                        INSERT INTO classification_log (
                            classification_id, mention_id, sentiment_flag, risk_flag,
                            llm_raw_output, classified_timestamp
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                    str(uuid.uuid4()), row["mention_id"], sentiment, risk,
                    json.dumps(res), datetime.now(timezone.utc).isoformat()
                ))
                success_count += 1

            except Exception as e:
                print(f"[Classifier] Failed for mention {row['mention_id']}: {e}")

        conn.commit()
        conn.close()
        return success_count
