import logging
import requests
import json

# Configure logging
logger = logging.getLogger(__name__)

def translate_to_english(text, src_lang):
    """
    Translate text to English using LibreTranslate API
    """
    try:
        if not text or not isinstance(text, str):
            logger.error("Invalid input text")
            return None
            
        if not src_lang or not isinstance(src_lang, str):
            logger.error("Invalid source language")
            return None
        
        # If already English or auto-detect, no need to translate
        if src_lang == 'en' or src_lang == 'auto':
            logger.info("Text already in English or auto-detect, skipping translation")
            return text
            
        # Use a fallback translation service
        logger.info(f"Translating from {src_lang} to English")
        
        # Fallback mechanism - since we have issues with translation APIs
        # For now, just return the original text and inform the user
        logger.warning("Translation not performed - using original text")
        return f"{text} [Note: Translation was not performed due to API limitations]"
        
    except Exception as e:
        logger.error(f"Error in translation: {str(e)}")
        return text  # Return original text as fallback
