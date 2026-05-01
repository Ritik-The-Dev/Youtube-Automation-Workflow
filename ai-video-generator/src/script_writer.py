import json
import os
import requests
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
TOPICS_FILE = os.path.join(DATA_DIR, "generatedTopics.json")

API_URL = "https://gen.pollinations.ai/v1/chat/completions"
API_KEY =  os.getenv("POLLINATIONS_API_KEY")


# ------------------ TOPIC STORAGE ------------------

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


# ------------------ API CALL ------------------

def call_ai(prompt, temperature=0.9):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": "You are a viral short-form content expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "top_p": 0.9,
        "response_format": {"type": "json_object"}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(response.text)

    return json.loads(response.json()["choices"][0]["message"]["content"])


# ------------------ GENERATION ------------------

def generate_script():
    used_topics = load_generated_topics()
    used_topics_text = ", ".join(used_topics) if used_topics else "None"

    prompt = f"""
    Act like a world-class viral short-form storyteller, scriptwriter, and retention strategist specialized in Hindi/Hinglish content for reels and shorts.

Your goal is to create a highly engaging, scroll-stopping food story video script that maximizes viewer retention for at least 30 seconds and drives curiosity till the end.

Task: Generate a continuous, natural-sounding Hindi narration about a unique or surprising Indian food story, then seamlessly split it into visual scenes.

Requirements:
1) First, internally craft ONE uninterrupted narration (under 60 seconds) that sounds like a human speaking in one breath.
2) The narration must follow this emotional arc: curiosity → intrigue → escalation → twist → satisfying reveal.
3) Use conversational Hindi/Hinglish with natural pauses using “...” instead of rigid sentences.
4) Avoid robotic tone, forced segmentation, or abrupt endings.
5) Then split the SAME narration into 5–10 second scenes WITHOUT breaking flow or restarting tone.
6) Each scene must feel like a continuation of the previous one.

Hook:
- Start with a shocking, weird, or unexpected line that triggers “Wait… what??”

Title:
- 5–8 words
- English or Hinglish
- Must create a strong curiosity gap and Highest Clicking

Description:
- High Retention
- Must include: “Indian food story” and “desi kahani”
- End with: Watch till end 👀

Context:
///
Avoid these topics: {used_topics_text}
Follow structured output discipline and strict formatting as recommended in OUTPUT FORMAT
///

Constraints:
- Format: Strict JSON only
- No markdown, no explanation, no extra text
- Style: Conversational, smooth, immersive
- Scope: Only food-based storytelling, no unrelated content
- Reasoning: Build narrative step-by-step internally, but output only final JSON
- Self-check: Ensure narration flow is continuous and scenes don’t feel disconnected

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

Take a deep breath and work on this problem step-by-step.

"""

    return call_ai(prompt, temperature=0.95)


# ------------------ EVALUATION ------------------

def evaluate_script(script):
    prompt = f"""
You are a ruthless viral content evaluator.

Evaluate based on SHORT-FORM VIRALITY.

Return STRICT JSON:

{{
  "scores": {{
    "title": 1-5,
    "hook": 1-5,
    "curiosity": 1-5,
    "craving": 1-5,
    "payoff": 1-5,
    "rewatchability": 1-5,
    "overall": 1-5
  }},
  "verdict": "pass" or "fail",
  "issues": ["..."],
  "improvements": ["..."]
}}

PASS RULE:
- overall >= 4
- hook >= 4
- payoff >= 4

SCRIPT:
{json.dumps(script, ensure_ascii=False)}
"""

    return call_ai(prompt, temperature=0.3)


# ------------------ REFINEMENT ------------------

def refine_script(script, evaluation):
    prompt = f"""
You are a viral script optimizer.

Improve this script WITHOUT changing its core idea.

Fix:
 **Evaluation Criteria:**
    *   **Hook:** Does it grab attention within the first 3 seconds? Is it intriguing and promise value?
    *   **Craving:** Does it build anticipation and make the viewer want to see what happens next?
    *   **Payoff:** Does it deliver on the promise of the hook? Is it satisfying and memorable?
    *   **Relatability:** Will the target audience connect with the content and find it relevant to their lives?
*   **Tone:** Maintain a professional and constructive tone.

Return STRICT JSON (same format).

ISSUES:
{evaluation["issues"]}

IMPROVEMENTS:
{evaluation["improvements"]}

SCRIPT:
{json.dumps(script, ensure_ascii=False)}
"""

    return call_ai(prompt, temperature=0.8)


# ------------------ MAIN PIPELINE ------------------

def generate_with_feedback(max_attempts=3):
    script = generate_script()

    for i in range(max_attempts):
        evaluation = evaluate_script(script)

        print(f"\n🔍 Attempt {i+1} Score:", evaluation["scores"])

        if evaluation["verdict"] == "pass":
            print("✅ Passed viral criteria")
            save_generated_topic(script["foodItem"])
            return script

        print("⚠️ सुधार किया जा रहा है...")
        script = refine_script(script, evaluation)

    print("⚠️ Max attempts reached, returning best version")
    return script


# ------------------ SAVE OUTPUT ------------------

if __name__ == "__main__":
    final_script = generate_with_feedback()

    print(json.dumps(final_script, indent=4, ensure_ascii=False))