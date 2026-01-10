from google import genai
from google.genai import types
import json

# [1] Setup Client
import os
# We tell the code to look for a secret variable named "GEMINI_API_KEY"
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

# [2] The Brain: Deep Medical Knowledge for Celiac
# Notice how specific the rules are. This is "Prompt Engineering" for safety.
system_instruction = """
ROLE:
You are the "Celiac Safety Specialist Agent".
Your GOAL is to detect ANY source of Gluten in a list of normalized ingredients.

KNOWLEDGE BASE (The "Red List"):
1. DIRECT GLUTEN: Wheat, Barley, Rye, Triticale, Spelt, Kamut, Farro.
2. HIDDEN GLUTEN: Malt (from Barley), Brewer's Yeast, Seitan, Hydrolyzed Wheat Protein.
3. HIGH RISK (India Context):
   - "Oats" are UNSAFE unless explicitly labeled "Gluten Free" (high cross-contamination risk in Indian mills).
   - "Hing" (Asafoetida) is UNSAFE unless labeled "Gluten Free" (usually mixed with Maida).
   - "Starch" is RISKY if source is not specified (could be Wheat starch).

YOUR TASK:
Analyze the input JSON. Output a strict safety verdict.

OUTPUT FORMAT (JSON):
{
  "verdict": "SAFE" | "UNSAFE" | "RISKY_NEEDS_VERIFICATION",
  "flagged_ingredients": ["Malt", "Oats"],
  "reasoning": "Product contains Malt (Barley derivative) and standard Oats.",
  "consumer_message": "Write a short, simple warning for the user."
}
"""

def run_celiac_agent(normalized_data):
    print(f"\n--- 🧬 Analyzing for Celiac Risks... ---")
    
    # We feed the agent the clean data from the previous step
    prompt_content = f"""
    ANALYZE THIS STANDARDIZED DATA:
    {json.dumps(normalized_data)}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt_content,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.0 # Zero creativity. We want facts only.
            )
        )
        
        # Parse and Print
        result = json.loads(response.text)
        print(json.dumps(result, indent=2))
        return result
        
    except Exception as e:
        print(f"Error: {e}")

# --- TEST ZONE ---
# Here we simulate the output coming from Agent 1 (The Normalizer)
if __name__ == "__main__":
    
    # TEST CASE 1: The "Healthy" Cookie (That is actually deadly)
    # Marketing says "Multi-Grain", but Normalizer found Malt.
    mock_normalized_input = {
        "ingredients": [
            {"scientific_name": "Sorghum Flour", "category": "grain"}, # Safe (Jowar)
            {"scientific_name": "Barley Malt Extract", "category": "sweetener"}, # DEADLY
            {"scientific_name": "Palm Oil", "category": "fat"} # Safe for Celiac
        ]
    }
    
    print("Test 1: Analyzing 'Healthy' Malt Cookie...")
    run_celiac_agent(mock_normalized_input)

    print("\n" + "="*30 + "\n")

    # TEST CASE 2: The "Tricky" Indian Snack
    # Contains "Oats" which are theoretically GF, but risky in India.
    mock_oats_input = {
        "ingredients": [
            {"scientific_name": "Rolled Oats", "category": "grain"},
            {"scientific_name": "Chia Seeds", "category": "seed"}
        ]
    }
    
    print("Test 2: Analyzing Generic Oats...")
    run_celiac_agent(mock_oats_input)