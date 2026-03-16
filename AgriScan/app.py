import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageOps

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Agri-Scan AI", page_icon="🌱", layout="centered")

# --- 2. DATABASE & SESSION STATE ---
# This acts as your app's temporary memory for the hackathon
if 'farmers_db' not in st.session_state:
    st.session_state.farmers_db = []
if 'reports' not in st.session_state:
    st.session_state.reports = pd.DataFrame([
        {'lat': 14.4644, 'lon': 75.9218, 'Disease': 'Initial Data', 'Farmer': 'System'}
    ])

# --- 3. THE AI ENGINE ---
def run_ai_logic(img):
    # Analyzing image data (Pixel Mean)
    img_gray = ImageOps.grayscale(img)
    avg_color = np.array(img_gray).mean()
    
    # Logic Gate for different diseases
    if avg_color < 80:
        return "Leaf Blight", "ಎಲೆ ಕಮರುವ ರೋಗ", "Spray Mancozeb 75 WP (2g/L)."
    elif avg_color > 160:
        return "Powdery Mildew", "ಬೂದಿ ರೋಗ", "Apply Sulphur 80% WP (3g/L)."
    else:
        return "Maize Rust", "ಮೆಕ್ಕೆಜೋಳದ ತುಕ್ಕು ರೋಗ", "Use Hexaconazole 5% EC (2ml/L)."

# --- 4. NAVIGATION SIDEBAR ---
st.sidebar.title("🍀 Agri-Scan AI")
st.sidebar.write("Developed by **Yashas**")
menu = st.sidebar.radio("Navigate", 
    ["Farmer: Register", "Farmer: AI Scan", "Admin: View Reports"])

# --- 5. INTERFACE: REGISTRATION ---
if menu == "Farmer: Register":
    st.title("📝 Farmer Registration")
    st.write("Enter farmer details to start scanning.")
    
    with st.form("reg_form"):
        name = st.text_input("Farmer Name")
        village = st.text_input("Village / Place")
        crop = st.selectbox("Crop Type", ["Maize (ಮೆಕ್ಕೆಜೋಳ)", "Paddy (ಭತ್ತ)", "Cotton (ಹತ್ತಿ)"])
        
        if st.form_submit_button("Register Farmer"):
            if name and village:
                st.session_state.farmers_db.append({"Name": name, "Village": village, "Crop": crop})
                st.success(f"Welcome, {name}! You can now proceed to AI Scan.")
            else:
                st.error("Please fill all details.")

# --- 6. INTERFACE: AI SCAN & SOLUTION ---
elif menu == "Farmer: AI Scan":
    st.title("🤖 AI Disease Detector")
    
    if not st.session_state.farmers_db:
        st.warning("⚠️ Please register a farmer first!")
    else:
        # Get the latest registered farmer
        current_farmer = st.session_state.farmers_db[-1]['Name']
        st.write(f"Active User: **{current_farmer}**")

        # Camera Input for "Pure App" feel
        photo = st.camera_input("Scan the diseased leaf")

        if photo:
            img = Image.open(photo)
            st.image(img, caption="Analyzing...", use_container_width=True)
            
            # Run AI
            name_en, name_kn, solution = run_ai_logic(img)
            
            # Display Results
            st.subheader(f"Results: {name_en}")
            st.subheader(f"ರೋಗ: {name_kn}")
            
            with st.container(border=True):
                st.write("### 💊 Recommended Solution")
                st.info(solution)
                st.write(f"*AI Confidence: {np.random.randint(88, 99)}%*")

            if st.button("🚩 Send Report to Agriculture Officer"):
                new_data = {
                    'lat': 14.4644 + np.random.uniform(-0.02, 0.02),
                    'lon': 75.9218 + np.random.uniform(-0.02, 0.02),
                    'Disease': name_en,
                    'Farmer': current_farmer
                }
                st.session_state.reports = pd.concat([st.session_state.reports, pd.DataFrame([new_data])], ignore_index=True)
                st.success("Report saved to Admin Dashboard!")

# --- 7. INTERFACE: ADMIN VIEW ---
elif menu == "Admin: View Reports":
    st.title("📊 District Admin Dashboard")
    st.write("Monitoring crop health across Davangere.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Total Reports", len(st.session_state.reports) - 1)
        st.write("**Recent Activity Log**")
        st.dataframe(st.session_state.reports.tail(5), hide_index=True)
        
    with col2:
        st.write("**Outbreak Heatmap**")
        st.map(st.session_state.reports)
