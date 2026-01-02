from src.fetch_videos import fetch_latest
from src.transcript import get_video_transcript
from src.filter_story import is_bravery_story
from src.script_writer import generate_scenes
from src.json2video import create_movie
from src.json2video import check_status

def run():
    video_ids = fetch_latest(5)
    for vid in video_ids:
        text = get_video_transcript(vid)
        if not is_bravery_story(text):
            print(f"Video {vid} is not a bravery story. Skipping.")
            continue
        if not text or not text.strip():
            print("Empty transcript, skipping scene generation")
            continue    
        scene_data = generate_scenes(text)
        print('Scenes Are Ready ',scene_data)
        response = create_movie(scene_data["scenes"])
        response = check_status(response.project)
        print("Submitted:", response)
        break   # ONE VIDEO PER RUN

if __name__ == "__main__":
    run()
