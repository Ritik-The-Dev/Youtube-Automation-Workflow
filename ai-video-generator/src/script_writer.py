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
    Transform the following real-life incident into an ultra-realistic, cinematic short film script. The story should be about a brave Indian soldier (Jawan) performing a courageous act. Condense the narrative into a dynamic, 30-60 second sequence with vivid, immersive details. The story should focus on the action and bravery of the soldier in the face of adversity.

    For each scene:
    - Focus on the action, drama, and thrill of the soldier’s courage.
    - Create a photorealistic, cinematic image prompt for each scene.
    - Write a powerful, engaging voiceover text (in Hindi), capturing the essence of the moment.
    - The response must strictly follow the JSON format and must include a scene breakdown with:
      - `voiceoverText`: 1–2 sentences in Hindi.
      - `imagePrompt`: A photorealistic, detailed description in English.

    The incident should revolve around a dramatic, intense moment where the soldier shows immense bravery, possibly in the midst of an intense battle, a rescue mission, or facing a life-or-death situation.

    JSON FORMAT:
    {{
      "scenes": [
        {{
          "voiceoverText": "...",
          "imagePrompt": "..."
        }},
        ...
      ]
    }}

    INCIDENT:
    A brave Indian soldier risks his life to rescue his comrades under heavy fire. Amidst the chaos of a fierce battle, he moves fearlessly through enemy lines to save a wounded soldier. With determination in his eyes, he fights through the storm of bullets, showing unparalleled bravery.
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
