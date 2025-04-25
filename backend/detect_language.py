from langdetect import detect, DetectorFactory, LangDetectException
import logging
import re

# Configure logging
logger = logging.getLogger(__name__)

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Map of common language codes
LANGUAGE_MAP = {
    # Common misdetections
    'id': 'hi',  # Indonesian often misdetected for Hindi
    'ms': 'hi',  # Malay often misdetected for Hindi
    'tl': 'en',  # Tagalog often misdetected for English
    # Default languages to support
    'hi': 'hi',  # Hindi
    'en': 'en',  # English
    'fr': 'fr',  # French
    'es': 'es',  # Spanish
    'de': 'de',  # German
}

# Default language if detection fails
DEFAULT_LANGUAGE = 'en'

def contains_hindi_characters(text):
    """Check if text contains Hindi characters (Unicode range)"""
    # Unicode range for Hindi (Devanagari)
    hindi_pattern = re.compile(r'[\u0900-\u097F]')
    return bool(hindi_pattern.search(text))

def detect_language(text):
    try:
        if not text or not isinstance(text, str):
            logger.error("Invalid input text")
            return DEFAULT_LANGUAGE
            
        # First check for Hindi characters
        if contains_hindi_characters(text):
            logger.info("Detected Hindi characters in text")
            return 'hi'
            
        # Then try language detection
        detected_lang = detect(text)
        
        # Map to supported languages
        mapped_lang = LANGUAGE_MAP.get(detected_lang, DEFAULT_LANGUAGE)
        
        # If detected language is not in our map, use English
        if mapped_lang != detected_lang:
            logger.info(f"Mapped detected language {detected_lang} to {mapped_lang}")
        
        logger.info(f"Detected Language: {mapped_lang}")
        return mapped_lang
        
    except LangDetectException as e:
        logger.error(f"Language detection exception: {str(e)}")
        return DEFAULT_LANGUAGE
    except Exception as e:
        logger.error(f"Error in language detection: {str(e)}")
        return DEFAULT_LANGUAGE
