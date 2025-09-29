from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import whisper
import groq
import tempfile
import os
import io
import base64
from collections import deque
from gtts import gTTS
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Voice Bot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

whisper_model = whisper.load_model("base")
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = groq.Groq(api_key=groq_api_key)
conversation_history = deque(maxlen=10)

@app.get("/")
async def root():
    return {"message": "Voice Bot API is running"}

@app.post("/process-audio")
async def process_audio(audio_file: UploadFile = File(...)):
    try:
        content_type = audio_file.content_type or ""
        if "webm" in content_type or "ogg" in content_type:
            suffix = ".webm"
        else:
            suffix = ".wav"
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        #Speech-to-Text using Whisper
        result = whisper_model.transcribe(temp_file_path)
        user_text = result["text"].strip()

        if not user_text:
            response_text = "I didn't hear anything. Please try speaking again..."
        else:
            if not groq_client:
                raise HTTPException(status_code=500, detail="Groq API key not configured")

            system_prompt = {
                "role": "system",
                "content": (
                    "You are a real-time voice AI assistant. "
                    "Respond in short, natural, conversational sentences with a little touch of gen-z language. "
                    "Avoid long or complex explanations unless the user explicitly asks. "
                    "Speak in a friendly, clear tone as if chatting face-to-face. "
                    "If the user interrupts or changes topic, adapt smoothly. "
                    "Keep answers under 3 sentences unless detail is requested."
                )
            }

            messages = [system_prompt] + list(conversation_history) + [
                {"role": "user", "content": user_text}
            ]

            chat_completion = groq_client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant",
                max_tokens=150,
                temperature=0.7
            )

            response_text = chat_completion.choices[0].message.content

            conversation_history.append({"role": "user", "content": user_text})
            conversation_history.append({"role": "assistant", "content": response_text})
        
        #Text-to-Speech using gTTS
        tts = gTTS(text=response_text, lang='en', slow=False)
        
        # audio buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert audio to base64 for JSON response
        audio_data = audio_buffer.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        # return both transcription and audio data
        return JSONResponse({
            "user_transcription": user_text,
            "bot_response": response_text,
            "audio_data": audio_base64
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
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