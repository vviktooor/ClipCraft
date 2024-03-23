from nltk.tokenize import sent_tokenize
from generate_voices import generate_voices
from generate_images import generate_images
from generate_video import generate_video
from generate_subtitles import generate_subtitles

def split_into_chapters(text, chapter_length):
    chapters = []
    sentences = sent_tokenize(text)
    current_chapter = ''
    for sentence in sentences:
        if len(current_chapter) + len(sentence) < chapter_length:
            current_chapter += sentence + ' '
        else:
            chapters.append(current_chapter)
            current_chapter = sentence + ' '

    if current_chapter:
        chapters.append(current_chapter)

    print(chapters)
    return chapters

def main():
    text = """Body: Our body is like a building made up of millions of small parts called cells. Cells are like tiny blocks that together make up our body.
    Bones: These are the hard parts inside our body that help us move and keep our body straight. They're like blocks put together to create a skeleton that gives us shape.
    Muscles: Muscles are the flexible parts of our body that help us move. When you want to lift something heavy or run fast, your muscles work hard to help you.
    Organs: Our organs are special parts of the body that do different things to help us function well. For example, the heart is an organ that pumps blood around our body, and the lungs help us breathe.
    Brain: This is our super important body part! The brain controls everything we do. It helps us think, feel, remember, and much more.
    Heart: This is the organ that pumps blood around our body. Without the heart, our body wouldn't get the oxygen and nutrients we need to stay healthy.
    Lungs: These are the organs that help us breathe. When we breathe in, the lungs take in oxygen from the air we inhale, which we need to live, and then remove carbon dioxide, which our body doesn't need."""

    chapters = split_into_chapters(text, 100)
    # generate_images(chapters, "chapter_images", "1024x1792", "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")
    generate_voices(chapters)
    generate_video("chapter_images", "chapter_music", "img_w_audio", "complete_clip")
    generate_subtitles("complete_clip\complete_clip.mp4", "b0e64dcaaa1b4f6a8b2359d55bd55b7a")


if __name__ == "__main__":
    main()