import os
import json
import googleapiclient.discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def get_youtube_client():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, SCOPES
        )

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            SCOPES,
        )

        creds = flow.run_local_server(
            host="localhost",
            port=8080,
            prompt="consent",
            authorization_prompt_message=""
        )

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return googleapiclient.discovery.build(
        "youtube", "v3", credentials=creds
    )
