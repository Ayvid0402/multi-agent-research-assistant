# 1_research_agent.py
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# ── Setup Logging ─────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/research_agent_{datetime.now().strftime('%Y%m%d')}.log"
logger = logging.getLogger("research_agent")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_filename)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

# ── Load API key ──────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ── Research Agent ────────────────────────────────────────────────────────────
def research_agent(query):
    print(f"\n🔍 Research Agent starting...")
    print(f"📋 Query received: {query}\n")
    logger.info(f"Research Agent started | Query: {query}")

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Research Agent.
Your job is to research a given topic and extract the most important information.

When given a topic:
- Identify the key concepts
- Explain the main components
- List important facts
- Keep your research detailed but clear

Format your response with clear headings and bullet points."""
                },
                {
                    "role": "user",
                    "content": f"Please research this topic thoroughly: {query}"
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        research_output = response.choices[0].message.content
        logger.info(f"Research Agent finished | Characters: {len(research_output)}")

        print("✅ Research Agent finished!")
        print("─" * 50)
        print(research_output)
        print("─" * 50)

        return research_output

    except Exception as e:
        logger.error(f"Research Agent failed | Error: {e}")
        print(f"❌ Research Agent error: {e}")
        raise

# ── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = research_agent("Explain Kubernetes architecture")