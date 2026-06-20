# 🎙️ Tamil Voice Agent - Real-Time Multilingual Conversational System

A real-time multilingual voice agent capable of conducting a complete customer-salesperson conversation in Tamil and English using Speech-to-Text (STT), Neural Machine Translation (NMT), and Text-to-Speech (TTS).

The system listens to a Tamil-speaking customer, transcribes the speech, translates it into English, captures the salesperson's English response, translates it back to Tamil, and finally speaks the response aloud to the customer.

---

## 🚀 Features

* 🎤 Real-time voice recording with automatic silence detection.
* 🗣️ Tamil Speech-to-Text using Faster-Whisper.
* 🌐 Tamil → English translation using Meta NLLB-200.
* 🧠 Tamil text cleaning and correction pipeline.
* 🎧 Salesperson speech capture using OpenAI Whisper.
* 🔄 English → Tamil translation.
* 🔊 Tamil Text-to-Speech generation using gTTS.
* ⚡ End-to-end multilingual conversational workflow.
* 🛑 Automatic recording termination based on silence threshold.

---

## 🏗️ System Architecture

```text
Customer Speaks (Tamil)
            │
            ▼
    Audio Recording
            │
            ▼
     Faster-Whisper STT
            │
            ▼
Tamil Text Correction Pipeline
(Cleaning + Fuzzy Matching + Seq2Seq)
            │
            ▼
    NLLB Translation
   Tamil → English
            │
            ▼
 Salesperson Reads English
            │
            ▼
 Salesperson Voice Capture
            │
            ▼
      Whisper STT
            │
            ▼
 English Response Text
            │
            ▼
 Google Translation API
   English → Tamil
            │
            ▼
      gTTS Synthesis
            │
            ▼
 Customer Hears Tamil Audio
```

---

## 📂 Project Structure

```text
voice-agent/
│
├── main.py
├── whisper_test.py
├── salesperson.py
├── translator.py
├── translatetotamil.py
├── text_to_speech_for_client.py
├── requirements.txt
├── .env
├── agent_audio.wav
├── salesperson_audio.wav
└── tamil_reply.mp3
```

---

## ⚙️ Technologies Used

| Category               | Technology                       |
| ---------------------- | -------------------------------- |
| Language               | Python                           |
| Speech Recognition     | Faster-Whisper, OpenAI Whisper   |
| Translation            | Meta NLLB-200, Google Translator |
| Deep Learning          | HuggingFace Transformers         |
| Audio Processing       | SoundDevice, NumPy, SciPy        |
| Text-to-Speech         | gTTS                             |
| Environment Management | python-dotenv                    |

---

## 🔧 Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/voice-agent.git
cd voice-agent
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📝 Environment Variables

Create a `.env` file:

```env
FFMPEG_PATH=C:\ffmpeg\bin
WHISPER_MODEL=medium

SILENCE_THRESHOLD=0.015
SILENCE_LIMIT=2.5
MAX_RECORD_SEC=180
```

---

## ▶️ Running the Application

```bash
python main.py
```

---

## 🔄 Conversation Flow

### Step 1

Customer speaks in Tamil.

Example:

```text
வணக்கம், இந்த பொருளின் விலை என்ன?
```

### Step 2

System transcribes and translates:

```text
Hello, what is the price of this product?
```

### Step 3

Salesperson replies in English:

```text
The price of this product is 50000 rupees.
```

### Step 4

System translates response to Tamil:

```text
இந்த பொருளின் விலை 50000 ரூபாய்.
```

### Step 5

Tamil audio is generated and played back.

---

## 🧠 Technical Highlights

* Implemented voice activity detection using RMS audio levels.
* Designed automatic recording stop using silence thresholds.
* Integrated Faster-Whisper for efficient multilingual transcription.
* Built a text correction pipeline involving:

  * Regex-based cleaning.
  * Fuzzy vocabulary matching.
  * Seq2Seq refinement.
* Utilized Meta's NLLB-200 multilingual translation model.
* Implemented modular architecture for extensibility and maintainability.

---

## 📈 Future Improvements

* Replace gTTS with low-latency neural TTS models.
* Integrate Large Language Models for intelligent responses.
* Add WebSocket-based real-time streaming.
* Containerize using Docker.
* Build a React/Next.js frontend.
* Deploy as a cloud-native conversational service.

---

## 👨‍💻 Author

**Ayush Tiwari**

Final Year Software Engineering Student passionate about building AI-powered systems, multilingual applications, and scalable backend architectures.

Feel free to connect and collaborate.
