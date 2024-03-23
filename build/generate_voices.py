from tiktokvoice import tts

def generate_voices(chapters, voice_select):
    sound_num = 1
    for chapter in chapters:
        try:
            text = chapter
            voice = voice_select  # all possible voices can be found here
            tts(text, voice, f"chapter{sound_num}.mp3", play_sound=True)
            print(f"Voice for chapter {sound_num} generated successfully.")
            sound_num += 1
        except Exception as e:
            print(f"An error occurred while generating voice for chapter {sound_num}: {e}")