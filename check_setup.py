# check_setup.py
# Verifies all libraries are installed and API key is working

import os
from dotenv import load_dotenv

libraries = [
    "groq",
    "dotenv",
]

print("Checking all libraries...\n")
all_good = True

for lib in libraries:
    try:
        __import__(lib)
        print(f"  ✅ {lib} — installed")
    except ImportError:
        print(f"  ❌ {lib} — NOT installed")
        all_good = False

# ── Check API key ─────────────────────────────────────────────────────────────
print()
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print(f"  ✅ GROQ_API_KEY — found in .env file")
else:
    print(f"  ❌ GROQ_API_KEY — NOT found! Check your .env file")
    all_good = False

print()
if all_good:
    print("🎉 Everything ready! Let's build agents!")
else:
    print("⚠️  Something is missing — check above errors")