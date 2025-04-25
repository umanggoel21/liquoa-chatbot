from listen import listen
from detect_language import detect_language
from translate import translate_to_english
from groq_chat import ask_groq
from translate_back import translate_back_to_user
from speak import speak
import logging
import os
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Supported languages for direct Groq response (no translation needed)
DIRECT_RESPONSE_LANGS = ['en', 'hi']

def main():
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists("output"):
            os.makedirs("output")
            
        # Step 1: Listen for voice
        logger.info("Listening for voice input...")
        text = listen()
        if not text:
            logger.warning("No text detected or error in listening")
            speak("I didn't hear anything. Please try again.", "en")
            return
        
        # Step 2: Detect language
        logger.info("Detecting language...")
        lang = detect_language(text)
        if not lang:
            logger.error("Failed to detect language")
            speak("I couldn't detect the language. Please try again in a common language.", "en")
            return
            
        # Display detected language
        lang_names = {
            'en': 'English',
            'hi': 'Hindi',
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German'
        }
        lang_name = lang_names.get(lang, lang)
        print(f"Detected language: {lang_name} ({lang})")
        
        # Check if we need translation or can respond directly
        need_translation = lang not in DIRECT_RESPONSE_LANGS
        
        if need_translation:
            # Step 3: Translate to English
            logger.info(f"Translating from {lang} to English...")
            english_text = translate_to_english(text, lang)
            if not english_text:
                logger.error("Translation to English failed")
                # Try again with auto-detection
                logger.info("Trying again with auto-detection...")
                english_text = translate_to_english(text, "auto")
                if not english_text:
                    speak("I couldn't translate your message. Please try again.", "en")
                    return
                    
            # Print what the user said in English
            print(f"You said (in English): {english_text}")
            
            # Step 4: Get Groq response in English
            logger.info("Getting response from Groq in English...")
            groq_reply = ask_groq(english_text, lang='en')
            
            # Step 5: Translate back to user's language
            logger.info(f"Translating response back to {lang}...")
            final_reply = translate_back_to_user(groq_reply, lang)
            if not final_reply:
                logger.error("Translation back to user's language failed")
                # If translation fails, use the English response
                logger.info("Using English response instead")
                final_reply = groq_reply
                lang = 'en'  # Fall back to English for speech
        else:
            # No translation needed - direct response in the user's language
            logger.info(f"Getting direct response from Groq in {lang_name}...")
            # Print what the user said in their original language
            print(f"You said (in {lang_name}): {text}")
            # Get response directly in the user's language
            final_reply = ask_groq(text, lang=lang)
        
        # Print Groq's response
        print(f"Groq says (in {lang_names.get(lang, lang)}): {final_reply}")
        
        # Step 6: Speak the final response
        logger.info(f"Speaking the response in {lang}...")
        success = speak(final_reply, lang)
        if not success:
            # If speaking in the detected language fails, try English
            logger.warning(f"Failed to speak in {lang}, trying English...")
            speak("I had trouble speaking in your language. Here's my response in English.", "en")
        
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        print("\nProgram interrupted. Exiting...")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
        # Try to speak the error message
        try:
            speak("I encountered an error. Please try again.", "en")
        except:
            pass
    finally:
        logger.info("Program execution completed")

if __name__ == "__main__":
    logger.info("Starting the application...")
    
    # Set up retry logic for the main loop
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            main()
            # Ask if the user wants to continue
            print("\nDo you want to ask another question? (yes/no)")
            choice = input().strip().lower()
            if choice != "yes" and choice != "y":
                print("Thank you for using the application. Goodbye!")
                break
        except Exception as e:
            logger.error(f"Main loop error: {str(e)}")
            retry_count += 1
            if retry_count < max_retries:
                logger.info(f"Retrying... ({retry_count}/{max_retries})")
                time.sleep(1)
            else:
                logger.error("Too many errors. Exiting.")
                print("Too many errors occurred. Please restart the application.")
                break
