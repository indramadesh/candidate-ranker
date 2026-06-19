import requests, time, os

API_KEY = os.getenv("GOOGLE_API_KEY")
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

def call_llm(prompt: str):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    for attempt in range(3):  # retry up to 3 times
        resp = requests.post(BASE_URL, json=payload)
        if resp.status_code == 200:
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        elif resp.status_code == 503:
            print("⚠️ Gemini service unavailable, retrying...")
            time.sleep(5)  # wait before retry
        else:
            resp.raise_for_status()

    raise Exception("Gemini API failed after retries")
