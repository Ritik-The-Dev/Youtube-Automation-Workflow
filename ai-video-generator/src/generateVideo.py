import os
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeAudioClip,
    vfx
)

from src.generateImage import generate_image
from src.generateAudio import generate_voice


# ================= CONFIG =================
VIDEO_SPEED = 1.25          # Default playback speed
BG_MUSIC_VOLUME = 0.15      # Background music volume
FADE_IN_DURATION = 1        # seconds
FPS = 24
# ==========================================


def generate_video(vid, scene_data, folder_path):
    clips = []

    # ---------- Background Music ----------
    bg_music_path = os.path.join("data", "bg_music.mp3")

    if not os.path.exists(bg_music_path):
        raise FileNotFoundError(f"Background music not found: {bg_music_path}")

    bg_music = AudioFileClip(bg_music_path).volumex(BG_MUSIC_VOLUME)

    # ---------- Scene Loop ----------
    for i, scene in enumerate(scene_data["scenes"]):
        voice_text = scene["voiceoverText"]
        image_prompt = scene["imagePrompt"]

        generate_image(image_prompt, i, vid)
        audio_path = generate_voice(voice_text, i, vid)

        if not audio_path or not os.path.exists(audio_path):
            print(f"[WARN] Skipping scene {i}: audio not generated")
            continue

        image_path = os.path.join(folder_path, f"Image{i}.png")

        if not os.path.exists(image_path):
            print(f"[WARN] Skipping scene {i}: image missing")
            continue

        # ---------- Load Clips ----------
        image_clip = ImageClip(image_path)
        voice_clip = AudioFileClip(audio_path)

        # ---------- SPEED FIX (VIDEO + AUDIO) ----------
        image_clip = image_clip.fx(vfx.speedx, VIDEO_SPEED)
        voice_clip = voice_clip.fx(vfx.speedx, VIDEO_SPEED)

        # ---------- Sync Duration ----------
        image_clip = image_clip.set_duration(voice_clip.duration)

        # ---------- Effects ----------
        image_clip = image_clip.fadein(FADE_IN_DURATION)
        image_clip = image_clip.set_audio(voice_clip)

        clips.append(image_clip)

    # ---------- Final Safety Check ----------
    if not clips:
        raise RuntimeError("No valid scenes were generated. Video aborted.")

    # ---------- Concatenate Video ----------
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
        audio_codec="aac",
        threads=4
    )

    print(f"\n✅ Video saved successfully: {output_path}\n")
