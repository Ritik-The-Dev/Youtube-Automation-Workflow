# import os
# from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
# from src.fetch_videos import fetch_latest
# from src.transcript import get_video_transcript
# from src.filter_story import is_bravery_story
# from src.script_writer import generate_scenes
# from src.generateImage import generate_image
# from src.generateAudio import generate_voice
# from src.generateVideo import generate_video

# def run():
#     video_ids = fetch_latest(5)  # Fetch latest 5 video IDs
#     for vid in video_ids:
#         text = get_video_transcript(vid)
        
#         if not is_bravery_story(text):
#             print(f"Video {vid} is not a bravery story. Skipping.")
#             continue
        
#         if not text or not text.strip():
#             print("Empty transcript, skipping scene generation")
#             continue    
        
#         scene_data = generate_scenes(text)
        
#         # Create a folder for the video ID if it doesn't exist
#         folder_path = f"./data/{vid}"
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)
        
#         print(scene_data)
        
#         # Generate images and audio for each scene
#         for i in range(len(scene_data['scenes'])):
#             voice = scene_data['scenes'][i]['voiceoverText']
#             prompt = scene_data['scenes'][i]['imagePrompt']
#             generate_image(prompt, i, vid)  
#             generate_voice(voice, i, vid)  
        
#         # Create the final video from the images and audio
#         generate_video(vid, scene_data, folder_path)

# if __name__ == "__main__":
#     run()


import os
import json
from src.fetch_videos import fetch_latest
from src.transcript import get_video_transcript
from src.filter_story import is_bravery_story
from src.script_writer import generate_scenes
from src.generateImage import generate_image
from src.generateAudio import generate_voice
from src.generateVideo import generate_video
from src.script_writer import save_generated_topic

def run():
    scene_data = generate_scenes()
    
    # Create a folder for the video ID if it doesn't exist
    folder_path = f"./data/{"File_To_Upload"}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Add Script to Folder
    scriptPath = os.path.join(f"./data/File_To_Upload", f"Script.json")
    with open(scriptPath, 'w', encoding="utf-8") as f:
            json.dump(scene_data, f, ensure_ascii=False, indent=4)
    
    print("Scene generated successfully")
    
    # Generate images and audio for each scene
    for i in range(len(scene_data['scenes'])):
        voice = scene_data['scenes'][i]['voiceoverText']
        prompt = scene_data['scenes'][i]['imagePrompt']
        generate_image(prompt, i, "File_To_Upload")  
        generate_voice(voice, i, "File_To_Upload")  
    
    # Create the final video from the images and audio
    generate_video("File_To_Upload", scene_data, folder_path)
    save_generated_topic(scene_data["foodItem"])


if __name__ == "__main__":
    run()
