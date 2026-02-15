
import requests
import base64
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

MODEL = "gemini-2.5-flash" 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def get_response(message, screenshot_path=None, page_source=None):
    parts = [{"text": message}]
    
    if page_source:
        parts.append({"text": f"Page Source:\n{page_source[:15000]}..."})
        
    if screenshot_path and os.path.exists(screenshot_path):
        try:
            with open(screenshot_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            mime_type = "image/png"
            if screenshot_path.lower().endswith(('.jpg', '.jpeg')):
                mime_type = "image/jpeg"
                
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_data
                }
            })
        except Exception as e:
            print(f"Warning: Failed to process screenshot: {e}")

    payload = {
        "contents": [{
            "parts": parts
        }]
    }

    headers = {'Content-Type': 'application/json'}
    
    max_retries = 3
    retry_delay = 30
    
    for attempt in range(max_retries):
        try:
            response = requests.post(URL, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                result = response.json()
                # Parse the response safely
                try:
                    return result['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError) as e:
                    return f"Error parsing AI response: {result}"
            
            elif response.status_code == 429 or "RESOURCE_EXHAUSTED" in response.text:
                print(f"Quota exceeded (Attempt {attempt + 1}/{max_retries}). Waiting {retry_delay}s before retrying...")
                time.sleep(retry_delay)
            else:
                 print(f"API Error ({response.status_code}): {response.text}")
                 # For non-retriable errors, maybe break or continue?
                 # If it's a 4xx error (other than 429), it might be permanent.
                 if response.status_code >= 400 and response.status_code < 500:
                     return f"API Error: {response.text}"
                 time.sleep(5) # Wait a bit for other errors
                 
        except Exception as e:
             print(f"Request failed: {e}")
             time.sleep(5)

    return "AI Request Failed after retries."