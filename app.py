import streamlit as st
import json
from guardian import guardian_orchestrator

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Satya-Health AI",
    page_icon="🌿",
    layout="centered", # 'Centered' looks more like a mobile app/modern tool than 'Wide'
    initial_sidebar_state="collapsed"
)

# --- 🎨 2025 MODERN UI CSS ---
st.markdown("""
    <style>
    /* GLOBAL FONTS & RESET */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8F9FA; /* Very soft grey background */
        color: #1A1A1A;
    }

    /* REMOVE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 🟢 HERO VERDICT CARDS (The "Verdict Part" you wanted fixed) */
    .verdict-card {
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        animation: fadeIn 0.8s ease-in-out;
    }
    
    /* UNSAFE STYLE (Modern Soft Red) */
    .unsafe {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        border: 2px solid #E57373;
        color: #C62828;
    }

    /* SAFE STYLE (Modern Mint/Teal) */
    .safe {
        background: linear-gradient(135deg, #E0F2F1 0%, #B2DFDB 100%);
        border: 2px solid #4DB6AC;
        color: #00695C;
    }

    /* RISKY STYLE (Soft Amber) */
    .risky {
        background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
        border: 2px solid #FFD54F;
        color: #F57F17;
    }

    .verdict-icon { font-size: 80px; display: block; margin-bottom: 10px; }
    .verdict-title { font-size: 32px; font-weight: 800; letter-spacing: -1px; margin: 0;}
    .verdict-desc { font-size: 18px; font-weight: 500; opacity: 0.9; margin-top: 10px; }

    /* 🍱 BENTO GRID CARDS (For Details) */
    .bento-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        border: 1px solid #F0F0F0;
        height: 100%;
    }
    .card-header { font-weight: 600; color: #555; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; }

    /* INPUT AREA STYLING */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        padding: 12px;
    }
    
    /* CUSTOM BUTTON */
    .stButton > button {
        background: #1A1A1A;
        color: white;
        border-radius: 12px;
        padding: 10px 25px;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: transform 0.1s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        background: #333;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Minimalist Profile) ---
with st.sidebar:
    st.markdown("## 👤 **My Health ID**")
    st.markdown("---")
    
    # Using columns for a tighter layout
    name = st.text_input("Name", "Arun")
    
    st.markdown("#### 🧬 My Conditions")
    # Modern "Tag" style layout? Streamlit checkboxes are limited, but we stick to clean checkmarks
    is_celiac = st.checkbox("🚫 Celiac (No Gluten)", value=True)
    is_diabetic = st.checkbox("🩸 Type 2 Diabetes", value=True)
    is_lactose = st.checkbox("🥛 Lactose Intolerance")
    has_nut_allergy = st.checkbox("🥜 Nut Allergy")
    
    # Dynamic Profile String
    profile_list = []
    if is_celiac: profile_list.append("Celiac Disease")
    if is_diabetic: profile_list.append("Type 2 Diabetes")
    if is_lactose: profile_list.append("Lactose Intolerance")
    if has_nut_allergy: profile_list.append("Nut Allergy")
    user_profile = ", ".join(profile_list)

# --- MAIN HERO SECTION ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=80) # Leaf Icon
with col2:
    st.markdown("<h1 style='margin-top: -10px;'>Satya-Health</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; margin-top: -15px;'>Your Personal AI Food Safety Guardian</p>", unsafe_allow_html=True)

st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True) # Spacer

# --- INPUT SECTION (Clean Tabs) ---
# We hide the default tab borders via CSS to make it look floating
tab_scan, tab_text, tab_link = st.tabs(["📸 Scan Label", "📝 Paste Ingredients", "🔗 Product Link"])

user_input = None
input_type_display = ""

with tab_scan:
    st.markdown("##### Upload a clear photo of the **Back Label**")
    uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Label Preview", width=150)
        
        if st.button("Analyze Scan", key="btn_scan"):
            
            # --- NEW CODE: SAVE TEMP FILE ---
            # We save the file locally so the Vision Agent can open it
            with open("temp_image.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            user_input = "temp_image.jpg" # Pass the filename, not the object
            input_type_display = "Scan"

with tab_text:
    text_val = st.text_area("Paste ingredients here:", height=100)
    if st.button("Check Ingredients", key="btn_text"):
        user_input = text_val
        input_type_display = "Text"

with tab_link:
    url_val = st.text_input("Paste product URL:")
    if st.button("Analyze Link", key="btn_link"):
        user_input = url_val
        input_type_display = "Link"

# --- 🚀 EXECUTION & UI RENDER ---
if user_input:
    st.markdown("---")
    
    # 1. LOADING STATE (Modern Spinner)
    with st.spinner(f"🔍 AI Swarm is analyzing your {input_type_display}..."):
        
        # CALL THE BRAIN
        # Note: Ensure guardian.py is returning the dictionary we set up in Step 1
        result = guardian_orchestrator(user_input, user_profile)
        
        final_msg = result['final_message']
        critique_data = result['critique_report']
        normalized_data = result['normalized_data']
        
        # 2. DETERMINE STATUS & STYLE
        status_class = "safe"
        icon = "✅"
        title = "LIKELY SAFE"
        
        lower_msg = final_msg.lower()
        if "unsafe" in lower_msg or "avoid" in lower_msg or "risk" in lower_msg:
            status_class = "unsafe"
            icon = "🛑"
            title = "UNSAFE TO EAT"
        elif "warning" in lower_msg or "caution" in lower_msg:
            status_class = "risky"
            icon = "⚠️"
            title = "PROCEED WITH CAUTION"

    # 3. HERO VERDICT CARD (The Big Visual)
    html_card = f"""
    <div class="verdict-card {status_class}">
        <span class="verdict-icon">{icon}</span>
        <h2 class="verdict-title">{title}</h2>
        <p class="verdict-desc">{final_msg}</p>
    </div>
    """
    st.markdown(html_card, unsafe_allow_html=True)

    # 4. BENTO GRID DETAILS (Safety Check + Ingredients)
    c1, c2 = st.columns(2)
    
    with c1:
        # DOCTOR'S NOTE CARD
        with st.container():
            st.markdown(f"""
            <div class="bento-card">
                <div class="card-header">🩺 Dr. Satya's Safety Check</div>
                <div style="font-size: 14px; color: #444; line-height: 1.6;">
                    {critique_data.get('critique_reason', 'Analysis Complete.')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with c2:
        # DETECTED INGREDIENTS CARD
        # We process the list to make it look like "Tags"
        ing_list = normalized_data.get('ingredients', [])
        ing_html = ""
        for item in ing_list[:5]: # Show top 5
            risk_style = "color: #D32F2F; background: #FFEBEE;" if item.get('risk_flags') else "color: #388E3C; background: #E8F5E9;"
            ing_html += f"<span style='display: inline-block; padding: 4px 10px; margin: 4px; border-radius: 20px; font-size: 12px; font-weight: 600; {risk_style}'>{item['scientific_name']}</span>"
        
        st.markdown(f"""
        <div class="bento-card">
            <div class="card-header">🧪 Detected Ingredients</div>
            {ing_html}
            <br><br>
            <small style="color: #888;">+ {max(0, len(ing_list)-5)} more detected</small>
        </div>
        """, unsafe_allow_html=True)

    # 5. EXPANDABLE DEEP DIVE (For nerds who want JSON)
    with st.expander("🔍 View Full Forensic Analysis"):
        st.json(result)