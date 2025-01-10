# School Infobot Streaming Tools

## Prompt

!!! prompt
     We are a group of software engineers that would like to get high-school
     students exposed to AI and LLMs.  We would like to build a mobile robot that will wonder the halls of schools and be able to interact with students via voice.  We have a brand new Raspberry Pi with an AI Hat that can do model inference faster than before.  The Raspberry Pi has a high-quality 360-degree mic and speakers.  We also have a wireless connection to a school's GPU which is a NVIDIA GTX 3080Ti with 12GB of  RAM.  It is running Ollama now.  Our team has a preference for Python.

    Here are the goals of the project:

    1. The robot will "listed" to a student and convert their speech to text.
    2. Text will be sent to the GPU running Ollama/Llama 3.3 which has a systems prompt that only allows it to answer questions about the school.
    3. The text comes out of Ollama/Llama 3.3 and must be converted to speech.
    4. The speech is sent back to the Robot and it is played to the speaker.

    What tools should I use to connect all these components together with a streaming interface?

## Response

Below is a high-level overview of how you can stitch all the components together for a real-time (i.e., "streaming") pipeline, along with recommended tools for each step. The approach will let your Raspberry Pi (with its AI Hat) continuously capture audio, convert speech to text, send text to Ollama/Llama running on the remote GPU, receive the response, convert it to speech, and then play it back in near real time.


### 1. Audio Capture and Streaming from the Raspberry Pi

**Tools and libraries:**

1.  **PyAudio (Python) or PortAudio (C/C++).**

    -   PyAudio is a popular Python wrapper for PortAudio, making it easy to capture audio from the mic in real time.

2.  **GStreamer**

If you want a lower-level pipeline approach (especially for complex audio routing or if you need to handle multiple input/output devices or audio filters), GStreamer provides a powerful framework with built-in elements for streaming audio over the network.

For example, you can capture audio from the Pi's 360-degree microphone and stream it out via a network protocol like RTP or TCP/UDP.

3.  **ROS (Robot Operating System) -- optional**

If your robot is already running ROS2, you could publish audio data to a topic and subscribe to it elsewhere. ROS2 can handle real-time communication via DDS. This might be overkill if you are not using ROS for other parts of your robot, but it's worth considering if you're building a larger robotics stack.

In many simpler cases, PyAudio plus a small Python script is enough to capture short audio segments (or continuous chunks) and feed them to your STT engine.

### 2. Speech-to-Text (STT)

**Local vs. Remote STT:**

-   If your new AI Hat can handle on-device STT with a lightweight model (like Vosk or Whisper on the Pi), that might be simplest.
-   Alternatively, you can stream raw audio data over the network to a remote GPU server (e.g., running NVIDIA Riva, DeepSpeech, or Whisper with GPU acceleration). However, this introduces more network complexity.

**Recommended approach:**

-   **Local STT with Vosk or Whisper** on the Pi, especially if your AI Hat can handle real-time inference. This avoids sending a constant stream of raw audio over the network.
-   If you do prefer streaming STT from the Pi to the remote GPU, you can use **gRPC streaming** or **WebSocket** connections (depending on which STT service you choose).

### 3. Sending Text to Ollama/Llama on the Remote GPU

Your recognized text then needs to be sent to the remote server (running Ollama / Llama 3.3 on the NVIDIA GTX 3080 Ti).

**Tools and libraries to connect to Ollama/Llama:**

