# import json
# import os
# from google import genai

# client = genai.Client(
#     api_key=os.environ["GEMINI_API_KEY"]
# )

# def generate_scenes(transcript_text):
#     if not transcript_text or not transcript_text.strip():
#         return None

#     # Ensure transcript is not too long for prediction limits
#     # transcript_text = transcript_text[:2500]

#     prompt = f"""
# Transform the following real-life incident into an ultra-realistic, cinematic short film script. Condense the narrative into a dynamic, 30-60 second sequence with vivid, immersive details. For each scene:
# - Keep only essential plot points.
# - Create a photorealistic, cinematic image prompt for each scene.
# - Write a powerful, engaging voiceover text (in Hindi), capturing the essence of the moment.
# - The response must strictly follow the JSON format and must include a scene breakdown with:
#     - `voiceoverText`: 1–2 sentences in Hindi.
#     - `imagePrompt`: A photorealistic, detailed description in English.
    
# Please break the story into 4-6 cinematic scenes.

# JSON FORMAT:
# {{
#   "scenes": [
#     {{
#       "voiceoverText": "...",
#       "imagePrompt": "..."
#     }},
#     ...
#   ]
# }}

# INCIDENT:
# {transcript_text}
# """

#     # Call to the AI model
#     response = client.models.generate_content(
#         model="models/gemini-flash-latest",
#         contents=prompt,
#         config={
#             "response_mime_type": "application/json",
#             "temperature": 0.3
#         }
#     )

#     return json.loads(response.text)


import json
import os
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

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


def generate_scenes():
  
    used_topics = load_generated_topics()
    used_topics_text = ", ".join(used_topics) if used_topics else "None"
    
    # New prompt for generating the thrilling Indian Jawan story
    prompt = f"""
You are a storyteller and food historian creating SHORT, ENGAGING STORIES
about how FAMOUS INDIAN FOOD ITEMS were invented or traditionally made
(like Jalebi, Rabri, Samosa, Lassi, Kulfi, etc.).

The content is for SHORT VIDEO PLATFORMS.

The story must be:
- Simple and engaging
- Family-friendly (kids + adults)
- Rooted in Indian culture
- Nostalgic and curious
- Easy to understand
- No modern slang, no complex history jargon

━━━━━━━━━━━━━━━━━━
CONTENT REQUIREMENTS:

- Duration: 30–60 seconds
- Tone: warm, nostalgic, slightly magical, storytelling style
- Setting: old India, villages, bazaars, royal kitchens, halwai shops
- Focus: ONE food item per story

━━━━━━━━━━━━━━━━━━
TITLE & DESCRIPTION (VERY IMPORTANT FOR REACH):

1. Generate a CURIOSITY-DRIVEN TITLE:
   - Hindi or Hinglish
   - 5–10 words
   - Emotional + mysterious
   - Examples:
     “जलेबी पहली बार कैसे बनी? 😲”
     “रबड़ी की मीठी कहानी 🍯”
     “समोसे का राज़ 🥟”

2. Generate a SHORT DESCRIPTION:
   - 2–3 simple lines
   - Use emojis
   - Include keywords:
     Indian food story, food history, desi kahani, short story
   - End with: “पूरी कहानी देखो 👀”

━━━━━━━━━━━━━━━━━━
SCENE STRUCTURE:

Break the story into 4–6 short scenes.

For EACH scene:
- `voiceoverText`:
  1–2 short Hindi / Hinglish sentences
  Spoken, simple, story-style narration

- `imagePrompt`:
  Traditional Indian illustration style
  Old halwai shop / village kitchen / royal rasoi
  Warm lighting, steam, sweets, utensils
  NOT photorealistic, NOT modern
  Artistic, cinematic, nostalgic

IMPORTANT:
❌ DO NOT generate a story about these food items:
{used_topics_text}

Pick a COMPLETELY NEW Indian food item not listed above.

━━━━━━━━━━━━━━━━━━
STRICT JSON FORMAT (NO EXTRA TEXT):

{{
  "foodItem": "NAME OF FOOD",
  "title": "...",
  "description": "...",
  "scenes": [
    {{
      "voiceoverText": "...",
      "imagePrompt": "..."
    }}
  ]
}}

━━━━━━━━━━━━━━━━━━
STORY SEED (CHANGE THIS EACH TIME):

The origin or making of ONE Indian food item,
told as a simple, interesting story.
"""

    # Call to the AI model
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "temperature": 0.3
        }
    )
    result = json.loads(response.text)
    return result

# Example usage
if __name__ == "__main__":
    scene_data = generate_scenes()
    print(json.dumps(scene_data, indent=4))  # Pretty print the generated JSON
