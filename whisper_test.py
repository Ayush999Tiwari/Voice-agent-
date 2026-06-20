# this file is extracting tamil text from tamil audio and transcribing it into english
import os  
import logging
from pathlib import Path
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from scipy.io.wavfile import write
from translator import translatetoenglish
import re
from faster_whisper import WhisperModel
from difflib import get_close_matches
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

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
    SILENCE_THRESHOLD: float = float(os.getenv("SILENCE_THRESHOLD", 0.015))
    SILENCE_LIMIT: float = float(os.getenv("SILENCE_LIMIT", 2.5))
    MAX_RECORD_SEC: int = int(os.getenv("MAX_RECORD_SEC", 180))
    AUDIO_FILE: Path = Path(r"C:\Users\ayvsh\OneDrive\Desktop\voice-agent") / "agent_audio.wav"
def configure_ffmpeg():
    if not Config.FFMPEG_PATH:
        logger.warning("FFMPEG_PATH not set — assuming ffmpeg is in PATH.")
        return
    if Config.FFMPEG_PATH not in os.environ.get("PATH", ""):
        os.environ["PATH"] += os.pathsep + Config.FFMPEG_PATH
        logger.info(f"FFmpeg configured: {Config.FFMPEG_PATH}")
_model = None
def get_model():
    global _model
    if _model is None:
        logger.info(f"Loading Faster-Whisper model: {Config.WHISPER_MODEL}")
        _model = WhisperModel(
            Config.WHISPER_MODEL,
            compute_type="int8",  
        )
        logger.info("Model ready.")
    return _model
def record_audio() -> Path:
    audio_buffer = []
    silent_time = 0.0
    def callback(indata, frames, time , status):
        nonlocal silent_time
        if status:
            logger.warning(f"Audio stream status: {status}")
        volume = np.sqrt(np.mean(indata.astype(np.float32) ** 2)) / 32768.0
        print(f"[VOL] {volume:.6f} | silence: {silent_time:.2f}")
        audio_buffer.append(indata.copy())
        if volume < Config.SILENCE_THRESHOLD:
            silent_time += frames / Config.SAMPLE_RATE
        else:
            silent_time = 0.0
        if silent_time > Config.SILENCE_LIMIT:
            raise sd.CallbackStop()
    logger.info(" Speak now...")
    try:
        with sd.InputStream(
            samplerate=Config.SAMPLE_RATE,
            channels=Config.CHANNELS,
            dtype="int16",
            callback=callback
        ):
            sd.sleep(Config.MAX_RECORD_SEC * 1000)
    except sd.CallbackStop:
        logger.info("Silence detected — stopping recording.")
    if not audio_buffer:
        raise RuntimeError("No audio captured.")
    audio = np.concatenate(audio_buffer, axis=0)
    write(str(Config.AUDIO_FILE), Config.SAMPLE_RATE, audio)
    logger.info(f"Audio saved → {Config.AUDIO_FILE}")
    return Config.AUDIO_FILE
def clean_text(text):
    return re.sub(r'[^\u0B80-\u0BFF\s]', '', text)
VOCAB = [
    "நமது", "நாடு", "நாட்டில்",
    "மழை", "சென்னை", "மாவட்டம்",
    "வானிலை", "ஆய்வு", "மையம்",
    "மணி", "நேரம்", "தாழ்வு", "பகுதி",
    "உருவாகும்", "கூடும்"
]
def correct_word(word):
    match = get_close_matches(word, VOCAB, n=1, cutoff=0.6)
    return match[0] if match else word
def fuzzy_correction(text):
    words = text.split()
    return " ".join(correct_word(w) for w in words)
def lm_correction(text):
    return text
seq_model_name = "google/mt5-small"
seq_tokenizer = AutoTokenizer.from_pretrained(seq_model_name)
seq_model = AutoModelForSeq2SeqLM.from_pretrained(seq_model_name)
def seq2seq_correct(text):
    if not text.strip():
        return text
    inputs = seq_tokenizer(text, return_tensors="pt", truncation=True)
    outputs = seq_model.generate(**inputs, max_length=128)
    return seq_tokenizer.decode(outputs[0], skip_special_tokens=True)
def transcribe(audio_path: Path):
    model = get_model()
    logger.info("Transcribing...")
    tamil_prompt = (
        "இது ஒரு தமிழ் குரல் உரையாடல். "
        "பேச்சு தெளிவாகவும் இயல்பாகவும் இருக்கும். "
        "வானிலை, செய்தி, அன்றாட உரையாடல் தொடர்பான வார்த்தைகள் இடம்பெறலாம். "
        "சரியான தமிழ் எழுத்துக்களில் எழுதவும்."
    )
    segments, info = model.transcribe(
        str(audio_path),
        language="ta",
        beam_size=10,
        temperature=[0.0, 0.2, 0.4], 
        best_of=5,
        vad_filter=True,
        vad_parameters=dict(
            min_silence_duration_ms=500
        ),
        condition_on_previous_text=True,
        initial_prompt=tamil_prompt,
        word_timestamps=True,
        no_speech_threshold=0.3,
        log_prob_threshold=-0.8

    )
    segments_list = list(segments)
    text = " ".join([segment.text for segment in segments_list]).strip()
    return {
        "text": text,
        "language": info.language
    }
def run():
    configure_ffmpeg()
    while True:
        audio_path = record_audio()
        result = transcribe(audio_path)
        if result["language"] == "ta":
            raw_text = result["text"]
            cleaned = clean_text(raw_text)
            fuzzy = fuzzy_correction(cleaned)
            lm_fixed = lm_correction(fuzzy)
            final_tamil = seq2seq_correct(lm_fixed)
            english_text = translatetoenglish(final_tamil)
            english_text = translatetoenglish(result["text"])
            print(f"Tamil (raw) : {result['text']}")
            print(f"Tamil (cleaned)  : {cleaned}")
            print(f"Tamil (corrected): {final_tamil}")
            print(f"English : {english_text}")
            return{
                "text": result["text"],
                "corrected": final_tamil,
                "english_text": english_text
            }
        else:
            print(f"\nDetected {result['language']} — please speak Tamil.\n")
if __name__ == "__main__":
    run()