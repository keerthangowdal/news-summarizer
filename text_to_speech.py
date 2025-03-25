import pyttsx3
from gtts import gTTS
import os

def text_to_speech(text, filename="news_audio.mp3", engine="gtts"):
    """
    Convert text to speech and save as an MP3 file.
    - `engine="gtts"`: Uses Google Text-to-Speech (Default)
    - `engine="pyttsx3"`: Uses offline text-to-speech
    """
    if engine == "gtts":
        tts = gTTS(text=text, lang="en")
        tts.save(filename)
    else:
        tts = pyttsx3.init()
        tts.save_to_file(text, filename)
        tts.runAndWait()
    
    print(f"✅ Audio saved as {filename}")

def play_audio(filename="news_audio.mp3"):
    """Play the saved audio file."""
    os.system(f"start {filename}")  # Windows
    # Use 'afplay' for Mac or 'mpg123' for Linux

if __name__ == "__main__":
    sample_text = "This is a test news summary for Text to Speech."
    text_to_speech(sample_text)
    play_audio()
