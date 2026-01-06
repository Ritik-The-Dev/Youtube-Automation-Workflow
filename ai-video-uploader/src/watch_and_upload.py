# uploader/watch_and_upload.py
import os
import shutil
from datetime import date
from .upload_video import upload_to_youtube

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTBOX = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "ai-video-generator", "data", "File_To_Upload")
)

UPLOADED = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "ai-video-generator", "data", "uploaded")
)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def find_video_file(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith(".mp4"):
            return os.path.join(folder_path, file)
    return None


def run():
    print("OUTBOX path:", OUTBOX)
    print("Exists:", os.path.exists(OUTBOX))
    print("Contents:", os.listdir(OUTBOX) if os.path.exists(OUTBOX) else "N/A")

    if not os.path.exists(OUTBOX):
        print("❌ OUTBOX folder does not exist")
        return

    video_path = find_video_file(OUTBOX)

    if not video_path:
        print("⚠️ No .mp4 file found in OUTBOX")
        return

    today = date.today().isoformat()
    today_folder = os.path.join(UPLOADED, today)
    ensure_dir(today_folder)

    # determine serial number (01, 02, ...)
    existing = [
        d for d in os.listdir(today_folder)
        if os.path.isdir(os.path.join(today_folder, d))
    ]
    serial = len(existing) + 1

    job_folder_name = f"{serial:02d}_upload"
    dest_folder = os.path.join(today_folder, job_folder_name)
    ensure_dir(dest_folder)

    print(f"Uploading video: {os.path.basename(video_path)}")
    video_id = upload_to_youtube(video_path)
    print(f"Uploaded → video_id={video_id}")

    # move ALL files from OUTBOX into the dated job folder
    for file in os.listdir(OUTBOX):
        src = os.path.join(OUTBOX, file)
        dst = os.path.join(dest_folder, file)
        shutil.move(src, dst)

    print(f"✅ Moved all files to: {dest_folder}")


if __name__ == "__main__":
    run()
