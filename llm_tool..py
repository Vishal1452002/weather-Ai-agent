# Fixed code
import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Setup basic logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Load .env file to get API key
load_dotenv()

# Retrieve the Gemini API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

# Validate that the API key is present
if not api_key:
    # Raise a clear error if the API key is missing, indicating a configuration issue
    raise ValueError("ERROR: GEMINI_API_KEY not found in .env file. Please ensure it's set.")

# For debugging purposes, print that the key is loaded (this can be removed in production)
print("DEBUG GEMINI KEY LOADED: ...") # Masking the actual key for security

# Configure the Google Generative AI library with the API key
try:
    genai.configure(api_key=api_key)
except Exception as e:
    # Log any configuration errors and re-raise to halt execution if configuration fails
    logging.error(f"Failed to configure Google Generative AI: {e}")
    raise

# Define the model name to be used for content generation.
# This model is a lightweight and fast option.
MODEL_NAME = "gemini-2.5-flash-lite"
# Alternatively, for a more powerful model: MODEL_NAME = "models/gemini-pro-latest"

def generate_response(context: str) -> str:
    """
    Generates a rewritten weather summary in a friendly, simple tone using a Gemini model.

    Args:
        context: A string containing the weather information to be rewritten.

    Returns:
        A string containing the rewritten weather summary, or an error message
        if generation fails.
    """
    # Construct the prompt for the Gemini model.
    # The prompt instructs the model on how to rewrite the weather info,
    # specifying constraints to avoid analysis, restricted content, and claims
    # about geography or political regions.
    prompt = f"""
Rewrite the following weather details in a friendly, simple tone.
Do NOT analyze location or provide restricted content.
Do NOT make claims about geography or political regions.
Just restate the weather information clearly.

WEATHER INFO:
{context}
"""
    try:
        # Instantiate the generative model
        model = genai.GenerativeModel(MODEL_NAME)
        # Generate content based on the constructed prompt
        response = model.generate_content(prompt)
        # Return the generated text, stripping any leading/trailing whitespace
        return response.text.strip()

    except Exception as e:
        # If any error occurs during content generation (e.g., API issues, model errors),
        # log the error for debugging and return a user-friendly error message.
        logging.error(f"Error generating content with Gemini model '{MODEL_NAME}': {e}")
        return f"[LLM ERROR] An issue occurred while processing your request. Please try again later."

# Example of how to use the function (this part is for demonstration and can be removed)
if __name__ == "__main__":
    sample_weather_info = "The temperature is currently 25 degrees Celsius with clear skies. Winds are light from the west at 10 km/h. There is a 0% chance of precipitation."
    try:
        friendly_weather = generate_response(sample_weather_info)
        print("Original Weather Info:")
        print(sample_weather_info)
        print("\nFriendly Weather Summary:")
        print(friendly_weather)
    except ValueError as ve:
        print(ve)
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

    # Example of a potential error scenario (e.g., if API key was invalid and configure failed)
    # To simulate this, you'd need to intentionally break the API key or configuration.
    # In a real app, you'd rely on the raised exceptions from genai.configure or model.generate_content.