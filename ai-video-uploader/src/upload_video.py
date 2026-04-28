import json
from googleapiclient.http import MediaFileUpload
from .auth import get_youtube_client


def upload_to_youtube(video_path: str, script_path:str) -> str:
    youtube = get_youtube_client()
    with open(script_path, "r", encoding="utf-8") as f:
        script = json.load(f)
    title = script.get(
    "title",
    "Amazing Food Stories"
)
    description = script.get(
    "description",
    "Amazing Food Stories || Story Behind Foods #shorts"
)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "22",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=MediaFileUpload(
            video_path,
            resumable=True,
            chunksize=-1
        ),
    )

    response = request.execute()
    return response["id"]
