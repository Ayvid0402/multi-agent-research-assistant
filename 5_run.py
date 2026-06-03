# 5_run.py
# Terminal version of the Multi-Agent Research Assistant
# Run this file to use the system in the terminal

import os
import logging
from datetime import datetime
import importlib

# ── Setup Logging ─────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/run_{datetime.now().strftime('%Y%m%d')}.log"
logger = logging.getLogger("run")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_filename)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

# ── Import the Coordinator Agent ──────────────────────────────────────────────
coordinator_module = importlib.import_module("4_coordinator_agent")
coordinator_agent  = coordinator_module.coordinator_agent

# ── Main Program ──────────────────────────────────────────────────────────────
def main():
    print("\n" + "═" * 60)
    print("   🤖 MULTI-AGENT RESEARCH ASSISTANT")
    print("   Powered by Groq + Llama 3.1")
    print("═" * 60)
    print("Type your question and press Enter")
    print("Type 'quit' or 'exit' to stop")
    print("═" * 60)

    logger.info("Multi-Agent Research Assistant started")

    while True:
        print()
        query = input("🔎 Your Question: ").strip()

        # ── Check if user wants to quit ───────────────────────────────────────
        if query.lower() in ["quit", "exit", "q"]:
            print("\n👋 Goodbye! Thanks for using the Research Assistant!")
            logger.info("User exited the application")
            break

        # ── Check if user typed nothing ───────────────────────────────────────
        if not query:
            print("⚠️  Please type a question first!")
            continue

        # ── Run the full agent pipeline ───────────────────────────────────────
        logger.info(f"New query received: {query}")

        try:
            result = coordinator_agent(query)
            logger.info(f"Query completed successfully: {query}")
            print(f"\n💾 Report saved to outputs/ folder!")

        except Exception as e:
            logger.error(f"Query failed | Error: {e}")
            print(f"\n❌ Something went wrong: {e}")
            print("Please try again with a different question.")

        # ── Ask if user wants to continue ─────────────────────────────────────
        print("\n" + "─" * 60)
        another = input("🔄 Research another topic? (yes/no): ").strip().lower()
        if another not in ["yes", "y"]:
            print("\n👋 Goodbye! Thanks for using the Research Assistant!")
            logger.info("User chose to exit after query")
            break

# ── Run the program ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()