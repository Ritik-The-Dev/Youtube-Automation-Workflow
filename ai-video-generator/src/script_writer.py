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

def generate_scenes():
    # New prompt for generating the thrilling Indian Jawan story
    prompt = """
    You are a storyteller creating SHORT MORAL STORIES for KIDS (age 4–10),
in the style of classic Indian stories like “लालची कचौड़ी वाला”, “जलपरी”,
and simple village or fantasy tales.

The story must be:
- Simple
- Beautiful
- Child-safe
- Light-hearted
- With a clear moral lesson at the end

NO violence, NO fear, NO complex language.

━━━━━━━━━━━━━━━━━━
STORY REQUIREMENTS:

- Duration: 30–60 seconds
- Tone: magical, warm, innocent, storybook-style
- Characters: simple (shopkeeper, child, fairy, animal, villager, etc.)
- Moral themes (pick ONE):
  honesty, kindness, sharing, greed is bad, helping others, truth wins

━━━━━━━━━━━━━━━━━━
TITLE & DESCRIPTION (VERY IMPORTANT FOR REACH):

1. Generate a KID-FRIENDLY TITLE:
   - Hindi or Hinglish
   - 5–10 words
   - Curious + emotional
   - Examples:
     “लालची कचौड़ी वाला 😲”
     “जलपरी की प्यारी सीख 🧜‍♀️”
     “ईमानदार बच्चा 🌟”

2. Generate a SHORT DESCRIPTION:
   - 2–3 simple lines
   - Use emojis
   - Include keywords:
     kids story, moral story, Hindi kahani, short story
   - End with: “पूरी कहानी देखो 👀”

━━━━━━━━━━━━━━━━━━
SCENE STRUCTURE:

Break the story into 4–6 short scenes.

For EACH scene:
- `voiceoverText`:  
  1–2 short Hindi sentences  
  Very simple words (spoken Hindi, child-friendly)

- `imagePrompt`:  
  Colorful, soft, storybook-style illustration  
  Bright lighting, expressive characters, magical feel  
  (NOT photorealistic, NOT dark)

━━━━━━━━━━━━━━━━━━
STRICT JSON FORMAT (NO EXTRA TEXT):

{
  "title": "...",
  "description": "...",
  "scenes": [
    {
      "voiceoverText": "...",
      "imagePrompt": "..."
    }
  ]
}

━━━━━━━━━━━━━━━━━━
STORY SEED (CHANGE THIS EACH TIME):

A greedy street food seller who learns a lesson,
OR a magical mermaid who teaches kindness,
OR any small character who learns a good habit.
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

    return json.loads(response.text)

# Example usage
if __name__ == "__main__":
    scene_data = generate_scenes()
    print(json.dumps(scene_data, indent=4))  # Pretty print the generated JSON
