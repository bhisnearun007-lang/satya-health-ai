# --- IMPORT THE TEAM ---
from ingestion_agent import run_ingestion_agent 
from normalizer_agent import run_agent as run_normalizer
from celiac_agent import run_celiac_agent
from metabolic_agent import run_metabolic_agent
from allergen_agent import run_allergen_agent
from additive_agent import run_additive_agent
from trust_agent import run_trust_agent
from critique_agent import run_critique_agent

def guardian_orchestrator(user_input, user_profile):
    print(f"\n🛡️  GUARDIAN ACTIVATED for User: {user_profile}")
    
    # STEP 1: INGESTION
    print(">> 📡 Guardian: Calling Ingestion Agent...")
    ingestion_result = run_ingestion_agent(user_input)
    ingredients_text = ingestion_result['content']
    
    # --- CRITICAL SAFETY CHECK ---
    # If vision failed, stop here. Don't waste money analyzing nothing.
    if "ERROR_VISION_FAILED" in ingredients_text or len(ingredients_text) < 5:
        return {
            "final_message": "⚠️ Error: The image could not be read. It might be blurry or the AI model is currently unavailable. Please try typing the ingredients manually.",
            "swarm_data": {},
            "normalized_data": {"ingredients": []},
            "critique_report": None
        }

    print(f">> 📝 Extracted Data: {ingredients_text[:50]}...")

    # STEP 2: NORMALIZATION
    print(">> 🧠 Guardian: Normalizing for Indian Context...")
    normalized_data = run_normalizer(ingredients_text)

    # STEP 3: SWARM ATTACK
    print(">> 🚑 Guardian: Deploying Specialist Swarm...")
    swarm_results = {}
    
    # Only run agents if relevant to user profile
    if any(k in user_profile for k in ["Celiac", "Gluten", "Wheat"]):
        swarm_results["celiac"] = run_celiac_agent(normalized_data)
        
    if any(k in user_profile for k in ["Diabetes", "BP", "Sugar", "Insulin"]):
        swarm_results["metabolic"] = run_metabolic_agent(normalized_data)

    if any(k in user_profile for k in ["Lactose", "Nut", "Soy", "Allergy", "Allergies"]):
        swarm_results["allergen"] = run_allergen_agent(normalized_data)
        
    # Always run Additive check
    swarm_results["additive"] = run_additive_agent(normalized_data)

    # STEP 4: SYNTHESIS
    print(">> ✍️  Guardian: Trust Agent is drafting report...")
    draft_response = run_trust_agent(user_profile, swarm_results)
    
    print(">> ⚖️  Guardian: Critique Agent is reviewing...")
    final_verdict = run_critique_agent(user_profile, normalized_data, draft_response)
    
    display_message = draft_response
    if final_verdict and "improved_response" in final_verdict:
        display_message = final_verdict["improved_response"]
        
    return {
        "final_message": display_message,
        "critique_report": final_verdict,
        "swarm_data": swarm_results,
        "normalized_data": normalized_data
    }