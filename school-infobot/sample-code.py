
# raspberry_pi/main.py
import asyncio
import websockets
import sounddevice as sd
import numpy as np
from whisper_cpp import Whisper

class RobotClient:
    def __init__(self):
        self.whisper = Whisper("base.en")
        self.sample_rate = 16000
        self.ws = None

    async def process_audio_stream(self, indata, frames, time, status):
        if status:
            print(status)
        
        # Process audio chunk with Whisper
        text = self.whisper.transcribe(indata)
        if text.strip():
            # Send to server
            await self.ws.send(text)

    async def start_streaming(self):
        self.ws = await websockets.connect('ws://gpu-server:8000/chat')
        
        # Start audio streaming
        with sd.InputStream(callback=self.process_audio_stream,
                          channels=1,
                          samplerate=self.sample_rate):
            while True:
                # Receive audio response from server
                audio_data = await self.ws.recv()
                # Play audio
                sd.play(audio_data, self.sample_rate)
                sd.wait()

# gpu_server/main.py
from fastapi import FastAPI, WebSocket
from TTS.api import TTS
import ollama
import asyncio

app = FastAPI()
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        # Receive text from robot
        text = await websocket.receive_text()
        
        # Stream to Ollama
        response_stream = ollama.chat(
            model='llama2:13b',
            messages=[{'role': 'user', 'content': text}],
            stream=True
        )
        
        full_response = ""
        for chunk in response_stream:
            full_response += chunk['message']['content']
            
        # Convert to speech
        audio = tts.tts(full_response)
        
        # Send audio back to robot
        await websocket.send_bytes(audio)

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)