1.  **HTTP/REST API (with streaming)**

    -   Ollama often provides a local REST/HTTP API. You can send requests (the student's question) and receive streaming responses from Llama 3.3.
    -   If it supports SSE (Server-Sent Events) or chunked transfer encoding, you can process partial responses in real time.

2.  **WebSocket**

If you want to implement your own streaming, you could stand up a small WebSocket server around Ollama. This is a bit more custom but allows you to send partial text to Llama, get partial responses back, and maintain an ongoing conversation state.

3.  **gRPC**

If Ollama supports or can be wrapped with a gRPC server, you could build a streaming gRPC endpoint.

**Recommended approach:**

Most out-of-the-box Ollama installations expose a local HTTP API that supports streaming tokens as they're generated. You can forward your text to that API, capture the streaming response in Python, and pass it on to the next step (TTS).

4. Text-to-Speech (TTS)

Once you receive text back from Llama, you need to turn it into speech. This can either happen locally on the Pi's AI Hat or on the remote server (and then streamed back). Often, TTS is relatively lightweight, so local TTS is common if you have a decent model (e.g., a smaller Coqui TTS or espeak).

**Tools and libraries:**

1.  **Local TTS Engines**

    -   **Coqui TTS:** Python-based, has numerous models with different footprints.
    -   **eSpeak / Festival:** Classic TTS solutions, fairly small footprints, though the quality is not as good as modern neural TTS.
    -   **Flite (Festival Lite):** Minimally sized TTS engine, but robotic-sounding.
2.  **Remote TTS**

    -   If you want a higher-fidelity, neural TTS model that needs the GPU, you can run something like NVIDIA Riva TTS, Coqui TTS, or another neural TTS on the GPU.
    -   Stream the raw audio or PCM frames back to the Pi over a socket or through gRPC.

### Recommended Approach

-   **Local neural TTS** on the Pi, if the AI Hat can handle real-time TTS. This avoids constant audio streaming from the remote server.
-   If the Pi cannot handle it, implement a streaming TTS server on the GPU with gRPC or WebSocket and send back a real-time audio stream to the Pi for playback.

5. Playback on the Raspberry Pi Speaker

Finally, the synthesized audio must be played on the Pi's speakers.

**Tools and libraries for audio playback:**

-   **PyAudio** or **PortAudio** for playback.
-   **GStreamer** can also handle audio output with something like the `alsasink` element on Raspberry Pi.
-   **SDL** or other audio libraries if you want more advanced features.

6. Recommended "Glue" for Streaming Architecture


Putting this all together, you essentially have two major "pipeline" paths:

1.  **Speech Input → STT → Send text to Llama (via HTTP/WS) → Receive text from Llama → TTS → Play Audio**
2.  **Control signals** and any advanced event handling (for example, handling partial transcripts or partial Llama responses).

Here are some good ways to implement the streaming "glue":

### A. **Python + Async I/O + WebSockets/gRPC**

-   **Asyncio** in Python can handle concurrent tasks---recording audio, sending requests to STT or Llama, receiving streaming responses, then passing them to TTS.
-   For a custom approach, you can implement streaming with **websockets** or **gRPC** in Python.
-   Example:
    1.  Use `PyAudio` to capture raw audio frames.
    2.  Send frames to STT (locally or remote) in a streaming manner.
    3.  As soon as partial text is available, forward it to Llama.
    4.  Llama starts streaming tokens back.
    5.  As tokens are received, feed them into TTS for partial audio generation.
    6.  Play partial audio on the speaker.

### B. **GStreamer Pipelines + HTTP/REST for Llama**

-   Use GStreamer to manage audio capture from mic and playback to speaker.
-   For the STT → Llama → TTS text steps, wrap them in a small Python (or Node.js) service that uses an HTTP request to talk to the Llama server (which can stream via SSE).
-   As text arrives from Llama, hand it off to your TTS pipeline in GStreamer.
-   GStreamer can be quite powerful but has a steeper learning curve if you're not already using it.

### C. **ROS 2 if you're a robotics-heavy stack**

-   If the robot is already using ROS 2 for navigation, sensor data, etc., you can publish/subscribe audio streams, STT results, TTS requests, etc.
-   Then a separate node can talk to Ollama over HTTP or a custom service.
-   This is a more modular approach but again, heavier if all you need is a simple pipeline.

#### Example Minimal Flow with Python Async

Below is a simplified, conceptual outline using Python async and websockets (assuming local STT and TTS on the Pi, plus a remote Ollama server that offers a streaming HTTP SSE endpoint):

```python
import asyncio
import websockets
import requests

async def audio_capture_stt():
    """
    Continuously capture audio from mic, run STT (local or remote).
    As soon as partial transcripts are ready, yield them.
    """
    while True:
        # Capture audio frames from PyAudio
        # Send frames to local STT or use local inference (Vosk/Whisper).
        # If partial transcript is ready, yield it.
        yield partial_transcript

async def ask_ollama(question):
    """
    Send `question` to remote Ollama (HTTP SSE).
    Yield partial responses (tokens) as they arrive.
    """
    # SSE or chunked transfer from Ollama
    response_stream = requests.get("http://GPU_SERVER:PORT/generate", stream=True)
    for chunk in response_stream.iter_content(chunk_size=None):
        yield chunk  # partial text token from Llama

async def text_to_speech_playback(text_chunk):
    """
    Convert text_chunk to speech (e.g. local Coqui TTS) and play immediately.
    """
    # local TTS
    audio_data = coqui_generate_audio(text_chunk)
    # Play with PyAudio or GStreamer sink
    play_audio(audio_data)

async def main():
    async for partial_text in audio_capture_stt():
        # Once a partial or final transcript is ready,
        # send it to the remote Llama server.
        async for partial_llama_answer in ask_ollama(partial_text):
            # As text arrives, TTS and play
            await text_to_speech_playback(partial_llama_answer)

if __name__ == "__main__":
    asyncio.run(main())

```

This architecture ensures minimal latency because everything is happening in a streaming manner:

-   Audio capture to STT doesn't block.
-   Llama's partial tokens are processed as they come in.
-   TTS is played back as the text is generated.

## Summary of Recommended Tools

1.  **For Audio Capture and Playback**:

    -   PyAudio (simple), GStreamer (more complex, more powerful).
2.  **For STT**:

    -   **Local**: Vosk / Whisper (possibly utilizing your AI Hat for acceleration).
    -   **Remote**: NVIDIA Riva, DeepSpeech, or a custom gRPC-based STT solution.
3.  **For Connection to Ollama/Llama 3.3**:

    -   HTTP-based streaming (SSE or chunked responses) or a custom WebSocket/gRPC wrapper if needed.
4.  **For TTS**:

    -   **Local**: Coqui TTS, eSpeak, Festival, or any neural TTS engine that can run on the Pi's AI Hat.
    -   **Remote**: Coqui TTS or NVIDIA Riva TTS on the GPU, streaming PCM data back.
5.  **For Orchestration**:

    -   Python with **asyncio** + **websockets** / **requests** for streaming.
    -   Or GStreamer pipelines for audio + Python for handling Llama queries.
    -   Or a ROS 2 approach if you need deep robotics integration.

With these pieces in place, you'll have a real-time pipeline where the Raspberry Pi captures audio, converts it to text, sends the text to Llama on the GPU, receives back a streaming text response, converts that response to speech, and plays it back to the student.

## Workflow

ChatGPT thought about it for 17 seconds.

**Creating the interaction experience**

I'm designing a pipeline for a mobile robot: speech to text on Raspberry Pi, text transformation for Ollama, and text to speech. Streaming interface options include WebSocket, gRPC, GStreamer, and ffmpeg for real-time audio transmission.

**Evaluating options**

I'm weighing Vosk, Google's TTS, Coqui TTS, espeak, NVIDIA's Riva, and cloud solutions for streaming STT to the GPU with Ollama. The Raspberry Pi's roles in audio capture and local or GPU-based processing are also considered.

**Crafting the strategy**

I'm mapping out the pipeline: real-time audio capture on Raspberry Pi, streaming STT to GPU with Ollama, and streaming text to speech for playback. WebSockets or gRPC are solutions I'm considering for data exchange.

**Mapping data flow**

I'm integrating the Raspberry Pi with PyAudio for mic audio, using a speech recognition service, and streaming text to the GPU server for Ollama's text generation, followed by TTS on the Pi or GPU.

**Integrating tools**

I'm pulling together GStreamer, WebSockets, gRPC, Docker, and containerization for streaming audio from the GPU server to the Raspberry Pi, ensuring smooth playback.

**Integrating solutions**

I'm steering towards using PyAudio or SoX for audio capture, streaming STT via Vosk or Google Speech, and passing text to Ollama through REST or WebSocket. For TTS, exploring eSpeak, gTTS, or Coqui TTS.