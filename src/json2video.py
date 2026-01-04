import requests
import json

API_URL = "https://api.json2video.com/v2/movies"
API_KEY = "dF0DA99kXLbXNhk5deX7kIASyfUNWbWAaimBD893"

def create_movie(scenes):
    payload = {
  "comment": "Indian Braveheart Tribute",
  "template": "H9bhMdrmHQ9ccvbBfbI7",
  "variables": {
    "scenes":  scenes,
    "music": {
      "volume": 0.2,
      "enabled": True
    },
    "imageSettings": {
      "model": "flux-schnell"
    },
    "voice1": {
      "enabled": True,
      "model": "azure",
      "id": "hi-IN-AartiNeural"
    }
  }
}

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    print('called payload ',payload)
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def check_status(project_id):
    headers = {"x-api-key": API_KEY}
    params = {"project": project_id}
    response = requests.get(API_URL, headers=headers, params=params)
    return response.json()