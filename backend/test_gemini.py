"""Quick test for Gemini API."""
import os
import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key found: {'Yes' if api_key else 'No'}")
print(f"API Key length: {len(api_key) if api_key else 0}")

if not api_key:
    print("ERROR: No API key found!")
    exit(1)

genai.configure(api_key=api_key)

print("\nListing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")

print("\nTrying to generate content with gemini-1.5-flash...")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say OK")
    print(f"SUCCESS! Response: {response.text}")
except Exception as e:
    print(f"Error with gemini-1.5-flash: {e}")
    
    print("\nTrying gemini-pro as fallback...")
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say OK")
        print(f"SUCCESS with gemini-pro! Response: {response.text}")
    except Exception as e2:
        print(f"Error with gemini-pro: {e2}")
