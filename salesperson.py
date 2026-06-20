import os
import logging
from pathlib import Path
import numpy as np
import sounddevice as sd
import whisper
from dotenv import load_dotenv
from scipy.io.wavfile import write

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)
load_dotenv()
class Config:
    FFMPEG_PATH: str = os.getenv("FFMPEG_PATH", "")
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "medium")
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    SILENCE_THRESHOLD: float = float(os.getenv("SILENCE_THRESHOLD", 0.02))
    SILENCE_LIMIT: float = float(os.getenv("SILENCE_LIMIT", 2.0))
    MAX_RECORD_SEC: int = int(os.getenv("MAX_RECORD_SEC", 180))
    AUDIO_FILE: Path  = Path(r"C:\Users\ayvsh\OneDrive\Desktop\voice-agent") / "salesperson_audio.wav"
def configure_ffmpeg():
    if not Config.FFMPEG_PATH:
        logger.warning("FFMPEG_PATH not set in .env — assuming ffmpeg is in system PATH.")
        return
    if Config.FFMPEG_PATH not in os.environ.get("PATH", ""):
        os.environ["PATH"] += os.pathsep + Config.FFMPEG_PATH
        logger.info(f"FFmpeg configured: {Config.FFMPEG_PATH}")
_model = None

def get_model() -> whisper.Whisper:
    global _model
    if _model is None:
        logger.info(f"Loading Whisper model: '{Config.WHISPER_MODEL}'")
        _model = whisper.load_model(Config.WHISPER_MODEL)
        logger.info("Whisper model ready.")
    return _model
def record_audio() -> Path:
    audio_buffer = []
    silent_time  = 0.0
    def callback(indata, frames, time, status):
        nonlocal silent_time
        if status:
            logger.warning(f"Audio stream status: {status}")
        volume = np.sqrt(np.mean(indata.astype(np.float32) ** 2)) / 32768.0
        print(f"[VOL] {volume:.6f} | silent_time: {silent_time:.2f}")
        audio_buffer.append(indata.copy())
        if volume < Config.SILENCE_THRESHOLD:
            silent_time += frames / Config.SAMPLE_RATE
        else:
            silent_time = 0.0
        if silent_time > Config.SILENCE_LIMIT:
            raise sd.CallbackStop()
    logger.info("Speak now — recording stops automatically after silence...")
    try:
        with sd.InputStream(
            samplerate=Config.SAMPLE_RATE,
            channels=Config.CHANNELS,
            dtype="int16",
            callback=callback
        ):
            sd.sleep(Config.MAX_RECORD_SEC * 1000)
    except sd.CallbackStop:
        logger.info("Silence detected — recording stopped.")
    except sd.PortAudioError as e:
        logger.error(f"Microphone error: {e}")
        raise RuntimeError("Could not access microphone.") from e
    if not audio_buffer:
        raise RuntimeError("No audio captured. Check your microphone.")
    audio = np.concatenate(audio_buffer, axis=0) 
    write(str(Config.AUDIO_FILE), Config.SAMPLE_RATE, audio)
    logger.info(f"Audio saved → {Config.AUDIO_FILE}")
    return Config.AUDIO_FILE

def transcribe(audio_path: Path) -> dict:
    model = get_model()
    logger.info("Transcribing...")
    result = model.transcribe(
        str(audio_path),
        task="transcribe",
        language="en",         
        fp16=False,
        verbose=False
    )
    return {
        "text": result["text"].strip(),
        "language": result["language"],
    }
def run(english_display: str) -> dict:
    configure_ffmpeg()
    print(" [SALESPERSON] Customer said:")
    print(f" {english_display}")
    audio_path = record_audio()
    result = transcribe(audio_path)
    print(f" Salesperson reply : {result['text']}")
    return {
        "text": result["text"],
        "language_code": result["language"],
    }
if __name__ == "__main__":
    sample = "Hey, I'm here to buy your stuff, tell me the price."
    run(sample)