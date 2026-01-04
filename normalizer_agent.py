# [1] Import the NEW library
from google import genai
from google.genai import types
import json
import os

# --- CONFIGURATION ---
# [2] Initialize the Client (The new "Connection")
import os
# We tell the code to look for a secret variable named "GEMINI_API_KEY"
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

# [3] Define the "Brain" (System Instruction)
system_instruction = """
ROLE:
You are the "Indian Context Normalizer Agent", a senior Food Safety Scientist specializing in Indian Retail Products. Your goal is to take messy, regional, or marketing-heavy ingredient lists and convert them into a strict, scientific Safety Object.

INPUT DATA:
You will receive text that may contain:
- Regional Hindi/Indian terms (e.g., "Maida", "Besan", "Khand").
- Ambiguous categories (e.g., "Edible Vegetable Oil").
- E-codes (e.g., "E621").

YOUR TASKS:
1. NORMALIZE: Convert all regional terms to their specific English scientific names.
   - "Maida" -> "Refined Wheat Flour"
   - "Rava/Sooji" -> "Semolina (Wheat)"
   - "Hing" -> "Asafoetida"
   - "Sendha Namak" -> "Rock Salt"

2. EXPAND HIDDEN INGREDIENTS (CRITICAL):
   - If you see "Hing" or "Asafoetida", you MUST list "Wheat Flour" as a hidden sub-ingredient unless the input explicitly says "Gluten Free Hing".
   - If you see "Margarine", add "Vegetable Fat" and "Milk Solids".
   - If you see "Soy Sauce", add "Wheat" and "Soy".

3. ASSESS RISK FLAGS:
   - Flag "High Glycemic Index" for sugars/starches.
   - Flag "Inflammatory" for processed oils (Palm/Cottonseed).
   - Flag "Allergen" for Wheat, Soy, Dairy, Nuts.

OUTPUT FORMAT:
Return ONLY a JSON object. Do not speak to the user.
{
  "normalized_ingredients": [
    {
      "original_term": "String",
      "scientific_name": "String",
      "risk_flags": ["String", "String"],
      "hidden_components": ["String"],
      "explanation": "Short reason for the flag"
    }
  ]
}
"""

def run_agent(ingredient_text):
    print(f"\n--- 🕵️‍♂️ Scanning: {ingredient_text} ---")
    
    # [4] Generate Content with Config Object
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Updated to a valid known model
            contents=f"INPUT TO ANALYZE: {ingredient_text}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json" # [Design Win] Enforces JSON mode natively!
            )
        )
        
        # [5] Parse Response
        # The new SDK handles JSON mode better, often returning pure JSON directly
        print(response.text) 
        
    except Exception as e:
        print(f"Error: {e}")

# --- TEST ZONE ---
if __name__ == "__main__":
    run_agent("Enriched unbleached flour (wheat flour, malted barley flour, ascorbic acid [dough conditioner], niacin, reduced iron, thiamin mononitrate, riboflavin, folic acid), sugar, degermed yellow cornmeal, salt, leavening (baking soda, sodium acid pyrophosphate), soybean oil, honey powder, natural flavor.)")
