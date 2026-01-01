import subprocess
import json

def generate_scenes(transcript_text):
    prompt = f"""
You are creating content for an Indian patriotic YouTube Short.

TASK:
- Convert the following real incident into EXACTLY 5 scenes.
- Each scene must have:
  1. Hindi voiceover text (1–2 sentences)
  2. A detailed photorealistic cinematic image prompt
- Tone: respectful, factual, emotional, not exaggerated
- No emojis, no hashtags, no titles

OUTPUT FORMAT (STRICT JSON ONLY):
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

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode("utf-8"),
        text=True,
        capture_output=True
    )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise ValueError("LLM output was not valid JSON")
