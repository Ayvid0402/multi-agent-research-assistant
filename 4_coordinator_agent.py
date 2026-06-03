# 4_coordinator_agent.py
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import importlib

# ── Setup Logging ─────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/coordinator_agent_{datetime.now().strftime('%Y%m%d')}.log"
logger = logging.getLogger("coordinator_agent")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_filename)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

# ── Import all agents ─────────────────────────────────────────────────────────
research_module   = importlib.import_module("1_research_agent")
summarizer_module = importlib.import_module("2_summarizer_agent")
reviewer_module   = importlib.import_module("3_reviewer_agent")

research_agent   = research_module.research_agent
summarizer_agent = summarizer_module.summarizer_agent
reviewer_agent   = reviewer_module.reviewer_agent

# ── Load API key ──────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ── Coordinator Agent ─────────────────────────────────────────────────────────
def coordinator_agent(query):
    print("\n" + "═" * 60)
    print("🤖 COORDINATOR AGENT — Starting Multi-Agent Pipeline")
    print("═" * 60)
    print(f"📋 User Query: {query}")
    print("═" * 60)
    logger.info(f"Coordinator started | Query: {query}")

    try:
        # ── STEP 1: Research ──────────────────────────────────────────────────
        print("\n📌 STEP 1: Sending to Research Agent...")
        logger.info("STEP 1 — Calling Research Agent")
        research_output = research_agent(query)
        logger.info(f"STEP 1 complete | Size: {len(research_output)} chars")

        # ── STEP 2: Summarize ─────────────────────────────────────────────────
        print("\n📌 STEP 2: Sending to Summarizer Agent...")
        logger.info("STEP 2 — Calling Summarizer Agent")
        summary_output = summarizer_agent(research_output)
        logger.info(f"STEP 2 complete | Size: {len(summary_output)} chars")

        # ── STEP 3: Review ────────────────────────────────────────────────────
        print("\n📌 STEP 3: Sending to Reviewer Agent...")
        logger.info("STEP 3 — Calling Reviewer Agent")
        review_output = reviewer_agent(summary_output)
        logger.info(f"STEP 3 complete | Size: {len(review_output)} chars")

        # ── STEP 4: Compile Report ────────────────────────────────────────────
        print("\n📌 STEP 4: Compiling Final Report...")
        logger.info("STEP 4 — Compiling final report")

        final_report = f"""
╔══════════════════════════════════════════════════════════╗
           MULTI-AGENT RESEARCH REPORT
╚══════════════════════════════════════════════════════════╝

QUERY: {query}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1 — RAW RESEARCH (from Research Agent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{research_output}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 — SUMMARY (from Summarizer Agent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{summary_output}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 — REVIEWED & IMPROVED (from Reviewer Agent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{review_output}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
END OF REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        # ── STEP 5: Save Report ───────────────────────────────────────────────
        os.makedirs("outputs", exist_ok=True)
        filename = query[:30].replace(" ", "_").replace("/", "_") + ".txt"
        filepath = os.path.join("outputs", filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_report)

        logger.info(f"Report saved to: {filepath}")
        logger.info("Coordinator finished successfully!")

        print(f"\n✅ Final report saved to: {filepath}")
        print("\n" + "═" * 60)
        print("🎉 COORDINATOR AGENT — Pipeline Complete!")
        print("═" * 60)

        return final_report

    except Exception as e:
        logger.error(f"Coordinator failed | Error: {e}")
        print(f"\n❌ Coordinator error: {e}")
        raise

# ── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = coordinator_agent("Explain Kubernetes architecture")