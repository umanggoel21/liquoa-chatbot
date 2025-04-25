import streamlit as st
import os
import base64
import sys
import logging
import time
import uuid
from datetime import datetime
import glob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to the path so Python can find the modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import dependencies
try:
    from detect_language import detect_language
    from groq_chat import process_chat
    from translate import translate_to_english
    from translate_back import translate_back_to_user
    from speak import speak
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Setup page config
st.set_page_config(
    page_title="Lynqo AI Chat",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'audio_files' not in st.session_state:
    st.session_state.audio_files = {}
if 'audio_enabled' not in st.session_state:
    st.session_state.audio_enabled = True

# Directory for audio files
output_dir = os.path.join(os.getcwd(), "output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to autoplay audio
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# Function to create a play button for saved audio
def get_audio_player(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            return f"""
                <audio controls style="width:100%; margin-top:12px; height:40px;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
    except Exception as e:
        logger.error(f"Error creating audio player: {str(e)}")
        return ""

# Custom CSS for Google-like UI
st.markdown("""
<style>
    /* Google-inspired fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Overall app styling */
    .main {
        background-color: #f8f9fa;
        font-family: 'Roboto', sans-serif;
        color: #202124;
    }
    
    /* Header styling */
    .main-header {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
    }
    
    .logo {
        display: flex;
        align-items: center;
        margin-right: 10px;
    }
    
    .logo-text {
        font-size: 22px;
        font-weight: 500;
        color: #202124;
        margin-left: 8px;
    }
    
    .logo-icon {
        background: linear-gradient(135deg, #4285F4, #0F9D58, #F4B400, #DB4437);
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
    }
    
    /* Chat container */
    .chat-container {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        margin-bottom: 20px;
    }
    
    /* Messages styling */
    .stChatMessage {
        padding: 0.5rem !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
    }
    
    .stChatMessage [data-testid="StyledAvatar"] {
        width: 38px !important;
        height: 38px !important;
    }
    
    /* User message styling */
    .stChatMessageContent {
        background-color: #f1f3f4 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
    }
    
    /* AI message styling */
    [data-testid="chat-message-content"]:has([data-testid="avatarIcon-assistant"]) {
        background-color: #0d2473 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    [data-testid="chat-message-content"]:has([data-testid="avatarIcon-assistant"]) p {
        color: white !important;
    }
    
    /* Audio player styling */
    audio {
        border-radius: 20px !important;
    }
    
    /* Footer styling */
    .footer {
        margin-top: 30px;
        text-align: center;
        color: #5f6368;
        font-size: 0.8rem;
        padding: 10px;
        border-top: 1px solid #dadce0;
    }
    
    /* Sidebar styling */
    .css-1544g2n {
        background-color: #f8f9fa !important;
    }
    
    /* Chat input styling */
    .stChatInputContainer {
        padding: 10px !important;
        background-color: white !important;
        border-radius: 24px !important;
        border: 1px solid #dadce0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Caption styling */
    .caption-container {
        display: flex;
        align-items: center;
        margin-top: 6px;
        font-size: 0.8rem;
        color: #5f6368;
    }
    
    .language-badge {
        background-color: #e8f0fe;
        color: #1a73e8;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        margin-right: 8px;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
        border: none !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #1765cc !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.24) !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom header
st.markdown("""
<div class="main-header">
    <div class="logo">
        <div class="logo-icon">🤖</div>
        <div class="logo-text">Lynqo AI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Language names mapping
lang_names = {
    'en': 'English',
    'hi': 'हिंदी',
    'es': 'Español', 
    'fr': 'Français',
    'de': 'Deutsch', 
    'zh-cn': '中文',
    'ja': '日本語', 
    'ko': '한국어',
    'pt': 'Português', 
    'it': 'Italiano',
    'ru': 'Русский',
    'ar': 'العربية'
}

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    with st.container():
        # Message content
        st.markdown(f"""
        <div class="chat-message {message['role']}">
            <div class="language-label">
                {lang_names.get(message['language'], message['language'])}
            </div>
            <div class="chat-text">
                {message['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # If this is an assistant message and has associated audio, show the player
        if message['role'] == 'assistant' and str(i) in st.session_state.audio_files:
            audio_path = st.session_state.audio_files[str(i)]
            if os.path.exists(audio_path):
                st.markdown(get_audio_player(audio_path), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    
    # Audio settings
    st.session_state.audio_enabled = st.checkbox("Enable audio responses", value=st.session_state.audio_enabled)
    
    # About section
    st.markdown("---")
    st.subheader("About")
    st.markdown("""
    **Lynqo AI Chat** is a multilingual assistant powered by Groq AI.
    
    - Understands multiple languages
    - Provides audio responses
    - Simple and easy to use
    """)
    
    st.markdown("---")
    st.markdown("© 2025 Lynqo")

# Chat input
user_input = st.chat_input("Type a message in any language...")

# Process user input
if user_input:
    # Clean up old audio files if too many
    if len(st.session_state.audio_files) > 10:
        # Get files that aren't in the current chat history
        current_files = set(st.session_state.audio_files.values())
        all_files = set(glob.glob(os.path.join(output_dir, "*.mp3")))
        to_delete = all_files - current_files
        
        # Delete unused files
        for file_path in to_delete:
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up unused audio file: {file_path}")
            except Exception as e:
                logger.error(f"Error cleaning up audio file: {str(e)}")
    
    # Add user message to chat history
    detected_lang = detect_language(user_input)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "language": detected_lang
    })
    
    # Display user message
    with st.container():
        st.markdown(f"""
        <div class="chat-message user">
            <div class="language-label">
                {lang_names.get(detected_lang, detected_lang)}
            </div>
            <div class="chat-text">
                {user_input}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create a placeholder for the AI response
    response_placeholder = st.empty()
    
    # Show a spinner while processing
    with st.spinner("Thinking..."):
        # Translate to English if needed
        english_message = translate_to_english(user_input, detected_lang)
        
        # Get AI response
        ai_response = process_chat(english_message, detected_lang)
        
        # Translate response back if needed
        final_response = translate_back_to_user(ai_response, detected_lang)
    
    # Add AI response to chat history
    message_index = len(st.session_state.messages)
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_response,
        "language": detected_lang
    })
    
    # Display AI response
    with st.container():
        st.markdown(f"""
        <div class="chat-message assistant">
            <div class="language-label">
                {lang_names.get(detected_lang, detected_lang)}
            </div>
            <div class="chat-text">
                {final_response}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate and play audio if enabled
    if st.session_state.audio_enabled:
        with st.spinner("Generating audio..."):
            # Generate the audio file
            speak_success = speak(final_response, detected_lang)
            
            if speak_success:
                # Find the latest audio file
                audio_files = [f for f in os.listdir(output_dir) if f.endswith('.mp3')]
                if audio_files:
                    latest_file = max(audio_files, key=lambda x: os.path.getmtime(os.path.join(output_dir, x)))
                    latest_file_path = os.path.join(output_dir, latest_file)
                    
                    # Store in session state with message index as key
                    st.session_state.audio_files[str(message_index)] = latest_file_path
                    
                    # Display the audio player with better error handling
                    audio_html = get_audio_player(latest_file_path)
                    if audio_html:
                        st.markdown(audio_html, unsafe_allow_html=True)
                    else:
                        st.warning("Could not load audio player. Please try again.")

# Controls
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Clear Chat", use_container_width=True):
        # Delete all audio files
        for audio_path in st.session_state.audio_files.values():
            if os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except Exception as e:
                    logger.warning(f"Error removing audio file: {str(e)}")
        
        # Clear session state
        st.session_state.messages = []
        st.session_state.audio_files = {}
        st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>Lynqo AI Chat • Breaking language barriers with artificial intelligence</p>
</div>
""", unsafe_allow_html=True) 