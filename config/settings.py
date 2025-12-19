import os
from dotenv import load_dotenv

# Force reload of .env to catch the new key
load_dotenv(override=True)

# Update to use Groq Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🔥 CRITICAL: Use Llama 3.3 70B (Best for Hindi & Logic on Groq)
MODEL_NAME = "llama-3.3-70b-versatile" 

LANGUAGE = "hi"