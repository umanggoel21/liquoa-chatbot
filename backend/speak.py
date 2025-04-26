from gtts import gTTS
import os
import logging
import platform
import uuid
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def speak(text, language='en'):
    """
    Convert text to speech using Google Text-to-Speech API
    
    Args:
        text (str): The text to convert to speech
        language (str): Language code (e.g., 'en' for English, 'es' for Spanish)
        
    Returns:
        str: Path to the saved audio file
    """
    try:
        logger.info(f"Converting text to speech: '{text}' in language '{language}'")
        
        # Create a unique filename for the audio
        filename = f"speech_{uuid.uuid4()}.mp3"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'audio', filename)
        
        # Ensure audio directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Create gTTS object
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Save the audio file
        tts.save(filepath)
        logger.info(f"Speech saved to {filepath}")
        
        # Play the audio file based on the operating system
        play_audio(filepath)
        
        return filepath
    
    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {str(e)}")
        return None

def play_audio(filepath):
    """
    Play the audio file using the appropriate command for the OS
    
    Args:
        filepath (str): Path to the audio file
    """
    try:
        system = platform.system()
        
        if system == 'Windows':
            os.startfile(filepath)
        elif system == 'Darwin':  # macOS
            os.system(f"afplay {filepath}")
        else:  # Linux and others
            os.system(f"mpg123 {filepath}")
            
        # Give some time for the audio to play
        time.sleep(0.5)
        
        logger.info(f"Playing audio: {filepath}")
    except Exception as e:
        logger.error(f"Error playing audio: {str(e)}")

if __name__ == "__main__":
    # Simple test
    speak("This is a test of the text to speech system", "en")
