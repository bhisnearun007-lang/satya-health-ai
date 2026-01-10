import os
import re
from google import genai
from google.genai import types
from PIL import Image
import io

# --- CONFIGURATION ---
# Ensure your API key is set in your environment variables
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

# --- THE VISION BRAIN (System Instruction) ---
VISION_INSTRUCTION = """
ROLE: Food Label OCR Specialist.
GOAL: Extract the 'Ingredients List' text from food packaging images.

RULES:
1. LOOK HARD: The ingredients are often in small print, curved, or on the back. Find them.
2. EXTRACT VERBATIM: Do not summarize. Copy every single word, comma, and bracket exactly as seen.
3. IGNORE NOISE: Ignore "Nutrition Facts" (Calories, Protein), Barcodes, and Marketing claims ("Healthy!", "Zero Fat").
4. CLEANUP: Return only the ingredient text string. Do not say "Here is the text". Just give the text.
5. IF UNCLEAR: If the image is too blurry to read, return: "ERROR: Image too blurry. Please try again."
"""

# --- HELPER FUNCTION: THE VISION SCANNER ---
def _scan_image(image_input):
    """
    Private helper function to send image to Gemini Vision.
    Accepts: File path (str) OR Byte Stream (from Streamlit)
    """
    print(f"\n--- 👁️ Vision Scanner: Processing Image... ---")
    try:
        # Load image (Handles both file paths and memory bytes)
        if isinstance(image_input, str):
            img = Image.open(image_input)
        else:
            # If it's bytes/buffer from Streamlit
            img = Image.open(image_input)

        response = client.models.generate_content(
            model='gemini-3-pro-preview', # Using gemini-3-flash-preview if pro dosent work
            contents=[VISION_INSTRUCTION, img],
            config=types.GenerateContentConfig(temperature=0.1)
        )
        
        extracted_text = response.text.strip()
        print(f">> Extracted Text: {extracted_text[:50]}...") 
        return extracted_text

    except Exception as e:
        print(f"Vision Error: {e}")
        return "Error: Could not read image."

# --- MAIN AGENT FUNCTION: THE ROUTER + PROCESSOR ---
def run_ingestion_agent(user_input):
    """
    The Single Entry Point.
    1. Detects input type (URL, Image, Text).
    2. If Image: Converting it to text immediately using Vision AI.
    3. If URL/Text: Formats it for the next agent.
    
    Returns: A dictionary with 'type', 'content' (processed), and 'source'.
    """
    print(f"\n--- 📡 Ingestion Agent Receiving Input... ---")

    # CASE 1: INPUT IS NOT A STRING (It's a File/Bytes from Streamlit)
    if not isinstance(user_input, str):
        print(">> Type Detected: Image File Object")
        extracted_text = _scan_image(user_input)
        return {
            "type": "PROCESSED_IMAGE",
            "content": extracted_text,
            "action": "Analysis Ready"
        }

    cleaned_input = user_input.strip()

    # CASE 2: INPUT IS A URL STRING
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if url_pattern.match(cleaned_input):
        print(">> Type Detected: URL")
        return {
            "type": "URL",
            "content": cleaned_input,
            "action": "Needs Web Scraper Tool" 
            # Note: You would add scraping logic here later if needed
        }

    # CASE 3: INPUT IS AN IMAGE FILE PATH STRING
    if cleaned_input.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        print(">> Type Detected: Image File Path")
        extracted_text = _scan_image(cleaned_input)
        return {
            "type": "PROCESSED_IMAGE",
            "content": extracted_text,
            "action": "Analysis Ready"
        }

    # CASE 4: INPUT IS RAW TEXT
    print(">> Type Detected: Manual Text")
    return {
        "type": "TEXT",
        "content": cleaned_input,
        "action": "Direct Processing"
    }

# --- TEST ZONE ---
if __name__ == "__main__":
    # Test 1: Text
    print(run_ingestion_agent("Sugar, Maida, Salt"))
    
    # Test 2: URL
    print(run_ingestion_agent("https://www.amazon.in/cookies"))
    
    # Test 3: Local Image (Make sure you have a file named 'test.jpg' to test this)
    if os.path.exists("test.jpg"):
        print(run_ingestion_agent("test.jpg"))