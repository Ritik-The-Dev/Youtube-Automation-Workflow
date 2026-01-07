import json
from googleapiclient.http import MediaFileUpload
from .auth import get_youtube_client


def upload_to_youtube(video_path: str, script_path:str) -> str:
    youtube = get_youtube_client()
    with open(script_path, "r", encoding="utf-8") as f:
        script = json.load(f)
    title = script.get(
    "title",
    "एक छोटी कहानी, बड़ी सीख 🌟 | Kids Moral Story"
)
    description = script.get(
    "description",
    "एक प्यारी सी बच्चों की कहानी जो सिखाती है अच्छी आदत ✨\n"
    "Kids Moral Story | Hindi Kahani | Short Story\n"
    "पूरी कहानी देखो 👀"
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
                "selfDeclaredMadeForKids": True,
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
