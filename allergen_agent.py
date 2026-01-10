from google import genai
from google.genai import types
import json

# SETUP
import os
# We tell the code to look for a secret variable named "GEMINI_API_KEY"
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

system_instruction = """
ROLE: Major Allergen Detective.
GOAL: Identify sources of Milk, Soy, Nuts, Peanuts, Egg, and Fish.

KNOWLEDGE BASE:
1. MILK / LACTOSE:
   - Obvious: Milk Solids, Milk Powder, Cheese, Butter, Ghee.
   - Hidden: Casein, Whey, Lactose, Curd Powder, Cream.
   
2. SOY:
   - Obvious: Soy Flour, Tofu, Soya Chunks.
   - Hidden: Lecithin (E322), Vegetable Protein (HVP), Edible Vegetable Oil (often Soy).

3. NUTS / PEANUTS:
   - Obvious: Cashew, Almond, Peanut, Groundnut.
   - Hidden: Marzipan, Praline, Nut Paste, Hydrolyzed Peanut Protein.

OUTPUT FORMAT (JSON):
{
  "verdict": "SAFE" | "UNSAFE",
  "detected_allergens": ["Milk", "Soy"],
  "reasoning": "Contains Whey Protein (Milk Derivative).",
  "contamination_warning": "Check label for 'Manufactured in facility' warning."
}
"""

def run_allergen_agent(normalized_data):
    print(f"   [+ Swarm] 🥜 Allergen Agent analyzing...")
    
    prompt = f"ANALYZE INGREDIENTS: {json.dumps(normalized_data)}"
    
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.0
            )
        )
        return json.loads(response.text)
    except Exception as e:
        return {"verdict": "ERROR", "reasoning": str(e)}