import speech_recognition as sr
import logging
import time
import sys
import os

# Configure logging
logger = logging.getLogger(__name__)

# Attempt to load PyAudio - this is a common source of issues
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    logger.warning("PyAudio not found. Voice input will not be available.")
    logger.warning("To install PyAudio on Windows: pip install pipwin && pipwin install pyaudio")
    logger.warning("On Mac: pip install pyaudio")
    logger.warning("On Linux: sudo apt-get install python3-pyaudio")

def listen():
    """
    Listen for voice input and convert to text.
    Falls back to text input if voice recognition fails or PyAudio is not available.
    """
    # Check if PyAudio is available
    if not PYAUDIO_AVAILABLE:
        print("Voice input is not available. Please type your text:")
        text = input().strip()
        if text:
            logger.info(f"User typed: {text}")
            return text
        return None
    
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Set up microphone with automatic energy threshold
        try:
            with sr.Microphone() as source:
                logger.info("Adjusting for ambient noise...")
                # Longer adjustment for better accuracy
                recognizer.adjust_for_ambient_noise(source, duration=2)
                
                # Increase dynamic energy threshold for better detection
                recognizer.dynamic_energy_threshold = True
                recognizer.energy_threshold = 300  # Default is 300, increase if in noisy environment
                
                logger.info("Listening...")
                print("Say something clearly! (Press Ctrl+C to stop)")
                
                try:
                    # Increase timeout and phrase time for longer sentences
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
                    logger.info("Audio captured, processing...")
                except sr.WaitTimeoutError:
                    logger.warning("No speech detected within timeout")
                    print("No speech detected. Please try again or type your text:")
                    text = input().strip()
                    if text:
                        logger.info(f"User typed: {text}")
                        return text
                    return None
        except Exception as e:
            logger.error(f"Error accessing microphone: {str(e)}")
            print(f"Error accessing microphone: {str(e)}")
            print("Please type your text instead:")
            text = input().strip()
            if text:
                logger.info(f"User typed: {text}")
                return text
            return None
                
        try:
            # Try using multiple recognition services
            # First, try Google's recognizer (most reliable but requires internet)
            try:
                logger.info("Attempting Google speech recognition...")
                text = recognizer.recognize_google(audio)
                logger.info(f"Google recognized: {text}")
                return text
            except sr.UnknownValueError:
                logger.warning("Google could not understand audio")
                
                # Try Sphinx as fallback (offline, less accurate)
                try:
                    logger.info("Attempting Sphinx speech recognition...")
                    # Low confidence threshold for Sphinx
                    text = recognizer.recognize_sphinx(audio)
                    logger.info(f"Sphinx recognized: {text}")
                    return text
                except (sr.UnknownValueError, ImportError) as e:
                    logger.warning(f"Sphinx recognition failed: {str(e)}")
                    
                    # Last resort: ask for text input
                    print("Sorry, I couldn't understand what you said. Please type your text:")
                    text = input().strip()
                    if text:
                        logger.info(f"User typed: {text}")
                        return text
                    return None
                    
            except sr.RequestError as e:
                logger.error(f"Could not request results from Google Speech Recognition: {str(e)}")
                print("Network error. Please type your text:")
                text = input().strip()
                if text:
                    logger.info(f"User typed: {text}")
                    return text
                return None
                
        except Exception as e:
            logger.error(f"Speech recognition error: {str(e)}")
            print(f"Error: {str(e)}")
            print("Please type your text:")
            text = input().strip()
            if text:
                logger.info(f"User typed: {text}")
                return text
            return None
            
    except KeyboardInterrupt:
        logger.info("User interrupted listening")
        print("\nInterrupted. Please type your text:")
        text = input().strip()
        if text:
            logger.info(f"User typed: {text}")
            return text
        return None
        
    except Exception as e:
        logger.error(f"Error in speech recognition: {str(e)}")
        print(f"Error in speech recognition: {str(e)}")
        print("Please type your text:")
        text = input().strip()
        if text:
            logger.info(f"User typed: {text}")
            return text
        return None
