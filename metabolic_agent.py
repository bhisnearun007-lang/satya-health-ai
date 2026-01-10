from google import genai
from google.genai import types
import json
import os

# SETUP
import os
# We tell the code to look for a secret variable named "GEMINI_API_KEY"
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

system_instruction = """
ROLE: Metabolic Health Specialist (Diabetes & Hypertension).
GOAL: Identify ingredients that spike Blood Sugar (Glycemic Index) or Blood Pressure (Sodium).

KNOWLEDGE BASE:
1. DIABETES TRIGGERS (High Risk):
   - Sugars: Sugar, Sucrose, Jaggery, Honey, High Fructose Corn Syrup (HFCS).
   - Hidden Sugars: Maltodextrin, Dextrose, Barley Malt.
   - High GI Carbs: Rice Flour, Potato Starch, Corn Starch, Maida.
   
2. DIABETES SAFE (Low Risk):
   - Sweeteners: Stevia, Erythritol, Monk Fruit, Maltitol (Safe but laxative warning).
   - Flours: Almond Flour, Coconut Flour, Chickpea Flour (Besan).

3. HYPERTENSION TRIGGERS (Salt):
   - Direct: Salt, Rock Salt.
   - Hidden Sodium: Baking Soda, Sodium Benzoate, Monosodium Glutamate (MSG).

OUTPUT FORMAT (JSON):
{
  "verdict": "SAFE" | "UNSAFE" | "MODERATE_RISK",
  "risky_ingredients": ["Sugar", "Maltodextrin"],
  "reasoning": "Contains high GI ingredients that will spike insulin.",
  "diabetes_friendly": boolean,
  "hypertension_friendly": boolean
}
"""

def run_metabolic_agent(normalized_data):
    print(f"   [+ Swarm] 🩸 Metabolic Agent analyzing...")
    
    prompt = f"ANALYZE INGREDIENTS: {json.dumps(normalized_data)}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
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

# TEST
if __name__ == "__main__":
    test_data = {"ingredients": [{"scientific_name": "Maltodextrin"}, {"scientific_name": "Stevia"}]}
    print(run_metabolic_agent(test_data))