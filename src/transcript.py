import subprocess
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def get_video_transcript(video_id):
    # Attempt 1: youtube-transcript-api
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["hi", "en"]
        )
        return " ".join(item["text"] for item in transcript)
    except Exception:
        pass

    # Attempt 2: yt-dlp auto captions
    return get_transcript_via_ytdlp(video_id)


def get_transcript_via_ytdlp(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_file = f"data/transcripts/{video_id}.vtt"

    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-auto-sub",
        "--sub-lang", "hi,en",
        "--sub-format", "vtt",
        "-o", f"data/transcripts/{video_id}.%(ext)s",
        url
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(output_file):
        return ""

    return parse_vtt(output_file)


def parse_vtt(path):
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith(("WEBVTT", "00:", "<")):
                lines.append(line)
    return " ".join(lines)
