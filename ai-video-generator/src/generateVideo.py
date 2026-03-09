from PIL import Image

# 🔧 Fix for MoviePy + Pillow >=10
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS
    
import os
import random
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeAudioClip,
    vfx
)

# ================= CONFIG =================
VIDEO_SPEED = 1.00
BG_MUSIC_VOLUME = 0.15
FADE_IN_DURATION = 1
FPS = 24
# =========================================


def animated_image_clip(image_path, duration):
    """
    Creates a cinematic animated image clip using
    zoom + subtle pan (Ken Burns effect)
    """

    clip = ImageClip(image_path).set_duration(duration)

    # Controlled randomness
    zoom_start = 1.00
    zoom_end = random.uniform(1.05, 1.08)

    x_move = random.uniform(-30, 30)
    y_move = random.uniform(-20, 20)

    def zoom(t):
        return zoom_start + (zoom_end - zoom_start) * (t / duration)

    def position(t):
        return (
            x_move * (t / duration),
            y_move * (t / duration)
        )

    clip = (
        clip
        .resize(lambda t: zoom(t))
        .set_position(position)
        .fx(vfx.fadein, FADE_IN_DURATION)
    )

    return clip


def generate_video(vid, scene_data, folder_path):
    clips = []

    # ---------- Background Music ----------
    bg_music_path = os.path.join("data", "bg_music.mp3")

    if not os.path.exists(bg_music_path):
        raise FileNotFoundError(f"Background music not found: {bg_music_path}")

    bg_music = AudioFileClip(bg_music_path).volumex(BG_MUSIC_VOLUME)

    # ---------- Scene Loop ----------
    for i, scene in enumerate(scene_data["scenes"]):

        image_path = os.path.join(folder_path, f"Image{i}.png")
        audio_path = os.path.join(folder_path, f"Scene{i}.mp3")

        if not os.path.exists(image_path) or not os.path.exists(audio_path):
            print(f"⚠️ Skipping scene {i} (missing files)")
            continue

        # ---------- Load Audio ----------
        voice_clip = AudioFileClip(audio_path)
        voice_clip = voice_clip.fx(vfx.speedx, VIDEO_SPEED)

        # ---------- Animated Image ----------
        image_clip = animated_image_clip(
            image_path=image_path,
            duration=voice_clip.duration
        )

        image_clip = image_clip.set_audio(voice_clip)
        clips.append(image_clip)

    # ---------- Safety Check ----------
    if not clips:
        raise RuntimeError("No valid scenes generated. Video aborted.")

    # ---------- Concatenate ----------
    final_video = concatenate_videoclips(clips, method="compose")

    # ---------- Background Music Loop ----------
    bg_music = bg_music.audio_loop(duration=final_video.duration)

    # ---------- Mix Audio ----------
    final_audio = CompositeAudioClip([
        final_video.audio,
        bg_music
    ])

    final_video = final_video.set_audio(final_audio)

    # ---------- Export ----------
    output_path = os.path.join(folder_path, f"{vid}_final_video.mp4")

    final_video.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )

    print(f"\n✅ Video saved successfully: {output_path}\n")


# generate_video("File_To_Upload", 
#                {"scenes" : [
#         {
#             "voiceoverText": "Uttarakhand ke haseen pahadon mein ek aisi mithai milti hai, jise log 'Pahadi Chocolate' kehte hain.",
#             "imagePrompt": "A panoramic view of the misty Almora hills in old India, with stone houses and pine trees, warm morning sunlight, traditional Indian illustration style, cinematic lighting."
#         },
#         {
#             "voiceoverText": "Yeh hai Bal Mithai. Isse banane ke liye khoya ko lohe ki kadhai mein itni der bhuna jata hai ki uska rang gehra bhura ho jaye.",
#             "imagePrompt": "An old halwai in a wooden shop stirring a large iron kadhai over a wood fire, the milk solids turning a rich dark chocolate brown, steam rising, warm glow from the hearth."
#         },
#         {
#             "voiceoverText": "Is bhune hue khoye mein cheeni milakar ise jamaya jata hai, bilkul kisi naye zamane ki fudge ki tarah.",
#             "imagePrompt": "Close-up of thick, dark brown fudge-like blocks being sliced on a rustic wooden board, brass utensils and copper pots in the background, nostalgic atmosphere."
#         },
#         {
#             "voiceoverText": "Lekin iska asli jaadu hai iske upar lage safed moti, jo ise ek anokha roop aur crunch dete hain.",
#             "imagePrompt": "Hands gently rolling the dark brown cubes in tiny white sugar-coated poppy seeds, the white balls sparkling against the dark sweet, artistic focus on texture."
#         },
#         {
#             "voiceoverText": "Aaj bhi Almora ki galiyon mein iski mehek sabko apni taraf khinch leti hai. Kya aapne ise kabhi khaya hai?",
#             "imagePrompt": "A happy family standing in front of an old traditional sweet shop in a bustling hill bazaar, holding a leaf-wrapped packet of Bal Mithai, warm and nostalgic colors."
#         }
#     ]},
#                f"./data/{"File_To_Upload"}")