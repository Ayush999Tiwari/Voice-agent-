from gtts import gTTS
import pygame
from pathlib import Path
AUDIO_OUT = Path(r"C:\Users\ayvsh\OneDrive\Desktop\voice-agent") / "tamil_reply.mp3"
def speak_tamil(tamil_text: str):
    tts = gTTS(text = tamil_text ,  lang = "ta")
    tts.save(str(AUDIO_OUT))
    pygame.mixer.init()
    pygame.mixer.music.load(str(AUDIO_OUT))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
if __name__ == "__main__":
    sample = "HII ஐயா குட் மார்னிங், ஐயா நாங்கள் எங்கள் பணியை 90% முடித்துவிட்டோம்"
    print("Speaking:", sample)
    speak_tamil(sample)