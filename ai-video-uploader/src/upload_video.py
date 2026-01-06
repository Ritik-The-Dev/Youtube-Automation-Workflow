from googleapiclient.http import MediaFileUpload
from .auth import get_youtube_client


def upload_to_youtube(video_path: str) -> str:
    youtube = get_youtube_client()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "AI Generated Short",
                "description": "Automatically generated & uploaded",
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
