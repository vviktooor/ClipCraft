from moviepy.config import change_settings
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, ImageClip
import os


def generate_video(img_dir, voice_dir, img_w_audio_dir, complete_clip_dir, l_of_chapters):

    change_settings({"IMAGEMAGICK_BINARY": r"ImageMagick-7.1.1-Q16\magick.exe"})

    i = 1

    audio_clips = []
    img_clips = []
    try:
        os.makedirs(img_w_audio_dir, exist_ok=True)
    except FileNotFoundError as ef:
        print(f"the specified path does not exist: {ef}")

    for filename in os.listdir(img_dir):
        img_path = os.path.join(img_dir, filename)
        if os.path.isfile(img_path):
            v_path = os.path.join(voice_dir, f"chapter{i}.mp3")
            if os.path.isfile(v_path):
                try:
                    audio = AudioFileClip(f"{voice_dir}\chapter{i}.mp3")
                    image_clip = ImageClip(f"{img_dir}\image_{i}.png").set_duration(1)
                    img_clips.append(image_clip)
                    audio_clips.append(audio)

                    final_image = concatenate_videoclips(img_clips)
                    final_image.audio = CompositeAudioClip(audio_clips)
                    final_image.fps = 30
                    final_image.write_videofile(f"{img_w_audio_dir}\clip_chapter_{i}.mp4")
                    audio_clips.clear()
                    img_clips.clear()
                    i += 1
                except Exception as e:
                    print(f"Unexpected error occurred while processing chapter {i}: {e}")
                    continue

    i = 1
    clips = []
    for file in os.listdir(img_w_audio_dir):
        img_w_audio_path = os.path.join(img_w_audio_dir, file)
        if os.path.isfile(img_w_audio_path) and i <= l_of_chapters:
            try:
                clip = VideoFileClip(f"{img_w_audio_dir}\clip_chapter_{i}.mp4")
                clip.audio.set_start(0.35)
                clip = clip.set_end(clip.duration - 0.35)
                clips.append(clip)
                i += 1
            except Exception as e:
                print(f"Unexpected error occurred while processing clip chapter {i}: {e}")
                continue

    os.makedirs(complete_clip_dir, exist_ok=True)

    try:
        complete_clip = concatenate_videoclips(clips)
        complete_clip.fps = 30
        complete_clip.write_videofile(f"{complete_clip_dir}\complete_clip.mp4", codec='libx264',
                                      audio_codec='aac', temp_audiofile='temp-audio.m4a',
                                      remove_temp=True)
    except Exception as e:
        print(f"Unexpected error occurred while writing the complete clip: {e}")
