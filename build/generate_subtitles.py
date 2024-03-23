from moviepy.config import change_settings
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
import assemblyai as aai
import os
import time

def generate_subtitles(video_dir, assemblyai_api_key):
    """ImageMagick BINARY"""
    change_settings({"IMAGEMAGICK_BINARY": r"ImageMagick-7.1.1-Q16\magick.exe"})

    """Your assemblyai API KEY"""
    aai.settings.api_key = assemblyai_api_key

    try:
        transcript = aai.Transcriber().transcribe(f"{video_dir}\complete_clip.mp4")
        subtitles = transcript.export_subtitles_srt()

        subtitles_dir = "subtitles"
        os.makedirs(subtitles_dir, exist_ok=True)

        with open("subtitles\subtitles.srt", "w+") as f:
            f.write(subtitles)

    except aai.AssemblyAIError as erra:
        print(f"Something gone wrong with transcription module: {erra}")
        return

    except aai.TranscriptError as errt:
        print(f"Something gone wrong with transcription: {errt}")
        return

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return

    main_video = VideoFileClip(f"{video_dir}\complete_clip.mp4")

    sub_height = main_video.size[1]
    sub_width = main_video.size[0]

    text_width = int(sub_width) * 3/4

    generator = lambda txt: TextClip(txt, font="Arial-Black", fontsize=40, color="#ffd400",
                                        method='caption', size=(text_width, None)
                                        , bg_color='#0d1117ad', stroke_width=0)

    sub_clip = SubtitlesClip('subtitles\subtitles.srt', generator)

    subtitle_x_position = 'center'
    subtitle_y_position = int(sub_height) * 3.1 / 5
    sub_clip = sub_clip.set_position((subtitle_x_position, subtitle_y_position))

    result = CompositeVideoClip([main_video, sub_clip], size=main_video.size)

    result = result.set_end(result.duration - 0.35)

    result = result.set_audio(main_video.audio.set_start(0.35))

    timestr = time.strftime("%Y%m%d-%H%M%S")

    try:
        result.write_videofile(f"{video_dir}\complete_clip_w_subtitles_{timestr}.mp4", temp_audiofile="temp-audio.m4a",
                               remove_temp=True, codec="libx264", audio_codec="aac", fps=main_video.fps)
    except Exception as e:
        print(f"Unexpected error occurred while writing the video file: {e}")