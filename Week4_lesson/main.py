from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import whisper
import groq
import tempfile
import os
import io
from gtts import gTTS
import uvicorn
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice Bot API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
whisper_model = None
groq_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global whisper_model, groq_client
    
    logger.info("Loading Whisper model...")
    whisper_model = whisper.load_model("base")
    
    # Initialize Groq client
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        logger.warning("GROQ_API_KEY not found in environment variables")
    else:
        groq_client = groq.Groq(api_key=groq_api_key)
        logger.info("Groq client initialized")

@app.get("/")
async def root():
    return {"message": "Voice Bot API is running"}

@app.post("/process-audio")
async def process_audio(audio_file: UploadFile = File(...)):
    """
    Process audio: STT -> LLM -> TTS
    """
    try:
        # Save uploaded audio to temporary file
        # Determine file extension based on content type
        content_type = audio_file.content_type or ""
        if "webm" in content_type or "ogg" in content_type:
            suffix = ".webm"
        else:
            suffix = ".wav"
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Step 1: Speech-to-Text using Whisper
        logger.info("Converting speech to text...")
        result = whisper_model.transcribe(temp_file_path)
        user_text = result["text"].strip()
        
        if not user_text:
            logger.warning("No speech detected in audio")
            # Return a friendly response instead of error
            response_text = "I didn't hear anything. Please try speaking again."
        else:
            # Step 2: Generate response using Groq LLM
            if not groq_client:
                raise HTTPException(status_code=500, detail="Groq API key not configured")
            
            logger.info("Generating LLM response...")
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Keep your responses conversational and concise, suitable for voice interaction."
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ],
                model="llama-3.1-8b-instant",
                max_tokens=150,
                temperature=0.7
            )
            
            response_text = chat_completion.choices[0].message.content
            logger.info(f"LLM response: {response_text}")
        
        # Step 3: Text-to-Speech using gTTS
        logger.info("Converting response to speech...")
        tts = gTTS(text=response_text, lang='en', slow=False)
        
        # Create audio buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        # Return audio stream
        return StreamingResponse(
            io.BytesIO(audio_buffer.read()),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=response.mp3"}
        )
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Error processing audio: {str(e)}")
        logger.error(f"Full traceback: {error_details}")
        # Clean up temporary file if it exists
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)} - {error_details}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "whisper_loaded": whisper_model is not None,
        "groq_configured": groq_client is not None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
