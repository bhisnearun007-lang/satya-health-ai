import streamlit as st
import time
from guardian import guardian_orchestrator

# --- PAGE CONFIG (Mobile Friendly) ---
st.set_page_config(
    page_title="Satya Health",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 🎨 2025 "GLASS & BENTO" CSS ---
st.markdown("""
    <style>
    /* 1. RESET STREAMLIT DEFAULTS */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(248, 250, 252) 0%, rgb(241, 245, 249) 90%);
        font-family: 'Inter', sans-serif;
    }
    header, footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;} /* Force hide sidebar */
    
    /* 2. ONBOARDING CARDS (Apple Style) */
    .condition-card-active {
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        color: white;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        transition: all 0.2s;
    }
    .condition-card-inactive {
        background: white;
        color: #64748b;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: all 0.2s;
    }
    
    /* 3. VERDICT HERO */
    .hero-safe { background: #dcfce7; color: #14532d; border: 1px solid #86efac; border-radius: 20px; padding: 30px; text-align: center; }
    .hero-danger { background: #fee2e2; color: #7f1d1d; border: 1px solid #fca5a5; border-radius: 20px; padding: 30px; text-align: center; }
    .hero-warning { background: #fef3c7; color: #78350f; border: 1px solid #fcd34d; border-radius: 20px; padding: 30px; text-align: center; }
    
    /* 4. DETAILS BENTO */
    .bento-box {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE (Memory) ---
if 'page' not in st.session_state: st.session_state.page = 'onboarding'
if 'profile' not in st.session_state: 
    st.session_state.profile = {"Celiac": False, "Diabetes": False, "Lactose": False, "Allergies": False}

# --- NAVIGATION FUNCTIONS ---
def go_to_scan(): st.session_state.page = 'scan'
def go_to_results(): st.session_state.page = 'results'
def go_back(): st.session_state.page = 'scan'
def toggle_condition(key):
    st.session_state.profile[key] = not st.session_state.profile[key]

# =========================================================
# PAGE 1: ONBOARDING (Health Profile)
# =========================================================
if st.session_state.page == 'onboarding':
    st.markdown("<h1 style='text-align: center;'>Satya Health 🌿</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Select your health profile to customize the AI.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Create a 2x2 Grid for buttons
    c1, c2 = st.columns(2)
    
    # Render Custom "Cards" as buttons
    with c1:
        if st.button(f"{'✅' if st.session_state.profile['Celiac'] else '⚪'} Celiac Disease", use_container_width=True):
            toggle_condition('Celiac')
            st.rerun()
            
        if st.button(f"{'✅' if st.session_state.profile['Lactose'] else '⚪'} Lactose Intolerant", use_container_width=True):
            toggle_condition('Lactose')
            st.rerun()

    with c2:
        if st.button(f"{'✅' if st.session_state.profile['Diabetes'] else '⚪'} Type 2 Diabetes", use_container_width=True):
            toggle_condition('Diabetes')
            st.rerun()
            
        if st.button(f"{'✅' if st.session_state.profile['Allergies'] else '⚪'} Nut/Soy Allergy", use_container_width=True):
            toggle_condition('Allergies')
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Continue Button
    if any(st.session_state.profile.values()):
        if st.button("Continue to Scanner ➡️", type="primary", use_container_width=True):
            go_to_scan()
            st.rerun()
    else:
        st.info("👆 Please select at least one condition to proceed.")


# =========================================================
# PAGE 2: SCANNER (The Input)
# =========================================================
elif st.session_state.page == 'scan':
    # Small header with 'Edit Profile' link
    c_back, c_title = st.columns([1,4])
    with c_back:
        if st.button("⬅️ Profile"):
            st.session_state.page = 'onboarding'
            st.rerun()
    with c_title:
        st.markdown("### Scan Product")

    # Active Profile Badge
    active_conditions = [k for k,v in st.session_state.profile.items() if v]
    st.caption(f"🛡️ Protecting: {', '.join(active_conditions)}")

    # Tabs
    t1, t2 = st.tabs(["📸 Camera/Upload", "🔗 Paste Link"])
    
    user_input = None
    
    with t1:
        img = st.file_uploader("Upload Back Label", type=['jpg','png','jpeg'])
        if img:
            st.image(img, width=150)
            if st.button("Analyze Image ✨", use_container_width=True):
                # Save temp file for agent
                with open("temp_scan.jpg", "wb") as f: f.write(img.getbuffer())
                st.session_state.scan_input = "temp_scan.jpg"
                go_to_results()
                st.rerun()

    with t2:
        url = st.text_input("Product URL")
        if url and st.button("Analyze Link ✨", use_container_width=True):
            st.session_state.scan_input = url
            go_to_results()
            st.rerun()


# =========================================================
# PAGE 3: RESULTS (The Verdict)
# =========================================================
elif st.session_state.page == 'results':
    st.button("⬅️ Scan Another", on_click=go_back)
    
    # Run the AI (Backend)
    # We reconstruct the profile string for the agent
    active_conditions = [k for k,v in st.session_state.profile.items() if v]
    profile_str = ", ".join(active_conditions)
    
    with st.spinner("🤖 Consulting Dr. Satya..."):
        # CALL BACKEND
        try:
            data = guardian_orchestrator(st.session_state.scan_input, profile_str)
            
            # PARSE DATA
            final_text = data['final_message']
            swarm = data.get('swarm_data', {})
            
            # --- 1. HERO VERDICT ---
            if "UNSAFE" in final_text.upper():
                st.markdown(f'<div class="hero-danger"><h1>🛑 UNSAFE</h1><p>{final_text}</p></div>', unsafe_allow_html=True)
            elif "RISK" in final_text.upper():
                st.markdown(f'<div class="hero-warning"><h1>⚠️ CAUTION</h1><p>{final_text}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="hero-safe"><h1>✅ SAFE TO EAT</h1><p>{final_text}</p></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

            # --- 2. CONDITION BREAKDOWN (Solving your UI issue) ---
            st.markdown("### 🧬 Impact on My Conditions")
            
            # Loop through active conditions and show specific agent results
            if st.session_state.profile['Celiac'] and 'celiac' in swarm:
                res = swarm['celiac']
                icon = "✅" if res.get('verdict') == "SAFE" else "🛑"
                st.markdown(f"""
                <div class="bento-box">
                    <strong>{icon} Celiac Analysis</strong><br>
                    <small>{res.get('reasoning', 'No specific data.')}</small>
                </div>""", unsafe_allow_html=True)

            if st.session_state.profile['Diabetes'] and 'metabolic' in swarm:
                res = swarm['metabolic']
                icon = "✅" if res.get('verdict') == "SAFE" else "⚠️"
                st.markdown(f"""
                <div class="bento-box">
                    <strong>{icon} Diabetes Analysis</strong><br>
                    <small>{res.get('reasoning', 'No specific data.')}</small>
                </div>""", unsafe_allow_html=True)

            # --- 3. INGREDIENT TAGS ---
            st.markdown("### 🧪 Ingredient Detection")
            ing_html = ""
            for ing in data['normalized_data']['ingredients']:
                color = "#fee2e2; color: #991b1b" if ing.get('risk_flags') else "#f1f5f9; color: #475569"
                ing_html += f"<span class='tag' style='background:{color}'>{ing['scientific_name']}</span>"
            
            st.markdown(f'<div class="bento-box">{ing_html}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Analysis Failed: {str(e)}")
            st.write("Please try scanning a clearer image.")