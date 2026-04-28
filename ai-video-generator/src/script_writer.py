import json
import os
import requests
import string
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
TOPICS_FILE = os.path.join(DATA_DIR, "generatedTopics.json")

def load_generated_topics(file_path=TOPICS_FILE):
    if not os.path.exists(file_path):
        return set()

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return set(data.get("topics", []))

def save_generated_topic(topic, file_path=TOPICS_FILE):
    topics = []

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            topics = data.get("topics", [])

    if topic not in topics:
        topics.append(topic)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"topics": topics}, f, indent=4, ensure_ascii=False)

def generate_scenes(max_retries=5):
    used_topics = load_generated_topics()
    used_topics_text = ", ".join(used_topics) if used_topics else "None"

    prompt = f"""
You are a HIGH-PERFORMING viral short video script writer.

Your job is NOT storytelling.
Your job is to MAXIMIZE RETENTION and STOP SCROLLING.

━━━━━━━━━━━━━━━━━━
STRICT RULES:

- ONLY voiceoverText must be in Hindi
- EVERYTHING ELSE must be in English
- Output STRICT JSON ONLY (no extra text)
- DO NOT use formal or robotic narration

━━━━━━━━━━━━━━━━━━
CORE VIRAL STRUCTURE (MANDATORY):

Scene 1 → HOOK (pattern interrupt)
Scene 2 → CONFUSION / curiosity
Scene 3 → BUILD-UP (story develops)
Scene 4 → TWIST / change
Scene 5 → REVEAL
Scene 6 → PAYOFF (memorable ending)

━━━━━━━━━━━━━━━━━━
HOOK RULE (VERY IMPORTANT):

First line MUST:
- break expectation
- feel surprising or weird
- create instant curiosity

❌ Avoid:
"क्या आप जानते हो"
"एक समय की बात है"

✅ Use patterns like:
"समोसा पहले मीठा था… और लोग उसे पसंद भी करते थे 😳"
"ये डिश गलती से बनी थी… और आज हर कोई खाता है 🤯"

━━━━━━━━━━━━━━━━━━
VOICE STYLE (MANDATORY):

- Conversational Hindi (not textbook)
- Include at least:
  • 1 relatable line (e.g. "सोचो ज़रा", "अजीब लगता है ना?")
  • 1 light humor moment (e.g. "किसी ने सोचा होगा… क्यों ना experiment करें 😅")
- Use pauses (...) for pacing
- Keep sentences SHORT

━━━━━━━━━━━━━━━━━━
EMOTIONAL FLOW:

Make viewer feel:
Surprise → Curiosity → Engagement → Satisfaction

━━━━━━━━━━━━━━━━━━
TITLE (HIGH CTR):

- 5–8 words
- English or Hinglish
- Must create curiosity gap
- Add 1 emoji

━━━━━━━━━━━━━━━━━━
DESCRIPTION:

- 2 lines
- Include: Indian food story, desi kahani
- Add emojis
- End with: Watch till end 👀

━━━━━━━━━━━━━━━━━━
SCENES:

4–6 scenes

Each scene:
- voiceoverText → Hindi only (1–2 short lines)
- imagePrompt → English only
  (cinematic, old India, halwai shop, warm lighting, storytelling visuals)

━━━━━━━━━━━━━━━━━━
AVOID THESE TOPICS:
{used_topics_text}

━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT:

{{
  "foodItem": "...",
  "title": "...",
  "description": "...",
  "scenes": [
    {{
      "voiceoverText": "...",
      "imagePrompt": "..."
    }}
  ]
}}
"""

    url = "https://gen.pollinations.ai/v1/chat/completions"

    headers = {
        "Authorization": "Bearer " + os.getenv("POLLINATIONS_API_KEY"),
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": "You generate viral short video scripts."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code != 200:
                raise Exception(response.text)

            raw_content = response.json()["choices"][0]["message"]["content"]

            result = json.loads(raw_content)

            # Validate Hindi (first char check)
            if result["scenes"][0]["voiceoverText"][0].lower() in string.ascii_lowercase:
                print(f"⚠️ Attempt {attempt}: English detected, retrying...")
                time.sleep(1)
                continue

            print("✅ Script generated successfully")
            return result

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            time.sleep(2)

    raise Exception("❌ Failed to generate valid Hindi script after retries")


if __name__ == "__main__":
    data = generate_scenes()
    print(json.dumps(data, indent=4, ensure_ascii=False))