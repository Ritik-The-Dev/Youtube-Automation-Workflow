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
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from src.fetch_videos import fetch_latest
from src.transcript import get_video_transcript
from src.filter_story import is_bravery_story
from src.script_writer import generate_scenes
from src.generateImage import generate_image
from src.generateAudio import generate_voice
from src.generateVideo import generate_video

def run():
    scene_data = generate_scenes()
    
    # Create a folder for the video ID if it doesn't exist
    folder_path = f"./data/{"Testing"}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    print(scene_data)
    
    # Generate images and audio for each scene
    for i in range(len(scene_data['scenes'])):
        voice = scene_data['scenes'][i]['voiceoverText']
        prompt = scene_data['scenes'][i]['imagePrompt']
        generate_image(prompt, i, "Testing")  
        generate_voice(voice, i, "Testing")  
    
    # Create the final video from the images and audio
    generate_video("Testing", scene_data, folder_path)

if __name__ == "__main__":
    run()
