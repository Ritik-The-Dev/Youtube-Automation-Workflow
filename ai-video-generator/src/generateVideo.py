from PIL import Image

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

    bg_music_path = os.path.join("data", "bg_music.mp3")

    if not os.path.exists(bg_music_path):
        raise FileNotFoundError(f"Background music not found: {bg_music_path}")

    bg_music = AudioFileClip(bg_music_path).volumex(BG_MUSIC_VOLUME)

    for i, scene in enumerate(scene_data["scenes"]):

        image_path = os.path.join(folder_path, f"Image{i}.png")
        audio_path = os.path.join(folder_path, f"Scene{i}.mp3")

        if not os.path.exists(image_path) or not os.path.exists(audio_path):
            print(f"⚠️ Skipping scene {i} (missing files)")
            continue

        voice_clip = AudioFileClip(audio_path)
        voice_clip = voice_clip.fx(vfx.speedx, VIDEO_SPEED)

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


generate_video("File_To_Upload", 
               {"scenes": [
        {
            "voiceoverText": "क्या आप जानते हो… समोसा पहले मीठा था? 😳… सच में!",
            "imagePrompt": "Cinematic old India street market, lantern lights, vintage shop signboards, a sweet filled pastry being sold, warm sepia tone, bustling crowd, shallow depth of field, 35mm film look"
        },
        {
            "voiceoverText": "उस जमाने में… मीठे स्वाद का दौर था… मसाला बाद में आया…",
            "imagePrompt": "Historical kitchen scene, Indian cooks preparing a sweet filling in brass bowls, wooden table, steam rising, traditional utensils, film grain, moody lighting, old city background"
        },
        {
            "voiceoverText": "फिर किसी ने सोच लिया… ‘मीठा ठीक है’… ‘पर तड़का और लगे!’…",
            "imagePrompt": "Cinematic close-up of hands sprinkling spices into a filling, spices spilling like sparks, clay stove glow, rustic textures, dramatic highlights, old India ambiance"
        },
        {
            "voiceoverText": "नतीजा… कुरकुरा… गरम… और एकदम देसी धमाका! 😄🔥",
            "imagePrompt": "Samosa frying in a deep iron kadhai, bubbling oil, golden crisp texture, crowd watching from behind, traditional garam light, slow motion feel, cinematic contrast"
        },
        {
            "voiceoverText": "आज हम सोचते हैं… ये हमेशा से ऐसा ही था… लेकिन नहीं! 😲… असली twist यही है…",
            "imagePrompt": "Street scene with vintage posters showing old recipes, samosas served with chutneys and kachori-style snacks, people smiling, night-time glow, old India aesthetic, cinematic wide shot"
        },
        {
            "voiceoverText": "तो अगली बार काटते ही… याद रखना… मीठा शुरू… और मसाला जीत गया! 😋…",
            "imagePrompt": "Hero shot: steaming samosa held close to camera, condensation on fingertips, chutney drizzle, warm bokeh lights of old bazaar, cinematic end frame, high detail"
        }
    ]},
               f"./data/{"File_To_Upload"}")