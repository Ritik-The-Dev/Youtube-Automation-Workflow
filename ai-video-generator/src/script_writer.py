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
# ROLE
You are a high-performance short-form content generator specialized in Indian street food reels.
You optimize for viewer retention, clarity, and rewatchability using psychological triggers.

---

# OBJECTIVE
Generate a short-form food video script that:
- Stops scrolling within the first 1 second
- Maintains retention by introducing a new curiosity gap every 2–3 seconds
- Clearly shows what the viewer is seeing at all times
- Delays the main payoff until the final 20% of the script
- Encourages rewatch by including at least one “replay-worthy” visual moment

---

# LANGUAGE CONSTRAINT (STRICT)
- Voiceover MUST be in pure Devanagari Hindi only
- No Hinglish, no English words, no Roman script
- Use simple, spoken Hindi (grade 6–8 level)
- Do NOT use complex metaphors or abstract phrases

---

# STRUCTURE (MANDATORY FLOW)

Scene 1 → Hook + clear visual anchor  
Scene 2 → Build curiosity (what is unusual)  
Scene 3 → Show preparation step  
Scene 4 → Increase tension or confusion  
Scene 5 → Twist or reveal setup  
Scene 6 → Final payoff (visual + sensory satisfaction)

---

# SCENE DESIGN RULES (ENFORCED)

For EACH scene:

1. Must start with a micro-hook (pattern interrupt)
2. Must clearly describe what is visible on screen
3. Must introduce ONE new piece of information or curiosity
4. Must NOT resolve the main curiosity until final scene
5. Must be logically connected to previous scene

---

# CLARITY RULE (CRITICAL)

At any point, the viewer must understand:
- What food item is being made
- What step is happening

If a line causes confusion without adding curiosity → it is invalid

---

# PSYCHOLOGICAL TRIGGERS (USE SYSTEMATICALLY)

Use at least 3 of the following across script:
- Pattern interrupt: "रुको...", "ध्यान से देखो..."
- Open loop: "लेकिन असली बात अभी बाकी है..."
- Mistake framing: "यहाँ लोग गलती करते हैं..."
- Delayed reveal: hide key ingredient until late
- Sensory build-up: texture, sound, heat, flow

---

# SENSORY LANGUAGE RULE

Each script must include at least:
- 1 texture description (e.g., कुरकुरा, नरम)
- 1 temperature cue (गरम, भाप)
- 1 motion cue (बहता हुआ, टूटता हुआ)

Do NOT use random sensory words without context

---

# FAILURE PREVENTION (STRICTLY FORBIDDEN)

- ❌ Random or meaningless phrases
- ❌ Abstract metaphors (e.g., "गरम जेब")
- ❌ Repetition of same hook pattern
- ❌ Early reveal of twist
- ❌ Generic hooks like "आप यकीन नहीं करेंगे"
- ❌ Disconnected scenes
- ❌ Overloaded or chaotic wording

---

# TITLE RULES

- 4–6 words only
- Must create a curiosity gap
- Must be understandable (not confusing)

---

# DESCRIPTION RULES

- Must include: "Indian food story" and "desi kahani"
- Must create curiosity, not summary
- Must end with: Watch till end 👀

---

# TOPIC CONSTRAINT

Avoid repeating topics from:
{used_topics_text}

Ensure the food concept is unique or has a unique twist

---

# JSON OUTPUT RULES (CRITICAL)

- Output MUST be valid JSON (no markdown, no explanation)
- Do NOT include double quotes inside text fields
- Do NOT include line breaks inside strings
- Escape all special characters properly
- Ensure array and object closure is correct

---

OUTPUT STRICT JSON:

STRICT JSON RULES:
- Do NOT use quotes inside text
- Avoid " symbols completely in voiceoverText
- Use single quotes only if needed
- Ensure valid JSON parsable output

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

---

---

# VALIDATION CHECK (MANDATORY BEFORE OUTPUT)

Ensure ALL are true:

1. First line creates immediate curiosity
2. Each scene introduces new information
3. Viewer always understands what is happening
4. Payoff is delayed until final scene
5. No vague or meaningless phrases exist
6. JSON is syntactically valid and parsable

If ANY condition fails → regenerate internally
"""

    for i in range(3):
        try:
            return call_ai(prompt)
        except Exception as e:
            print(f"Retry {i+1} بسبب JSON error...")
            time.sleep(1)
    raise Exception("Failed after retries")


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
            return script

        print("⚠️ सुधार किया जा रहा है...")
        script = refine_script(script, evaluation)

    print("⚠️ Max attempts reached, returning best version")
    return script


# ------------------ SAVE OUTPUT ------------------

if __name__ == "__main__":
    final_script = generate_with_feedback()

    print(json.dumps(final_script, indent=4, ensure_ascii=False))