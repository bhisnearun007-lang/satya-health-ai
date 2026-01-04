import streamlit as st
import json
from guardian import guardian_orchestrator

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Satya-Health",
    page_icon="🌿",
    layout="wide"
)

# --- CUSTOM STYLING (Designer's Touch) ---
st.markdown("""
    <style>
    .main-header {font-size: 3rem; color: #2E7D32; font-weight: 700;}
    .sub-header {font-size: 1.2rem; color: #555;}
    .safe-box {background-color: #E8F5E9; padding: 20px; border-radius: 10px; border-left: 5px solid #2E7D32;}
    .danger-box {background-color: #FFEBEE; padding: 20px; border-radius: 10px; border-left: 5px solid #C62828;}
    .warning-box {background-color: #FFF3E0; padding: 20px; border-radius: 10px; border-left: 5px solid #EF6C00;}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: USER PROFILE (Memory Manager) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=100)
    st.title("My Health Passport")
    
    st.markdown("### 👤 User Profile")
    name = st.text_input("Name", "Arun")
    
    st.markdown("### 🧬 Conditions")
    is_celiac = st.checkbox("Celiac Disease (No Gluten)", value=True)
    is_diabetic = st.checkbox("Type 2 Diabetes", value=True)
    is_lactose = st.checkbox("Lactose Intolerance")
    has_nut_allergy = st.checkbox("Nut Allergy")
    
    # Build the profile string dynamically
    profile_list = []
    if is_celiac: profile_list.append("Celiac Disease")
    if is_diabetic: profile_list.append("Type 2 Diabetes")
    if is_lactose: profile_list.append("Lactose Intolerance")
    if has_nut_allergy: profile_list.append("Nut Allergy")
    
    user_profile = ", ".join(profile_list)
    
    st.info(f"**Active Profile:**\n{user_profile}")

# --- MAIN PAGE: THE INPUT ROUTER ---
st.markdown('<div class="main-header">Satya-Health 🌿</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your AI Food Safety Guardian for Indian Context</div>', unsafe_allow_html=True)
st.markdown("---")

# Tabs for different input types
tab1, tab2, tab3 = st.tabs(["🔗 Paste Link", "📸 Upload Image", "📝 Type Ingredients"])

user_input = None

with tab1:
    url_input = st.text_input("Paste product URL (BigBasket, Amazon, Blinkit):")
    if st.button("Analyze URL"):
        user_input = url_input

with tab2:
    uploaded_file = st.file_uploader("Upload photo of ingredients (Back of pack)", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None and st.button("Analyze Image"):
        # For this demo, we just pass the filename. 
        # In a real app, you'd save the file temporarily.
        user_input = uploaded_file.name 
        st.image(uploaded_file, caption="Product Scanned", width=300)

with tab3:
    text_input = st.text_area("Paste ingredient list here:")
    if st.button("Analyze Text"):
        user_input = text_input

# --- THE RESULTS SECTION ---
if user_input:
    with st.spinner("🤖 The Swarm is analyzing... (Normalizing -> Detecting Risks -> verifying)"):
        
        # CALL THE BACKEND
        result = guardian_orchestrator(user_input, user_profile)
        
        # 1. VISUALIZE THE VERDICT
        # We assume the AI returns "UNSAFE" or "SAFE" in the text.
        # Simple heuristic for color coding:
        final_text = result['final_message']
        
        if "UNSAFE" in final_text.upper():
            st.markdown(f'<div class="danger-box"><h3>🛑 UNSAFE DETECTED</h3>{final_text}</div>', unsafe_allow_html=True)
        elif "RISK" in final_text.upper() or "WARNING" in final_text.upper():
            st.markdown(f'<div class="warning-box"><h3>⚠️ PROCEED WITH CAUTION</h3>{final_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="safe-box"><h3>✅ LIKELY SAFE</h3>{final_text}</div>', unsafe_allow_html=True)

        st.divider()

        # 2. DESIGNER FEATURE: TRANSPARENCY (Show the "Why")
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("🔍 See Normalized Ingredients"):
                st.write("The AI found these ingredients:")
                # Display the raw data from the Normalizer Agent
                st.json(result['normalized_data'])

        with col2:
            with st.expander("🩺 Dr. Satya's Safety Report"):
                st.write("The Critique Agent reviewed this decision:")
                # Display the critique JSON
                st.json(result['critique_report'])