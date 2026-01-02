import requests
import json

API_URL = "https://api.json2video.com/v2/movies"
API_KEY = "dF0DA99kXLbXNhk5deX7kIASyfUNWbWAaimBD893"

def create_movie(scenes):
    payload = {
        "name": "Indian Braveheart Tribute",
        "description": "",
        "script": {
            "template": "H9bhMdrmHQ9ccvbBfbI7",
            "variables": {
                "scenes": scenes,
                "voice1": {
                    "enabled": True,
                    "model": "azure",
                    "id": "hi-IN-AartiNeural"
                },
                "music": {
                    "enabled": True,
                    "volume": 0.2
                },
                "imageSettings": {
                    "model": "flux-schnell"
                }
            }
        }
    }

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def check_status(project_id):
    headers = {"x-api-key": API_KEY}
    params = {"project": project_id}
    response = requests.get(API_URL, headers=headers, params=params)
    return response.json()

result = check_status('rtX4EDA3n6qxxu7c')
print('The result is ',result)