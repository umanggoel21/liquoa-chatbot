import logging
import requests
import json
import os
import time
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# List of Groq models to try in order
GROQ_MODELS = [
    "llama3-70b-8192",  # First choice
    "mixtral-8x7b-32768-instruct",  # Second choice
    "llama3-8b-8192"  # Fallback option
]

# Language-specific prompts
LANGUAGE_PROMPTS = {
    'en': "You are a helpful multilingual AI assistant. Provide clear, concise, and accurate responses in English.",
    'hi': "You are a helpful multilingual AI assistant. Provide clear, concise, and accurate responses in Hindi (use both Hindi and Roman script when appropriate). Make sure your Hindi is grammatically correct and natural sounding.",
    'default': "You are a helpful multilingual AI assistant. Provide clear, concise, and accurate responses."
}

def ask_groq(text, retry_count=2, lang='en'):
    """
    Send a request to Groq API and get a response.
    Will try multiple models if the first one fails.
    
    Args:
        text (str): The user's input
        retry_count (int): Number of retries if all models fail
        lang (str): The language code for response
    """
    try:
        if not text or not isinstance(text, str):
            logger.error("Invalid input text for Groq")
            return None
            
        # Get API key from environment variable
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            logger.error("GROQ_API_KEY not found in environment variables")
            return "I'm sorry, but I don't have access to the Groq API at the moment. Please check your API key."
        
        # Get the appropriate system prompt for the language
        system_prompt = LANGUAGE_PROMPTS.get(lang, LANGUAGE_PROMPTS['default'])
        
        # Add language-specific instructions
        if lang == 'hi':
            # Add specific instructions for Hindi
            text = f"{text}\n\nPlease respond in Hindi. Use a mix of Hindi script and Roman script where appropriate."
        
        # Try each model in sequence
        for model in GROQ_MODELS:
            try:
                logger.info(f"Trying Groq model: {model}")
                
                # Groq API endpoint
                url = "https://api.groq.com/openai/v1/chat/completions"
                
                # Headers
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                # Request body with system prompt
                data = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
                
                # Make the API request
                response = requests.post(url, headers=headers, json=data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    reply = result['choices'][0]['message']['content']
                    logger.info(f"Groq response success with model {model}")
                    return reply
                else:
                    error_details = response.json().get('error', {}).get('message', 'Unknown error')
                    logger.error(f"Groq API error with model {model}: {response.status_code} - {error_details}")
                    # Continue to next model
                    continue
                    
            except requests.exceptions.Timeout:
                logger.error(f"Timeout error with model {model}")
                continue
            except requests.exceptions.RequestException as e:
                logger.error(f"Request exception with model {model}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error with model {model}: {str(e)}")
                continue
        
        # If we've tried all models and none worked, try one more time after a delay
        if retry_count > 0:
            logger.info(f"All models failed. Retrying in 2 seconds. Retries left: {retry_count}")
            time.sleep(2)
            return ask_groq(text, retry_count - 1, lang)
        
        # All models failed after retries, return language-specific message
        logger.error("All Groq models failed after retries")
        if lang == 'hi':
            return "मुझे खेद है, मैं इस समय AI से जवाब नहीं ले पा रहा हूँ। कृपया बाद में पुनः प्रयास करें।"
        return "I'm sorry, but I couldn't get a response from the AI at this time. Please try again later."
            
    except Exception as e:
        logger.error(f"Error in Groq chat: {str(e)}")
        if lang == 'hi':
            return "क्षमा करें, आपके अनुरोध को संसाधित करते समय एक त्रुटि हुई।"
        return "I'm sorry, but an error occurred while processing your request."

def process_chat(message, lang='en'):
    """
    Process a chat message through the Groq API.
    This is a wrapper around the ask_groq function for easier use in the frontend and main application.
    
    Args:
        message (str): The user's message to process
        lang (str): The language code for the response
        
    Returns:
        str: The AI's response
    """
    try:
        if not message or not isinstance(message, str):
            logger.error("Invalid message for processing")
            return "I'm sorry, I couldn't process that message."
            
        # Process through Groq API
        response = ask_groq(message, retry_count=2, lang=lang)
        
        if not response:
            logger.error("Empty response from Groq API")
            return "I'm sorry, I couldn't generate a response. Please try again."
            
        return response
        
    except Exception as e:
        logger.error(f"Error in process_chat: {str(e)}")
        return "I apologize, but I encountered an error while processing your message."

