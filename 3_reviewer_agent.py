# 3_reviewer_agent.py
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# ── Setup Logging ─────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/reviewer_agent_{datetime.now().strftime('%Y%m%d')}.log"
logger = logging.getLogger("reviewer_agent")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_filename)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

# ── Load API key ──────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ── Reviewer Agent ────────────────────────────────────────────────────────────
def reviewer_agent(summary_text):
    print(f"\n✅ Reviewer Agent starting...")
    print(f"📥 Received summary ({len(summary_text)} characters)\n")
    logger.info(f"Reviewer Agent started | Input size: {len(summary_text)} chars")

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Reviewer Agent.
Your job is to review a summary and improve it.

When reviewing:
- Check if all important points are covered
- Identify any missing information
- Fix any unclear explanations
- Add any critical missing details
- Make the final version complete and accurate

Format your response as:

## Review Notes
[What was good and what was missing]

## Improved Summary
[The complete improved version]

## Final Verdict
[1-2 sentences on quality of the summary]"""
                },
                {
                    "role": "user",
                    "content": f"Please review and improve this summary:\n\n{summary_text}"
                }
            ],
            temperature=0.5,
            max_tokens=1024
        )

        review_output = response.choices[0].message.content
        logger.info(f"Reviewer Agent finished | Output size: {len(review_output)} chars")

        print("✅ Reviewer Agent finished!")
        print("─" * 50)
        print(review_output)
        print("─" * 50)

        return review_output

    except Exception as e:
        logger.error(f"Reviewer Agent failed | Error: {e}")
        print(f"❌ Reviewer Agent error: {e}")
        raise

# ── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = """
## Summary
Kubernetes is an open-source container orchestration system by Google.
## Key Points
* Manages containerized applications
* Has Control Plane and Worker Nodes
* Pods are basic execution units
    """
    result = reviewer_agent(sample)