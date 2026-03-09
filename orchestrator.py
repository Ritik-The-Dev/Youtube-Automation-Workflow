import subprocess
import time
import random
import logging

logging.basicConfig(
    filename="logs/orchestrator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

GENERATIONS_PER_DAY = 5

def run_once():
    try:
        logging.info("Starting video generation")

        GEN_PYTHON = "ai-video-generator/venv/Scripts/python.exe"
        UPLOADER_PYTHON = "ai-video-uploader/upload-env/Scripts/python.exe" 

        # 1. Generate video
        # subprocess.run(
        #     [GEN_PYTHON, "run.py"],
        #     cwd="ai-video-generator",
        #     check=True,
        # )

        # 2. Upload video
        subprocess.run(
            [UPLOADER_PYTHON,"-m", "src.watch_and_upload",],
            cwd="ai-video-uploader",
            check=True
        )

        logging.info("Upload successful")

    except Exception as e:
        logging.error(f"FAILED: {e}")

if __name__ == "__main__":
    for i in range(GENERATIONS_PER_DAY):
        run_once()

        # RANDOM DELAY (VERY IMPORTANT)
        sleep_time = random.randint(60*30, 60*90)  # 30–90 min
        logging.info(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)
