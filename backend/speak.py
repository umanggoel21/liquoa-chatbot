from gtts import gTTS
import os
import logging
import platform
import uuid
import subprocess
import time

# Configure logging
logger = logging.getLogger(__name__)

def speak(text, lang):
    try:
        if not text or not isinstance(text, str):
            logger.error("Invalid text for speech")
            return False
            
        if not lang or not isinstance(lang, str):
            logger.error("Invalid language code")
            return False
            
        # Map language codes to gTTS compatible codes if needed
        lang_map = {
            'zh-cn': 'zh-CN',
            'zh': 'zh-CN',
            'en': 'en',
            'hi': 'hi',
            'es': 'es',
            'fr': 'fr',
            'de': 'de',
            'ja': 'ja',
            'ko': 'ko',
            'pt': 'pt',
            'it': 'it',
            'ru': 'ru',
            'ar': 'ar'
        }
        
        # Get the correct language code or default to 'en'
        tts_lang = lang_map.get(lang.lower(), 'en')
        logger.info(f"Using TTS language code: {tts_lang} for requested language: {lang}")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Create a unique filename for this audio
        filename = f"response_{uuid.uuid4().hex[:8]}.mp3"
        audio_file = os.path.join(output_dir, filename)
        
        # Ensure the path is absolute and normalized
        audio_file = os.path.abspath(os.path.normpath(audio_file))
        
        # Log the text we're going to speak (for debugging)
        logger.info(f"Converting text to speech: '{text[:50]}...' (truncated)")
            
        # Create gTTS object with appropriate settings
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        
        # Save the audio file
        logger.info(f"Saving audio to: {audio_file}")
        tts.save(audio_file)
        
        # Verify the file exists and has content
        if not os.path.exists(audio_file):
            logger.error(f"Audio file not found after creation: {audio_file}")
            return False
            
        # Log file size for debugging
        file_size = os.path.getsize(audio_file)
        logger.info(f"Audio file size: {file_size} bytes")
        
        if file_size < 1000:  # If file is suspiciously small
            logger.warning(f"Audio file is very small ({file_size} bytes), may not contain speech")
        
        # Play the audio file based on the operating system
        system = platform.system()
        
        if system == "Windows":
            try:
                # On Windows, simplest and most reliable method is os.startfile
                logger.info(f"Playing audio with os.startfile: {audio_file}")
                os.startfile(audio_file)
                
                # Wait longer for audio to start playing
                time.sleep(3)
                logger.info("Audio playback initiated")
                return True
            except Exception as e:
                logger.error(f"Error playing audio with os.startfile: {str(e)}")
                try:
                    # Fallback to Windows Media Player COM automation
                    cmd = f'start /min wmplayer "{audio_file}"'
                    subprocess.run(cmd, shell=True, check=True)
                    time.sleep(3)
                    logger.info("Audio played using Windows Media Player")
                    return True
                except Exception as e2:
                    logger.error(f"Error playing audio with Windows Media Player: {str(e2)}")
                    return False
                
        elif system == "Darwin":  # macOS
            try:
                # Use afplay on macOS
                os.system(f"afplay '{audio_file}'")
                logger.info(f"Audio played using afplay")
                return True
            except Exception as e:
                logger.error(f"Error playing audio with afplay: {str(e)}")
                return False
                
        else:  # Linux and others
            try:
                # Use mpg123 on Linux
                os.system(f"mpg123 -q '{audio_file}'")
                logger.info(f"Audio played using mpg123")
                return True
            except Exception as e:
                logger.error(f"Error playing audio with mpg123: {str(e)}")
                return False
        
    except Exception as e:
        logger.error(f"Error in text-to-speech: {str(e)}")
        return False
