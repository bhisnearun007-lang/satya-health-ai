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

# --- 🎨 THEME-ADAPTIVE CSS ENGINE ---
st.markdown("""
    <style>
    /* 1. DEFINE COLOR PALETTES (CSS Variables) */
    :root {
        /* LIGHT MODE (Default) */
        --app-bg: radial-gradient(circle at 10% 20%, #f8fafc 0%, #f1f5f9 90%);
        --card-bg: #ffffff;
        --text-main: #0f172a;
        --text-sub: #64748b;
        --border-color: #e2e8f0;
        --shadow: 0 4px 20px rgba(0,0,0,0.05);
        
        /* Status Colors (Light) */
        --safe-bg: #dcfce7; --safe-text: #14532d; --safe-border: #86efac;
        --risk-bg: #fef3c7; --risk-text: #78350f; --risk-border: #fcd34d;
        --danger-bg: #fee2e2; --danger-text: #7f1d1d; --danger-border: #fca5a5;
        
        /* Tag Colors (Light) */
        --tag-bg-neutral: #f1f5f9; --tag-text-neutral: #475569;
        --tag-bg-risk: #fee2e2; --tag-text-risk: #991b1b;
    }

    /* DARK MODE OVERRIDES (System Preference) */
    @media (prefers-color-scheme: dark) {
        :root {
            --app-bg: radial-gradient(circle at 10% 20%, #0f172a 0%, #020617 90%);
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --border-color: #334155;
            --shadow: 0 4px 20px rgba(0,0,0,0.4);

            /* Status Colors (Dark - Deep & Glowing) */
            --safe-bg: rgba(20, 83, 45, 0.4); --safe-text: #4ade80; --safe-border: #14532d;
            --risk-bg: rgba(120, 53, 15, 0.4); --risk-text: #fbbf24; --risk-border: #78350f;
            --danger-bg: rgba(127, 29, 29, 0.4); --danger-text: #f87171; --danger-border: #7f1d1d;
            
            /* Tag Colors (Dark) */
            --tag-bg-neutral: #334155; --tag-text-neutral: #e2e8f0;
            --tag-bg-risk: #7f1d1d; --tag-text-risk: #fca5a5;
        }
    }

    /* 2. APPLY VARIABLES TO ELEMENTS */
    
    .stApp {
        background: var(--app-bg);
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }
    
    h1, h2, h3, h4, strong { color: var(--text-main) !important; }
    p, small, .caption { color: var(--text-sub) !important; }

    header, footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    /* CARDS */
    .condition-card-active {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white !important;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.3);
        border: 2px solid transparent;
        transition: transform 0.2s;
    }
    .condition-card-active strong { color: white !important; }
    
    .condition-card-inactive {
        background: var(--card-bg);
        color: var(--text-sub);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        border: 2px solid var(--border-color);
        box-shadow: var(--shadow);
        transition: transform 0.2s;
    }

    /* HERO VERDICTS */
    .hero-safe { background: var(--safe-bg); color: var(--safe-text); border: 1px solid var(--safe-border); border-radius: 20px; padding: 30px; text-align: center; }
    .hero-safe h1 { color: var(--safe-text) !important; }
    .hero-safe p { color: var(--safe-text) !important; opacity: 0.9; }

    .hero-danger { background: var(--danger-bg); color: var(--danger-text); border: 1px solid var(--danger-border); border-radius: 20px; padding: 30px; text-align: center; }
    .hero-danger h1 { color: var(--danger-text) !important; }
    .hero-danger p { color: var(--danger-text) !important; opacity: 0.9; }

    .hero-warning { background: var(--risk-bg); color: var(--risk-text); border: 1px solid var(--risk-border); border-radius: 20px; padding: 30px; text-align: center; }
    .hero-warning h1 { color: var(--risk-text) !important; }
    .hero-warning p { color: var(--risk-text) !important; opacity: 0.9; }

    /* BENTO BOX DETAILS */
    .bento-box {
        background: var(--card-bg);
        padding: 20px;
        border-radius: 16px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        margin-bottom: 15px;
    }

    /* TAGS */
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    .tag-neutral { background: var(--tag-bg-neutral); color: var(--tag-text-neutral); }
    .tag-risk { background: var(--tag-bg-risk); color: var(--tag-text-risk); }

    /* BUTTON OVERRIDES */
    .stButton > button {
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 'onboarding'
if 'profile' not in st.session_state: 
    st.session_state.profile = {"Celiac": False, "Diabetes": False, "Lactose": False, "Allergies": False}
if 'scan_input' not in st.session_state: st.session_state.scan_input = None

# --- NAVIGATION ---
def go_to_scan(): st.session_state.page = 'scan'
def go_to_results(): st.session_state.page = 'results'
def go_back(): st.session_state.page = 'scan'
def toggle_condition(key):
    st.session_state.profile[key] = not st.session_state.profile[key]

# =========================================================
# PAGE 1: ONBOARDING (Profile Setup)
# =========================================================
if st.session_state.page == 'onboarding':
    st.markdown("<h1 style='text-align: center;'>Satya Health 🌿</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Select your health profile to customize the AI.</p>", unsafe_allow_html=True)
    st.markdown("---")

    c1, c2 = st.columns(2)
    
    # Helper to render card-like buttons using HTML for style + Streamlit for Logic? 
    # Streamlit buttons are hard to style perfectly inside, so we use logic on click.
    # We visually swap classes based on state.
    
    with c1:
        # Celiac Card
        state_class = "condition-card-active" if st.session_state.profile['Celiac'] else "condition-card-inactive"
        icon = "✅" if st.session_state.profile['Celiac'] else "🍞"
        st.markdown(f"""<div class="{state_class}"><h2>{icon}</h2><strong>Celiac</strong></div>""", unsafe_allow_html=True)
        if st.button("Toggle Celiac", key="btn_celiac", use_container_width=True):
            toggle_condition('Celiac')
            st.rerun()

        # Lactose Card
        state_class = "condition-card-active" if st.session_state.profile['Lactose'] else "condition-card-inactive"
        icon = "✅" if st.session_state.profile['Lactose'] else "🥛"
        st.markdown(f"""<div class="{state_class}"><h2>{icon}</h2><strong>Lactose</strong></div>""", unsafe_allow_html=True)
        if st.button("Toggle Lactose", key="btn_lactose", use_container_width=True):
            toggle_condition('Lactose')
            st.rerun()

    with c2:
        # Diabetes Card
        state_class = "condition-card-active" if st.session_state.profile['Diabetes'] else "condition-card-inactive"
        icon = "✅" if st.session_state.profile['Diabetes'] else "🩸"
        st.markdown(f"""<div class="{state_class}"><h2>{icon}</h2><strong>Diabetes</strong></div>""", unsafe_allow_html=True)
        if st.button("Toggle Diabetes", key="btn_diabetes", use_container_width=True):
            toggle_condition('Diabetes')
            st.rerun()
            
        # Allergy Card
        state_class = "condition-card-active" if st.session_state.profile['Allergies'] else "condition-card-inactive"
        icon = "✅" if st.session_state.profile['Allergies'] else "🥜"
        st.markdown(f"""<div class="{state_class}"><h2>{icon}</h2><strong>Allergy</strong></div>""", unsafe_allow_html=True)
        if st.button("Toggle Allergy", key="btn_allergy", use_container_width=True):
            toggle_condition('Allergies')
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    if any(st.session_state.profile.values()):
        if st.button("Continue to Scanner ➡️", type="primary", use_container_width=True):
            go_to_scan()
            st.rerun()
    else:
        st.info("👆 Tap a card above to activate a condition.")

# =========================================================
# PAGE 2: SCANNER
# =========================================================
elif st.session_state.page == 'scan':
    c_back, c_title = st.columns([1,4])
    with c_back:
        if st.button("⬅️ Profile"):
            st.session_state.page = 'onboarding'
            st.rerun()
    with c_title:
        st.markdown("### Scan Product")

    # Dynamic "Active Profile" tags
    active_conditions = [k for k,v in st.session_state.profile.items() if v]
    st.markdown(f"<small>🛡️ Protection Active: {', '.join(active_conditions)}</small>", unsafe_allow_html=True)

    t1, t2 = st.tabs(["📸 Camera/Upload", "🔗 Paste Link"])
    
    with t1:
        img = st.file_uploader("Upload Back Label", type=['jpg','png','jpeg'])
        if img:
            st.image(img, width=150)
            if st.button("Analyze Image ✨", use_container_width=True):
                with open("temp_scan.jpg", "wb") as f: f.write(img.getbuffer())
                st.session_state.scan_input = "temp_scan.jpg"
                go_to_results()
                st.rerun()

    with t2:
        url = st.text_input("Product URL (Amazon/Blinkit)")
        if url and st.button("Analyze Link ✨", use_container_width=True):
            st.session_state.scan_input = url
            go_to_results()
            st.rerun()

# =========================================================
# PAGE 3: RESULTS
# =========================================================
elif st.session_state.page == 'results':
    st.button("⬅️ Scan Another", on_click=go_back)
    
    active_conditions = [k for k,v in st.session_state.profile.items() if v]
    profile_str = ", ".join(active_conditions)
    
    with st.spinner("🤖 Consulting Dr. Satya..."):
        try:
            # CALL BACKEND
            data = guardian_orchestrator(st.session_state.scan_input, profile_str)
            
            final_text = data['final_message']
            swarm = data.get('swarm_data', {})
            
            # 1. HERO VERDICT (Theme-Aware)
            if "UNSAFE" in final_text.upper():
                st.markdown(f'<div class="hero-danger"><h1>🛑 UNSAFE</h1><p>{final_text}</p></div>', unsafe_allow_html=True)
            elif "RISK" in final_text.upper():
                st.markdown(f'<div class="hero-warning"><h1>⚠️ CAUTION</h1><p>{final_text}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="hero-safe"><h1>✅ SAFE TO EAT</h1><p>{final_text}</p></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

            # 2. CONDITION BREAKDOWN
            st.markdown("### 🧬 Impact Analysis")
            
            if st.session_state.profile['Celiac'] and 'celiac' in swarm:
                res = swarm['celiac']
                icon = "✅" if res.get('verdict') == "SAFE" else "🛑"
                st.markdown(f"""
                <div class="bento-box">
                    <strong>{icon} Celiac Report</strong><br>
                    <small>{res.get('reasoning', 'Analysis pending.')}</small>
                </div>""", unsafe_allow_html=True)

            if st.session_state.profile['Diabetes'] and 'metabolic' in swarm:
                res = swarm['metabolic']
                icon = "✅" if res.get('verdict') == "SAFE" else "⚠️"
                st.markdown(f"""
                <div class="bento-box">
                    <strong>{icon} Diabetes Report</strong><br>
                    <small>{res.get('reasoning', 'Analysis pending.')}</small>
                </div>""", unsafe_allow_html=True)

            # 3. INGREDIENT TAGS (Theme-Aware)
            st.markdown("### 🧪 Ingredients Detected")
            ing_html = ""
            for ing in data['normalized_data']['ingredients']:
                # Logic: If risky, use risk tag class. Else neutral tag class.
                tag_class = "tag-risk" if ing.get('risk_flags') else "tag-neutral"
                ing_html += f"<span class='tag {tag_class}'>{ing['scientific_name']}</span>"
            
            st.markdown(f'<div class="bento-box">{ing_html}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Analysis Failed: {str(e)}")
            st.write("Please check your image or internet connection.")