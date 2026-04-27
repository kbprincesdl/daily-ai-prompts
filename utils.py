import requests
import pandas as pd
from datetime import datetime
import os

# =========================
# CONFIGURATION
# =========================

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# 🔑 Replace with your OpenRouter API key
OPENROUTER_API_KEY = os.getenv("sk-or-v1-05100e61296c9e85fd5cbf14b03b0b50f80962e9c5fbd9f834fa8d2bf48a48a1Y") or "sk-or-xxxxxxxxxxxxxxxx"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

EXCEL_FILE = "prompts.xlsx"


# =========================
# GENERATE AI PROMPT
# =========================

def generate_prompt():
    payload = {
        "model": "mistralai/mistral-7b-instruct",  # ✅ Free & good quality
        "messages": [
            {
                "role": "user",
                "content": "Generate one creative daily AI prompt for learning or productivity."
            }
        ]
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]

        elif response.status_code == 401:
            return "❌ Invalid API key. Check your OpenRouter token."

        else:
            return f"⚠️ API Error {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Try again."

    except Exception as e:
        return f"❌ Error: {str(e)}"


# =========================
# SAVE TO EXCEL
# =========================

def save_to_excel(prompt):
    data = {
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Prompt": [prompt]
    }

    df_new = pd.DataFrame(data)

    try:
        if os.path.exists(EXCEL_FILE):
            df_existing = pd.read_excel(EXCEL_FILE, engine="openpyxl")
            df = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df = df_new

    except Exception:
        # If file is corrupted → recreate
        df = df_new

    df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")


# =========================
# LOAD DATA FOR DASHBOARD
# =========================

def load_data():
    try:
        if os.path.exists(EXCEL_FILE):
            return pd.read_excel(EXCEL_FILE, engine="openpyxl")
        else:
            return pd.DataFrame(columns=["Date", "Prompt"])
    except Exception:
        return pd.DataFrame(columns=["Date", "Prompt"])
