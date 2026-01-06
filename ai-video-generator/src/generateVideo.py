import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from src.generateImage import generate_image
from src.generateAudio import generate_voice

def generate_video(vid, scene_data, folder_path):
    clips = []  # List to hold the video clips
    
    # Loop over sceneData and generate images and audio
    for i in range(len(scene_data['scenes'])):
        # Get the voiceover and image prompt for each scene
        voice = scene_data['scenes'][i]['voiceoverText']
        prompt = scene_data['scenes'][i]['imagePrompt']
        
        # Generate image and audio for the scene
        generate_image(prompt, i, vid)  
        audio_path = generate_voice(voice, i, vid)
        
        if audio_path is None:
            print(f"Failed to generate audio for scene {i}, skipping.")
            continue
        
        image_path = os.path.join(folder_path, f"Image{i}.png")
        
        # Create video clip for the image
        image_clip = ImageClip(image_path)
        
        # Load the audio clip for the scene
        audio_clip = AudioFileClip(audio_path)
        
        # Set the duration of the image clip to match the audio clip's duration
        image_clip = image_clip.set_duration(audio_clip.duration)
        
        # Apply a simple fade-in effect (for 1 second)
        image_clip = image_clip.fadein(1)
        
        # Set the audio of the clip to the corresponding audio
        image_clip = image_clip.set_audio(audio_clip)
        
        # Add this clip to the list
        clips.append(image_clip)
    
    # Concatenate all video clips into one
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Output the video to a file
    output_path = os.path.join(folder_path, f"{vid}_final_video.mp4")
    final_video.write_videofile(output_path, fps=24)
    print(f"Video saved as '{output_path}'")
