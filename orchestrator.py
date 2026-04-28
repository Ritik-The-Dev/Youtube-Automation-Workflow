import subprocess
import time
import random
import logging
from sendTelegramNotification import send_telegram
# from dotenv import load_dotenv
# load_dotenv()

logging.basicConfig(
    filename="logs/orchestrator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_once():
    try:
        logging.info("Starting video generation")

        # GEN_PYTHON = "ai-video-generator/venv/Scripts/python.exe"
        # UPLOADER_PYTHON = "ai-video-uploader/upload-env/Scripts/python.exe" 

        # 1. Generate video
        subprocess.run(
            ["python", "run.py"],
            cwd="ai-video-generator",
            check=True,
        )

        # 2. Upload video
        subprocess.run(
            ["python","-m", "src.watch_and_upload",],
            cwd="ai-video-uploader",
            check=True
        )
        print("Uploaded Properly")
        send_telegram("✅ Video uploaded successfully!")
        logging.info("Upload successful")

    except Exception as e:
        logging.error(f"FAILED: {e}")

if __name__ == "__main__":
        run_once()