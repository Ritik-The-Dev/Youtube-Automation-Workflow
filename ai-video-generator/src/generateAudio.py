import os
import time
import json
import http.client
import requests
import wave
import numpy as np

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

def generate_voice(
    voiceOverText,
    sceneNumber,
    folderName,
    voice_name="st8o4LADtfxckX2PH08x",
    max_retries=3
):

    folder_path = os.path.join("data", folderName)
    os.makedirs(folder_path, exist_ok=True)

    final_audio_path = os.path.join(folder_path, f"Scene{sceneNumber}.mp3")

    for attempt in range(1, max_retries + 1):
        try:
            conn = http.client.HTTPSConnection("gen.pollinations.ai")

            payload = json.dumps({
                "model": "whisper",
                "input": voiceOverText,
                "voice": voice_name,
                "response_format": "mp3",
                "speed": 0.9,
                "language": "hi",
                "instruct": "Speak naturally in Hindi with a warm storytelling tone"
            })

            headers = {
                "Authorization": f"Bearer {POLLINATIONS_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "audio/mpeg"
            }

            conn.request("POST", "/v1/audio/speech", payload, headers)
            res = conn.getresponse()

            if res.status != 200:
                raise Exception(f"HTTP {res.status}")

            audio_data = res.read()

            with open(final_audio_path, "wb") as f:
                f.write(audio_data)

            if verify_audio(final_audio_path):
                print(f"✅ Pollinations success: Scene {sceneNumber}")
                return final_audio_path

        except Exception as e:
            print(f"⚠️ Pollinations attempt {attempt} failed: {e}")
            time.sleep(2)

    print("🔁 Switching to Cartesia fallback...")

    try:
        return generate_voice_cartesia(
            voiceOverText,
            sceneNumber,
            folder_path
        )
    except Exception as e:
        print(f"❌ Cartesia also failed: {e}")
        return None


# ------------------ CARTESIA FUNCTION ------------------
def generate_voice_cartesia(text, sceneNumber, folder_path):

    url = "https://api.cartesia.ai/tts/bytes"

    output_path = os.path.join(folder_path, f"Scene{sceneNumber}.wav")

    payload = {
        "model_id": "sonic-3",
        "transcript": text,
        "voice": {
            "mode": "id",
            "id": "f6c804d1-2c0c-4bc3-8745-a94f5f39227d"
        },
        "output_format": {
            "container": "wav",
            "encoding": "pcm_s16le",
            "sample_rate": 44100
        },
        "language": "hi"
    }
    headers = {
        "Cartesia-Version": "2026-03-01",
        "Authorization": f"Bearer {CARTESIA_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Cartesia HTTP {response.status_code}: {response.text}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    if verify_audio(output_path):
        print(f"✅ Cartesia success: Scene {sceneNumber}")
        return output_path

    raise Exception("Invalid Cartesia audio")

# ------------------ VALIDATION ------------------
def verify_audio(audio_path):
    return os.path.exists(audio_path) and os.path.getsize(audio_path) > 2000