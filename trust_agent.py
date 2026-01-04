from google import genai
from google.genai import types
import json

# [1] Setup Client
import os
# We tell the code to look for a secret variable named "GEMINI_API_KEY"
API_KEY = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

# [2] The Brain: The Communication Expert
system_instruction = """
ROLE:
You are the "Trust Agent" for Satya-Health. 
Your goal is to synthesize technical findings from multiple medical specialist agents into a single, CLEAR, EMPATHETIC, and ACTIONABLE response for the user.

INPUT:
1. User Health Profile (e.g., "Diabetic + Celiac")
2. Specialist Verdicts (A list of JSON outputs from the Swarm)

YOUR LOGIC (The "Hierarchy of Safety"):
1. THE RED FLAG RULE: If ANY specialist says "UNSAFE", the overall product is UNSAFE. Do not sugarcoat it.
2. CONFLICT RESOLUTION: If the Gluten Agent says "Safe" but the Diabetes Agent says "High Sugar", you must say: "This is safe for your Celiac disease, BUT it is risky for your Diabetes."
3. TONE: Be like a helpful, knowledgeable friend. Not a robot. Use emojis for visual cues (🛑, ⚠️, ✅).

OUTPUT FORMAT:
Return a plain text string (the final draft message). Do not return JSON. Write exactly what the user should read.
"""

def run_trust_agent(user_profile, swarm_results):
    print(f"\n--- ✍️ Trust Agent is drafting the response... ---")
    
    # We flatten the swarm results into a string for the AI to read
    swarm_text = json.dumps(swarm_results, indent=2)
    
    complex_input = f"""
    USER PROFILE: {user_profile}
    
    FINDINGS FROM SPECIALISTS:
    {swarm_text}
    
    TASK: Write the final response for this user.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3-pro',
            contents=complex_input,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7 # Higher temp allows for better, more natural writing
            )
        )
        
        print("\n[DRAFT RESPONSE]:")
        print(response.text)
        return response.text
        
    except Exception as e:
        print(f"Error: {e}")
        return "System Error: Could not generate response."

# --- TEST ZONE ---
if __name__ == "__main__":
    # Simulated data from the other agents (Mocking the inputs)
    
    mock_profile = "Type 2 Diabetes + Lactose Intolerance"
    
    mock_swarm_results = {
        "celiac_agent": {"verdict": "SAFE", "reason": "No gluten detected."},
        "diabetes_agent": {"verdict": "UNSAFE", "reason": "Contains 15g Added Sugar per serving."},
        "allergen_agent": {"verdict": "SAFE", "reason": "No dairy found."}
    }
    
    run_trust_agent(mock_profile, mock_swarm_results)