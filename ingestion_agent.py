import os
import re
from google import genai
from google.genai import types
from PIL import Image
import io

# --- CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

# --- THE VISION BRAIN ---
VISION_INSTRUCTION = """
ROLE: Food Label OCR Specialist.
GOAL: Extract the 'Ingredients List' text from food packaging images.

RULES:
1. LOOK HARD: The ingredients are often in small print, curved, or on the back. Find them.
2. EXTRACT VERBATIM: Copy every word exactly.
3. IGNORE NOISE: Ignore Nutrition Facts, Barcodes, and Marketing.
4. CLEANUP: Return ONLY the ingredient text string.
5. IF UNCLEAR: Return "ERROR: Image too blurry."
"""

def _scan_image(image_input):
    print(f"\n--- 👁️ Vision Scanner: Processing Image... ---")
    try:
        # Load image (Handles both file paths and memory bytes)
        if isinstance(image_input, str):
            img = Image.open(image_input)
        else:
            img = Image.open(image_input)

        response = client.models.generate_content(
            model='gemini-2.5-flash', # <--- FIXED: Using stable model
            contents=[VISION_INSTRUCTION, img],
            config=types.GenerateContentConfig(temperature=0.1)
        )
        
        extracted_text = response.text.strip()
        print(f">> Extracted Text: {extracted_text[:50]}...") 
        return extracted_text

    except Exception as e:
        print(f"Vision Error: {e}")
        # Return a simplified error so Guardian can catch it
        return "ERROR_VISION_FAILED"

def run_ingestion_agent(user_input):
    print(f"\n--- 📡 Ingestion Agent Receiving Input... ---")

    # CASE 1: INPUT IS NOT A STRING (It's a File/Bytes from Streamlit)
    if not isinstance(user_input, str):
        print(">> Type Detected: Image File Object")
        extracted_text = _scan_image(user_input)
        return {"type": "PROCESSED_IMAGE", "content": extracted_text}

    cleaned_input = user_input.strip()

    # CASE 2: INPUT IS A URL STRING
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if url_pattern.match(cleaned_input):
        print(">> Type Detected: URL")
        return {"type": "URL", "content": cleaned_input}

    # CASE 3: INPUT IS AN IMAGE FILE PATH
    if cleaned_input.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        print(">> Type Detected: Image File Path")
        extracted_text = _scan_image(cleaned_input)
        return {"type": "PROCESSED_IMAGE", "content": extracted_text}

    # CASE 4: INPUT IS RAW TEXT
    print(">> Type Detected: Manual Text")
    return {"type": "TEXT", "content": cleaned_input}