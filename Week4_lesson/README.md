# Voice Bot - Real-time Conversational AI

A simple real-time voice bot that captures audio from the browser, converts it to text using Whisper, generates responses with Groq LLM, and converts the response back to speech using gTTS.

## Features

- 🎤 Real-time audio capture from browser microphone
- 🗣️ Speech-to-Text using OpenAI Whisper
- 🤖 AI responses using Groq LLM
- 🔊 Text-to-Speech using Google TTS
- 🌐 Web-based interface with modern UI
- ⚡ FastAPI backend for processing

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/login and create an API key
3. Copy the API key

### 3. Configure Environment

Create a `.env` file in the project root:

```bash
# Copy the example file
cp env_example.txt .env

# Edit .env and add your Groq API key
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 4. Run the Backend

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 5. Open the Frontend

Open `index.html` in your web browser, or serve it using a simple HTTP server:

```bash
# Using Python's built-in server
python -m http.server 3000

# Then open http://localhost:3000
```

## Usage

1. Open the web interface
2. Click "Start Recording"
3. Allow microphone access when prompted
4. Speak your message
5. Click "Stop Recording"
6. Wait for the AI response to be played back

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /process-audio` - Process audio file and return AI response

## Architecture

```
Browser (WebRTC) → FastAPI → Whisper (STT) → Groq (LLM) → gTTS (TTS) → Browser
```

## Troubleshooting

### Microphone Access Issues
- Ensure your browser has microphone permissions
- Try refreshing the page and allowing access again

### API Key Issues
- Verify your Groq API key is correct in the `.env` file
- Check the `/health` endpoint to see if Groq is configured

### Audio Processing Issues
- Check the browser console for error messages
- Ensure the backend is running on port 8000
- Verify all dependencies are installed correctly

## Development

The project is structured as:
- `main.py` - FastAPI backend with all processing logic
- `index.html` - Frontend with WebRTC audio capture
- `requirements.txt` - Python dependencies
- `env_example.txt` - Environment variables template

## Notes

- First run will download the Whisper model (~140MB)
- Audio is processed in real-time but may have slight delays
- The system uses the "base" Whisper model for good balance of speed/accuracy
- Responses are limited to 150 tokens for faster processing
