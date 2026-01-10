from google import genai
from google.genai import types
import json

# SETUP
import os
# We tell the code to look for a secret variable named "GEMINI_API_KEY"
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

system_instruction = """
ROLE: Additive & Chemical Safety Agent.
GOAL: Flag inflammatory oils, preservatives, and artificial chemicals.

KNOWLEDGE BASE:
1. INFLAMMATORY OILS (The "Bad Fats"):
   - Palm Oil (Palmolein), Cottonseed Oil, Soybean Oil, Hydrogenated Vegetable Fat (Dalda/Vanaspati).

2. GUT IRRITANTS (IBS Triggers):
   - Carrageenan, Gum Arabic, Xanthan Gum (in high amounts), Sorbitol/Maltitol (Gas/Bloating).

3. ARTIFICIAL CHEMICALS:
   - MSG (E621), Sodium Benzoate, Artificial Colors (Red 40, Yellow 5), TBHQ.

OUTPUT FORMAT (JSON):
{
  "verdict": "CLEAN_LABEL" | "HIGHLY_PROCESSED",
  "bad_additives": ["Palm Oil", "E621"],
  "health_impact": "Contains inflammatory fats and gut irritants."
}
"""

def run_additive_agent(normalized_data):
    print(f"   [+ Swarm] 🧪 Additive Agent analyzing...")
    
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