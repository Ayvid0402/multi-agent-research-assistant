# 2_summarizer_agent.py
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# ── Setup Logging ─────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/summarizer_agent_{datetime.now().strftime('%Y%m%d')}.log"
logger = logging.getLogger("summarizer_agent")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_filename)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

# ── Load API key ──────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ── Summarizer Agent ──────────────────────────────────────────────────────────
def summarizer_agent(research_text):
    print(f"\n✂️  Summarizer Agent starting...")
    print(f"📥 Received research text ({len(research_text)} characters)\n")
    logger.info(f"Summarizer Agent started | Input size: {len(research_text)} chars")

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Summarizer Agent.
Your job is to take detailed research and create a clean, concise summary.

When summarizing:
- Remove all redundant and repeated information
- Keep only the most important points
- Make it easy to read and understand
- Use clear bullet points
- Keep the summary under 300 words

Format:
## Summary
[2-3 sentence overview]

## Key Points
[5-7 most important bullet points]

## Important Facts
[3-5 critical facts to remember]"""
                },
                {
                    "role": "user",
                    "content": f"Please summarize this research:\n\n{research_text}"
                }
            ],
            temperature=0.5,
            max_tokens=1024
        )

        summary_output = response.choices[0].message.content
        logger.info(f"Summarizer Agent finished | Output size: {len(summary_output)} chars")

        print("✅ Summarizer Agent finished!")
        print("─" * 50)
        print(summary_output)
        print("─" * 50)

        return summary_output

    except Exception as e:
        logger.error(f"Summarizer Agent failed | Error: {e}")
        print(f"❌ Summarizer Agent error: {e}")
        raise

# ── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = """
    Kubernetes is an open-source container orchestration system.
    Designed by Google, maintained by CNCF.
    Key components: Control Plane, Worker Nodes, Pods, Services.
    """
    result = summarizer_agent(sample)