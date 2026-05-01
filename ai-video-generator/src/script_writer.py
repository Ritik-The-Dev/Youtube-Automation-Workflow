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
You are a viral storyteller for short-form videos.

Your ONLY goal:
Make the viewer NOT scroll for 30 seconds.

IMPORTANT:
- First generate ONE continuous Hindi narration (like someone speaking naturally) make the narration under 1 min continuous.
- Then split it into scenes WITHOUT breaking flow of around 5-10 secs

━━━━━━━━━━━━━━━━━━

VOICE RULES:

- Sounds like a human telling a story in one breath
- Use natural pauses (...), not hard sentence breaks
- No robotic or segmented lines
- Avoid forcing structure

━━━━━━━━━━━━━━━━━━

HOOK:

Start with something shocking, weird, or unexpected.
Must feel like: “Wait… what??”

━━━━━━━━━━━━━━━━━━

FLOW:

The narration must feel like:
curiosity → intrigue → escalation → twist → satisfying reveal

━━━━━━━━━━━━━━━━━━

STYLE:

- Conversational Hindi / Hinglish
- Smooth transitions between lines
- Avoid abrupt stops
- No textbook tone

━━━━━━━━━━━━━━━━━━

OUTPUT PROCESS:

Step 1: Write FULL narration (internally)
Step 2: Split into 4–6 scenes WITHOUT breaking flow

Each scene should feel like continuation, not restart.

━━━━━━━━━━━━━━━━━━
TITLE (HIGH CTR):

- 5–8 words
- English or Hinglish
- Must create curiosity gap

━━━━━━━━━━━━━━━━━━
DESCRIPTION:

- 2 lines
- Include: Indian food story, desi kahani
- End with: Watch till end 👀

━━━━━━━━━━━━━━━━━━
AVOID THESE TOPICS:
{used_topics_text}

━━━━━━━━━━━━━━━━━━

OUTPUT REQUIREMENT:

- OUTPUT MUST BE VALID JSON ONLY
- Do not include any extra text
- No explanation, no markdown, no comments

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
        "temperature": 0.95,
        "top_p": 0.9,
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
            # if result["scenes"][0]["voiceoverText"][0].lower() in string.ascii_lowercase:
            #     print(f"⚠️ Attempt {attempt}: English detected, retrying...")
            #     time.sleep(1)
            #     continue

            print("✅ Script generated successfully")
            return result

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            time.sleep(2)

    raise Exception("❌ Failed to generate valid Hindi script after retries")


if __name__ == "__main__":
    data = generate_scenes()
    print(json.dumps(data, indent=4, ensure_ascii=False))