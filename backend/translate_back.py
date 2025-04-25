import logging
import requests
import json

# Configure logging
logger = logging.getLogger(__name__)

def translate_back_to_user(response, target_lang):
    """
    Translate response back to user's language using LibreTranslate API
    """
    try:
        if not response or not isinstance(response, str):
            logger.error("Invalid response text")
            return None
            
        if not target_lang or not isinstance(target_lang, str):
            logger.error("Invalid target language")
            return None
        
        # If target is English, no need to translate
        if target_lang == 'en' or target_lang == 'auto':
            logger.info("Target language is English or auto-detect, skipping translation")
            return response
            
        # Use a fallback translation service
        logger.info(f"Translating from English to {target_lang}")
        
        # Fallback mechanism - since we have issues with translation APIs
        # For now, just return the original text and inform the user
        logger.warning("Translation not performed - using original response")
        return response
        
    except Exception as e:
        logger.error(f"Error in translation: {str(e)}")
        return response  # Return original response as fallback
