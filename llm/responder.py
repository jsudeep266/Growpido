from openai import OpenAI
from groq import Groq
from config import Config

class DraftResponder:

    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        if self.provider == "openai":
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        elif self.provider == "groq":
            self.client = Groq(api_key=Config.GROQ_API_KEY)

    def generate_draft(self, claim_content: str) -> str:
        system_prompt = """
        You are a reputation advisory representative at Growpido in Dubai.
        Draft a direct, professional response to the hostile claim provided.
        
        Strict House Rules:
        1. Absolutely NO em dashes. Use standard hyphens or colons only.
        2. Absolutely NO hashtags.
        3. Absolutely NO AI filler vocabulary (never use words like delve, testament, tapestry, landscape, beacon, cutting-edge, or game-changer).
        4. Absolutely NO numbers or statistics published without a cited source in brackets.
        
        Keep the response clear, factual, and strictly under 3 sentences.
        """
        user_prompt = f"Hostile Claim: {claim_content}"

        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                temperature=0.2
            )
            return response.choices[0].message.content
        elif self.provider == "groq":
            # Using GPT-OSS 120B on Groq for high-quality response drafting
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                temperature=0.2
            )
            return response.choices[0].message.content
        else:
            raise ValueError(f"Unknown LLM Provider: {self.provider}")
