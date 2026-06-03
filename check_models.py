# check_models.py
# This lists all available Gemini models on your account

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("Available models on your account:\n")
for model in client.models.list():
    print(f"  📌 {model.name}")