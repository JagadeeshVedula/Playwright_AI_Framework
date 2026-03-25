
# Import the requests library to make HTTP API calls
import requests
# Import base64 module to encode image files into text format for the API
import base64
# Import os module for accessing environment variables and file system operations
import os
# Import time module for adding delays (sleep) between retry attempts
import time
# Import json module for converting Python dictionaries to JSON strings
import json
# Import load_dotenv to load environment variables from a .env file
from dotenv import load_dotenv

# Load environment variables from the .env file into the system
load_dotenv()

# Read the Gemini API key from the environment variables
API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key was found in the environment
if not API_KEY:
    # If no API key was found, raise an error and stop execution
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Set the AI model name to use for generating responses
MODEL = "gemini-2.5-flash" 
# Build the full API endpoint URL using the model name and API key
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# Define a function that sends a message (with optional screenshot and page source) to the AI and returns its response
def get_response(message, screenshot_path=None, page_source=None):
    # Start building the list of content parts with the text message
    parts = [{"text": message}]
    
    # Check if page source HTML was provided
    if page_source:
        # Add the page source to the parts list, trimmed to the first 15,000 characters to stay within limits
        parts.append({"text": f"Page Source:\n{page_source[:15000]}..."})
        
    # Check if a screenshot path was provided and the file actually exists on disk
    if screenshot_path and os.path.exists(screenshot_path):
        # Try to read and encode the screenshot image
        try:
            # Open the screenshot file in binary read mode
            with open(screenshot_path, "rb") as image_file:
                # Read the image file and convert it to a base64-encoded string
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Set the default image type to PNG
            mime_type = "image/png"
            # Check if the file extension indicates it's a JPEG image instead
            if screenshot_path.lower().endswith(('.jpg', '.jpeg')):
                # If it's a JPEG, update the mime type accordingly
                mime_type = "image/jpeg"
                
            # Add the encoded image data to the parts list along with its file type
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_data
                }
            })
        # If something goes wrong while processing the screenshot, handle the error
        except Exception as e:
            # Print a warning but continue without the screenshot instead of crashing
            print(f"Warning: Failed to process screenshot: {e}")

    # Build the complete request payload (body) with all the content parts
    payload = {
        "contents": [{
            "parts": parts
        }]
    }

    # Set the HTTP headers to tell the API we're sending JSON data
    headers = {'Content-Type': 'application/json'}
    
    # Set the maximum number of times to retry if the request fails
    max_retries = 3
    # Set the number of seconds to wait between retries when rate-limited
    retry_delay = 30
    
    # Loop through each retry attempt
    for attempt in range(max_retries):
        # Try to make the API request
        try:
            # Send a POST request to the Gemini API with the headers and JSON payload
            response = requests.post(URL, headers=headers, data=json.dumps(payload))
            
            # Check if the API returned a successful response (status code 200)
            if response.status_code == 200:
                # Parse the JSON response body into a Python dictionary
                result = response.json()
                # Parse the response safely
                # Try to extract the AI-generated text from the nested response structure
                try:
                    # Navigate through the response JSON to get the actual text reply
                    return result['candidates'][0]['content']['parts'][0]['text']
                # If the expected keys or indices don't exist in the response
                except (KeyError, IndexError) as e:
                    # Return an error message with the raw response for debugging
                    return f"Error parsing AI response: {result}"
            
            # Check if the API returned a rate-limit error (too many requests)
            elif response.status_code == 429 or "RESOURCE_EXHAUSTED" in response.text:
                # Print a message showing which retry attempt this is and how long we'll wait
                print(f"Quota exceeded (Attempt {attempt + 1}/{max_retries}). Waiting {retry_delay}s before retrying...")
                # Pause execution for the retry delay period before trying again
                time.sleep(retry_delay)
            # Handle all other error status codes
            else:
                 # Print the error status code and response body for debugging
                 print(f"API Error ({response.status_code}): {response.text}")
                 # For non-retriable errors, maybe break or continue?
                 # If it's a 4xx error (other than 429), it might be permanent.
                 # Check if it's a client error (400-499) which usually means the request itself is wrong
                 if response.status_code >= 400 and response.status_code < 500:
                     # Return the error message since client errors won't be fixed by retrying
                     return f"API Error: {response.text}"
                 # Wait 5 seconds before retrying for server errors (5xx)
                 time.sleep(5) # Wait a bit for other errors
                 
        # If the request itself fails (network error, connection timeout, etc.)
        except Exception as e:
             # Print the error message for debugging
             print(f"Request failed: {e}")
             # Wait 5 seconds before retrying
             time.sleep(5)

    # If all retry attempts have been exhausted, return a failure message
    return "AI Request Failed after retries."