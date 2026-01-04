import json
import os
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

def generate_scenes(transcript_text):
    if not transcript_text or not transcript_text.strip():
        return None

    # keep quota + latency predictable
    transcript_text = transcript_text[:2500]

    prompt = f"""
Convert the following real incident into EXACTLY 5 scenes.

Rules:
- Output STRICT JSON only
- Hindi language only in voiceoverText
- English language only in imagePrompt
- No markdown, no explanations, no extra text
- Each scene must contain:
  - voiceoverText (1–2 sentences)
  - imagePrompt (photorealistic cinematic description)

JSON FORMAT:
{{
  "scenes": [
    {{
      "voiceoverText": "...",
      "imagePrompt": "..."
    }}
  ]
}}

INCIDENT:
{transcript_text}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "temperature": 0.3
        }
    )

    return json.loads(response.text)
