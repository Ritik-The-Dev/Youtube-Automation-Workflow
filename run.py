from src.fetch_videos import fetch_latest
from src.transcript import get_video_transcript
from src.filter_story import is_bravery_story
from src.script_writer import generate_scenes
from src.json2video import create_movie

def run():
    video_ids = fetch_latest(5)
    print("Fetched Video IDs:", video_ids)
    for vid in video_ids:
        text = get_video_transcript(vid)
        print(f"Transcript stats for {vid}:",   "length =", len(text),"| sample =", repr(text[:300]))
        if not is_bravery_story(text):
            print(f"Video {vid} is not a bravery story. Skipping.")
            continue

        scene_data = generate_scenes(text)
        print("Generated Scenes:", scene_data)
        print("###")
        print("###")
        print("###")
        print("###")
        print("###")
        response = create_movie(scene_data["scenes"])

        print("Submitted:", response)
        break   # ONE VIDEO PER RUN

if __name__ == "__main__":
    run()
