# Lynqo AI Assistant

<div align="center">
  <h3>Breaking language barriers with AI - Speak freely, connect globally</h3>
</div>

## Overview

Lynqo AI Assistant is a multilingual voice-enabled AI chatbot powered by Groq. It allows users to interact with AI in multiple languages through both text and voice, with responses delivered in the same language as the input.

## Current Features

- **Voice and Text Input**: Interact using voice (with automatic transcription) or text input
- **Real-time Language Detection**: Automatically identifies the user's language
- **Multilingual Support**: Works with 10+ languages including English, Hindi, Spanish, French, German, Chinese, Japanese, Russian, Arabic, and Portuguese
- **Text-to-Speech**: Generates spoken responses in the detected language
- **Streamlit Web Interface**: Clean, responsive UI for browser-based interaction
- **Command-line Interface**: Direct terminal-based interaction option

## Project Structure

```
Lynqo-chatbot/
├── backend/
│   ├── frontend.py            # Streamlit web interface
│   ├── main.py                # Command-line interface
│   ├── groq_chat.py           # Groq API integration
│   ├── listen.py              # Voice input processing
│   ├── speak.py               # Text-to-speech functionality
│   ├── detect_language.py     # Language detection
│   ├── translate.py           # Translation to English
│   ├── translate_back.py      # Translation to user's language
│   └── saved_audio/           # Directory for temporary audio files
├── output/                    # Generated audio output
├── assets/                    # Project assets and images
├── tests/                     # Unit and integration tests
└── requirements.txt           # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for API access)
- Microphone (for voice input)
- Speakers (for audio output)

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/username/Lynqo-chatbot.git
   cd Lynqo-chatbot
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file in the project root)
   ```
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

### Web Interface

1. Start the Streamlit application
   ```bash
   streamlit run backend/frontend.py
   ```

   If you see an error about port 8501 already being in use, you can specify a different port:
   ```bash
   streamlit run backend/frontend.py --server.port=8502
   ```
   
   You can also find and terminate the process using port 8501:
   - On Windows: `netstat -ano | findstr 8501` then `taskkill /PID <PID> /F`
   - On Mac/Linux: `lsof -i :8501` then `kill -9 <PID>`

2. Open your browser and navigate to `http://localhost:8501` (or the port you specified)

3. Type or speak your message in any supported language

4. The AI will respond in the same language, with both text and audio

### Command-line Interface

1. Run the main script
   ```bash
   python backend/main.py
   ```

2. Follow the prompts to speak or type your message

3. The AI will respond in the detected language

## Troubleshooting

### Audio Issues

- **No audio output**: Make sure your system's audio is working and not muted
- **Audio plays but no speech**: Check internet connection for TTS service access
- **Windows audio problems**: Try running the application as administrator

### Voice Recognition Issues

- **Voice input not working**: Ensure your microphone is properly connected and permitted
- **Poor transcription quality**: Speak clearly and reduce background noise
- **PyAudio errors**: Run `pip install pipwin && pipwin install pyaudio` on Windows

### Streamlit Issues

- **Port already in use**: Follow the instructions above to use a different port or terminate the blocking process
- **Browser doesn't open automatically**: Manually navigate to the URL shown in the terminal
- **Screen reader compatibility**: PowerShell might disable PSReadLine when screen readers are detected - run `Import-Module PSReadLine` to re-enable if needed

## Dependencies

Key libraries:
- **groq**: AI chat processing
- **gTTS**: Text-to-speech conversion
- **SpeechRecognition**: Voice input processing 
- **streamlit**: Web interface
- **langdetect**: Language detection
- **googletrans**: Translation services

## License

This project is open source and available under the MIT License.

---

Developed with ❤️ by the rohan and umang 
