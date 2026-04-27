import requests
import certifi

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

HEADERS = {
    "Authorization": "Bearer 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"
}

def generate_prompt():
    payload = {
        "inputs": "Generate one creative daily AI prompt for learning or productivity:"
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            verify=False,   # ✅ bypass SSL (important for your system)
            timeout=30
        )

        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            return f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return str(e)
