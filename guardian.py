# --- IMPORT THE TEAM ---
from ingestion_agent import run_ingestion_agent 

# Import the Normalizer Agent as "run_normalizer"
from normalizer_agent import run_agent as run_normalizer

# The Specialists
from celiac_agent import run_celiac_agent
from metabolic_agent import run_metabolic_agent
from allergen_agent import run_allergen_agent
from additive_agent import run_additive_agent

# The Reviewers
from trust_agent import run_trust_agent
from critique_agent import run_critique_agent

# Import the routing function
from ingestion_agent import route_user_input


def guardian_orchestrator(user_input, user_profile):
    print(f"\n🛡️  GUARDIAN ACTIVATED for User: {user_profile}")
    
    # ====================================================
    # STEP 1: ROUTING & INGESTION (The Senses)
    # ====================================================
    print(">> 📡 Guardian: Calling Ingestion Agent...")
    
    ingestion_result = run_ingestion_agent(user_input)
    
    input_type = ingestion_result['type']
    ingredients_text = ingestion_result['content']
    
    print(f">> 🚦 Ingestion Complete: {input_type}")
    print(f">> 📝 Extracted Data: {ingredients_text[:50]}...") # Print first 50 chars only


    # ====================================================
    # STEP 2: NORMALIZATION (The Context)
    # ====================================================
    print(">> 🧠 Guardian: Normalizing for Indian Context...")
    
    normalized_data = run_normalizer(ingredients_text)
    
     # If the normalizer failed, handle it gracefully
    if not normalized_data or "ingredients" not in normalized_data:
        normalized_data = {"ingredients": []}


    # ====================================================
    # STEP 3: SWARM ATTACK (The Diagnosis)
    # ====================================================
    print(">> 🚑 Guardian: Deploying Specialist Swarm...")
    swarm_results = {}
    
    # LOGIC: Dynamic Activation
    # We save money/time by only calling agents relevant to the User's Profile
    
    # 1. Celiac Agent
    if any(keyword in user_profile for keyword in ["Celiac", "Gluten", "Wheat"]):
        swarm_results["celiac"] = run_celiac_agent(normalized_data)
        
    # 2. Metabolic Agent (Diabetes/BP)
    if any(keyword in user_profile for keyword in ["Diabetes", "BP", "Sugar", "Insulin"]):
        swarm_results["metabolic"] = run_metabolic_agent(normalized_data)

    # 3. Allergen Agent (Dairy/Nuts/Soy)
    if any(keyword in user_profile for keyword in ["Lactose", "Nut", "Soy", "Allergy"]):
        swarm_results["allergen"] = run_allergen_agent(normalized_data)
        
    # 4. Additive Agent (Always runs for general health)
    swarm_results["additive"] = run_additive_agent(normalized_data)

    # ====================================================
    # STEP 4: SYNTHESIS & SAFETY (The Verdict)
    # ====================================================
    print(">> ✍️  Guardian: Trust Agent is drafting report...")
    draft_response = run_trust_agent(user_profile, swarm_results)
    
    print(">> ⚖️  Guardian: Critique Agent (Dr. Satya) is reviewing...")
    final_verdict = run_critique_agent(user_profile, normalized_data, draft_response)
    
    # LOGIC: Decide what to show the user
    display_message = draft_response # Default
    
    if final_verdict and "improved_response" in final_verdict:
        # If Dr. Satya rewrote it, use that version
        display_message = final_verdict["improved_response"]
        
    # PACKAGING THE RETURN DATA FOR THE UI
    return {
        "final_message": display_message,
        "critique_report": final_verdict,
        "swarm_data": swarm_results,
        "normalized_data": normalized_data
    }