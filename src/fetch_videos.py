import yt_dlp

URL = "https://www.youtube.com/@PresidentOfIndia/videos"

def fetch_latest(limit = 10):
    ydl_opts = {
        "quiet" : True,
        "extract_flat" : True,
        "playlistend" : limit,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL , download = False)
        return [v['id'] for v in info['entries']]