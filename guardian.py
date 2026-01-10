# --- IMPORT THE TEAM ---
from input_router import route_user_input
from vision_scanner import scan_image_for_ingredients

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


def guardian_orchestrator(user_input, user_profile):
    print(f"\n🛡️  GUARDIAN ACTIVATED for User: {user_profile}")
    
    # ====================================================
    # STEP 1: ROUTING & INGESTION (The Senses)
    # ====================================================
    routed_data = route_user_input(user_input)
    
    input_type = routed_data['type']
    raw_content = routed_data['content']
    
    print(f">> 🚦 Route Selected: {input_type} | Action: {routed_data['action']}")
    
    # Ingestion Logic: Convert everything to "Clean Text"
    ingredients_text = ""
    
    if input_type == "URL":
        print("   [+ Tool] Web Scraper running... (Simulated)")
        # Real code: ingredients_text = scrape_url(raw_content)
        ingredients_text = "Whole Wheat Flour, Sugar, Palmolein Oil, Malt Extract, E621"
        
    elif input_type in ["IMAGE_FILE", "PDF_DOCUMENT"]:
        print(f"   [+ Tool] 👁️ Vision Scanner activating for {raw_content}...")

    # REAL CALL to the Vision Agent
    # Note: raw_content is the file path or bytes passed from App.py
    ingredients_text = scan_image_for_ingredients(raw_content)

    # Fallback if vision fails
    if "Error" in ingredients_text or len(ingredients_text) < 5:
         ingredients_text = "Error: No ingredients detected. Please type manually."
        
    elif input_type == "BARCODE":
        print(f"   [+ Tool] Database Lookup for UPC {raw_content}... (Simulated)")
        # Real code: ingredients_text = openfoodfacts.get(raw_content)
        ingredients_text = "Corn Starch, Potato Starch, Rice Flour, Guar Gum"
        
    elif input_type in ["INGREDIENT_LIST", "USER_QUERY"]:
        ingredients_text = raw_content
        
    print(f">> 📝 Extracted Data: {ingredients_text}")

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