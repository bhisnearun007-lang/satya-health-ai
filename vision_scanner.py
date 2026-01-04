import os
from google import genai
from google.genai import types
from PIL import Image

# 1. SETUP CLIENT
# Make sure your API Key is set in your environment or paste it here for testing
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

# 2. THE VISION BRAIN
system_instruction = """
ROLE: Food Label OCR Specialist.
GOAL: Extract the 'Ingredients List' text from food packaging images.

RULES:
1. LOOK HARD: The ingredients are often in small print, curved, or on the back. Find them.
2. EXTRACT VERBATIM: Do not summarize. Copy every single word, comma, and bracket exactly as seen.
3. IGNORE NOISE: Ignore "Nutrition Facts" (Calories, Protein), Barcodes, and Marketing claims ("Healthy!", "Zero Fat").
4. CLEANUP: Return only the ingredient text string. Do not say "Here is the text". Just give the text.
5. IF UNCLEAR: If the image is too blurry to read, return: "ERROR: Image too blurry. Please try again."
"""

def scan_image_for_ingredients(image_path_or_bytes):
    print(f"\n--- 👁️ Vision Scanner: Analyzing image... ---")
    
    try:
        # We need to handle the image format for the API
        # Using the PIL library to open the image to ensure it's valid
        if isinstance(image_path_or_bytes, str):
            img = Image.open(image_path_or_bytes)
        else:
            img = Image.open(image_path_or_bytes)

        # Call Gemini Vision Model
        response = client.models.generate_content(
            model='gemini-3-flash', # Flash is excellent and fast for vision
            contents=[
                system_instruction, # The instruction
                img # The actual image data
            ],
            config=types.GenerateContentConfig(
                temperature=0.1 # Low creativity = high accuracy
            )
        )
        
        extracted_text = response.text.strip()
        print(f">> Extracted Text: {extracted_text[:50]}...") # Print first 50 chars
        return extracted_text

    except Exception as e:
        print(f"Vision Error: {e}")
        return "Error: Could not read image. Ensure it is clear and contains text."

# --- TEST ZONE ---
if __name__ == "__main__":
    # To test this, put a real image named 'test_label.jpg' in your folder
    # run: python3 vision_scanner.py
    if os.path.exists("test_label.jpg"):
        print(scan_image_for_ingredients("test_label.jpg"))
    else:
        print("Please add a 'test_label.jpg' file to test this script.")