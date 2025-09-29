# Voice Bot - Real-time Conversational AI

A sophisticated real-time voice bot that captures audio from the browser, converts it to text using OpenAI Whisper, generates intelligent responses with Groq LLM, and converts the response back to speech using Google Text-to-Speech. Built with FastAPI backend and modern web frontend.

## Features

- **Real-time audio capture** from browser microphone using WebRTC
- **Speech-to-Text** using OpenAI Whisper (base model)
- **AI responses** using Groq LLM (Llama 3.1 8B Instant)
- **Text-to-Speech** using Google TTS
- **Modern web interface** with responsive design and real-time status updates
- **FastAPI backend** with CORS support and error handling
- **Conversation history** with context-aware responses
- **Cross-platform compatibility** (Windows, macOS, Linux)

## Prerequisites

- Python 3.8 or higher
- Groq API key (free tier available)

## Quick Start

### 1. Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd voice-bot

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Create a new API key
4. Copy the API key for the next step

### 3. Configure Environment

Create a `.env` file in the project root:

```bash
# Create .env file
echo "GROQ_API_KEY=your_actual_groq_api_key_here" > .env
```

**Important**: Replace `your_actual_groq_api_key_here` with your actual Groq API key.

### 4. Start the Application

```bash
# Start the backend server
python main.py
```

The API will be available at `http://localhost:8000`

### 5. Launch the Frontend

Open `index.html` in your web browser, or use a local server:

```bash
# Option 1: Direct file access
# Simply open index.html in your browser

# Option 2: Local server (recommended)
python -m http.server 3000
# Then open http://localhost:3000
```

## How to Use

1. **Launch the application** by opening the web interface
2. **Grant microphone access** when prompted by your browser
3. **Click "Start Recording"** to begin voice interaction
4. **Speak clearly** into your microphone
5. **Click "Stop Recording"** when finished speaking
6. **Wait for processing** - the AI will transcribe, respond, and play back audio
7. **Continue the conversation** by repeating the process

## System Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Browser   │───▶│   FastAPI   │───▶│   Whisper   │───▶│    Groq     │
│  (WebRTC)   │    │  (Backend)  │    │   (STT)     │    │    (LLM)    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       ▲                   │                   │                   │
       │                   ▼                   ▼                   ▼
       │            ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       └────────────│    gTTS     │◀───│  Response   │◀───│  Processing │
                    │   (TTS)     │    │  Generation │    │   Logic     │
                    └─────────────┘    └─────────────┘    └─────────────┘
```

## Project Structure

```
voice-bot/
├── main.py              # FastAPI backend server
├── index.html           # Frontend web interface
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Technical Details

- **Whisper Model**: Uses "base" model for optimal speed/accuracy balance
- **Response Limit**: 150 tokens for faster processing
- **Audio Format**: WebM with Opus codec for browser compatibility
- **Conversation Memory**: Maintains last 10 exchanges for context
- **CORS**: Configured for cross-origin requests
- **Error Handling**: Comprehensive error catching and user feedback